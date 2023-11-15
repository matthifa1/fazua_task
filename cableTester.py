import RPi.GPIO as GPIO
import time

CON1_P1 = 3
CON1_P2 = 5
CON1_P3 = 7
CON1_P4 = 11
CON1_P5 = 13
CON1_P6 = 15
CON2_P1 = 19
CON2_P2 = 21
CON2_P3 = 23
CON2_P4 = 27
CON2_P5 = 29
CON2_P6 = 31
CON3_P1 = 33
CON3_P2 = 35
CON3_P3 = 37
CON3_P4 = 36
CON3_P5 = 38
CON3_P6 = 40

LED_GREEN = 16

#        Connector 1                                             ||Connector 2                                             ||  Connector 3
#        1        | 2       | 3       | 4         | 5      | 6   || 1      | 2    | 3       | 4      | 5        | 6        || 1      | 2    | 3      | 4      | 5        | 6
#        Green    | Blue    | Orange  | Brown     | Red    |Black|| Red    |Black | Blue    | Orange | Green    | Brown    || Orange |White | Brown  | Green  | Black    | Purple
#        CAN High | CAN Low | LV 12 V | LIGHT OUT | HV 42V | GND || HV 42V | GND  | CAN Low | LV 12V | CAN High | LIGTH OUT|| LV12V  | HV42V|LIGHT O | CAN HI | GND      | CAN LOW
pin_assign=[CON1_P1,CON1_P2,  CON1_P3,  CON1_P4,    CON1_P5,CON1_P6,CON2_P1,CON2_P2,CON2_P3, CON2_P4,  CON2_P5,   CON2_P6,    CON3_P1, CON3_P2, CON3_P3, CON3_P4, CON3_P5,CON3_P6]
output = [[1,       0,        0,        0,          0,       0,     0,       0,     0,        0,       0,         0,          0,       0,     0,       0,       0,          0 ],
          [0,       1,        0,        0,          0,       0,     0,       0,     0,        0,       0,         0,          0,       0,     0,       0,       0,          0 ],
          [0,       0,        1,        0,          0,       0,     0,       0,     0,        0,       0,         0,          0,       0,     0,       0,       0,          0 ],
          [0,       0,        0,        1,          0,       0,     0,       0,     0,        0,       0,         0,          0,       0,     0,       0,       0,          0 ],
          [0,       0,        0,        0,          1,       0,     0,       0,     0,        0,       0,         0,          0,       0,     0,       0,       0,          0 ],
          [0,       0,        0,        0,          0,       1,     0,       0,     0,        0,       0,         0,          0,       0,     0,       0,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     1,       0,     0,        0,       0,         0,          0,       0,     0,       0,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       1,     0,        0,       0,         0,          0,       0,     0,       0,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       0,     1,        0,       0,         0,          0,       0,     0,       0,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       0,     0,        1,       0,         0,          0,       0,     0,       0,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       0,     0,        0,       1,         0,          0,       0,     0,       0,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       0,     0,        0,       0,         1,          0,       0,     0,       0,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       0,     0,        0,       0,         0,          1,       0,     0,       0,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       0,     0,        0,       0,         0,          0,       1,     0,       0,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       0,     0,        0,       0,         0,          0,       0,     1,       0,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       0,     0,        0,       0,         0,          0,       0,     0,       1,       0,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       0,     0,        0,       0,         0,          0,       0,     0,       0,       1,          0 ],
#          [0,       0,        0,        0,          0,       0,     0,       0,     0,        0,       0,         0,          0,       0,     0,       0,       0,          1 ],
]
result = [[1,       0,        0,        0,          0,       0,     0,       0,     0,        0,       1,         0,          0,       0,     0,       1,       0,          0 ],
          [0,       1,        0,        0,          0,       0,     0,       0,     1,        0,       0,         0,          0,       0,     0,       0,       0,          1 ],
          [0,       0,        1,        0,          0,       0,     0,       0,     0,        1,       0,         0,          1,       0,     0,       0,       0,          0 ],
          [0,       0,        0,        1,          0,       1,     0,       1,     0,        0,       0,         1,          0,       0,     1,       0,       1,          0 ],
          [0,       0,        0,        0,          1,       0,     1,       0,     0,        0,       0,         0,          0,       1,     0,       0,       0,          0 ],
          [0,       0,        0,        1,          0,       1,     0,       1,     0,        0,       0,         1,          0,       0,     1,       0,       1,          0 ],
#          [0,       0,        0,        0,          1,       0,     1,       0,     0,        0,       0,         0,          0,       1,     0,       0,       0,          0 ],
#          [0,       0,        0,        1,          0,       1,     0,       1,     0,        0,       0,         1,          0,       0,     1,       0,       1,          0 ],
#          [0,       1,        0,        0,          0,       0,     0,       0,     1,        0,       0,         0,          0,       0,     0,       0,       0,          1 ],
#          [0,       0,        1,        0,          0,       0,     0,       0,     0,        1,       0,         0,          1,       0,     0,       0,       0,          0 ],
#          [1,       0,        0,        0,          0,       0,     0,       0,     0,        0,       1,         0,          0,       0,     0,       1,       0,          0 ],
#          [0,       0,        0,        1,          0,       1,     0,       1,     0,        0,       0,         1,          0,       0,     1,       0,       1,          0 ],
#          [0,       0,        1,        0,          0,       0,     0,       0,     0,        1,       0,         0,          1,       0,     0,       0,       0,          0 ],
#          [0,       0,        0,        0,          1,       0,     1,       0,     0,        0,       0,         0,          0,       1,     0,       0,       0,          0 ],
#          [0,       0,        0,        1,          0,       1,     0,       1,     0,        0,       0,         1,          0,       0,     1,       0,       1,          0 ],
#          [1,       0,        0,        0,          0,       0,     0,       0,     0,        0,       1,         0,          0,       0,     0,       1,       0,          0 ],
#          [0,       0,        0,        1,          0,       1,     0,       1,     0,        0,       0,         1,          0,       0,     1,       0,       1,          0 ],
#          [0,       1,        0,        0,          0,       0,     0,       0,     1,        0,       0,         0,          0,       0,     0,       0,       0,          1 ],
]

