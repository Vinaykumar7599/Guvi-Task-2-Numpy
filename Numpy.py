pip install dnspython
pip install pymongo[srv]
pip install Pillow
pip install qrcode
pip install tabulate

import tabulate
from tabulate import tabulate
import pymongo
from pymongo import MongoClient
from PIL import Image
import io
import matplotlib.pyplot as plt
import pandas as pd
import qrcode

client = pymongo.MongoClient("mongodb+srv://Dtyagi:DTyagi234@cluster0.ta0ig.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.movie
records=db.login
film=db.movie_list
book=db.booking

def register():
      mail =input("Enter E-mail-id: ")
      for x in records.find():
        if x["E-mail"]==mail:
          print("Already exist")
          register()
        else:
          name=input("Enter Your name: ")
          contact=input("Enter Your Contact number: ")
          password=input("Create your password: ")
          pic=input("Enter Photo URL: ")
          im = Image.open(pic)
          image_bytes = io.BytesIO()
          im.save(image_bytes, format='JPEG')
          a= {
            "Name":name,
            "Contact":contact,
            "E-mail":mail,
            "Password":password,
            "Total_Seats": 0,
            "Photo":image_bytes.getvalue()

          }
          records.insert_one(a)
          print("Registration Successful")
          welcome()

def login():
  mail=input("Enter your registered mail-id: ")
  pas=input("Please Enter your password: ")
  for x in records.find():
    if x["E-mail"]!=mail and x["Password"]!=pas:
      print("WRONG CREDENTIALS! TRY AGAIN")
      welcome()
    elif x["E-mail"]==mail and x["Password"]==pas:
      print("===================================")
      print("Welcome"+" "+ x["Name"])
      image = records.find_one({"E-mail":mail})
      pil_img = Image.open(io.BytesIO(image['Photo']))
      plt.imshow(pil_img)
      plt.show()
      TS= int(x["Total_Seats"])
      print("Total Seats booked: ", + TS)
      print("===================================")
      if TS>=5:
        print("Sorry your limit exhaust")
      else:
        print("MOVIE LIST")
        print("----------------")
        li=[]
        for x in film.find({},{"_id":0, "Movie":1, "CBFC":1}):
          if x not in li:
            li.append(x)
        d=pd.DataFrame(li, index=[1,2,3,4])
        print(d)
        ind=int(input("Enter index number to choose movie: "))
        if ind==1:
          M="Pushpa"
        if ind==2:
          M="KGF"
        if ind==3:
          M="The UNBREAKABLE"
        if ind==4:
          M="The FURY"
        print("Your Selected Movie is: ",M)
        print("--------------------------------------")
        print("Theater list is ")
        print("--------------------------------------")
        li1=[]
        for i in film.find({"Movie": M},{"_id":0, "Screen":1, "Rating":1, "Shift":1, "Seats":1}):
          if i not in li1:
            li1.append(i)
        df=pd.DataFrame(li1)
        print(df)              
        ST=5 - TS
        STT=abs(ST)
        print("You only allowed to book number of seats are: ",+ STT)
        if STT==0:
          print("SORRY YOU EXHAUST ALL YOUR LIMIT! REGISTER WITH ANOTHER ID FOR BOOKING")
          welcome()
        else:
          seats=int(input("Enter number of seats you want to book: "))
          if seats>STT:
            print("Sorry You are not eligible")
            login()
          else:
            scr=input("Enter name of Theater[P/O/S]: ")
            if scr=="P":
              screen="PVR"
            if scr=="O":
              screen="OPPULENT"
            if scr=="S":
              screen="SILVERCITY"
            sh=input("Enter shift in which you want ticket[M/E]: ")
            if sh=="M":
              shift="Morning"
            if sh=="E":
              shift="Evening"            
            X={"Movie": M, "Screen": screen, "Shift": shift}
            for c in film.find(X):
              if c["Seats"]==0:
                print("Sorry Selected Screen now full! TRY AGAIN WITH NEW SCREEN")
                login()
              else:
                update={"$inc":{"Seats": -seats}}
                film.update_one(X,update)           
            Y={"E-mail": mail}
            updat={"$inc":{"Total_Seats": seats}}
            records.update_one(Y,updat)
            my={"$currentDate":{"Time": True}}
            film.update_one(X,my)
            print("Your seat is confirmed")
            print("===========================================")
            print("===========================================")
            for y in records.find(Y):
              A=("Name : "+y['Name'])
            for z in film.find(X):
              B=("Theater: "+z['Screen'])
              C=("Shift:"+z['Shift'])
              D=("Number of Seats: "+str(seats))
              E=("Time: "+str(z['Time']))
              F=("Movie: "+ M)
            table=[[A],[B],[C],[D],[E],[F]]
            T=tabulate(table, headers=["WELCOME TO MOVIE WORLD"], tablefmt= "grid")
            import qrcode
            img = qrcode.make(T)
            type(img)  # qrcode.image.pil.PilImage
            img.save("some_file.png")
            pic="/content/some_file.png"
            im = Image.open(pic)
            image_bytes = io.BytesIO()
            im.save(image_bytes, format='PNG')
            data={
                "E-mail": mail,
                "Movie": M,
                "Time": E,
                "QR-code":image_bytes.getvalue()
            }
            book.insert_one(data)
            print(T)
            image = book.find_one({"E-mail":mail, "Time": E, "Movie": M})
            pil_img = Image.open(io.BytesIO(image['QR-code']))
            plt.imshow(pil_img)
            plt.show()
            break
    else:
      print("Enter credentials carefully")
                           
def welcome():
  print("WELCOME IN THE BOX OFFICE WORLD")
  A=input("For ticket booking you need to Login/Register[L/R]: ")
  if A=="L":
    login()
  if A=="R":
    register()
welcome()
