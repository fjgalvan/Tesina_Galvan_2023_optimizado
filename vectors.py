import pandas as pd
import numpy as np
import cv2

class Vectors:
    def __init__(self,Pa,Pb):
        self.Pa= [int(Pa[0]), int(Pa[1])]
        self.Pb= [int(Pb[0]), int(Pb[1])]

    def existeVectorDirector(self):
        if((self.Pa[0]<0) or (self.Pb[0]<0)): # x
            return False
        if((self.Pa[1]<0) or (self.Pb[1]<0)): # y
            return False
        else:
            return True

    def getVectorDirector(self,Pa, Pb):
        vector_director = np.array(Pb) - np.array(Pa)
        return vector_director

    def getAngle(self,Va, Vb):
        angle= np.math.atan2(np.linalg.det([Va,Vb]),np.dot(Va,Vb))
        angle= np.degrees(angle)
        return int(angle)

    def getDistance(self,Pa,Pb):
        distance= np.math.sqrt((Pa[0] - Pb[0])**2 + (Pa[1] - Pb[1])**2)
        return round(distance,2) #redondeo a 2 decimales



if __name__ == '__main__':

    pa=[0,2]
    pb=[2,2]
    v= Vectors(pa,pb)

    res= v.existeVectorDirector()
    print("res: ",res)

    angulo= v.getAngle(pa,pb)
    print("angulo: ",angulo)