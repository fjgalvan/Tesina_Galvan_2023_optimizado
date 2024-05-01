# $ source "c:/Users/Usuario/Desktop/Tesina 2022/ProyectoTesina/cv/Scripts/activate"
## $ source cvTesina2/Scripts/activate

# CARGAR YOLO + COCO
# BUSCAR LOS FRAMES ENUMERADOS
# MIENTRAS QUEDEN FRAMES SIN ANALIZAR:
    ## CARGAR UN FRAME
    ## DETECTAR EL ROI
    ## ANALIZAR CON YOLO + COCO CADA IMAGEN DEL ROI
    ## BUSCAR A PERSON FOLLOWED
    ## GUARDAR TRAZABILIDAD DE PERSON FOLLOWED
    ## ANALIZAR PELIGRO DE COLISIÓN
        ### RECOMENDAR DESVÍO DE MÁS SEGURO
    ## CARGAR DATOS EN UN MAPA VIRTUAL (con TKinter)


import cv2
import numpy as np
from detect_mov_roi import Detect_mov_roi 
from perspective_roi import Perspective_roi
from gui_interface import Gui_interface
from yolo_class import Yolo_class
from perspective_video import Perspective_video
from vectorDirector import VectorDirector
from buscarPersonFollowed import BuscarPersonFollowed
from trayectorias_de_obstaculos import Trayectorias_de_obstaculos
from graficos_tk import Graficos_tk
from trayectoria_de_personas import Trayectoria_De_Personas