GPIO.setmode(GPIO.BOARD) #Board numbering system
GPIO.setup(LED_GREEN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup([CON1_P1, CON1_P2, CON1_P3, CON1_P4, CON1_P5, CON1_P6, CON2_P1, CON2_P2, CON2_P3, CON2_P4, CON2_P5, CON2_P6, CON3_P1, CON3_P2, CON3_P3, CON3_P4, CON3_P5, CON3_P6], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

error_det = 0

for i in range(len(output)):
  GPIO.setup([CON1_P1, CON1_P2, CON1_P3, CON1_P4, CON1_P5, CON1_P6, CON2_P1, CON2_P2, CON2_P3, CON2_P4, CON2_P5, CON2_P6, CON3_P1, CON3_P2, CON3_P3, CON3_P4, CON3_P5, CON3_P6], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  
  # Setup output
  for z in range(len(output[i])):
    #set output
    if (1 == output[i][z]):
      #set output
      GPIO.setup(pin_assign[z], GPIO.OUT)
      GPIO.output(pin_assign[z], GPIO.HIGH)
      print('Set output: ' + str(z))

  # read input
  for z in range(len(output[i])):
  #set input
    if (0 == output[i][z]):
      #read input
      print('Expected Result at Pin: ' + str(z) + ' = ' + str(result[i][z]))
      if result[i][z] != GPIO.input(pin_assign(z)):
        error_det |= (1 << z) #save error and position of the fault

if 0 != error_det:
  GPIO.output(LED_GREEN, GPIO.HIGH)
  
  

