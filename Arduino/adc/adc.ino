#include <Arduino.h>
#include <Math.h>

#define RED 0
#define GREEN 1
#define BLUE 2
#define FALSE 0
#define TRUE 1

#define LED_RED 9 //PWM output
#define LED_GREEN 10 //PWM output
#define LED_BLUE 11 //PWM output
#define HEART_PIN 12 // PWM output

//#define DEBUG // loop() execution time

int adc_red   = 0;
int adc_blue  = 0;
int adc_green = 0;

float t = 0; // Independant variable for sine function.
int duty_cycle = 0; // Dependant variable for sine function.


void setup(){

  noInterrupts();
  // ADC Setup
  // This is sensitive work. Disabling interrupts prevents some ISR from stomping on our work.
  // We can be sure that register values are positively known. 

    ADMUX  = B01000000; // AVcc, right adjust (read both registers), ADC0.
    ADCSRA = B11100101; // ADC Enable, start conversion, auto trigger enable,
    // no IRQ, prescalar 64 (19.2k samples/sec)
    ADCSRB = B00000000; // MUX disable, free running mode.

  interrupts();
  
  pinMode(HEART_PIN,OUTPUT);

  Serial.begin(9600);

 }


void loop(){

  // Get ADC results for each channel.
  adc_red   = adc_read(RED);
  adc_green = adc_read(GREEN);
  adc_blue  = adc_read(BLUE);
  
  Serial.println((String) adc_red + "," + adc_green + "," + adc_blue); 

  // Dim/illuminate LEDs according to ADC values.
  analogWrite(LED_RED, adc_red);
  analogWrite(LED_GREEN, adc_green);
  analogWrite(LED_BLUE, adc_blue);



  #ifdef DEBUG 
  // Meaure loop execution time.
    Serial.println(micros());
  #endif

  // Blink the LED using a sine wave for PWM duty cycle.
  // This gives it a more lifelike quality than just straight toggling.
  analogWrite(HEART_PIN,duty_cycle);

  // Scale independant variable relative to ADC value. 
  // Blink rate when ADC==255 is 4x the rate when ADC==0;
  t += 0.3+0.9*(float)(adc_red)/255;

  //+128 to shift the curve up so that values range from 0 to 255 instead of -128 to +128
  duty_cycle = (unsigned int)(127*sin(t/(2*PI))+128); 

  delay(5);
}


int adc_read(int color){
  // Get 8-bits from ADCH register.
  // Set reference selection bits.
  // datasheet page 248
  noInterrupts();
  switch (color){
    case RED:
    ADMUX = B01100000; // AVcc, left adjust (high register only), ADC0.
    break;

    case GREEN:
    ADMUX = B01100001; // ADC1.
    break;
    
    case BLUE:
    ADMUX = B01100010; // ADC2.
    break;
  }
  interrupts();

  // It doesn't switch inputs without this. Mixing and matching Arduino code
  // with AVR c++ leads to weird stuff.
  delay(1); 

  return ADCH;
}
