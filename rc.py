from tkinter import *
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
from Sou_Sapphire_Solver import DIFF_SOLVE, EXTREMAS, LAPLACE_SOLVE
from PIL import Image,ImageTk
import numpy as np
import guideManager as gum
guide = None

def XY_Units(x,y,x_title,y_title,axes=None):
    if axes == None:
        plt.gca().xaxis.set_major_formatter(EngFormatter(unit=x))
        plt.gca().yaxis.set_major_formatter(EngFormatter(unit=y))
    else:
        axes.xaxis.set_major_formatter(EngFormatter(unit=x))
        axes.yaxis.set_major_formatter(EngFormatter(unit=y))
    plt.xlabel(x_title + ' [' + x +']')
    plt.ylabel(y_title + ' [' + y +']')

def MAIN_RLC_LIBRE(mainy):
    global guide
    guide = None

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTkToplevel(mainy)
    app.geometry("750x350")
    app.resizable(False,False)
    app.title("Circuit RLC Libre")
    

    #app.mainloop()

    def RLCTools(choice):
        if choice == "RLC Forcé":
            app.destroy()
            MAIN_RLC_FORCE(mainy)
        if choice == "RC":
            app.destroy()
            MAIN_RC(mainy)
        else:
            return 0

    RLCBox = ctk.CTkOptionMenu( master=app,
                                values=["RLC Libre","RLC Forcé", "RC"],
                                command=RLCTools,
                                width=200, height=30)
    RLCBox.place(relx=0.5,rely=0.95,anchor=CENTER)

    #Canvas definition
    coff = 1.75
    rlclImg = ImageTk.PhotoImage(Image.open("./res/rlcl.png").resize((int(120*coff), int(128*coff)), Image.Resampling.LANCZOS))
    canvas = Canvas(app,bg="#1A1A1A")
    canvas.grid(row=0,column=3,columnspan=3,rowspan=5)
    canvas.create_image(200,130,anchor='center',image=rlclImg)

    #Labels
    '''canvas.create_text(x,y,text="Condensateur",font=('Arial',20),fill="white")
    canvas.create_text(x,y,text="Résistor",font=('Arial',20),fill="white")
    canvas.create_text(x,y,text="Bobine",font=('Arial',20),fill="white")'''

    #Entries
    #R = 0.1, C = 1e-7, E = 12, L = 1e-8
    entryWidth = 150
    PADY_CONST = 1
    PADX_CONST = 1
    fontName = "Arial"
    fontSize = 18
    
    ctk.CTkLabel(app,text="Résistance R",font=(fontName,fontSize)).grid(row=0,column=0,pady=PADY_CONST,padx=PADX_CONST)
    entryResistance     = ctk.CTkEntry(app, width=entryWidth, placeholder_text="Résistance [Ω]", corner_radius=10,font=(fontName,fontSize))
    entryResistance.insert(0,'0.1')
    entryResistance.grid(row=0,column=1,pady=PADY_CONST,padx=PADX_CONST)
    ctk.CTkLabel(app,text="Ω",font=(fontName,fontSize)).grid(row=0,column=2,pady=PADY_CONST,padx=PADX_CONST)
    
    ctk.CTkLabel(app,text="Capacité C",font=(fontName,fontSize)).grid(row=1,column=0,pady=PADY_CONST,padx=PADX_CONST)
    entryCapacitance    = ctk.CTkEntry(app, width=entryWidth, placeholder_text="Capacité [F]", corner_radius=10,font=(fontName,fontSize))
    entryCapacitance.insert(0,'1')
    entryCapacitance.grid(row=1,column=1,pady=PADY_CONST,padx=PADX_CONST)
    ctk.CTkLabel(app,text="F",font=(fontName,fontSize)).grid(row=1,column=2,pady=PADY_CONST,padx=PADX_CONST)
    
    ctk.CTkLabel(app,text="F.E.M. E",font=(fontName,fontSize)).grid(row=2,column=0,pady=PADY_CONST,padx=PADX_CONST)
    entryFEM            = ctk.CTkEntry(app, width=entryWidth, placeholder_text="F.E.M. [V]", corner_radius=10,font=(fontName,fontSize))
    entryFEM.insert(0,'12')
    entryFEM.grid(row=2,column=1,pady=PADY_CONST,padx=PADX_CONST)
    ctk.CTkLabel(app,text="V",font=(fontName,fontSize)).grid(row=2,column=2,pady=PADY_CONST,padx=PADX_CONST)
    
    ctk.CTkLabel(app,text="Inductance L",font=(fontName,fontSize)).grid(row=3,column=0,pady=PADY_CONST,padx=PADX_CONST)
    entryInductance     = ctk.CTkEntry(app, width=entryWidth, placeholder_text="Inductance [H]", corner_radius=10,font=(fontName,fontSize))
    entryInductance.insert(0,'1')
    entryInductance.grid(row=3,column=1,pady=PADY_CONST,padx=PADX_CONST)
    ctk.CTkLabel(app,text="H",font=(fontName,fontSize)).grid(row=3,column=2,pady=PADY_CONST,padx=PADX_CONST)
    
    ctk.CTkLabel(app,text="Résistance r",font=(fontName,fontSize)).grid(row=4,column=0,pady=PADY_CONST,padx=PADX_CONST)
    entryResInducta     = ctk.CTkEntry(app, width=entryWidth, placeholder_text="Résistance [Ω]", corner_radius=10,font=(fontName,fontSize))
    entryResInducta.insert(0,'0')
    entryResInducta.grid(row=4,column=1,pady=PADY_CONST,padx=PADX_CONST)
    ctk.CTkLabel(app,text="Ω",font=(fontName,fontSize)).grid(row=4,column=2,pady=PADY_CONST,padx=PADX_CONST)
    
    def unpack_values():
        try:
            R = float(entryResistance.get())
            r = float(entryResInducta.get())
            C = float(entryCapacitance.get())
            L = float(entryInductance.get())
            E = float(entryFEM.get())
            assert ((R+r)>=0) and (C>0) and (L>0) and (E>0)
        except:
            print("Merci d'entrer des valuers valides et positives")
            print("Utilisant les valeurs par défaut...")
            return [0.1,1,1,12]
        return [R+r,C,L,E]

    def diff_q(t,y):
        R, C, L, E = unpack_values()
        dy0 = y[1]
        dy1 = - (R/L)*y[1] - (1/(L*C))*y[0]
        return [dy0, dy1]

    def plot_q():
        R, C, L, E = unpack_values()

        y0 = [C*E, 0]
        t_span = (0, 5*2*np.pi*np.sqrt(L*C))

        RLC_diff = r'$L\frac{\mathrm{d^2} Q(t)}{\mathrm{d} t^2}+R \frac{\mathrm{d} Q(t)}{\mathrm{d} t}+\frac{1}{C}Q(t)=0$'
        #sol_q = solve_ivp(diff_q, t_span, y0, method='RK23')

        #q_t = sol_q.t
        #sol_q0 = sol_q.y[0]
        #q_prime = sol_q.y[1]

        q_t = np.linspace(t_span[0],t_span[1],400)
        diff_qsol = DIFF_SOLVE(L,R,1/C,C*E)
        sol_q0 = np.array([diff_qsol(t) for t in q_t])

        plt.figure()
        plt.title("Charge au Condensateur")
        plt.gcf().canvas.manager.set_window_title(f'Charge pour R = {R}, C = {C}, L = {L} et E = {E}')
        XY_Units('s','C','Temps','Charge')
        plt.plot(q_t,sol_q0,label=RLC_diff,color='red')
        plt.ylim(min(sol_q0),max(sol_q0))
        #extremas = list(argrelextrema(sol_q0, np.greater))[0]
        #minimas  = list(argrelextrema(sol_q0, np.less))[0]
        extremas = EXTREMAS(sol_q0)[0]
        minimas = EXTREMAS(sol_q0)[1]

        '''engFormatted = EngFormatter()(tensionCircuit*(1-np.exp(-i)))
        engSplit = engFormatted.split('.')
        taus.append((str(i)+r'$\tau$',engSplit[0]+'.'+engSplit[1][:2]+engFormatted[-1]+"V"))'''

        def formatterThing(num):
                if abs(num) > 1e9:
                    return '{:.2f}G'.format(num/1e9)
                elif abs(num) > 1e6:
                    return '{:.2f}M'.format(num/1e6)
                elif abs(num) > 1e3:
                    return '{:.2f}k'.format(num/1e3)
                elif abs(num) > 1e-3:
                    return '{:.f}'.format(num)
                elif abs(num) > 1e-6:
                    return '{:.2f}$\\mathdefault{\\mu}$'.format(num*1e6)
                elif abs(num) > 1e-9:
                    return '{:.2f}n'.format(num*1e9)
                else:
                    return '{:.2f}p'.format(num*1e12)
        prefixFormatter = EngFormatter()
        prefixFormatter.format = formatterThing
        
        for i in [*extremas[:2]]:
            plt.hlines(y = sol_q0[i], xmin= 0,
               xmax = q_t[i], colors = "purple",
               linestyles="dashed")
            engFormatted = EngFormatter()(sol_q0[i]).split('.')
            plt.text(-0.05,sol_q0[i]/(abs(min(sol_q0))+max(sol_q0))+0.45,prefixFormatter(sol_q0[i]) +"C",
               bbox={'facecolor': 'blue', 'alpha': 0.75, 'pad': 2},
               horizontalalignment='center',
               verticalalignment='center',
               fontsize = 12,
               transform=plt.gca().transAxes)
        for i in [*minimas[:2]]:
            plt.hlines(y = sol_q0[i], xmin= 0,
               xmax = q_t[i], colors = "purple",
               linestyles="dashed")
            engFormatted = EngFormatter()(sol_q0[i]).split('.')
            plt.text(-0.05,sol_q0[i]/(abs(min(sol_q0))+max(sol_q0))+0.45,prefixFormatter(sol_q0[i]) + "C",
               bbox={'facecolor': 'blue', 'alpha': 0.75, 'pad': 2},
               horizontalalignment='center',
               verticalalignment='center',
               fontsize = 12,
               transform=plt.gca().transAxes)
        plt.grid()
        plt.legend()
        plt.show()

    def plot_i():
        R, C, L, E = unpack_values()

        t_span = (0, 5*2*np.pi*np.sqrt(L*C))

        RLC_diff = r'$L\frac{\mathrm{d^2} i(t)}{\mathrm{d} t^2}+R \frac{\mathrm{d} i(t)}{\mathrm{d} t}+\frac{1}{C}i(t)=0$'
        #sol_q = solve_ivp(diff_q, t_span, y0, method='RK23')

        #q_t = sol_q.t
        #sol_i0 = sol_q.y[1] #I = Q'

        q_t = np.linspace(t_span[0],t_span[1],400)
        diff_isol = DIFF_SOLVE(L,R,1/C,C*E,derivative=True)
        sol_i0 = np.array([diff_isol(t) for t in q_t])

        plt.figure()
        plt.title("Intensité au circuit")
        plt.gcf().canvas.manager.set_window_title(f'Intensité pour R = {R}, C = {C}, L = {L} et E = {E}')
        XY_Units('s','A','Temps','Intensité')
        plt.plot(q_t,sol_i0,label=RLC_diff,color='green')
        plt.grid()
        plt.legend()
        plt.show()

    def plot_e():
        R, C, L, E = unpack_values()

        y0 = [C*E, 0]
        t_span = (0, 5*2*np.pi/np.sqrt(L*C))
        
        #ENERGIE
        if R == 0:
            antiF = E
            t = np.linspace(0,t_span[1],500)
            hDT = 1e-5
            #E_m = (0.5*L*(sol_q.y[1]**2))
            #E_m = E*2*np.pi*L*np.abs(np.sin(C*E*t/antiF)**2)
            E_m = 0.25*L*(((C*E*(t+hDT)-C*E*t)/hDT)**2)*(1-np.cos(2*np.sqrt(L*C)*t))
            #E_e = 0.5*(sol_q.y[0]**2)/C
            E_e = ((y0[0]**2)/(C))*0.25*(1+np.cos(2*np.sqrt(L*C)*t))
            #E_e = E*2*np.pi*np.abs(np.cos(C*E*t/antiF)**2)/C
            E_t = E_m + E_e
        else:       
            '''sol_q = solve_ivp(diff_q, t_span, y0, method='BDF')
            t = sol_q.t
            E_m = 0.5*L*(sol_q.y[1]**2)
            E_e = 0.5*(sol_q.y[0]**2)/C
            E_t = E_m + E_e
            '''
            q_t = np.linspace(t_span[0],t_span[1],400)
            diff_qsol = DIFF_SOLVE(L,R,1/C,C*E,False)
            sol_q = np.array([diff_qsol(t) for t in q_t])
            diff_isol = DIFF_SOLVE(L,R,1/C,C*E,True)
            sol_i = np.array([diff_isol(t) for t in q_t])
            t = q_t
            E_m = 0.5*L*((sol_i/2)**2)
            E_e = 0.5*(sol_q**2)/C
            E_t = E_m + E_e
        plt.figure()
        plt.plot(t,E_m,color='red', label='Energie Magnétique')
        plt.plot(t,E_e,color='black', label='Energie Electrostatique')
        plt.plot(t,E_t,color='blue', label='Energie Totale')
        plt.grid()
        plt.legend()

        plt.title("Evolution Temporelle des Energies")
        plt.gcf().canvas.manager.set_window_title(f'Enegie pour R = {R}, C = {C}, L = {L} et E = {E}')
        XY_Units('s','J','Temps','Energie')

        plt.show()

    #Buttons
    BTN_plot_q          = ctk.CTkButton(app, text="Tracer la charge", command=plot_q)
    BTN_plot_q.grid(row=5,column=3,pady=PADY_CONST,padx=PADX_CONST)#.place(relx=0.25,rely=0.95,anchor=CENTER)
    BTN_plot_i          = ctk.CTkButton(app, text="Tracer l'intensité", command=plot_i)
    BTN_plot_i.grid(row=5,column=4,pady=PADY_CONST,padx=PADX_CONST)
    BTN_plot_e          = ctk.CTkButton(app, text="Tracer l'énergie", command=plot_e)
    BTN_plot_e.grid(row=5,column=5,pady=PADY_CONST,padx=PADX_CONST)

    #GUM LOGIC
    def gumCall():
        global guide
        if guide is None:
            guide = gum.createGuideWindow(app, "Guide: Circuit RLC Libre","rlcl.txt")
        else:
            guide.destroy()
            guide = gum.createGuideWindow(app, "Guide: Circuit RLC Libre","rlcl.txt")

    gumButton = ctk.CTkButton(app,text="Guide",width=50,height=20,command=gumCall,image=ctk.CTkImage(dark_image=Image.open("./res/guide.png"),size=(30, 30)))
    gumButton.place(relx=0.2,rely=0.85,anchor='center')

    app.mainloop()

