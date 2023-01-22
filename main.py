from tkinter import *
import customtkinter as ctk
import rc
import guiWorks
import nbodyTk
import guideManager as gum
#import pyi_splash


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("400x300+150+150")
app.resizable(False,False)
app.title("Suite de Physique")

gum.createGuideWindow(app, "Guide", "main.txt")

def ATOM_PROG():
    guiWorks.MAIN_ATOM(app)

def GRAV_PROG():
    nbodyTk.MAIN_GRAV(app)

def RC_PROG():
    rc.MAIN_RC(app)

#pyi_splash.close()

ATOM = ctk.CTkButton(app, text="L'atome",command=ATOM_PROG,font=("Arial", 25),width=250,height=30)
ATOM.place(relx=0.5,rely=0.25,anchor=S)
GRAV = ctk.CTkButton(app, text="Gravitation", command=GRAV_PROG,font=("Arial", 25),width=250,height=30)
GRAV.place(relx=0.5,rely=0.5,anchor=S)
COND = ctk.CTkButton(app, text="Circuit RC",command=RC_PROG,font=("Arial", 25),width=250,height=30)
COND.place(relx=0.5,rely=0.75,anchor=S)

app.mainloop()
