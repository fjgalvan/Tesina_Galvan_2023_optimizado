import cv2
import imutils

for i in range(290):
    imagen1 = cv2.imread('images/fondoFrameDst_'+str(i)+".jpg")
    imagen2 = cv2.imread('images/img_tkinter_'+str(i)+".jpg")
    imagen3 = cv2.imread('images/object-detection_'+str(i)+".jpg")
    #imagen3 = imutils.resize(imagen3, width=236)
    #imagen3 = imutils.resize(imagen3, height=220)
    imagen3 = imutils.resize(imagen3, width=494)


    # Concatenando una imagen arriba y 3 abajo
    ##concat_h_2imagenes = cv2.hconcat([imagen1, imagen2])
    ##concat_v_1sobre2 = cv2.vconcat([imagen3, concat_h_2imagenes])

    #concat_v_1sobre2= cv2.vconcat([imagen1, imagen2])
    #concat_h_2imagenes = cv2.hconcat([imagen3, concat_v_1sobre2])
    #final_concat= concat_h_2imagenes

    concat_h= cv2.hconcat([imagen1, imagen2])
    concat_v= cv2.vconcat([concat_h, imagen3])
    final_concat= concat_v


    final_concat_num= "images/concat_"+str(i)+".jpg"
    cv2.imwrite(final_concat_num, final_concat)

    #cv2.imshow('final_concat', final_concat)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''
imagen1 = cv2.imread('images/fondoFrameDst_0.jpg')
imagen2 = cv2.imread('images/img_tkinter_0.jpg')
imagen3 = cv2.imread('images/object-detection_0.jpg')
imagen3 = imutils.resize(imagen3, width=236)

# Concatenando una imagen arriba y 3 abajo
concat_h_2imagenes = cv2.hconcat([imagen1, imagen2])
concat_v_1sobre2 = cv2.vconcat([imagen3, concat_h_2imagenes])

cv2.imshow('concat_v_1sobre2', concat_v_1sobre2)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''