def MAIN_RLC_FORCE(mainy):
    global guide
    guide = None

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTkToplevel(mainy)
    app.geometry("800x475")
    app.resizable(False,False)
    app.title("Circuit RLC Forcé")
    

    def RLCTools(choice):
        if choice == "RLC Libre":
            app.destroy()
            MAIN_RLC_LIBRE(mainy)
        if choice == "RC":
            app.destroy()
            MAIN_RC(mainy)
        else:
            return 0

    RLCBox = ctk.CTkOptionMenu( master=app,
                                values=["RLC Forcé","RC", "RLC Libre"],
                                command=RLCTools,
                                width=200, height=30)
    RLCBox.place(relx=0.5,rely=0.95,anchor=CENTER)

    #R = 5
    L = 1e-8
    C = 0.5e-10
    resN = 1/np.sqrt(L*C)
    f = 2e8
    w = 2 * np.pi * f

    I0 = 110
    E = 1200
    t0 = 0.0
    tf = 2e-8
    t_span = (t0,tf)

    entryWidth = 150
    PADY_CONST = 2
    fontName = "Arial"
    fontSize = 16

    
    ctk.CTkLabel(app, text="Paramétres de circuit", font=(fontName,fontSize)).grid(row=0,column=0,columnspan=3,pady=PADY_CONST)
    ctk.CTkLabel(app, text="Capacité C", font=(fontName,fontSize)).grid(row=1,column=0,pady=PADY_CONST)
    entryCapacitance    = ctk.CTkEntry(app, width=entryWidth,corner_radius=10)
    entryCapacitance.grid(row=1,column=1,pady=PADY_CONST)
    entryCapacitance.insert(0,'1e-2')
    ctk.CTkLabel(app, text="F", font=(fontName,fontSize)).grid(row=1,column=2,pady=PADY_CONST)
    
    ctk.CTkLabel(app, text="Charge Initiale Q0", font=(fontName,fontSize)).grid(row=2,column=0,pady=PADY_CONST)
    entryQ0             = ctk.CTkEntry(app, width=entryWidth,corner_radius=10)
    entryQ0.grid(row=2,column=1,pady=PADY_CONST)
    entryQ0.insert(0,'0')
    ctk.CTkLabel(app, text="C", font=(fontName,fontSize)).grid(row=2,column=2,pady=PADY_CONST)
    
    ctk.CTkLabel(app, text="Résistance R", font=(fontName,fontSize)).grid(row=3,column=0,pady=PADY_CONST)
    entryResistance     = ctk.CTkEntry(app, width=entryWidth,corner_radius=10)
    entryResistance.grid(row=3,column=1,pady=PADY_CONST)
    entryResistance.insert(0,'5e-2')
    ctk.CTkLabel(app, text="Ω", font=(fontName,fontSize)).grid(row=3,column=2,pady=PADY_CONST)
    
    ctk.CTkLabel(app, text="Inductance L", font=(fontName,fontSize)).grid(row=4,column=0,pady=PADY_CONST)
    entryInductance     = ctk.CTkEntry(app, width=entryWidth,corner_radius=10)
    entryInductance.grid(row=4,column=1,pady=PADY_CONST)
    entryInductance.insert(0,'1e-2')
    ctk.CTkLabel(app, text="H", font=(fontName,fontSize)).grid(row=4,column=2,pady=PADY_CONST)
    
    ctk.CTkLabel(app, text="Résistance r", font=(fontName,fontSize)).grid(row=5,column=0,pady=PADY_CONST)
    entryInductRes      = ctk.CTkEntry(app, width=entryWidth,corner_radius=10)
    entryInductRes.grid(row=5,column=1,pady=PADY_CONST)
    entryInductRes.insert(0,'1e-3')
    ctk.CTkLabel(app, text="Ω", font=(fontName,fontSize)).grid(row=5,column=2,pady=PADY_CONST)
    
    ctk.CTkLabel(app, text="Paramétres de GBF:", font=(fontName,fontSize)).grid(row=6,column=0, columnspan=3,pady=PADY_CONST)
    
    ctk.CTkLabel(app, text="Tension Maximale Um", font=(fontName,fontSize)).grid(row=7,column=0,pady=PADY_CONST)
    entryUm             = ctk.CTkEntry(app, width=entryWidth,corner_radius=10)
    entryUm.grid(row=7,column=1,pady=PADY_CONST)
    entryUm.insert(0,'5')
    ctk.CTkLabel(app, text="V", font=(fontName,fontSize)).grid(row=7,column=2,pady=PADY_CONST)
    
    ctk.CTkLabel(app, text="Fréquence N", font=(fontName,fontSize)).grid(row=8,column=0,pady=PADY_CONST)
    entryN              = ctk.CTkEntry(app, width=entryWidth,corner_radius=10)
    entryN.grid(row=8,column=1,pady=PADY_CONST)
    entryN.insert(0,'10')
    ctk.CTkLabel(app, text="Hz", font=(fontName,fontSize)).grid(row=8,column=2,pady=PADY_CONST)

    '''ctk.CTkLabel(app, text="Pour les amplitudes et les phases:", font=(fontName,fontSize)).grid(row=9,column=0, columnspan=3,pady=PADY_CONST)
    
    ctk.CTkLabel(app, text="Fréquence minimale", font=(fontName,fontSize)).grid(row=10,column=0,pady=PADY_CONST)
    entryNm             = ctk.CTkEntry(app, width=entryWidth,corner_radius=10)
    entryNm.grid(row=10,column=1,pady=PADY_CONST)
    entryNm.insert(0,'20')
    ctk.CTkLabel(app, text="Hz", font=(fontName,fontSize)).grid(row=10,column=2,pady=PADY_CONST)
    
    ctk.CTkLabel(app, text="Fréquence maximale", font=(fontName,fontSize)).grid(row=11,column=0,pady=PADY_CONST)
    entryNn             = ctk.CTkEntry(app, width=entryWidth,corner_radius=10)
    entryNn.grid(row=11,column=1,pady=PADY_CONST)
    entryNn.insert(0,'40')
    ctk.CTkLabel(app, text="Hz", font=(fontName,fontSize)).grid(row=11,column=2,pady=PADY_CONST)'''

    '''#Dessiner le circuit
    generateurImg = ImageTk.PhotoImage(Image.open("./res/generateur.png").resize((128, 128), Image.Resampling.LANCZOS))
    condensateurImg = ImageTk.PhotoImage(Image.open("./res/condensateur.png").resize((128, 128), Image.Resampling.LANCZOS))
    resistorImg = ImageTk.PhotoImage(Image.open("./res/resistor.png").resize((128, 128), Image.Resampling.LANCZOS))
    #800x600
    canvas.create_image(400,100,anchor='center',image=generateurImg)'''

    coff = 2
    rlcfImg = ImageTk.PhotoImage(Image.open("./res/rlcf.png").resize((int(192*coff), int(128*coff)), Image.Resampling.LANCZOS))
    #ctk.CTkImage(light_image=rlcfImg, dark_image=rlcfImg,size=(30,30))
    #ctk.CTkButton(app,image=rlcfImg)
    canvas = Canvas(app,bg='#1A1A1A')
    canvas.grid(row=1,column=5,columnspan=5,rowspan=7,pady=PADY_CONST)
    canvas.create_image(195,135,anchor='center',image=rlcfImg)
    

    spacingThing = 10
    #ctk.CTkLabel(app, text=" "*spacingThing).grid(row=0,column=6)
    #ctk.CTkLabel(app, text=" "*spacingThing).grid(row=0,column=4)


    def unpack_values():
        try:
            R = float(entryResistance.get())
            r = float(entryInductRes.get())
            C = float(entryCapacitance.get())
            L = float(entryInductance.get())
            f = float(entryN.get())
            Q0 = float(entryQ0.get())
            Um = float(entryUm.get())
            assert ((R+r)>=0) and (C>0)and(L>0)and(Um>0)and(f>0)
        except:
            print("Merci d'entrer des valuers valides et positives")
            print("Utilisant les valeurs par défaut...")
            return [0.1,0,5e-2,1e-2,1e-3,5,10]
        return [C, Q0, R, L, r, Um, f]
    #C, Q0, R, L, r, Um, f = unpack_values()

    def U_GBF(U_max,frequence,t,phi):
        return U_max * np.sin(2*np.pi*frequence*t+phi)

    def diff_q(t,y):
        C, Q0, R, L, r, Um, f = unpack_values()

        dy0 = y[1]
        dy1 = (1/L)*(U_GBF(Um,f,t) - (R+r)*y[1]-y[0]/C)
        return [dy0,dy1]

    hFD = 1e-5
    def diff_i(t,y):
        C, Q0, R, L, r, Um, f = unpack_values()

        dy0 = y[1]
        dy1 = (1/L)*((U_GBF(Um,f,t+hFD)-U_GBF(Um,f,t))/hFD - (R+r)*y[1]-y[0]/C)
        return [dy0,dy1]

    def plot_i():
        C, Q0, R, L, r, Um, f = unpack_values()
        t_span = (0,10/f)
        y0 = [Q0,0.0]
        
        TIME = np.linspace(t_span[0],t_span[1],400)
        solI = np.real(LAPLACE_SOLVE(L,R,1/C,y0[0],Um,2*np.pi*f,0,1)(TIME))

        plt.figure()
        plt.gcf().canvas.manager.set_window_title("Intensité au Circuit")
        plt.title(f'Intensité pour C={C}, Q0={Q0}, R={R}, L={L}, r={r}, Um={Um}, f={f}')
        plt.plot(TIME,solI,color='red')
        XY_Units('s','A','Temps','Intensité')
        plt.grid()
        plt.show()

    def plot_q():
        C, Q0, R, L, r, Um, f = unpack_values()
        t_span = (0,10/f)
        y0 = [Q0,0.0]

        TIME = np.linspace(t_span[0],t_span[1],400)
        solQ = np.real(LAPLACE_SOLVE(L,R,1/C,y0[0],Um,2*np.pi*f,0)(TIME))

        plt.figure()
        plt.gcf().canvas.manager.set_window_title("Charge au Condensateur")
        plt.title(f'Charge pour C={C}, Q0={Q0}, R={R}, L={L}, r={r}, Um={Um}, f={f}')
        plt.plot(TIME,solQ,color='purple',label='Charge')
        XY_Units('s','C','Temps','Charge')
        plt.grid()
        plt.show()

    def plot_uc():
        C, Q0, R, L, r, Um, f = unpack_values()
        t_span = (0,10/f)
        y0 = [Q0,0.0]

        TIME = np.linspace(t_span[0],t_span[1],400)
        solQ = np.real(LAPLACE_SOLVE(L,R,1/C,y0[0],Um,2*np.pi*f,0)(TIME))
        
        plt.figure()
        plt.gcf().canvas.manager.set_window_title("Tension au Condensateur")
        plt.title(f'Tension pour C={C}, Q0={Q0}, R={R}, L={L}, r={r}, Um={Um}, f={f}')
        plt.plot(TIME,solQ/C,color='purple',label='Tension')
        plt.plot(TIME,Um*np.sin(2*np.pi*f*TIME),color='green',label='Tension du Générateur')
        XY_Units('s','V','Temps','Tension')
        plt.legend()
        plt.grid()
        plt.show()

    def plot_phi():
        C, Q0, R, L, r, Um, f = unpack_values()
        resN=1/np.sqrt(L*C)
        
        #DEPHASAGE
        size = 500
        aph = 2
        #frequencies = np.linspace(float(entryNn.get()), float(entryNm.get()), size)
        frequencies = np.linspace(resN/aph, aph*resN, size)
        phases = [np.arctan((1/(C*f) - L*f)/(R+r)) for f in frequencies]
        phases10 = [np.arctan((1/(C*f) - L*f)/((R+r)*10)) for f in frequencies]

        plt.figure()
        plt.plot(frequencies, phases, label=r'$\varphi$ (rad), $\Sigma$R = ' + str(round(R+r,2)) + r'$\Omega$')
        plt.plot(frequencies, phases10, label=r'$\varphi$ (rad), 10*$\Sigma$R = ' + str(round((R+r)*10,2)) + r'$\Omega$')

        plt.vlines(x=resN,ymin=min(phases),ymax=max(phases),color='red',linestyle='--',label="")

        plt.title("Dephasage vs Frequence")
        plt.gcf().canvas.manager.set_window_title("Dephasage vs Frequence")
        XY_Units('Hz','rad','Frequence','Dephasage')

        plt.legend()
        plt.grid()
        plt.show()   

    def plot_im():
        C, Q0, R, L, r, Um, f = unpack_values()
        resN=1/np.sqrt(L*C)

        #AMPLITUDE
        size = 500
        aph = 2
        #frequencies = np.linspace(float(entryNn.get()), float(entryNm.get()), size)
        frequencies = np.linspace(resN/aph, aph*resN, size)
        amplitudes = [E/np.sqrt((R+r)**2 + (L*f - 1/(C*f))**2) for f in frequencies]
        amplitudes10 = [E/np.sqrt(((R+r)*10)**2 + (L*f - 1/(C*f))**2) for f in frequencies]

        plt.figure()
        plt.plot(frequencies, amplitudes, label="Amplitude, $\Sigma$R = " + str(round(R+r,2)) + r'$\Omega$')
        plt.plot(frequencies, amplitudes10, label="Amplitude, 10*$\Sigma$R = " + str(round((R+r)*10,2)) + r'$\Omega$')
        plt.ylim(min(amplitudes),max(amplitudes))
        plt.vlines(x=resN,ymin=0,ymax=max(amplitudes),color='red',linestyle='--',label="")

        plt.title("Amplitude vs Frequence")
        plt.gcf().canvas.manager.set_window_title("Amplitude vs Frequence")
        XY_Units('Hz','A','Frequence',r'Amplitude $I_m$')

        plt.legend()
        plt.grid()
        plt.show()

    
    btn_i   = ctk.CTkButton(app,text="Tracer l'intensité", font=(fontName,fontSize),command=plot_i)
    btn_i.grid(row=10,column=5)
    btn_q   = ctk.CTkButton(app,text="Tracer la charge", font=(fontName,fontSize),command=plot_q)
    btn_q.grid(row=10,column=7)
    btn_uc  = ctk.CTkButton(app,text="Tracer la tension", font=(fontName,fontSize),command=plot_uc)
    btn_uc.grid(row=10,column=6)
    btn_im  = ctk.CTkButton(app,text="Tracer les amplitudes", font=(fontName,fontSize),command=plot_im)
    btn_im.grid(row=11,column=5)
    btn_phi = ctk.CTkButton(app,text="Tracer les déphasages", font=(fontName,fontSize),command=plot_phi)
    btn_phi.grid(row=11,column=7)


    #GUM LOGIC
    def gumCall():
        global guide
        if guide is None:
            guide = gum.createGuideWindow(app, "Guide: Circuit RLC Forcé","rlcf.txt")
        else:
            guide.destroy()
            guide = gum.createGuideWindow(app, "Guide: Circuit RLC Forcé","rlcf.txt")

    gumButton = ctk.CTkButton(app,text="Guide",width=70,height=40,command=gumCall,image=ctk.CTkImage(dark_image=Image.open("./res/guide.png"),size=(40, 40)))
    gumButton.place(relx=0.2,rely=0.775,anchor='center')


    app.mainloop()


