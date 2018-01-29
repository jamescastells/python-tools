import httplib, urllib, base64
import cv2
import requests
import json
import datetime
import time,sys

_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key = '11e94f84d22f45a2b34544f49a0e7826'
_maxNumRetries = 10
ts = time.time()
tiempo=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
session=sys.argv[1]
estudiante=sys.argv[2]

i=0
frame_v=0
data={}
suma=0
segundo=0
data['feature']='emociones'
data['values']=[]
data['hora']=tiempo
cap=cv2.VideoCapture(sys.argv[3])
headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'

def processRequest( json, data, headers, params ):
    retries = 0
    result = None
    while True:
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
        if response.status_code == 429:
            print( "Message: %s" % ( response.json()['error']['message'] ) )
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )

        break

    return result

#video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret == True:
        #cv2.imshow('frame', frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
        if (frame_v==30):
            segundo=segundo+1
            frame_v=0
            cv2.imwrite('frame.jpg',frame)
            json_o = None
            params = None
            pathToFileInDisk = 'frame.jpg'
            with open( pathToFileInDisk, 'rb' ) as f:
                image_r = f.read()
            print 'Analizando segundo: ' + str(segundo)
            v_w = cap.get(3)
            result = processRequest( json_o, image_r, headers, params )

            if result is not None:
                if len(result)==1:
                    data['values'].append({'tiempo':str(segundo),'emociones':str(result[0]['scores'])})
                elif len(result)>1:
                    mas_cerca=-1
                    for r in result:
                        if mas_cerca == -1:
                            x = r['faceRectangle']['left']
                            mas_cerca = abs(x - v_w/2)
                            resultado = r
                        else:
                            if (abs(r['faceRectangle']['left'] - v_w/2) < mas_cerca):
                                x = r['faceRectangle']['left']
                                mas_cerca = abs(x - v_w/2)
                                resultado = r
                    data['values'].append({'tiempo':str(segundo),'emociones':str(resultado['scores'])})
                else:
                    frame_v=frame_v+1
        else:
            frame_v=frame_v+1
    else:
        break

cap.release()
with open('Session_'+str(session)+'/Estudiante_'+str(estudiante)+'/Features/Video/emociones.txt', 'w') as outfile:
    json.dump(data, outfile)

print 'Saved to Session_'+str(session)+'/Estudiante_'+str(estudiante)+'/Features/Video/emociones.txt'

#if result is not None:
#    print result
#    print(result[0]['scores']['sadness'])
