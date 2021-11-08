import numpy as np
timesteps=8; data_dim=16
x_train = np.random.random((10, timesteps, data_dim))
print(x_train.shape)
print(x_train[-1])
# sns.set()
# Candledf=pd.read_csv('../result.dat',low_memory=False)
# Candledf['ndatetime']=pd.to_datetime(Candledf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')


