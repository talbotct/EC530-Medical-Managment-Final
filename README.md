# EC 530 Final Project Medical Management

## 1. Overview
This project was based on previous work on the creation of an API for management of a medical platform.  The API and chat implementation was rooted in these previous projects.  I was able to create a web platform to allow for the creation of user accounts to manage the user medical and device data.  Flask in Python was used in the development of the web application that wraps up these other features.  Google Cloud Platform was used for the database storage as well as the cloud hosting.  These and other features are supported well through this join platform.  Below are the original user stories for the project, the web application was developed with the features in mind.  I believe I was fairly successful in reaching these goals, with some changes in direction during the development process.  Below is also installation instructions, additional documentation can be found on the wiki page.

## 2. User Stories
Administrators
1. Add users to the system
2. Assign and Change Roles to users
3. A user can have different roles
4. Provide interfaces to third party medical device makers 
5. Ability to disable or enable any device maker or application developer

Medical Professionals
1. Browse Patients
2. Assign a medical device to a Patient
3. Assign Alert and scheduling for medical measurement
4. Can input data for any patient
5. Can chat with patients using text, voice or videos.
6. Can read transcripts of Patient uploaded videos and messages
7. Can search for keywords in messages and chats
8. Have a calendar where they can show open time slots for appointments
9. Can see all appointments booked at any time

Patients
1. Can enter measurement at any time
2. Can write a text or upload video or voice message to the MP
3. Can book an appointment with the MP
4. Can view their medical measurements


## 3. Installation
1. Clone repo
2. pip install -r /path/to/requirements.txt
3. Place Google Cloud API key in cloned location
4. Run app.py to host locally
5. Go to http://127.0.0.1:5000/ to use web application or make API calls

## 4. Google Cloud API Setup
### Login to Google Cloud Console and Search "Service Accounts"
![0740d0973f45b075b2fb7e88faad0640](https://user-images.githubusercontent.com/56003386/162986908-44702ce8-ff10-457b-a455-cc87857f0f03.png)
### Create or select the service account to use
![78d35354936698f67d63b59866f9940c](https://user-images.githubusercontent.com/56003386/162986941-41a99ba5-b182-4298-bc79-287422cf9bb0.png)
### Select "add key" to generate a new api access key
![617957eca99b0bd77c76b789d4a7e427](https://user-images.githubusercontent.com/56003386/162986961-f5d3b2b6-0713-408a-bbbf-ad491ddc4c92.png)
### Select and generate a .json version of the key
![de34b0d3ab51bf2f72233c5395a28324](https://user-images.githubusercontent.com/56003386/162986983-57d016d8-cc02-406c-a857-1a675c02774d.png)

## 5. Resources
RESTful API Info
https://cloud.google.com/blog/products/application-development/rest-vs-rpc-what-problems-are-you-trying-to-solve-with-your-apis

API Status Codes
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

Flask Basic API Structure
https://flask-restful.readthedocs.io/en/latest/quickstart.html

Full Flask REST Documentation
https://flask-restx.readthedocs.io/_/downloads/en/latest/pdf/

Swagger API Editor
https://swagger.io/tools/swagger-editor/

Pandas Dataframe Manipulation
https://re-thought.com/how-to-change-or-update-a-cell-value-in-python-pandas-dataframe/

Google Cloud Firestore Documentation
https://firebase.google.com/docs/firestore

Google Cloud Compute Engine Documentation
https://cloud.google.com/compute/docs#docs

Flask Web App Tutorial
https://www.techwithtim.net/tutorials/flask/a-basic-website/

In depth Flask Application Tutorial Series
https://www.youtube.com/watch?v=8wxVCiFGUzo&list=PLG5KvF1OpdCWNNul4xDrUNNrs3olOaEIW&ab_channel=GeeksforGeeksDevelopment

Introduction to HTML
https://www.w3schools.com/html/
