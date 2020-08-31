#include <Time.h>
#include <TimeLib.h>
#include "FastLED.h"
#include <Wire.h> // for the RTC
#include <Timezone.h>
#include <DS1307RTC.h>
#include <OneButton.h>


#if FASTLED_VERSION < 3001000
#error "Requires FastLED 3.1 or later; check github for latest code."
#endif

/* Color states
1 == no color, just show time as
1 == confetti
2 == juggle
3 == matrix
*/
uint8_t colorState = 0;

// Fixed definitions cannot change on the fly.
#define LED_DT 6                                             // Data pin to connect to the strip.
#define LED_CK 7                                             // Clock pin for the strip.
#define COLOR_ORDER BGR                                       // Are they RGB, GRB or what??
#define LED_TYPE APA102                                       // Don't forget to change LEDS.addLeds
#define NUM_LEDS 130                                           // Number of LED's.
#define MAX_BRIGHT 128
#define CONFETTI_DELAY 5
#define ALL_LEDS leds(0, NUM_LEDS - 1)
#define IT leds(11, 12)
#define IS leds(8, 9)
#define MTEN leds(4, 6)
#define HALF leds(0, 3)
#define QUARTER leds(13, 19)
#define TWENTY leds(20, 25)
#define MFIVE leds(35, 38)
#define MINUTES leds(27, 33)
#define HAPPY leds(39, 43)
#define TO leds(45, 46)
#define PAST leds(48, 51)
#define BIRTHDAY leds(53, 60)
#define ONE leds(62, 64)
#define ELEVEN leds(65, 70)
#define THREE leds(72, 76)
#define FOUR leds(79, 82)
#define NINE leds(83, 86)
#define SIX leds(88, 90)
#define SEVEN leds(91, 95)
#define HFIVE leds(96, 99)
#define TWO leds(100, 102)
#define HTEN leds(106, 108)
#define EIGHT leds(111, 115)
#define TWELVE leds(117, 122)
#define OCLOCK leds(124, 129)

OneButton colorButton(2, false);
OneButton timePlusButton(3, false);
OneButton timeMinusButton(4, false);

bool updateDone = false;
bool changeHour = false;
bool changeBrightness = false;
uint8_t currentBrightness = MAX_BRIGHT;

// birthday
bool isBirthday = false;
uint8_t jessBdayMonth = 8;
uint8_t jessBdayDay = 14;
uint8_t joeBdayMonth = 2;
uint8_t joeBdayDay = 28;
uint8_t jasonBdayMonth = 6;
uint8_t jasonBdayDay = 5;

// Juggle
// Routine specific variables
uint8_t    juggleDots =   4;                                     // Number of dots in use.
uint8_t   juggleFadeRate =   2;                                     // How long should the trails be. Very low value = longer trails.
uint8_t     juggleHueInc =  16;                                     // Incremental change in hue between each dot.
uint8_t    juggleHue =   0;                                     // Starting hue.
uint8_t     juggleCurHue =   0;                                     // The current hue
uint8_t    juggleSat = 255;                                     // Saturation of the colour.
uint8_t   juggleBaseBeat =   5;                                     // Higher = faster movement.
// end juggle

// Matrix
// Palette definitions
CRGBPalette16 currentPalette;
CRGBPalette16 targetPalette;
TBlendType    currentBlending;


// Initialize global variables for sequences
int      matrixDelay =  50;                                          // A delay value for the sequence(s)
uint8_t    matrixHue =  95;
uint8_t    matrixSat = 255;
int        matrixDir =   0;
bool        huerot =   0;                                          // Does the hue rotate? 1 = yes
uint8_t      bgclr =   0;
uint8_t      bgbri =   0;
// end matrix

