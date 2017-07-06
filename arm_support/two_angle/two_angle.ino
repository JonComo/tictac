/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

#define RED 8
#define GREEN 9
#define BLUE 10

Servo myservo1; 
Servo myservo2; 
Servo myservo3;

int a1, a2; // servo angles
float x, y;

void setup() {
  a1 = -1; // will be changed on first move
  a2 = -1;
  
  myservo1.attach(5); // arm away (drawing to the right)
  myservo2.attach(6); // arm close
  myservo3.attach(3); // pen up and down

  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);

  Serial.begin(115200);

  // LED cycle
  digitalWrite(RED, HIGH);
  delay(100);
  digitalWrite(RED, LOW);

  digitalWrite(GREEN, HIGH);
  delay(100);
  digitalWrite(GREEN, LOW);

  digitalWrite(BLUE, HIGH);
  delay(100);
  digitalWrite(BLUE, LOW);

  pen_up();
  delay(250);

  Serial.println("arduino ready");
}

void pen_up() {
  myservo3.write(90);
}

void pen_down() {
  myservo3.write(120);
}

void move_to(int t1, int t2) {
  bool there = false;

  t1 += 90 - 10;
  t2 -= 45;

  if (a1 == -1) {
    a1 = t1;
    a2 = t2;
    there = true;
  }

  while (!there) {
    there = true;
    
    if (a1 < t1) {
      a1 += 1;
      there = false;
    } else if (a1 > t1) {
      a1 -= 1;
      there = false;
    }
  
    if (a2 < t2) {
      a2 += 1;
      there = false;
    } else if (a2 > t2) {
      a2 -= 1;
      there = false;
    }
  
    myservo1.write(a1 + a2);
    myservo2.write(a1 - a2);
    
    delay(50);
  }
}

void move_to_xy(float x, float y) {

  // offset due to pen position
  x -= 1;
  y -= 1;
  
  int angle = int(  atan2(y, x) * 180 / PI );
  float d = sqrt(x*x + y*y);
  int spread = int(  acos(d/20.5) * 180 / PI );

  move_to(angle, spread);
}

void line(float sx, float sy, float ex, float ey, int steps) {
  float t = 0;
  float dt = 1.0/float(steps);
  for (float t = 0; t <= 1; t += dt) {
    // interp
    move_to_xy(sx * (1-t) + ex * t, sy * (1-t) + ey * t);
    delay(100);
  }
}

void draw_line(float sx, float sy, float ex, float ey, int steps) {
  pen_up();
  delay(250);
  move_to_xy(sx, sy);
  delay(250);
  pen_down();
  delay(250);
  line(sx, sy, ex, ey, steps);
  delay(250);
  pen_up();
  delay(250);
}

void draw_board(float sx, float sy) {
  int steps = 10; // steps per line

  // vert lines
  draw_line(sx-.7, sy+2, sx-.7, sy-2, steps);
  draw_line(sx+.7, sy+2, sx+.7, sy-2, steps);

  // horiz lines
  draw_line(sx-2, sy+.7, sx+2, sy+.7, steps);
  draw_line(sx-2, sy-.7, sx+2, sy-.7, steps);
}

float a, b, c, d;
int ia, ib;

void python_control() {
  if (Serial.available() > 0) {
    int cmd = Serial.parseInt();

    if (cmd == 0) {
      pen_up();
      delay(250);
    } else if (cmd == 1) {
      pen_down();
      delay(250);
    } else if (cmd == 2) {
      // move to
      a = Serial.parseFloat();
      b = Serial.parseFloat();
      move_to_xy(a, b);
    } else if (cmd == 3) {
      // line
      a = Serial.parseFloat();
      b = Serial.parseFloat();
      c = Serial.parseFloat();
      d = Serial.parseFloat();
      ia = Serial.parseInt();
      draw_line(a, b, c, d, ia);
    } else if (cmd == 4) {
      // control led
      ia = Serial.parseInt(); // color, 0: red, 1: green, 2: blue
      ib = Serial.parseInt(); // 0: off, 1: on
      if (ia == 0) {
        digitalWrite(RED, ib);
      } else if (ia == 1) {
        digitalWrite(GREEN, ib);
      } else if (ia == 2) {
        digitalWrite(BLUE, ib);
      }
    }

    Serial.println("d"); // done
  }
}

void loop() {
  python_control();
  /*
  draw_board(14, 0);

  draw_board(12, 0);

  draw_board(10, 0); */
  
  /*
  float sx = 14;
  float sy = 0;
  
  move_to_xy(sx, sy);
  delay(250); */

  /*
  if (Serial.available() > 0) {
    t1 = Serial.parseInt();
    t2 = Serial.parseInt();
    Serial.println(t1);
  }
   */

  /*
  move_to_xy(0, 0);
  delay(250);
  move_to_xy(-.9, -.9);
  delay(250);
  move_to_xy(.9, -.9);
  delay(250);
  move_to_xy(.9, .9);
  delay(250);
  move_to_xy(-.9, .9);
  delay(250);  */

  /*
  // squiggle square
  for (x = -.8; x < .8; x += .2) {
    for (y = -.8; y < .8; y += .2) {
      move_to_xy(x, y);
    }
  } */

  /*
  float r = random(100)/100.0 * .01 + .1;
  float sx = float(random(100))/100 * .8 - .4;
  float sy = float(random(100))/100 * .8 - .4;
  for (float t = 0; t < 4 * PI; t += PI/12) {
      move_to_xy(sx + cos(t)*r, sy + sin(t)*r);
  } */

  // spiral madness
  /*
  float sx = 12;
  float sy = 0;
  
  move_to_xy(sx, sy);
  delay(500);
  
  pen_down();
  delay(250);
  
  float r = .1;
  while (r < 3) {
    for (float t = 0; t < 2 * PI; t += PI/24) {
        r += 0.005;
        move_to_xy(sx + cos(t)*r, sy + sin(t)*r);
    }
  }

  pen_up();
  delay(250);  */

  // dot grid
  /*
  float sx = 10;
  float sy = 0;
  
  pen_up();
  delay(250);
  
  for (x = sx-4; x <= sx+4; x += 1) {
    for (y = sy-4; y <= sy+4; y += 1) {
      move_to_xy(x,y);
      delay(100);
      
      pen_down();
      delay(150);
      pen_up();
      delay(150);
    }
  }  */
  
}

