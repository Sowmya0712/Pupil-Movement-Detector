from flask import Flask, render_template, request,Response
import cv2,imutils,time
import pyshine as ps
app = Flask(__name__)
@app.route('/')
def index():   
   return render_template('about.html')	

def pupil_detector(params):
    #print("PARAM['mode'] is ", params['mode'])
    #print("PARAM['file'] is ", params['file'])
    if(params['mode'] == "WEBCAM"):
        cap = cv2.VideoCapture(0)
    else:
        path=str(params['file'])
        cap = cv2.VideoCapture('videos\\'+path)       
   
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    print('FUNCTION DONE')
    
    center=[0, 0]    
    pupil_loc=[0, 0]    

    while True:
        ret, frame = cap.read()
        if ret is False:   #If video ends
            cap.release()  #If webcam used, release the resource
            break
        rows, cols, _ = frame.shape
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
        for (fx, fy, fw, fh) in faces:
            cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 5)
            face_gray = gray_frame[fy:fy+fw, fx:fx+fw]
            face_color = frame[fy:fy+fh, fx:fx+fw]
            eyes = eye_cascade.detectMultiScale(face_gray, 1.3, 5)
            count=0
            for (ex, ey, ew, eh) in eyes:
                #print("INSIDE EYE DETECTOR")
                cv2.rectangle(face_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
                
                center[0] = ex + ew/2
                center[1] =  ey + eh/2    

                eye_gray = face_gray[ey:ey+ew, ex:ex+ew]
                eye_color = face_color[ey:ey+ew, ex:ex+ew]
                
                _, threshold = cv2.threshold(eye_gray, 25, 255, cv2.THRESH_BINARY_INV)   # 255 is white , 0 is black
                
                contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
                
                for cnt in contours:
                    #print("INSIDE PUPIL DETECTOR")
                    (x, y, w, h) = cv2.boundingRect(cnt)
 
                    pupil_loc[0] = ex + x + w/2
                    pupil_loc[1] = ey + y + h/2


                    cv2.rectangle(eye_color, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.line(eye_color, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
                    cv2.line(eye_color, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)
                    break

                count+=1
                if(count == 2):
                    break                
        
            direction = ["", ""]
            print(center[0], center[1])
            print(pupil_loc[0], pupil_loc[1])      
            haxis =  center[0] - pupil_loc[0]
            vaxis = center[1] - pupil_loc[1]
            print(haxis, vaxis)
            if(haxis > 5):
                direction[0] = "RIGHT"
            elif(haxis < -5):
                direction[0] = "LEFT"
            else:
                direction[0] = "CENTRE"
                
            if(vaxis > 4):
                direction[1] = "TOP"
            elif(vaxis < -4):
                direction[1] = "DOWN"
            else:
                direction[1] = "CENTRE"
            print(direction[0], direction[1])    
            print()    
            cv2.putText(frame, direction[1], (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2) 
            cv2.putText(frame, direction[0], (125, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            frame = imutils.resize(frame, width=800)   #resize video width

            #Encoding frame to bytes to send
            stream = cv2.imencode('.JPEG', frame,[cv2.IMWRITE_JPEG_QUALITY,20])[1].tobytes()
            time.sleep(0.016)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream + b'\r\n')
            if(params['mode']=="WEBCAM"):
                time.sleep(0.08)
            break
   
@app.route('/res',methods = ['POST','GET'])
def res():
    global result
    if request.method == 'POST':
          
        result = request.form.to_dict()
        
	#If mode is video, save video provided by user
        if(result['mode']=='VIDEO'):
            f = request.files['file']
            filename = f.filename
            if(filename==""):   #If no video provided by user, use default video
                filename = "default.mp4"
            else:
                f.save('videos/' + filename)
            result['file'] = filename
        else:       #If webcam option selected
            result['file']=""      

        return render_template("results.html",result = result)

@app.route('/results')
def video_feed():
	global result
	params= result
	return Response(pupil_detector(params),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True,threaded=True)
