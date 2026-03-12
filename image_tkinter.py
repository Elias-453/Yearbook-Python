import tkinter
from PIL import ImageTk , Image




def tkinte():
    
    fenetre = tkinter.Tk()

    fenetre.title("Logo supinfo")
    fenetre.config()
    
    img = ImageTk.PhotoImage(Image.open("output/images/photoClasse.png"))
    mon_label = tkinter.Label(fenetre, image=img, )
    mon_label.pack()

    mon_bouton = tkinter.Button(fenetre, image= img)
    mon_bouton.pack()

    fenetre.mainloop()