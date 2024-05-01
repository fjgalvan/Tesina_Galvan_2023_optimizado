import numpy as np
import pandas as pd
import os
from objeto_detectado_roi import Objeto_detectado_roi
from geometry_roi import Geometry_Roi


class Perspective_roi:
    
    def __init__(self, M,pts1,pts2):
        self.M = M
        self.pts1 = pts1
        self.pts2= pts2

    def destination(self,u,v):
        d= np.array([u,v,1])
        q1p= self.M.dot(d)

        a=q1p[0]
        b=q1p[1]
        c=q1p[2]

        d=int(a/c)
        e=int(b/c)

        dest= np.array([d,e])

        return dest

    def setTrazabilidad(self,fecha,hora,objeto,confidence,dest_q1, dest_q2, dest_q3, dest_q4,centro_x,centro_y):
        #GUARDO LA INFO EN archivo .csv
        archivo="data/Trazabilidad.csv"

        if(os.path.isfile(archivo) == False):
            #GUARDO LA INFO EN archivo .csv
            csv=open(archivo,'w')
            nombre_columnas= "fecha,hora,objeto,confidence,dest_q1_x,dest_q1_y,dest_q2_x,dest_q2_y,dest_q3_x,dest_q3_y,dest_q4_x,dest_q4_y,centro_x,centro_y\n"
            csv.write(nombre_columnas)
            csv.close()	
        csv=open(archivo,'a')
        ##Ver bien como usar los datos de los df !!!
        filas=str(fecha)+','+str(hora)+","+str(objeto)+","+str(confidence)+","+str(dest_q1[0])+","+str(dest_q1[1])+","+str(dest_q2[0])+","+str(dest_q2[1])+","+str(dest_q3[0])+","+str(dest_q3[1])+","+str(dest_q4[0])+","+str(dest_q4[1])+","+str(centro_x)+","+str(centro_y)+"\n"
        csv.write(filas)
        objeto= Objeto_detectado_roi(str(fecha),str(hora),str(objeto),str(confidence),str(dest_q1[0]),str(dest_q1[1]),str(dest_q2[0]),str(dest_q2[1]),str(dest_q3[0]),str(dest_q3[1]),str(dest_q4[0]),str(dest_q4[1]),str(centro_x),str(centro_y))
        return objeto
    
    def setObstaculos(self,fecha,hora,objeto,centro_x,centro_y,centro_x_old,centro_y_old,centro_x_obstaculo,centro_y_obstaculo,vd_x,vd_y,vd_angulo,vd_distancia):
        #GUARDO LA INFO EN archivo .csv
        archivo="data/Obstaculos.csv"

        csv=open(archivo,'a')
        ##Ver bien como usar los datos de los df !!!
        filas=str(fecha)+','+str(hora)+","+str(objeto)+","+str(centro_x)+","+str(centro_y)+","+str(centro_x_old)+","+str(centro_y_old)+","+str(centro_x_obstaculo)+","+str(centro_y_obstaculo)+","+str(vd_x)+","+str(vd_y)+","+str(vd_angulo)+","+str(vd_distancia)+"\n"
        csv.write(filas)

    def correctionOfPointOutROI(self,dstPoint):
        #Reviso si al proyectar el punto me devuelve un punto que esté fuera del límite de  Pts2

        #Reviso los límites del eje x
        if(dstPoint[0]<0): #si dstPoint(x)<0
            dstPoint[0]= 0
        if(dstPoint[0]>self.pts2[1][0]): #si dstPoint(x)> x_extremoMaximo
            dstPoint[0]= self.pts2[1][0]

        #Reviso los límites del eje y
        if(dstPoint[1]<0): #si dstPoint(y)<0
            dstPoint[1]= 0
        if(dstPoint[1]>self.pts2[2][1]): #si dstPoint(1)> y_extremoMaximo
            dstPoint[1]= self.pts2[2][1]

        return dstPoint

    def get_centro_x_y_old(self):
        #Obtengo primero los centros de la persona del instante previo
        array=[]
        
        datos_Trazabilidad_old=pd.read_csv('data/Trazabilidad.csv')
        df_Trazabilidad_old=pd.DataFrame(datos_Trazabilidad_old)

        ultima_fecha=df_Trazabilidad_old.iloc[len(df_Trazabilidad_old)-1]['fecha']
        ultima_hora=df_Trazabilidad_old.iloc[len(df_Trazabilidad_old)-1]['hora']

        for i in range(len(df_Trazabilidad_old)):
            if(df_Trazabilidad_old.iloc[i]['fecha']== ultima_fecha):
                if(df_Trazabilidad_old.iloc[i]['hora']== ultima_hora):
                    if(df_Trazabilidad_old.iloc[i]['objeto']== 'person'):
                        array.append(df_Trazabilidad_old.iloc[i]['centro_x'])
                        array.append(df_Trazabilidad_old.iloc[i]['centro_y'])
        return array

    def get_objetos_detectados_roi_array(self,w_window,h_window,X0_Y0_imageOut,puntos):
        geo_roi= Geometry_Roi(puntos)
        x_io= int(X0_Y0_imageOut[0])
        y_io= int(X0_Y0_imageOut[1])
        #Falta Validar que pts1, pts2 y M no estén vacios.
        datos=pd.read_csv('data/Objeto_confidence_x_w_y_h_fecha_hora.csv')
        df=pd.DataFrame(datos)

        archivo="data/Trazabilidad.csv"
        array=[]
        array_new=[]
        array_obstaculo=[100,100]
        objeto_detectado_roi_array=[]

        if(os.path.isfile(archivo) != False):
            array= self.get_centro_x_y_old()
            #print("array old centro x y: ", array)

        hayPersonas= False
        
        area_dest= np.zeros((4,2))
        ##detection_id= df.shape[0] -1
        for detection_id in range(df.shape[0]):
            q1_x= df['x'][detection_id] + x_io 
            q1_y= df['y'][detection_id] + df['h'][detection_id]  + y_io

            q2_x= df['x'][detection_id]+ df['w'][detection_id] + x_io  #Faltaba el "+ x_io"
            q2_y= df['y'][detection_id] + df['h'][detection_id] + y_io #Faltaba el "+ y_io"

            '''if(geo_roi.is_in_Area_ROI(q1_x,q1_y)):
                print("El punto ({},{}) se halla en el area Area_ROI.".format(q1_x,q1_y))
            else: 
                print("El punto ({},{}) no se halla en el area Area_ROI.".format(q1_x,q1_y))

            if(geo_roi.is_in_Area_ROI(q2_x,q2_y)):
                print("El punto ({},{}) se halla en el area Area_ROI.".format(q2_x,q2_y))
            else: 
                print("El punto ({},{}) no se halla en el area Area_ROI.".format(q2_x,q2_y))
            '''

            if((geo_roi.is_in_Area_ROI(q1_x,q1_y)) or (geo_roi.is_in_Area_ROI(q2_x,q2_y))):

                #q1=(u1,v1)=(x,y+h)
                u1=df['x'][detection_id] + x_io #### + x_io
                v1=df['y'][detection_id] + df['h'][detection_id] + y_io #### + y_io

                #q2=(u2,v2)=(x+w,y+h)
                u2=u1 + df['w'][detection_id]
                v2=v1

                # M * [u1 v1 1]^t = [x y z] ----> q1'= [x/z  y/z]
                # T[u1 v1]= [x/z y/z] => T(q1)= q1'
                source_q1= np.array([u1,v1])
                dest_q1= self.destination(u1,v1)
                #correction_dest_q1= self.correctionOfPointOutROI(dest_q1)
                dest_q1= self.correctionOfPointOutROI(dest_q1)

                source_q2= np.array([u2,v2])
                dest_q2= self.destination(u2,v2)
                #correction_dest_q2= self.correctionOfPointOutROI(dest_q2)
                dest_q2= self.correctionOfPointOutROI(dest_q2)

                count_error_limit_q1= 0
                if((dest_q1[0] >= w_window) or (dest_q1[0] <= 0)):
                    count_error_limit_q1= count_error_limit_q1 +1
                if((dest_q1[1] >= h_window) or (dest_q1[1] <= 0)):
                    count_error_limit_q1= count_error_limit_q1 +1

                count_error_limit_q2= 0
                if((dest_q2[0] >= w_window) or (dest_q2[0] <= 0)):
                    count_error_limit_q2= count_error_limit_q2 +1
                if((dest_q2[1] >= h_window) or (dest_q2[1] <= 0)):
                    count_error_limit_q2= count_error_limit_q2 +1


                q3x= dest_q2[0]
                q3y= dest_q2[1] - (dest_q2[0] - dest_q1[0])
                dest_q3= np.array([q3x,q3y])
                #correction_dest_q3= self.correctionOfPointOutROI(dest_q3)
                dest_q3= self.correctionOfPointOutROI(dest_q3)

                q4x= dest_q1[0]
                q4y= dest_q2[1] - (dest_q2[0] - dest_q1[0])
                dest_q4= np.array([q4x,q4y])
                #correction_dest_q4= self.correctionOfPointOutROI(dest_q4)
                dest_q4= self.correctionOfPointOutROI(dest_q4)

                area_dest= np.zeros((4,2))
                area_dest[0]= dest_q4
                area_dest[1]= dest_q3
                area_dest[2]= dest_q2
                area_dest[3]= dest_q1

                area_dest = np.array(area_dest).reshape((-1,1,2)).astype(np.int32)

                ##REALIZAR MÁS PRUEBAS DE TODOS LOS CASOS !!!

                ## Crear un dataFrame con el archivo csv de archivo="data/Objeto_confidence_x_w_y_h_fecha_hora.csv"
                #Filtramos la df_SPY y realizamos una agrupacion
                ####df_SPY_Fecha = df_SPY.groupby(['Anio', 'Mes']).mean()[['Minimo', 'Maximo', 'Variacion']]
                aux= int((dest_q2[0] - dest_q1[0])/2)
                centro_x= int( ((dest_q2[0] - dest_q1[0])/2) + dest_q1[0] )
                #centro_y= int( ((dest_q2[0] - dest_q3[0])/2) + dest_q3[0] )
                centro_y= int(dest_q2[1] - int(aux/4) )

                guardar= True
                if((count_error_limit_q1>0) and (count_error_limit_q2>0)):
                    guardar= False

                if((df['cantPersonas'][0] >0) and (guardar)): #Reviso si se detectó al menos 1 personan sino no lo persisto
                    hayPersonas= True
                    objeto= self.setTrazabilidad(df['fecha'][detection_id],df['hora'][detection_id],df['objeto'][detection_id],df['confidence'][detection_id],dest_q1,dest_q2,dest_q3,dest_q4,centro_x,centro_y)
                    objeto_detectado_roi_array.append(objeto)

                    if(df['objeto'][detection_id] == 'person'):
                        if(len(array)==0):
                            array.append(centro_x)
                            array.append(centro_y)
                        
                        array_new.append(centro_x)
                        array_new.append(centro_y)
                    else:
                        array_obstaculo.append(centro_x)
                        array_obstaculo.append(centro_y)
                        
                detection_id= detection_id+1

        return objeto_detectado_roi_array