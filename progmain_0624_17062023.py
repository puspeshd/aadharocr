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


	

app = Flask(__name__)
CORS(app)
current_time1=datetime.datetime.now()
current_time1=str(current_time1)
current_time1=current_time1.replace(":","")
current_time1=current_time1.replace("-","")
current_time1=current_time1.replace(".","")
current_time1=current_time1.replace(" ","")


current_time1=current_time1+".jpg"
x=0
@app.route('/test', methods=["GET", "POST"])
  
def photoupd():
  
  
  
    
    if (request.method == "POST"):
        image_path = request.files["upd"]
        print(type(image_path))
        image_path.save(image_path.filename)
        name=image_path.filename
        print(name)
        #name=name.replace(".pdf","")
        print(name, "THIS IS DOC NAME")
        if(name.find(".pdf")>-1):
             doc=fitz.open(name)
             for i in range(doc.page_count):
                 page=doc[i]
                 image_path=page.get_pixmap()
                 print(image_path," **********")
                 name=name.replace(".pdf",".jpg")
                 image_path.save(name)
                 img=''
                 
                 image_path=[name,img,1,image_path]
        
        return (image_path)
    
    return render_template("input.html")
@app.route('/test/results', methods=["GET", "POST"])
def mainfunc():
   #logfile=open("logs/"+str(datetime.datetime.now().microsecond)+".txt","w+")
   
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
            
        except:
            dictfinal = {"NAME": '', "FATHER_NAME": ''
                         , "DOB": '', "PAN_NO": '',"error_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
        #logfile.write("\n"+str(dictfinal)+" FINAL PAN CARD LIST ")
        return (dictfinal)

    def aadharcardf(strdf):
        listdf = strdf.split(",")
        try:
            finallist = []
            #logfile.write("\n"+str(listdf)+" THIS IS OCR DATA CONVERTED TO LIST BY COMMA SEPERATION")
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
            
            
        except:
            dictfinal = {"Name": '', "DOB": '',
                         "GENDER": '', "AADHAR NO": '',"error_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
        #logfile.write("\n"+str(dictfinal)+" THIS IS FINAL AADHAR FRONT RESULT")
        return (dictfinal)

    def aadharcardb(strdf):
        
        listdf = strdf.split(",")
        #logfile.write("\n"+str(listdf)+"THIS IS LIST CONVERTED AFTER FORMATTING FROM OCR RECEIVE")
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
                
                if (len(listdf[j]) < 3 or listdf[j].find("1947") > -1 or listdf[j].find("VID") >-1 or listdf[j].find('uidai') > -1 or bool(re.search(" \d\d\d\d \d\d\d\d \d\d\d\d", listdf[j])) == True or listdf[j].find("Corp.")>-1 or listdf[j].find("Government of India")>-1 or listdf[j].find("Unique Identification Authority of India")>-1 or  listdf[j].find("AADHAAR")>-1):
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
            #logfile.write("\n"+str(listdf)+"THIS IS LIST after removing unnecessary elements ")
            addgoogle = addgoogle.split(",")
            #logfile.write("\n"+str(addgoogle)+"This is google response (formatted)")
            temp=listdf[0].replace(" ","")
            #print(temp)   
            
            #print(addgoogle)
            if(temp.isalpha()):
             houseno='' 
             
            else: 
             houseno = listdf[0]
             listdf=listdf[1:]
            #print(houseno)
            #logfile.write("\n"+str(listdf)+"THIS IS LIST AFTER EXTRACTING HOUSE NO ="+str(houseno))
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
            pincode = gpin
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
                
                if (listdf[i].find(city) > -1 ):
                   #print(len(listdf))
                   listdf.pop(i)
                   #listdf.pop(len(listdf)-1)
                   break
                
                
                if(listdf[len(listdf)-1].find(state)>-1):
                    listdf.pop(len(listdf)-1)
                    break
                str(listdf).replace("State","")

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
            #..##logfile.write("\n"+str(addfinal)+"THIS IS FINAL RESULT OF AADHAR BACK")
            
        except:
            addfinal = {"Flag": '' ,"House_no": '', "Building_name": '', "locality": '', "street": '', "city": '', "state": '', "country": '', "PIN": '', "LATITUDE": '', "LONGITUDE": '',"error_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
        #logfile.write("\n"+str(addfinal)+"THIS IS FINAL RESULT OF AADHAR BACK")
        return(addfinal)
    def aadharfull(strdf):
             
        
        finallist = []
        try:
            listdf = strdf.split(",")
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
                        dob=dob.replace("DOB","")
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
            #logfile.write("\n"+str(dictfinal)+"THIS IS  RESULT OF AADHAR FULL NAME SIDE")

            
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
            #logfile.write("\n"+str(listdf)+"THIS IS LIST AFTER REMOVING UNNECESARY DATA INCLUDING SO / DO etc")

            for j in range( len(listdf)):
                
                if (len(listdf[j]) < 2 or listdf[j].find("1947") > -1 or listdf[j].find("VID") >-1 or listdf[j].find('uidai') > -1 or bool(re.search(" \d\d\d\d \d\d\d\d \d\d\d\d", listdf[j])) == True or listdf[j].find("Corp.")>-1 or listdf[j].find("Government of India")>-1 or listdf[j].find("Unique Identification Authority of India")>-1 or listdf[j].replace(" ","").isdigit() or listdf[j].find(name)>-1):
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
            #logfile.write("\n"+str(listdf)+"THIS IS LIST AFTER REMOVING UNNECESARY DATA INCLUDING SO / DO etc and extracting pincode")
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
            pincode = gpin
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
                
                
            if(listdf[len(listdf)-1].find(state)>-1):
                    listdf.pop(len(listdf)-1)
                    
            str(listdf).replace("State","")
                         
                      
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
           
            
            #print(addgoogle ,"TJIS IS GOOGLE ADDRESS")
            
            addfinal = {"Flag": flag, "House no": houseno, "Building_name": buildingname, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pincode, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle,"error_code":1,"error_message":"Success"}
            #print(addfinal)
            #print(strdf)
            #print(len(strdf))
            
            
            
            dictfinal.update(addfinal)   
            print("YAHA TAK CHAL RAHA HAI strdf") 
            #print(dictfinal)
            ##logfile.write("\n"+str(dictfinal)+"THIS IS FINAL AADHAR FULL/STRIP RESULTS")
            #return (dictfinal)
        except:
            addfinal = {"Name": '', "DOB": '',"GENDER": '', "AADHAR NO": '',"Flag": '' ,"House no": '', "Building_name": '', "locality": '', "street": '', "city": '', "state": '', "country": '', "PIN": '', "LATITUDE": '', "LONGITUDE": '',"error_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
        #logfile.write("\n"+str(addfinal)+"THIS IS FINAL AADHAR FULL/STRIP RESULTS")
        return (dictfinal)
    
    
    if(type(image_path)!=list):
      #print(,"HEEEEEEEEE")
      xx = open(image_path.filename,'rb')
      xx:bytes=xx.read()
      image = vision.Image(content=xx)
      try:
        response = vision_client.text_detection(image=image)
        txt= response.text_annotations[0].description
        li = list(txt.split("\n"))
        response={'result':li}		
      except:
          pass  
     
    else:
      xx = open(image_path[0],'rb')
      xx=xx.read()
      image = vision.Image(content=xx)
      print("PURV")
      try:
            response = vision_client.text_detection(image=image)	
            txt= response.text_annotations[0].description
            li = list(txt.split("\n"))
            response={'result':li}
            #print(response, "PDF RESPONES")
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
     image_path.save("images/"+current_time+".jpg")
     #image_path.save()
     os.remove(image_path.filename)     
     #print(image_path)
     
    except:
        
        image_path[3].save("images/"+current_time+".jpg")
        os.remove(image_path[0])
        os.remove(str(image_path[0].replace(".jpg", ".pdf"))) 
    try:
        df = response
        strdf = list(df["result"])
        strdf = str(strdf).encode("utf-8")
        strdf = str(strdf)
        
        strdf = strdf.replace("\\", "")
        strdf = strdf.replace("|", "")
        strdf = strdf.replace("/", "")
        strdf = strdf.replace("'\'", "")
        strdf = strdf.replace("'", "")
        strdf = strdf.replace("\n", "")
        strdf = re.sub("x..", "", strdf)
        strdf = strdf.replace("(","")
        strdf = strdf.replace(")","")
    except:
        strdf='lol' 
    print(strdf)       
    #logfile.write("\n"+strdf+"THIS IS OCR RESPONSE IN STRING FORMAT")    
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
    elif(len(strdf)<4):
        results = {"error_message":"NO TEXT FOUND "}
        ##logfile.write("\n"+str(results))
    else:
        results={"error_message":"UNIDENTIFIED DOCUMENT"}    
    print(results,"HO HO HO HOO HOO HOO HOO HOO HOO H")    
    current_time=current_time+".jpg"    
    file_name={"file_name":current_time}
    results.update(file_name)
    #logfile.write("\n"+str(results)+"::::::::::::::: FINAL RESPONSE")
    ###logfile.close()
    
 
    ##logfile.close()
    return results     
    

if __name__ == '__main__':
     
     app.run(host="0.0.0.0")
