import os

class Config:
	doujin_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'app/doujins/')
	port = '8002'
