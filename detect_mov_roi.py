import numpy as np
import cv2

class Detect_mov_roi:
    
    def __init__(self, frame,fgbg,kernel):#Array [*, *]
        self.frame = frame
        self.fgbg = fgbg
        self.kernel = kernel
    

    ##### detectar_mov_area - inicio #####
    def getAreaToDetectMove(self,frame, gray, area_pts):

        imAux = np.zeros(shape=(self.frame.shape[:2]), dtype=np.uint8)
        imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
        image_area = cv2.bitwise_and(gray, gray, mask=imAux)

        return image_area
        
    def getMoveDetectioInBinaryImage(self,image_area):
        fgmask = self.fgbg.apply(image_area)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        fgmask = cv2.dilate(fgmask, None, iterations=2) 

        return fgmask

'''    def getRectMoveDetection(self,frame,color,texto_estado, fgmask):
        cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #En Opencv 4.1.0 es [0]
        #cv2.findContours(image, mode, method)
        #OpenCV 3: image, contours, hierarchy
        #OpenCV 4: contours, hierarchy

        for cnt in cnts:
            if cv2.contourArea(cnt) >= 500:
                x, y, w, h = cv2.boundingRect(cnt)
                #rectangulos blancos donde hay movimientos
                #cv2.rectangle(self.frame, (x,y), (x+w, y+h),(255,255,255), 2) #(0,255,0)
                texto_estado = "Hay Movimiento en ROI!"
                color = (0, 0, 255)
        
        return texto_estado, color

    def drawRect(self,frame):
        cv2.rectangle(self.frame,(0,0),(self.frame.shape[1],40),(0,0,0),-1)
        color = (0, 255, 0)
        texto_estado = "No hay movimientos en ROI"
        return texto_estado, color
''' 
##### detectar_mov_area - fin #####