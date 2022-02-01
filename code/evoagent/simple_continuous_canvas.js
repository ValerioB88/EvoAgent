var canvas_width;
var canvas_height;
var env_width;
var env_height;

function roundOf(n, p) {
	const n1 = n * Math.pow(10, p + 1);
	const n2 = Math.floor(n1 / 10);
	if (n1 >= (n2 * 10 + 5)) {
		return (n2 + 1) / Math.pow(10, p);
	}
	return n2 / Math.pow(10, p);
}

var ContinuousVisualization = function(canvas, context) {
	var ctx = context;
	var net_plotted = ""

	this.draw = function(objects) {

		for (const [idx, element] of objects.entries()) {
			this.drawEntities(idx, element);
		};

	};

	this.drawEntities = function(idx, p) {

		let cx = p.x // / env_width * scale
		let cy = p.y // / env_height * scale
		let r = p.r // / env_width * scale;

		ctx.beginPath();
		let rplot;
		if (p.type === "agent" && p.selected === true) {
			rplot = r * 2.5
		} else {
			rplot = r
		}
		ctx.arc(cx, cy, rplot, 0, Math.PI * 2, false);
		ctx.closePath();

		// ctx.fillStyle = p.selected?"Red":p.color;
		ctx.fillStyle = p.color
		ctx.fill();

		if (p.type === "agent")
		{
			let fov = p.fov;
			let max_vision = p.mvisd;
			let c = ctx.lineWidth
			ctx.lineWidth = p.selected?3:1;
			ctx.strokeStyle = "white";
			ctx.stroke()

			ctx.beginPath();
			ctx.moveTo(cx, cy);
			ctx.lineTo(cx + ((rplot + 3) * Math.cos(p.dir)), cy + ((r + 3) * Math.sin(p.dir)));
			ctx.strokeStyle = 'magenta';
			ctx.stroke();
			ctx.lineWidth = c

			if (document.getElementById("render_fov").checked) {
				ctx.beginPath();
				ctx.moveTo(cx, cy);
				ctx.arc(cx, cy, max_vision, p.dir - fov / 2, p.dir + fov / 2, false);
				// ctx.arc(cx, cy, max_vision,0, Math.PI*2, false);

				ctx.closePath();
				ctx.fillStyle = "rgb(255, 255, 0, 0.1)";
				ctx.strokeStyle = 'yellow';
				ctx.fill();
				ctx.stroke();
			}
			ctx.fillStyle = "white";
			ctx.font = "10px Arial"
			ctx.fillText(idx + ":" + p.unique_id , cx-3, cy-10)
			if (p.selected) {
				ctx.fillText(roundOf(cx,0) + "; " + roundOf(cy, 0), cx - 18, cy - 20)
			}
			// Life Bar
			if (document.getElementById("render_bars").checked) {
				let size_life_bar = 30
				ctx.beginPath();
				ctx.rect(cx - 16, cy + 10, size_life_bar, 6)
				ctx.strokeStyle = 'white';
				ctx.stroke();
				ctx.closePath();

				ctx.beginPath();
				ctx.rect(cx - 16, cy + 11, size_life_bar - p.age / p.max_age * size_life_bar, 5)
				ctx.strokeStyle = 'black';
				ctx.fillStyle = "Red"
				ctx.fill();
				ctx.closePath();


				// Reproductive Bar
				if (p.age > p.fertile_age_start) {
					let size_repro_bar = 30
					ctx.beginPath();
					ctx.rect(cx - 16, cy + 20, size_repro_bar, 6)
					ctx.strokeStyle = 'white';
					ctx.stroke();
					ctx.closePath();

					ctx.beginPath();
					ctx.rect(cx - 16, cy + 21, p.countdown_offspring / p.time_between_children * size_repro_bar, 5)
					ctx.strokeStyle = 'black';
					ctx.fillStyle = "Blue"
					ctx.fill();
					ctx.closePath();
				}
			}
			if (p.selected)
			{
				el = document.getElementById('sel_net')
				el.src = '/images/id' + p.unique_id + '.svg'
				el = document.getElementById('print_info')
				el.innerText = ''
				for (const name of p.print_info) {
					el.innerText+= name + ': ' + p[name] + '\n'
				}


				for (i = 0; i < p.children_pos.length; i++) {
					ctx.beginPath();
					ctx.moveTo(cx, cy);
					ctx.lineTo(p.children_pos[i][0], p.children_pos[i][1])
					ctx.strokeStyle = 'white';
					ctx.stroke();
					ctx.closePath();
				}
			}

		}
	};

	this.resetCanvas = function() {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
	};


};

