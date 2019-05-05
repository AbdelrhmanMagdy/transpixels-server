import pytesseract
import cv2
import numpy as np

def run(path):
    img = cv2.imread(path)

    paper = img.copy()
    x = 200
    condition = np.bitwise_or(paper[:,:,0] < x, paper[:,:,1] < x, paper[:,:,2] < x)
    paper[condition] = 0
    paper[np.invert(condition)] = 255
    gray = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(gray,(0,0),(gray.shape[1],gray.shape[0]),0,100)

    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((10,10),np.uint8)
    kernel3 = np.ones((15,15),np.uint8)

    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel2) 


    bounds = cv2.findNonZero(closing)
    test = closing[np.amin(bounds[:,0,1]):np.amax(bounds[:,0,1]), np.amin(bounds[:,0,0]):np.amax(bounds[:,0,0])]

    finalisa2 = cv2.cvtColor(test,cv2.COLOR_GRAY2RGB)
    cv2.rectangle(finalisa2,(0,0),(finalisa2.shape[1],finalisa2.shape[0]),(255,255,255),500)


    return pytesseract.image_to_string(finalisa2)
