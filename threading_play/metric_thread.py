import time
import queue
import logging
import requests
import threading

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class line_handler():
    """ Consume and send InfluxDB metric lines

        This runs on a single threaded loop and stop_event MUST be raised
        to exit properly. Metrics are sent every 10 seconds or when queue
        exceeds 5000 pending messages.

    """

    def __init__(self) -> None:
        self.stop_event = threading.Event()
        self._shutdown = False
        self._url = 'https://us-west-2-1.aws.cloud2.influxdata.com/api/v2/write'  # noqa
        self._token = ''  # noqa
        self._headers = {
            'Accept': 'application/json',
            'Authorization': ' '.join(['Token', self._token])
        }
        self._params = {
            'org': '',
            'bucket': 'sandbox',
            'precision': 'ns'
        }
        self._metrics = queue.Queue(maxsize=100000)
        return

    def __del__(self) -> None:
        """ Force stops thread, queue is dropped """
        del self._metrics
        self._metrics = queue.Queue(maxsize=100000)
        self.stop_event.set()

    def write(self, metric: str) -> bool:
        """ Writes metric to queue. If full or invalid, returns False """
        # Mesurement,key=value field=value time
        if len(metric.split()) != 3:
            logger.error('Bad line format')
            return False
        if len(metric.split()[0].split(',')) != 2:
            logger.error('Bad messurement format')
            return False
        try:
            self._metrics.put(metric, timeout=.5)
        except queue.Full:
            logger.error('Queue Full')
            return False
        return True

    def start(self) -> None:
        """ Starts single thread """
        self.stop_event.clear()
        t = threading.Thread(target=self._thread_loop)
        t.start()

    def stop(self) -> None:
        """ Stops single thread """
        self.stop_event.set()

    def _thread_loop(self) -> None:
        """ Thread loop for sending metric bundles """
        tic = time.time()
        batch = []
        while not self.stop_event.is_set():
            toc = time.time()
            if (self._metrics.qsize() > 5000) or (toc - tic > 10):
                while len(batch) <= 5000:
                    try:
                        batch.append(self._metrics.get(True, .5))
                    except queue.Empty:
                        break
                self._send_batch(tuple(batch))
                batch.clear()
                tic = time.time()
        logger.info('Stop request recieved. Flushing queue')
        while True:
            try:
                batch.append(self._metrics.get(True, .5))
            except queue.Empty:
                break
        self._send_batch(tuple(batch))
        logger.info('Queue has been flushed and transmitted')
        self._shutdown = True
        return

    def _send_batch(self, batch: tuple) -> None:
        """ Transmit batch to Influx. Results logged to console """
        if not batch:
            return
        response = requests.post(
            self._url, headers=self._headers,
            params=self._params, data='\n'.join(batch))
        print(response.status_code)
        print(response.text)
        if response.status_code == 204:
            logger.info(f'{len(batch)} metrics lines successfully sent')
        else:
            logger.info(f'{len(batch)} metrics lines lost in delivery')
        return
