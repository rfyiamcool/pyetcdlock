#pyetcdlock

基于etcd的分布式锁，简单说就是利用etcd.test_and_set函数来判断lock key是否被占用，存在那就说明有人占用。在创建key的时候加入了ttl，防止因为进程异常退出而没有释放锁。

to do list:

加入watch机制，因为etcdlock没有zookeeper那种临时节点的概念，需要我们来处理

### 安装方法

```
git clone https://github.com/rfyiamcool/pyetcdlock.git
cd pyetcdlock
python setup.py
```

```
pip instlal pyetcdlock
```

模块说明:

ttl     : expire过期时间,这样可以指定锁定的时间

renew   : 如果你的ttl时间将要过期了，那么可以使用renew(),再加点锁定的ttl时间

force_acquire : 强制获取锁


### 创建连接

```
import etcd
from pyetcdnetlock import Lock

client = client = etcd.Client(host='127.0.0.1')
lock = Lock(client, 'path/to/my/key', ttl=30, renewSecondsPrior=5)
```

###  使用方法

```
if lock.acquire(timeout=20):
    # some work
    lock.renew()
    # some other work
    lock.release() 
else
    # failed to acquire the lock in 20 seconds
    pass

```

OR

```
with lock as l:
    #如果时间不够，可以用renew()参数，加点时间
    l.renew()
    # some other work
```

