from vectors import Vectors
from prediction import Prediction
from recalculating import Recalculating

class Graficos_tk:
    def __init__(self,p_personFollowedTrayectoria):
        self.p_personFollowedTrayectoria= p_personFollowedTrayectoria

    def get_colorsPersonFollowedTrayectory(self):
        colorsPFTrayectory_array= ["white","light gray","light blue","light green","green"]
        return colorsPFTrayectory_array

    def peligroObstaculos(self,obstaculos_array_actual,anguloArcConoRojo,radioArcoConoRojo,vd_p_vectorDirector,g,person_followed_array):
        points_oval_array_array= []
        msg_array= []
        for o_array in (obstaculos_array_actual):
            nivel_danger_array= []
            i=0
            distancia_recorrida_persona_follow= 1 #0
            saltosDanger= 3 #1
            distanceDanger= int(saltosDanger*distancia_recorrida_persona_follow)
            arco_ancho= anguloArcConoRojo
            distanceDanger= arco_ancho

            ## Analizo todos los obstáculos
            for o in o_array:
                pred= Prediction([int(o.centro_x_persona_old),int(o.centro_y_persona_old)],[int(o.centro_x_persona),int(o.centro_y_persona)])
                danger= ""
                nivel_danger= 0
                if(o.obstaculo == "person"): # Si el obstaculo sí es una persona
                    if(o.distancia_persona_obstaculo != 0.0): #Si person == person_followed
                        distancia_recorrida_persona_follow= o.get_distance([int(o.centro_x_persona),int(o.centro_y_persona)],[int(o.centro_x_persona_old),int(o.centro_y_persona_old)])
                        distanceDanger= radioArcoConoRojo
                        v= Vectors([int(o.centro_x_persona_old),int(o.centro_y_persona_old)],[int(o.centro_x_persona),int(o.centro_y_persona)])
                        vd_pf_vs_obst= v.getVectorDirector([int(o.centro_x_persona_old),int(o.centro_y_persona_old)],[int(o.centro_x_obstaculo),int(o.centro_y_obstaculo)])
                        vd_pfPromedio= vd_p_vectorDirector
                        angulo_persona_obstaculo= v.getAngle(vd_pf_vs_obst,vd_pfPromedio) #(inicio,destino) # Actualizo !!!!
                        res_pred_getDangerPrediction= pred.getDangerPrediction(angulo_persona_obstaculo,int(o.distancia_persona_obstaculo),distanceDanger)
                        danger= res_pred_getDangerPrediction[0]
                        nivel_danger= int(res_pred_getDangerPrediction[1])
                        nivel_danger_array.append(nivel_danger)
                        points_oval_array= g.get_X0_Y0_X1_Y1_area(o.centro_x_obstaculo,o.centro_y_obstaculo,10)
                        points_oval_array_array.append(points_oval_array)
                        ####g.draw_oval(points_oval_array[0],points_oval_array[1],points_oval_array[2],points_oval_array[3],1,"orange")

                '''else: # Si el obstaculo no es una persona
                    points_oval_array= g.get_X0_Y0_X1_Y1_area(o.centro_x_obstaculo,o.centro_y_obstaculo,10)
                    #g.draw_oval(points_oval_array[0],points_oval_array[1],points_oval_array[2],points_oval_array[3],1,"red") #DESCARTADO POR AHORA el ver a no personas!!
                    #distanceDanger= distancia_recorrida_persona_follow*saltosDanger
                    distanceDanger= radioArcoConoRojo
                    danger,nivel_danger= pred.getDangerPrediction(o.angulo_persona_obstaculo,o.distancia_persona_obstaculo,distanceDanger)
                    nivel_danger_array.append(nivel_danger)'''
                i= i+1

            #(vd_persona_follow, angulo_persona_follow, obstaculos_array)
            if(len(person_followed_array)>0):
                recalculando= Recalculating(nivel_danger_array)
                girar_angulos= recalculando.girar_angulo_director()
                if(girar_angulos == 0):
                    msg= "Sin desvios"
                    print(msg)
                else:
                    msg= ""
                    if(girar_angulos < 0):
                        giro= int(-1*girar_angulos)
                        msg= "Gire ",giro,"º hacia la derecha!"
                        print(msg)
                    else:
                        msg= "Gire ", girar_angulos,"º hacia la izquierda!"
                        print(msg)
                    #g.draw_text(str(msg))
                msg_array.append(msg)

        return points_oval_array_array, msg_array
