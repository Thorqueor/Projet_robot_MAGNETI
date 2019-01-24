import numpy as np
import cv2
import cv2.aruco as aruco
ID=1#ID du marqueur !

'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''
files=""
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
squareLength = 40   # Here, our measurement unit is centimetre.
markerLength = 30   # Here, our measurement unit is centimetre.
board = aruco.CharucoBoard_create(5, 7, squareLength, markerLength, aruco_dict)
for i in range(12):
# second parameter is id number
# last parameter is total image size
    img = aruco.drawMarker(aruco_dict, i, 125)
   # BBB = board.draw((200*3,200*3))
    files="ID"+str(i)+".jpg"
    cv2.imwrite(files, img)
   # cv2.imwrite("test.jpg",board)

cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
