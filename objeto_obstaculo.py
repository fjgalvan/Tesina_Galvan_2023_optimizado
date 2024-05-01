import numpy as np
import os

class Objeto_obstaculo:
    def __init__(self,fecha,hora,obstaculo,centro_x_persona,centro_y_persona,centro_x_persona_old,centro_y_persona_old,vd_x_persona,vd_y_persona,centro_x_obstaculo,centro_y_obstaculo,angulo_persona_obstaculo,distancia_persona_obstaculo):
        self.fecha= fecha
        self.hora= hora
        self.obstaculo= obstaculo
        self.centro_x_persona= centro_x_persona
        self.centro_y_persona= centro_y_persona
        self.centro_x_persona_old= centro_x_persona_old
        self.centro_y_persona_old= centro_y_persona_old
        self.vd_x_persona= vd_x_persona
        self.vd_y_persona= vd_y_persona
        self.centro_x_obstaculo= centro_x_obstaculo
        self.centro_y_obstaculo= centro_y_obstaculo
        self.angulo_persona_obstaculo= angulo_persona_obstaculo
        self.distancia_persona_obstaculo= distancia_persona_obstaculo
        self.create_obstaculos_csv()

    def get_description(self):
        descripcion_0= self.fecha + ", " + self.hora + ", obstaculo:" + self.obstaculo + ", person_new_old: (" +self.centro_x_persona +", " + self.centro_y_persona +"), "
        descripcion_1= "(" +self.centro_x_persona_old +", " + self.centro_y_persona_old +") - "
        descripcion_2= "vd= (" +str(self.vd_x_persona) +", " + str(self.vd_y_persona) +") - "
        descripcion_3= "obstaculo: (" +self.centro_x_obstaculo +", " + self.centro_y_obstaculo +"), "
        descripcion_4= "angulo: "+str(self.angulo_persona_obstaculo)+" - "
        descripcion_5= "distancia: "+str(self.distancia_persona_obstaculo)
        descripcion= descripcion_0 + descripcion_1 + descripcion_2 + descripcion_3 + descripcion_4 + descripcion_5

        return descripcion

    def create_obstaculos_csv(self):
        archivo="data/Obstaculos.csv"
        #GUARDO LA INFO EN archivo .csv
        if(os.path.isfile(archivo) == False):
            csv=open(archivo,'w')
            nombre_columnas= "fecha,hora,objeto,centro_x,centro_y,centro_x_old,centro_y_old,vd_x,vd_y,centro_x_obst,centro_y_obst,vd_angulo,vd_distancia\n"
            csv.write(nombre_columnas)
            csv.close()


    def save_obstaculos_csv(self):
        #GUARDO LA INFO EN archivo .csv
        archivo="data/Obstaculos.csv"

        csv=open(archivo,'a')
        ##Ver bien como usar los datos de los df !!!
        filas=str(self.fecha)+','+str(self.hora)+","+str(self.obstaculo)+","+str(self.centro_x_persona)+","+str(self.centro_y_persona)+","+str(self.centro_x_persona_old)+","+str(self.centro_y_persona_old)+","+str(self.vd_x_persona)+","+str(self.vd_y_persona)+","+str(self.centro_x_obstaculo)+","+str(self.centro_y_obstaculo)+","+str(self.angulo_persona_obstaculo)+","+str(self.distancia_persona_obstaculo)+"\n"
        csv.write(filas)

    def get_angle(self,vector_person, vector_obstacle):
        angle= np.math.atan2(np.linalg.det([vector_person,vector_obstacle]),np.dot(vector_person,vector_obstacle))
        angle= np.degrees(angle)
        angle= int(angle)
        return angle

    def get_distance(self,p1,p2):
        distance= np.math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        return round(distance,2) #redondeo a 2 decimales