import numpy as np
from limitesMapaVirtual import LimitesMapaVirtual

class Trayectoria_De_Personas:
    def __init__(self,personas_Obst_y_PF_historial_array_array): ##,trayectorias_de_personas_array):
        self.personas_Obst_y_PF_historial_array_array= personas_Obst_y_PF_historial_array_array
        long= len(self.personas_Obst_y_PF_historial_array_array)
        self.personas_new_array= self.personas_Obst_y_PF_historial_array_array[long -1]
        if(len(personas_Obst_y_PF_historial_array_array)==1):
            self.personas_old_array=[]
        else:
            self.personas_old_array= self.personas_Obst_y_PF_historial_array_array[long -2]
        ##self.trayectorias_de_personas_array= trayectorias_de_personas_array

    def get_puntos_trayectoria(self):
        puntos_array=[]
        return puntos_array

    def esta_enVigencia(self):
        res= False
        return res

    def esta_enPerdidaParcial(self):
        res= False
        return res

    def esta_enPerdidaDefinitiva(self):
        res= False
        return res

    def esta_enElCentroDelROI(self):
        res= False
        return res

    def está_enElExtremoDelROI(self):
        res= False
        return res

    def get_distancias(self):
        print("self.personas_old_array: ",self.personas_old_array)
        print("self.personas_new_array: ",self.personas_new_array)

        d=-1
        distancia_array_array= []
        i= 0
        for old in self.personas_old_array:
            distancia_array= []
            j= 0
            for new in self.personas_new_array:
                p1= old
                p2= new
                d= self.getDistance(p1,p2)
                distancia_array.append(d)
                j= j+1
            distancia_array_array.append(distancia_array)
            i= i+1
        return distancia_array_array

    def getDistance(self,p1,p2):
        distance= np.math.sqrt((int(p1[0]) - int(p2[0]))**2 + (int(p1[1]) - int(p2[1]))**2)
        return round(distance,2) #redondeo a 2 decimales

    def isDistanciaAceptable(self, distancia_array_array, distAceptable):
        isAceptable_array_array= []
        i= 0
        for distancia_array in distancia_array_array:
            isAceptable_array= []
            j= 0
            for distancia in distancia_array:
                aceptable= False
                if(distancia <= distAceptable):
                    aceptable= True
                isAceptable_array.append(aceptable)
                j= j+1
            isAceptable_array_array.append(isAceptable_array)
            i= i+1
        return isAceptable_array_array

    def limitesExtremosDelMapa(self,w_window,h_window):
        lmv= LimitesMapaVirtual(w_window,h_window)
        areNewEnElExtremoROI_array= lmv.areNewEnElExtremoROI(self.personas_new_array)
        return areNewEnElExtremoROI_array
    
    def limitesCentroDelMapa(self,w_window,h_window):
        lmv= LimitesMapaVirtual(w_window,h_window)
        areNewEnElCentroROI_array= lmv.areNewEnElCentroROI(self.personas_new_array)#lmv.estaEnElCentroDelMapa(self.personas_new_array)
        return areNewEnElCentroROI_array


    '''def getAngle(self,vector_person, vector_obstacle):
        angle= np.math.atan2(np.linalg.det([vector_person,vector_obstacle]),np.dot(vector_person,vector_obstacle))
        angle= np.degrees(angle)
        return int(angle)'''