// Define variables used by the sequences.
uint8_t  thisfade = 1;                                        // How quickly does it fade? Lower = slower fade rate.
uint8_t  thishue = 50;                                       // Starting hue.
uint8_t  thisinc = 1;                                        // Incremental value for rotating hues
uint8_t  thissat = 150;                                      // The saturation, where 255 = brilliant colours.
uint8_t  thisbri = 255;                                      // Brightness of a sequence. Remember, MAX_BRIGHT is the overall limiter.
int  huediff = 256;                                      // Range of random #'s to use for hue

CHSV color = CHSV(0, 0, 255);

unsigned long timeButtonClickedMillis = 0;
unsigned long timeButtonDoubleClickedMillis = 0;

// Setup LED array and sets of LEDs
CRGBArray<NUM_LEDS> leds;

// Timezone
TimeChangeRule usPDT = {"PDT", Second, Sun, Mar, 2, -420};
TimeChangeRule usPST = {"PST", First, Sun, Nov, 2, -480};
Timezone myTZ(usPDT, usPST);
time_t local;
tmElements_t new_tm;

void setup() {
  delay(1000);                                                // Power-up safety delay or something like that.
  Serial.begin(9600);
  Wire.begin();
  setSyncProvider(RTC.get);
  if (timeStatus() != timeSet){
    Serial.println("RTC not running");
  } else {
    Serial.println("RTC running");
  }
  FastLED.addLeds<LED_TYPE, LED_DT, LED_CK, COLOR_ORDER>(leds, NUM_LEDS);  // Use this for WS2801 or APA102

  FastLED.setBrightness(currentBrightness);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 2200);

  // Color button handlers
  colorButton.attachClick(colorClicked);
  colorButton.attachDoubleClick(colorDoubleClicked);
  colorButton.attachLongPressStart(colorOn);
  colorButton.attachDuringLongPress(changeColorsOrBrightness);
  colorButton.attachLongPressStop(colorOff);

  // Increase time handlers
  timePlusButton.attachClick(timeButtonClicked);
  timePlusButton.attachLongPressStart(timeChangeStart);
  timePlusButton.attachDuringLongPress(increaseTime);
  timePlusButton.attachLongPressStop(timeButtonsOff);

  // Decrease time handler
  timeMinusButton.attachClick(timeButtonClicked);
  timeMinusButton.attachLongPressStart(timeChangeStart);
  timeMinusButton.attachDuringLongPress(decreaseTime);
  timeMinusButton.attachLongPressStop(timeButtonsOff);

  // matrix
  currentPalette  = CRGBPalette16(CRGB::Black);
  targetPalette   = RainbowColors_p;                            // Used for smooth transitioning.
  currentBlending = LINEARBLEND;  
  // end matrix

  displayTime();
  FastLED.show();
}

void displayOff(){
  ALL_LEDS = CRGB::Black;
  displayBirthday();
}

