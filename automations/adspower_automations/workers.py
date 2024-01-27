"""
用来创建线程，批量进行任务
"""
from threading import Thread, Semaphore


def run(ads_host: str, ads_key: str, machines: list, function_to_run, human_like: bool = True, debug_mode: bool = False):
    threads = []
    print(type(function_to_run))