import os
from config import Config

db_path = os.path.join(Config.doujin_path, 'db.json')
with open(db_path, 'w') as f:
	f.write('{}')
