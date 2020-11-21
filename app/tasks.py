from multiprocessing import Process
from threading import Thread
from time import time

# Download Request -> Download Process -> TaskManager.start(process) -> subtask(process) -> Process(target=subtask)
# TaskManager -> 'task_run_loop() -> 'subtask()

'''
TaskManager
'''

class TaskManager:
	'''routes.py -> 'TaskManager -> task()'''
	queue = []
	main_thread = None
	terminate = False
	cur_task = None
	recent_complete = []
	recent_error = []

	@classmethod
	def main_loop(cls):
		while True:
			if len(cls.queue) > 0:
				(id, task) = cls.queue.pop(0)
				cls.cur_task = id
				result = task()
				cls.cur_task = None
				if result == 'Complete':
					cls.recent_complete.append(id)
				elif result.startswith('Error') or result.startswith('ID'):
					cls.recent_error.append((id, result))
			if cls.terminate:
				break

	@classmethod
	def start(cls):
		cls.main_thread = Thread(target=cls.main_loop)
		cls.main_thread.start()

	@classmethod
	def halt(cls):
		cls.terminate = True

	@classmethod
	def add_task(cls, id, task):
		cls.queue.append((id, task))

	@classmethod
	def get_completed(cls, **kwargs):
		if kwargs.get('key'):
			return sorted(cls.recent_complete, **kwargs)
		return cls.recent_complete

	@classmethod
	def get_errored(cls, **kwargs):
		if kwargs.get('key'):
			return sorted(cls.recent_error, **kwargs)
		return cls.recent_error


'''
class TaskManager:
	tasks = {}
	terminate = False
	recent_complete = []
	recent_error = []

	@classmethod
	def task_run_loop(cls):
		print('Started task_run_loop')
		i = 0
		while True:
			for id in cls.tasks.keys():
				if cls.tasks.get(id).get('status') == 'Added to Queue':
					task = cls.tasks.get(id).get('task')
					print('Cleared0')
					def subtask():
						return_code = task()
						cls.tasks[id]['status'] = return_code
					task_process = Process(
						target=subtask,
						daemon=True
					)
					print('Cleared1')
					cls.tasks[id]['status'] = 'Processing'
					task_process.start()
					print('Added %s #%s' % (task, id))
				elif cls.tasks.get(id).get('status') == 'Complete':
					cls.recent_complete.append((time(), id, cls.tasks.get(id)))
					del cls.tasks[id]
				elif cls.tasks.get(id).startswith('Error') or 'ID Found' in cls.tasks.get(id).get('status'):
					cls.recent_error.append((time(), id, cls.tasks.get(id)))
					del cls.tasks[id]

			if cls.terminate:
				print('Ended task_run_loop')
				break
			print('%s' % i)
			i += 1

	@classmethod
	def start(cls):
		task_loop_process = Process(
			target=cls.task_run_loop,
			daemon=False
		)
		task_loop_process.start()

	@classmethod
	def add_task(cls, id, task):
		cls.tasks[id] = {
			'task': task,
			'status': 'Added to Queue'
		}

	@classmethod
	def clear(cls):
		cls.halt()
		cls.tasks = {}
		cls.start()

	@classmethod
	def halt(cls):
		cls.terminate = True

	@classmethod
	def get_completed(cls, **kwargs):
		if kwargs.get('key'):
			return sorted(cls.recent_complete, **kwargs)
		return cls.recent_complete

	@classmethod
	def get_errored(cls, **kwargs):
		if kwargs.get('key'):
			return sorted(cls.recent_error, **kwargs)
		return cls.recent_error

'''
