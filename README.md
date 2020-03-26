# Software-Engineering-project
Police informant system to detect social gathering during covid-19 breakdown

    I. Introduction
    II. Proposed Model
    a) Formation of Distributed System
    b) Image extraction from Webcam with location(database formation)
    c) ML on images
    d) Data transmission and alert messages

# I. INTRODUCTION
    

<p align="center">
  <img src="images/model_intro.png">
</p>

<p align="center">
  <img src="images/stage1.png">
</p>

 ## A) Formation of Distributed System .
    
Distributed System is a system with multiple components located on different machines that communicate and coordinate actions in order to appear as a single coherent system to the end user.\
In our project,the role of Distributed System is that cameras are installed at different places and these cameras will         store the data of that place and put the stored data on the server.and the data of the server of these different places       will be sent to the server of a nearest police station,so that police will find out how many people are standing in the       crowd. If 5 or more people stand in the crowd then the police will act on them.
    
## B) Image Extraction from Webcam and storing the image in database with webcam location.

  This task needs to be done in 3 parts:\
   (i) Extracting image from webcam:\
      → Webcam will capture the video continously,so we need to extract image frames from that video stream after some       
        particular interval.This can be done using openCV and timer from time package in python.Also, we need to take care of 
        deleting/overwriting images after a particular time interval in database.\
   (ii) Fetching the location of webcam\
      → We will fetch the location of webcam, using already created database (which we have created while installing the             cameras).The proposed structure of this database is <license_number,location>. Using this license number we will
        fetch the location of the webcam.\
   (iii) Storing image with corresponding webcam location in the database\
       →
## C) Applying ML based techniques to identify the number of people in a particular image.
The technique to estimate the number of objects/entities in an image is called “Crowd Counting”. In our case we will perform people counting ie., to find the count of people present in an image. There are various ways to perform this, which are as follows : 

* Detection based methods
* Regression based methods
* Density Estimation based methods
* CNN(Convolutional Neural Network) based methods

 ![Crowd](https://miro.medium.com/max/878/1*BxF31bnOrPR5YbgLqv_wfQ.jpeg)

We will employ the optimum performing method based on our experimentation with empirical data. The steps that need to be performed for Crowd Counting are :
1) Data Acquisition
2) Loading Input Data
3) Cleaning
4) Segmentation and Classification
5) Counting

After performing the above mentioned steps, we will obtain the number of people in a particular image of a location, which will be used for further action.