void displayTime(){
  // Serial.println("In display time");
  displayOff();
  local = myTZ.toLocal(now());

  // IT IS
  IT = color;
  IS = color;

  int currentHour = hour(local);
  if (currentHour > 12){
    currentHour = currentHour - 12;
  }

  if (minute(local) < 5){
    OCLOCK = color;
    // Serial.println("OClock.");
  }

  if ((minute(local)>4) && (minute(local)<10)){
    MFIVE = color;
    MINUTES = color;
    PAST = color;
    // Serial.print("Five minutes past ");
  }

  if ((minute(local)>9) && (minute(local)<15)){
    MTEN = color;
    MINUTES = color;
    PAST = color;
    // Serial.print("Ten minutes past ");
  }
  if ((minute(local)>14) && (minute(local)<20)){
    QUARTER = color;
    PAST = color;
    // Serial.print("Quarter past ");
  }
  if ((minute(local)>19) && (minute(local)<25)){
    TWENTY = color;
    MINUTES = color;
    PAST = color;
    // Serial.print("Twenty minutes past ");
  }
  if ((minute(local)>24) && (minute(local)<30)){
    TWENTY = color;
    MFIVE = color;
    MINUTES = color;
    PAST = color;
    // Serial.print("Twenty five minutes past ");
  }
  if ((minute(local)>29) && (minute(local)<35)){
    HALF = color;
    PAST = color;
    // Serial.print("Half past ");
  }
  if ((minute(local)>34) && (minute(local)<40)){
    TWENTY = color;
    MFIVE = color;
    MINUTES = color;
    TO = color;
    // Serial.print("Twenty five minutes to ");
  }
  if ((minute(local)>39) && (minute(local)<45)){
    TWENTY = color;
    MINUTES = color;
    TO = color;
    // Serial.print("Twenty minutes to ");
  }
  if ((minute(local)>44) && (minute(local)<50)){
    QUARTER = color;
    TO = color;
    // Serial.print("Quarter to ");
  }
  if ((minute(local)>49) && (minute(local)<55)){
    MTEN = color;
    MINUTES = color;
    TO = color;
    // Serial.print("Ten to ");
  }
  if (minute(local)>54){
    MFIVE = color;
    MINUTES = color;
    TO = color;
    // Serial.print("Five to ");
  }

  if ((minute(local)<35)){
    switch (currentHour) {
      case 0:
        TWELVE = color;
        // Serial.println("One ");
        break;
      case 1:
        ONE = color;
        // Serial.println("One ");
        break;
      case 2:
        TWO = color;
        // Serial.println("Two ");
        break;
      case 3:
        THREE = color;
        // Serial.println("Three ");
        break;
      case 4:
        FOUR = color;
        // Serial.println("Four ");
        break;
      case 5:
        HFIVE = color;
        // Serial.println("Hour five ");
        break;
      case 6:
        SIX = color;
        // Serial.println("Six ");
        break;
      case 7:
        SEVEN = color;
        // Serial.println("Seven ");
        break;
      case 8:
        EIGHT = color;
        // Serial.println("Eight ");
        break;
      case 9:
        NINE = color;
        // Serial.println("Nine ");
        break;
      case 10:
        HTEN = color;
        // Serial.println("Ten ");
        break;
      case 11:
        ELEVEN = color;
        // Serial.println("Eleven ");
        break;
      case 12:
        TWELVE = color;
        // Serial.println("Twelve ");
        break;
    }

  } else {
    switch (currentHour){
      case 0:
        ONE = color;
        // Serial.println("One.");
        break;
      case 1:
        TWO = color;
       // Serial.println("Two.");
       break;
      case 2:
        THREE = color;
        // Serial.println("Three.");
        break;
      case 3:
        FOUR = color;
        // Serial.println("Four.");
        break;
      case 4:
        HFIVE = color;
        // Serial.println("Five.");
        break;
      case 5:
        SIX = color;
        // Serial.println("Six.");
        break;
      case 6:
        SEVEN = color;
        // Serial.println("Seven.");
        break;
      case 7:
        EIGHT = color;
        // Serial.println("Eight.");
        break;
      case 8:
        NINE = color;
        // Serial.println("Nine.");
        break;
      case 9:
        HTEN = color;
        // Serial.println("HTen.");
        break;
      case 10:
        ELEVEN = color;
        // Serial.println("Eleven.");
        break;
      case 11:
        TWELVE = color;
        // Serial.println("Twelve.");
        break;
      case 12:
        ONE = color;
        // Serial.println("One.");
        break;
    }
  }
}

uint8_t anotherHue = 0;
uint8_t anotherDelta = 1;

