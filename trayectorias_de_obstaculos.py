

class Trayectorias_de_obstaculos:
    def __init__(self,obstaculos_array_actual):
        self.obstaculos_array_actual= obstaculos_array_actual

    def get_PuntosDeObstaculos_Actual(self,obstaculos_position_array_array):
        obstaculos_position_array= []
        for o_array in (self.obstaculos_array_actual):
            ## Analizo todos los obstáculos
            for o in o_array:
                if(o.obstaculo == "person"): # Si el obstaculo sí es una persona
                    if(o.distancia_persona_obstaculo != 0.0): #Si person NO es person_followed
                        obstaculo_position= [o.centro_x_obstaculo,o.centro_y_obstaculo]
                        obstaculos_position_array.append(obstaculo_position)
        return obstaculos_position_array

    def get_PuntosDeObstaculos(self,obstaculos_position_array_array):
        obstaculos_position_array= []
        for o_array in (self.obstaculos_array_actual):
            ## Analizo todos los obstáculos
            for o in o_array:
                if(o.obstaculo == "person"): # Si el obstaculo sí es una persona
                    if(o.distancia_persona_obstaculo != 0.0): #Si person NO es person_followed
                        obstaculo_position= [o.centro_x_obstaculo,o.centro_y_obstaculo]
                        obstaculos_position_array.append(obstaculo_position)
        if(len(obstaculos_position_array)>=1):
            obstaculos_position_array_array.append(obstaculos_position_array)
        
        #print("obstaculos_position_array: ",obstaculos_position_array)

        return obstaculos_position_array_array
    
    '''def persistirData(self, obstaculos_position_array_array):
        print("Complear Trayectorias_de_obstaculos persistirData !!!")
    '''

    def si_HayPerdidasDeCantidadDeObstaculos(self,obstaculos_position_array_array):
        res= False
        cant_Frames= len(obstaculos_position_array_array)
        cant_obstPrevio= len(obstaculos_position_array_array[cant_Frames-2])
        cant_obstActual= len(obstaculos_position_array_array[cant_Frames-1])
        #print("Cantidad de obstaculos previo: ",cant_obstPrevio)
        #print("Cantidad de obstaculos actual: ",cant_obstActual)

        if(cant_obstPrevio != cant_obstActual):
            res= True
        return res

    def si_HayMenosObstáculosActual(self,obstaculos_position_array_array):
        res= False
        cant_Frames= len(obstaculos_position_array_array)
        cant_obstPrevio= len(obstaculos_position_array_array[cant_Frames-2])
        cant_obstActual= len(obstaculos_position_array_array[cant_Frames-1])
        #print("Cantidad de obstaculos previo: ",cant_obstPrevio)
        #print("Cantidad de obstaculos actual: ",cant_obstActual)

        if(cant_obstPrevio > cant_obstActual):
            res= True
            print("Actual tiene menos obstáculos detectados que en el frame previo")
        return res