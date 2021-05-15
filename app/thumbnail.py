from PIL import Image
import os
import json

def resize(source, width):
	'''Resizes an image, setting the width to `width` and scaling the height accordingly'''
	source_dir = os.path.dirname(os.path.abspath(source))
	im = Image.open(os.path.abspath(source))
	wpercent = width/float(im.size[0])
	hsize = int(float(im.size[1]) * float(wpercent))
	im.thumbnail((width, hsize))
	im.save(os.path.join(source_dir, 'thumbnail.png'), 'PNG')

def config_edit_thumbnail(config_file):
	with open(config_file) as f:
		config = json.loads(f.read())
	for doujin_key in config.keys():
		current_thumbnail_path = config[doujin_key]['thumbnail']
		new_thumbnail_path = os.path.join(os.path.dirname(current_thumbnail_path), 'thumbnail.png')
		config[doujin_key]['thumbnail'] = new_thumbnail_path
	with open(config_file, 'w') as f:
		f.write(json.dumps)
