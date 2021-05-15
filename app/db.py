import json
import hentai
import pathlib
from urllib.parse import quote
import os
from pprint import pprint
from .thumbnail import resize

'''
Methods
	- set_path(path)		sets the path
	- loads()			loads the json file in the path
	- add_new(id)			Adds the id to the database (and downloads)
	- add_json(doujin)		Adds the json info from the doujin obj
	- get(id)			Retrieves the json info at <id>
	- update()			Updates the json file at path with current info
	- get_all()			Returns all jsons
	- get_file_path(id, page_num)	Returns the path of the image file for <id> and <page_num>
'''


class DB:
	doujins = {}
	path = ''
	db_path = ''

	@classmethod
	def set_path(cls, path):
		cls.path = path
		cls.db_path = os.path.join(cls.path, 'db.json')

	@classmethod
	def load(cls):
		'''Loads the json file at path into DB'''
		if not cls.db_path:
			return None
		with open(cls.db_path) as f:
			json_out = json.loads(f.read())
		d = {}
		for key in json_out.keys():
			temp = json_out[key]
			d[int(key)] = temp
		cls.doujins = d

	@classmethod
	def add_new(cls, id):
		'''Adds id'''
		# Get json
		doujin = hentai.Hentai(id)
		d_json = cls.add_json(doujin)
		dest = pathlib.Path(cls.path) / str(id)
		os.mkdir(dest)
		# Download
		doujin.download(folder=dest)
		new_path =  os.path.join(cls.path, str(id))
		try:
			os.rename(os.path.join(cls.path, d_json['title']), new_path)
		except:
			pass
		with open(os.path.join(new_path, 'info.json'), 'w') as f:
			f.write(json.dumps(d_json))

		# Create thumbnail
		page_path = cls.get_file_path(id, 1)
		cover = os.path.join(cls.path, '/'.join(page_path.split('/')[-2:]))
		resize(cover, 190)

		cls.update()

	@classmethod
	def add_json(cls, hentai_obj):
		h_json = hentai_obj.json
		id = int(h_json['id'])
		num_pages = h_json['num_pages']
		title = h_json['title']['pretty']
		tags = [dict['name'] for dict in h_json['tags']]
		db_json = {
			'num_pages': int(num_pages),
			'title': title,
			'tags': tags
		}
		cls.doujins[id] = db_json
		return db_json

	@classmethod
	def get(cls, id):
		return cls.doujins.get(id)

	@classmethod
	def update(cls):
		#pprint(cls.doujins)
		with open(cls.db_path, 'w') as f:
			f.write(json.dumps(cls.doujins))

	@classmethod
	def get_all(cls):
		return [(id, cls.doujins[id]) for id in cls.doujins.keys()]

	@classmethod
	def get_file_path(cls, id, page_number):
		if page_number == 0: # Code for thumbnail/cover
			return os.path.join('/static/doujins/', os.path.join(str(id), 'thumbnail.png'))
		jpg_snippet = os.path.join(str(id), str(page_number) + '.jpg')
		png_snippet = os.path.join(str(id), str(page_number) + '.png')
		if not cls.path:
			return None
		jpg_test = os.path.join(cls.path, jpg_snippet)
		png_test = os.path.join(cls.path, png_snippet)
		if os.path.exists(jpg_test):
			jpg = os.path.join('/static/doujins', jpg_snippet)
			return jpg
		elif os.path.exists(png_test):
			png = os.path.join('/static/doujins', png_snippet)
			return png
		print('Neither %s nor %s existed for id #%s' % (jpg_test, png_test, id))
		return None

