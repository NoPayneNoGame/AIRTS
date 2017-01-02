var Render = function() {
	this.renderer = PIXI.autoDetectRenderer(512, 512);
	this.renderer.backgroundColor = 0x201a28;

	document.getElementById("game").appendChild(this.renderer.view);

	this.stage = new PIXI.Container();

	this.sprites = [];
}

Render.prototype.addSprite = function(x, y, textureURL) {
	var texture = PIXI.Texture.fromImage(textureURL);
	var character = new PIXI.Sprite(texture);

	character.anchor.x = 0.5;
	character.anchor.y = 0.5;

	character.position.x = x;
	character.position.y = y;

	this.sprites.push(character);
}

Render.prototype.updateStage = function() {
	self = this;

	var oldSprites = this.sprites;
	//this.addSprite(100, 100, '/static/images/tank.png');

	update();
	addNewSprites();


	function addNewSprites() { 
		for(var i = 0; i < self.sprites.length; i++) {
			self.stage.addChild(self.sprites[i])
		}
	}


	function update() {
		if(self.sprites !== oldSprites) {
			addNewSprites();
		}

		requestAnimationFrame(update);

		self.renderer.render(self.stage);
		oldSprites = self.sprites;
	}
}
