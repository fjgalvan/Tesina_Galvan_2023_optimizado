# Desde VSCode: 
#$ source "c:/Users/Usuario/Desktop/Tesina 2022/ProyectoTesina/cv/Scripts/activate"
#$ python perspective_transformation_clics_video.py

import cv2
import numpy as np
from persist_data_roi_csv import Persist_data_roi_csv
from person_followed import Person_followed
from objeto_obstaculo import Objeto_obstaculo



class Perspective_video:
    '''
    def __init__(self):
        print("class Perspective_video")

    def clics(self,event,x,y,flags,param):
        global puntos
        if event == cv2.EVENT_LBUTTONDOWN:
            puntos.append([x,y])
    '''
    def __init__(self,puntos):
        #print("class Perspective_video")
        self.puntos= puntos
    
    def clics(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.puntos.append([x,y])

    def dibujando_puntos(self,puntos,frame):# (...,frame)
        for x, y in puntos:
            cv2.circle(frame,(x,y),5,(0,255,0),2)

    def uniendo4puntos(self,puntos,frame):# (...,frame)
        cv2.line(frame,tuple(puntos[0]),tuple(puntos[1]),(255,0,0),1)
        cv2.line(frame,tuple(puntos[0]),tuple(puntos[2]),(255,0,0),1)
        cv2.line(frame,tuple(puntos[2]),tuple(puntos[3]),(255,0,0),1)
        cv2.line(frame,tuple(puntos[1]),tuple(puntos[3]),(255,0,0),1)

    def maxWidth(self,pts1):
        maxW= 0
        tl= pts1[0][0]
        tr= pts1[0][1]
        bl= pts1[0][2]
        br= pts1[0][3]
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxW = max(int(widthA), int(widthB))

        return maxW

    def maxHeight(self,pts1):
        maxH= 0
        tl= pts1[0][0]
        tr= pts1[0][1]
        bl= pts1[0][2]
        br= pts1[0][3]
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxH = max(int(heightA), int(heightB))

        return maxH

    def persist_data_roi(self,M,pts1,pts2):
        pd1=Persist_data_roi_csv("data/pts1.csv","x1,y1,x2,y2,x3,y3,x4,y4\n",'w')
        pd1.persist_pts1(pts1)
        pd2=Persist_data_roi_csv("data/pts2.csv","x1,y1,x2,y2,x3,y3,x4,y4\n",'w')
        pd2.persist_pts2(pts2)
        pd3=Persist_data_roi_csv("data/M.csv","0,1,2\n",'w')
        pd3.persistirDatosM(M)
        print("M: \n",M)
        print("pts1: \n",pts1)
        print("pts2: \n",pts2)
        print("\n")

    def get_person_followed(self,objeto_detectado_roi_person_array, centro_x_old, centro_y_old):
        '''print("¿Quien es person_followed?")
        print("centro_x_old: ",centro_x_old)
        print("centro_y_old: ",centro_y_old)'''
        count= 0
        distance_array= []
        for objeto_detectado_roi_person in objeto_detectado_roi_person_array:

            person= Person_followed(objeto_detectado_roi_person.fecha,objeto_detectado_roi_person.hora,objeto_detectado_roi_person.centro_x,objeto_detectado_roi_person.centro_y)
            p1= [int(person.centro_x),int(person.centro_y)]
            p2= [int(centro_x_old), int(centro_y_old)]
            dist= person.getDistance(p1,p2)
            distance_array.append(dist)
            
            count= count+1

        minimo= min(distance_array)
        posicion_min= distance_array.index(minimo)

        maximo= max(distance_array)
        posicion_max= distance_array.index(maximo)

        i=0
        person_followed= None
        for objeto_detectado_roi_person in objeto_detectado_roi_person_array:
            if(i==posicion_min):
                p1= [int(objeto_detectado_roi_person.centro_x),int(objeto_detectado_roi_person.centro_y)]
                p2= [int(centro_x_old), int(centro_y_old)]
                person_followed= Person_followed(objeto_detectado_roi_person.fecha,objeto_detectado_roi_person.hora,objeto_detectado_roi_person.centro_x,objeto_detectado_roi_person.centro_y)
            i= i+1

        centro_x_new= person_followed.centro_x
        centro_y_new= person_followed.centro_y
        #print("centro_x_new: ",centro_x_new)
        #print("centro_y_new: ",centro_y_new)
        return person_followed

   

    def set_obstaculos(self,objeto_detectado_roi_array,person_followed,centro_x_old,centro_y_old,vd_p_promedio): #,vd_p): 
        i=0
        obstaculos_array= []

        for o in objeto_detectado_roi_array:
            Point_old= [int(centro_x_old),int(centro_y_old)]
            Point_new= [int(person_followed.centro_x),int(person_followed.centro_y)]

            vd_p= o.getVectorDirector(Point_old, Point_new)
            vd_p= [vd_p[0],vd_p[1]]
            #vd_x_persona= vd_p[0]
            #vd_y_persona= vd_p[1]
            vd_x_persona= vd_p_promedio[0]
            vd_y_persona= vd_p_promedio[1]
            Point_o= [int(o.centro_x),int(o.centro_y)]
            vd_o= o.getVectorDirector(Point_new,Point_o)
            angulo_persona_obstaculo=  o.getAngle(vd_o,vd_p_promedio)  #angulo_persona_obstaculo=  o.getAngle(vd_p, vd_o)
            distancia_persona_obstaculo= o.getDistance(Point_new,Point_o)

            obst= Objeto_obstaculo(o.fecha,o.hora,o.objeto,person_followed.centro_x,person_followed.centro_y,centro_x_old,centro_y_old,vd_x_persona,vd_y_persona,o.centro_x,o.centro_y,angulo_persona_obstaculo,distancia_persona_obstaculo)
            obst_descripcion= obst.get_description()
            obst.save_obstaculos_csv()
            ####print("obst_descripcion: ",obst_descripcion)
            obstaculos_array.append(obst)
            i= i+1

        return obstaculos_array

    def getDistance(self,p1,p2):
        distance= np.math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        return round(distance,2) #redondeo a 2 decimales

    def getAngle(self,vector_person, vector_obstacle):
        angle= np.math.atan2(np.linalg.det([vector_person,vector_obstacle]),np.dot(vector_person,vector_obstacle))
        angle= np.degrees(angle)
        return int(angle)

    def getVectorDirector(self,Point_old_array, Point_new_array):
        vector_director = np.array(Point_new_array) - np.array(Point_old_array)
        return vector_director

    def get_distance_array(self,objeto_detectado_roi_person_array, centro_x_old, centro_y_old,centro_xy_old_array):
        count= 0
        distance_array= []
        '''print("get_distance_array")
        print("centro_xy_old_array: ",centro_xy_old_array)
        print("centro_x_old: ",centro_x_old)
        print("centro_y_old: ",centro_y_old)'''

        if(len(centro_xy_old_array)>=3):
            for objeto_detectado_roi_person in objeto_detectado_roi_person_array:
                person= Person_followed(objeto_detectado_roi_person.fecha,objeto_detectado_roi_person.hora,objeto_detectado_roi_person.centro_x,objeto_detectado_roi_person.centro_y)
                p1= [int(person.centro_x),int(person.centro_y)]
                p2= [int(centro_x_old), int(centro_y_old)]
                dist= person.getDistance(p1,p2)
                distance_array.append(dist)
                count= count+1
        
        return distance_array

    def get_distance_array_sort(self,distance_array):
        #ordeno la lista de menor a mayor:
        aux= distance_array
        distance_array_menorAmayor= sorted(aux)
        
        return distance_array_menorAmayor

    def get_distance_array_sort_index(self,distance_array,distance_array_menorAmayor):
        dist_sorted_index= []
        for d in distance_array_menorAmayor:
            d_index= distance_array.index(d)
            dist_sorted_index.append(d_index)

        return dist_sorted_index


    def get_angle_array(self,objeto_detectado_roi_person_array, centro_x_old, centro_y_old,centro_xy_old_array):
        count= 0
        distance_array= []
        #print("get_angle_array")
        #print("centro_xy_old_array: ",centro_xy_old_array)
        #print("centro_x_old: ",centro_x_old)
        #print("centro_y_old: ",centro_y_old)
        
        angle_personFollow_old= 0
        vd= []
        vd_old= []
        diferencia_angle_old_vs_objeto_array=[]
        if(len(centro_xy_old_array)>=3):
            
            longitud= len(centro_xy_old_array)
            p1= [int(centro_x_old), int(centro_y_old)] #Nuevo
            p2= [int(centro_xy_old_array[longitud-2][0]), int(centro_xy_old_array[longitud-2][1])] #viejo
            #vd_old= self.getVectorDirector(p1,p2) #Obtengo el vector director de old 
            vd_old= self.getVectorDirector(p2,p1)
            #print("vd_old: ",vd_old)
            
            '''
            t= Trayectoria(p2,p1)
            versor= t.versor()
            desplazamiento= t.sentidoDesplazamiento(vd_old)
            #print("desplazamiento person follow: ", desplazamiento)

            angle_personFollow_old= self.getAngle([int(vd_old[0]),int(vd_old[1])],[1,0])
            if(angle_personFollow_old < 0):
                angle_personFollow_old= 360 + angle_personFollow_old
            #print("angle_personFollow_old: ",angle_personFollow_old)
            '''

            for objeto_detectado_roi_person in objeto_detectado_roi_person_array:
                person= Person_followed(objeto_detectado_roi_person.fecha,objeto_detectado_roi_person.hora,objeto_detectado_roi_person.centro_x,objeto_detectado_roi_person.centro_y)
                p1= [int(person.centro_x),int(person.centro_y)]
                p2= [int(centro_x_old), int(centro_y_old)]
                #vd_objeto= self.getVectorDirector(p2,p1)
                vd_objeto= self.getVectorDirector(p2,p1)
                vd.append(vd_objeto)
                angle= self.getAngle([int(vd_objeto[0]),int(vd_objeto[1])],[int(vd_old[0]),int(vd_old[1])]) #,[1,0])
                if(angle < 0):
                    angle= angle*(-1) #Es diferencia => es positivo su módulo
                diferencia_angle_old_vs_objeto_array.append(angle)
        
        #ordeno la lista de menor a mayor:
        ##angle_old_vs_objeto_array_menorAmayor= angle_old_vs_objeto_array
        ##angle_old_vs_objeto_array_menorAmayor= angle_old_vs_objeto_array_menorAmayor.sort()
        
        return diferencia_angle_old_vs_objeto_array

    def get_angle_array_sort(self,diferencia_angle_old_vs_objeto_array):
        #ordeno la lista de menor a mayor:
        aux= diferencia_angle_old_vs_objeto_array
        diferencia_angle_old_vs_objeto_array_menorAmayor= sorted(aux)

        #print("diferencia_angle_old_vs_objeto_array_menorAmayor: ",diferencia_angle_old_vs_objeto_array_menorAmayor)
        
        return diferencia_angle_old_vs_objeto_array_menorAmayor

    def get_angle_array_sort_index(self,diferencia_angle_old_vs_objeto_array,diferencia_angle_old_vs_objeto_array_menorAmayor):
        angulo_sorted_index= []
        for d in diferencia_angle_old_vs_objeto_array_menorAmayor:
            d_index= diferencia_angle_old_vs_objeto_array.index(d)
            angulo_sorted_index.append(d_index)

        return angulo_sorted_index

    def get_person_followed_segun_angulo_y_distancia(self,objeto_detectado_roi_person_array,angulo_sort_index,distancia_sort_index,person_f_angulos_array,person_f_distancias_array,distanciaUltima):#,distanciaUltima)
        angulo= None
        dist= None
        person= None
        encontrado= False

        ## Teniendo en cuenta la distancia Max aceptada para el menor ángulo ##
        distanciaDelMenorAngulo= person_f_distancias_array[angulo_sort_index[0]]
        if(distanciaDelMenorAngulo <= 10*distanciaUltima):
            print("distanciaDelMenorAngulo",distanciaDelMenorAngulo) 
        
        # Si se detecta más de 1 persona : ...

        # Si es el más cercano a centro xy_old y el de menor angulo al vd_old => es la persona_follow
        if(angulo_sort_index[0] == distancia_sort_index[0]): 
                person= objeto_detectado_roi_person_array[distancia_sort_index[0]]
                angulo= person_f_angulos_array[angulo_sort_index[0]]
                dist= person_f_distancias_array[distancia_sort_index[0]]
        #La prioridad es la distancia, salvo que la persona halla girado más de 90º
        else: 
            # Si la 2da persona más cercana es la de menor ángulo y el más cercano tiene un angulo en direccion contraria, 
            # el de menor ángulo => es la persona_follow
            if((angulo_sort_index[0] == distancia_sort_index[1]) and (person_f_angulos_array[distancia_sort_index[0]] >= 90 )):
                # Debo buscar a la persona, con dist de menor a mayor, cuyo angulo sea menor a 90º. 
                # Si no encuentro a nadie, me quedo con la persona de menor distancia
                
                

                person= objeto_detectado_roi_person_array[angulo_sort_index[0]]
                angulo= person_f_angulos_array[angulo_sort_index[0]]
                dist= person_f_distancias_array[angulo_sort_index[0]]
                encontrado = True
            else:
                i= 0
                for p in objeto_detectado_roi_person_array:
                    #reviso los angulos de todas las personas desde las dist de menor a mayor
                    if(person_f_angulos_array[distancia_sort_index[i]] < 90): # < 90): 
                        person= objeto_detectado_roi_person_array[angulo_sort_index[i]] # VER EL [0]]
                        angulo= person_f_angulos_array[angulo_sort_index[i]] # VER EL [0]]
                        dist= person_f_distancias_array[angulo_sort_index[i]] # VER EL [0]]

                        encontrado = True
                    i= i + 1    
                
            # Sino, la persona más cercana a centro_xy_old => es la persona_follow
            if(encontrado == False):
                person= objeto_detectado_roi_person_array[distancia_sort_index[0]]
                angulo= person_f_angulos_array[distancia_sort_index[0]]
                dist= person_f_distancias_array[distancia_sort_index[0]]

        print("get_person_followed_segun_angulo_y_distancia: (",person.centro_x,",",person.centro_y,")"," - angulo:",angulo," - distancia:",dist)
        return person

    ## Person Follow, reviso de menor a mayor ángulo y reviso si está dentro de una distancia aceptada. 
    ## Sino, elijo a la person más cercana como la nueva Person Follow.
    def getPersonFollow_by_angle_and_distance(self,objeto_detectado_roi_person_array,angulo_sort_index,distancia_sort_index,person_f_angulos_array,person_f_distancias_array,distanciaUltima,area_mapaVirtual):
        angulo= None
        dist= None
        person= None
        encontrado= False
        porcentajeAreaMapaVirtual= int(area_mapaVirtual*0.01)
        #print("porcentajeAreaMapaVirtual: ",porcentajeAreaMapaVirtual)
        distanciaTolerable= 3*distanciaUltima

        #Hay que tener en cuenta cuando la última distancia es "0", esto se soluciona con un <=
        if(distanciaUltima == 0.0):
            print("La persona se mantuvo en el mismo lugar!!!")
        '''
        if((person_f_distancias_array[angulo_sort_index[0]] > distanciaTolerable) and (encontrado == False)):
            print("La persona con menor ángulo supera la distanciaTolerable de: ",distanciaTolerable)
        '''
        if((distanciaUltima == 0.0) or ((person_f_distancias_array[angulo_sort_index[0]] > distanciaTolerable) and (encontrado == False))):
            #print("ver distanciaUltima cuando es 0.0 podria buscar a la persona mas cercana con una distancia menor al 10% del área del mapa por ejemplo")
            if((person_f_distancias_array[0]) <= porcentajeAreaMapaVirtual):
                person= objeto_detectado_roi_person_array[distancia_sort_index[0]]
                encontrado= True

        i= 0
        for p in objeto_detectado_roi_person_array:
            #reviso los angulos de todas las personas desde las dist de menor a mayor
            #print("angulo ",i,": ",person_f_angulos_array[angulo_sort_index[i]])
            #print("distancia ",i,": ",person_f_distancias_array[angulo_sort_index[i]])

            
            #3*distanciaUltima
            if((person_f_distancias_array[angulo_sort_index[i]] <= distanciaTolerable) and (encontrado == False)):
                person= objeto_detectado_roi_person_array[angulo_sort_index[i]]
                encontrado= True
            
            i= i + 1  
        

        return person
    
    def get_angle_array_promedio(self,objeto_detectado_roi_person_array, centro_x_old, centro_y_old,centro_xy_old_array, vd_promedio):
            count= 0
            distance_array= []
            #print("get_angle_array")
            #print("centro_xy_old_array: ",centro_xy_old_array)
            #print("centro_x_old: ",centro_x_old)
            #print("centro_y_old: ",centro_y_old)
            
            angle_personFollow_old= 0
            vd= []
            vd_old= []
            diferencia_angle_old_vs_objeto_array=[]
            if(len(centro_xy_old_array)>=3):

                for objeto_detectado_roi_person in objeto_detectado_roi_person_array:
                    person= Person_followed(objeto_detectado_roi_person.fecha,objeto_detectado_roi_person.hora,objeto_detectado_roi_person.centro_x,objeto_detectado_roi_person.centro_y)
                    p1= [int(person.centro_x),int(person.centro_y)]
                    p2= [int(centro_x_old), int(centro_y_old)]
                    #vd_objeto= self.getVectorDirector(p2,p1)
                    vd_objeto= self.getVectorDirector(p2,p1)
                    vd.append(vd_objeto)
                    angle= self.getAngle([int(vd_objeto[0]),int(vd_objeto[1])],[int(vd_promedio[0]),int(vd_promedio[1])]) #,[1,0])
                    if(angle < 0):
                        angle= angle*(-1) #Es diferencia => es positivo su módulo
                    diferencia_angle_old_vs_objeto_array.append(angle)
            
            #ordeno la lista de menor a mayor:
            ##angle_old_vs_objeto_array_menorAmayor= angle_old_vs_objeto_array
            ##angle_old_vs_objeto_array_menorAmayor= angle_old_vs_objeto_array_menorAmayor.sort()
            
            return diferencia_angle_old_vs_objeto_array
