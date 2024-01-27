import random
import time
from threading import Thread


def down(file_name):
    sleep_time = random.randint(2, 5)
    print('开始下载:' + file_name)
    time.sleep(sleep_time)
    print('下载完毕:' + file_name)


def sim():
    for uid in range(3):
        down('file{}'.format(uid + 1))


def more():
    threads = []  # 放线程的数组
    # 创建 3 个线程
    for uid in range(3):
        temp_t = Thread(target=down, args=('file{}'.format(uid + 1),))
        threads.append(temp_t)
        temp_t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    start = time.time()
    sim()
    end = time.time()
    print('单线程共耗时:%ds' % round(end - start))

    start = time.time()
    more()
    end = time.time()
    print('多线程共耗时:%ds' % round(end - start))

