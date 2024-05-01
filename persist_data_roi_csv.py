import numpy as np
import cv2

class Persist_data_roi_csv:
    
    def __init__(self, archivo,nombre_columnas,modo_open):
        self.archivo = archivo
        self.nombre_columnas = nombre_columnas
        self.modo_open= modo_open

    def persist_pts1(self,pts1):
        csv=open(self.archivo,self.modo_open)
        nombre_columnas= self.nombre_columnas
        filas=str(pts1[0][0][0])+","+str(pts1[0][0][1])+","+str(pts1[0][1][0])+","+str(pts1[0][1][1])+","+str(pts1[0][2][0])+","+str(pts1[0][2][1])+","+str(pts1[0][3][0])+","+str(pts1[0][3][1])+"\n"
        csv.write(nombre_columnas)
        csv.write(filas)
        csv.close()

    def persist_pts2(self,pts2):
        csv=open(self.archivo,self.modo_open)
        nombre_columnas= self.nombre_columnas
        filas=str(pts2[0][0])+","+str(pts2[0][1])+","+str(pts2[1][0])+","+str(pts2[1][1])+","+str(pts2[2][0])+","+str(pts2[2][1])+","+str(pts2[3][0])+","+str(pts2[3][1])+"\n"
        csv.write(nombre_columnas)
        csv.write(filas)
        csv.close()

    def persistirDatosM(self,M):
        csv=open(self.archivo,self.modo_open)
        nombre_columnas= self.nombre_columnas
        csv.write(nombre_columnas)

        filas0=str(M[0][0])+","+str(M[0][1])+","+str(M[0][2])+"\n"
        csv.write(filas0)

        filas1=str(M[1][0])+","+str(M[1][1])+","+str(M[1][2])+"\n"
        csv.write(filas1)

        filas2=str(M[2][0])+","+str(M[2][1])+","+str(M[2][2])+"\n"
        csv.write(filas2)

        csv.close()