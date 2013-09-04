'''
Created on Aug 29, 2013

@author: root
'''

import calendar
import datetime


from oslo.config import cfg

memcache_opts = [
                 cfg.ListOpt('memcached_servers',
                             default=None,
                             help='Memcached servers or None for in process cache')
                 ]

CONF = cfg.CONF
CONF.register_opts(memcache_opts)


def get_client():
    client_cls = Client
    
    if CONF.memcached_servers:
        import memcache
        client_cls = memcache.Client
    
    return client_cls(CONF.memcached_servers, debug=0)
    

class Client(object):

    def __init__(self, *args, **kwargs):
        """Ignores the passed in args."""
        self.cache = {}

    def get(self, key):
        """Retrieves the value for a key or None.

        this expunges expired keys during each get"""

        for k in self.cache.keys():
            (timeout, _value) = self.cache[k]
            if timeout and calendar.timegm(datetime.datetime.utcnow().timetuple())>= timeout:
                del self.cache[k]

        return self.cache.get(key, (0, None))[1]

    def set(self, key, value, time=0, min_compress_len=0):
        """Sets the value for a key."""
        timeout = 0
        if time != 0:
            timeout = calendar.timegm(datetime.datetime.utcnow().timetuple())+ time
        self.cache[key] = (timeout, value)
        return True

    def add(self, key, value, time=0, min_compress_len=0):
        """Sets the value for a key if it doesn't exist."""
        if self.get(key) is not None:
            return False
        return self.set(key, value, time, min_compress_len)

    def incr(self, key, delta=1):
        """Increments the value for a key."""
        value = self.get(key)
        if value is None:
            return None
        new_value = int(value) + delta
        self.cache[key] = (self.cache[key][0], str(new_value))
        return new_value

    def delete(self, key, time=0):
        """Deletes the value associated with a key."""
        if key in self.cache:
            del self.cache[key]
    
