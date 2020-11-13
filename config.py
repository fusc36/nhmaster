class Config:
	path = '' # Path to directory storing doujins
	master_path = '' # Path to a "masterlist" text file containing doujin links/#s to download
	filter = lambda doujin: filter_none(doujin) # Function that determines what links/#s get downloaded
	port = '8100'

def filter_language(doujin, lang=['english']):
	for language in doujin.language:
		for _lang in lang:
			if language == _lang:
				return True
	return False

def filter_none(doujin):
	# Filter nothing
	return True
