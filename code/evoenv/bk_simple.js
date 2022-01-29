var ContinuousVisualization = function(height, width, canvas) {
	var height = height;
	var width = width;
	// var ctx = context;

	this.draw = function(objects) {
		var rect = new fabric.Circle({
			left: p.x,
			top: p.y,
			fill: p.color,
			radius: p.radius
		});
		console.log(canvas)

		canvas.add(rect);

	};

	this.drawEntities = function(p) {

		let cx = p.x //* width;
		let cy = p.y //* height;
		let r = p.r;

		ctx.beginPath();
		ctx.arc(cx, cy, r, 0, Math.PI * 2, false);
		ctx.closePath();

		ctx.fillStyle = p.color;
		ctx.fill();

		if (p.type === "agent")
		{
			let fov = p.fov;
			let max_vision = p.mvisd;
			let c = ctx.lineWidth
			ctx.lineWidth = 3;
			ctx.strokeStyle = "white";
			ctx.stroke();

			ctx.beginPath();
			ctx.moveTo(cx, cy);
			ctx.lineTo(cx + ((r + 3) * Math.cos(p.dir)), cy + ((r + 3) * Math.sin(p.dir)));
			ctx.strokeStyle = 'magenta';
			ctx.stroke();
			ctx.lineWidth = c

			ctx.beginPath();
			ctx.moveTo(cx, cy);
			ctx.arc(cx, cy, max_vision, p.dir - fov/2, p.dir + fov/2, false);
			// ctx.arc(cx, cy, max_vision,0, Math.PI*2, false);

			ctx.closePath();
			context.fillStyle = "rgb(255, 255, 0, 0.1)";
			ctx.strokeStyle = 'yellow';
			ctx.fill();
			ctx.stroke();
		}
	};

	//
	this.resetCanvas = function() {
		let a = 1//	ctx.clearRect(0, 0, height, width);
	//	ctx.beginPath();
	};


};

var Simple_Continuous_Module = function(canvas_width, canvas_height) {
	// Create the element
	// ------------------

	// Create the tag:
	var canvas_tag = "<canvas id='c', width='" + canvas_width + "' height='" + canvas_height + "' ";
	canvas_tag += "style='border:5px dashed' class='col-xs-12'></canvas>";
	// var canvas = document.createElementFromString(canvas_tag[0]);

	console.log(canvas)
	// Append it to body:
	var canvas = $(canvas_tag)[0];

	$("#elements").append(canvas);
	var canvasF = new fabric.StaticCanvas('c');

	// Create the context and the drawing controller:
	// var context = canvas.getContext("2d");
	var canvasDraw = new ContinuousVisualization(canvas_width, canvas_height, canvasF);

	this.render = function(data) {
		canvasDraw.resetCanvas();
		canvasDraw.draw(data);
	};

	this.reset = function() {
		let a = 1
		// canvasDraw.resetCanvas();
	};

};