import sys
import time
import queue
import requests
import threading
import metric_thread

stopping = threading.Event()
metrics = metric_thread.line_handler()


def single():
    payload = {
        'messages': [
            {
                'type': 'message.post',
                'value': 1
            }
        ]
    }

    header = {
        'Content-Type': 'application/json'
    }

    requests.post('http://127.0.0.1:5000/hit', json=payload, headers=header)


def slam_it(n, cli):
    header = {
        'Content-Type': 'application/json'
    }
    for idx in range(0, n):
        payload = {
            'messages': [
                {
                    'type': cli,
                    'value': idx
                }
            ]
        }
        requests.post('http://127.0.0.1:5000/hit',
                      json=payload, headers=header)


def thread_it_consumer(thread_id, q_name):
    while not stopping.is_set():
        try:
            message = q_name.get(True, 1)
            message['thread'] = thread_id
            thread_it_producer(message)
        except queue.Empty:
            continue
        q_name.task_done()
    return


def thread_it_producer(message):
    header = {
        'Content-Type': 'application/json'
    }
    tic = time.time_ns()
    response = requests.post('http://127.0.0.1:5000/slow',
                             json=message, headers=header)
    toc = time.time_ns()
    elapsed = round((toc - tic) / 1000000, 2)
    m_line = f'FGS,type=blackbox elapsed={elapsed} {time.time_ns()}'
    metrics.write(m_line)
    return


def thread_it(n, cli, threads):
    # Build the queue
    work_queue = queue.Queue()
    for idx in range(0, n):
        work_queue.put({'messages': [{'type': cli, 'value': idx}]})

    # Create six threads
    for idx in range(threads):
        t = threading.Thread(target=thread_it_consumer, args=(idx, work_queue))
        t.start()

    print('Running threads')
    work_queue.join()
    stopping.set()
    print('Job\'s finished')
    return


if __name__ == '__main__':
    args = sys.argv[1]
    # single()
    # slam_it(10000, args)

    tic = time.time_ns()
    metrics.start()
    thread_it(120, args, 6)
    metrics.stop()
    toc = time.time_ns()

    print(f'Total runtime, 6 threads: {(toc - tic) / 1000000}ms')
