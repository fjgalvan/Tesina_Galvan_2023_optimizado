import numpy as np
import os

class Person_followed:
    
    def __init__(self,fecha,hora,centro_x,centro_y):
        self.fecha= fecha
        self.hora= hora
        self.centro_x= centro_x
        self.centro_y= centro_y

    def getDistance(self,p1,p2):
        distance= np.math.sqrt((int(p1[0]) - int(p2[0]))**2 + (int(p1[1]) - int(p2[1]))**2)
        return round(distance,2) #redondeo a 2 decimales

    '''def getAngle(self,vector_person, vector_obstacle):
        angle= np.math.atan2(np.linalg.det([vector_person,vector_obstacle]),np.dot(vector_person,vector_obstacle))
        angle= np.degrees(angle)
        return int(angle)

    # Dada una lista de centros(x,y) de personas detectadas en cierto instante,
    # obtengo el centro(x,y) más cercano al centro(x,y) de la persona en seguimiento
    def get_person_closet_to_a_point(self, persons_centroXY_array):
        distancias_array= []
        person_followed_xy= [self.centro_x,self.centro_y]
        for persons_centroXY in persons_centroXY_array: #analizo todos los centrosXY de los objetos de cada detección
            person_xy= [persons_centroXY[0],persons_centroXY[1]]
            dist= self.getDistance(person_followed_xy,person_xy)
            distancias_array.append(dist)

        return distancias_array'''

    def create_person_followed_csv(self):
        archivo="data/Person_followed.csv"
        #GUARDO LA INFO EN archivo .csv
        if(os.path.isfile(archivo) == False):
            csv=open(archivo,'w')
            nombre_columnas= "fecha,hora,centro_x,centro_y\n"
            csv.write(nombre_columnas)
            csv.close()

    def save_person_followed_csv(self):
        #GUARDO LA INFO EN archivo .csv
        archivo="data/Person_followed.csv"

        csv=open(archivo,'a')
        ##Ver bien como usar los datos de los df !!!
        filas=str(self.fecha)+','+str(self.hora)+","+str(self.centro_x)+","+str(self.centro_y)+"\n"
        csv.write(filas)