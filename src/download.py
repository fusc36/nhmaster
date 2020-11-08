import hentai
import pathlib
from pathlib import Path
from tqdm import tqdm

def get_id(url):
	'''Given a url, returns the id'''
	tokens = url.split('/')
	if tokens[-1] == '':
		tokens.pop(-1)
	id = int(tokens[-1])
	return id

def download(doujin, path):
	if isinstance(path, pathlib.Path):
		return doujin.download(dest=path)
	else:
		return doujin.download(dest=Path(path))

def batch_download(ids, path, filter=lambda x: x, extend_list=None, use_tqdm=False):
	ids_tqdm = tqdm(ids) if use_tqdm else ids
	for id in ids_tqdm:
		if hentai.Hentai.exists(id):
			doujin = hentai.Hentai(id)
			if filter(doujin):
				download(doujin, path)
				if isinstance(extend_list, list):
					extend_list.append(id)

def master_to_ids(fpath, verbose=False):
	with open(fpath) as f:
		contents = f.read()
	if verbose:
		print(contents)

	ids = []
	for line in contents.split('\n'):
		try:
			ids.append(get_id(line))
		except:
			pass
	return ids
