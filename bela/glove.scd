/*******************
Analog Input
Connect analog sources (e.g.: potentiometers, LDR, FSR) to analog input 0 and 1

AnalogIn returns a value from 0-1

.ar (analogPin: 0, mul: 1, add: 0)

analogPin:  Analog pin number to read. Pin numbers begin at 0. This value can be modulated at audiorate.

(c) 2017: Jonathan Reus, Marije Baalman, Giulio Moro, Andrew McPherson
*/

s = Server.default;

s.options.numAnalogInChannels = 2; // can only be 2, 4 or 8
s.options.numAnalogOutChannels = 2;
s.options.numDigitalChannels = 0;
s.options.maxLogins = 16;  	   // set max number of clients

s.options.blockSize = 16;
s.options.numInputBusChannels = 2;
s.options.numOutputBusChannels = 2;

s.waitForBoot{
	"Server Booted".postln;
	(
	  ~ctrl = {
		var a0 = AnalogIn.kr(0);
		var a1 = AnalogIn.kr(1);
		var a2 = AnalogIn.kr(2);
		var a3 = AnalogIn.kr(3);
		SendReply.kr(Impulse.kr(10), '/ctrl', [a0,a1,a2,a3]);
	  }.play;
	);
	
	OSCdef('listen', {arg msg;

		~preset = msg[3].linlin(0.0, 1.0, 0.0, 1.0).trunc(0.001);

	    [~preset].postln;

		p = ~preset;

        ~out_address  = NetAddr("toaster.local", 6060);
        ~out_address.sendMsg('/ctrl', 
        // "gloveA", 
        msg[1].linlin(0.0, 1.0, 0.0, 1.0).trunc(0.001),
        msg[2].linlin(0.0, 1.0, 0.0, 1.0).trunc(0.001),
        msg[3].linlin(0.0, 1.0, 0.0, 1.0).trunc(0.001),
        msg[4].linlin(0.0, 1.0, 0.0, 1.0).trunc(0.001)
        )
	}, '/ctrl');
	

	s.sync;
};

ServerQuit.add({ 0.exit }); // quit if the button is pressed

