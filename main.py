import tkinter
from tkinter import *
from functools import partial
from tkinter import messagebox
import mysql.connector
import cv2 # pip install opencv-python
import PIL.Image, PIL.ImageTk # pip install pillow
import threading
import time
import imutils # pip install imutils

def mainprog():
    stream = cv2.VideoCapture("clip.mp4")

    def play(speed):
        flag = True
        print(f"You clicked on play. Speed is {speed}")

        # Play the video in reverse mode
        frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
        stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

        grabbed, frame = stream.read()
        if not grabbed:
            exit()
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
        if flag:
            canvas.create_text(134, 26, fill="black", font="Times 26 bold", text="Decision Pending")
        flag = not flag

    def pending(decision):
        # 1. Display decision pending image
        frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
        # 2. Wait for 1 second
        time.sleep(1.5)

        # 3. Display sponsor image
        # frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
        # frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        # frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        # canvas.image = frame
        # canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

        # 4. Wait for 1.5 second
        time.sleep(2.5)
        # 5. Display out/notout image
        if decision == 'out':
            decisionImg = "out.png"
        else:
            decisionImg = "not_out.png"
        frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    def out():
        thread = threading.Thread(target=pending, args=("out",))
        thread.daemon = 1
        thread.start()
        print("Player is out")

    def not_out():
        thread = threading.Thread(target=pending, args=("not out",))
        thread.daemon = 1
        thread.start()
        print("Player is not out")

    # Width and height of our main screen
    SET_WIDTH = 650
    SET_HEIGHT = 368

    # Tkinter gui starts here
    window = tkinter.Tk()
    window.title("Third Umpire Decision Review Kit")
    cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)
    canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
    image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
    canvas.pack()

    # Buttons to control playback
    btn = tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -25))
    btn.pack()

    btn = tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2))
    btn.pack()

    btn = tkinter.Button(window, text="Next (slow) >>", width=50, command=partial(play, 2))
    btn.pack()

    btn = tkinter.Button(window, text="Next (fast) >>", width=50, command=partial(play, 25))
    btn.pack()

    btn = tkinter.Button(window, text="Give Out", width=50, command=out)
    btn.pack()

    btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
    btn.pack()
    window.mainloop()


def validateReg(username, password, name):
    # print("username entered :", username.get())
    # print("password entered :", password.get())
    un = str(username.get())
    ps = str(password.get())
    nm = str(name.get())
    if nm == "":
        messagebox.showinfo("Error", "Please enter name")
    elif un == "":
        messagebox.showinfo("Error", "Please enter email")
    elif ps == "":
        messagebox.showinfo("Error", "Please enter password")
    else:
        try:
            mycursor = mydb.cursor()

            sqll = f"SELECT * FROM users WHERE email = '{un}'"

            aa = mycursor.execute(sqll)

            myresult = mycursor.fetchall()

            if myresult:
                messagebox.showinfo("Error", "User Already Exist")
            else:
                sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                val = (nm, un, ps)
                mycursor.execute(sql, val)

                mydb.commit()
                messagebox.showinfo("Success", "Registration Successful")

        except Exception as e:
            messagebox.showinfo("Error", "Error in Registration")


