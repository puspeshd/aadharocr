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
import logging

	

app = Flask(__name__)
#app= Flask(__name__,root_path="/newapp")
CORS(app)
current_time1=datetime.datetime.now()
current_time1=str(current_time1)
current_time1=current_time1.replace(":","")
current_time1=current_time1.replace("-","")
current_time1=current_time1.replace(".","")
current_time1=current_time1.replace(" ","")

logging.basicConfig(level=logging.DEBUG,filename="logs/"+current_time1+".log")


current_time1=current_time1+".jpg"

@app.route('/newapp', methods=["GET", "POST"])
  
def photoupd():
  
  
  
    
    if (request.method == "POST"):
        image_path = request.files["upd"]
        print(type(image_path))
        image_path.save(image_path.filename)
        logging.info("FILE RECIEVED TO API")
        name=image_path.filename
        print(name)
        #name=name.replace(".pdf","")
        print(name, "THIS IS DOC NAME")
        if(name.find(".pdf")>-1):
             doc=fitz.open(name)
             for i in range(doc.page_count):
                 page=doc[0]
                 image_path=page.get_pixmap(dpi=200)
                 print(image_path," **********")
                 name=name.replace(".pdf",".jpg")
                 image_path.save(name)
                 img=''
                 
                 image_path=[name,img,1,image_path]
        logging.info(f"{str(image_path)} THIS IS TO BE RETURNED TO OCR ")
        return (image_path)
    return render_template("input.html")
