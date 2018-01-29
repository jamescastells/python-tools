import cv2
import sys
import json
import datetime
import time

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)
ts = time.time()
tiempo=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
session=sys.argv[1]
estudiante=sys.argv[2]
data={}
frame_v=0
segundo=0
data['feature']='head_position'
data['values']=[]
data['hora']=tiempo
cap=cv2.VideoCapture(sys.argv[3])

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces

        v_w = cap.get(3)
        mas_cerca = -1

        if len(faces) == 1:
            x = faces[0][0]
            y = faces[0][1]
            w = faces[0][2]
            h = faces[0][3]
        else:
            for face in faces:
                if mas_cerca == -1:
                    x = face[0]
                    y = face[1]
                    w = face[2]
                    h = face[3]
                    mas_cerca = abs(x - v_w/2)
                else:
                    if (abs(face[0] - v_w/2) < mas_cerca):
                        x = face[0]
                        y = face[1]
                        w = face[2]
                        h = face[3]
                        mas_cerca = abs(x - v_w/2)


        #for (x, y, w, h) in faces:
        #    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        #cv2.imshow('Video', frame)

        print 'Analyzing frame ' + str(30*segundo + frame_v)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_v=frame_v+1
        if (frame_v==30):
            segundo+=1
            data['values'].append({'tiempo':str(segundo),'pos_x':str(x),'pos_y':str(y),'weight':str(w),'height':str(h) })
            frame_v=0
    else:
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

with open('Session_'+str(session)+'/Estudiante_'+str(estudiante)+'/Features/Video/head_position.txt', 'w') as outfile:
    json.dump(data, outfile)

print 'Saved to Session_'+str(session)+'/Estudiante_'+str(estudiante)+'/Features/Video/head_position.txt'
