import numpy as np       
import cv2
import dlib    # contain the implementation of facial landmark detection which is used to detect the eye on the frontal face.
from scipy.spatial import distance as dist
import winsound
import time
from win10toast import ToastNotifier
import pymongo
import tkinter
import requests
from validate_email import validate_email
import pymongo
from tkinter import simpledialog,messagebox
import hashlib
import numpy as np       
import cv2
import dlib    # contain the implementation of facial landmark detection which is used to detect the eye on the frontal face.
from scipy.spatial import distance as dist
import winsound
import time
from win10toast import ToastNotifier
import pymongo


#myclient=pymongo.MongoClient("mongodb://localhost:27017/")
#mydb=myclient["EyeDB"]


user_names_values=""
login_pass_values=""
blinks=0
#import requests
#from practice import *
# Initial Time
year=time.localtime()[0]
month=time.localtime()[1]
dates=time.localtime()[2]
hours=time.localtime()[3]            # getting value by using indexing
minutes=time.localtime()[4]
seconds=time.localtime()[5]
initial_time=(hours,minutes,seconds) 

user_names_values=""
login_pass_values=""
x=0

#first time when we open app or when ever open app

def update(email,data):
    myclient=pymongo.MongoClient("mongodb://localhost:27017/")
    mydb=myclient["EyeDB"]
    mycol=mydb["newData"]
    myquery={'email':email}
    new_values={"$set":data}
    mycol.update_one(myquery, new_values)


def send_data_to_database(data):
    myclient=pymongo.MongoClient("mongodb://localhost:27017/")
    mydb=myclient["EyeDB"]
    mycol=mydb["newData"]
    mycol.insert_one(data)
    

def delete_data_from_database(email):
    myclient=pymongo.MongoClient("mongodb://localhost:27017/")
    mydb=myclient["EyeDB"]
    mycol=mydb["newData"]
    #myquery = { "email":email }
    database=mycol.find()
    for values in database:
        if values['email']==email:
            times=values['time']
            #mycol.delete_one(myquery)
            return times
        
        
        




def calculate_gap(interval,f_hours,f_minutes,f_seconds, initial_time=initial_time):
    
    # getting value by using indexing

    gap=f_seconds-seconds
    print(gap)
    # print(seconds,f_seconds)
    #print(gap)
    hgap=(60-seconds)
    h_gap=hgap+f_seconds
    #print(h_gap)
    
    return (gap,h_gap)



def alarm(duration=3000, freq=440):
    duration = 5000  # millisecond
    freq = 440  # Hz
    winsound.Beep(freq, duration)




def eye_aspect_ratio(eye):
    # compute the euclidean distance between the vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal eye landmarks
    C = dist.euclidean(eye[0], eye[3])

    # compute the EAR
    ear = (A + B) / (2 * C)
    return ear


