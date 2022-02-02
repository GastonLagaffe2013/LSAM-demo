#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN  150 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  600 // This is the 'maximum' pulse length count (out of 4096)
#define USMIN  600 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2400 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

#define NUMPWM 16
#define NUMBUF 20
#define STAG 83
#define STAGL 115
#define DTAG 36
uint8_t bufferCount;    // Anzahl der eingelesenen Zeichen
char buffer[NUMBUF];    // Serial Input-Buffer
uint16_t PWMArray[NUMPWM] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
boolean dbgLvl = 1;

void setup() {
  Serial.begin(115200);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates
  for (uint8_t i=0;i<NUMPWM;i++){
    PWMArray[i]=0;
    PWMArray[i] = 0;
  }
//  for (int i=9; i>=0; i--){
  //  Serial.print(i);
    delay(1000);
//  }
  Serial.println();
  Serial.println("PWM Control v0.1 - Ready");
}

void loop() {
  if (Serial.available()) serialEvent();
}

void serialEvent(){
  char ch = Serial.read();
  buffer[bufferCount] = ch;
  bufferCount++;
  if(ch == 13)
    evalSerialData();
}

void evalSerialData(){
  // S-ascii: S=83
  // Dollar: $=36
  /* Command definition
   * $$ - list PWM status array
   * $<n> - list PWM status of PWM <n>, <n> range: [0..F]
   * $<n>=<val> - set value of PWM <n> to <val>
   * S0 <n> - set PWM to 0
   * S1 <n> - set PWM to max
   */
  boolean cmdOK=false;
  uint8_t val;
  uint8_t svo;
  uint16_t sval;
  if (dbgLvl>0){
    Serial.print("Arduino: >>");
    for (uint8_t i=0; i<bufferCount;i++){Serial.print(buffer[i]);}
    Serial.println("<<");  
  }
  if ((buffer[0] == 'D')&&(buffer[1] == 'E')&&(buffer[2] == 'B')&&(buffer[3] == 'U')&&(buffer[4] == 'G')){
    cmdOK = true;
    if (dbgLvl==0) {
      dbgLvl = 1;
      Serial.println("DEBUG ON");
    }else{
      dbgLvl = 0;
      Serial.println("DEBUG OFF");
    }
  }
  if (buffer[0] == DTAG){
    cmdOK = true;
    if (buffer[1] == DTAG){
      if (dbgLvl>0){Serial.println("$$ output");}
      for (uint8_t i=0;i<NUMPWM;i++){
        Serial.print("$");
        Serial.print(i,HEX);
        Serial.print("=");
        Serial.println(PWMArray[i]);
      }
    } else {
      svo = hexChar(buffer[1]);
      if ((svo >= 0) && (svo < NUMPWM)){
        if (bufferCount<8){
//          Serial.print("buffer length: ");
//          Serial.println(bufferCount);
          if (bufferCount==3){
            Serial.println(PWMArray[svo]);
          }
          if (bufferCount==5){
            sval=hexChar(buffer[3]);
            PWMArray[svo] = sval;
            pwm.setPWM(svo, 0, sval);
            Serial.println("OK");
          }
          if (bufferCount==6){
            sval=hexChar(buffer[3])*10+hexChar(buffer[4]);
            PWMArray[svo] = sval;
            pwm.setPWM(svo, 0, sval);
            Serial.println("OK");
          }
          if (bufferCount==7){
            sval=hexChar(buffer[3])*100+hexChar(buffer[4])*10+hexChar(buffer[5]);
//            Serial.println(sval);
            PWMArray[svo] = sval;
            pwm.setPWM(svo, 0, sval);
            Serial.println("OK");
          }
//          Serial.println(svo);
//          Serial.println(sval);
        } else {
          Serial.print("malformed command, expected up to 8 characters, received ");
          Serial.println(bufferCount);
        }
      } else {
        Serial.print("malformed command, illegal PWM number: ");
        Serial.println(svo);
      }
    }
  }
  if ((buffer[0] == STAG)||(buffer[0] == STAGL)){
    cmdOK=true;
    if (bufferCount == 5){
      val = buffer[1]-48;
      svo = hexChar(buffer[3]);
      if (dbgLvl>0){
        Serial.print("Setting Servo ");
        Serial.print(svo);
        Serial.print(" to ");
      }
      if (val==0) {
        if (dbgLvl>0){Serial.println(SERVOMIN);}
        pwm.setPWM(svo, 0, SERVOMIN);
        PWMArray[svo] = SERVOMIN;
      }
      if (val==1) {
        if (dbgLvl>0){Serial.println(SERVOMAX);}
        pwm.setPWM(svo, 0, SERVOMAX);
        PWMArray[svo] = SERVOMAX;
      }
    } else {
      Serial.print("malformed command, expected 4 characters, received ");
      Serial.println(bufferCount);
    }
  }
  if (cmdOK){
    Serial.println("OK");
  } else {
    Serial.println("unknown Command");
  }
  buffer[0] = '.';
  bufferCount = 0;                  // Reset Buffer Counter
}


uint8_t hexChar(char c){
  uint8_t chex = -1;
//  Serial.print("char >>");
//  Serial.print(c);
//  Serial.print("<< ");
  if (c == '0') chex = 0;
  if (c == '1') chex = 1;
  if (c == '2') chex = 2;
  if (c == '3') chex = 3;
  if (c == '4') chex = 4;
  if (c == '5') chex = 5;
  if (c == '6') chex = 6;
  if (c == '7') chex = 7;
  if (c == '8') chex = 8;
  if (c == '9') chex = 9;
  if (c == 'A') chex = 10;
  if (c == 'B') chex = 11;
  if (c == 'C') chex = 12;
  if (c == 'D') chex = 13;
  if (c == 'E') chex = 14;
  if (c == 'F') chex = 15;
//  Serial.println(chex);
  return chex;
}
