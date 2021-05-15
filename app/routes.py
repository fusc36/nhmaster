from flask import Flask, render_template, redirect, url_for, request, jsonify
from .db import DB
from .tasks import TaskManager
import traceback
from .thumbnail import resize
import os


app = Flask(__name__)
cache = {}


@app.route('/')
@app.route('/index')
def index():
	global cache
	cache = {}
	return render_template('index.html', db=DB)

@app.route('/<int:id>/')
@app.route('/<int:id>')
def first_page(id):
	return redirect(url_for('doujin_serve', id=id, page_number=1))

@app.route('/<int:id>/<int:page_number>/')
@app.route('/<int:id>/<int:page_number>')
def doujin_serve(id, page_number):
	global cache
	if cache.get(id):
		cache_set = False
		json = cache.get(id)
	else:
		cache_set = True
		json = DB.get(id)
	if json and json.get('num_pages') >= page_number and page_number >= 1:
		if not cache and cache_set:
			cache[id] = json
		elif cache and cache_set:
			cache = {id: json}
		return render_template('serve_doujin.html', db=DB, json=json, pnumber=page_number, id=id)
	return 404

'''
@app.route('/download', methods=['GET'])
def doujin_download():
	return render_template('download.html', db=DB)
'''

@app.route('/download', methods=['POST'])
def doujin_download_post():
	download_ids = request.form.get('id').replace('\n', ' ')
	ids = []
	for id in download_ids.split(' '):
		#print(repr(id))
		id_int = url_to_id(id)
		if id_int:
			def subtask_creator(id_int): #This is a workaround so that we don't keep downloading the same fucking id. Fuck this system. Sorry for the inelegant system.
				def subtask():
					if not DB.get(id_int):
						try:
							DB.add_new(id_int)
							return 'Complete'
						except Exception as e:
							return 'Error downloading #%s: <%s>' % (id_int, traceback.format_exc())
					#print("%s was already in the dict" % id_int)
					return 'ID Found in DB'
				return subtask
			TaskManager.add_task(id_int, subtask_creator(id_int))
			#print('added %s' % id_int)
		ids.append(id_int)
	#print('%s ids' % len(set(ids)))

	return redirect(url_for('doujin_download_tasks'))

@app.route('/tasks', methods=['GET'])
def doujin_download_tasks():
	def sort_by(x):
		return x[1]
	return render_template('tasks.html', task_manager=TaskManager)

@app.route('/api')
def retrieve_json_data():
	doujins = DB.doujins.copy() # We should copy it so we don't modify it
	for id in doujins.keys():
		doujins[id]['thumbnail'] = DB.get_file_path(id, 0)
	DB.doujins = doujins
	return jsonify(doujins)

@app.route('/repair', methods=['POST'])
def repair():
	doujins = DB.doujins
	for id in doujins.keys():
		#print(doujins[id]['thumbnail'])
		if 'thumbnail.png' not in doujins[id]['thumbnail']:
			cover_path = os.path.join(os.path.dirname(__file__), DB.get_file_path(id, 1)[1:])
			#print(cover_path)
			resize(cover_path, 190)
	return '', 200


def url_to_id(url):
	try:
		tokens = url.split('/')
		if (tokens[-1] == '' or tokens[-1] == '\r') and len(tokens) > 1:
			return int(tokens[-2])
		return int(tokens[-1])
	except:
		return None

