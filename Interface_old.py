from tkinter import *
from tkinter import filedialog
import numpy as np
import cv2
import PIL.Image, PIL.ImageTk
import psutil
import Find_cnt_img
import os
import Class
import math
from functools import partial
import Custom_Scale
import Tiff_converter
from Tiff_converter import load_tiff

class Interface_GUI(Frame):
    def __init__(self, parent, color, **kwargs):
        Frame.__init__(self, parent, bd=5, **kwargs)


        # Color of interest:
        all_colors={"1L":(42,214,0),"2L":(248,59,59),"3L":(24,24,220),"4L":(24,217,243),"1M":(148,236,121),"2M":(255,127,12),"3M":(127,127,255),"4M":(121,229,236)}
        self.col_mask = all_colors[color]#BGR


        self.grid(sticky="nsew")
        self.config()

        self.calculated=False

        Grid.columnconfigure(parent, 0, weight=1)
        Grid.rowconfigure(parent, 0, weight=1)

        self.Photos_file = filedialog.askopenfilename()
        self.all_images=Tiff_converter.load_multi_tiff(self.Photos_file)



        '''   
        self.Photos_dir = filedialog.askdirectory()
        files = os.listdir(self.Photos_dir)
        files = [f for f in files if ".tif" in f]
        Files_numbers = [int(f[(len(f)) - 6:(len(f)) - 4]) for f in files]
        print(Files_numbers)
        temp = sorted(Files_numbers)
        self.files_photos = [files[Files_numbers.index(i)] for i in temp]


             
        self.Labels_dir = filedialog.askdirectory()
        files = os.listdir(self.Labels_dir)
        files = [f for f in files if ".tif" in f]
        Files_numbers = [int(f[(len(f)) - 6:(len(f)) - 4]) for f in files]
        temp = sorted(Files_numbers)
        self.files_labels = [files[Files_numbers.index(i)] for i in temp]
        


        if len(self.files_labels) != len(self.files_photos):
            print("Error, the number of photos and mask are not similar")

        first_mask = cv2.imread(self.Labels_dir + "/" + self.files_labels[0], cv2.IMREAD_UNCHANGED)
        self.general_mask = np.zeros([first_mask.shape[0], first_mask.shape[1], 3], np.uint8)
        

        self.Size = self.general_mask.shape
       



        for lab in self.files_labels:
            tmp = cv2.imread(self.Labels_dir + "/" + lab)
            self.general_mask[
                (tmp[:, :, 0] == self.col_mask[0]) & (tmp[:, :, 1] == self.col_mask[1]) & (tmp[:, :, 2] == self.col_mask[2])] = (255, 255, 255)
                
                        self.general_mask = cv2.cvtColor(self.general_mask, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(self.general_mask, 1, 255, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        self.cut_x, self.cut_y, self.cut_w, self.cut_h = cv2.boundingRect(cnt)
        '''


        self.Size = self.all_images.shape[1:3]

        self.ImCanvas = Canvas(self, bd=2, highlightthickness=1, relief='ridge')
        self.ImCanvas.grid(column=1, row=0, sticky="nsew")

        self.ImCanvas.bind("<Configure>", partial(self.show_image, "x",False))

        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 1, weight=100)


        self.current_img = IntVar()
        self.current_img.set(0)
        self.scale_img_nb = Custom_Scale.CustomScale(self, variable=self.current_img, label="Image Nb", from_=0, to=len(self.files_photos) - 1, resolution=1, orient=HORIZONTAL, command=partial(self.show_image, "x",False))
        self.scale_img_nb.grid(column=1, row=1)

        Frame_options = Frame(self)
        Frame_options.grid(column=0, row=0, rowspan=2, sticky="nse")

        self.minimum_surface = IntVar()
        self.minimum_surface.set(10)
        Custom_Scale.CustomScale(Frame_options, label="Minimum size", from_=0, to=200, variable=self.minimum_surface, orient=HORIZONTAL, command=self.show_image).grid(column=0, row=3)

        self.maximum_surface = IntVar()
        self.maximum_surface.set(1000)
        Custom_Scale.CustomScale(Frame_options, label="Maximum size", from_=0, to=1000, variable=self.maximum_surface, orient=HORIZONTAL, command=self.show_image).grid(column=0, row=4)

        self.dilation = IntVar()
        self.dilation.set(1)
        Custom_Scale.CustomScale(Frame_options, label="dilation", from_=-5, to=5, orient=HORIZONTAL, variable=self.dilation, command=self.show_image).grid(column=0,
                                                                                                               row=5)

        self.threshold_mini = IntVar()
        self.threshold_mini.set(0)
        Custom_Scale.CustomScale(Frame_options, label="Minimum light", from_=0, to=255, resolution=1, variable=self.threshold_mini, orient=HORIZONTAL, command=self.show_image).grid(column=0, row=6)

        self.reso_thresh = IntVar()
        self.reso_thresh.set(-1)
        Custom_Scale.CustomScale(Frame_options, label="Resolution", from_=-3, to=-15, resolution=1, variable=self.reso_thresh,
              orient=HORIZONTAL, command=self.show_image).grid(column=0, row=7)


        self.thresh_method = IntVar()
        self.thresh_method.set(0)
        Radiobutton(Frame_options, text="Progressive", value=0, variable=self.thresh_method, command=self.show_image).grid(column=0, row=8)
        Radiobutton(Frame_options, text="Simple", value=1, variable=self.thresh_method, command=self.show_image).grid(column=0, row=9)

        self.NB_var=IntVar()
        self.NB_var.set(0)
        Label_micro=Label(text="Number of microglomeruli: ").grid(column=2, row=0, rowspan=1, sticky="new")
        self.Nb_Micro=Label(textvariable=self.NB_var)
        self.Nb_Micro.grid(column=3, row=0,rowspan=11, sticky="new")

        self.Label_results=Label(text="")
        self.Label_results.grid(column=2, row=1, rowspan=4, columnspan=2, sticky="new")

        self.normalise=BooleanVar()
        self.normalise.set(False)
        Checkbutton(variable=self.normalise, text="Normalise grey", command=self.show_image).grid(column=3, row=6,rowspan=5, sticky="new")


        Button(Frame_options, text="Proceed", command=self.Compute_3D).grid(column=0, row=10)
        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 1, weight=100)
        Grid.columnconfigure(self, 2, weight=1)
        Grid.columnconfigure(self, 3, weight=1)

        Grid.rowconfigure(self, 0, weight=100)
        for row in range(1,11):
            Grid.rowconfigure(self, row, weight=1)


    def update_results(self, nb_micro,Volume,Density):
        self.Label_results.config(text= "Number of microglomerulis detected = " + str(nb_micro)+"\nVolume = " + str (Volume) + " um3" + "\nDensity = " + str (Density) + " microglomeruli/um3")

    def Compute_3D(self):
        try:
            del self.showing
        except:
            pass

        self.showing = Class.Graph(self, self.Photos_dir, self.Labels_dir, self.files_photos, self.files_labels,
                              list(np.arange(255, self.threshold_mini.get(), self.reso_thresh.get())), self.minimum_surface.get(), self.maximum_surface.get(),
                              self.dilation.get(), self.thresh_method.get(), (self.cut_x, self.cut_y, self.cut_w, self.cut_h), self.col_mask)
        self.calculated=True
        self.show_image(reset=False)

    def update_ratio(self):
        self.ratio = max(self.Size[1] / self.ImCanvas.winfo_width(), self.Size[0] / self.ImCanvas.winfo_height())

    def show_image(self, event=None, reset=True,*args):
        if reset:
            self.calculated=False

        if not self.calculated:
            image = load_tiff(os.path.join(self.Photos_dir, self.files_photos[self.current_img.get()]), self.normalise.get())
            image2 = image.copy()
            #image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            cur_mask = cv2.imread(self.Labels_dir + "/" + self.files_labels[self.current_img.get()],
                                  cv2.IMREAD_UNCHANGED)
            cur_mask = cv2.inRange(cur_mask, self.col_mask, self.col_mask)
            _, cur_mask = cv2.threshold(cur_mask, 1, 255, cv2.THRESH_BINARY)
            image2 = cv2.bitwise_and(image2, image2, mask=cur_mask)
            image2 = image2[self.cut_y:self.cut_y + self.cut_h, self.cut_x:self.cut_x + self.cut_w]
            cnts = Find_cnt_img.find_cnts(list(np.arange(255, self.threshold_mini.get(), self.reso_thresh.get())), image2, self.minimum_surface.get(), self.maximum_surface.get(), self.dilation.get(), self.thresh_method.get())
            image2 = cv2.cvtColor(image2, cv2.COLOR_GRAY2BGR)

            self.NB_var.set(len(cnts))

            if np.sum(cur_mask) > 0:
                image2 = cv2.drawContours(image2, cnts, -1, (75, 162, 255), 1)

        else:
            image2, nb_cnts=self.showing.show_img(self.current_img.get())
            self.NB_var.set(nb_cnts)

        image = image2
        if not self.Size == image.shape:
            self.Size = image.shape

        self.update_ratio()
        width = int(self.Size[1]/ self.ratio)
        height = int(self.Size[0] / self.ratio)


        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
        self.shape = image.shape

        self.image_to_show3 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
        self.can_import = self.ImCanvas.create_image((self.ImCanvas.winfo_width() - self.shape[1]) / 2,
                                                         (self.ImCanvas.winfo_height() - self.shape[0]) / 2,
                                                         image=self.image_to_show3, anchor=NW)
        self.ImCanvas.itemconfig(self.can_import, image=self.image_to_show3)
        self.update_idletasks()
