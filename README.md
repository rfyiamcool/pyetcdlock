### 创建连接

ttl是expire过期时间,这样可以指定锁定的时间
renew是再加点锁定的ttl时间

```python
import etcd
from pyetcdnetlock import Lock

client = client = etcd.Client(host='127.0.0.1')
lock = Lock(client, 'path/to/my/key', ttl=30, renewSecondsPrior=5)
```

###  使用方法

```
if lock.acquire(timeout=20):
    t = Thread(target=someheavywork)
    t.run()
    t.wait()
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
