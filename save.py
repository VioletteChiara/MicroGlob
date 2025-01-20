from tkinter import *
import Interface

# load a 2D sample
def start_mainframe():
    Mainframe = Tk()
    Mainframe.title("Test")
    GUI=Interface.Interface_GUI(Mainframe, color="2L")


    Mainframe.mainloop()






'''

img=cv2.imread("G:\Pologne\Ants_Iago\Microglomerulis\Lh_183/Lh_183_100x_MB0027.jpg")
img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img)

impulse_response = [[2, 1],[2,1]]
recovered, remainder = signal.deconvolve(img, impulse_response)

print(recovered)

#Apply different thresholds:
#img=cv2.threshold(img,50,255)

cv2.imshow("W",cv2.resize(img, (int(img.shape[0]/3),int(img.shape[1]/3))))
cv2.imshow("Deconv", cv2.resize(recovered, (int(img.shape[0] / 3), int(img.shape[1] / 3))))

cv2.waitKey()

'''