void loop () {
  local = myTZ.toLocal(now());

  colorButton.tick();
  timePlusButton.tick();
  timeMinusButton.tick();

  uint8_t currentDay = day(local);
  uint8_t currentMonth = month(local);
  // birthday
  if ((currentDay == jessBdayDay and currentMonth == jessBdayMonth) or
      (currentDay == joeBdayDay and currentMonth == joeBdayMonth) or
      (currentDay == jasonBdayDay and currentMonth == jasonBdayDay)){
    isBirthday = true;
  } else {
    isBirthday = false;
  }

  EVERY_N_MILLISECONDS(50) {
    if (isBirthday) {
      displayBirthday();
    }
  }

  // juggle
  if (colorState == 2){
      ChangeJuggle();
      juggle();
  }

  // matrix
  if (colorState == 3){
      ChangeMatrix();
  }

  EVERY_N_MILLISECONDS(100) {
    if (colorState == 3){
        uint8_t maxChanges = 24; 
        nblendPaletteTowardPalette(currentPalette, targetPalette, maxChanges);   // AWESOME palette blending capability.
    }
  }

  EVERY_N_MILLISECONDS(matrixDelay) {
    if (colorState == 3){
        matrix();
    }
  }
  // end matrix

  EVERY_N_MILLISECONDS(CONFETTI_DELAY) {
    if (colorState == 1){
      confetti();
    }
  }

  if ((second(local) == 0) && (updateDone == false) && (colorState == 0)){
    // Serial.println("New minute.");
    displayTime();
    updateDone = true;
  }

  /* Reset the updateDone bool for the next minute */
  if ((second(local) == 1) && (colorState == 0)){
    updateDone = false;
  }

  FastLED.show();
}

void displayBirthday() {
  if (!isBirthday){
    return;
  }
  static uint8_t hue=0;
  HAPPY.fill_rainbow(hue++);
  BIRTHDAY.fill_rainbow(hue++);
}

void confetti() {
  if (colorState != 1){
    return;
  }
  fadeToBlackBy(leds, NUM_LEDS, thisfade);                    // Low values = slower fade.
  int pos = random16(NUM_LEDS);                               // Pick an LED at random.
  leds[pos] += CHSV((thishue + random16(huediff))/4 , thissat, thisbri);  // I use 12 bits for hue so that the hue increment isn't too quick.
  thishue = thishue + thisinc;                                // It increments here.
} // confetti()

void colorClicked(){
  switch(colorState){
    case 0:
      colorState = 1;
      break;
    case 1:
      colorState = 2;
      break;
    case 2:
      colorState = 3;
      break;
    case 3:
      color = CHSV(0, 0, 255);
      currentBrightness = MAX_BRIGHT;
      FastLED.setBrightness(MAX_BRIGHT);
      colorState = 0;
      displayTime();
      break;
  }
}

void colorOn(){
  Serial.println("Color on");
  if ((millis() - timeButtonDoubleClickedMillis) < 2000){
    changeBrightness = true;
  }
}

void colorOff(){
  Serial.println("Color off");
  changeBrightness = false;
}

void colorDoubleClicked(){
  Serial.println("Color button double clicked");
  timeButtonDoubleClickedMillis = millis();
}

void changeColorsOrBrightness(){
  if (changeBrightness){
    Serial.println("In change brightness");
    currentBrightness = currentBrightness - 2;
    if (currentBrightness > MAX_BRIGHT){
      currentBrightness = MAX_BRIGHT;
    }
    FastLED.setBrightness(currentBrightness);
    FastLED.delay(50);
  } else {
    Serial.println("In change colors");
    color = CHSV(anotherHue, 255, 255);
    anotherHue += anotherDelta;
    displayTime();
    FastLED.delay(50);
  }
}

void timeButtonClicked(){
  Serial.println("Time button clicked");
  timeButtonClickedMillis = millis();
}

void timeChangeStart(){
  if ((millis() - timeButtonClickedMillis) < 2000){
    changeHour = true;
  }
}

void increaseTime(){
  if (changeHour){
    Serial.println("Increase hour");
    breakTime((now() + 3600), new_tm);
  } else {
    Serial.println("Increase minutes");
    breakTime((now() + 60), new_tm);
  }
  displayTimeAfterChange();
}

void decreaseTime(){
  if (changeHour){
    Serial.println("Increase hour");
    breakTime((now() - 3600), new_tm);
  } else {
    Serial.println("Increase minutes");
    breakTime((now() - 60), new_tm);
  }
  displayTimeAfterChange();
}

