from flask import Flask, url_for, redirect, render_template
from .hasht import HashT

app = Flask(__name__)

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
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
