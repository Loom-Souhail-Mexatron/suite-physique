from tkinter import *
import customtkinter as ctk
import rc
import guiWorks
import nbodyTk
import mech
import guideManager as gum
from PIL import Image
#import pyi_splash


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("400x350+150+150")
app.resizable(False,False)
app.title("Suite de Physique")


atomApp = None
def ATOM_PROG():
    global atomApp
    if atomApp is None:
        atomApp = guiWorks.MAIN_ATOM(app)
    else:
        atomApp.destroy()
        atomApp = guiWorks.MAIN_ATOM(app)

gravApp = None
def GRAV_PROG():
    global gravApp
    if gravApp is None:
        gravApp = nbodyTk.MAIN_GRAV(app)
    else:
        gravApp.destroy()
        gravApp = nbodyTk.MAIN_GRAV(app)


def RC_PROG():
    rc.MAIN_RC(app)

mechApp = None
def MECH_PROG():
    global mechApp
    if mechApp is None:
        mechApp = mech.MAIN_MECH(app)
    else:
        mechApp.destroy()
        mechApp = mech.MAIN_MECH(app)

ctk.CTkLabel(app,text="Pour la 2ème année:",font=("Arial", 25)).place(relx=0.05,rely=0.05,anchor=NW)
ATOM = ctk.CTkButton(app, text="L'atome",command=ATOM_PROG,font=("Arial", 25),width=250,height=30)
ATOM.place(relx=0.5,rely=0.225,anchor=S)

ctk.CTkLabel(app,text="Pour la 3ème année:",font=("Arial", 25)).place(relx=0.05,rely=0.25,anchor=NW)
GRAV = ctk.CTkButton(app, text="Gravitation", command=GRAV_PROG,font=("Arial", 25),width=250,height=30)
GRAV.place(relx=0.5,rely=0.425,anchor=S)

ctk.CTkLabel(app,text="Pour la 4ème année:",font=("Arial", 25)).place(relx=0.05,rely=0.45,anchor=NW)
COND = ctk.CTkButton(app, text="Circuit RC",command=RC_PROG,font=("Arial", 25),width=250,height=30)
COND.place(relx=0.5,rely=0.625,anchor=S)
COND = ctk.CTkButton(app, text="Mécanique",command=MECH_PROG,font=("Arial", 25),width=250,height=30)
COND.place(relx=0.5,rely=0.75,anchor=S)

guide = None
#GUM LOGIC
def gumCall():
    global guide
    if guide is None:
        guide = gum.createGuideWindow(app, "Guide", "main.txt")
    else:
        guide.destroy()
        guide = gum.createGuideWindow(app, "Guide", "main.txt")

gumButton = ctk.CTkButton(app,text="Guide",width=50,height=20,command=gumCall,image=ctk.CTkImage(dark_image=Image.open("./res/guide.png"),size=(30, 30)))
gumButton.place(relx=0.5,rely=0.95,anchor=S)

app.mainloop()
