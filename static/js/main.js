
var socket = io();
var render = new Render();

socket.on('spawn', function(data){
	render.addSprite(data.x, data.y, data.texture);
	console.log("Spawning: " + data.texture + " at " + x + " " + y);
})


render.updateStage();

