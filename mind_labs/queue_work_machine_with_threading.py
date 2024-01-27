# Let's say we got 23 pcs of machine, and need maximum 5 machine to work at a time, When a machine done its work,
# the next machine will start his work. Help me to rewrite my code.
import random
import time
from threading import Thread, Semaphore

work_machines = [
    '3001', '3002', '3003', '3004', '3005', '3006', '3007', '3008', '3009', '3010',
    '3011', '3012', '3013', '3014', '3015', '3016', '3017', '3018', '3019', '3020',
    '3021', '3022', '3023', '3024', '3025', '3026', '3027', '3028', '3029', '3030',
    '3031', '3032', '3033', '3034'
]

machine_working_together_limit = 5
semaphore = Semaphore(machine_working_together_limit)


def worker(work_machine):
    with semaphore:
        print('Working on ' + work_machine)
        time.sleep(random.randint(2, 5))
        print('Finished working on ' + work_machine)


def work():
    threads = []
    for machine in work_machines:
        t = Thread(target=worker, args=(machine,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    start = time.time()
    work()
    end = time.time()
    print(f'Total time: {round(end - start)}s')
