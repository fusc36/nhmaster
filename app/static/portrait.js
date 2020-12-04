// Credit to https://stackoverflow.com/questions/10240110/how-do-you-cache-an-image-in-javascript
function preloadImages(array, waitForOtherResources, timeout) {
	var loaded = false, list = [], imgs = array.slice(0), t = timeout || 15*1000, timer;
	if (!waitForOtherResources || document.readyState === 'complete') {
		loadNow();
	} else {
		window.addEventListener("load", function() {
			clearTimeout(timer);
			loadNow();
		});
		timer = setTimeout(loadNow, t);
	}
	function loadNow() {
		if (!loaded) {
			loaded = true;
			for (var i = 0; i < imgs.length; i++) {
				var img = new Image();
				img.onload = img.onerror = img.onabort = function() {
					var index = list.indexOf(this);
					if (index !== -1) {
						list.splice(index, 1);
					}
				}
				list.push(img);
				img.src = imgs[i]
			}
		}
	}
}
