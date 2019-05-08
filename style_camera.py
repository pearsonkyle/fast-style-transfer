from matplotlib import cm
import numpy as np
import time
import cv2

from evaluate import ffwds 

c = 0
cmaps = ['CMRmap', 'gnuplot', 'prism','spring', 'Dark2', 'Paired', 'Set1',  'tab10', 'tab20', 'tab20b', 'tab20c', 'CMRmap_r','gnuplot_r', 'inferno_r', 'twilight', 'twilight_r', ]

cap = cv2.VideoCapture(0)

def quad(frame):
    top = np.hstack([frame,frame[:,::-1]])
    return np.vstack([top,top[::-1]])

nextframe = time.time()
ret, currentframe = cap.read()
currentframe = quad( currentframe/255. ) 
oldframe = np.copy(currentframe)
newframe = np.copy(currentframe)
lerp = 0
frames = []

print('press n to switch color maps')
print('press p to take a stylized picture')
print('press q to exit program')

while(True):

    # Display the resulting frame
    ret, currentframe = cap.read()
    
    cmap = cm.get_cmap(cmaps[c])
    gray = cv2.cvtColor(currentframe, cv2.COLOR_BGR2GRAY)
    currentframe = cmap(gray/255)
    quadframe =  quad( currentframe ) 
    cv2.imshow('frame',quadframe)

    # keyboard controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    
    if key == ord('n'):
        c += 1
        c = c % len(cmaps)

    # turn on kaleidoscope
    if key == ord('k'):
        pass

    # apply style 
    if key == ord('p'):

        oldframe = np.copy(quadframe[:,:,:3])
        out = ffwds([currentframe[:,:,:3]], 'wave.ckpt', batch_size=1)
        newframe = quad( out[0]/255. ) 
        lerp = 0

        frames = []
        while (lerp < 1):
            currentframe = newframe*lerp + oldframe * (1-lerp)
            cv2.imshow('frame',currentframe)
            cv2.waitKey(1)
            lerp += 0.1
        
        time.sleep(1)

        while (lerp >0):

            # lerp back to frame
            currentframe = newframe*lerp + oldframe * (1-lerp)
            cv2.imshow('frame',currentframe)
            cv2.waitKey(1)
            lerp -= 0.2
    
        while (lerp <= 1):
            # get current camera frame
            ret, currentframe = cap.read()
            cmap = cm.get_cmap(cmaps[c])
            gray = cv2.cvtColor(currentframe, cv2.COLOR_BGR2GRAY)
            currentframe = cmap(gray/255)
            newframe =  quad( currentframe )[:,:,:3]
                        
            currentframe = newframe*lerp + oldframe * (1-lerp)
            cv2.imshow('frame',currentframe)
            cv2.waitKey(1)
            lerp += 0.25

        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# TODO 
# add controls to loop through styles 
# save picture/ pause mode 
# add controls for kaleidoscope 