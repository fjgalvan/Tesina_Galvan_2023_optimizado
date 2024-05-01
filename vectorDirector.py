from vectors import Vectors

class VectorDirector:
    def __init__(self,obstaculos_array_actual,person_followed_xy_array):
        self.obstaculos_array_actual= obstaculos_array_actual
        self.person_followed_xy_array= person_followed_xy_array

    def get_vd_promedio(self):
        p_white= [-1,-1] # todavia no existe
        p_lightGray= [-1,-1] # todavia no existe
        p_lightBlue= [-1,-1] # todavia no existe
        p_lightGreen= [-1,-1] # todavia no existe
        p_green= [-1,-1] # todavia no existe
        vd_p_vectorDirector= [0,0]
        for o_array in (self.obstaculos_array_actual):

            ## Grafico la trayectoria de Person Followed, sus últimos 4 pasos previos a la actual:
            j=0
            for pf in self.person_followed_xy_array:
                if(j<(len(self.person_followed_xy_array)-1)):
                    #white
                    if((j < len(self.person_followed_xy_array)-1) and (j == len(self.person_followed_xy_array)-5)): #if(j==4): ##
                        p_white= [pf[0],pf[1]]
                    #light gray
                    if((j < len(self.person_followed_xy_array)-1) and (j == len(self.person_followed_xy_array)-4)): #if(j==3): ##
                        p_lightGray= [pf[0],pf[1]]
                    #light blue
                    if((j < len(self.person_followed_xy_array)-1) and (j == len(self.person_followed_xy_array)-3)): #if(j==2): ##
                        p_lightBlue= [pf[0],pf[1]]
                    #light green
                    if((j < len(self.person_followed_xy_array)-1) and (j == len(self.person_followed_xy_array)-2)): #if(j==1): ##
                        p_lightGreen= [pf[0],pf[1]]
                    j= j+1

            ## Analizo todos los obstáculos
            for o in o_array:

                if(o.obstaculo == "person"): # Si el obstaculo sí es una persona
                    #if((o.angulo_persona_obstaculo == 0) and (o.distancia_persona_obstaculo == 0.0)): #Si person == person_followed
                    if(o.distancia_persona_obstaculo == 0.0): #Si person == person_followed
                        p_green= [o.centro_x_obstaculo,o.centro_y_obstaculo]

                        '''print("p_white: ",p_white)
                        print("p_lightGray: ",p_lightGray)
                        print("p_lightBlue: ",p_lightBlue)
                        print("p_lightGreen: ",p_lightGreen)
                        print("p_green: ",p_green)'''

                        v03= [0,0]
                        v0= [0,0]
                        v1= [0,0]
                        v2= [0,0]
                        v3= [0,0]
                        # Existen los vectores directores?
                        v03_test= Vectors(p_white,p_green)
                        v0_test= Vectors(p_white,p_lightGray)
                        v1_test= Vectors(p_lightGray,p_lightBlue)
                        v2_test= Vectors(p_lightBlue,p_lightGreen)
                        v3_test= Vectors(p_lightGreen,p_green)

                        if(v03_test.existeVectorDirector()):
                            v03= [int(p_green[0]) - int(p_white[0]), int(p_green[1]) - int(p_white[1])]

                        if(v0_test.existeVectorDirector()):
                            v0= [int(p_lightGray[0]) - int(p_white[0]), int(p_lightGray[1]) - int(p_white[1])]

                        if(v1_test.existeVectorDirector()):
                            v1= [int(p_lightBlue[0]) - int(p_lightGray[0]), int(p_lightBlue[1]) - int(p_lightGray[1])]

                        if(v2_test.existeVectorDirector()):
                            v2= [int(p_lightGreen[0]) - int(p_lightBlue[0]), int(p_lightGreen[1]) - int(p_lightBlue[1])]

                        if(v3_test.existeVectorDirector()):
                            v3= [int(p_green[0]) - int(p_lightGreen[0]), int(p_green[1]) - int(p_lightGreen[1])]


                        # Para el calculo del GUI el eje y de los vectores directores debo mult. por -1, para obtener bien el ángulo

                        vd_p_vectorDirector= [v03[0] + v0[0] + v1[0] + v2[0] + v3[0], v03[1] + v0[1] + v1[1] + v2[1] + v3[1]] ## Busco el vector director
                        #print("vd_p_vectorDirector: ",vd_p_vectorDirector)

                        #arco_ancho= 60
                        angulo_persona_arco= int(o.get_angle([1,0],[vd_p_vectorDirector[0],(-1)*vd_p_vectorDirector[1]])) ## corrijo con *(-1) al eje y para la GUI de TKinter
                        angulo_vectorDirector= self.get_angulo_gui(angulo_persona_arco)
                        #print("angulo_vectorDirector: ",angulo_vectorDirector)

        p_personFollowedTrayectoria= [p_white,p_lightGray,p_lightBlue,p_lightGreen,p_green]
        #print("p_personFollowedTrayectoria: ",p_personFollowedTrayectoria)
        return vd_p_vectorDirector,angulo_vectorDirector,p_personFollowedTrayectoria

    def get_angulo_gui(self,angulo):
        angulo_gui= 0
        if(angulo < 0): # 0º<angulos<360º
            angulo_gui= 360 + angulo
        else:
            angulo_gui= angulo

        return angulo_gui
    
