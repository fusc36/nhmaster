from config import Config
from app.db import DB
import time
from pathlib import Path

ctime = time.time()
filter = Config.filter
db = DB(Config.path, Config.master_path)


def update(use_tqdm=False):
	db.download_new(use_tqdm=use_tqdm)
print('Took %s seconds to load' % (time.time() - ctime))

if __name__ == '__main__':
	import sys
	opt = sys.argv[1]
	if opt == 'dl':
		update(use_tqdm=True)
	elif opt == 'serve':
		from app.routes import app
		from app.hasht import HashT
		HashT.set_path(Config.path)
		app.run('0.0.0.0', port=str(Config.port))
