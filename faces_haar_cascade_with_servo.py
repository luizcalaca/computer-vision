import cv2
import sys
import RPi.GPIO as GPIO
import time

##Config Servo
P_SERVO = 7 # adapt to your wiring
fPWM = 50  # Hz (not higher with software PWM)
a = 10
b = 2


###Config Web Cam and Classifier
NUM_WEBCAM = 0
classificador = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
vc = cv2.VideoCapture(NUM_WEBCAM)

##setup servo
def setup():
    global pwm
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_SERVO, GPIO.OUT)
    pwm = GPIO.PWM(P_SERVO, fPWM)
    pwm.start(0)

##set servo direction
def setDirection(direction):
    duty = a / 180 * direction + b
    pwm.ChangeDutyCycle(duty)
    print("direction =", direction, "-> duty =", duty)
    time.sleep(1) # allow to settle

setup()

if vc.isOpened():
    retval, frame = vc.read()
else:
    sys.exit(1)

while retval:
    frame_show = frame
    imagemCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    facesDetectadas = classificador.detectMultiScale(imagemCinza, scaleFactor=1.2, minSize=(50,50))
    print(facesDetectadas)
    print("Faces detectadas: ", len(facesDetectadas))
    
    ##face detection
    for (x, y, l, a) in facesDetectadas:
        cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 255, 0), 2)
        cv2.imshow("Detector haar", frame)
        ##servo motor in action
        for direction in range(0, 181, 10):
            setDirection(direction)
        direction = 0    
        setDirection(direction)    
        GPIO.cleanup() 
    
    retval, frame = vc.read()
    
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break


