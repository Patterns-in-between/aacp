let x1 =0, x2 =0, x3 =0, x4 =0, x5 =0, x6 =0;

let pts = [];
let angle = 0;
let coords = [[200, 100], [250, 250], [150, 200], [250, 200], [250, 350], [300,100]]

function setup() {
	createCanvas(500, 500);
	setupOsc(6011, 6012 );

	 //Create 2 data trails 
	for (let i=0; i< 2; i++) {
		pts.push(new Particle(coords[i][0], coords[i][1]));
	}

	// pts.push(new Particle(100, 100));
	
}

function draw() {
	background(220);
	// fill(0, 255, 0);
	noFill();
	stroke(0);
  	strokeWeight(4);

	// console.log(x1, x2,x3);

	// drawPoints();
	// drawLinesMovement();
	// drawCurvesMovement();
	

	pts[0].show();
	pts[0].update(x1, x2, x3);

	pts[1].show();
	pts[1].update(x1, x2, x3);
	
	
	angle += 0.1;

}

function receiveOsc(address, value) {
	// console.log("received OSC: " + address + ", " + value);

	if (address == '/all') {
		x1 = value[0];
		x2 = value[1];
		x3 = value[2];
		x4 = value[3];
		x5 = value[4];
		x6 = value[5];
	}

	// console.log(x1); 
}

function sendOsc(address, value) {
	socket.emit('message', [address].concat(value));
}

function setupOsc(oscPortIn, oscPortOut) {
	var socket = io.connect('http://127.0.0.1:8081', { port: 8081, rememberTransport: false });
	socket.on('connect', function() {
		socket.emit('config', {
			server: { port: oscPortIn,  host: '127.0.0.1'},
			client: { port: oscPortOut, host: '127.0.0.1'}
		});
	});
	socket.on('message', function(msg) {
		if (msg[0] == '#bundle') {
			for (var i=2; i<msg.length; i++) {
				receiveOsc(msg[i][0], msg[i].splice(1));
			}
		} else {
			receiveOsc(msg[0], msg.splice(1));
		}
	});
}



class Particle {

	constructor(x, y) {
	  this.x = x;
	  this.y = y;
	  this.history = [];
	 


	}
  
	update(x1_, x2_, x3_) {
	
	this.x1 = (x1_ -0.5)*10;
	this.x2 = (x2_ -0.5)*10;
	this.x3 = (x3_)*2;

	console.log(this.x1, this.x2, this.x3);

	this.x = this.x + (this.x1) *cos(angle) + random(-this.x3, this.x3) ;
	this.y = this.y + (this.x2) *sin(angle) + random(-this.x3, this.x3); 
	

	// wrap around
	// if (this.x> width +50) {
	// 	this.x = 0;
	// }

	// if (this.x < -50) {
	// 	this.x = width;
	// }

		
	// if (this.y>height+50) {
	// 	this.y = 0;
	// }

	// if (this.y < -50) {
	// 	this.y = height;
	// }


	
	//   this.x = map(cos(angle), -1, 1, this.x, this.y);
	//   this.y = map(sin(angle), -1, 1, this.x, this.y);
  
	  let v = createVector(this.x, this.y);
	
	  // remember points
	  this.history.push(v);

	// forget points after 100 inputs
	  if (this.history.length > 100) {
		this.history.splice(0, 1);
	  }
	}
  
	show() {
	  stroke(2);
	  strokeWeight(2);
	  beginShape();
	  for (let i = 0; i < this.history.length; i++) {
		let pos = this.history[i];
		noFill();
		vertex(pos.x, pos.y);
		endShape();
	  }
  
	  noStroke();
	  fill(200);
	  ellipse(this.x, this.y, 12, 12);
	}
  }


// Old code , delete ..? 


function drawPoints() {


	// shoulder 
	point(200*x1 , 100);

	// left foot
	point (250*x2, 300); 
	
	// left upper leg
	point(250*x3, 200);

	// right upper leg
	point(350*x4, 200);

	// right foot
	point(350*x4, 300);

	// right shoulder
	point(400*x5 , 100);

}


function drawLinesMovement() {

	strokeWeight(2);
	line(100*x1 , 100, 150*x2, 300);
	line(150*x2, 300, 150*x3, 200);
	line(150*x3, 200, 250*x4, 200);
	line(250*x4, 200, 250*x4, 300 );
	line(250*x4, 200, 300*x5, 100);
	line( 300*x5 , 100, 100*x1 , 100);
	

	// strokeWeight(2);
	// line(100*x1+10, 110, 150*x2+10, 310);
	// line(150*x2+10, 310, 150*x3+10, 210);
	// line(150*x3+10, 210, 250*x4+10, 210);
	// line(250*x4+10, 210, 250*x4+10, 310 );
	// line(250*x4+10, 210, 300*x5+10, 110);
	// line( 300*x5+10, 110, 100*x1+10, 110);

	// strokeWeight(1);
	// line(100*x1+10, 120, 150*x2+10, 320);
	// line(150*x2+10, 320, 150*x3+10, 220);
	// line(150*x3+10, 220, 250*x4+10, 220);
	// line(250*x4+10, 220, 250*x4+10, 320 );
	// line(250*x4+10, 220, 300*x5+10, 120);
	// line( 300*x5+10, 120, 100*x1+10, 120);


}


function drawCurvesMovement() {

	strokeWeight(2);
	bezier(constrain(85/x1, 0, height), 
			constrain(20/x2, 0, height), 
			constrain( 10/x3, 0, height),
			constrain( 10/x3, 0, height),
			constrain(  90/x4, 0, height),
			constrain( 90/x4, 0, height),
			constrain( 15/x5, 0, height),
			constrain( 80/x6, 0, height));


	
	// bezier(constrain( 80/x1, 0, height), 
	// 		constrain(15/x2, 0, height), 
	// 		constrain( 90/x3, 0, height),
	// 		constrain( 90/x3, 0, height),
	// 		constrain(  10/x4, 0, height),
	// 		constrain( 10/x4, 0, height),
	// 		constrain( 20/x5, 0, height),
	// 		constrain( 85/x6, 0, height));

}