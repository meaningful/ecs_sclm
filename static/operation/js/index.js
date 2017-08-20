
function generateList() {
	var content = document.getElementById("content");
	for(var i=0; i<10; i++) {
		var rowDiv = document.createElement("div");
		rowDiv.setAttribute("class", "rowDiv");

		for(var j=0; j<2; j++) {
			var gridItem = document.createElement("div");
			gridItem.setAttribute("class", "gridItem");

            //TODO:点击图片进行跳转
			var link = document.createElement("a");
			//link.setAttribute("href", "commodityDetail.html");

			var gridImg = document.createElement("img");
			gridImg.setAttribute("class", "gridImg");
			gridImg.setAttribute("src", "http://pic33.nipic.com/20130928/10588125_101514420159_2.jpg");

			var gridText = document.createElement("input");
			gridText.setAttribute("class", "gridText");
			gridText.setAttribute("value", "商品名称");
			gridText.setAttribute("type", "text");
			gridText.setAttribute("disabled", "true");

            //TODO：按钮改为商品简介，无需跳转
			var gridButton = document.createElement("input");
			gridButton.setAttribute("class", "gridButton");
			gridButton.setAttribute("value", "商品简介");
			gridButton.setAttribute("type", "text");
			gridButton.setAttribute("readOnly","true");
//			gridButton.setAttribute("onClick", "navigatorTo()");

			link.appendChild(gridImg);
			gridItem.appendChild(link);
			gridItem.appendChild(gridText);
			gridItem.appendChild(gridButton);

			rowDiv.appendChild(gridItem);
		}
		content.appendChild(rowDiv);

	}
}

//function navigatorTo() {
//	window.location.href="phone_bind.html"
//}
