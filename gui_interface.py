from tkinter import Tk
from tkinter import Canvas as canvas1 
from tkinter import Button
#import pandas as pd
import cv2
#import pyautogui as pg
from tkinter import filedialog
#from PIL import ImageTk, Image, ImageDraw 
import PIL.ImageGrab as ImageGrab 

# pip install ipycanvas
#from ipycanvas import Canvas as canvas2

import numpy as np


class Gui_interface:
    #window= Tk()
    def __init__(self,w_window,h_window):
        self.w_window= str(w_window)
        self.h_window= str(h_window)
        self.window= Tk()
        geometry_w_h= self.w_window+"x"+self.h_window
        self.window.geometry(geometry_w_h)#("400x400")
        self.window.configure(background = "grey")
        self.window.title("area dibujo")
        self.window.resizable(False, False)
        #button= Button(self.window, text="Quit", command=self.window.destroy)
        #button.pack()
        #self.canvas= Canvas(self.window, width=self.w_window,height=self.h_window,bg='white')
        self.canvas= canvas1(width=self.w_window,height=self.h_window,bg='white')
        self.canvas.pack() #pady = 20 

    def draw_arc(self,x0,y0,x1,y1,start_angle,extend_angle,fill_color):
        self.canvas.create_arc(x0,y0,x1,y1,start=start_angle,extent=extend_angle,fill =fill_color)

    def draw_oval(self,x0,y0,x1,y1,width_perimetro,fill_color):
        self.canvas.create_oval(x0,y0,x1,y1,width= width_perimetro,fill=fill_color)

    def draw_line(self):
        self.canvas.create_line(0,0,800,800)

    def draw_rectangle(self):
        self.canvas.create_rectangle(150,300,50,500,width=10,fill='blue')

    def draw_text(self,text_input):
        self.canvas.create_text(100,20,text=text_input,font=('arial',10),fill='blue')

    def get_X0_Y0_X1_Y1_area(self, centro_x_obstaculo,centro_y_obstaculo,ancho):
        points_rectangle= []
        X0= int(centro_x_obstaculo)
        Y0= int(centro_y_obstaculo)
        X1= int(centro_x_obstaculo)
        Y1= int(centro_y_obstaculo)
        X0_area= X0-ancho
        Y0_area= Y0-ancho
        X1_area= X1+ancho
        Y1_area= Y1+ancho
        '''
        if(X0_area < 0):
            X0_area=0
        if(Y0_area < 0):
            Y0_area=0
        if(X1_area >= int(self.w_window)):
            X1_area=int(self.w_window)
        if(Y1_area >= int(self.h_window)):
            Y1_area=int(self.h_window)
        '''
        points_rectangle.append(X0_area)
        points_rectangle.append(Y0_area)
        points_rectangle.append(X1_area)
        points_rectangle.append(Y1_area)
        
        return points_rectangle
    
    def get_angulo_gui(self,angulo):
        angulo_gui= 0
        if(angulo < 0): # 0º<angulos<360º
            angulo_gui= 360 + angulo
        else:
            angulo_gui= angulo

        return angulo_gui

    '''def get_angulo_gui(self,angulo):
        angulo_gui= 0
        if(angulo < 0): # 0º<angulos<360º
            angulo= 180 + 180 + angulo ## ESTO NOO VAAAAA!!!!
        angulo_gui= 360 - angulo

        return angulo_gui'''

    def hide_window(self):
        # hiding the tkinter window while taking the screenshot
        self.window.withdraw()
        self.window.after(1000, self.screenshot)

    def saveImage(self,img_tkinter_num):
        self.window.update()
        x= self.window.winfo_rootx()
        y= self.window.winfo_rooty()

        img= ImageGrab.grab(bbox=(x,y,x+int(self.w_window),y+int(self.h_window)))
        #img.show()
        img_np= np.array(img)
        img_np= cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        cv2.imwrite(img_tkinter_num, img_np)
        
        return img_np

if __name__ == '__main__':
    
    
    g= Gui_interface(400,400)
    g.draw_arc(50,70,170,190,0,45,"red")
    g.draw_oval(100,120,120,140,1,"green")
    #g.window.after(2000, g.window.destroy)
    
    
    button = Button(g.window, text="Take Screenshot", font=('Aerial 11 bold'), background="#aa7bb1", foreground="white", command=g.hide_window)
    button.pack(pady=20)
    g.window.mainloop()

    g= Gui_interface(400,400)
    g.draw_arc(250,270,370,390,0,45,"red")
    g.draw_oval(300,320,320,340,1,"green")
    g.window.after(2000, g.window.destroy)
    g.window.mainloop()
    

    '''
    #crear una lista tipos de graficos
    
    datos_Trazabilidad=pd.read_csv('data/Trazabilidad_test_2.csv')
    df_Trazabilidad=pd.DataFrame(datos_Trazabilidad)

    #print(df_Trazabilidad.dtypes)
    df_Trazabilidad_final = df_Trazabilidad.drop(["confidence","dest_q1_x", "dest_q1_y","dest_q2_x", "dest_q2_y","dest_q3_x", "dest_q3_y","dest_q4_x", "dest_q4_y"], axis=1)
    
    #Agrego columnas init
    vector_director_x= []
    vector_director_y= []
    vector_director_angulo= []
    vector_director_distancia= []
    id_posicion_viejo= []
    for i in range(len(df_Trazabilidad_final)):
        #df_Trazabilidad_final.iloc[i]['vector_director_x']= 0
        vector_director_x.append(0)
        vector_director_y.append(0)
        vector_director_angulo.append(0)
        vector_director_distancia.append(0)
        id_posicion_viejo.append(-1)

    df_Trazabilidad_final['vd_x']= vector_director_x
    df_Trazabilidad_final['vd_y']= vector_director_y
    df_Trazabilidad_final['vd_angulo']= vector_director_angulo
    df_Trazabilidad_final['vd_distancia']= vector_director_distancia
    df_Trazabilidad_final['id_old']= id_posicion_viejo

    df_Trazabilidad_final['centro_x_old']= df_Trazabilidad_final['centro_x']
    df_Trazabilidad_final['centro_y_old']= df_Trazabilidad_final['centro_y']

    print(df_Trazabilidad_final)

    #grafico
    print("grafico:")
    g= Gui_interface(400,400)
    for i in range(len(df_Trazabilidad_final)):
        #if(df_Trazabilidad_final.iloc[i]['id_old']>=0):
            if(df_Trazabilidad_final.iloc[i]['objeto']== 'person'):
                print("i: ",i)
                g.draw_arc(50,70,170,190,0,45,"red")
                g.draw_oval(100,120,120,140,1,"green")
    g.window.after(2000, g.window.destroy)
    g.window.mainloop()
    '''