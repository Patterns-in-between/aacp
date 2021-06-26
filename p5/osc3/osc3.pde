import oscP5.*;
import netP5.*;

OscP5 oscP5;


ArrayList<Point> history = new ArrayList<Point>();

void setup() {
  size(400,400);
  oscP5 = new OscP5(this, 6011);
}

void draw() {
  background(0);
  //println(history.size());
  if (history.size() > 0) {
    Point last = history.get(0);
    for (int i = 1; i < history.size(); ++i) {
      Point p = history.get(i);
      stroke(255);
      line(p.x*width, p.y*height, last.x*width, last.y*height);
      last = p;
    }
    for (int i = 1; i < history.size(); ++i) {
      Point p = history.get(i);
      stroke(128);
      line(p.x*width, p.z*height, last.x*width, last.z*height);
      last = p;
    }
  }
}

void oscEvent(OscMessage m) {
  print("### received an osc message.");
  print(" addrpattern: "+m.addrPattern());
  println(" typetag: "+m.typetag());
  
  if(m.checkTypetag("fff")) {
    history.add(new Point(m.get(0).floatValue(),
                          m.get(1).floatValue(),
                          m.get(2).floatValue()
    ));
    while (history.size() > 100) {
      history.remove(0);
    }
  }
  if(m.checkTypetag("ffffffff")) {
    history.add(new Point(m.get(0).floatValue(),
                          m.get(1).floatValue(),
                          m.get(2).floatValue()
    ));
    while (history.size() > 100) {
      history.remove(0);
    }
  }
}

class Point {
  float x;
  float y;
  float z;
  Point(float a, float b, float c) {
    //println(a + "x" + b + "x" + c);
    x = a; y = b; z = c;
  }
}
