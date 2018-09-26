class dataprocess:
    def __init__(self,type,name):
        self.name=name
        self.type=type
        self.selftickpd=pd.DataFrame(columns=['date','time','bid','ask','close','volume'])
        