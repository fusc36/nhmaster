# NHMaster

This is an ongoing project of mine with the purpose of creating a simple app that will handle my doujin hentai collection.
I wrote this in about half a day so the quality of code is not very good. Also I don't have much talent for graphical interfaces and web design so it looks ugly. But the good thing is that it works (at least for me).
Several things about this project that are bad (that I plan to fix/replace):
* ~~Masterlist and db files are text files (yeah I know it's not the best, but it was the easiest to code.)~~ Downloads are now through the `/downloads` page.
* Needs more prompts for setup
* Needs a better UI that doesn't look like an nginx sample web page
* More documentation
* ~~Ability to add doujin links from the web interface~~ Access through `/downloads`
If you want to add features/fix bugs, feel free to send a pull request or fork the repo (but that goes without saying).

# Setup

* Run `python3 -m pip install -r requirements.txt` (or `python -m pip install -r requirements.txt` or `pip install -r requirements.txt` or...)
* Edit `config.py` and add the path to where you want to store your comics (default is `app/doujins`)
* Symlink the doujin download path to `app/static/doujins` (i.e. `ln -s /path/to/doujin/download/path ./app/static/doujins`)

# Usage
* `python3 main.py` to run the server
* The port should be specified in `config.py`
