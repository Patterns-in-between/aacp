import oscP5.*;
import netP5.*;

OscP5 oscP5;

int lines = 3;
int histsz = 100;

ArrayList<Point> history = new ArrayList<Point>();

void setup() {
  size(800,600);
  oscP5 = new OscP5(this, 6011);
}

void draw() {
  background(0);
  stroke(255);
  if (history.size() == 0) {
    return;
  }
  synchronized(history) {
    Point last = history.get(0);
    for (int h = 1; h < history.size(); ++h) {
      Point p = history.get(h);
      for (int l = 0; l < lines; ++l) {
        line(((h-1)/100.0)*width, last.dims[l]*height, (h/100.0)*width, p.dims[l]*height);
      }
      last = p;
    }
  }
  //println(history.size());
  /*
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
  */
}

void oscEvent(OscMessage m) {
  print("### received an osc message.");
  print(" addrpattern: "+m.addrPattern());
  println(" typetag: "+m.typetag());
  
  if(m.checkTypetag("fff")) {
    float dims[] = new float[lines];
    for (int i = 0; i < lines; ++i) {
      dims[i] = m.get(i).floatValue();
    }
    synchronized(history) {
      history.add(new Point(dims));
      while (history.size() > histsz) {
        history.remove(0);
      }
    }
  }
}

class Point {
  float dims[];
  
  Point(float[] a) {
    dims = a;
  }
}
