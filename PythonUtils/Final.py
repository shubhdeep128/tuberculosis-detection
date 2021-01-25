import cv2
import numpy as np 

drawing=False # true if mouse is pressed
mode=True # if True, draw rectangle. Press 'm' to toggle to curve

# mouse callback function
x =[]
y =[]
def crop_image(event,former_x,former_y,flags,param):
    global current_former_x,current_former_y,drawing, mode

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        current_former_x,current_former_y=former_x,former_y
        x.append(current_former_x)
        y.append(current_former_y)


    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            if mode==True:
                cv2.line(resized,(current_former_x,current_former_y),(former_x,former_y),(255,0,0),5)
                current_former_x = former_x
                current_former_y = former_y
                x.append(current_former_x)
                y.append(current_former_y)

                #print former_x,former_y
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode==True:
            cv2.line(resized,(current_former_x,current_former_y),(former_x,former_y),(255,0,0),1)
            current_former_x = former_x
            current_former_y = former_y
            x.append(current_former_x)
            y.append(current_former_y)
    return former_x,former_y    

cs = []
def mousecallback(event,x,y,flags ,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print("click")
        for i in range(len(contours)):
            r = cv2.pointPolygonTest(contours[i],(x,y),False)
            if r>0:
                print("in")
                cs.append(cv2.contourArea(contours[i]))
                print("contour selected",i)
                cv2.fillPoly(im_use,pts=[contours[i]],color= (0,0,0))
                print('done')


# input the image path down here
image = cv2.imread('/home/jathin/Downloads/1.jpg')
scale_percent = 15 # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
cv2.imwrite( "/home/jathin/Desktop/resized.jpg", resized );