def MAIN_RC(mainy):
    global guide
    guide = None

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTkToplevel(mainy)
    app.geometry("700x500")
    app.resizable(False,False)
    app.title("RC Condensateur")

    canvas = Canvas(app,width=800,height=600,bg="#1A1A1A",relief="ridge")
    canvas.pack()

    #Paramétres de simulation
    resistance = 100 #Ohm

    capacitance = 1e-6 #F
    tau = resistance * capacitance #Constant du temps

    tensionCircuit = 12 #V
    vTau = tensionCircuit*(1-np.exp(-1))

    #Dessiner le circuit
    generateurImg = ImageTk.PhotoImage(Image.open("./res/generateur.png").resize((128, 128), Image.Resampling.LANCZOS))
    condensateurImg = ImageTk.PhotoImage(Image.open("./res/condensateur.png").resize((128, 128), Image.Resampling.LANCZOS))
    resistorImg = ImageTk.PhotoImage(Image.open("./res/resistor.png").resize((128, 128), Image.Resampling.LANCZOS))
    #800x600
    canvas.create_image(400,100,anchor='center',image=generateurImg)
    canvas.create_image(200,400,anchor='center',image=condensateurImg)
    canvas.create_image(600,400,anchor='center',image=resistorImg)
    canvas.create_line(250, 400, 550, 400, fill='white', width=6)
    canvas.create_line(135, 403, 135, 97, fill='white', width=6)
    canvas.create_line(665, 403, 665, 97, fill='white', width=6)
    canvas.create_line(665, 100, 460, 100, fill='white', width=6)
    canvas.create_line(135, 100, 340, 100, fill='white', width=6)

    #Boite texte pour les paramétres
    EMF = ctk.CTkEntry(app, font=("Arial", 25), width = 75,height=5)#,state="normal",wrap=None)
    EMF.place(relx=0.5, rely=0.3, anchor='center')
    ctk.CTkLabel(app, text="V", font=("Arial", 25)).place(relx=0.575, rely=0.3, anchor='center')
    ctk.CTkLabel(app, text="Génerateur", font=("Arial", 28)).place(relx=0.5125, rely=0.2125, anchor='center')
    EMF.insert(0,"12")

    C = ctk.CTkEntry(app, font=("Arial", 25), width = 75,height=5)
    C.place(relx=0.25, rely=67/120, anchor='center')
    ctk.CTkLabel(app, text="F", font=("Arial", 25)).place(relx=0.32, rely=0.56, anchor='center')
    ctk.CTkLabel(app, text="Condensateur", font=("Arial", 28)).place(relx=0.3125, rely=0.8, anchor='center')
    C.insert(0,"1e-6")

    R = ctk.CTkEntry(app, font=("Arial", 25), width = 75,height=5)
    R.place(relx=0.71875, rely=67/120, anchor='center')
    ctk.CTkLabel(app, text="Ω", font=("Arial", 25)).place(relx=0.7875, rely=0.56, anchor='center')
    ctk.CTkLabel(app, text="Résistor", font=("Arial", 28)).place(relx=0.7125, rely=0.8, anchor='center')
    R.insert(0,"100")


    def RLCTools(choice):
        if choice == "RLC Forcé":
            app.destroy()
            MAIN_RLC_FORCE(mainy)
        if choice == "RLC Libre":
            app.destroy()
            MAIN_RLC_LIBRE(mainy)
        else:
            return 0

    def simuler(traceCharge,uPlot=True):
        global execution, Vc, Ic, tensionCircuit, vTau, resistance, capacitance, tau
        if not uPlot:
            vTau = (tensionCircuit/resistance)*np.exp(-1)
        t = 0
        tensions = []
        taus = []
        temps = []
        tempsMax = 6 * tau
        dt = tau/100
        Vc = 0
        Ic = 0
        
        #Graph
        fig, axes = plt.subplots()
        VorA = 'V' if uPlot else 'A'
        TorI = 'Tension' if uPlot else "Intensité"
        plt.title(TorI+' aux Bornes du Condensateur')
        plt.gcf().canvas.manager.set_window_title(TorI+' aux Bornes du Condensateur')
        
        #axes.set_xlabel('Temps (s)')
        #axes.set_ylabel('Tension (V)')
        XY_Units('s',VorA,'Temps',TorI,axes)
        axes.set_xlim(0,tempsMax)
        axes.tick_params(axis='x', rotation=15)
        #axes.set_facecolor((0.65, 0.65, 0.65))
        #fig.set_facecolor((0.78, 0.78, 0.78))
        
        print("="*11,"PARAMETRES",11*"=")
        print("Tension du générateur:"+" "*3,tensionCircuit,"V")
        print("Resistance:"+" "*14,resistance,"Ohm")
        print("Capacité du condensateur:",capacitance,"F\n")
        
        
        while t < tempsMax and execution:
            Ic = (tensionCircuit - Vc) / resistance
            Vc +=  Ic * dt / capacitance
            
            tensions.append(Vc if uPlot else Ic)
            temps.append(t)
            
            t += dt

        plt.grid()
        if not traceCharge:
            unitTau0=''
            #Tableau
            #EngFormatter()(vTau).split('.')
            #taus = [(str(i)+r'$\tau$',str(EngFormatter()(tensionCircuit*(1-np.exp(-i))).split('.')[0]+'.'+EngFormatter()(tensionCircuit*(1-np.exp(-i))).split('.')[1][:2]+EngFormatter()(tensionCircuit*(1-np.exp(-i)))[-1]+"V")) for i in range(1,6)]
            taus=[]
            for i in range(1,6):
                if uPlot:
                    engFormatted = EngFormatter()(tensionCircuit*(1-np.exp(-i)))
                else:
                    engFormatted = EngFormatter()((tensionCircuit/resistance)*np.exp(-i))
                engSplit = engFormatted.split('.')
                unitTau0+=engSplit[1][:2]+engFormatted[-1]
                taus.append((str(i)+r'$\tau$',engSplit[0]+'.'+engSplit[1][:2]+engFormatted[-1]+VorA))
            
            plt.subplots_adjust(left=0.1,right=0.7,bottom=0.133,top=0.95)
            table = axes.table(cellText=taus, colWidths=[0.175,0.275], colLabels=['Temps',TorI], colLoc='center', rowLoc='center', loc='right')
            table.auto_set_font_size(False)
            table.set_fontsize(14)
            table.scale(1,2)

            maxy = tensionCircuit if uPlot else tensionCircuit/resistance
            axes.set_ylim(0, maxy)
            axes.plot(temps, tensions)
            fig.canvas.draw()
            
            plt.vlines(x = tempsMax - tau, ymin = 0,
                       ymax = maxy, colors = "green",
                       linestyles="dashed")
            axes.text(5/6,
                           2/tensionCircuit,
                           'Condensateur chargé 99.3%',
                           bbox={'facecolor': 'green', 'alpha': 0.75, 'pad': 2},
                           horizontalalignment='left',
                           rotation = 90,
                           #color = "red",
                           fontsize = 15,
                           transform=axes.transAxes)
            
            plt.vlines(x = tau, ymin = 0,
                       ymax = vTau, colors = "red",
                       linestyles="dashed")
            axes.text(1/6,-0.05,r'$\tau$',
                           bbox={'facecolor': 'red', 'alpha': 0.75, 'pad': 2},
                           horizontalalignment='center',
                           #color = "red",
                           fontsize = 15,
                           transform=axes.transAxes)
            
            plt.hlines(y = vTau, xmin= 0,
                       xmax = tau, colors = "red",
                       linestyles="dashed")
            vTauSplit = EngFormatter()(vTau).split('.')
            axes.text(-0.05,
                           vTau/maxy,
                           vTauSplit[0]+'.'+vTauSplit[1][:2]+unitTau0[2]+VorA,
                           bbox={'facecolor': 'red', 'alpha': 0.75, 'pad': 2},
                           horizontalalignment='center',
                           verticalalignment='center',
                           #color = "red",
                           fontsize = 12,
                           transform=axes.transAxes)
        
            figTitre = TorI+' pour ' + str(tensionCircuit) + 'V '+ str(resistance) +'Ohm '+ str(capacitance)+ 'F'
            plt.savefig(figTitre + '.png')
            plt.show()
        else:
            #plt.figure()
            plt.title('Charge au Condensateur')
            plt.gcf().canvas.manager.set_window_title('Charge aux Bornes du Condensateur')
            XY_Units('s','C','Temps','Charge',axes)
            tc = tensionCircuit*capacitance
            plt.hlines(y = tc, xmin= 0,
                       xmax = temps[-1], colors = "red",
                       linestyles="dashed")
            axes.text(-0.05,0.95,
                           EngFormatter()(tensionCircuit*capacitance)+"C",
                           bbox={'facecolor': 'red', 'alpha': 0.75, 'pad': 2},
                           horizontalalignment='center',
                           verticalalignment='center',
                           #color = "red",
                           fontsize = 12,
                           transform=axes.transAxes)
            axes.set_ylim(0, tc*21/20)
            axes.plot(temps,[tension*capacitance for tension in tensions])
            plt.show()
        
        
        #Also draw table showing voltages at 1 tau, 2, 3, 4 and 5


    def commence(traceCharge,uPlot=True):
        global execution, tensionCircuit, vTau, resistance, capacitance, tau
        execution = True
        try:
            tensionCircuit = float(EMF.get())
            assert tensionCircuit >= 0
            vTau = tensionCircuit*(1-np.exp(-1))
        except:
            EMF.delete(0,"end")
            EMF.insert(0,"???")
            execution = False
        
        try:
            capacitance = float(C.get())
            assert capacitance >= 0
        except:
            C.delete(0,"end")
            C.insert(0,"???")
            execution = False
        
        try:
            resistance = float(R.get())
            assert resistance >= 0
        except:
            R.delete(0,"end")
            R.insert(0,"???")
            execution = False
        
        tau = capacitance * resistance
        
        if execution:
            simuler(traceCharge,uPlot)
        
        
    uBtn = ctk.CTkButton(app, text='Tracer la tension', command=lambda: commence(False))
    uBtn.place(relx=0.5,rely=0.5,anchor=CENTER)
    iBtn = ctk.CTkButton(app, text="Tracer l'intensité", command=lambda: commence(False,False))
    iBtn.place(relx=0.5,rely=0.575,anchor=CENTER)
    qBtn = ctk.CTkButton(app, text='Tracer la charge', command=lambda: commence(True))
    qBtn.place(relx=0.5,rely=0.425,anchor=CENTER)

    execution = False

    RLCBox = ctk.CTkOptionMenu( master=app,
                                values=["RC","RLC Forcé", "RLC Libre"],
                                command=RLCTools,
                                width=200, height=30)
    RLCBox.place(relx=0.5,rely=0.95,anchor=CENTER)

    def updateGraphics():
        width = app.winfo_width()
        height = app.winfo_height()
        canvas.place(rely=0.5,relx=0.5,anchor=CENTER)
        
        app.after(int(1e3/3), updateGraphics)

    #GUM LOGIC
    def gumCall():
        global guide
        if guide is None:
            guide = gum.createGuideWindow(app, "Guide: Circuit RC","rc00.txt")
        else:
            guide.destroy()
            guide = gum.createGuideWindow(app, "Guide: Circuit RC","rc00.txt")

    gumButton = ctk.CTkButton(app,text="Guide",width=50,height=20,command=gumCall,image=ctk.CTkImage(dark_image=Image.open("./res/guide.png"),size=(30, 30)))
    gumButton.place(relx=0.95,rely=0.9,anchor=E)

    app.after(int(1e3/2), updateGraphics)
    app.mainloop()



if __name__ == '__main__':
    mainy = ctk.CTk()
    MAIN_RLC_FORCE(mainy)
