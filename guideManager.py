from tkinter import *
from PIL import Image,ImageTk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

mainGuidyPath = './res/guidy/'
widthGuidy = 500
heightGuidy = 600


def create_circle(x, y, r, canvas):
    return canvas.create_oval(x - r, y - r, x + r, y + r, width=1.75, outline="white")


globals().update({'garbageCollector' : {}})

def createGuideWindow(parent, title, text):
    textLi = [i[:-1] for i in open(mainGuidyPath+text,'r').readlines()]
    linesSpacing = 25
    hLi = (len(textLi)+2)*linesSpacing


    guide = ctk.CTkToplevel(parent)
    guide.geometry(f'{widthGuidy+20}x{min(heightGuidy,hLi+60)}+550+150')
    guide.resizable(False,False)
    guide.title(title)

    #parent.after(10, lambda: parent.wm_attributes("-topmost" , -1))
    
    scb = ctk.CTkScrollbar(guide)
    scb.grid(row=0, column=0, sticky='ns')

    cont = Canvas(guide, width=widthGuidy,
                         height=min(heightGuidy,hLi+60),
                         scrollregion=(0,0,0,hLi),
                  bg="#1A1A1A",relief="ridge")
    cont.grid(row=0,column=1,sticky='nsew')


    cont.configure(yscrollcommand=scb.set)
    scb.configure(command=cont.yview)
    
    
    i=0
    pady = 1
    padx = 1
    Cx = widthGuidy/2

    
    for line in textLi:
        attrLine = ''
        offset = len(line)
        if '_' in line:
            attrLine += 'underline'
            offset -= 1
        elif '-' in line:
            attrLine += 'italic'
            offset -= 1
        if '@' in line:
            linClr = line.split('£')
            offset = -len(line)+offset+len(linClr[0])
            if len(linClr)>1:
                cont.create_text(Cx,i*linesSpacing+15,
                                 text=linClr[0][1:offset],font=("Arial", 20,attrLine),
                                 fill=linClr[1].strip())#"white")
            else:
                cont.create_text(Cx,i*linesSpacing+15,
                                 text=linClr[0][1:offset],font=("Arial", 20,attrLine),
                                 fill="white")
        elif '¤' in line:
            jList = line.split(';')
            Cl = widthGuidy/(len(jList)+1)
            i+=1
            for l in range(len(jList)):
                img = Image.open(jList[l][1:])
                img = img.resize((int(float(img.size[0])*30/(img.size[1])),30), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                garbageCollector.update({'image'+str(i)+'-'+str(l): img})
                imgObj = cont.create_image(Cl*(l+1),(i-0.5)*linesSpacing+15,anchor='center',image=img)
        elif '$' in line:
            jList = line.split(';')
            Cl = widthGuidy/(len(jList)+1)
            i+=1
            for l in range(len(jList)):
                img = Image.open(jList[l][1:])
                img = img.resize((int(float(img.size[0])*50/(img.size[1])),50), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                garbageCollector.update({'image'+str(i)+'-'+str(l): img})
                imgObj = cont.create_image(Cl*(l+1),(i-0.5)*linesSpacing+15,anchor='center',image=img)
                
        else:
            #print(len(line))
            '''if(len(line)>69):
                cont.create_text(Cx,i*linesSpacing+15,
                             text=line[:69],font=("Arial", 12),
                             fill="white",justify=CENTER)
                i+=1
                cont.create_text(Cx,i*linesSpacing+15,
                             text=line[69:],font=("Arial", 12),
                             fill="white",justify=CENTER)
            else:'''
            linClr = line.split('£')
            if len(linClr)>1:
                cont.create_text(Cx,i*linesSpacing+15,
                             text=linClr[0][0:offset],font=("Arial", 12,attrLine),
                             fill=linClr[1].strip(),width=480,justify=CENTER)
            else:
                cont.create_text(Cx,i*linesSpacing+15,
                             text=line[0:offset],font=("Arial", 12,attrLine),
                             fill="white",width=480,justify=CENTER)
            
        i+=1
    cont.rowconfigure(0,weight=1)
    cont.columnconfigure(0,weight=1)


    return guide
    #guide.mainloop()

if __name__ == "__main__":
    app = ctk.CTk()
    createGuideWindow(app, "Test Guide", 'testText.txt')
    app.mainloop()
