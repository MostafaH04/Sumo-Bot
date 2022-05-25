# Write your code here :-)
from cyberbot import *
from machine import time_pulse_us
from utime import *
from qti import *
from random import randint

Left = bot(19)
Right = bot(18)

trig = pin13
echo = pin14


trig.write_digital(0)
trig.read_digital()


Left.servo_speed(0)
Right.servo_speed(0)

turnLeft = False

irLeft = bot(11,12)
irRight = bot(8,9)

while True:
    if pin_logo.is_touched():
        break

def forward(back = False):
    if back:
        backMult = -1
    else:
        backMult = 1
    Right.servo_speed(-75 * backMult)
    Left.servo_speed(75 * backMult)

def turn(left = False):
    if left:
        leftMult = -1
    else:
        leftMult = 1
    Right.servo_speed(75 * leftMult)
    Left.servo_speed(75 * leftMult)

def stopServ():
    Right.servo_speed(0)
    Left.servo_speed(0)

def getdistance():
    trig.write_digital(1)
    trig.write_digital(0)

    time = time_pulse_us(echo, 1)
    return time*0.034/2

timeDelay = 100
timeSet = False

while True:
    if pin_logo.is_touched():
        stopServ()
        sleep_ms(500)
        while True:
            if pin_logo.is_touched():
                sleep_ms(500)
                break

    dist_cm = getdistance()

    current = qti(1,0).read()
    if current !=3:
        forward(True)
        sleep_ms(600)
        turn()
        sleep_ms(randint(300,500))
    
    if not irLeft.ir_detect(37500):
        turnLeft = False
    elif not irRight.ir_detect(37500):
        turnLeft = True
        
    
    if dist_cm < 70:
        forward()
        timeDelay = 100
        timeSet = False
    else:
        if not timeSet:
            startTime = ticks_ms()
            timeSet = True

        if ticks_diff(startTime, ticks_ms()) < -timeDelay:
            timeDelay+=100
            startTime = ticks_ms()+timeDelay
            turnLeft = not turnLeft

        if not turnLeft:
            turn(True)
        else:
            turn()


