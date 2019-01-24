import numpy as np
import cv2
import cv2.aruco as aruco
import glob
import yaml

class Camera:

#fonction deplacement

	def __init__(self,tailleBras,idOrigine,iOutils):
		self.tailleBras = tailleBras
		self.idOrigine = idOrigine
		self.iOutils = iOutils
		self.listPos = []

	def detectARUCO(self):
		i=0
		aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
		parameters = aruco.DetectorParameters_create()
		lists=[]
		idd=""

		cv_file = cv2.FileStorage("../Calibration/calib_images/Data.yaml", cv2.FILE_STORAGE_READ)

		#note we also have to specify the type to retrieve other wise we only get a
		# FileNode object back instead of a matrix
		camera_matrix = cv_file.getNode("camera_matrix").mat()
		dist_matrix = cv_file.getNode("dist_coeff").mat()

		cap = cv2.VideoCapture(0)
		# termination criteria
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
		# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
		objp = np.zeros((6*7,3), np.float32)
		objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
		# Arrays to store object points and image points from all the images.
		objpoints = [] # 3d point in real world space
		imgpoints = [] # 2d points in image plane.
		images = glob.glob('../Calibration/calib_images/*.jpg')

		for fname in images:
		    img = cv2.imread(fname)
		    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		    # Find the chess board corners
		    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
		    # If found, add object points, image points (after refining them)

		    if ret == True:
		        objpoints.append(objp)
		        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		        imgpoints.append(corners2)
		        # Draw and display the corners
		        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)

		ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)


		while (i<25):
			# print(i)
			ide=""
			ret, frame = cap.read()
			# operations on the frame come here
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			#lists of ids and the corners beloning to each id
			corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
			font = cv2.FONT_HERSHEY_SIMPLEX #font for displaying text (below)
			if np.all(ids != None):
				rvec, tvec,_ = aruco.estimatePoseSingleMarkers(corners[0], 0.05, mtx, dist) #Estimate pose of each marker and return the values rvet and tvec---different from camera coefficients
				(rvec-tvec).any() # get rid of that nasty numpy value array error
				aruco.drawAxis(frame, mtx, dist, rvec[0], tvec[0], 0.1) #Draw Axis
				aruco.drawDetectedMarkers(frame, corners) #Draw A square around the markers
				###### DRAW ID #####
				cv2.putText(frame, "Id: " + str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
				# Display the resulting frame
				idd=str(ids)
				# print ("___________> ids = ",ids)
				for i in range(len(idd)):
					if idd[i] != "[" and idd[i]!="]" and idd[i] !="\n" and idd[i] !=" ":
						if idd[i+1] != "[" and idd[i+1]!="]" and idd[i+1] !="\n" and idd[i+1] !=" ":
							ide=str(idd[i])+str(idd[i+1])
							if int(ide) not in lists:
								lists.append(int(ide))
								if int(idd[i]) not in lists and ide=="":
									lists.append(int(idd[i]))
									# print("")
			cv2.imshow('frame',frame)
			i=i+1

		lists.sort()
		cap.release()
		cv2.destroyAllWindows()

		return lists


	def CalcDeplacementVert(self,sens):
		self.listePos.append([0,sens * self.tailleBras,0])

	def CalcDeplacementHor(self,sens):
		self.listePos.append([sens * self.tailleBras,0,0])


	def TestMarqueur(self,listeM):
		for i in range(len(listeM)):
			if (listeM[i]==self.iOutils):
				return True
		return False

	def Deplacement(self):


		listeID = self.detectARUCO()
		Test = True

		while(Test == True):
			if(self.TestMarqueur(listeID)== True):
				pFinal = (self.iOutils - self.idOrigine)
				if(pFinal//10 != 0):
					if(pFinal//10 > 0):
						self.CalcDeplacementVert(1)
						self.idOrigine = self.idOrigine + 10
					if(pFinal//10 < 0):
						self.CalcDeplacementVert(-1)
						self.idOrigine = self.idOrigine - 10
				if(pFinal%10 !=0):
					if(pFinal%10 > 0):
						self.CalcDeplacementVert(1)
						self.idOrigine = self.idOrigine + 1
					if(pFinal%10 < 0):
						self.CalcDeplacementVert(-1)
						self.idOrigine = self.idOrigine - 1
				if(self.idOrigine == self.iOutils):
					Test = False
			else:
				Test=False
