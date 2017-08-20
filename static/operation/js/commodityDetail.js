
function generateList() {
	var grids = document.getElementById("grids");
	for(var i=0; i<9; i++) {
		var grid = document.createElement("a");
		grid.setAttribute("class", "weui_grid");
		grid.setAttribute("href", "");

		var gridImg = document.createElement("img");
		gridImg.setAttribute("class", "gridImg");
		gridImg.setAttribute("src", "img/testImg.jpg");

		var gridLabel = document.createElement("input");
		gridLabel.setAttribute("type", "text");
		gridLabel.setAttribute("class", "weui_grid__label gridLabel");
		gridLabel.setAttribute("disabled", "true");
		gridLabel.setAttribute("value", "XXXXXX");

		grid.appendChild(gridImg);
		grid.appendChild(gridLabel);
		grids.appendChild(grid);
	}





}