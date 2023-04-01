import tkinter as tk
import customtkinter as ctk
from PIL import Image,ImageTk
import numpy as np
import guideManager as gum

bodies = []
didReset = False
canPlace = True
guide = None

#1 period = 1 seconde
orbPerCoff = 86400
orbDisCoff = 175
            #Planet   #AU               #AU             #Jours
planets = {'Mercury':(0.38*orbDisCoff,0.47*orbDisCoff, 88*orbPerCoff, np.pi),
           'Venus'  :(0.72*orbDisCoff,0.73*orbDisCoff,225*orbPerCoff,0),
           'Earth'  :(1.00*orbDisCoff,1.02*orbDisCoff,365*orbPerCoff,4*np.pi/3),
           'Mars'   :(1.52*orbDisCoff,1.67*orbDisCoff,687*orbPerCoff,np.pi/3),}
planetsData = [planets[i] for i in planets.keys()]

globals().update({'earthGarbage' : {}})

speedLabels = ["1 sec = 1 sec","1 sec = 1 heure", "1 sec = 1 jour", "1 sec = 1 mois", "1 sec = 1 an"]
speedCoffs  = [1              ,3600             ,86400            ,2592000          ,31536000]
speed = 1

def MAIN_GRAV(mainy):
    global bodies, didReset, speed, guide

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")


    app = ctk.CTkToplevel(mainy)
    w0 = 800
    h0 = 600
    app.geometry(str(w0)+"x"+str(h0)+'+50+50')
    app.title("Gravitation")

    canvas = tk.Canvas(app, width=w0, height=h0,bg="#1A1A1A",relief="ridge")
    canvas.pack()

    #Images de soleil, lune eet terre
    SOL_IMG = ImageTk.PhotoImage(Image.open("./res/soleil.png").resize((128, 128), Image.Resampling.LANCZOS))
    LUN_IMG = ImageTk.PhotoImage(Image.open("./res/lucyna.png").resize((64, 64), Image.Resampling.LANCZOS))
    TER_R = 56
    TER_RAW = Image.open("./res/terre.png").resize((TER_R*2, TER_R*2), Image.Resampling.LANCZOS)
    TER_IMG = ImageTk.PhotoImage(TER_RAW)

    cpc = ctk.CTkLabel(app, text='Cliquez pour créer', font=("Arial", 20))
    
    massLabel = ctk.CTkLabel(app, text = 'Masse: ', font=("Arial", 20))
    massText = ctk.CTkEntry(app, width = 65,height=5)
    massText.insert(0,"1")
    
    vxLabel = ctk.CTkLabel(app, text=u'Vx\u2080' ,font=("Arial", 20))
    vxText = ctk.CTkEntry(app, width = 65,height=5)
    vxText.insert(0,"0")

    vyLabel = ctk.CTkLabel(app, text =u'Vy\u2080', font=("Arial", 20))
    vyText = ctk.CTkEntry(app, width = 65,height=5)
    vyText.insert(0,"0")
    
    
    cpc.place(relx=0.025, rely=0.8,anchor=tk.W)
    massLabel.place(relx=0.025, rely=0.85,anchor=tk.W)
    massText.place(relx=0.15, rely=0.85,anchor=tk.CENTER)
    vxLabel.place(relx=0.025, rely=0.9,anchor=tk.W)
    vxText.place(relx=0.15, rely=0.9,anchor=tk.CENTER)
    vyLabel.place(relx=0.025, rely=0.95,anchor=tk.W)
    vyText.place(relx=0.15, rely=0.95,anchor=tk.CENTER)


    #Objet caracterisé par sa position, mass et vitesse
    class Body:
        def __init__(self, x, y, mass, radius, velocity_x, velocity_y, canvas, colour="white", img=None):
            self.x = x
            self.y = y
            self.mass = mass

            self.radius = radius
            self.isBounded = False
            
            self.velocity_x = velocity_x
            self.velocity_y = velocity_y

            self.force_x = 0
            self.force_y = 0
            
            self.canvas = canvas
            self.img = img

            #Un disque ou une image pour representer ce corps
            if img == None:
                self.shape = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=colour)
            else:
                self.shape = canvas.create_image(x, y, image=self.img)

        def update_position(self, width, height,dt):
            #Il n'est pas necessaire de changer la position d'un corps hors de l'espace
            if self.isBounded:
                return 0
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt

            if 0 > self.x or self.x > width:
                self.x = -1
                self.mass = 0
                self.isBounded = True
                canvas.delete(self.shape)
                return 0
            if 0 > self.y or self.y > height:
                self.y = -1
                self.mass = 0
                self.isBounded = True
                canvas.delete(self.shape)
                return 0


            # F = ma -> a = F/m -> dv/dt = F/m
            self.velocity_x += self.force_x / self.mass * dt
            self.velocity_y += self.force_y / self.mass * dt

            self.force_x = 0
            self.force_y = 0

            # Changer la position
            if self.img == None:
                self.canvas.coords(self.shape, self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius)
            else:
                self.canvas.coords(self.shape,self.x,self.y)

    bodies = [
        #Body(500, 100, 100, 10, 0, 0, canvas),
        #Body(200, 100, 20, 2, 0, 0, canvas),
        #Body(300, 300, 30, 3, 0, 0, canvas)
    ]


    def gravitational_force(body1, body2):
        # Calcule de distance entre b1 et b2
        dx = body2.x - body1.x
        dy = body2.y - body1.y
        r = np.sqrt(dx**2 + dy**2)

        # Calculer la force gravitationnelle
        try:
            force = body1.mass * body2.mass / r**2 #G est 1 ici
        except ZeroDivisionError:
            force = 0

        if r <= body1.radius+body2.radius:
            force=0#force = -body1.mass * body2.mass / r**2
        
        # Calculer les composantes de la force
        force_x = force * dx / r
        force_y = force * dy / r

        return force_x, force_y

    def update_forces(width, height):
        global bodies
        # Ce 'decalage' de i+1 de i sert a un solution optimale pour le calcul entre tous les corps
        for i in range(len(bodies)):
            #Supprimers le corps s'il était hors de le canvas
            try:
                if 0 > bodies[i].x or bodies[i].x > width:
                    bodies.pop(i)
                    break
                if 0 > bodies[i].y or bodies[i].y > height:
                    bodies.pop(i)
                    break
            except:
                break
            for j in range(i+1, len(bodies)):
                #Supprimers le corps s'il était hors de le canvas
                try:
                    if 0 > bodies[j].x or bodies[j].x > width:
                        bodies.pop(j)
                        break
                    if 0 > bodies[j].y or bodies[j].y > height:
                        bodies.pop(j)
                        break
                except:
                    break
                try:
                    force_x, force_y = gravitational_force(bodies[i], bodies[j])

                    # Appliquer la force
                    bodies[i].force_x += force_x
                    bodies[i].force_y += force_y
                    bodies[j].force_x -= force_x
                    bodies[j].force_y -= force_y

                    # Longuer?
                    lengthi = np.sqrt(bodies[i].force_x**2 + bodies[i].force_y**2)
                    lengthj = np.sqrt(bodies[j].force_x**2 + bodies[j].force_y**2)

                    # Dessiner ce vecter
                    li = canvas.create_line(bodies[i].x, bodies[i].y,
                                            bodies[j].x + bodies[j].force_x / lengthj, bodies[j].y + bodies[j].force_y / lengthj, fill="red", arrow=tk.LAST)
                    lj = canvas.create_line(bodies[j].x, bodies[j].y,
                                            bodies[i].x + bodies[i].force_x / lengthi, bodies[i].y + bodies[i].force_y / lengthi, fill="red", arrow=tk.LAST)

                    # Changer la longuer à un tier au lieu de lignes super longs
                    x1, y1, x2, y2 = canvas.coords(li)
                    canvas.coords(li,x1,y1,(2*x1+x2)/3,(2*y1+y2)/3)

                    x1, y1, x2, y2 = canvas.coords(lj)
                    canvas.coords(lj,x1,y1,(2*x1+x2)/3,(2*y1+y2)/3)
                except ZeroDivisionError:
                    li = canvas.create_line(0,0,0,0, fill="red", arrow=tk.LAST)
                    lj = canvas.create_line(0,0,0,0, fill="red", arrow=tk.LAST)                 
                    pass
                
                
                # Supprimer les lignes
                canvas.after(30,canvas.delete,li)
                canvas.after(30,canvas.delete,lj)

    class FakeBody:
        def __init__(self, min_distance,max_distance, period, angle0, main_object, radius,canvas, colour="white", img=None):
            self.x = 0
            self.y = 0
            self.radius=radius
            
            self.max_distance = max_distance
            self.min_distance = min_distance
            self.main_object = main_object
            self.eccentricity = (self.max_distance-self.min_distance)/(self.max_distance+self.min_distance)
            
            self.time = 0
            self.period = period
            self.angle0 = angle0
            self.angle = 0

            self.canvas = canvas
            self.img = img
            if img == None:
                self.shape = canvas.create_oval(self.x-radius, self.y-radius, self.x+radius, self.y+radius, fill=colour)
            else:
                self.shape = canvas.create_image(self.x, self.y, image=self.img)

        def update(self):
            self.time += 0.01*speed
            self.angle = (2 * np.pi / self.period) * self.time + self.angle0
            '''self.x = self.main_object.x + self.max_distance * np.cos(self.angle)
            self.y = self.main_object.y + self.min_distance * np.sin(self.angle)'''
            distance = self.min_distance * (1 - self.eccentricity**2) / (1 + self.eccentricity * np.cos(self.angle))
            self.x = self.main_object.x + distance * np.cos(self.angle)
            self.y = self.main_object.y + distance * np.sin(self.angle)
            if self.img == None:
                self.canvas.coords(self.shape, self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius)
            else:
                self.canvas.coords(self.shape,self.x,self.y)

    class MainObject:
        def __init__(self, x, y, canvas, colour="white", img=None, rawImage = False, rotRate=0):
            self.x = x
            self.y = y
            self.fake_bodies = []

            self.rawImage = rawImage
            self.rotRate = rotRate
            self.img = img
            if rawImage:
                self.time = 0
                self.counter = 0
            self.canvas=canvas
            radius = 35
            
            if img == None:
                self.shape = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=colour)
            else:
                if rawImage:
                    self.shape = canvas.create_image(x, y, image=ImageTk.PhotoImage(self.img))
                else:
                    self.shape = canvas.create_image(x, y, image=self.img)

        def add_fb(self, fake_body):
            self.fake_bodies.append(fake_body)

        def update(self):
            '''if self.rawImage:
                self.counter+=1
                if self.counter%3==0:
                    earthGarbage.clear()
                    del self.shape
                    #self.time += 0.01*speed
                    #self.img = 
                    earthGarbage.update({'rotE'+str(self.time):ImageTk.PhotoImage(self.img.rotate((2 * np.pi / (24*orbPerCoff)) * self.fake_bodies[-1].time))})
                    self.shape = canvas.create_image(self.x, self.y, image=earthGarbage[list(earthGarbage)[-1]])'''
            for fake_body in self.fake_bodies:
                fake_body.update()

    def changeSpeed(argument):
        global speed
        speed = speedCoffs[speedLabels.index(argument)]

    def update_positions(width, height,dt):
        global bodies
        for body in bodies:
            body.update_position(width, height,dt)


    def simuler(root, width, height, canvas, dt):
        global bodies
        update_forces(width, height)
        update_positions(width, height,dt)
        width = root.winfo_width()
        height = root.winfo_height()
        canvas.configure(width=width,height=height)
        canvas.after(10, simuler, root, width, height, canvas, dt)


    def clickDeal(clickEvent):
        global bodies
        massInput = int(massText.get())
        if canPlace:
            try:
                assert massInput > 0
                bodies.append(Body(clickEvent.x, clickEvent.y,
                                   massInput, 10,
                                   float(vxText.get()),
                                   float(vyText.get()), canvas))
            except:
                print("Merci d'entrer un nombre valide pour la masse ou la vitesse")
        #else:
        #    print("Merci de choisir une autre scène")



    #this function is from stackoverflow
    def poly_oval(x0,y0, x1,y1, steps=25, rotation=30):
        """return an oval as coordinates suitable for create_polygon"""

        # x0,y0,x1,y1 are as create_oval

        # rotation is in degrees anti-clockwise, convert to radians
        rotation = rotation * np.pi / 180.0

        # major and minor axes
        a = (x1 - x0) / 2.0
        b = (y1 - y0) / 2.0

        # center
        xc = x0 + a
        yc = y0 + b

        point_list = []

        # create the oval as a list of points
        for i in range(steps):

            # Calculate the angle for this step
            # 360 degrees == 2 pi radians
            theta = (np.pi * 2) * (float(i) / steps)

            x1 = a * np.cos(theta)
            y1 = b * np.sin(theta)

            # rotate x, y
            x = (x1 * np.cos(rotation)) + (y1 * np.sin(rotation))
            y = (y1 * np.cos(rotation)) - (x1 * np.sin(rotation))

            point_list.append(round(x + xc))
            point_list.append(round(y + yc))

        return point_list


    def updateMainy(sol):
        #sol.time += 0.01*speed
        global didReset
        if not didReset:
            return 0
        sol.update()
        tempEcouVa.configure(text=str(np.round(sol.fake_bodies[-1].time/86400 ,2))+' jour(s)')
        sol.canvas.after(10, lambda: updateMainy(sol))

    speedBox = ctk.CTkOptionMenu(app, values=speedLabels,command=changeSpeed)
    tempEcoule = ctk.CTkLabel(app, text="Temps écoulé: ")
    tempEcouVa = ctk.CTkLabel(app, text="0 jour(s)")

    reinitVide = ctk.CTkButton(master=app, text="Réinitialiser")
    
    def systemTemplate(template='Vide'):
        global bodies, didReset, speed, canPlace

        speedBox.place(relx=-0.5,rely=-0.05,anchor=tk.CENTER)
        tempEcoule.place(relx=-0.5,rely=-0.05,anchor=tk.CENTER)
        tempEcouVa.place(relx=-0.5,rely=-0.05,anchor=tk.CENTER)
        reinitVide.place(relx=-0.5,rely=-0.5,anchor=tk.CENTER)
        
        cpc.place(relx=0.025, rely=0.8,anchor=tk.W)
        massLabel.place(relx=0.025, rely=0.85,anchor=tk.W)
        massText.place(relx=0.15, rely=0.85,anchor=tk.CENTER)
        vxLabel.place(relx=0.025, rely=0.9,anchor=tk.W)
        vxText.place(relx=0.15, rely=0.9,anchor=tk.CENTER)
        vyLabel.place(relx=0.025, rely=0.95,anchor=tk.W)
        vyText.place(relx=0.15, rely=0.95,anchor=tk.CENTER)
        
        speedBox.set("1 sec = 1 sec")
        tempEcouVa.configure(text='0 jour(s)')
        speed=1
        didReset = True
        canPlace = True

        width = app.winfo_width()
        height = app.winfo_height()

        cX = width//2
        cY = height//2

        bodies = []
        canvas.delete("all")

        if template == "Vide":
            reinitVide.place(relx=0.95,rely=0.95,anchor=tk.E)
            return 0
        elif template == "Carré":
            a=40
            b=50
            p = 10
            m = 1e4
            bodies = [Body(300+a,200+b,m,10,0,p,canvas),
                      Body(400+a,200+b,m,10,-p,0,canvas),
                      Body(400+a,300+b,m,10,0,-p,canvas),
                      Body(300+a,300+b,m,10,p,0,canvas),
                      Body(200+a,100+b,m*4,10,0,p*2,canvas),
                      Body(500+a,100+b,m*4,10,-p*2,0,canvas),
                      Body(500+a,400+b,m*4,10,0,-p*2,canvas),
                      Body(200+a,400+b,m*4,10,p*2,0,canvas),
                      Body(100+a,0+b,m*8,10,0,p*4,canvas),
                      Body(600+a,0+b,m*8,10,-p*4,0,canvas),
                      Body(600+a,500+b,m*8,10,0,-p*4,canvas),
                      Body(100+a,500+b,m*8,10,p*4,0,canvas),]
            
        elif template == "Système Solaire":
            canPlace = False
            didReset = True

            cpc.place(relx=-1, rely=-1,anchor=tk.W)
            massLabel.place(relx=-1, rely=-1,anchor=tk.W)
            massText.place(relx=-1, rely=-1,anchor=tk.CENTER)
            vxLabel.place(relx=-1, rely=-1,anchor=tk.W)
            vxText.place(relx=-1, rely=-1,anchor=tk.CENTER)
            vyLabel.place(relx=-1, rely=-1,anchor=tk.W)
            vyText.place(relx=-1, rely=-1,anchor=tk.CENTER)
            
            sol = MainObject(cX,cY, canvas,"#FFFF46", img=SOL_IMG)
            radii = [2,6,6,3]
            colii = ["#545E7B","#B39E6C","#5435FF","#DA5D4A"]
            j=0
            for i in planetsData:
                e = (i[1]-i[0])/(i[1]+i[0])
                aef = i[0] * (1 - e**2)
                d0x = aef / (1 + e * np.cos(0))
                d1x = aef / (1 + e * np.cos(180))
                d0y = aef / (1 + e * np.cos(90))
                d1y = aef / (1 + e * np.cos(270))
                canvas.create_oval(cX-d1x-5, cY-d1y-5, cX+d0x, cY+d0y-5,outline='white',dash=(1,2),width=1)
                sol.add_fb(FakeBody(i[0],i[1],i[2],i[3],sol,radii[j]*2,canvas,colour=colii[j]))
                j+=1
            speedBox.place(relx=0.5,rely=0.05,anchor=tk.CENTER)
            tempEcoule.place(relx=0.05,rely=0.05,anchor=tk.W)
            tempEcouVa.place(relx=0.25,rely=0.05,anchor=tk.CENTER)
            updateMainy(sol)

        elif template == "Terre et Lune":
            canPlace = False
            didReset = False

            cpc.place(relx=-1, rely=-1,anchor=tk.W)
            massLabel.place(relx=-1, rely=-1,anchor=tk.W)
            massText.place(relx=-1, rely=-1,anchor=tk.CENTER)
            vxLabel.place(relx=-1, rely=-1,anchor=tk.W)
            vxText.place(relx=-1, rely=-1,anchor=tk.CENTER)
            vyLabel.place(relx=-1, rely=-1,anchor=tk.W)
            vyText.place(relx=-1, rely=-1,anchor=tk.CENTER)
            
            tides = canvas.create_polygon(poly_oval(cX-(TER_R+5),cY-TER_R,cX+(TER_R+5),cY+TER_R,rotation=0),fill="blue")    
            terre = MainObject(cX,cY, canvas,"#5435FF", img=TER_IMG)
            perLun = 360//2
            apoLun = 405//2
            e = (apoLun-perLun)/(apoLun+perLun)
            aef = perLun * (1 - e**2)
            d0x = aef / (1 + e * np.cos(0))
            d1x = aef / (1 + e * np.cos(180))
            d0y = aef / (1 + e * np.cos(90))
            d1y = aef / (1 + e * np.cos(270))
            canvas.create_oval(cX-d1x, cY-d1y-5, cX+d0x, cY+d0y,outline='white',dash=(1,2),width=1)
            moon = FakeBody(perLun,apoLun,27.32166*orbPerCoff,0,terre,10,canvas,colour="#545E7B",img=LUN_IMG)
            terre.add_fb(moon)
            speedBox.place(relx=0.5,rely=0.05,anchor=tk.CENTER)
            tempEcoule.place(relx=0.05,rely=0.05,anchor=tk.W)
            tempEcouVa.place(relx=0.25,rely=0.05,anchor=tk.CENTER)
            canvas.after(10, lambda: rot(tides, canvas, terre,moon))


    def rot(objec, canvas, terre, moon):
        global didReset
        if didReset:
            del moon
            del terre
            try:
                canvas.delete(tides)
            except:
                return 0
            return 0
        width = app.winfo_width()
        height = app.winfo_height()

        cX = terre.x
        cY = terre.y
        
        canvas.delete(objec)
        terre.update()
        tempEcouVa.configure(text=str(np.round(moon.time/86400 ,2))+' jour(s)')
        tides = canvas.create_polygon(poly_oval(cX-(TER_R+5),cY-TER_R,cX+(TER_R+5),cY+TER_R,rotation=-moon.angle*180/np.pi+5),fill="blue")
        canvas.tag_lower(tides)
        canvas.after(10, lambda: rot(tides, canvas, terre,moon))


    templatesBox = ctk.CTkOptionMenu(master=app,
                                     values=["Vide",
                                             "Système Solaire",
                                             "Carré",
                                             "Terre et Lune"],
                                     command=systemTemplate)
    templatesBox.configure(width=200, height=30)
    templatesBox.set("Vide")
    templatesBox.place(relx=0.5, rely=0.95,anchor=tk.CENTER)
    reinitVide.configure(command=systemTemplate)
    reinitVide.place(relx=0.95,rely=0.95,anchor=tk.E)

    
    #GUM LOGIC
    def gumCall():
        global guide
        if guide is None:
            guide = gum.createGuideWindow(app, "Guide: Gravitation","grav.txt")
        else:
            guide.destroy()
            guide = gum.createGuideWindow(app, "Guide: Gravitation","grav.txt")

    gumButton = ctk.CTkButton(app,text="Guide",width=50,height=20,command=gumCall,image=ctk.CTkImage(dark_image=Image.open("./res/guide.png"),size=(30, 30)))
    gumButton.place(relx=0.35,rely=0.95,anchor=tk.E)

    canvas.bind("<Button 1>",clickDeal)


    dt = 0.1 #was 0.1
    simuler(app, w0, h0, canvas, dt)
    return app
    app.mainloop()

if __name__ == '__main__':
    mainy = ctk.CTk()
    MAIN_GRAV(mainy)
