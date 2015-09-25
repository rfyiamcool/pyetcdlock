#coding:utf-8
import etcd
import uuid
import threading

class Lock(object):

    def __init__(self, client, key, ttl=60, renewSecondsPrior=5, timeout=None):
        if not isinstance(client, etcd.Client):
            raise ValueError("A python-etcd Client must be provided")
        if key is None or key is '':
            raise ValueError("A etcd key must be specified")
        if ttl is None or ttl <= 0:
            raise ValueError("ttl >0")
        if renewSecondsPrior is not None:
            if not isinstance(renewSecondsPrior, int) or renewSecondsPrior < 0:
                raise ValueError("A positive prior renew must be specified, or None to not renew")
            if ttl - renewSecondsPrior < 1:
                raise ValueError("lock at least 2 seconds")

        self.client = client
        if not key.startswith('/'):
            key = '/' + key
        self.key = key
        self.ttl = ttl
        self.renewSecondsPrior = renewSecondsPrior
        self._index = None
        self.token = None
        self.timeout = timeout
        threading.Thread(target=self.watch_key).start()

    def watch_key():
        for event in self.client.eternal_watch(self.key,recursive = True):
            if event.action == "expire":
                self.client.write(self.key,self.token,ttl=0)
                self.token = None
                

    def __enter__(self):
        return self.acquire()

    def __exit__(self, type, value, traceback):
        return self.release()

    def force_acquire(self):
        self.client.write(self.key,self.token,ttl=0)
        self.token = None

    def acquire(self, **kwargs):
        token = str(uuid.uuid4())
        attempted = False
        while self.token is None:
            try:
                self.client.test_and_set(self.key, token, "0", ttl=self.ttl)
                self.token = token
            except etcd.EtcdKeyNotFound, e:
                try:
                    self.client.write(self.key, token, prevExist=False, recursive=True, ttl=self.ttl)
                    self.token = token
                except etcd.EtcdAlreadyExist, e:
                    pass 
            except ValueError, e:
                if 'timeout' in kwargs or self.timeout is not None:
                    if attempted is True: return False
                    kwargs.setdefault("timeout", self.timeout)
                    try:
                        self.client.read(self.key, wait=True, timeout=kwargs["timeout"])
                        attempted = True
                    except etcd.EtcdException, e:
                        return False
                else:
                    self.client.watch(self.key)

        if self.renewSecondsPrior is not None:
            def renew():
                if (self.renew()):
                    threading.Timer(self.ttl, self.renew)
            threading.Timer(self.ttl - self.renewSecondsPrior, lambda: self.renew())
        else:
            def cleanup():
                if self.token is token:
                    self.token = None
            threading.Timer(self.ttl, cleanup)

        return True

    def renew(self,ttl=None):
        ttl = ttl if ttl else self.ttl 
        if (self.token is not None):
            try:
                self.client.test_and_set(self.key, self.token, self.token, ttl=ttl)
                return True
            except ValueError, e:
                self.token = None
                return False

    def is_locked(self):
        return self.token is not None

    def release(self):
        if (self.token is not None):
            try:
                self.client.test_and_set(self.key, 0, self.token)
            except (ValueError, etcd.EtcdKeyError, etcd.EtcdKeyNotFound) as e:
                pass 
            finally:
                self.token = None