def detect():
    
    global year
    global month
    global dates
    global hours
    global minutes
    global seconds
    global blinks
    global user_names_values
    global login_pass_values

      
    toaster = ToastNotifier()
    
    RIGHT_EYE_POINTS = list(range(36, 42))
    LEFT_EYE_POINTS = list(range(42, 48))
    
    
    EYE_AR_THRESH = 0.20                # eye aspect Threshold
    EYE_AR_CONSEC_FRAMES = 1            # three successive frames with an eye aspect ratio less than EYE_AR_THRESH  must happen in order for a blink to be registered.
    EAR_AVG = 0
    
    COUNTER = 0
    TOTAL = 0
    
    h_initial=str(hours)+":"+str(minutes)+":"+str(seconds)

    
    
    
    
    # to detect the facial region
    detector = dlib.get_frontal_face_detector()  # initialise dlib's pre-trained detector based on modification  to the standard HOG (Histogram of oriented Gradients) + Linear SVM method
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat') # load the facial landmark predictor using 68_face land_mark
    
    # capture video from live video stream
    cap = cv2.VideoCapture(0)
    while True:
        # get the frame
        ret, frame = cap.read()
        #frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        if ret:
            # convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 0)   # first one is gray scale captured frame and 2nd is 
            
            for rect in rects:
                x = rect.left()
                y = rect.top()
                x1 = rect.right()
                y1 = rect.bottom()
                # get the facial landmarks
                landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()])
                
                # get the left eye landmarks
                left_eye = landmarks[LEFT_EYE_POINTS]
                
                # get the right eye landmarks
                right_eye = landmarks[RIGHT_EYE_POINTS]
                # draw contours on the eyes
                
                left_eye_hull = cv2.convexHull(left_eye)
                right_eye_hull = cv2.convexHull(right_eye)
                
                cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1) # (image, [contour], all_contours, color, thickness)
                cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)
                
                # compute the EAR for the left eye
                ear_left = eye_aspect_ratio(left_eye)
                
                # compute the EAR for the right eye
                ear_right = eye_aspect_ratio(right_eye)
                
                # compute the average EAR
                ear_avg = (ear_left + ear_right) / 2.0
    
                f_year=time.localtime()[0]
                #print(type(f_year))
                f_month=time.localtime()[1]       #month
                f_date=time.localtime()[2]        #date
                f_hours=time.localtime()[3]     # hour      
                f_minutes=time.localtime()[4]   # min
                f_seconds=time.localtime()[5]   # sec
                final_time=(f_hours,f_minutes,f_seconds)
    
                
    
                
                
                # detect the eye blink
                if ear_avg < EYE_AR_THRESH:
                    COUNTER += 1
                else:
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        TOTAL += 1
                        blinks=TOTAL
    
                        print("Eye blinked")
                    COUNTER = 0
                    
                        
                if TOTAL==5:
                    toaster.show_toast("MOHIT", "WORKING PERFECTLY", duration=10,threaded=True)
                    #alarm()
                    
                cv2.putText(frame, "Blinks{}".format(TOTAL), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 1)
                cv2.putText(frame, "EAR {}".format(ear_avg), (10, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 1)
                
                h_final=str(f_hours)+":"+str(f_minutes)+":"+str(f_seconds)
            cv2.imshow("Winks Found", frame)
            key = cv2.waitKey(1) & 0xFF
            if key is ord('q'):
                
                data={'email':user_names_values ,'time':[[h_initial,h_final,blinks]]}
                values=delete_data_from_database(data['email'])
                for i in values:    
                    data['time'].append(i)
                
                #send_data_to_database(data)
                update(user_names_values,data)
               # r=requests.post('https://httpbin.org/post',data=payload)
                break
    
    # release all resources
    cap.release()
    # destroy all windows
    cv2.destroyAllWindows()
    


    

    
##########################################################################################################################################################################################################################################################################
    
                    #GUI PARTS'''
###################################################################################################################################













#import main2


###### checking repetation  ##############
def check_login_email_pass(email,log_pass):
    strings=log_pass
    myclient=pymongo.MongoClient("mongodb://localhost:27017/")
    mydb=myclient["EyeDB"]
    mycol=mydb["registers"]
    result=hashlib.md5(strings.encode())
    #print(type(result.hexdigest()))
    log_pass_final=result.hexdigest()
    x=mycol.find()    
    for a in x:
        if a['email']==email and a['password']==log_pass_final:
            return '1'
        else:
            continue



########### email validity checking function ###########################
def check_email_validity(email):
    is_valid = validate_email(email)
    return is_valid




################################ LOG_IN funtion #######################################
def LOG_IN():
    window.destroy()
    already_account()



################################# SIGN_UP function ######################################    
def SIGN_UP():
    root.destroy()
    new_account()




################### MAIN login function ###############################################
    
def loginto_account():
    global user_names_values
    global login_pass_values
    user_name_value=user_name.get()
    login_password_value=login_password.get()


    checked = check_login_email_pass(user_name_value,login_password_value)
    if checked=='1':
        
        user_names_values=user_name_value
        print(user_names_values)
        print("login successfully")
        detect()
    else:
        messagebox.askokcancel("Invalid input","Something went wrong")
    


############################ MAIN Sign up function ####################################
    
def create_account():
    
    first_name_value=first_name.get()
    last_name_value=last_name.get()
    emai_id_value=emai_id.get()
    password_value=password.get()
    confirm_password_value=confirm_password.get()
    validity=check_email_validity(emai_id_value)
    data={'email':emai_id_value,'time':[['0','0',0]]}
    send_data_to_database(data)
    
    
    #requests.post()
    data={'fname':first_name_value,'lname':last_name_value,'email':emai_id_value,'password':password_value}
    requests.post('http://localhost:3000/register',data=data)
    window.destroy()
    already_account()
        

    
        
    
    







####################################### tkinter Signup function #################################
def new_account():
    
# Create a window
    global window
    global labelframe
    global invalid
    window = tkinter.Tk()
    window.title("Sign up page")
    
    h=window.winfo_screenheight()-300
    w=window.winfo_screenwidth()-800  
    
    # Login page widgets
    fonts=('Times',20,'bold')
    label_font=('Times',15,'bold')
    #tkinter.Label(window,text="HELLO AND WELCOME",font=('Times',50,'bold'),fg='red').place(x=150,y=0)
    
    #VARIABLES---
    global first_name
    global last_name
    global emai_id
    global password
    global confirm_password
    
    first_name=tkinter.StringVar()
    last_name=tkinter.StringVar()
    emai_id=tkinter.StringVar()
    password=tkinter.StringVar()
    confirm_password=tkinter.StringVar()
    
    #### labelframe1
    labelframes = tkinter.LabelFrame(window, text="",font=fonts,fg='red',width=400,height=500,bd=5,bg='black')
    labelframes.place(x=15,y=10)
    
    tkinter.Label(labelframes,text="Already have an account",font=('Times',10,'bold'),width=43,bd=7).grid(row=0,column=0,padx=5)
    tkinter.Button(labelframes,text="Login",font=('Times',10,'bold'),bg='green',fg='white',bd=7,command=LOG_IN).grid(row=0,column=1)
    
    #### labelframe2 
    labelframe = tkinter.LabelFrame(window, text="",font=fonts,fg='black',width=400,height=500,bd=10)
    labelframe.place(x=15,y=65)
    
    reg = tkinter.LabelFrame(labelframe, text="",font=fonts,fg='black',bd=10)
    reg.grid(row=0,column=0,columnspan=2)
    
    tkinter.Label(reg,text="REGISTER",font=('Times',15)).grid(row=1,column=2,columnspan=4)
    
    
    tkinter.Label(labelframe,text=" Its for your eye protection ",font=('Times',10),width=40).grid(row=2,column=0,columnspan=2)
    
    tkinter.Label(labelframe, text="First name * :",font=label_font,fg='blue').grid(row=5,column=0,sticky="W",pady=15)
    tkinter.Entry(labelframe,width=30,bd=2,textvariable=first_name).grid(row=5,column=1,sticky="W")
    
    tkinter.Label(labelframe,text="Last name  *:",fg='blue',font=label_font).grid(row=6,column=0,sticky="W",pady=15)
    tkinter.Entry(labelframe,width=30,bd=2,textvariable=last_name).grid(row=6,column=1,sticky="W")
    
    tkinter.Label(labelframe,text="Email Id  *:",fg='blue',font=label_font).grid(row=7,column=0,sticky="W",pady=15)
    tkinter.Entry(labelframe,width=30,bd=2,textvariable=emai_id).grid(row=7,column=1,sticky="W")
    
    
    tkinter.Label(labelframe,text="Password *:",fg='blue',font=label_font).grid(row=8,column=0,sticky="W",pady=15)
    tkinter.Entry(labelframe,width=30,bd=2,show="*",textvariable=password).grid(row=8,column=1,sticky="W")
    
    tkinter.Label(labelframe,text="Minimum length of password is 8 character",fg='red',font=('Times',7,'bold')).grid(row=9,column=1,sticky="W",pady=0)
    
    tkinter.Label(labelframe,text="Confirm Password  *:",fg='blue',font=label_font).grid(row=10,column=0,sticky="W",pady=15)
    tkinter.Entry(labelframe,width=30,bd=2,show="*",textvariable=confirm_password).grid(row=10,column=1,sticky="W")
    
    tkinter.Button(labelframe,text=" Create Account ",font=('Times',10,'bold'),width=15,bg='green',fg='white',border=5,height=1,command=create_account).grid(row=11,column=0,pady=15,sticky="W")
    
    tkinter.Label(labelframe,text="Already have an account",fg='blue',font=('Times',10,'bold')).grid(row=12,column=0)
    tkinter.Button(labelframe,text="Log In ",font=('Times',8,'bold'),width=15,bg='green',fg='white',border=5,height=1,command=LOG_IN).grid(row=12,column=1,pady=15,sticky="W")
    
    window.wm_attributes('-alpha', 0.9)
    #Run the window loop
    window.geometry("420x600")
    window.resizable(0,0)
    window.configure(background='black')
    window.mainloop()








################################ tkinter log_in function ##############################################3

def already_account():
# Create a window
    global root
    global user_name
    global login_password
    
    root = tkinter.Tk()
    root.title("Sign up page")
    
    
    user_name=tkinter.StringVar()
    login_password=tkinter.StringVar()    
    
    # Login page widgets
    fonts=('Times',20,'bold')
    label_font=('Times',15,'bold')
        
    
    labelframes = tkinter.LabelFrame(root, text="",font=fonts,fg='red',width=400,height=500,bd=5,bg='black')
    labelframes.place(x=10,y=10)
    
    tkinter.Label(labelframes,text="Create new account ",font=('Times',10,'bold'),width=32,bd=7).grid(row=0,column=0)
    tkinter.Button(labelframes,text="Create Account",font=('Times',10,'bold'),bg='green',fg='white',bd=5,command=SIGN_UP).grid(row=0,column=1,padx=5,sticky="E")
    
    labelframe = tkinter.LabelFrame(root, text="-------------LOGIN-------------",font=fonts,fg='red',width=400,height=500,bd=10)
    labelframe.place(x=10,y=55)
    
    tkinter.Label(labelframe,text="Log In to your Account. Its for your eye protection",font=('Times',10)).grid(row=0,column=0,columnspan=2)
    
    left = tkinter.Label(labelframe, text="User name :",font=label_font,fg='blue').grid(row=1,column=0,pady=15,sticky="W")
    tkinter.Entry(labelframe,width=30,bd=2,textvariable=user_name).grid(row=1,column=1,sticky="W")
        
    tkinter.Label(labelframe,text="Password :",fg='blue',font=label_font).grid(row=4,column=0,sticky="W",pady=10)
    tkinter.Entry(labelframe,width=30,bd=2,show="*",textvariable=login_password).grid(row=4,column=1,sticky="W")
    
    
    tkinter.Button(labelframe,text=" Log In ",font=('Times',10,'bold'),width=15,bg='green',fg='white',border=5,height=1,command=loginto_account).grid(row=6,column=0,pady=15,sticky="W")
    
    tkinter.Label(labelframe,text="New Here !!  ",fg='blue',font=('Times',10,'bold')).grid(row=8,column=0)
    tkinter.Button(labelframe,text="Create Account ",font=('Times',10,'bold'),bg='green',fg='white',border=5,command=SIGN_UP).grid(row=8,column=1,pady=15,sticky="W")
    
    root.wm_attributes('-alpha', 0.9)
    #Run the window loop
    root.geometry("374x365+100+100")
    root.resizable(0,0)
    root.configure(background='black')
    root.mainloop()
    


new_account()









    
