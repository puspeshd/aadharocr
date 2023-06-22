import cv2
import os
def fileresize(img,time):
        cv2.imread("images/"+time+".jpg")
        size=os.path.getsize("images/"+time+".jpg")/1024
        h,w,_=img.shape()
        if(size>100 and size<200):
         img=cv2.resize(img,((w*(80//100),h*(80//100))))
        elif(filesize>200 and filesize<500):
         img=cv2.resize(img,(w*(70//100),h*(70//100)))  
        elif(filesize>500 and filesize<700):
            img=cv2.resize(img,(w*50//100,h*50//100))
        elif(filesize>700 and filesize<1000):
            img=cv2.resize(img,(w*30//100,h*30//100))
        elif(filesize>1000 and filesize<2000):    
         img=cv2.resize(img,(w*20//100,h*20//100))                       
        elif(filesize>2000):    
         img=cv2.resize(img,(w*10//100,h*10//100))   
        cv2.imwrite("images/"+time+".jpg",img)      