def regg():
    global validateReg


    def close_win():
        tkk.destroy()

    def switch1():
        tkk.destroy()
        loginn()


    def loginn():
        global validateLog
        try:
            mydb = mysql.connector.connect(
                host="sql6.freesqldatabase.com",
                user="sql6518322",
                password="HNtCrWCpIm",
                database="sql6518322"
            )
        except:
            messagebox.showinfo("Error", "Please connect internet")

        # window
        tkwindow = Tk()
        tkwindow.geometry('600x350')
        tkwindow.title('DRS Login')

        def close_win():
            tkwindow.destroy()

        def switch2():
            tkwindow.destroy()
            regg()


        # username label and text entry box
        my_font1 = ('Times', 15, 'bold')
        my_font2 = ('Times', 15,)
        my_font3 = ('Times', 20, 'bold')
        titlee = Label(tkwindow, text="DRS Login", font=my_font3).place(x=250, y=40)
        usernameLabel = Label(tkwindow, text="Email :", font=my_font1).place(x=150, y=70 + 40)

        username = StringVar()
        usernameEntry = Entry(tkwindow, textvariable=username, font=my_font2).place(x=270, y=70 + 40)

        # password label and password entry box
        passwordLabel = Label(tkwindow, text="Password :", font=my_font1).place(x=150, y=108 + 40)
        password = StringVar()
        passwordEntry = Entry(tkwindow, textvariable=password, show='*', font=my_font2).place(x=270, y=108 + 40)

        # validateLog = partial(validateLog, username, password)

        def validateLog():
            # print("username entered :", username.get())
            # print("password entered :", password.get())
            un = str(username.get())
            ps = str(password.get())
            if un == "":
                messagebox.showinfo("Error", "Please enter email")
            elif ps == "":
                messagebox.showinfo("Error", "Please enter password")
            else:
                try:
                    mycursor = mydb.cursor()

                    sql = f"SELECT * FROM users WHERE email ='{un}' and password = '{ps}'"

                    aa = mycursor.execute(sql)

                    myresult = mycursor.fetchone()

                    if myresult:
                        messagebox.showinfo("Success", "Login Success")
                        tkwindow.destroy()
                        mainprog()
                    else:
                        messagebox.showinfo("Error", "Invalid ID and Pass")
                except Exception as e:
                    messagebox.showinfo("Error", "Error in Registration")

        # log button
        loginButton = Button(tkwindow, text="Login", command=validateLog, font=my_font1).place(x=230, y=160 + 40)
        closeButton = Button(tkwindow, text="Close", command=close_win, font=my_font1).place(x=360, y=160 + 40)
        regButton = Button(tkwindow, text="New User?", command=switch2, font=my_font1).place(x=470, y=300)

        tkwindow.mainloop()


    tkk = Tk()
    tkk.geometry('600x350')
    tkk.title('DRS Registration')
    # username label and text entry box
    my_font1 = ('Times', 15, 'bold')
    my_font2 = ('Times', 15,)
    my_font3 = ('Times', 20, 'bold')
    titlee = Label(tkk, text="DRS Registration", font=my_font3).place(x=200, y=40)

    nameLabel = Label(tkk, text="Name :", font=my_font1).place(x=140, y=70 + 40)
    name = StringVar()
    nameEntry = Entry(tkk, textvariable=name, font=my_font2).place(x=260, y=70 + 40)

    usernameLabel = Label(tkk, text="Email :", font=my_font1).place(x=140, y=70 + 80)
    username = StringVar()
    usernameEntry = Entry(tkk, textvariable=username, font=my_font2).place(x=260, y=70 + 80)

    # password label and password entry box
    passwordLabel = Label(tkk, text="Password :", font=my_font1).place(x=140, y=108 + 80)
    password = StringVar()
    passwordEntry = Entry(tkk, textvariable=password, show='*', font=my_font2).place(x=260, y=108 + 80)

    validateReg = partial(validateReg, username, password, name)

    # reg button
    RegButton = Button(tkk, text="Register", command=validateReg, font=my_font1).place(x=200, y=160 + 80)
    closeButton = Button(tkk, text="Close", command=close_win, font=my_font1).place(x=330, y=160 + 80)
    logButton = Button(tkk, text="Already a User?", command=switch1, font=my_font1).place(x=440, y=300)

    tkk.mainloop()



if __name__ == '__main__':
    try:
        mydb = mysql.connector.connect(
            host="sql6.freesqldatabase.com",
            user="sql6518322",
            password="HNtCrWCpIm",
            database="sql6518322"
        )
    except:
        messagebox.showinfo("Error", "Please connect internet")
    regg()
