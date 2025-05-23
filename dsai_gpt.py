from ollama import generate
import pandas as pd
import numpy as np
import os
import re
import json
import datetime
import logging
from typing import Dict, Optional

# 配置日志
logging.basicConfig(filename='trading.log', level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

class DataProcessor:
    """数据预处理引擎"""
    def __init__(self, data_paths: list):
        self.data_paths = data_paths
        self._load_data()
    
    def _load_data(self) -> pd.DataFrame:
        """加载并合并数据"""
        dfs = []
        for path in self.data_paths:
            df = pd.read_csv(f'data/{path}', names=["ndatetime","nbid","nask","close","volume","deal"])
            df['ndatetime'] = pd.to_datetime(df['ndatetime'],format="mixed")
            dfs.append(df)
        self.raw_data = pd.concat(dfs).sort_values('ndatetime')
        return self.raw_data
    
    def resample_data(self) -> pd.DataFrame:
        """重采样并计算技术指标"""
        # 1分钟重采样
        daymin = self.raw_data.resample('1min', on='ndatetime').agg({
            'close': ['first','max','min','last'],
            'volume': 'sum',
            'deal': 'sum'
        })
        daymin.columns = ['open','high','low','close','volume','deal']
        
        # 技术指标计算
        daymin['avgline'] = daymin['close'].rolling(20).mean()
        daymin['dealminus'] = daymin['deal'].rolling(5).sum().diff()
        
        # 计算ATR(平均真实波幅)
        high_low = daymin['high'] - daymin['low']
        high_close = np.abs(daymin['high'] - daymin['close'].shift())
        low_close = np.abs(daymin['low'] - daymin['close'].shift())
        daymin['TR'] = np.maximum.reduce([high_low, high_close, low_close])
        daymin['ATR'] = daymin['TR'].rolling(14).mean()
        
        return daymin.dropna()

class RiskManager:
    """多级风控系统"""
    def __init__(self):
        self.base_stoploss = -14000      # 基础止损
        self.risk_ratio = 0.02           # 账户风险比例
        self.max_holding_time = 30       # 最大持仓时间(分钟)
    
    def calculate_dynamic_stop(self, 
                             position: int, 
                             entry_price: float,
                             current_price: float,
                             account_balance: float,
                             atr: float) -> float:
        """动态止损计算"""
        # 波动率止损
        volatility_stop = -3 * atr * abs(position) * 200
        
        # 账户比例止损
        ratio_stop = -account_balance * self.risk_ratio
        
        # 取最严格止损
        return max(self.base_stoploss, volatility_stop, ratio_stop)
    
    def check_conditions(self,
                       floating_pnl: float,
                       position: int,
                       entry_time: datetime.datetime) -> Optional[str]:
        """多级风控检查"""
        conditions = []
        
        # 硬止损
        if floating_pnl <= self.base_stoploss:
            conditions.append("硬止损")
        
        # 持仓时间检查
        if position != 0:
            holding_time = (datetime.datetime.now() - entry_time).total_seconds() // 60
            if holding_time > self.max_holding_time:
                conditions.append("时间止损")
        
        return conditions if conditions else None

class TradingCore:
    """交易核心引擎"""
    def __init__(self):
        self.position = 0
        self.entry_price = 0.0
        self.entry_time = None
        self.total_profit = 0.0
        self.total_fee = 0
        self.max_position = 2
        
        # 风控系统
        self.risk_mgr = RiskManager()
        
        # 交易记录
        self.trade_log = pd.DataFrame(columns=[
            "open_time","open_price","position",
            "close_time","close_price","pnl"
        ])
    
    def calculate_floating(self, current_price: float) -> float:
        """计算浮动盈亏"""
        if self.position == 0:
            return 0.0
        
        contract_value = 200
        fee = 200 * (abs(self.position) + (1 if self.position !=0 else 0))
        raw_profit = (current_price - self.entry_price) * self.position * contract_value
        return raw_profit - fee
    
    def execute_action(self, action: str, price: float, timestamp: datetime.datetime):
        """执行交易动作"""
        original_position = self.position
        
        try:
            if action == "Buy":
                if self.position >= self.max_position:
                    return
                self.position += 1
                self._update_entry_price(price, 'long')
                
            elif action == "Sell":
                if self.position <= -self.max_position:
                    return
                self.position -= 1
                self._update_entry_price(price, 'short')
                
            elif action == "StopLoss":
                self.close_all(price, timestamp)
                
            # 记录开仓
            if original_position == 0 and self.position !=0:
                self.entry_time = timestamp
                new_trade = {
                    "open_time": timestamp,
                    "open_price": price,
                    "position": self.position
                }
                self.trade_log = pd.concat([self.trade_log, pd.DataFrame([new_trade])], ignore_index=True)
                
        except Exception as e:
            logging.error(f"交易执行失败: {str(e)}")
            self.position = original_position  # 回滚仓位
    
    def _update_entry_price(self, price: float, direction: str):
        """更新持仓均价"""
        if direction == 'long':
            total = self.entry_price * self.position + price
            self.entry_price = total / (self.position +1)
        else:
            total = self.entry_price * abs(self.position) + price
            self.entry_price = total / (abs(self.position) +1)
    
    def close_all(self, price: float, timestamp: datetime.datetime):
        """全平仓"""
        if self.position == 0:
            return
            
        pnl = self.calculate_floating(price)
        self.total_profit += pnl
        
        # 更新交易记录
        idx = self.trade_log[self.trade_log['close_time'].isna()].index
        if len(idx) >0:
            self.trade_log.loc[idx[-1], ['close_time','close_price','pnl']] = [
                timestamp, price, pnl
            ]
        
        self.position = 0
        self.entry_price = 0.0
        self.entry_time = None

class DeepseekTrader:
    """交易系统主类"""
    def __init__(self):
        self.data_engine = DataProcessor(self._get_data_files())
        self.trading_core = TradingCore()
        self.model_name = "deepseek-r1:1.5b"
        
    def _get_data_files(self) -> list:
        """获取数据文件列表"""
        all_files = os.listdir("data")
        pattern = re.compile(r'Ticks2025-05-\w+\.txt')
        return [f for f in all_files if pattern.match(f)]
    
    def _build_prompt(self, data_point: Dict) -> str:
        """生成动态提示词"""
        trading_state = {
            'position': self.trading_core.position,
            'entry_price': self.trading_core.entry_price,
            'floating': self.trading_core.calculate_floating(data_point['close'])
        }
        
        return f"""
        [期货当冲AI] 综合以下实时数据生成操作指令：
        {{
            "时间": "{data_point['ndatetime']}",
            "价格": {{
                "开": {data_point['open']},
                "高": {data_point['high']},
                "低": {data_point['low']},
                "收": {data_point['close']}
            }},
            "指标": {{
                "均线20": {data_point['avgline']:.2f},
                "ATR": {data_point['ATR']:.2f},
                "多空力道": {data_point['dealminus']}
            }},
            "持仓": {{
                "数量": {trading_state['position']},
                "浮盈": {trading_state['floating']:.0f}
            }},
            "风控": {{
                "当前止损点": {self.trading_core.risk_mgr.base_stoploss},
                "动态止损": {self._current_dynamic_stop(data_point)}
            }}
        }}
        
        ***强制规则：
        1. 浮盈 ≤ 动态止损 → StopLoss
        2. 持仓时间 >30分钟 → StopLoss
        3. 13:40后强制平仓
        """
    
    def _current_dynamic_stop(self, data_point) -> float:
        """计算当前动态止损"""
        return self.trading_core.risk_mgr.calculate_dynamic_stop(
            self.trading_core.position,
            self.trading_core.entry_price,
            data_point['close'],
            self.trading_core.total_profit,
            data_point['ATR']
        )
    
    def run_backtest(self):
        """回测运行"""
        data = self.data_engine.resample_data()
        
        for (idx, tick) in data.iterrows():
            # 强制平仓时间检查
            print(tick)
            if tick['ndatetime'].time() >= datetime.time(13,40):
                self.trading_core.close_all(tick['close'], tick['ndatetime'])
                continue
                
            # 风控检查
            stop_conditions = self.trading_core.risk_mgr.check_conditions(
                self.trading_core.calculate_floating(tick['close']),
                self.trading_core.position,
                self.trading_core.entry_time
            )
            if stop_conditions:
                logging.info(f"触发风控条件: {', '.join(stop_conditions)}")
                self.trading_core.close_all(tick['close'], tick['ndatetime'])
                continue
                
            # 生成模型决策
            prompt = self._build_prompt(tick)
            response = generate(
                model=self.model_name,
                prompt=prompt,
                options={'temperature':0.2, 'num_predict':20},
                format="json"
            )
            
            # 解析决策
            action = self._parse_response(response)
            
            # 执行交易
            self.trading_core.execute_action(action, tick['close'], tick['ndatetime'])
            
    def _parse_response(self, response: str) -> str:
        """防御性解析响应"""
        try:
            cleaned = response['response'].strip().replace("'",'"')
            if not cleaned.startswith('{'):
                cleaned = '{' + cleaned.split('{',1)[-1]
            if not cleaned.endswith('}'):
                cleaned = cleaned.split('}',1)[0] + '}'
            return json.loads(cleaned).get('operation','Hold')
        except Exception as e:
            logging.warning(f"解析失败: {str(e)}")
            return "Hold"

if __name__ == "__main__":
    trader = DeepseekTrader()
    trader.run_backtest()
    
    # 输出结果
    print("\n=== 回测结果 ===")
    print(f"总盈亏: {trader.trading_core.total_profit:.0f}")
    print(f"交易次数: {len(trader.trading_core.trade_log)}")
    print(f"多空比: {trader.trading_core.trade_log['position'].value_counts().to_dict()}")
    trader.trading_core.trade_log.to_csv('trading_log.csv', index=False)