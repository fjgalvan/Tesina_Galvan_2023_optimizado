import numpy as np

class Objeto_detectado_roi:
    
    def __init__(self,fecha,hora,objeto,confidence,dest_q1_x,dest_q1_y,dest_q2_x,dest_q2_y,dest_q3_x,dest_q3_y,dest_q4_x,dest_q4_y,centro_x,centro_y):
        self.fecha= fecha
        self.hora= hora
        self.objeto = objeto
        self.confidence = confidence
        self.dest_q1_x= dest_q1_x
        self.dest_q1_y= dest_q1_y
        self.dest_q2_x= dest_q2_x
        self.dest_q2_y= dest_q2_y
        self.dest_q3_x= dest_q3_x
        self.dest_q3_y= dest_q3_y
        self.dest_q4_x= dest_q4_x
        self.dest_q4_y= dest_q4_y
        self.centro_x= centro_x
        self.centro_y= centro_y

'''    def getVectorDirector(self,Point_old_array, Point_new_array):
        vector_director = np.array(Point_new_array).astype(int) - np.array(Point_old_array).astype(int)
        return vector_director
    
    def getAngle(self,vector_person, vector_obstacle):
        angle= np.math.atan2(np.linalg.det([vector_person,vector_obstacle]),np.dot(vector_person,vector_obstacle))
        angle= np.degrees(angle)
        return int(angle)

    def getDistance(self,p1,p2):
        distance= np.math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        return round(distance,2) #redondeo a 2 decimales

    def get_description(self):
        descripcion= self.fecha + ", " + self.hora + ", " + self.objeto + ", (" +self.centro_x +", " + self.centro_y +")"
        return descripcion

    def get_objeto_detectado_roi_person_menorDistancia(self,objeto_detectado_roi_person_array,centro_x_old,centro_y_old):


        return objeto_detectado_roi_person_array[0]
'''  