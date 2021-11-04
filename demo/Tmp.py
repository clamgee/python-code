import tensorflow as tf
tf_vr1 = tf.Variable([1,2,3,4])
a = 10
tf_vr1=tf.multiply(tf_vr1, a)
print(tf_vr1)

# sns.set()
# Candledf=pd.read_csv('../result.dat',low_memory=False)
# Candledf['ndatetime']=pd.to_datetime(Candledf['ndatetime'],format='%Y-%m-%d %H:%M:%S.%f')