@app.route('/newapp/results', methods=["GET", "POST"])
def mainfunc():
   
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
            finallist[0][0]=finallist[0][0].title()    
            dictfinal = {"NAME": finallist[0][0], "FATHER_NAME": finallist[0]
                         [1], "DOB": finallist[0][2], "PAN_NO": finallist[0][3],"status_code":1,"status_message":"SUCCESS"}
            logging.info(str(dictfinal)+"SUCCESS FOR PAN CARD")           
        except:
            dictfinal = {"NAME": '', "FATHER_NAME": ''
                         , "DOB": '', "PAN_NO": '',"status_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
            logging.error(dictfinal,Exception,"ERROR FOR PAN CARD")
        
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
                         "GENDER": finallist[0][2], "AADHAR NO": finallist[0][3],"status_code":1,"status_message":"SUCCESS"}
            
            logging.info(f"{str(dictfinal)} ::: SUCCESS In AADHAR FRONT ")
        except:
            dictfinal = {"Name": '', "DOB": '',
                         "GENDER": '', "AADHAR NO": '',"status_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
            logging.error(f"{str(dictfinal)} ::: ERROR IN AADHAR FRONT ")
        return (dictfinal)

    def aadharcardb(strdf):
        
        listdf = strdf.split(",")
        #logfile.write("\n"+str(listdf)+"THIS IS LIST CONVERTED AFTER FORMATTING FROM OCR RECEIVE")
        try:
            for i in range(len(listdf)):

                if (listdf[i].find("Address") > 0 or listdf[i].find("Addre") > 0):
                    listdf[i] = listdf[i].replace("Address", "")
                    listdf[i]=listdf[i].replace(" ","")
                    
                    if(len(listdf[i])<3):
                     listdf = listdf[i+1:]
                     break
                    else:
                        listdf=listdf[i:]
                        break
            logging.info(f"{str(listdf)}:::: INITIAL LIST")
            for i in range(len(listdf)):
                tempo=listdf[i].lower()
                if (tempo.find("d o") > -1 or tempo.find("s o") > -1 or tempo.find("c o") > -1 or tempo.find("so:")>-1 or tempo.find("do:")>-1 or tempo.find("co:")>-1):
                    listdf = listdf[i+1:]
                    break
            
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
            logging.info(f"{str(addgoogle)}:::: GOOGLE PLACES LIST")
            #logfile.write("\n"+str(addgoogle)+"This is google response (formatted)")
            temp=listdf[0].replace(" ","")
            #print(temp)   
            
            #print(addgoogle)
            houseno=''
            for i in range(0,2):
                if(listdf[i].replace(" ", "").isalpha()==False):
                    houseno=listdf[i]
                    listdf=listdf[i+1:]
                    break
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
            pincode = ''
            #print(state,city)                #now till here 
            for i in temppincode:
                if (i.isdigit()):
                    pincode = pincode+i
            if(len(str(pincode))<3):
               pincode=gpin
            
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
            
            #print(listdf)
            #print(len(listdf))
            logging.info(f"{str(listdf)}:::: LIST FOR PACKING ")
            listdf1=listdf.copy()
            listdf1.insert(0,houseno)
            listdf1.append(city)
            listdf1.append(state)
            listdf1.append(country)
            lent=0
            for lst in listdf1:
                lent=lent+len(lst)
            

            if(lent>120):
                for i in range(len(listdf1)):            #to remove starting spaces
                  if(listdf1[i].startswith(" ")):
                    listdf1[i]=listdf1[i][1:]
                
                
                for i in range(len(listdf1)-3):
                    if(listdf1[i].find(city)>-1 or listdf1[i].find(state)>-1 or listdf1[i].find(country)>-1 or listdf1[i].lower().find("district")>-1 or listdf1[i].find("State")>-1 or listdf1[i].lower().find("country")>-1):
                        listdf1[i]=''
                x=len(listdf1)-1
                while x>=0:
                    if(listdf1[x]==''):
                        listdf1.pop(x)
                    x=x-1    
                lent=0
                for lst in listdf1:
                    lent=lent+len(lst)              
                if(lent>120):
                    buildingname=listdf1[1]
                    locality=addgoogle[2]
                    street=addgoogle[1]
                    xxx=-1
                    logging.info("NOT ABLE TO SET MIN LENGTH, USING GOOGLE PLACES ")
                else:
                    listdf1=listdf1[1:len(listdf1)-3]
                    listdf=listdf1.copy()        
                    logging.info("NO OF CHARS NOW BELOW 120 ..... now appending as per logic")   
                    xxx = len(listdf)      
            else:
                xxx=len(listdf)             
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
            
            if(len(locality)>39  or  len(street)>39  or len(buildingname)>39):
                    logging.info("FIRST PASS")
                    if (xxx == 6):
                        locality = listdf[4]+listdf[5]
                        street = listdf[2]+listdf[3]
                        buildingname = listdf[0]+listdf[1]
                    elif (xxx == 7):
                        locality = listdf[5]+listdf[6]
                        street = listdf[2]+listdf[3]+listdf[4]
                        buildingname = listdf[0]+listdf[1]
                    elif (xxx == 8):
                        locality = listdf[6]+listdf[7]
                        street = listdf[3]+listdf[4]+listdf[5]
                        buildingname = listdf[0]+listdf[1]+listdf[2]
                    elif (xxx == 9):
                        locality = listdf[7]+listdf[8]
                        street = listdf[4]+listdf[5]+listdf[6]
                        buildingname = listdf[0]+listdf[1]+listdf[2]+listdf[3]
            if(len(buildingname)>39 or len(street)>39 or len(locality)>39):
                    logging.info("SECOND PASS")
                    if (xxx == 6):
                        locality = listdf[5]
                        street = listdf[4]
                        buildingname = listdf[2]+listdf[3]
                        houseno=houseno+listdf[0]+listdf[1]
                    elif (xxx == 7):
                        locality = listdf[6]
                        street = listdf[4]+listdf[5]
                        buildingname = listdf[2]+listdf[3]
                        houseno=houseno+listdf[0]+listdf[1]
                    elif (xxx == 8):
                        locality = listdf[6]+listdf[7]
                        street = listdf[4]+listdf[5]
                        buildingname = listdf[2]+listdf[3]
                        houseno=houseno+listdf[0]+listdf[1]
                    elif (xxx == 9):
                        locality = listdf[7]+listdf[8]
                        street = listdf[5]+listdf[6]
                        buildingname = listdf[3]+listdf[4]
                        houseno=houseno+listdf[0]+listdf[1]+listdf[2]
            if(len(houseno)>39 or len(buildingname)>39 or len(locality)>39 or len(street)>39):
                logging.info("PASS 3 TRIM")
                houseno=list(houseno[:39])
                houseno="".join(houseno)
                buildingname=list(buildingname[:39])
                buildingname="".join(buildingname)
                locality=list(locality[:39])
                locality="".join(locality)
                street=list(street[:39])
                street="".join(street)
                        
            logging.info(f"{len(houseno)}:::HOUSE NO {len(buildingname)}:::BUILDING {len(locality)}:::::LOCALITY {len(street)}::::: STREET")       
            
            addfinal = {"Flag": flag, "House_no": houseno, "Building_name": buildingname, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pincode, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle,"status_code":1,"status_message":"SUCCESS"}
            logging.info(f"{str(addfinal)}:::: FINAL RESULTS ")
            #..##logfile.write("\n"+str(addfinal)+"THIS IS FINAL RESULT OF AADHAR BACK")
            
        except:
            addfinal = {"Flag": '' ,"House_no": '', "Building_name": '', "locality": '', "street": '', "city": '', "state": '', "country": '', "PIN": '', "LATITUDE": '', "LONGITUDE": '',"status_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
            logging.error(f"{str(addfinal)}:::: ERRORS IN AADHAR BACK")
        #logfile.write("\n"+str(addfinal)+"THIS IS FINAL RESULT OF AADHAR BACK")
        return(addfinal)
    def aadharfull(strdf):
             
        
        finallist = []
        try:
            listdf = strdf.split(",")
            gender=''
            dob=''
            name=''   
            ano=''    
            #print(listdf," THIS WOULD BE FINAL LIST")    
            for i in range(len(listdf)):
                if(listdf[i].lower().replace(" ","")=='male' or listdf[i].lower().replace(" ","")=='female' or listdf[i].lower().replace(" ","")=='mae'):
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
                elif(listdf[i].find("Address")>-1):
                    listdf=listdf[i+1:]
                    break
            logging.info(f"LIST AFTER TO {listdf}")    
                    
            for i in range(len(listdf)):
                tempo=str(listdf[i]).lower()
                if ((tempo.find("d o") > -1 or tempo.find("s o") > -1 or tempo.find("c o") > -1) or tempo.find("so:")>-1 or tempo.find("co:")>-1 or tempo.find("do:")>-1 ):
                    listdf = listdf[i+1:]
                    break
            logging.info(f"LIST after SO check {str(listdf)}")
            for j in range( len(listdf)):
                
                if (len(listdf[j]) < 5 or listdf[j].find("1947") > -1 or listdf[j].find("VID") >-1 or listdf[j].find('uidai') > -1 or bool(re.search(" \d\d\d\d \d\d\d\d \d\d\d\d", listdf[j])) == True or listdf[j].find("Corp.")>-1 or listdf[j].find("Government of India")>-1 or listdf[j].find("Unique Identification Authority of India")>-1 or  listdf[j].find(name)>-1):
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
            logging.info(f"LIST BEFORE FINDING PIN CODE {str(listdf)}")
            for i in range(len(listdf)):
                
                if (bool(re.search("\D\d\d\d\d\d\d", listdf[i])) == True):
                    temppincode=listdf[i]
                    
                    #print(temppincode," CHECK HERE 222")
                    
                    listdf = listdf[0:i]
                    
                    break
            logging.info(f"LIST AFTER FINDING PIN CODE {str(listdf)}")
            #print(listdf)    
            for i in range(len(listdf)):
                if (str(listdf[i]).find("560 001") > -1):
                    listdf.pop(i)
                    break
            #print(listdf," CHECK HERE 3333")   
            logging.info(f"SENT TO GOOGLE API : {listdf},{temppincode},PINCODE FROM AADHAR")
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
            logging.info(f"RESPONSE FROM GOOGLE API  {addgoogle}")
            temp=listdf[0].replace(" ","")
            #print(temp)   
            print(listdf)
            houseno=''
            for i in range(0,2):
                if(listdf[i].replace(" ", "").isalpha()==False):
                    houseno=listdf[i]
                    listdf=listdf[i+1:]
                    break
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
            logging.info("RUNNING BEFORE PINCODE OPERATION")
            #print(state,city)                #now till here 
            pincode=''
            for i in temppincode:
                if (i.isdigit()):
                    pincode = pincode+i
            if(len(str(pincode))<3):
                pincode=gpin
            logging.info("RUNNING AFTER PINCODE OPERATION")     
            #print(pincode)
            if (pincode.find(gpin) > -1):
                flag = 'VERIFIED FROM GOOGLE MAPS API'
            else:
                flag = ' NOT VERIFIED FROM GOOGLE MAPS API' 
                pincode=gpin  
            #print(pincode,flag)          
            
            for i in range(len(listdf)):
                if (listdf[i].find(city) > -1 ):
                   #print(len(listdf))
                   listdf.pop(i)
                   #listdf.pop(len(listdf)-1)
                   break
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
                
            logging.info(f"LIST FOR PACK {listdf}")
            listdf1=listdf.copy()
            listdf1.insert(0,houseno)
            listdf1.append(city)
            listdf1.append(state)
            listdf1.append(country)
            lent=0
            for lst in listdf1:
                lent=lent+len(lst)
            
            print(lent)
            if(lent>120):
                for i in range(len(listdf1)):            #to remove starting spaces
                  if(listdf1[i].startswith(" ")):
                    print("ERROR CHECK 1")
                    listdf1[i]=listdf1[i][1:]
                    
                print("ERROR CHECK 2")
                print(listdf1)
                rng=len(listdf1)-3
                for i in range(rng):
                    if((listdf1[i].find(city.lower()))>-1 or (listdf1[i].find(state.lower()))>-1 or  (listdf1[i].lower().find("district"))>-1 or (listdf1[i].find("State"))>-1 or (listdf1[i].lower().find("country"))>-1):
                        print("CHECK 11",i)
                        listdf1[i]=''
                        print("CHECK 22",i)    
                print("HERE")        
                x=len(listdf1)-1
                print(x)
                while x>=0:
                    if(listdf1[x]=='xxxxx'):
                        listdf1.pop(x)
                    print(x)
                    x=x-1   
                print("ERROR CHECK 3")     
                lent=0
                for lst in listdf1:
                    lent=lent+len(lst) 
                print("ALPHA")                 
                if(lent>120):
                    buildingname=listdf1[1]
                    locality=addgoogle[2]
                    street=addgoogle[1]
                    xxx=-1
                    logging.info("NOT ABLE TO SET MIN LENGTH, USING GOOGLE PLACES ")
                else:
                    listdf1=listdf1[1:len(listdf1)-3]
                    listdf=listdf1.copy()        
                    logging.info("NO OF CHARS NOW BELOW 120 ..... now appending as per logic")   
                    xxx = len(listdf)
            else:
                xxx=len(listdf)    
            print("ALPHA 1")        
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
            if(len(locality)>39  or  len(street)>39  or len(buildingname)>39):
                
                    if (xxx == 6):
                        locality = listdf[4]+listdf[5]
                        street = listdf[2]+listdf[3]
                        buildingname = listdf[0]+listdf[1]
                    elif (xxx == 7):
                        locality = listdf[5]+listdf[6]
                        street = listdf[2]+listdf[3]+listdf[4]
                        buildingname = listdf[0]+listdf[1]
                    elif (xxx == 8):
                        locality = listdf[6]+listdf[7]
                        street = listdf[3]+listdf[4]+listdf[5]
                        buildingname = listdf[0]+listdf[1]+listdf[2]
                    elif (xxx == 9):
                        locality = listdf[7]+listdf[8]
                        street = listdf[4]+listdf[5]+listdf[6]
                        buildingname = listdf[0]+listdf[1]+listdf[2]+listdf[3]
            if(len(buildingname)>39 or len(street)>39 or len(locality)>39):
                    logging.info("SECOND PASS")
                    if (xxx == 6):
                        locality = listdf[5]
                        street = listdf[4]
                        buildingname = listdf[2]+listdf[3]
                        houseno=houseno+listdf[0]+listdf[1]
                    elif (xxx == 7):
                        locality = listdf[6]
                        street = listdf[4]+listdf[5]
                        buildingname = listdf[2]+listdf[3]
                        houseno=houseno+listdf[0]+listdf[1]
                    elif (xxx == 8):
                        locality = listdf[6]+listdf[7]
                        street = listdf[4]+listdf[5]
                        buildingname = listdf[2]+listdf[3]
                        houseno=houseno+listdf[0]+listdf[1]
                    elif (xxx == 9):
                        locality = listdf[7]+listdf[8]
                        street = listdf[5]+listdf[6]
                        buildingname = listdf[3]+listdf[4]
                        houseno=houseno+listdf[0]+listdf[1]+listdf[2]
            if(len(houseno)>39 or len(buildingname)>39 or len(locality)>39 or len(street)>39):
                logging.info("PASS #3")
                houseno=list(houseno[:39])
                houseno="".join(houseno)
                buildingname=list(buildingname[:39])
                buildingname="".join(buildingname)
                locality=list(locality[:39])
                locality="".join(locality)
                street=list(street[:39])
                street="".join(street)        
            logging.info(f"{len(houseno)}:::HOUSE NO {len(buildingname)}:::BUILDING {len(locality)}:::::LOCALITY {len(street)}::::: STREET")       
            #print(temppincode)
            logging.info(f"{len(buildingname)} : BNAME {len(street)} : STREET {len(locality)} : LOCALITY ")
            #print(listdf)
            #print(addgoogle ,"TJIS IS GOOGLE ADDRESS")
            
            
            
            addfinal = {"Flag": flag, "House no": houseno, "Building_name": buildingname, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pincode, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle,"status_code":1,"status_message":"Success"}
            #print(addfinal)
            #print(strdf)
            #print(len(strdf))
            
            
            
            dictfinal.update(addfinal)   
            logging.info(f"{str(dictfinal)}:::: SUCCESS RESPONSE")
        except Exception as e:
            dictfinal = {"Name": '', "DOB": '',"GENDER": '', "AADHAR NO": '',"Flag": '' ,"House no": '', "Building_name": '', "locality": '', "street": '', "city": '', "state": '', "country": '', "PIN": '', "LATITUDE": '', "LONGITUDE": '',"status_code":2,"error_msg":"DIDN'T RECOGNIZE ,PLEASE PROCEED MANUALLY OR UPLOAD AGAIN"}
            logging.error(f"{str(dictfinal)}{e}:::: ERROR AADHAR STRIP")
        return (dictfinal)
    def fileresize(time):
        img=cv2.imread("images/"+time+".jpg")
        logging.info(f"{time}")
        print(time,"FINAAAAAAAA")
        size=os.path.getsize("images/"+time+".jpg")/1024
        h,w,_=img.shape
        if(size>100 and size<200):
         img1=cv2.resize(img,(w*90//100,h*90//100))
        elif(size>200 and size<500):
         img1=cv2.resize(img,(w*80//100,h*80//100))  
        elif(size>500 and size<700):
            img1=cv2.resize(img,(w*70//100,h*70//100))
        elif(size>700 and size<1000):
            img1=cv2.resize(img,(w*65//100,h*65//100))
        elif(size>1000 and size<2000):    
         img1=cv2.resize(img,(w*60//100,h*60//100))                       
        elif(size>2000):    
         img1=cv2.resize(img,(w*50//100,h*50//100))  
        else:
          img1=img    
        cv2.imwrite("images/"+time+".jpg",img1)  
        if(size>100 and size<200):
         img2=cv2.resize(img,(w*70//100,h*70//100))
        elif(size>200 and size<500):
         img2=cv2.resize(img,(w*55//100,h*55//100))  
        elif(size>500 and size<700):
         img2=cv2.resize(img,(w*40//100,h*40//100))
        elif(size>700 and size<1000):
            img2=cv2.resize(img,(w*30//100,h*30//100))
        elif(size>1000 and size<2000):    
         img2=cv2.resize(img,(w*25//100,h*25//100))                       
        elif(size>2000):    
         img2=cv2.resize(img,(w*20//100,h*20//100))   
        else:
            img2=img 
        cv2.imwrite("images/"+"compressed_"+time+".jpg",img2)
        
    if(type(image_path)!=list):
      #print(,"HEEEEEEEEE")
      xx = open(image_path.filename,'rb')
      xy:bytes=xx.read()
      image = vision.Image(content=xy)
      xx.close()
      try:
        response = vision_client.text_detection(image=image)
        txt= response.text_annotations[0].description
        li = list(txt.split("\n"))
        response={'result':li}		
      except:
          pass  
     
    else:
      xx = open(image_path[0],'rb')
      xy=xx.read()
      image = vision.Image(content=xy)
      xx.close()
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
     logging.info(f"{image_path}")
     xyz=cv2.imread(image_path.filename)
     cv2.imwrite("images/"+current_time+".jpg",xyz) 
     #image_path.save("images/"+current_time+".jpg")
     #image_path.save()
     os.remove(image_path.filename)     
     #print(image_path)
     logging.info(" jpg orig IMAGE SAVED TO SERVER") 
    except:
        
        xyz=cv2.imread(image_path[0])
        cv2.imwrite("images/"+current_time+".jpg",xyz)
        #image_path[3].save("images/"+current_time+".jpg")
        os.remove(image_path[0])
        os.remove(str(image_path[0]).replace(".jpg", ".pdf")) 
        logging.info("pdf to jpg IMAGE SAVED TO SERVER")
    try:
        df = response
        strdf = list(df["result"])
        strdf = str(strdf).encode("utf-8")
        strdf = str(strdf)
        #print(strdf)
        strdf = strdf.replace("\\", "")
        strdf = strdf.replace("|", "")
        strdf = strdf.replace("/", " ")
        strdf = strdf.replace("'", "")
        strdf = strdf.replace("\n", " ")
        strdf = re.sub("x..", "", strdf)
        strdf = strdf.replace("(","")
        strdf = strdf.replace(")","")
        logging.info(f"{strdf}:::: FORMATTED STRING FROM GOOGLE OCR ")
    except:
        strdf='lol' 
        logging.error(f"{strdf}:::: ERROR IN OCR")
    print(strdf)       
    
    if (strdf.find("INCOME TAX DEPARTMENT") > 1):
        results = pancard(strdf)
        logging.info("PAN CARD FUNCTION CALLED")
    elif (strdf.find("Government of India") > -1 and (strdf.find("Unique Identification Authority of India") > -1 or strdf.find("UNIQUE IDENTIFICATION AUTHORITY OF INDIA") > -1)):
        results = aadharfull(strdf)
        logging.info("AADHAR FULL FUNCTION CALLED")
    elif (strdf.find("Government of India") > 0 or strdf.find("GOVERNMENT OF INDIA") > 0):
        results = aadharcardf(strdf)
        logging.info("AADHAR FRONT FUNCTION CALLED")

    elif (strdf.find("Unique Identification Authority of India") > 1):
        results = aadharcardb(strdf)
        
        logging.info("AADHAR BACK FUNCTION CALLED")
    elif (strdf.find("UNIQUE IDENTIFICATION AUTHORITY OF INDIA") > 1):
        results = aadharcardb(strdf)
        logging.info("AADHAR BACK FUNCTION CALLED")
    elif(len(strdf)<4):
        results = {"status_message":"NO TEXT FOUND "}
        logging.warn("OCR RESPONSE STRING IS EMPTY, IF IT IS APPLICANT PHOTO, IGNORE")
        
    else:
        results={"status_message":"UNIDENTIFIED DOCUMENT"}    
        logging.error("DOCUMENT IS UNIDENTIFIED")
    try:    
        fileresize(current_time)
    except Exception as e:
        logging.info(f"{e}:::: THIS IS THE EXCEPTION FOR FILE RESIZE")
    
    current_time=current_time+".jpg"    
    file_name={"file_name":current_time}
    results.update(file_name)
    #logfile.write("\n"+str(results)+"::::::::::::::: FINAL RESPONSE")
    ###logfile.close()
    
 
    logging.info(f"{str(results)}:::::::::: FINAL RESULTS ")
    return results     
    

if __name__ == '__main__':
     
     app.run(host="0.0.0.0")
