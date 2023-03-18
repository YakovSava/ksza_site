function checkRTMP() {
	if (flvjs.isSupported) {
		let player = flvjs.createPlayer({
			type: 'flv',
			url: 'rtmp://localost'
		});
		let toReturn = false;
		player.on(flvjs.Events.PLAYING, function() {
			let toReturn = true;
		});
		
		return toReturn;
	}
}

function translation(type) {
	if (type) {
		let player = flvjs.createPlayer({
			type: 'flv',
			url: 'rtmp://localost'
		});
		player.on(flvjs.Events.PLAYING, function() {
			player.play();
		});

		player.on(flvjs.Events.ERROR, function() {
			alert('Транcляция окончена или произошла неизвестная ошибка!');
		});
	} else {
		var element = document.getElementById('videoPlayer');
		// element.remove();

		var element = document.getElementById('stream');
		element.innerHTML = 'Транляция не происходит или завершена!';
	}
}

function reconnecting() {
	translation(checkRTMP());
}

reconnecting();