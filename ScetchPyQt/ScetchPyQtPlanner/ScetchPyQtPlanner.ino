#include <GyverFIFO.h>

#include <FIFO.h>
#include <GStypes.h>
#include <GyverStepper2.h>
#include <GyverPlanner.h>
#include <GParser.h>
#include <parseUtils.h>
#include <unicode.h>
#include <url.h>

#include <AsyncStream.h>

// дигит пины
#define LED 13

AsyncStream<50> serial(&Serial, ';');   // указываем обработчик и стоп символ

long target1 = 1000;
long target2 = 1000;
bool cycle = false;
bool first_iter = false;
bool cycle_continue = false;
long path[][1] = {
  {target1},
  {target2},
  {target1},
  {target2},
  {target1},
  {target2},
  {target1},
  {target2}
};

// количество точек (пусть компилятор сам считает)
// как вес всего массива / (2+2) байта
GStepper2<STEPPER4WIRE> stepper1(2048, 11, 9, 10, 8);
GStepper2<STEPPER4WIRE> stepper2(2048, 7, 6, 5, 4);
GPlanner<STEPPER4WIRE, 1> planner;

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  stepper1.setAcceleration(200);
  stepper1.setMaxSpeed(500);
  stepper1.setTarget(0);
  stepper2.setAcceleration(200);
  stepper2.setMaxSpeed(500);
  stepper2.setTarget(0);
  // stepper3.setAcceleration(200);
  // stepper3.setMaxSpeed(500);
  // stepper3.setTarget(0);

  planner.addStepper(0, stepper1);  // ось 0
  planner.addStepper(1, stepper2);  // ось 1
  // planner.addStepper(2, stepper3);  // ось 2
  // устанавливаем ускорение и скорость
  planner.setAcceleration(500);
  planner.setMaxSpeed(500);

  // начальная точка системы должна совпадать с первой точкой маршрута
//  planner.setCurrent(path[0]);
//  planner.start();
}

int count = 0;  // счётчик точек маршрута
void loop() {
//  static uint32_t tmr = 0;
//  if (millis() - tmr > 100) {
//    tmr = millis();
//    Serial.println('t');
//  }
  planner.tick();
  stepper1.tick();
  stepper2.tick();
  // stepper3.tick();
  parsing();
  if (first_iter){
      Serial.println(count);
      planner.setTarget(path[count]);
      count++;
      first_iter = false;
      cycle = true;
  }
  if (planner.ready() and count < 8 and cycle) {
    // добавляем точку маршрута и является ли она точкой остановки (0 - нет)
    planner.setTarget(path[count]);
    Serial.println(count);
    count ++;
    if (count > 7){
      count = 0;
      cycle = false;
    }
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
        if (ints[1] == 2){
          if (ints[2] == 1){
            stepper2.reverse(false);
            stepper2.setSpeed(500);
          }
          if (ints[2] == 2){
            stepper2.reverse(true);
            stepper2.setSpeed(500);
          }
          if (ints[2] == 3){
            stepper2.setSpeed(0);
          }
        }
        // if (ints[1] == 3){
        //   if (ints[2] == 1){
        //     stepper3.reverse(false);
        //     stepper3.setSpeed(500);
        //   }
        //   if (ints[2] == 2){
        //     stepper3.reverse(true);
        //     stepper3.setSpeed(500);
        //   }
        //   if (ints[2] == 3){
        //     stepper3.setSpeed(0);
        //   }
        // }
        break;
      }
      case 2:{
        if (ints[1] == 1){
          stepper1.setTarget(ints[2]);
        }
        if (ints[1] == 2){
          stepper2.setTarget(ints[2]);
        }
        // if (ints[1] == 3){
        //   stepper3.setTarget(ints[2]);
        // }
        break;
      }
      case 3:
        if (ints[1] == 1){
          stepper1.reset();
        }
        if (ints[1] == 2){
          stepper2.reset();
        }
        // if (ints[1] == 3){
        //   stepper3.reset();
        // }
        break;
      case 4:{
        if (cycle_continue){
          planner.resume();
          cycle_continue = false;
        }
        else{
          target1 = ints[1];
          target2 = ints[2];
          path[0][0] = target1;
          path[1][0] = target2;
          path[2][0] = target1;
          path[3][0] = target2;
          path[4][0] = target1;
          path[5][0] = target2;
          path[6][0] = target1;
          first_iter = true;
          break;
        }
      }
      case 5:{
        planner.pause();
        cycle_continue = true;
        break;
      }
    }
  }
}
