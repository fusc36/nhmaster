import os
from .download import batch_download, master_to_ids
import hentai
from pathlib import Path

class DB:
	def __init__(self, path, master, console=False):
		self.path = path
		self.db_fpath = os.path.join(self.path, 'db.txt')
		self.master = master
		self.ids = self.load_ids()
		self.doujins = self.load_dict()
		self.console = console
		self.hasht = os.path.join(self.path, 'hasht.txt')
		Path(self.hasht).touch()
		Path(self.master).touch()
		Path(self.db_fpath).touch()

	def load_ids(self):
		Path(self.db_fpath).touch()
		with open(self.db_fpath) as f:
			contents = f.read()
		ids = []
		for line in contents.split('\n'):
			try:
				ids.append(int(line))
			except:
				pass
		return ids

	def load_dict(self):
		d = {}
		'''
		for id in self.ids:
			doujin = hentai.Hentai(id)
			d[id] = doujin.title(hentai.Format.Pretty)
		return d
		'''
		hasht_path = os.path.join(self.path, 'hasht.txt')
		Path(hasht_path).touch()
		with open(hasht_path) as f:
			contents = f.read()
		for line in contents.split('\n'):
			if not line:
				pass
			try:
				tokens = line.split(',')
				id = int(tokens[0])
				dirname = ','.join(tokens[1:])
				d[id] = dirname
			except:
				pass
		return d


	def download_new(self, master_file=None, filter=lambda doujin: True, use_tqdm=False):
		if not master_file:
			master_file = self.master
		master_ids = set(master_to_ids(master_file, verbose=True))
		ids_set = set(self.ids)
		download_batch = [id for id in master_ids if id not in ids_set]
		if use_tqdm or self.console:
			print(master_ids)
			print(ids_set)
			print(download_batch)
		batch_download(download_batch, self.path, filter=filter, extend_list=self.ids, use_tqdm = self.console or use_tqdm)
		for id in download_batch:
			title = hentai.Hentai(id).title(hentai.Format.Pretty)
			self.doujins[id] = title
		self.update()

	def update(self):
		with open(self.db_fpath, 'w') as f:
			f.write('\n'.join([str(id) for id in self.ids]))
		with open(self.hasht, 'w') as f:
			f.write('\n'.join(['%s,%s' % (key, value) for (key, value) in self.doujins.items()]))
