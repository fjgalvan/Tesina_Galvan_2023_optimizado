import cv2
import numpy as np
import time

class Yolo_class:
    
    def __init__(self):
        # --------------- READ DNN MODEL ---------------
        # Model configuration
        self.config = "model/yolov3.cfg"
        # Weights
        self.weights = "model/yolov3.weights"
        # Labels
        self.LABELS = open("model/coco.names").read().split("\n")
        #print(LABELS, len(LABELS))
        self.colors = np.random.randint(0, 255, size=(len(self.LABELS), 3), dtype="uint8")
        #print("colors.shape:", colors.shape)
        self.confidence= 0.5 #0.05 #minimum probability to filter weak detections
        self.threshold= 0.3 #0.3 #threshold when applyong non-maxima suppression
        # Load model, load our YOLO object detector trained on COCO dataset (80 classes)
        print("[INFO] loading YOLO from disk...")
        self.net = cv2.dnn.readNetFromDarknet(self.config, self.weights)

    def create_Objeto_confidence_x_w_y_h_fecha_hora_csv(self,path_file):
        #GUARDO LA INFO EN archivo .csv
        archivo= path_file
        #GUARDO LA INFO EN archivo .csv
        csv=open(archivo,'w')
        nombre_columnas= "objeto,confidence,x,w,y,h,fecha,hora,cantPersonas\n"
        csv.write(nombre_columnas)
        csv.close()

    def save_Objeto_confidence_x_w_y_h_fecha_hora_csv(self,path_file,object,confidence,x,w,y,h,fecha,hora,cantPersonas):
        csv=open(path_file,'a')
        filas=str(object)+","+str(confidence)+','+str(x)+","+str(w)+","+str(y)+","+str(h)+","+fecha+","+hora+","+str(cantPersonas)+"\n"
        csv.write(filas)

    def exit(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def readImage_and_prediction(self,image_path,num_image):
        # --------------- READ THE IMAGE AND PREPROCESSING ---------------
        image = cv2.imread(image_path) #("Images/imagen_0005.jpg")
        height, width, _ = image.shape
        # Create a blob
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                    swapRB=True, crop=False)   ### VEEEEER! (416,416) => (ANCHO * ALTO)  es lo que la red espera!
        #print("blob.shape:", blob.shape)
        # --------------- DETECTIONS AND PREDICTIONS ---------------
        ln = self.net.getLayerNames()
        #print("ln:", ln)
        #ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()] 
        ln = [ln[i - 1] for i in self.net.getUnconnectedOutLayers()] #original
        #print("ln:", ln)
        self.net.setInput(blob)
        start = time.time()
        outputs = self.net.forward(ln)
        end = time.time()
        #print("outputs:", outputs)
        # show timing information on YOLO
        print("\n\n")
        print("[INFO] YOLO took {:.6f} seconds".format(end - start))

        boxes = []
        confidences = []
        classIDs = []
        for output in outputs:
            for detection in output:
                #print("detection:", detection)
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > self.confidence: #0.5
                    #print("detection:", detection)
                    #print("classID:", classID)
                    box = detection[:4] * np.array([width, height, width, height])
                    #print("box:", box)
                    (x_center, y_center, w, h) = box.astype("int")
                    #print((x_center, y_center, w, h))
                    x = int(x_center - (w / 2))
                    y = int(y_center - (h / 2))
                    #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        # apply non-maxima suppression to suppress weak, overlapping bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence, self.threshold) #, 0.5, 0.5)
        #print("idxs:", idxs)

        # ensure at least one detection exists
        fecha=str(time.strftime("%d/%m/%y"))
        hora=str(time.strftime("%H:%M:%S"))
        cantPersonas=int(0)
        probaPersonas=float(0.0)
        path_file="data/Objeto_confidence_x_w_y_h_fecha_hora.csv"

        if len(idxs) == 0: #Guardo data vacio.
            self.create_Objeto_confidence_x_w_y_h_fecha_hora_csv(path_file)

        if len(idxs) > 0:
            self.create_Objeto_confidence_x_w_y_h_fecha_hora_csv(path_file)
            for i in idxs:
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = self.colors[classIDs[i]].tolist()
                text = "{}: {:.3f}".format(self.LABELS[classIDs[i]], confidences[i])
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, color, 2)
                #print("Objeto: ",self.LABELS[classIDs[i]]," | confidence:",confidences[i], " | (w:",w, "h:",h, ")-(x:",x, "y:",y,")")
                if self.LABELS[classIDs[i]]== "person":
                    cantPersonas= cantPersonas+1
                    probaPersonas= probaPersonas+ float(confidences[i])

                self.save_Objeto_confidence_x_w_y_h_fecha_hora_csv(path_file,str(self.LABELS[classIDs[i]]),str(confidences[i]),x,w,y,h,fecha,hora,cantPersonas)

        #cv2.imshow("Image", image)
        #cv2.waitKey(0)#(0)
        path_objectDetection= "images/object-detection_"+str(num_image)+".jpg"
        cv2.imwrite(path_objectDetection, image)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    y= Yolo_class()
    y.readImage_and_prediction("extras/Images/soccer.jpg")
    y.readImage_and_prediction("images/fondo.jpg")
    y.readImage_and_prediction("extras/Images/soccer.jpg")
    y.readImage_and_prediction("images/fondo.jpg")