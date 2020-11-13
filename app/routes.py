from flask import Flask, url_for, redirect, render_template, request
from .hasht import HashT
from .db import DB
from .download import get_id

app = Flask(__name__)

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
	HashT.load()
	return render_template('index.html', hasht=HashT)

@app.route('/<int:id>/<int:pagenum>')
def retr_page(id, pagenum):
	cur_path = HashT.retr(id, pagenum)
	prev_link = url_for('retr_page', id=id, pagenum=pagenum-1) if pagenum > 1 else None
	next_link = url_for('retr_page', id=id, pagenum=pagenum+1) if HashT.retr(id, pagenum+1) else None
	return render_template('serve_doujin.html', cur_path=cur_path, prev_link=prev_link, next_link=next_link)

@app.route('/<int:id>/')
def retr_cover(id):
	return redirect(url_for('retr_page', id=id, pagenum=1))

@app.route('/download', methods=['GET'])
def download_page():
	return render_template('download.html')

@app.route('/download', methods=['POST'])
def download():
	id_raw = request.form.get('id')
	if not id_raw:
		return 400
	id = get_id(id_raw)
	DB.db.add(id)
	HashT.load()
