import os
import pathlib
from config import Config

pathlib.Path(os.path.join(Config.doujin_path, 'db.json')).touch()
