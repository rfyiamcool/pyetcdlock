#pyetcdlock

基于etcd的分布式锁，简单说就是利用etcd.test_and_set函数来判断lock key是否被占用，存在那就说明有人占用。在创建key的时候加入了ttl，防止因为进程异常退出而没有释放锁。

更新:
支持指定renew时间
```
renew(ttl=3)
```

待修复的问题:

针对etcd key 加入watch机制,解决客户端意外退出没有释放锁的问题.


**曾经写过关于分布式互斥锁的文章:**

zookeeper:
[http://xiaorui.cc/2015/04/09/python-zookeeper%E8%A7%A3%E5%86%B3redis%E5%81%9A%E5%88%86%E5%B8%83%E5%BC%8F%E9%94%81%E5%B8%A6%E6%9D%A5%E7%9A%84%E5%9D%91/](http://xiaorui.cc/2015/04/09/python-zookeeper%E8%A7%A3%E5%86%B3redis%E5%81%9A%E5%88%86%E5%B8%83%E5%BC%8F%E9%94%81%E5%B8%A6%E6%9D%A5%E7%9A%84%E5%9D%91/) 

redis:
[http://xiaorui.cc/2014/12/19/python%E4%BD%BF%E7%94%A8redis%E5%AE%9E%E7%8E%B0%E5%8D%8F%E5%90%8C%E6%8E%A7%E5%88%B6%E7%9A%84%E5%88%86%E5%B8%83%E5%BC%8F%E9%94%81/](http://xiaorui.cc/2014/12/19/python%E4%BD%BF%E7%94%A8redis%E5%AE%9E%E7%8E%B0%E5%8D%8F%E5%90%8C%E6%8E%A7%E5%88%B6%E7%9A%84%E5%88%86%E5%B8%83%E5%BC%8F%E9%94%81/)

### 安装方法

```
git clone https://github.com/rfyiamcool/pyetcdlock.git
cd pyetcdlock
python setup.py
```

pypi的安装方式 (话说，pypi有些问题，你在pypi search搜东西的时候，不显示详细信息)

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

