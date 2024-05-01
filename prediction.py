import numpy as np

class Prediction:
    
    def __init__(self, puntoPrevio, puntoActual):#Array [*, *]
        self.puntoPrevio = puntoPrevio
        self.puntoActual = puntoActual
  
    '''def getVector(self, p0, p1):
        v0 = np.array(p1) - np.array(p0)
        return v0

    def getAngulo(self, v0, v1):
        angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1)) #radianes
        angle= np.degrees(angle) #grados
        return angle'''

    def get_distance(self,p1,p2):
        distance= np.math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        return round(distance,2) #redondeo a 2 decimales

    def getDangerPrediction(self, angulo, distanciaPersonaObstaculo,distanceDanger):
        if(angulo < 0):
            angulo= angulo + 360
        
        if(distanceDanger == 0.0):
            danger= "Este es el caso 0 !!"
            return danger,0

        danger= "No hay peligro evidente"
        nivel_danger= 0
        ultimaDistanciaPersona= self.get_distance([int(self.puntoPrevio[0]),int(self.puntoPrevio[1])],[int(self.puntoActual[0]),int(self.puntoActual[1])])
        if(distanciaPersonaObstaculo <= distanceDanger): #<= ultimaDistanciaPersona):
            if((0<= angulo<=15) or (345< angulo<=360)):
                danger= "Peligro alto de colisión centro"
                nivel_danger= 5
            if(315< angulo<=345):
                danger= "Peligro medio de colisión a la derecha"
                nivel_danger= 4
            if(15<= angulo<45):
                danger= "Peligro medio de colisión a la izquierda"
                nivel_danger= 3 
            if(285<= angulo<=315):
                danger= "Peligro bajo de colisión a la derecha"
                nivel_danger= 2
            if(45<= angulo<=75):
                danger= "Peligro bajo de colisión a la izquierda"
                nivel_danger= 1
        #print("danger: ",danger)
        #print("nivel_danger: ",nivel_danger)
        return danger,nivel_danger