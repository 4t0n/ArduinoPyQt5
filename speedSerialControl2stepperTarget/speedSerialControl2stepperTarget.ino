// управляем скоростью из СОМ порта
// отправь q для тормоза
// отправь w для плавной остановки
// отправь e для скорости 5 град/сек
// отправь r для скорости 100 град/сек

#include <GyverStepper2.h>
//GStepper<STEPPER4WIRE> stepper(2048, 5, 3, 4, 2);
GStepper2<STEPPER2WIRE> stepper1(800, 4, 3, 2);
GStepper2<STEPPER2WIRE> stepper2(800, 7, 6, 5);
double X = 900;
double l1;
double l2;
long l01 = 410;
long l02 = 450;
double b1 = 242.074;
double b2 = 105;
double alpha = 0.903;
long L = 730;
long a1 = 340;
long a2 = 370;
int32_t l1int;
int32_t l2int;


void setup() {
  Serial.begin(9600);
  //stepper1.setRunMode(KEEP_SPEED); // режим поддержания скорости
  //stepper1.setSpeedDeg(0);         // в градусах/сек
  stepper1.setTarget(0);
  stepper1.setMaxSpeed(400);
  stepper1.reverse(true);
  stepper2.reverse(true);
  //stepper2.setRunMode(KEEP_SPEED); // режим поддержания скорости
  //stepper2.setSpeedDeg(0);         // в градусах/сек
  stepper2.setTarget(0);
  stepper2.setMaxSpeed(258);
  l1 = ((l01 - (b1 * sin(alpha - asin(X / (2 * L))) + sqrt(pow(b1, 2) * pow(sin(alpha - asin(X / (2 * L))), 2) - pow(b1, 2) + pow(a1, 2)))) / 1.75) * 800;
  l2 = ((l02 - (-b2 * (pow(X, 2) - 2 * pow(L, 2))/ pow(L, 2) + sqrt(pow(b2, 2) * pow((pow(X, 2) - 2 * pow(L, 2)), 2)/ pow(L, 4) + 4 * (pow(a2, 2) - pow(b2, 2))))/2) / 1.75) * 800;
  l1int = l1;
  l2int = l2;
  Serial.print(l1int);
  Serial.print(' ');
  Serial.print(l2int);

}

void loop() {
  stepper1.tick();
  stepper2.tick();
  if (Serial.available()) {
    char ch = Serial.read();
    if (ch == 'q') stepper1.reverse(false);
    if (ch == 'w') stepper1.reverse(true);
    if (ch == 'e') stepper1.brake();
    if (ch == 'r') stepper1.stop();
    if (ch == 't') stepper1.setSpeedDeg(100);
    if (ch == 'y') stepper1.setSpeedDeg(500);
    if (ch == 'u') stepper1.setTarget(0);
    if (ch == 'i') stepper1.setTarget(l1int);
    if (ch == 's') stepper2.reverse(false);
    if (ch == 'a') stepper2.reverse(true);
    if (ch == 'd') stepper2.brake();
    if (ch == 'r') stepper2.stop();
    if (ch == 'g') stepper2.setSpeedDeg(100);
    if (ch == 'h') stepper2.setSpeedDeg(500);
    if (ch == 'o') stepper2.setTarget(0);
    if (ch == 'p') stepper2.setTarget(l2int);
  }
}
