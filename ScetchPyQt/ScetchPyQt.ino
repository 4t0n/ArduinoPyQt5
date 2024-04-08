#include <GyverFIFO.h>

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
  static uint32_t tmr = 0;
  if (millis() - tmr > 100) {
    tmr = millis();
    Serial.println(stepper1.getTarget());
  }
  if (stepper1.ready()){
    Serial.print(1);
  }
}

// функция парсинга, опрашивать в лупе
void parsing() {
  if (serial.available()) {
    GParser data(serial.buf, ',');  // отдаём парсеру
    long ints[10];           // массив для численных данных
    data.parseLongs(ints);   // парсим в него
    switch (ints[0]) {
      case 0: digitalWrite(LED, ints[1]);
        break;
      case 1:{
        if (ints[1] == 1){
          if (ints[2] == 1){
            stepper1.reverse(false);
            stepper1.setSpeed(500);
          }
          if (ints[2] == 2){
            stepper1.reverse(true);
            stepper1.setSpeed(500);
          }
          if (ints[2] == 3){
            stepper1.setSpeed(0);
          }
        }
        break;
      }
      case 2:{
        if (ints[1] == 1){
          stepper1.setTarget(ints[2]);
        }
        break;
      }
      case 3:
        if (ints[1] == 1){
          stepper1.reset();
        }
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
