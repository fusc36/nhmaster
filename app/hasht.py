from urllib.parse import quote
import os

class HashT:
	path=None
	hasht = {}
	@classmethod
	def set_path(cls, path):
		cls.path = path
		cls.hasht_path = os.path.join(path, 'hasht.txt')
		cls.load()

	@classmethod
	def load(cls):
		with open(cls.hasht_path) as f:
			contents = f.read()
		for line in contents.split('\n'):
			if not line:
				pass
			try:
				tokens = line.split(',')
				id = int(tokens[0])
				dirname = ','.join(tokens[1:])
				cls.hasht[id] = dirname
			except:
				pass

	@classmethod
	def retr(cls, id, pagenum):
		if cls.path == None:
			return None
		if id not in cls.hasht.keys():
			return None
		actpath = os.path.join(os.path.join(cls.path, cls.hasht[id]), str(pagenum) + '.jpg')
		if os.path.isfile(actpath):
			pattern = '/static/doujins/%s/%s.jpg' % (cls.hasht[id], pagenum)
			return quote(pattern, safe='/:?=&')
		return None

	@classmethod
	def iter(cls):
		for key in cls.hasht.keys():
			yield (key, cls.hasht[key])