if __name__ == '__main__':
    puntos = []
    puntos= [[125,45],[300,30],[145,160],[390,120]] #asia
    margen= 0 #20 para aeropuerto
    X0_Y0_imageOut= [0,0]  #[60-margen,300-margen]
    pv= Perspective_video(puntos)
    yolo_coco= Yolo_class()
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG() # detectar_mov_area
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)) # detectar_mov_area
    M= np.zeros((3,3))
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame',pv.clics)
    pts1 = np.float32([[0,0], [0,0], [0,0], [0,0]])
    pts2 = np.float32([[0,0], [0,0], [0,0], [0,0]])
    area_pts= np.float32([[0,0], [0,0], [0,0], [0,0]])#np.zeros((4,2))
    area_pts1= np.float32([[0,0], [0,0], [0,0], [0,0]])#np.zeros((4,2))
    Contador_ROI= 0
    objetos_detectados_roi_array_array=[]
    person_followed_array= []
    centro_xy_old_array= []
    obstaculos_array_array= []
    w_window= 0
    h_window= 0
    person_followed_xy_array= []
    num_image= 0
    resize_frame= 3#3#3
    area_mapaVirtual= 0
    vd_p= [0,0]
    vd_p_vectorDirector= [0,0]
    angulo_vectorDirector= 0
    cont = 121 #13 #4 #0
    path = 'videos/frames_asia/' #'videos/frames_GenteCaminando/' # 'videos/frames_aeropuerto/' # 1658 frames
    anguloPerspectiva= 0#9 #9,20689
    anguloIncialArcCanvas= 15
    anguloArcConoRojo= 30
    radioArcoConoRojo= int(2*anguloArcConoRojo)
    obstaculos_position_array_array= []
    personas_Obst_y_PF_historial_array_array= []
    trayectorias_de_personas_array= []
    
    #Trayectorias Historicos !!!
    personFollowed_trayectoria_array= []
    obstaculos_trayectorias_array_array= []

    while True:
        count_person_followed=0
        obstaculos_array_actual= []
        pérsonas_historial_array= []

        vd_p_promedio= vd_p

        ### --------------- READ THE IMAGE ---------------
        image = cv2.imread(path + 'IMG_%04d.jpg' % cont)
        cont += 1
        height, width, _ = image.shape
        frame= image
        height, width = frame.shape[:2]
        frame = cv2.resize(frame, (int(width/resize_frame), int(height/resize_frame)))
        pv.dibujando_puntos(puntos,frame)
        frameDst= frame
        ### --------------- DETECTION MOVE ---------------
        mov= Detect_mov_roi(frame,fgbg,kernel)#Objeto
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) ##mov_

        if(Contador_ROI == 1):
            area_pts1= np.array(pts1).reshape((-1,1,2)).astype(np.int32)

        if(Contador_ROI >= 1):
            #OBS: El area es en sentido horario!
            area_pts[0]= area_pts1[0]
            area_pts[1]= area_pts1[1]
            area_pts[2]= area_pts1[3]
            area_pts[3]= area_pts1[2]
            area_pts = np.array(area_pts).reshape((-1,1,2)).astype(np.int32)
            image_area= mov.getAreaToDetectMove(frame, gray, area_pts) ##mov_
            fgmask= mov.getMoveDetectioInBinaryImage(image_area) ##mov_
            cv2.drawContours(frame, [area_pts], -1, (0,255,0), 2)

        if len(puntos) == 4:
            Contador_ROI= Contador_ROI+1
            pv.uniendo4puntos(puntos,frame)
            #pts1 y pts2 deben de ser cuadrados !!!
            pts1 = np.float32([puntos])
            proporcional_x= 1# GenteCaminando
            proporcional_y= 1#1 GenteCaminando
            divido= 1 #2
            max_roi_w= int((pv.maxWidth(pts1) -1)/divido)
            pts2 = np.float32([[0,0], [max_roi_w,0], [0,int((max_roi_w)/proporcional_x)], [max_roi_w,int((max_roi_w)/proporcional_x)]])
            M = cv2.getPerspectiveTransform(pts1,pts2)
            dst = cv2.warpPerspective(frame, M, (max_roi_w,int((max_roi_w)/proporcional_x))) #aeropuerto
            frameDst= dst
            w_window= max_roi_w
            h_window= int((max_roi_w)/proporcional_x)
            area_mapaVirtual= int(w_window)*int(h_window)
            if Contador_ROI==1:
                pv.persist_data_roi(M,pts1,pts2)
            cv2.imshow('dst', dst)
        cv2.imshow('frame',frame)
        k = cv2.waitKey(600) & 0xFF  ##(200)  ##(1)
        if k == ord('n'): # Limpiar el contenido de la frame
            puntos = []

        ### --------------- DETECTIONS AND PREDICTIONS WITH YOLO + COCO ---------------
        #if k == ord('p'): # Captura de una imagen 
        if(frame is not None):
            objeto_detectado_roi_person_array= []

            fondo_num= "images/fondo_"+str(num_image)+".jpg"
            cv2.imwrite(fondo_num, frame)
            fondoFrameDst_num= "images/fondoFrameDst_"+str(num_image)+".jpg"
            cv2.imwrite(fondoFrameDst_num, frameDst)
            image_fondo = cv2.imread(fondo_num) #Recortar una imagen

            ## Analizo la imagen fondo.jpg con Deep Learning: ##
            yolo_coco.readImage_and_prediction(fondo_num,num_image) #para gente caminando no hay recorte
            yolo_coco.exit()
            print("Contador_ROI: ",Contador_ROI)
            print("Contador_img_tkinter: ",Contador_ROI-1)
            if(Contador_ROI >= 1): #Busco los puntos q1, q2, q1' y q2'.
                pr= Perspective_roi(M,pts1,pts2) #Objeto
                objeto_detectado_roi_array= pr.get_objetos_detectados_roi_array(w_window,h_window,X0_Y0_imageOut,puntos)
                objetos_detectados_roi_array_array.append(objeto_detectado_roi_array)

                ## BUSCAR PERSON FOLLOWED ##
                peFo= BuscarPersonFollowed(objeto_detectado_roi_array)
                res_peFo_getPersonFollowed= peFo.getPersonFollowed(person_followed_array,centro_xy_old_array,person_followed_xy_array,objeto_detectado_roi_array,obstaculos_array_actual,pv,vd_p_promedio,obstaculos_array_array,objeto_detectado_roi_person_array,count_person_followed,vd_p,area_mapaVirtual)
                person_followed_xy_array= res_peFo_getPersonFollowed[0][0]
                obstaculos_array_actual= res_peFo_getPersonFollowed[0][1]
                print("person_followed_xy_array: ",person_followed_xy_array)

                ## BUSCAR DIRECCIÓN Y SENTIDO PROMEDIO DE PERSON FOLLOWED ##
                vd= VectorDirector(obstaculos_array_actual,person_followed_xy_array)
                res_vd_get_vd_promedio= vd.get_vd_promedio()
                vd_p_vectorDirector= res_vd_get_vd_promedio[0]
                angulo_vectorDirector= res_vd_get_vd_promedio[1]
                p_personFollowedTrayectoria= res_vd_get_vd_promedio[2]

                ## Guardar la trazabilidad de todos los Obstáculos ##
                tdo= Trayectorias_de_obstaculos(obstaculos_array_actual)
                obstaculos_position_array_array= tdo.get_PuntosDeObstaculos(obstaculos_position_array_array)
                print("obstaculos_position_array_array: ", obstaculos_position_array_array)
                si_hayCambiosDeCantidadDeObstaculos= tdo.si_HayPerdidasDeCantidadDeObstaculos(obstaculos_position_array_array)
                print("si_hayCambiosDeCantidadDeObstaculos: ",si_hayCambiosDeCantidadDeObstaculos)
                si_HayMenosObstáculosActual= tdo.si_HayMenosObstáculosActual(obstaculos_position_array_array)
                print("si_HayMenosObstáculosActual: ",si_HayMenosObstáculosActual)

                ##Obtengo el listado de todas las personas detectadas
                obstaculos_position_array= tdo.get_PuntosDeObstaculos_Actual(obstaculos_position_array_array)
                print("obstaculos_position_array: ",obstaculos_position_array)
                position= len(person_followed_xy_array)-1
                pf_xy= person_followed_xy_array[position]
                obstaculos_position_array.append(pf_xy)
                personas_Obst_y_PF_historial_array_array.append(obstaculos_position_array)
                print("personas_Obst_y_PF_historial_array_array: ",personas_Obst_y_PF_historial_array_array)

                ## Trayectorias - inicio ##
                tdp= Trayectoria_De_Personas(personas_Obst_y_PF_historial_array_array) ##, trayectorias_de_personas_array)
                distancia_array_array= tdp.get_distancias()
                print("distancia_array_array: ",distancia_array_array)
                isAceptable_array_array= tdp.isDistanciaAceptable(distancia_array_array, 10)
                print("isAceptable_array_array: ",isAceptable_array_array)

                #lmv= LimitesMapaVirtual(w_window,h_window)
                areNewEnElExtremoROI_array= tdp.limitesExtremosDelMapa(w_window,h_window)######################## jsjhshshvhxsvxn
                print("areNewEnElExtremoROI_array: ",areNewEnElExtremoROI_array)
                areNewEnElCentroROI_array= tdp.limitesCentroDelMapa(w_window,h_window)######################## jsjhshshvhxsvxn
                print("areNewEnElCentroROI_array: ",areNewEnElCentroROI_array)

                ## Trayectorias - fin ##

                ## Grafico ##
                g= Gui_interface(w_window,h_window)
                g_tk= Graficos_tk(p_personFollowedTrayectoria)
                colorsPFTrayectory_array= g_tk.get_colorsPersonFollowedTrayectory()
                aux_colors=0
                for pf_trayectoria in p_personFollowedTrayectoria:
                    if(pf_trayectoria != [-1,-1]):
                        points_oval_array= g.get_X0_Y0_X1_Y1_area(pf_trayectoria[0],pf_trayectoria[1],10)
                        g.draw_oval(points_oval_array[0],points_oval_array[1],points_oval_array[2],points_oval_array[3],1,colorsPFTrayectory_array[aux_colors])
                    aux_colors= aux_colors+1

                ## CONO ROJO Person Followed ##
                points_arc_array= g.get_X0_Y0_X1_Y1_area(p_personFollowedTrayectoria[4][0],p_personFollowedTrayectoria[4][1],radioArcoConoRojo)
                angulo_cono_inicio= angulo_vectorDirector - anguloIncialArcCanvas + anguloPerspectiva
                g.draw_arc(points_arc_array[0],points_arc_array[1],points_arc_array[2],points_arc_array[3],angulo_cono_inicio,anguloArcConoRojo,"red") #angulo_gui-15,

                ## Analizo todos los obstáculos ##
                res_peligroObstaculos= g_tk.peligroObstaculos(obstaculos_array_actual,anguloArcConoRojo,radioArcoConoRojo,vd_p_vectorDirector,g,person_followed_array)
                points_oval_array_array= res_peligroObstaculos[0]
                msg_array= res_peligroObstaculos[1]
                for points_oval_array in points_oval_array_array:
                    g.draw_oval(points_oval_array[0],points_oval_array[1],points_oval_array[2],points_oval_array[3],1,"orange")
                for msg in msg_array:
                    if (msg != "Sin desvios"):
                        g.draw_text(str(msg))

                ## GUI ##
                g.window.after(600, g.window.destroy)
                img_tkinter_num= "images/img_tkinter_"+str(num_image)+".jpg"
                g.saveImage(img_tkinter_num)
                g.saveImage(img_tkinter_num)

                g.saveImage(img_tkinter_num)
                g.saveImage(img_tkinter_num)
                g.saveImage(img_tkinter_num)
                g.saveImage(img_tkinter_num)
                g.saveImage(img_tkinter_num)
                g.saveImage(img_tkinter_num)
                g.saveImage(img_tkinter_num)
                g.saveImage(img_tkinter_num)

                g.window.mainloop()
                num_image= num_image +1
        elif k == 27:
            break
    cv2.destroyAllWindows()