var add_checkbox = function(id, label, elementid, start_checked=true) {
	let c = '<div class="input-group input-group-lg">\n' +
		'                    <label class="label label-primary" style="margin-right: 15px">' + label + '</label>\n' +
		'                    <input id="' + id  + '"' + (start_checked? ' checked':'') + '  type="checkbox"/>\n' +
		'\n' +
		'                </div>'
	$("#" + elementid).append($(c)[0])

	return c

}
var Simple_Continuous_Module = function(penv_width, penv_height, name_sim, model_load) {

	// Create the element
	// ------------------
	canvas_scale = 800
	env_width = penv_width
	env_height = penv_height

	var canvas_tag = "<canvas id='c' width='" + env_width + "' height='" + env_height + "' class='col-xs-12' style='border:5px dashed; padding:0px; position: relative; left: 0px; top: 0px; touch-action: none; user-select: none; cursor: default'></canvas>"
	var canvas = $(canvas_tag)[0];

	$("#elements").append(canvas);
	let context = canvas.getContext("2d");
	let canvasDraw = new ContinuousVisualization(canvas, context);

	var info_tag = "<p> Population <span id='popcount'>0</span></p>"
	$("#sidebarRight").append($(info_tag)[0])

	// Text Info
	var new_formatted_text = "<pre id='print_info' style='min-height:250px' ></pre>"
	var elem = $(new_formatted_text)[0]
	$("#sidebarRight").append(elem)

	add_checkbox("render_canvas", "Render CANVAS", "sidebarLeft")
	add_checkbox("render_fov", "Render FOV", "sidebarLeft", false)
	add_checkbox("render_bars", "Render BARS", "sidebarLeft", false)

	var output_tag = "<pre>...</pre>"
	var output = $(output_tag)[0]
	$("#sidebarRight").append(output)

	var selected_net = '<img class="col-xs-12" style="padding-left: 0px; padding-right: 0px" id="sel_net" alt="sel_net" width="160" height="160">selected Net</img>'
	$("#sidebarLeft").append($(selected_net)[0])

	document.getElementById("simName").innerHTML = name_sim
	document.getElementById("loadInfo").innerHTML = model_load


	document.addEventListener("keydown",
		function onEvent(event) {
			console.log("PRESSED")
			if (event.key === "a") {
				send({"type": "command",
					"command": "previous"})
				if (controller.running == false)
					controller.step()
				output.innerHTML = "previous agent"


			}
			if (event.key === "d") {
				send({"type": "command",
					"command": "next"})
				if (controller.running == false)
					controller.step()
				output.innerHTML = "next agent"
			}
			if (event.key === "k") {
				send({"type": "command",
					"command": "kill"})
				if (controller.running == false)
					controller.step()
				output.innerHTML = "kill"
			}
			if (event.key === "c") {
				send({"type": "command",
					"command": "offspring"})
				if (controller.running == false)
					controller.step()
				output.innerHTML = "child"

			}
			if (event.key === "s") {
				send({"type": "command",
					"command": "save"})
				if (controller.running == false)
					controller.step()
				output.innerHTML = "saved"

			}
			if (event.key === "q") {
				if (controller.running) {
					controller.stop()
					output.innerHTML = "stopped"
				}
				else {
					controller.start()
					output.innerHTML = "started"
				}
			}
			if (event.key === "x") {
				if (controller.running)
					controller.stop()
				controller.step()
				output.innerHTML = "step"

			}
		});

	this.render = function(data) {
		document.getElementById("currentStep").innerText = data["step"]
		if (data["message"] !== '') {
			output.innerHTML = data["message"]
		}
		canvasDraw.resetCanvas();
		document.getElementById("popcount").innerHTML=data["popcount"]
		if (document.getElementById("render_canvas").checked)
			canvasDraw.draw(data["entities"])
	};

	this.reset = function() {
		let a = 1
		// canvasDraw.resetCanvas();
	};

};