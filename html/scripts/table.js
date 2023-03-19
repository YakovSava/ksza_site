async function getRequest() {
	try {
		let response = await fetch('/service/get?method=getColumns&data={}');
		var data = await response.json();
		return data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

function processRawData(data) {
	if (data != null) {
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
}

async function updateTable() {
	var doc = document.getElementById('dynamicTable');
	var data = await getRequest();
	var elements = processRawData(data);
	for (let i = 0; i < elements.length; i++) doc.appendChild(elements[i]);
}

updateTable().then(() => {});