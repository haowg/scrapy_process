# coding:utf8

"""
代理管理器
"""

import time
import random
import sys
import copy
import logging

class Singleton(object):
    '''
    单例
    '''
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class ProxyManager(Singleton):
    """代理管理器

    提供代理时间控制
    """
    def __init__(self, proxies_or_path, interval_per_ip=5, is_single=False):
        '''
        @proxies_or_path, basestring or list, 代理path或列表
        @interval_per_ip, int, 每个ip调用最小间隔
        @is_single, bool, 是否启用单点代理,例如使用squid
        '''
        self.proxies_or_path = proxies_or_path
        self.interval = interval_per_ip
        self.host_time_map = {}
        self.is_single = is_single
        self.init_proxies(self.proxies_or_path)
        self.count = 0

    def init_proxies(self, proxies_or_path):
        '''初始化代理列表

        @proxies_or_path, list or basestring
        '''
        if isinstance(proxies_or_path, basestring):
            if self.is_single:
                self.proxies = proxies_or_path
            else:
                with open(proxies_or_path) as fip:
                    self.proxies = fip.readlines()
        else:
            self.proxies = proxies_or_path

    def reload_proxies(self):
        '''
        重新加载代理，proxies_or_path必须是文件路径
        '''
        if not isinstance(self.proxies_or_path, basestring):
            raise TypeError("proxies_or_path type is invalid!")
        if self.is_single:
            raise TypeError("is_single must be False!")
        with open(self.proxies_or_path) as fip:
            self.proxies = fip.readlines()
        logging.info("reload %s proxies ...", len(self.proxies))

    def _get_proxy(self, count_num):
        '''
        随机获取代理ip的方法
        '''
        count = [0]
        def getter():
            '''
            获取ip代理,闭包
            '''
            if count[0] >= count_num:
                self.reload_proxies()
                count[0] = 0
            count[0] += 1
            my_proxys = copy.deepcopy(self.proxies)
            min_latest_time = sys.maxint
            min_time_proxy = ''
            for i in range(len(my_proxys)):
                proxy = random.choice(my_proxys)
                # 获取最近一次使用该代理的时间
                host, _ = proxy.split(':')
                latest_time = self.host_time_map.get(host, 0)
                # 记录最早使用的proxy
                if min_latest_time > latest_time:
                    min_latest_time = latest_time
                    min_time_proxy = proxy
                # 判断间隔时间有没有达到
                my_interval = time.time() - latest_time
                if my_interval < self.interval:
                    my_proxys.remove(proxy)
                else:
                    self.host_time_map[host] = time.time()
                    return proxy
            else:
                # 如果遍历完成则，暂停到第一个可用的代理时间
                time.sleep(self.interval - time.time() + min_latest_time)
                return min_time_proxy
        return getter

    def get_proxy(self):
        '''
        获取一个可用代理
        如果代理使用过于频繁会阻塞，以防止服务器屏蔽
        '''
        # 如果使用单点代理,直接返回
        if self.is_single: return self.proxies
        getter = self._get_proxy(1000)
        proxy = getter()
        logging.info('now proxy is %s' ,proxy.strip())
        return "http://%s" % proxy.strip()

