
function generateList() {
	var content = document.getElementById("content");
	{% for picName in filepath %} {
		var rowDiv = document.createElement("div");
		rowDiv.setAttribute("class", "rowDiv");

		for(var j=0; j<2; j++) {
			var gridItem = document.createElement("div");
			gridItem.setAttribute("class", "gridItem");

			var link = document.createElement("a");
			link.setAttribute("href", "commodityDetail.html");

			var gridImg = document.createElement("img");
			gridImg.setAttribute("class", "gridImg");
			gridImg.setAttribute("src", "media/{{picName}}");

			var gridText = document.createElement("input");
			gridText.setAttribute("class", "gridText");
			gridText.setAttribute("value", "商品名称");
			gridText.setAttribute("type", "text");
			gridText.setAttribute("disabled", "true");

			link.appendChild(gridImg);
			gridItem.appendChild(link);
			gridItem.appendChild(gridText);

			rowDiv.appendChild(gridItem);
		}
		content.appendChild(rowDiv);

	 {% endfor %}
}

function navigatorTo() {
	window.location.href="register.html"
}
