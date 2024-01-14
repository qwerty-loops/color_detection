#This project shall attempt to accurately identify colors
#The project shall be constrcuted in a manner where clicking on different objects in an image, will give the color of that image
#The dataset being utilised contains 2 fearures : Name and value. Once an image is clicked, its distance from the nearest colours will be tallied and shortest distance taken

#There are 3 primary colors Red, Green and Blue with range of (0-255) each
#There are totally 16.5 million colors, (256 * 256 * 256)

#Step 1:Import the necessary libraries
import pandas as pd
import numpy as np
import cv2
#We shall be utilising argparser for the same, with this we can specify the image path directly in command prompt
import argparse

#Step 2 : Taking an image as an arguement from the user
ap=argparse.ArgumentParser() #adding an instance
ap.add_argument('-i','--image',required=True,help='Image path')
#ap.pars_args returns the arguements provided at the command line, in the form of a namespace
args=vars(ap.parse_args()) #vars returns the dictionary attribute of namespace object
img_path=args['image']
#Reading image using OpenCV
img=cv2.imread(img_path)


#Step 3 : Read the csv dataset and store in a dataframe
index=["color","color_name","hex","R","G","B"]
df=pd.read_csv(r'D:\Allen Archive\Allen Archives\NEU_academics\Semester1\Python_notebooks\All Semesters\Self_projects\Color_detection\colors.csv',names=index,header=None)


#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

#Step 4 : Creating a function that computes the RGB value upon  double clicking
#Upon double clicking, the x,y coordinates are computed and the RGB values computed.
def draw_function(event, x,y,flags,param):
    if (event == cv2.EVENT_LBUTTONDBLCLK):
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

#Step 5 : Creating a window in which the image shall appear
cv2.namedWindow('image')
#The call back function is maintained if a mouseclick within the window occurs
cv2.setMouseCallback('image',draw_function)

#Step 6 : Based on minimum distance to the closest color, we determine the color
#After obtaining rgb values, we compute the colors and the color having the least distance is selected
        
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(df)):
        d = abs(R- int(df.loc[i,"R"])) + abs(G- int(df.loc[i,"G"]))+ abs(B- int(df.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = df.loc[i,"color_name"]
    return cname

#Step 7 :Post double click, the RGB values and color are updated
while(True):
    cv2.imshow("image",img) #Imshow plots image in window
    if (clicked):
        #cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills rectangle entirely
        cv2.rectangle(img,(20,20), (700,60), (b,g,r), -1) #Generates a rectangle for the output text

        #Creating text string to display ( Color name and RGB values )
        text = getColorName(r,g,b) + ' Red='+ str(r) + ' Green='+ str(g) + ' Blue='+ str(b)

        #cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA) #Puts text in the rectangle
  #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

        clicked=False

    #Break the loop when user hits 'esc' key 
    if cv2.waitKey(20) & 0xFF ==27:
        break

cv2.destroyAllWindows()



