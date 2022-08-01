
let result;
// let index = 0; 
let numTrails = 30;
let size=40;

 // To do- convert to array of arrays 
let sensor1 = [], sensor2= [], sensor3 = [];
let sensor4 = [], sensor5= [], sensor6 = [];

let vals = [];


function setup() {
	mycanvas = createCanvas(500, 500);
	setupOsc(6011, 6012);


}

function draw() {
    background(0);
    fill(255);
    stroke(255);


	// Sensor 1
    sensor1.push(vals[0]); 

    for (let i=0; i < numTrails; i++) {
        fill(255, i*10);
        noStroke();
        ellipse(50+i*5, 350- 100*sensor1[i+1], 5,5);
    }

    if (sensor1.length >= numTrails) {
        sensor1 = sensor1.splice(1);
    }


	// Sensor 2
	// sensor2.push(vals[1]); 

	// for (let i=0; i < numTrails; io++) {
	// 		fill(255, i*10);
	// 		noStroke();
	// 		ellipse(250+i*5, 350-100*sensor2[i+1], 5,5);
	// 	}
	
	// 	if (sensor2.length >= numTrails) {
	// 		sensor2 = sensor2.splice(1);
	// 	}
	


}

function receiveOsc(address, value) {
	console.log("received OSC: " + address + ", " + value);

	if (address == '/ctrl') {

		if (value[0] == 'carpet') vals[0] = value[1]; 

		// else if (value[1] = 'carpet1') vals[1] = value[1];
		// x2 = value[1];


	}
	// print([vals]);

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