void timeButtonsOff(){
  Serial.println("Time buttons off");
  changeHour = false;
}

void displayTimeAfterChange(){ 
  if (RTC.write(new_tm)){
    setSyncProvider(RTC.get);
  }
  
  displayTime();
  FastLED.show();
  FastLED.delay(1000); 
}

void matrix() {                                               // One line matrix

  if (huerot) matrixHue++;
  
  if (random16(90) > 80) {
    if (matrixDir == 0) leds[0] = ColorFromPalette(currentPalette, matrixHue, thisbri, currentBlending); else leds[NUM_LEDS-1] = ColorFromPalette( currentPalette, matrixHue, thisbri, currentBlending);
  }
  else {
    if (matrixDir ==0) leds[0] = CHSV(bgclr, matrixSat, bgbri); else leds[NUM_LEDS-1] = CHSV(bgclr, matrixSat, bgbri);
  }

  if (matrixDir == 0) {
    for (int i = NUM_LEDS-1; i >0 ; i-- ) leds[i] = leds[i-1];
  } else {
    for (int i = 0; i < NUM_LEDS-1 ; i++ ) leds[i] = leds[i+1];
  }
} // matrix()


void ChangeMatrix() {                                             // A time (rather than loop) based demo sequencer. This gives us full control over the length of each sequence.
  uint8_t secondHand = (millis() / 1000) % 25;                // Change '25' to a different value to change length of the loop.
  static uint8_t lastSecond = 99;                             // Static variable, means it's only defined once. This is our 'debounce' variable.
  if (lastSecond != secondHand) {                             // Debounce to make sure we're not repeating an assignment.
    lastSecond = secondHand;
    switch(secondHand) {
      case  0: matrixDelay=50; matrixHue=95; bgclr=140; bgbri=16; huerot=0; break;
      case  5: matrixDir=1; bgbri=0; break;
      case 10: targetPalette = LavaColors_p; matrixDelay=30; matrixHue=0; bgclr=50; bgbri=15; huerot=0; break;
      case 15: matrixDelay=80; bgbri = 32; bgclr=96; break;
      case 25: break;
    }
  }
} // ChangeMatrix()
// end matrix

// Juggle
void juggle() {                                               // Several colored dots, weaving in and out of sync with each other
  juggleCurHue = juggleHue;                                           // Reset the hue values.
  fadeToBlackBy(leds, NUM_LEDS, juggleFadeRate);
  for( int i = 0; i < juggleDots; i++) {
    leds[beatsin16(juggleBaseBeat+i+juggleDots,0,NUM_LEDS)] += CHSV(juggleCurHue, juggleSat, thisbri);   //beat16 is a FastLED 3.1 function
    juggleCurHue += juggleHueInc;
  }
} // juggle()

void ChangeJuggle() {                                             // A time (rather than loop) based demo sequencer. This gives us full control over the length of each sequence.
  uint8_t secondHand = (millis() / 1000) % 30;                // IMPORTANT!!! Change '30' to a different value to change duration of the loop.
  static uint8_t lastSecond = 99;                             // Static variable, means it's only defined once. This is our 'debounce' variable.
  if (lastSecond != secondHand) {                             // Debounce to make sure we're not repeating an assignment.
    lastSecond = secondHand;
    switch(secondHand) {
      case  0: juggleDots = 1; juggleBaseBeat = 20; juggleHueInc = 16; juggleFadeRate = 2; juggleHue = 0; break;                  // You can change values here, one at a time , or altogether.
      case 10: juggleDots = 4; juggleBaseBeat = 10; juggleHueInc = 16; juggleFadeRate = 8; juggleHue = 128; break;
      case 20: juggleDots = 8; juggleBaseBeat =  3; juggleHueInc =  0; juggleFadeRate = 8; juggleHue=random8(); break;           // Only gets called once, and not continuously for the next several seconds. Therefore, no rainbows.
      case 30: break;
    }
  }
} // ChangeJuggle()
// end juggle
