import cv2

capture = cv2.VideoCapture('videos/Asia_GenteCaminando.mp4') #cv2.VideoCapture('videos/aeropuerto.mp4') #('videos/GenteCaminando.mp4')
cont = 0
path = 'videos/frames_asia/' #'videos/frames_GenteCaminando/'  # 'videos/frames_aeropuerto/' # 1658 frames

while (capture.isOpened()):
    ret, frame = capture.read()
    if (ret == True):
        cv2.imwrite(path + 'IMG_%04d.jpg' % cont, frame)
        cont += 1
        if (cv2.waitKey(1) == ord('s')):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()