# references:
# 1. https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
# 2. https://stackoverflow.com/questions/9187388/possible-to-prevent-init-from-being-called
# 3. https://stackoverflow.com/questions/58386188/how-to-not-run-init-based-on-new-method

import os
import sys
import functools
import signal


class Singleton(type):
	instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls.instances:
			cls.instances[cls] = cls.__new__(
				cls, *args, **kwargs
			)  # obj = cls.__new__(cls, *args, **kwargs)
			if isinstance(cls.instances[cls], cls):
				cls.instances[cls].__init__(*args, **kwargs)
		elif kwargs.get("_run_init", None) is not None:
			if isinstance(cls.instances[cls], cls):
				del kwargs["_run_init"]
				cls.instances[cls].__init__(*args, **kwargs)

		return cls.instances[cls]


class SuppressStderr:
	"""
	A context manager to temporarily suppress stderr output.
	"""

	def __enter__(self):
		sys.stderr = open(os.devnull, "w")

	def __exit__(self, exc_type, exc_val, exc_tb):
		sys.stderr.close()


class TimeoutError(Exception):
	pass


def timeout(seconds, error_message="Function call timed out"):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			def timeout_handler(signum, frame):
				raise TimeoutError(error_message)

			original_handler = signal.signal(signal.SIGALRM, timeout_handler)
			signal.alarm(seconds)

			try:
				result = func(*args, **kwargs)
			finally:
				signal.alarm(0)
				signal.signal(signal.SIGALRM, original_handler)
			return result

		return wrapper

	return decorator


if __name__ == "__main__":

	class A(metaclass=Singleton):
		def __init__(self):
			print("init 'A' runs :(")

	a1 = A()  # init runs
	a2 = A()  # init will not run

	a3 = A(_run_init=True)  # init will run

	print(a1 is a2 is a3)  # True

	print(id(a1) == id(a2) == id(a3))  # True