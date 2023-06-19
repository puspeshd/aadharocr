import pandas as pd
import regex as re
import requests
from fileinput import filename
import os
from flask import Flask, request, render_template
import cv2
from flask_cors import CORS,cross_origin


app = Flask(__name__)
CORS(app)

@app.route('/newapp', methods=["GET", "POST"])
def photoupd():

    if (request.method == "POST"):
        image_path = request.files["upd"]
        image_path.save(image_path.filename)
        
        
        '''filesize=os.path.getsize(image_path.filename)/1024 
        if(filesize>1000 and filesize<2500):
            image_path1=cv2.imread(image_path.filename)
            height,width,_=image_path1.shape
            print(image_path1.shape)
            image_path1=cv2.resize(image_path1, (int(height*20/100),int(width*20/100)))
            print(image_path1.shape)
            cv2.imwrite(image_path.filename,image_path1)
        elif(filesize>2500):    
            image_path1=cv2.imread(image_path.filename)
            height,width,_=image_path1.shape
            print(image_path1.shape)
            image_path1=cv2.resize(image_path1, (int(height*10/100),int(width*10/100)))
            print(image_path1.shape)
            cv2.imwrite(image_path.filename,image_path1)'''
        return (image_path)
    return render_template("input.html")


@app.route('/newapp/results', methods=["GET", "POST"])
def mainfunc():
    image_path = photoupd()

    def pancard(strdf):

        listdf = strdf.split(",")
        try:
            finallist = []
            print(listdf)
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
                         [1], "DOB": finallist[0][2], "PAN_NO": finallist[0][3]}
            return (dictfinal)
        except:
            listdf.insert(
                0, "SOME INCORRECTNESS IN DATA FROM IMAGE....WILL BE SOON CORRECTED")
            return (listdf)

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
                            
            dictfinal = {"Name": finallist[0][0], "DOB": finallist[0][1],
                         "GENDER": finallist[0][2], "AADHAR NO": finallist[0][3]}
            return (dictfinal)
        except:
            listdf.insert(
                0, "SOME INCORRECTNESS IN DATA FROM IMAGE....WILL BE SOON CORRECTED")
            return (listdf)

    def aadharcardb(strdf):

        listdf = strdf.split(",")
        finallist = []
        try:
            for i in range(len(listdf)):

                if (listdf[i].find("Address") > 0 or listdf[i].find("Addre") > 0):
                    listdf[i] = listdf[i].replace("'Address: ", "")
                    listdf = listdf[i+1:]
                    break
            for i in range(len(listdf)):
                if ((listdf[i].find("D O") > 0 or listdf[i].find("S O") > 0 or listdf[i].find("C O") > 0) or listdf[i].find("C o") > 0 or listdf[i].find("c o") > 0):
                    listdf = listdf[i+1:]
                    break

            print(listdf)
            for j in range(len(listdf)):
                if (len(listdf[j]) < 3 or listdf[j].find("1947") > 0 or listdf[j].find("VID:") > 0 or listdf[j].find('uidai') > 0 or bool(re.search(" \d\d\d\d \d\d\d\d \d\d\d\d", listdf[j])) == True):
                    listdf[j] = "puspesh@puspesh"
            y = listdf.count("puspesh@puspesh")
            x = len(listdf)-1

            while (x > -1):
                if (listdf[x] == "puspesh@puspesh"):
                    listdf.pop(x)
                    y = y-1
                x = x-1
            x = len(listdf)-1
            print(listdf)
            for i in range(x):
                if (bool(re.search("\d\d\d\d\d", listdf[i])) == True):

                    listdf = listdf[0:i+1]
                    break

            for i in range(len(listdf)):
                if (str(listdf[i]).find("560 001") > 0):
                    listdf.pop(i)
                    break

            params = {'address': str(listdf),
                      'key': 'AIzaSyDISrKu3mOEE100DwCDUvNsTeCssciGh4o'}
            jsonfromgoogle = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json", params=params)
            dfgoogle = pd.read_json(jsonfromgoogle.text)
            strgoogle = dfgoogle['results']
            addgoogle = str(strgoogle[0]['formatted_address'])
            latgoogle = str(strgoogle[0]['geometry']['location']['lat'])
            lnggoogle = str(strgoogle[0]['geometry']['location']['lng'])

            # print(listdf)
            addgoogle = addgoogle.split(",")

            # print(addgoogle)
            houseno = listdf[0]
            houseno = houseno.replace(" ", "")
            if (houseno.isalpha() == False):
                houseno = listdf[0]
            else:
                listdf.pop(0)
                houseno = listdf[0]

            tempstate = addgoogle[len(addgoogle)-2]
            state = ''
            gpin = ''
            city = ''
            tempcity = addgoogle[len(addgoogle)-3]
            print(addgoogle)
            if (str(listdf).find(str(tempcity)) > -1):
                city = tempcity
            tempstate = re.sub(" ", "", tempstate)
            country = addgoogle[len(addgoogle)-1]
            for i in tempstate:
                if (i.isalpha()):
                    state = state+i
                elif (i.isdigit()):
                    gpin = gpin+i
            temppincode = listdf[len(listdf)-1]
            print(temppincode)
            pincode = ''
            for i in temppincode:
                if (i.isdigit()):
                    pincode = pincode+i
            if (pincode.isdigit()):
                pass
            else:
                pincode = gpin

            if (pincode.find(gpin) > -1):
                flag = 'VERIFIED FROM GOOGLE MAPS API'
            else:
                flag = ' NOT VERIFIED FROM GOOGLE MAPS API'
            city = listdf[len(listdf)-2]

            listdf = listdf[0:len(listdf)-2]

            xxx = len(listdf)
            if (xxx == 1):
                locality = ''
                street = ''
                buildingname = ''

            elif (xxx == 2):
                locality = listdf[1]
                street = ''
                buildingname = ''
            elif (xxx == 3):
                locality = listdf[2]
                street = listdf[1]
                buildingname = ''
            elif (xxx == 4):
                locality = listdf[3]
                street = listdf[2]
                buildingname = listdf[1]
            elif (xxx == 5):
                locality = listdf[3]+listdf[4]
                street = listdf[2]
                buildingname = listdf[1]
            elif (xxx == 6):
                locality = listdf[4]+listdf[5]
                street = listdf[2]+listdf[3]
                buildingname = listdf[1]
            elif (xxx == 7):
                locality = listdf[4]+listdf[5]+listdf[6]
                street = listdf[2]+listdf[3]
                buildingname = listdf[1]
            elif (xxx == 8):
                locality = listdf[5]+listdf[6]+listdf[7]
                street = listdf[2]+listdf[3]+listdf[4]
                buildingname = listdf[1]
            elif (xxx == 9):
                locality = listdf[6]+listdf[7]+listdf[8]
                street = listdf[2]+listdf[3]+listdf[4]+listdf[5]
                buildingname = listdf[1]

            print(listdf, len(listdf))
            addfinal = {"Flag": flag, "House no": houseno, "Building name": buildingname, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pincode, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle}
            return (addfinal)
        except:
            listdf.insert(
                0, "SOME INCORRECTNESS IN DATA FROM IMAGE....WILL BE SOON CORRECTED")
            return (listdf)

    def aadharfull(strdf):

        len(strdf)
        astrdf=strdf
        strdf = strdf[200:]
        # print(strdf)
        listdf = strdf.split(",")
        #print(listdf)
        finallist = []
        try:
            for i in range(len(listdf)):
                if (listdf[i].find(" Government of India") > -1 or listdf[i].find(" GOVERNMENT OF INDIA") > -1):
                    if (len(listdf[i+4]) == 15):
                        listtemp = [listdf[i+1], listdf[i+2],
                                    listdf[i+3], listdf[i+4]]

                    else:
                        listdf[i+3] = listdf[i+3].replace(" ", "")
                        if (listdf[i+3].isalpha() == True):
                            tempstr = listdf[i+2]+" "+listdf[i+3]
                            listtemp = [tempstr, listdf[i+4],
                                        listdf[i+5], listdf[i+6]]
                        else:
                            listtemp = [listdf[i+2], listdf[i+3],
                                        listdf[i+4]]
                            abc=re.search(r"\d\d\d\d \d\d\d\d \d\d\d\d",astrdf)
                            abc=abc.span()
                            ano=astrdf[abc[0]:abc[1]+1]
                            listtemp.append(ano)
                    finallist.append(listtemp)
                    break
            for i in finallist[0][1]:
                if(i.isalpha() == True):
                    finallist[0][1]=finallist[0][1].replace(i,"")
                elif(i == ":"):
                     finallist[0][1]=finallist[0][1].replace(i,"")
            dictfinal1 = {"Name": finallist[0][0], "DOB": finallist[0][1],
                          "GENDER": finallist[0][2], "AADHAR_NO": finallist[0][3]}
            for i in range(len(listdf)):

                if (listdf[i]=="To" ):
                    #listdf[i] = listdf[i].replace("'Address: ", "")
                    listdf = listdf[i+1:]
                    #print(listdf)
                    break
                    
            for i in range(len(listdf)):
                if ((listdf[i].find("D O") > -1 or listdf[i].find("S O") > -1 or listdf[i].find("C O") > -1) or listdf[i].find("C o") > 0-1 or listdf[i].find("c o") > -1 ):
                    listdf = listdf[i+1:]
                    break

            for j in range(1, len(listdf)):
                if (len(listdf[j]) < 5 or listdf[j].find("1947") > 0 or listdf[j].find("VID:") > 0 or listdf[j].find('uidai') > 0 or bool(re.search(" \d\d\d\d \d\d\d\d \d\d\d\d", listdf[j])) == True):
                    listdf[j] = "puspesh@puspesh"
            y = listdf.count("puspesh@puspesh")
            x = len(listdf)-1

            while (x > -1):
                if (listdf[x] == "puspesh@puspesh"):
                    listdf.pop(x)
                    y = y-1
                x = x-1
            x = len(listdf)-1
            #print(listdf)
            for i in range(x):
                if (bool(re.search("\d\d\d\d\d", listdf[i])) == True):

                    listdf = listdf[0:i+1]
                    
                    break
                
            for i in range(len(listdf)):
                if (str(listdf[i]).find("560 001") > 0):
                    listdf.pop(i)
                    break
                

            params = {'address': str(listdf),
                      'key': 'AIzaSyDISrKu3mOEE100DwCDUvNsTeCssciGh4o'}
            jsonfromgoogle = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json", params=params)
            dfgoogle = pd.read_json(jsonfromgoogle.text)
            strgoogle = dfgoogle['results']
            addgoogle = str(strgoogle[0]['formatted_address'])
            latgoogle = str(strgoogle[0]['geometry']['location']['lat'])
            lnggoogle = str(strgoogle[0]['geometry']['location']['lng'])

            # print(listdf)
            addgoogle = addgoogle.split(",")
            temp=listdf[0].replace(" ","")
            # print(addgoogle)
            if(temp.isalpha()):
             listdf=listdf[1:]
            houseno = listdf[0]
       
            tempstate = addgoogle[len(addgoogle)-2]
            state = ''
            gpin = ''
            city = ''
            tempcity = addgoogle[len(addgoogle)-3]
            #print(addgoogle)
            if (str(listdf).find(str(tempcity)) > -1):
                city = tempcity
            tempstate = re.sub(" ", "", tempstate)
            country = addgoogle[len(addgoogle)-1]
            for i in tempstate:
                if (i.isalpha()):
                    state = state+i
                elif (i.isdigit()):
                    gpin = gpin+i
            for i in range(len(listdf)):
                if (listdf[i].find(city) > 0):
                    city = listdf[i+1]

                    #listdf = listdf[0:i+1]
 
                    break
            print(listdf," THIS IS AADHAR ADDRESS")    
            print(addgoogle," THIS IS GOOGLE ADDRESS")    
            xxx = len(listdf)
            if (xxx >= 1):
                locality = ''
                street = ''
                buildingname = ''

            elif (xxx == 2):
                locality = listdf[1]
                street = ''
                buildingname = ''
            elif (xxx == 3):
                locality = listdf[2]
                street = listdf[1]
                buildingname = ''
            elif (xxx == 4):
                locality = listdf[3]
                street = listdf[2]
                buildingname = listdf[1]
            elif (xxx == 5):
                locality = listdf[3]+listdf[4]
                street = listdf[2]
                buildingname = listdf[1]
            elif (xxx == 6):
                locality = listdf[4]+listdf[5]
                street = listdf[2]+listdf[3]
                buildingname = listdf[1]
            elif (xxx == 7):
                locality = listdf[4]+listdf[5]+listdf[6]
                street = listdf[2]+listdf[3]
                buildingname = listdf[1]
            elif (xxx == 8):
                locality = listdf[5]+listdf[6]+listdf[7]
                street = listdf[2]+listdf[3]+listdf[4]
                buildingname = listdf[1]
            elif (xxx == 9):
                locality = listdf[6]+listdf[7]+listdf[8]
                street = listdf[2]+listdf[3]+listdf[4]+listdf[5]
                buildingname = listdf[1]
            temppincode = listdf[len(listdf)-1]
            #print(temppincode)
            pincode = ''
            for i in temppincode:
                if (i.isdigit()):
                    pincode = pincode+i
            if (pincode.isdigit()):
                pass
            else:
                pincode = gpin

            if (pincode.find(gpin) > -1):
                flag = 'VERIFIED FROM GOOGLE MAPS API'
            else:
                flag = ' NOT VERIFIED FROM GOOGLE MAPS API'
            print(listdf)
            addfinal = {"Flag": flag, "House no": houseno, "Building name": buildingname, "locality": locality, "street": street,
                        "city": city, "state": state, "country": country, "PIN": pincode, "LATITUDE": latgoogle, "LONGITUDE": lnggoogle}

            dictfinal1.update(addfinal)
            return (dictfinal1)
        except:
            listdf.insert(
                0, "SOME INCORRECTNESS IN DATA FROM IMAGE....WILL BE SOON CORRECTED")
            return (listdf)

    url = 'https://verify.bluealgo.com/pan'

    headers = {}

    xx = open(image_path.filename, 'rb')
    files = [('file', (image_path.filename, xx, 'image/jpg'))]

    response = requests.request('POST', url=url, files=files, headers=headers)

    if response.status_code == 200:
        print(response)
        xx.close()
        os.remove(image_path.filename)  # tobedeleted
    else:
        print('Error:', response.status_code)
        exit()

    
    df = pd.read_json(response.text)
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
    print(len(strdf))
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
    else:
        results = "INCORRECT DATA FOUND"
    return (results)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
