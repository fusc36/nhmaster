from app.routes import app
from app.db import DB
from app.tasks import TaskManager
from config import Config

TaskManager.thread_pool_limit = Config.max_concurrent_downloads
TaskManager.start()
DB.set_path(Config.doujin_path)
DB.load()
app.run('0.0.0.0', port=Config.port)
