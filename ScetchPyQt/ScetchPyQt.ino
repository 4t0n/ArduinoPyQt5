#include <FIFO.h>
#include <GStypes.h>
#include <GyverStepper2.h>

#include <GParser.h>
#include <parseUtils.h>
#include <unicode.h>
#include <url.h>

#include <AsyncStream.h>

// дигит пины
#define LED 13

AsyncStream<50> serial(&Serial, ';');   // указываем обработчик и стоп символ

bool flag = 0;
GStepper2<STEPPER4WIRE> stepper1(2048, 11, 9, 10, 8);

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  stepper1.setAcceleration(200);
  stepper1.setMaxSpeed(500);
  stepper1.setTarget(0);
}
// с пк на ардуино, терминтаор ;
// 0,лед 13
void loop() {
  stepper1.tick();
  parsing();
  if (digitalRead(LED) == 1){
    stepper1.setTarget(6000);
  }
}

// функция парсинга, опрашивать в лупе
void parsing() {
  if (serial.available()) {
    GParser data(serial.buf, ',');  // отдаём парсеру
    int ints[10];           // массив для численных данных
    data.parseInts(ints);   // парсим в него
    switch (ints[0]) {
      case 0: digitalWrite(LED, ints[1]);
        break;
      case 1:{
        stepper1.reverse(false);
        stepper1.setSpeed(500);
        break;
      }
      case 2:{
        stepper1.reverse(true);
        stepper1.setSpeed(500);
        break;
      }
      case 3: stepper1.setSpeed(0);
        break;
      case 4:{
        stepper1.setTarget(ints[1]);
        break;
      }
      case 5:{
        stepper1.reset();
        break;
      }
    }
  }
}
