import numpy as np
import cv2
from person_followed import Person_followed

class BuscarPersonFollowed:
    def __init__(self,objeto_detectado_roi_array):
        self.objeto_detectado_roi_array= objeto_detectado_roi_array

    def getPersonFollowed(self,person_followed_array,centro_xy_old_array,person_followed_xy_array,objeto_detectado_roi_array,obstaculos_array_actual,pv,vd_p_promedio,obstaculos_array_array,objeto_detectado_roi_person_array,count_person_followed,vd_p,area_mapaVirtual):

        objeto_detectado_roi_person_array,person_followed_xy_array,obstaculos_array_actual,count_person_followed= self.getFirstPersonFollowed(person_followed_array,centro_xy_old_array,person_followed_xy_array,objeto_detectado_roi_array,obstaculos_array_actual,pv,vd_p_promedio,obstaculos_array_array,objeto_detectado_roi_person_array,count_person_followed)

        person_followed_xy_array= self.getRestPersonFollowed(objeto_detectado_roi_person_array,count_person_followed,person_followed_array,centro_xy_old_array,vd_p,person_followed_xy_array,pv,objeto_detectado_roi_array,vd_p_promedio,obstaculos_array_actual,obstaculos_array_array,area_mapaVirtual)

        return person_followed_xy_array,obstaculos_array_actual

    def getFirstPersonFollowed(self,person_followed_array,centro_xy_old_array,person_followed_xy_array,objeto_detectado_roi_array,obstaculos_array_actual,pv,vd_p_promedio,obstaculos_array_array,objeto_detectado_roi_person_array,count_person_followed):

        for objeto_detectado_roi in self.objeto_detectado_roi_array:
            #Quiero saber cual de todas las personas es el Person_followed
            if(objeto_detectado_roi.objeto == 'person'):
                if(len(person_followed_array)==0): #ENTRO SOLO 1 VEZ !!!
                    person_followed= Person_followed(objeto_detectado_roi.fecha,objeto_detectado_roi.hora,objeto_detectado_roi.centro_x,objeto_detectado_roi.centro_y)
                    person_followed_array.append(person_followed)
                    centro_x_old= objeto_detectado_roi.centro_x
                    centro_y_old= objeto_detectado_roi.centro_y
                    centro_xy_old_array.append([centro_x_old,centro_y_old])
                    count_person_followed= count_person_followed+1

                    person_followed_xy_array.append([centro_x_old,centro_y_old]) # NUEVO

                    obstaculos_array= pv.set_obstaculos(objeto_detectado_roi_array,person_followed,centro_x_old,centro_y_old,vd_p_promedio) #,vd_p)
                    obstaculos_array_actual.append(obstaculos_array)
                    obstaculos_array_array.append(obstaculos_array)

                    person_followed.create_person_followed_csv()
                    person_followed.save_person_followed_csv()

                    #print("Primer person_followed_xy_array detectado!!")
                    #print("person_followed_xy_array: ",person_followed_xy_array)

                # Agrego a la lista de personas detectadas al mismo instante
                objeto_detectado_roi_person_array.append(objeto_detectado_roi)

        return objeto_detectado_roi_person_array,person_followed_xy_array,obstaculos_array_actual,count_person_followed

    def getRestPersonFollowed(self,objeto_detectado_roi_person_array,count_person_followed,person_followed_array,centro_xy_old_array,vd_p,person_followed_xy_array,pv,objeto_detectado_roi_array,vd_p_promedio,obstaculos_array_actual,obstaculos_array_array,area_mapaVirtual):
        if(len(objeto_detectado_roi_person_array)>0): # si se detecto al menos 1 persona

            if(count_person_followed == 0): #Es para no guardar 2 veces la primer persona followed
                longitud= len(person_followed_array)
                centro_x_old= person_followed_array[longitud-1].centro_x
                centro_y_old= person_followed_array[longitud-1].centro_y
                centro_xy_old_array.append([centro_x_old,centro_y_old])

                #Person Followed debe ser:
                # 1ro) la primer persona en ser detectada
                # 2do) la persona más cercana a centro_xy_old
                # 3ro) la persona más cercana al nuevo centro_xy_old y al ángulo vd_old
                ####person_f= pv.get_person_followed(objeto_detectado_roi_person_array,centro_x_old,centro_y_old)
                #### nuevo - inicio ####

                ## ÁNGULOS ##
                person_f_angulos_array,person_f_angulos_array_sort_index= self.getAngulos(objeto_detectado_roi_person_array,centro_x_old,centro_y_old,centro_xy_old_array,vd_p,pv)

                ## DISTANCIAS ##
                person_f_distancias_array,person_f_distancias_array_sort_index= self.getDistancias(objeto_detectado_roi_person_array,centro_x_old,centro_y_old,centro_xy_old_array,pv)

                ## ÚLTIMA DISTANCIA ##
                distanciaUltima= self.getUltimaDistancia(person_followed_xy_array)

                ## BUSCO "person_f" ##
                person_f= self.busco_person_f(person_f_angulos_array,objeto_detectado_roi_person_array,centro_x_old,centro_y_old,pv,person_f_angulos_array_sort_index,person_f_distancias_array_sort_index,person_f_distancias_array,distanciaUltima,area_mapaVirtual)

                person_followed_array.append(person_f)

                #Antes de esto, debo de definir bien a la Person_Follow !!

                obstaculos_array= pv.set_obstaculos(objeto_detectado_roi_array,person_f,centro_x_old,centro_y_old,vd_p_promedio) #,vd_p)
                obstaculos_array_actual.append(obstaculos_array)
                obstaculos_array_array.append(obstaculos_array)

                person_f.save_person_followed_csv()

                person_followed_xy_array.append([person_f.centro_x,person_f.centro_y])
                #print("Otros person_followed_xy_array detectado!!")
                #print("person_followed_xy_array: ",person_followed_xy_array)

                # OBS: Esto lo puedo hacer primero, con los 2 últimos posiciones de PersonFollow !!!

        return person_followed_xy_array,obstaculos_array_actual

    def busco_person_f(self,person_f_angulos_array,objeto_detectado_roi_person_array,centro_x_old,centro_y_old,pv,person_f_angulos_array_sort_index,person_f_distancias_array_sort_index,person_f_distancias_array,distanciaUltima,area_mapaVirtual):
        ## BUSCO "person_f" ##
        person_f= None
        #print("len(person_f_angulos_array): ",len(person_f_angulos_array))
        if(len(person_f_angulos_array)<3): #Busca a la Peson más cercana a xy old.
            person_f= pv.get_person_followed(objeto_detectado_roi_person_array,centro_x_old,centro_y_old) # Muevo
        if(len(person_f_angulos_array)>=3):
            ####person_followed_segun_angulo_y_distancia= pv.get_person_followed_segun_angulo_y_distancia(objeto_detectado_roi_person_array,person_f_angulos_array_sort_index,person_f_distancias_array_sort_index,person_f_angulos_array,person_f_distancias_array,distanciaUltima) #,distanciaUltima)

            ##MEJORA test
            person_followed_segun_angulo_y_distancia= pv.getPersonFollow_by_angle_and_distance(objeto_detectado_roi_person_array,person_f_angulos_array_sort_index,person_f_distancias_array_sort_index,person_f_angulos_array,person_f_distancias_array,distanciaUltima,area_mapaVirtual)

            p_f= person_followed_segun_angulo_y_distancia
            if(p_f is not None):
                person_f= Person_followed(p_f.fecha, p_f.hora, p_f.centro_x, p_f.centro_y)
            if(p_f is None):
                print("p_f is None")

        #print("person_followed_xy_array: ",person_followed_xy_array)
        #### nuevo - fin ####
        return person_f

    def getAngulos(self,objeto_detectado_roi_person_array,centro_x_old,centro_y_old,centro_xy_old_array,vd_p,pv):
        person_f_angulos_array= pv.get_angle_array_promedio(objeto_detectado_roi_person_array, centro_x_old, centro_y_old,centro_xy_old_array, vd_p) #Ver como obtener vd_p antes!!!
        ##person_f_angulos_array= pv.get_angle_array(objeto_detectado_roi_person_array,centro_x_old,centro_y_old,centro_xy_old_array)
        person_f_angulos_array_sort= pv.get_angle_array_sort(person_f_angulos_array)
        person_f_angulos_array_sort_index= pv.get_angle_array_sort_index(person_f_angulos_array,person_f_angulos_array_sort)
        #print("vd_p en ANGULOS: ", vd_p)
        #print("person_f_angulos_array_sort: ",person_f_angulos_array_sort)
        #print("person_f_angulos_array: ",person_f_angulos_array)

        return person_f_angulos_array,person_f_angulos_array_sort_index

    def getDistancias(self,objeto_detectado_roi_person_array,centro_x_old,centro_y_old,centro_xy_old_array,pv):
        person_f_distancias_array= pv.get_distance_array(objeto_detectado_roi_person_array,centro_x_old,centro_y_old,centro_xy_old_array)
        person_f_distancias_array_sort= pv.get_distance_array_sort(person_f_distancias_array)
        person_f_distancias_array_sort_index= pv.get_distance_array_sort_index(person_f_distancias_array,person_f_distancias_array_sort)
        #print("person_f_distancias_array: ",person_f_distancias_array)
        #print("person_f_distancias_array_sort: ",person_f_distancias_array_sort)

        return person_f_distancias_array,person_f_distancias_array_sort_index

    def getUltimaDistancia(self,person_followed_xy_array):
        ## ÚLTIMA DISTANCIA ##
        distanciaUltima= -1
        #Busco la ultima distancia - inicio -
        #En esta seccion ya debería de haber por lo menos 2 posiciones detectadas de PersonFollow
        #print("person_followed_xy_array: ",person_followed_xy_array)
        cant_person_follow_posictions= len(person_followed_xy_array)
        #print("cant_person_follow_posictions: ",cant_person_follow_posictions)

        if(cant_person_follow_posictions >= 2):
            posicion_anteUltimo= cant_person_follow_posictions-2
            posicion_ultimo= cant_person_follow_posictions-1

            p1= person_followed_xy_array[posicion_anteUltimo]
            p2= person_followed_xy_array[posicion_ultimo]

            distanciaUltima= self.getDistance(p1,p2)
            #print("distanciaUltima: ",distanciaUltima)
        #Busco la ultima ditancia - fin -

        return distanciaUltima

    def getDistance(self,p1,p2):
        distance= np.math.sqrt((int(p1[0]) - int(p2[0]))**2 + (int(p1[1]) - int(p2[1]))**2)
        return round(distance,2) #redondeo a 2 decimales