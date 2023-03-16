function getRequest() {
	fetch('/service/get?method=getColumns&data={}')
		.then(response => response.json())
		.then(data => {
			var jsonData = data;
		})
		.catch(error => console.error(error));
	return jsonData;
}

function processRawData(data) {
	var trElements = Array.from({length: data.columns.lenght}, (value, index) => document.createElement('tr'));
	for (let i = 0; i < trElements.lenght; i++) {
		for (let j = 0; j < 3; j++) {
			var thElement = document.createElement('th');
			thElement.innerHTML = data.columns[i][j];	
			trElements[i].appendChild(thElement);
		}
	}
	return trElements;
}

function updateTable() {
	var doc = document.getElementById('dynamicTable');
	var elements = processRawData(getRequest());
	for (let i = 0; i < elements.length; i++) doc.appendChild(elements[i]);
}

updateTable();