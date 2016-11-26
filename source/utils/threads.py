import signal, threading, os


class StoppableThread(threading.Thread):
	"""Thread class with a stop() method. When the stop method is called and a process id is set (via set_pid) it kills the process"""

	def __init__(self, target=None):
		super(StoppableThread, self).__init__(target=target)

		self.pid = None
		self._stop = threading.Event()

	def set_pid(self, pid):
		self.pid = pid

	def stop(self):
		self._stop = threading.Event()
		self._stop.set()
		if self.pid:
			os.kill(self.pid, signal.SIGTERM)

	def stopped(self):
		return self._stop.isSet()
