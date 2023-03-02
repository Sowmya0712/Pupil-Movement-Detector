# Pupil-Movement-Detector 

Salient features of the project are:

The project has been implemented using python, HTML, CSS and JavaScript.
The code for the detector is written using the popular python library, OpenCV, which also includes the famous “Haar Cascade Classifier”, used to detect the face and eye. The python micro framework, Flask, is being used to create the web application.
The backend of the project consists of the code for the detector. Frontend consists of the website through which users interact with the detector and see the results.
The detector accurately detects the pupil and tracks it, and also prints direction of sight.
Users can choose to either upload a video or use the webcam for detection.
For more details, please read the mini project report file.

In order to run the project:

Download the project to a suitable location. Do not change the heirarchy of the folders, keep it as it is.
Open a command prompt and change directory to the directory that contains "process.py".
Type the command "py process.py" to run the file.
Open a web browser and type "http:// 127.0.0.1:5000/" or "localhost:5000". This will open the required webpage of the project.
While using the detector, please remember to ensure the following so that the detector works properly:

The face must be well within the frame
Both eyes must be visible (No side profile)
Room should be well-lit
Objects blocking the face may cause accuracy to fall
