#include <Servo.h>

Servo spen;
Servo sx;
Servo sy;

int button = 4; // pin 2

bool is_pen_down;

int x_rest = 68;
int y_rest = 112;
int pen_down = 90;
int pen_up = 80;

// twelve servo objects can be created on most boards

int data[5];
int offset;

void setup() {
  spen.attach(9);
  sx.attach(10);
  sy.attach(11);

  sx.write(x_rest);
  sy.write(y_rest);

  // lift the pen
  spen.write(pen_up);
  is_pen_down = false;

  // setup serial
  offset = 0;
  
  Serial.begin(115200);
}

void loop() {

  // serial control
  
  while (Serial.available() > 0) {
    byte byte_read = Serial.read();

    if (byte_read == 44) {
      // delimeter
      offset = 0;
    } else {
      data[offset] = byte_read - 48;
      offset ++;

      if (offset == 5) {
        // got a full command
        offset = 0;
  
        Serial.println("got command:");
        Serial.println(data[0]);
        Serial.println(data[1]);
        Serial.println(data[2]);
        Serial.println(data[3]);
        Serial.println(data[4]);
  
        int cmd = data[0];
        
        if (cmd == 0) {
          // pen down
          spen.write(pen_down);
        } else if (cmd == 1) {
          // pen up
          spen.write(pen_up);
        } else if (cmd == 2) {
          // move fractional
          
          int inx = data[1] * 10 + data[2];
          int iny = data[3] * 10 + data[4];
  
          // range from 0-99
          
          float dx = float(inx+1)/100.0 * 2.0 - 1.0;
          float dy = float(iny+1)/100.0 * 2.0 - 1.0;
    
          sx.write(x_rest - int(90 * dx));
          sy.write(y_rest - int(90 * dy));
        }
      }
    }
  }
  
  // manual control
  /*
  if (analogRead(button) == 0) {
    is_pen_down = !is_pen_down;
    if (is_pen_down) {
      spen.write(pen_down);
    } else {
      spen.write(pen_up);
    }

    delay(200);
  }
  
  float x = (float)analogRead(2);
  float y = (float)analogRead(3);

  x = x/1024.0 * 2.0 - 1.0;
  y = y/1024.0 * 2.0 - 1.0;

  if (abs(x)<.1) {
    x = 0;
  }

  if (abs(y)<.1) {
    y = 0;
  }

  sx.write(x_rest - int(x * 90));
  sy.write(y_rest - int(y * 90)); */
}

