import cv2
import sys
import json
import datetime
import time


video_capture = cv2.VideoCapture(0)
ts = time.time()
tiempo=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
session=sys.argv[1]
estudiante=sys.argv[2]

i=0
frame_v=0
data={}
suma=0
segundo=0
data['feature']='movimiento'
data['values']=[]
data['hora']=tiempo
cap=cv2.VideoCapture(sys.argv[3])

while True:
    # Capture frame-by-frame

    ret, frame = cap.read()
    if ret == True:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        if i!=0:
            n=cv2.absdiff(gray,ant)
            ret,thresh1 = cv2.threshold(n,80,255,cv2.THRESH_BINARY)
            cant=cv2.countNonZero(thresh1)

            cv2.putText(thresh1,str(cant), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
            #cv2.imshow('Diff', thresh1)
            ant=gray
            suma=suma+cant
        else:
            ant=gray
            i=1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print 'Analyzing frame ' + str(30*segundo + frame_v)
         #cv2.imshow('Ant', ant)
         #cv2.imshow('Actual', gray)
        frame_v=frame_v+1
        if (frame_v==30):
            segundo+=1
            data['values'].append({'tiempo':str(segundo),'valor':str(suma)})
            suma=0
            frame_v=0
    else:
        break


# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
with open('Session_'+str(session)+'/Estudiante_'+str(estudiante)+'/Features/Video/movimiento.txt', 'w') as outfile:
    json.dump(data, outfile)

print 'Saved to Session_'+str(session)+'/Estudiante_'+str(estudiante)+'/Features/Video/movimiento.txt'
