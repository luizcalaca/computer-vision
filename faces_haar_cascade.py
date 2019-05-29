import cv2
import sys

NUM_WEBCAM = 0

classificador = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

vc = cv2.VideoCapture(NUM_WEBCAM)

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
    
    for (x, y, l, a) in facesDetectadas:
        cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 255, 0), 2)
        cv2.imshow("Detector haar", frame)
    
    retval, frame = vc.read()
    
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break

