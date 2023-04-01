from tkinter import *
import customtkinter as ctk
from chems import elems, names, getShellsVal, retrieveNature, valency, neutrons, atomColors
import numpy as np
import random
from PIL import Image,ImageTk
import guideManager as gum

t = -np.pi/2
isTurning = False
elecs = []
NZ = [4,8,28,60]
currN=0
currZ=1
currVal = 1
guide = None


def MAIN_ATOM(mainy):
    global t, isTurning, elecs, currVal, currN, currZ, guide

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    app = ctk.CTkToplevel(mainy)
    app.geometry("800x600+100+50")
    app.title("L'atome")


    canvas = Canvas(app,width=800,height=600,bg="#1A1A1A",relief="ridge")
    canvas.pack()

    xOffset = -0.395#-0.39375
    yOffset = 0.325
    fontSizeOffset = 18

    #app.wm_attributes('-transparentcolor', '#FFFFFF')
    #Colour was #006EDD

    elemSymbol = Label(app, text = 'H', font=("Arial", fontSizeOffset, 'bold'), fg = "#FFFFFF", bg="#006EDD")
    elemSymbol.place(relx=0.4875 + xOffset, rely=0.5 + yOffset,anchor=W)

    Anum = Label(app, text = '1', font=("Arial", fontSizeOffset, 'bold'), fg = "#FFFFFF", bg="#006EDD")
    Anum.place(relx=0.4875 + xOffset, rely=0.475 + yOffset,anchor=E)

    Znum = Label(app, text = '1', font=("Arial", fontSizeOffset, 'bold'), fg = "#FFFFFF", bg="#006EDD")
    Znum.place(relx=0.4875 + xOffset, rely=0.5325 + yOffset,anchor=E)

    elemName = ctk.CTkLabel(app, text = 'Hydrogène', font=("Arial", 25))
    elemName.place(relx=0.025, rely=0.95,anchor=W)



    #case = canvas.create_image(0, 0, anchor=SW, image=caseImg)

    #elemSy = ctk.CTkLabel(app, text = '1\n        H\n1', font=("Arial", 25))
    #elemSy.place(relx=0, rely=0.9,anchor=SW)

    #app.wm_attributes("-transparentcolor", 'grey')

    ctk.CTkLabel(app,text='Famille:', font=("Arial", 25)).place(relx=0.025, rely=0.05,anchor=W)
    elemNature = ctk.CTkLabel(app, text = 'Non-métaux', font=("Arial", 25))
    elemNature.place(relx=0.025, rely=0.1,anchor=W)

    elemValHeader = ctk.CTkLabel(app, text = 'Nombre de liaisons', font=("Arial", 25))
    elemValHeader.place(relx=0.975, rely=0.05,anchor=E)

    elemVal = ctk.CTkLabel(app, text = '1 électron(s)', font=("Arial", 25))
    elemVal.place(relx=0.975, rely=0.1,anchor=E)

    '''Ztextbox = ctk.CTkTextbox(app, width = 45,height=5,state="normal")
    Ztextbox.insert("0.0","1")
    Ztextbox.place(relx=0.35, rely=0.95,anchor=CENTER)'''


    def create_circle(x, y, r, canvas,colour=None):
        if colour is None:
            return canvas.create_oval(x - r, y - r, x + r, y + r, width=1.75, outline="white")
        else:
            return canvas.create_oval(x - r, y - r, x + r, y + r, width=0.5, fill=colour)


    elecs = []
    currVal = 1
    isTurning = False

    def Zwork(feedback=None):
        global elecs, currVal, dessN, dessZ, currZ, currN, NZ
        if feedback is None:
            ZworkVerbose = ctk.CTkInputDialog(text="Entrer le nombre Z (1-102)",title="Nombre Z")
            value = ZworkVerbose.get_input()#Ztextbox.get("0.0","end")
        else:
            value = int(feedback)
        try:
            if (1>int(value)) or (int(value)>102):
                raise ValueError
            index = int(value)-1
            currN = neutrons[index]
            currZ = index+1
            Anum.configure(text=str(currZ+currN))
            Znum.configure(text=str(currZ))
            elemSymbol.configure(text=elems[index])
            #elemySy.configure(text=str(index+1+neutrons[index])+"\n        "+elems[index]+"\n"+str(index+1))
            elemNature.configure(text=retrieveNature(elems[index]))
            try:
                elemValHeader.configure(text="Nombre de liaisons")
                currVal = valency[index]
                if not isinstance(currVal, tuple):
                    if currVal > 7:
                        elemVal.configure(text="?")
                    else:
                        elemVal.configure(text=str(currVal)+" électron(s)")
                else:
                    elemVal.configure(text=str(currVal)[1:-1]+" électron(s)")
            except IndexError:
                elemValHeader.configure(text="")
                elemVal.configure(text="")
            name = names[index][0]
            elemName.configure(text=name)
            elecs = [i[:-2] if len(i) > 2 else i for i in getShellsVal(name)[0].split(")")]
            elecs = elecs[1:]
            elemsBox.set(str(value)+"-"+name)
            print(name, *elecs)
            
        except ValueError:
            elemValHeader.configure(text="Nombre de liaisons")
            elemSymbol.configure(text="H")
            currN = 0
            currZ = 1
            elemName.configure(text='Hydrogène')
            elemNature.configure(text='Non-métaux')
            Anum.configure(text="1")
            Znum.configure(text="1")
            elecs = [1]
            currVal = 1
            elemVal.configure(text=str(currVal)+" électron(s)")
            elemsBox.set("1-Hydrogène")
            print("Merci d'entrer une valuer valable (utilisant l'Hydrogène par défaut)")
      
    def elemsBoxy(elemy):
        #Ztextbox.delete("0.0","end")
        #Ztextbox.insert("0.0",elemy.split("-")[0])
        Zwork(elemy.split("-")[0])

    def toggleTurn():
        global isTurning
        isTurning = not isTurning

    #elemSymbol.configure(text="H")
    elemName.configure(text='Hydrogène')
    elemNature.configure(text='Non-métaux')
    elecs = [1]

    zInput = ctk.CTkButton(master=app, text="Choisir le nombre Z", font=("Arial",25), command=Zwork)
    zInput.place(relx=0.5, rely=0.95, anchor=CENTER)

    button2 = ctk.CTkButton(master=app, text="Animer", font=("Arial",25),command=toggleTurn, width = 100)
    button2.place(relx=0.975, rely=0.95, anchor=E)

    elemsBox = ctk.CTkOptionMenu(master=app,
                                     values=[str(i+1)+"-"+names[i][0] for i in range(len(names))],
                                     command=elemsBoxy)
    elemsBox.configure(width=200, height=30)
    elemsBox.set("1-Hydrogène")
    elemsBox.place(relx=0.5, rely=0.05,anchor=CENTER)

    electronImg = ImageTk.PhotoImage(Image.open("./res/electron.png").resize((25, 25), Image.Resampling.LANCZOS))
    protonImg = ImageTk.PhotoImage(Image.open("./res/proton.png").resize((25, 25), Image.Resampling.LANCZOS))
    neutronImg = ImageTk.PhotoImage(Image.open("./res/neutron.png").resize((25, 25), Image.Resampling.LANCZOS))
    caseImg = ImageTk.PhotoImage(Image.open("./res/case.png").resize((100, 100), Image.Resampling.LANCZOS))

    def hadron(hadron, x, y):
        if hadron == 'proton':
            canvas.create_image(x, y, anchor=CENTER, image=protonImg)
        else:
            canvas.create_image(x, y, anchor=CENTER, image=neutronImg)

    def circle_dist(cx,cy,N,n1,n2,nd1,nd2,rayon,randy=False):
        if N <= 4 and n1 == 1:
            rayon = 0
            
        for i in range(N):
            nudgy = random.uniform(-1,1) if isTurning else 0
            nudgx = random.uniform(-1,1) if isTurning else 0
            angle = i * (np.pi*2 / (n1+n2))#+random.uniform(0,np.pi*2)
            x = cx + rayon * np.cos(angle)+nudgx
            y = cy + rayon * np.sin(angle)+nudgy

            if nd1 < n1 and nd2 < n2:
                if (nd1+nd2)%2==0:
                    currHadron = "proton"
                else:
                    currHadron = "neutron"
            elif nd1 < n1:
                currHadron = "proton"
            elif nd2 < n2:
                currHadron = "neutron"
            elif randy:
                #currHadron = np.random.choice(["proton","neutron"],p=[0.6,0.4])
                if (nd1+nd2)%3==0:
                    currHadron = "proton"
                else:
                    currHadron = "neutron"

            hadron(currHadron, x, y)
            
            if currHadron == "proton":
                nd1 += 1
            else:
                nd2 += 1
    Zwork(1)

    def updateGraphics():
        global t, dessN, dessZ, currZ, currN, NZ
        #t -= np.pi/8 if isTurning else 0 #ternary
        t -= random.uniform(0,np.pi/2) if isTurning else 0
        canvas.delete("all")
        #canvas.move()
        width = app.winfo_width()
        Cx = width//2
        height = app.winfo_height()
        Cy = height//2
        canvas.configure(height=height,width=width)

        canvas.create_image(width/40 + (width-800)/15, height*0.825, anchor=W, image=caseImg)

        create_circle(width*9/10,height*8/10,50,canvas,"#"+atomColors[currZ-1])

        #print(width, height)
        for i in range(1,len(elecs)+1):
            create_circle(Cx,Cy,i*30+50,canvas)
        #app.after(int(1e2), updateGraphics)

        for i in range(1,len(elecs)+1):
            randAng0 = random.uniform(0,np.pi*2) if isTurning else 0
            i = int(i)
            for j in range(int(elecs[i-1])):
                da = ((2*np.pi)/int(elecs[i-1]))*j + randAng0
                #da = ((2*np.pi)/shellex[i-1])*j
                r = 50+i*30
                canvas.create_image(r*np.cos(t+da) + Cx, r*np.sin(t+da) + Cy, anchor=CENTER, image=electronImg)
                #create_circle(r*np.cos(t+da) + width//2, r*np.sin(t+da) + height//2, 8, canvas)

        dessN = 0
        dessZ = 0

        
        #circle_dist(Cx, Cy, currZ+currN, currZ, currN, dessZ, dessN, (currZ+currN)*15/4)
        
        '''for i in range(1, currZ + currN + 1):
            currHadron = 'proton'
            if i <= NZ[0]:
                circle_dist(Cx, Cy, NZ[0], currZ, currN, dessZ, dessN, NZ[0]*15/4)
            elif NZ[0] < i <= NZ[1]:
                circle_dist(Cx, Cy, NZ[1], currZ, currN, dessZ, dessN, NZ[1]*15/4)'''

        AT = currZ + currN
        #currHadron = 'proton'
        if NZ[3] >= AT and 51 >= AT > 30:
            circle_dist(Cx, Cy, NZ[3], currZ-15, currN-15, dessZ, dessN, 15*15/4)
        elif NZ[3] <= AT+8:
            circle_dist(Cx, Cy, NZ[3], 11, 11, dessZ, dessN, 15*15/4,True)
        if NZ[2] >= AT and AT > 12:
            circle_dist(Cx, Cy, NZ[2], currZ-6, currN-6, dessZ, dessN, 9*15/3)
        elif NZ[2] < AT and AT >= 28:
            circle_dist(Cx, Cy, NZ[2], 8, 8, dessZ, dessN, 9*15/3)
        if NZ[1] >= AT-7 and AT > 6:#not NZ[0] >= AT:
            circle_dist(Cx, Cy, NZ[1], currZ-3, currN-3, dessZ, dessN, NZ[1]*15/5)
        elif NZ[1] <= AT:
            circle_dist(Cx, Cy, NZ[1], 4, 4, dessZ, dessN, NZ[1]*15/5)
        if NZ[0] >= AT:
            circle_dist(Cx, Cy, NZ[0], currZ, currN, dessZ, dessN, NZ[0]*15/5)
        elif NZ[0] < AT:
            circle_dist(Cx, Cy, NZ[0], 2, 2, dessZ, dessN, NZ[0]*15/5)
        app.after(int(1e2), updateGraphics)


    #GUM LOGIC
    def gumCall():
        global guide
        if guide is None:
            guide = gum.createGuideWindow(app, "Guide: L'atome","atom.txt")
        else:
            guide.destroy()
            guide = gum.createGuideWindow(app, "Guide: L'atome","atom.txt")

    gumButton = ctk.CTkButton(app,text="Guide",width=50,height=20,command=gumCall,image=ctk.CTkImage(dark_image=Image.open("./res/guide.png"),size=(30, 30)))
    gumButton.place(relx=0.95,rely=0.5,anchor=E)
        
    app.after(int(1e3/2), updateGraphics)
    return app
    app.mainloop()

if __name__ == '__main__':
    mainy = ctk.CTk()
    MAIN_ATOM(mainy)
