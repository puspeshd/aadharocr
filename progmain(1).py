import pandas as pd
import regex as re
import requests
from fileinput import filename
import os
from flask import Flask, request, render_template
import cv2
from flask_cors import CORS,cross_origin
import fitz
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='chetan.json'
from google.cloud import vision
vision_client = vision.ImageAnnotatorClient()
import datetime
import numpy


	

app = Flask(__name__,root_path="/test")
CORS(app)
current_time1=datetime.datetime.now()
current_time1=str(current_time1)
current_time1=current_time1.replace(":","")
current_time1=current_time1.replace("-","")
current_time1=current_time1.replace(".","")
current_time1=current_time1.replace(" ","")
current_time1=current_time1+".jpg"
@app.route('/test', methods=["GET", "POST"])
def photoupd():
  try:
    if (request.method == "POST"):
        image_path = request.files["upd"]
        image_path.save(current_time1)
        image=cv2.imread(current_time1)
        name=current_time1
        print(type(image))
        image_path=image
        if(type(image)==numpy.ndarray):
           x='x'
            #name=name.replace(".pdf","")
        else:    
             os.rename(name,name.replace(".jpg",".pdf"))
             name=name.replace(".jpg",".pdf")
             print(name)
             doc=fitz.open(name)
             for i in range(doc.page_count):
                 page=doc[i]
                 image_path=page.get_pixmap()
                 print(image_path," **********")
                 name=name.replace(".pdf",".jpg")
                 print("TILL HERE PROBLEM IN SAVE")
                 image_path.save(name)
                 img=''
                 
                 image_path=[name,img,1,image_path]
        #print(name)  
        name=os.path.basename(name)
               
        img=cv2.imread(name)
        #img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ''' h,w,_=img.shape
        h,w=int(h),int(w)
        filesize=os.path.getsize(name)/1024
        print(filesize)
        if(filesize>500 and filesize<1000):
         img=cv2.resize(img,(w*(80//100),h*(80//100)))  
        elif(filesize>1000 and filesize<2500):
            img=cv2.resize(img,(w*60//100,h*60//100))
        elif(filesize>2500 and filesize<5000):
            img=cv2.resize(img,(w*30//100,h*30//100))
        elif(filesize>5000 and filesize<10000):    
         img=cv2.resize(img,(w*20//100,h*20//100))                       
        elif(filesize>10000):    
         img=cv2.resize(img,(w*10//100,h*10//100))                        
        
        print(name)         
        cv2.imwrite(name,img) '''    
        
        print(name,"IT IS GETTING")
        cv2.imwrite(name,img)
        print(12344234)
        return (image_path)
  
  except:
    errcode={"error_code":3,"error_message":"Could not read. Please Proceed with manual mode or upload again"}
    return(errcode) 
  return render_template("input.html")
@app.route('/test/results', methods=["GET", "POST"])
def mainfunc():
 try:
    image_path = photoupd()

    def pancard(strdf):

        listdf = strdf.split(",")
        try:
            finallist = []
            #print(listdf)
            for i in range(len(listdf)):
                listdf[i] = listdf[i].replace("'", "")
            for i in range(len(listdf)):
                if (listdf[i].find(" INCOME TAX DEPARTMENT") > -1):
                    listdf[i+5] = listdf[i+5].replace(" ", '')
                    if (listdf[i+5].isalnum() == True and listdf[i+5].isalpha() == False and listdf[i+1].find("Name") < 0):
                        listtemp = [listdf[i+1], listdf[i+2],
                                    listdf[i+3], listdf[i+5]]

                    elif (listdf[i+5].isalnum() == True and listdf[i+5].isalpha() == False and listdf[i+1].find("Name") > -1):
                        listtemp = [listdf[i+2], listdf[i+7],
                                    listdf[i+10], listdf[i+5]]

                    else:
                        tempstr = listdf[i+1]+listdf[i+2]
                        # tempstr=tempstr.replace("'","")
                        listtemp = [tempstr, listdf[i+3],
                                    listdf[i+4], listdf[i+6]]

                    finallist.append(listtemp)
                    break
            dictfinal = {"NAME": finallist[0][0], "FATHER_NAME": finallist[0]
                         [1], "DOB": finallist[0][2], "PAN_NO": finallist[0][3],"error_code":1,"error_message":"SUCCESS"}
            return (dictfinal)
        except:
            dictfinal = {"NAME": '', "FATHER_NAME": ''
                         , "DOB": '', "PAN_NO": '',"error_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
            return (dictfinal)

    def aadharcardf(strdf):
        listdf = strdf.split(",")
        try:
            finallist = []

            for i in range(len(listdf)):
                
                if (listdf[i].find("Government of India") > -1 or (listdf[i].find("GOVERNMENT OF INDIA") > -1)):
                    
                    if (len(listdf[i+5]) == 15):
                        listtemp = [listdf[i+2], listdf[i+3],
                                    listdf[i+4], listdf[i+5]]
                    elif (len(listdf[i+4]) == 15):

                        listtemp = [listdf[i+1], listdf[i+2],
                                    listdf[i+3], listdf[i+4]]
                    elif (len(listdf[i+7]) == 15 and listdf[i+4].find("Father") > -1):

                        listtemp = [listdf[i+2], listdf[i+5],
                                    listdf[i+6], listdf[i+7]]
                    elif (len(listdf[i+6]) == 15 and listdf[i+4].find("Father") > -1):
                        listtemp = [listdf[i+2], listdf[i+4],
                                    listdf[i+5], listdf[i+6]]
                    elif (len(listdf[i+6]) == 15 and listdf[i+4].find("Father") == -1):
                        temp = listdf[i+3].replace(" ", "")
                        if (temp.isalpha() == True):
                            tempstr = listdf[i+2]+" "+listdf[i+3]
                            listtemp = [tempstr, listdf[i+4],
                                        listdf[i+5], listdf[i+6]]
                        else:
                            listtemp = [listdf[i+2], listdf[i+3],
                                        listdf[i+4], listdf[i+5]]

                    elif (len(listdf[i+8]) == 15 and listdf[i+4].find("Father") > -1):
                        listtemp = [listdf[i+2], listdf[i+6],
                                    listdf[i+7], listdf[i+8]]
                        

                    finallist.append(listtemp)
                    break
            for i in finallist[0][1]:
                if(i.isalpha() == True):
                    finallist[0][1]=finallist[0][1].replace(i,"")
                elif(i == ":"):
                     finallist[0][1]=finallist[0][1].replace(i,"")
            if(bool(re.search("\d\d\d\d \d\d\d\d \d\d\d\d",finallist[0][3])==True)):
                pass
            else:
                            
                            abc=re.search(r"\d\d\d\d \d\d\d\d \d\d\d\d",strdf)
                            abc=abc.span()
                            ano=strdf[abc[0]:abc[1]+1]
                            finallist[0][3]=ano                
            dictfinal = {"Name": finallist[0][0], "DOB": finallist[0][1],
                         "GENDER": finallist[0][2], "AADHAR NO": finallist[0][3],"error_code":1,"error_message":"SUCCESS"}
            return (dictfinal)
        except:
            dictfinal = {"Name": '', "DOB": '',
                         "GENDER": '', "AADHAR NO": '',"error_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
            return (dictfinal)

    def aadharcardb(strdf):

        listdf = strdf.split(",")
        
        try:
            for i in range(len(listdf)):

                if (listdf[i].find("Address") > 0 or listdf[i].find("Addre") > 0):
                    listdf[i] = listdf[i].replace("Address", "")
                    listdf[i]=listdf[i].replace(" ","")
                    
                    if(len(listdf[i])<2):
                     listdf = listdf[i+1:]
                     break
                    else:
                        listdf=listdf[i:]
                        break
            for i in range(len(listdf)):
                tempo=listdf[i].lower()
                if (tempo.find("d o") > -1 or tempo.find("s o") > -1 or tempo.find("c o") > -1 or tempo.find("so:")>-1 or tempo.find("do:")>-1 or tempo.find("co:")>-1):
                    listdf = listdf[i+1:]
                    break
            print(listdf," CHECK HERE FOR FULL ADDRESS")
            for j in range( len(listdf)):
                
                if (len(listdf[j]) < 5 or listdf[j].find("1947") > -1 or listdf[j].find("VID") >-1 or listdf[j].find('uidai') > -1 or bool(re.search(" \d\d\d\d \d\d\d\d \d\d\d\d", listdf[j])) == True or listdf[j].find("Corp.")>-1 or listdf[j].find("Government of India")>-1 or listdf[j].find("Unique Identification Authority of India")>-1 or  listdf[j].find("AADHAAR")>-1):
                    listdf[j] = "puspesh@puspesh"
            y = listdf.count("puspesh@puspesh")
            x = len(listdf)-1
             
            while (x > -1):
                if (listdf[x] == "puspesh@puspesh"):
                    listdf.pop(x)
                    y = y-1
                x = x-1
            #print(listdf," CHECK HERE")
            #print(listdf)
            for i in range(len(listdf)):
                listdf[i]=listdf[i].replace(":","")
                temppincode='x'
                if (bool(re.search("\D\d\d\d\d\d\d", listdf[i])) == True):
                    temppincode=listdf[i]
                    
                    
                    listdf1=listdf[i+1:]
                    listdf = listdf[0:i]
                    
                    break
            #print(temppincode)    
            for i in range(len(listdf)):
                if (str(listdf[i]).find("560 001") > -1):
                    listdf.pop(i)
                    break
            #print(listdf," CHECK HERE 3333 ",temppincode)   
            #print(listdf,"  THIS IS THE LIST AFTER address HELLO ")
            
            params = {'address': str(listdf)+temppincode,'key': 'AIzaSyDISrKu3mOEE100DwCDUvNsTeCssciGh4o'}
            jsonfromgoogle = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
            dfgoogle = pd.read_json(jsonfromgoogle.text)
            strgoogle = dfgoogle['results']
            addgoogle = str(strgoogle[0]['formatted_address'])
            
            #print(type(addgoogle))
            #print(addgoogle)
            latgoogle = str(strgoogle[0]['geometry']['location']['lat'])
            lnggoogle = str(strgoogle[0]['geometry']['location']['lng'])
            #print(latgoogle,lnggoogle)
            
            addgoogle = addgoogle.split(",")
            temp=listdf[0].replace(" ","")
            #print(temp)   
            
            #print(addgoogle)
            if(temp.isalpha()):
             houseno='' 
             
            else: 
             houseno = listdf[0]
             listdf=listdf[1:]
            #print(houseno)
            tempstate = addgoogle[len(addgoogle)-2]
            #print(tempstate,"TILL HERE EEE")
            state = ''
            gpin = ''
            
            city = addgoogle[len(addgoogle)-3]
            
            #print(addgoogle," GOOGLE ADDRESS")      #running till here
            
            #print(tempcity)    
            tempstate = re.sub(" ", "", tempstate)
            #print(tempstate)
            country = addgoogle[len(addgoogle)-1]
            if(country.find("India")==-1):
                country="India"
            for i in tempstate:
                if (i.isalpha()):
                    state = state+i
                elif (i.isdigit()):
                    gpin = gpin+i
            pincode = ''
            #print(state,city)                #now till here 
            for i in temppincode:
                if (i.isdigit()):
                    pincode = pincode+i
           
            
            #print(pincode)
            if (pincode.find(gpin) > -1):
                flag = 'VERIFIED FROM GOOGLE MAPS API'
            else:
                flag = ' NOT VERIFIED FROM GOOGLE MAPS API'   
                pincode=gpin
            #print(pincode,flag)          
            #print(pincode," PIN CODE IS ALL RIGHT ",houseno)
            #print(city," THIS IS THE CITY")
            #print(str(listdf).find(city),"THIS ARE THE SEARCH RESULTS FOR CITY")
            if(str(listdf).find(city)>-1):
             for i in range(len(listdf)):
                if (listdf[i].find(str(city)) > -1) :
                   
                   listdf.pop(i)
                   #listdf.pop(len(listdf)-1)
                   break
                elif(temppincode.find(city)>-1):
                    #print(temppincode,city)
                    break
            
            if(str(listdf).find(state)>-1):
                for i in range(len(listdf)):
                    if(listdf[i].find(state)>-1):
                        listdf.pop(i)

            #print(listdf, "THIS IS THE FINAL LIST")          
            #print(listdf," THIS IS AADHAR ADDRESS")    
            #print(addgoogle," THIS IS GOOGLE ADDRESS")    
            xxx = len(listdf)
            #print(listdf)
            #print(len(listdf))
            if(xxx==0):
                locality = ''
                street = ''
                buildingname = ''
            elif (xxx == 1 ):
                locality = listdf[0]
                street = ''
                buildingname = ''

            elif (xxx == 2):
                locality = listdf[1]
                street = ''
                buildingname = listdf[0]
            elif (xxx == 3):
                locality = listdf[2]
                street = listdf[1]
                buildingname = listdf[0]
            elif (xxx == 4):
                locality = listdf[2]+listdf[3]
                street = listdf[1]
                buildingname = listdf[0]
            elif (xxx == 5):
                locality = listdf[3]+listdf[4]
                street = listdf[1]+listdf[2]
                buildingname = listdf[0]
            elif (xxx == 6):
                locality = listdf[3]+listdf[4]+listdf[5]
                street = listdf[1]+listdf[2]
                buildingname = listdf[0]
            elif (xxx == 7):
                locality = listdf[4]+listdf[5]+listdf[6]
                street = listdf[1]+listdf[2]+listdf[3]
                buildingname = listdf[0]
            elif (xxx == 8):
                locality = listdf[4]+listdf[5]+listdf[6]+listdf[7]
                street = listdf[1]+listdf[2]+listdf[3]
                buildingname = listdf[0]
            elif (xxx == 9):
                locality = listdf[5]+listdf[6]+listdf[7]+listdf[8]
                street = listdf[1]+listdf[2]+listdf[3]+listdf[4]
                buildingname = listdf[0]
            
            #print(temppincode)
           
            #print(listdf)
            #print(addgoogle ,"TJIS IS GOOGLE ADDRESS")
            
            addfinal = {"Flag": flag, "House_no": houseno, "Building_name": buildingname, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pincode, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle,"error_code":1,"error_message":"SUCCESS"}
            return(addfinal)
        except:
            addfinal = {"Flag": '' ,"House_no": '', "Building_name": '', "locality": '', "street": '', "city": '', "state": '', "country": '', "PIN": '', "LATITUDE": '', "LONGITUDE": '',"error_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
            return(addfinal)
    def aadharfull(strdf):
             
        
        #strdf = strdf[175:]
        
        # print(strdf)
        listdf = strdf.split(",")
        #print(listdf," ORIGINAL LIST")
        #print(listdf)
        finallist = []
        try:
            listdf=strdf.split(",")
            for i in range(len(listdf)):
               
               if(len(listdf[i])<5):
                    listdf[i]="REMOVEME"
            x=len(listdf)-1
            while(x>-1):
                if(listdf[x]=="REMOVEME"):
                 listdf.pop(x)
                x=x-1         
            #print(listdf," THIS WOULD BE FINAL LIST")    
            for i in range(len(listdf)):
                if(listdf[i].lower().replace(" ","")=='male' or listdf[i].lower().replace(" ","")=='female'):
                    gender=listdf[i]
                    
                    #print(listdf," LIST AFTER TRIMMING WITH GENDER FLAG")
                    
                    dob=listdf[i-1]
                    
                    name=listdf[i-2]
                    dob=dob.replace("DOB:","") 
                    if(dob.replace(" ","").isalpha()):
                        dob=listdf[i+1]
                        name=listdf[i-1]   
                    listdf=listdf[i-6:i+6]
                    break
                
            for i in range(len(listdf)):
                if(bool(re.search("\d\d\d\d \d\d\d\d \d\d\d\d",listdf[i]))==True):
                    ano=listdf[i]
                    break
            #print(listdf)    
            #print(name,dob,gender,ano," THIS IS THE FINAL DATA")        
            
            dictfinal = {"Name": name, "DOB": dob,
                         "GENDER": gender, "AADHAR NO": ano}
            

            
            listdf=strdf.split(",")
            
            
            for i in range(len(listdf)):

                if (listdf[i]==" To" ):
                    #print(i)
                    listdf = listdf[i+1:]
                    
                    break
                    
            for i in range(len(listdf)):
                tempo=listdf[i].lower()
                if ((tempo.find("d o") > -1 or tempo.find("s o") > -1 or tempo.find("c o") > -1) or tempo.find("so:")>-1 or tempo.find("co:")>-1 or tempo.find("do:")>-1 ):
                    listdf = listdf[i+1:]
                    break
            
            for j in range( len(listdf)):
                
                if (len(listdf[j]) < 5 or listdf[j].find("1947") > -1 or listdf[j].find("VID") >-1 or listdf[j].find('uidai') > -1 or bool(re.search(" \d\d\d\d \d\d\d\d \d\d\d\d", listdf[j])) == True or listdf[j].find("Corp.")>-1 or listdf[j].find("Government of India")>-1 or listdf[j].find("Unique Identification Authority of India")>-1 or listdf[j].replace(" ","").isdigit() or listdf[j].find(name)>-1):
                    listdf[j] = "puspesh@puspesh"
            y = listdf.count("puspesh@puspesh")
            x = len(listdf)-1
            #print(listdf,"  THIS IS THE LIST AFTER TO ") 
            while (x > -1):
                if (listdf[x] == "puspesh@puspesh"):
                    listdf.pop(x)
                    y = y-1
                x = x-1
            #print(listdf," CHECK HERE")
            #print(listdf)
            for i in range(len(listdf)):
                
                if (bool(re.search("\D\d\d\d\d\d\d", listdf[i])) == True):
                    temppincode=listdf[i]
                    
                    #print(temppincode," CHECK HERE 222")
                    listdf1=listdf[i+1:]
                    listdf = listdf[0:i]
                    
                    break
            #print(listdf)    
            for i in range(len(listdf)):
                if (str(listdf[i]).find("560 001") > -1):
                    listdf.pop(i)
                    break
            #print(listdf," CHECK HERE 3333")   
            
            params = {'address': str(listdf)+temppincode,'key': 'AIzaSyDISrKu3mOEE100DwCDUvNsTeCssciGh4o'}
            jsonfromgoogle = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
            dfgoogle = pd.read_json(jsonfromgoogle.text)
            strgoogle = dfgoogle['results']
            addgoogle = str(strgoogle[0]['formatted_address'])
            
            #print(type(addgoogle))
            #print(addgoogle)
            latgoogle = str(strgoogle[0]['geometry']['location']['lat'])
            lnggoogle = str(strgoogle[0]['geometry']['location']['lng'])
            #print(latgoogle,lnggoogle)
            
            addgoogle = addgoogle.split(",")
            temp=listdf[0].replace(" ","")
            #print(temp)   
            
            if(temp.isalpha()):
             houseno='' 
            else: 
             houseno = listdf[0]
             listdf=listdf[1:]
            
            tempstate = addgoogle[len(addgoogle)-2]
            #print(tempstate,"TILL HERE EEE")
            state = ''
            gpin = ''
            
            city = addgoogle[len(addgoogle)-3]
            
            #print(addgoogle," GOOGLE ADDRESS")      #running till here
            
            #print(tempcity)    
            tempstate = re.sub(" ", "", tempstate)
            #print(tempstate)
            country = addgoogle[len(addgoogle)-1]
            if(country.find("India")==-1):
                country="India"
            for i in tempstate:
                if (i.isalpha()):
                    state = state+i
                elif (i.isdigit()):
                    gpin = gpin+i
            pincode = ''
            #print(state,city)                #now till here 
            for i in temppincode:
                if (i.isdigit()):
                    pincode = pincode+i
           
            
            #print(pincode)
            if (pincode.find(gpin) > -1):
                flag = 'VERIFIED FROM GOOGLE MAPS API'
            else:
                flag = ' NOT VERIFIED FROM GOOGLE MAPS API'   
            #print(pincode,flag)          
            
            for i in range(len(listdf)):
                if (listdf[i].find(city) > -1 ):
                   #print(len(listdf))
                   listdf.pop(i)
                   #listdf.pop(len(listdf)-1)
                   break
                elif(temppincode.find(city)>-1):
                    #print(temppincode,city)
                    break
                else:
                   if(listdf[len(listdf)-1].find(state)>-1):
                    city=listdf[len(listdf)-2]
                    if(city.find("District:")>-1):
                        city=city.replace("District:","")
                        listdf=listdf[0:(len(listdf)-2)]  
                        break                    

                     
                   else:  
                    city=listdf[len(listdf)-1]
                    listdf.pop(len(listdf)-1)  
                    break 
                      
            #print(listdf," THIS IS AADHAR ADDRESS")    
            #print(addgoogle," THIS IS GOOGLE ADDRESS")    
            xxx = len(listdf)
            #print(listdf)
            #print(len(listdf))
            if(xxx==0):
                locality = ''
                street = ''
                buildingname = ''
            elif (xxx == 1 ):
                locality = listdf[0]
                street = ''
                buildingname = ''

            elif (xxx == 2):
                locality = listdf[1]
                street = ''
                buildingname = listdf[0]
            elif (xxx == 3):
                locality = listdf[2]
                street = listdf[1]
                buildingname = listdf[0]
            elif (xxx == 4):
                locality = listdf[2]+listdf[3]
                street = listdf[1]
                buildingname = listdf[0]
            elif (xxx == 5):
                locality = listdf[3]+listdf[4]
                street = listdf[1]+listdf[2]
                buildingname = listdf[0]
            elif (xxx == 6):
                locality = listdf[3]+listdf[4]+listdf[5]
                street = listdf[1]+listdf[2]
                buildingname = listdf[0]
            elif (xxx == 7):
                locality = listdf[4]+listdf[5]+listdf[6]
                street = listdf[1]+listdf[2]+listdf[3]
                buildingname = listdf[0]
            elif (xxx == 8):
                locality = listdf[4]+listdf[5]+listdf[6]+listdf[7]
                street = listdf[1]+listdf[2]+listdf[3]
                buildingname = listdf[0]
            elif (xxx == 9):
                locality = listdf[5]+listdf[6]+listdf[7]+listdf[8]
                street = listdf[1]+listdf[2]+listdf[3]+listdf[4]
                buildingname = listdf[0]
            
            #print(temppincode)
           
            #print(listdf)
            #print(addgoogle ,"TJIS IS GOOGLE ADDRESS")
            
            addfinal = {"Flag": flag, "House no": houseno, "Building_name": buildingname, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pincode, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle,"error_code":1,"error_message":"Success"}
            #print(addfinal)
            #print(strdf)
            #print(len(strdf))
            
            
            
            dictfinal.update(addfinal)    
            #print(dictfinal)
            return (dictfinal)
        except:
            addfinal = {"Name": '', "DOB": '',"GENDER": '', "AADHAR NO": '',"Flag": '' ,"House no": '', "Building_name": '', "locality": '', "street": '', "city": '', "state": '', "country": '', "PIN": '', "LATITUDE": '', "LONGITUDE": '',"error_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
            return (addfinal)
    url = 'https://verify.bluealgo.com/pan'

    headers = {}

    
    if(type(image_path)!=list):
      #print(,"HEEEEEEEEE")
      xx = open(current_time1,'rb')
      xx:bytes=xx.read()
      image = vision.Image(content=xx)
      try:
        response = vision_client.text_detection(image=image)
        txt= response.text_annotations[0].description
        li = list(txt.split("\n"))
        response={'result':li}	
        print(li,"WORKING TILLHERE")	
      except:
          pass  
     
    else:
      xx = open(image_path[0],'rb')
      xx:bytes=xx.read()
      image = vision.Image(content=xx)
      try:
            response = vision_client.text_detection(image=image)	
            txt= response.text_annotations[0].description
            li = list(txt.split("\n"))
            response={'result':li}
      except:
          pass      

       
    current_time=datetime.datetime.now()
    current_time=str(current_time)
    current_time=current_time.replace(":","")
    current_time=current_time.replace("-","")
    current_time=current_time.replace(".","")
    current_time=current_time.replace(" ","")
    #print(str(response).encode('utf-8'))
    try:
     x=cv2.imread(current_time1)
     cv2.imwrite("images/"+current_time+".jpg",x)
     #image_path.save()
     #os.remove(image_path.filename)     to be added later
     #print(image_path)
     os.remove(current_time1)
    except:
        
        image_path[3].save("images/"+current_time+".jpg")
        os.remove(current_time1)
        os.remove(str(image_path[0].replace(".jpg", ".pdf"))) 
    xxyx='images/'+current_time+'.jpg'
    print(xxyx)
    img=cv2.imread(xxyx)
    print(type(img))
    print(img.shape)
    h,w,_=img.shape
    h,w=int(h),int(w)
    print(h,w,"SADDAXS")
    
    print(xxyx,"PAPPI")
    filesize=os.path.getsize(xxyx)/1024
    print(filesize,"JAISHREERAM")
    if(filesize>150 and filesize<1000):
         img=cv2.resize(img,(w*(80//100),h*(80//100)))  
    elif(filesize>1000 and filesize<2500):
            img=cv2.resize(img,(w*60//100,h*60//100))
    elif(filesize>2500 and filesize<5000):
            img=cv2.resize(img,(w*30//100,h*30//100))
    elif(filesize>5000 and filesize<10000):    
         img=cv2.resize(img,(w*20//100,h*20//100))                       
    elif(filesize>10000):    
         img=cv2.resize(img,(w*10//100,h*10//100)) 
    cv2.imwrite('images/'+current_time+".jpg",img)    
    print("CHECKING FOR THIS SKAKJBSJFB")
    try:
        df = response
        strdf = list(df["result"])
        strdf = str(strdf).encode("utf-8")
        strdf = str(strdf)
        #print(strdf)
        strdf = strdf.replace("\\", "")
        strdf = strdf.replace("|", "")
        strdf = strdf.replace("/", " ")
        strdf = strdf.replace("'\'", " ")
        strdf = strdf.replace("'", "")
        strdf = strdf.replace("\n", " ")
        strdf = re.sub("x..", "", strdf)
        strdf = strdf.replace("(","")
        strdf = strdf.replace(")","")
    except:
        strdf='lol'    
    #print(len(strdf))
    # print(type(strdf))
    if (strdf.find("INCOME TAX DEPARTMENT") > 1):
        results = pancard(strdf)
    elif (strdf.find("Government of India") > -1 and (strdf.find("Unique Identification Authority of India") > -1 or strdf.find("UNIQUE IDENTIFICATION AUTHORITY OF INDIA") > -1)):
        results = aadharfull(strdf)
    elif (strdf.find("Government of India") > 0 or strdf.find("GOVERNMENT OF INDIA") > 0):
        results = aadharcardf(strdf)
    elif (strdf.find("Unique Identification Authority of India") > 1):
        results = aadharcardb(strdf)
    elif (strdf.find("UNIQUE IDENTIFICATION AUTHORITY OF INDIA") > 1):
        results = aadharcardb(strdf)
    elif(len(strdf)<10):
        results = {"error_message":"NO TEXT FOUND "}
    else:
        results={"error_message":"UNIDENTIFIED DOCUMENT"}    
    #print(results)    
    current_time=current_time+".jpg"    
    file_name={"file_name":current_time}
    results.update(file_name)
    return results
 except:
    errcode={"error_code":3,"error_message":"Could not read. Please Proceed with manual mode or upload again"}
    return(errcode)  

if __name__ == '__main__':
    app.run(host="0.0.0.0")
