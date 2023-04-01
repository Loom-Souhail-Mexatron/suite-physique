from tkinter import *
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
from functools import lru_cache
from Sou_Sapphire_Solver import LAPLACE_SOLVE_MECH, EXTREMAS
from PIL import Image,ImageTk
import numpy as np
import guideManager as gum
import time

guide = None

def MAIN_MECH(mainy):
    global guide
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTkToplevel(mainy)
    app.geometry("750x450")
    app.resizable(False,False)
    app.title("Mécanique")

    canvas = Canvas(app,bg="#1A1A1A",width=750,height=450)
    canvas.pack()

    mEntry = ctk.CTkEntry(app, font=("Arial", 25), width = 100,height=5)
    hEntry = ctk.CTkEntry(app, font=("Arial", 25), width = 100,height=5)
    kEntry = ctk.CTkEntry(app, font=("Arial", 25), width = 100,height=5)
    x0Entry = ctk.CTkEntry(app, font=("Arial", 25), width = 100,height=5)
    v0Entry = ctk.CTkEntry(app, font=("Arial", 25), width = 100,height=5)
    mEntry.place(relx=0.25,rely=0.5,anchor='center')
    hEntry.place(relx=0.5,rely=0.5,anchor='center')
    kEntry.place(relx=0.75,rely=0.5,anchor='center')
    x0Entry.place(relx=1/3,rely=2/3,anchor='center')
    v0Entry.place(relx=2/3,rely=2/3,anchor='center')
    mEntry.insert(0,'1')
    hEntry.insert(0,'0.1')
    kEntry.insert(0,'1')
    x0Entry.insert(0,'0')
    v0Entry.insert(0,'0')
    ctk.CTkLabel(app,text="Masse [Kg]", font=("Arial", 22)).place(relx=0.25,rely=0.45,anchor=S)
    ctk.CTkLabel(app,text="Frottement [Kg.s-1]", font=("Arial", 22)).place(relx=0.5,rely=0.45,anchor=S)
    ctk.CTkLabel(app,text="Raideur [N.m-1]", font=("Arial", 22)).place(relx=0.75,rely=0.45,anchor=S)
    ctk.CTkLabel(app,text="Position Initiale [m]", font=("Arial", 22)).place(relx=1/3,rely=0.62,anchor=S)
    ctk.CTkLabel(app,text="Vitesse Initiale [m.s-1]", font=("Arial", 22)).place(relx=2/3,rely=0.62,anchor=S)

    def imgManip(name,width,height):
        return ImageTk.PhotoImage(Image.open("./res/"+name+".png").resize((int(width), int(height)), Image.Resampling.LANCZOS))

    boxImg = imgManip('box',70,70)
    boxOffset = 8
    xBox = 400
    yBox = 100 + boxOffset
    xBorder = 50
    yBorder = 100
    yLine = 135
    borderImg = imgManip('border',70,70)
    springIm = Image.open("./res/spring.png")
    springScale = 350-70//2+boxOffset
    springImg = ImageTk.PhotoImage(springIm.resize((int(abs(springScale)), 70), Image.Resampling.LANCZOS))
    boxShape = canvas.create_image(xBox,yBox,anchor='center',image=boxImg)
    canvas.create_image(xBorder,yBorder,anchor='center',image=borderImg)
    springShape = canvas.create_image(xBorder+springScale//2,yBox,anchor='center',image=springImg)
    canvas.create_line(49, yLine, 730, yLine,width=2,fill='white')
    xO, yO = 400, 100
    canvas.create_line(xO,yO+35,xO,yO+35+boxOffset//2,width=2,fill='white')
    canvas.create_text(xO-0.75,yO+35+boxOffset*1.5,anchor='center',text='o',font=('Arial',20),fill='white')
    globals().update({'springGarbage' : {}})

    def updatePosValue(event):
        springGarbage.clear()
        try:
            actualX = 10*float(x0Entry.get())+400
        except:
            actualX = 0
            x0Entry.delete(0,END)
            x0Entry.insert(0,'0')
        canvas.coords(boxShape,actualX,yBox)
        springScale = actualX-70-boxOffset
        springImg = ImageTk.PhotoImage(springIm.resize((int(np.max([abs(springScale),1])), 70), Image.Resampling.LANCZOS))
        springGarbage.update({'t'+str(actualX):springImg})
        canvas.coords(springShape,xBorder+springScale//2,yBox)
        canvas.itemconfig(springShape,image=springImg)
    def updaterPos(event):
        updatePosValue(event)
        canvas.after(2,updatePosValue,event)
    def updatePos(event):
        springGarbage.clear()
        canvas.coords(boxShape,event.x,yBox)
        springScale = event.x-70-boxOffset
        springImg = ImageTk.PhotoImage(springIm.resize((int(np.max([abs(springScale),1])), 70), Image.Resampling.LANCZOS))
        springGarbage.update({'t'+str(event.x):springImg})
        canvas.coords(springShape,xBorder+springScale//2,yBox)
        canvas.itemconfig(springShape,image=springImg)
    def set_newpos(event):
        updatePos(event)
        x0Entry.delete(0,END)
        x0Entry.insert(0,str((event.x-400)/10))
    canvas.bind('<B1-Motion>', updatePos)
    canvas.bind('<ButtonRelease-1>', set_newpos)
    x0Entry.bind('<Key>',updaterPos)
    x0Entry.bind('<ButtonRelease>',updaterPos)
    
    def unpack_values():
        m = float(mEntry.get())
        h = float(hEntry.get())
        k = float(kEntry.get())
        x0 = float(x0Entry.get())
        v0 = float(v0Entry.get())
        try:
            assert (m > 0) and (h >= 0) and (k > 0)
        except:
            print("Donnez des valuers positives/valides.")
            return [0,0,0,0,0]
        return [m,h,k,x0,v0]

    def nulReturn():
        return 0
    sim = False
    func = nulReturn()
    funcPRIME = nulReturn()
    T0 = time.time()
    def simuler():
        global sim, func, funcPRIME, T0
        m, h, k,x0,v0 = unpack_values()
        sim = True
        if m*k == 0:
            sim = False
        if sim:
            func = LAPLACE_SOLVE_MECH(m,h,k,x0,v0)
            funcPRIME = LAPLACE_SOLVE_MECH(m,h,k,x0,v0,1)
            T0 = time.time()
            updateGraphics(h,k,0)
            
    def arreter(memes=False):
        global sim
        sim = False
        canvas.delete('all')
        springGarbage.clear()
        boxOffset = 8
        xBox = 400
        yBox = 100 + boxOffset
        xBorder = 50
        yBorder = 100
        yLine = 135
        springScale = 350-70//2+boxOffset
        boxShape = canvas.create_image(xBox,yBox,anchor='center',image=boxImg)
        canvas.create_image(xBorder,yBorder,anchor='center',image=borderImg)
        springShape = canvas.create_image(xBorder+springScale//2,yBox,anchor='center',image=springImg)
        canvas.create_line(49, yLine, 730, yLine,width=2,fill='white')
        canvas.create_line(xO,yO+35,xO,yO+35+boxOffset//2,width=2,fill='white')
        canvas.create_text(xO-0.75,yO+35+boxOffset*1.5,anchor='center',text='o',font=('Arial',20),fill='white')
        def updatePos(event):
            springGarbage.clear()
            canvas.coords(boxShape,event.x,yBox)
            springScale = event.x-70-boxOffset
            springImg = ImageTk.PhotoImage(springIm.resize((int(np.max([abs(springScale),1])), 70), Image.Resampling.LANCZOS))
            springGarbage.update({'t'+str(event.x):springImg})
            canvas.coords(springShape,xBorder+springScale//2,yBox)
            canvas.itemconfig(springShape,image=springImg)
        def set_newpos(event):
            updatePos(event)
            x0Entry.delete(0,END)
            x0Entry.insert(0,str((event.x-400)/10))
        def updatePosValue(event):
            springGarbage.clear()
            try:
                actualX = 10*float(x0Entry.get())+400
            except:
                actualX = 0
                x0Entry.delete(0,END)
                x0Entry.insert(0,'0')
            canvas.coords(boxShape,actualX,yBox)
            springScale = actualX-70-boxOffset
            springImg = ImageTk.PhotoImage(springIm.resize((int(np.max([abs(springScale),1])), 70), Image.Resampling.LANCZOS))
            springGarbage.update({'t'+str(actualX):springImg})
            canvas.coords(springShape,xBorder+springScale//2,yBox)
            canvas.itemconfig(springShape,image=springImg)
        def updaterPos(event):
            updatePosValue(event)
            canvas.after(2,updatePosValue,event)
        if memes:
            canvas.bind('<B1-Motion>', updatePos)
            canvas.bind('<ButtonRelease-1>', set_newpos)
            x0Entry.bind('<Key>',updaterPos)
            x0Entry.bind('<ButtonRelease>',updaterPos)
        if not memes:
            app.after(50,arreter,True)
            
    def energyPlot():
        m, h, k,x0,v0 = unpack_values()
        X, Y = [],[]
        if not (m*k == 0):
            TIME = np.linspace(0,20*np.sqrt(m/k),400)
            X = np.real(LAPLACE_SOLVE_MECH(m,h,k,x0,v0)(TIME))
            V = np.real(LAPLACE_SOLVE_MECH(m,h,k,x0,v0,1)(TIME))
            Ep = 0.5*(X**2)*k
            Ec = 0.5*(V**2)*m
            Et = [Ep[i]+Ec[i] for i in range(len(TIME))]
            maxE = max(Et)
            plt.figure()
            title = 'Énergie en Oscillations en Régime '
            sgn = -int(np.sign(h*h-4*m*k))
            if h==0:
                title+='Harmonique'
            else:
                title += ['Apériodique','Critique','Pseudo-Périodique'][sgn+1]
            title += r', $\zeta$ = '+str(np.round(h/(2*np.sqrt(k*m)),2))
            plt.title(title)
            plt.plot(X, Ep,color='fuchsia',label='Énergie Potentielle',lw=2)
            plt.plot(X, Ec,color='dodgerblue',label='Énergie Cinétique',lw=2)
            plt.gca().xaxis.set_major_formatter(EngFormatter(unit='m'))
            plt.gca().yaxis.set_major_formatter(EngFormatter(unit='J'))
            try:
                extX = EXTREMAS(X)
                maxX = X[extX[0][0]]
                minX = X[extX[1][0]]
                if x0 < minX:
                    minX = x0
                elif x0 > maxX:
                    maxX = x0
                plt.vlines(maxX,0,maxE,linestyles='--',color='black')
                plt.vlines(minX,0,maxE,linestyles='--',color='black')
                if h==0:
                    plt.gca().text(maxX,0,r'$X_m$')
                    plt.gca().text(minX,0,r'$-X_m$')
            except IndexError:
                print('')
            plt.plot(X,Et,color='mediumorchid',label='Énergie Totale')
            if h==0:
                plt.gca().text(0,maxE,'E')
            plt.xlabel('Position')
            plt.ylabel('Énergie')
            plt.legend()
            plt.grid()
            plt.show()

    def phasePlot():
        m, h, k,x0,v0 = unpack_values()
        X, Y = [],[]
        if not (m*k == 0):
            TIME = np.linspace(0,50*np.sqrt(m/k),400)
            X = np.real(LAPLACE_SOLVE_MECH(m,h,k,x0,v0)(TIME))
            V = np.real(LAPLACE_SOLVE_MECH(m,h,k,x0,v0,1)(TIME))
            plt.figure()
            eigenValue = -h/(2*m) #ou valuer propre
            sqrt = ((h/m)**2 - 4*(k/m))/2
            sqrt = np.sqrt(sqrt) if (sqrt>=0) else np.sqrt(-sqrt)*1j
            eigenPlus = eigenValue+sqrt
            eigenMinus = eigenValue-sqrt
            lambdaTitle = r'$\lambda_1 =$'+ str(np.round(np.real(eigenPlus),2)) +(r'$+$' if np.imag(eigenPlus)>=0 else r'$-$')+ str(np.round(np.imag(eigenPlus),2)) +r'$i$'
            lambdaTitle += r', $\lambda_2 =$'+ str(np.round(np.real(eigenMinus),2)) +(r'$+$' if np.imag(eigenMinus)>=0 else r'')+ str(np.round(np.imag(eigenMinus),2)) +r'$i$'
            plt.title("Diagramme de l'Espace des Phases " + lambdaTitle)
            plt.plot(X, V, color='purple',label='Trajectoire de Phase')
            plt.scatter(0,0,color='green',label="Point d'Equilibre")
            plt.xlabel('Position')
            plt.ylabel('Vitesse')
            plt.grid()
            plt.legend()
            plt.show()

    ctk.CTkButton(app,text="Simuler", font=("Arial", 24),command=simuler).place(relx=1/3,rely=0.8,anchor=CENTER)
    ctk.CTkButton(app,text="Réinitialiser", font=("Arial", 24),command=arreter).place(relx=2/3,rely=0.8,anchor=CENTER)
    ctk.CTkButton(app,text="Tracer l'énergie", font=("Arial", 24),command=energyPlot).place(relx=1/3,rely=0.9,anchor=CENTER)
    ctk.CTkButton(app,text="Plan de Phase", font=("Arial", 24),command=phasePlot).place(relx=2/3,rely=0.9,anchor=CENTER)


    FPS = 24
    #@lru_cache
    def updateGraphics(h,k,t):
        global sim, func, funcPRIME,T0
        #canvas.place(rely=0.5,relx=0.5,anchor=CENTER)
        canvas.delete('all')
        springGarbage.clear()

        if sim:
            #print(func(t))
            xBox = np.real(func(t))*10+400
            
            canvas.create_image(xBox,yBox,anchor='center',image=boxImg)
            canvas.create_image(xBorder,yBorder,anchor='center',image=borderImg)

            #springScale = abs((300-70//2+boxOffset)*np.cos(10*t))
            #springScale = abs((300-70//2+boxOffset)*2*np.cos(10*t))
            #springImg = imgManip('spring',springScale,70)
            T = k*(xBox-400)
            springScale = xBox-70-boxOffset
            springImg = ImageTk.PhotoImage(springIm.resize((int(np.max([abs(springScale),1])), 70), Image.Resampling.LANCZOS))
            springGarbage.update({'t'+str(t):springImg})
            canvas.create_image(xBorder+springScale//2,yBox,anchor='center',image=springImg)
            
            canvas.create_line(49, yLine, 730, yLine,width=2,fill='white')

            prOffset = 1
        
            #Vecteur Poids
            canvas.create_text(xBox+16-prOffset,yBox+44,text=u'\u20D7',font=("Arial", 24),fill='lime')
            canvas.create_text(xBox+15-prOffset,yBox+45,text='P',font=("Arial", 15),fill='lime')
            canvas.create_line(xBox-prOffset, yBox, xBox-prOffset, yBox+70, arrow=LAST,fill='lime',width=2)

            #Vecteur Réaction
            canvas.create_text(xBox+16+prOffset,yBox-1,text=u'\u20D7',font=("Arial", 24),fill='red')
            canvas.create_text(xBox+15+prOffset,yBox,text='R',font=("Arial", 15),fill='red')
            canvas.create_line(xBox+prOffset, yBox+35-boxOffset, xBox+prOffset, yBox-75+35, arrow=LAST,fill='red',width=2)

            #Vecteur Tension
            canvas.create_text(xBox-35+boxOffset-T/8,yBox-boxOffset-8,text=u'\u20D7',font=("Arial", 24),fill='cyan')
            canvas.create_text(xBox-35+boxOffset-T/8,yBox-boxOffset-7,text='T',font=("Arial", 15),fill='cyan')
            canvas.create_line(xBox-35+boxOffset, yBox, xBox-35+boxOffset-T/4, yBox, arrow=LAST,fill='cyan',width=2)

            #Vecteur Tension
            f = 50*np.real(funcPRIME(t))*h
            canvas.create_text(xBox-f/4,yBox-boxOffset-8+35,text=u'\u20D7',font=("Arial", 24),fill='red')
            canvas.create_text(xBox-f/4,yBox-boxOffset-7+35,text='f',font=("Arial", 15),fill='red')
            canvas.create_line(xBox, yBox+35-boxOffset, xBox-f/2, yBox+35-boxOffset, arrow=LAST,fill='red',width=2)

            canvas.create_line(xO,yO+35,xO,yO+35+boxOffset//2,width=2,fill='white')
            canvas.create_text(xO-0.75,yO+35+boxOffset*1.5,anchor='center',text='o',font=('Arial',20),fill='white')

            #print(time.time())
            t = time.time() - T0
            #t += 1
            canvas.after(10,updateGraphics, h,k,t)

    #GUM LOGIC
    def gumCall():
        global guide
        if guide is None:
            guide = gum.createGuideWindow(app, "Guide: Mécanique", "mech.txt")
        else:
            guide.destroy()
            guide = gum.createGuideWindow(app, "Guide: Mécanique", "mech.txt")

    gumButton = ctk.CTkButton(app,text="Guide",width=50,height=20,command=gumCall,image=ctk.CTkImage(dark_image=Image.open("./res/guide.png"),size=(30, 30)))
    gumButton.place(relx=0.5,rely=0.75,anchor=CENTER)
    
    return app
    #app.after(10, updateGraphics, 0)
    app.mainloop()

if __name__ == '__main__':
    MAIN_MECH(ctk.CTk())
