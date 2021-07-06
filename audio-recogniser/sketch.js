
// let classifier = 2;
let classif = 0;
// get the value from tensorflow 

// const classifier = (labelTensor.data())[0];

let message = ["aaah", "eeeh", "iiih", "oooh", "uuuh", "yaah", "yeeh", "yiih", "yooo", "yuuh", "taah", "teeh", "tiih", "tooh", "tuuh"]

let deltaT = 250;
let count =0;

function setup() {
 
  createCanvas(400, 400);
  
  background(220);
  startT = millis();
}

function draw() {

  textSize(32);
  
  let thisMessage;
  var label = document.getElementById('text-out');
  classif = parseInt(label.textContent);

  print(classif);
  thisMessage = message[classif];  
  

  
  // Change this to modulo.. 
  if ( millis() > startT + deltaT) {
    // print("Time elapsed");
    startT =  millis();

    
    text(thisMessage[count], count*100, 100);
    
    count ++;

    
    if (count > thisMessage.length) {
      count =0;
      background(220);
    }
  } 
  
  

//   for (let i =0; i < thisMessage.length; i++) {
//      text(thisMessage[i], i*100, 400);
//   }
 
}