import numpy as np

class Recalculating:
    
    def __init__(self, nivel_danger_array):
        self.nivel_danger_array = nivel_danger_array
        self.giro_derecha_30_grados= [[345,315],[315,285]]
        self.giro_izquierda_30_grados= [[15,45],[45,75]]


    def girar_angulo_director(self):
        girar_angulos= 0
        if not (5 in self.nivel_danger_array):
            girar_angulos= 0
            return girar_angulos
        if not (4 in self.nivel_danger_array):
            girar_angulos= -30
            return girar_angulos
        if not (3 in self.nivel_danger_array):
            girar_angulos= 30
            return girar_angulos
        if not (2 in self.nivel_danger_array):
            girar_angulos= -60
            return girar_angulos
        if not (1 in self.nivel_danger_array):
            girar_angulos= 60
            return girar_angulos

        return girar_angulos
        

    