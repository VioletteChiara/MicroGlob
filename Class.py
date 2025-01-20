from tkinter import *
import cv2
import os
import numpy as np
import pyvista as pv
from Find_cnt_img import find_cnts
import Tiff_converter
from PIL import ImageTk,Image
import math
import colorsys


class Graph:
    def __init__(self, parent, photos, range_thresh, minimum_surface, maximum_surface, dilation, thresh_method):
        self.photos=photos
        self.range_thresh = range_thresh
        self.minimum_surface=minimum_surface
        self.maximum_surface=maximum_surface
        self.thresh_method=thresh_method
        self.dilation = dilation
        self.parent=parent

        #Parameters
        all_cnts = [[] for i in self.range_thresh]

        saved_imgs = []
        step = 0
        z = 0
        print("Step 1/4")
        for photo in self.photos:
            print(str(round((z/len(self.photos))*100,2)) + "%")
            all_cnts[step].append([])
            image = Tiff_converter.convert_img(photo, self.parent.normalise.get())
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            np_image_saved=image.copy()

            saved_imgs.append(np_image_saved)
            cnts=find_cnts(self.range_thresh,np_image_saved, self.minimum_surface,self.maximum_surface,self.dilation, self.thresh_method)
            all_cnts[step][z].append(cnts)
            z += 1


        # We then try to associate contours from different images:
        association = []
        cnts_long_asso = [[ID for ID in list(range(len(all_cnts[step][0][0])))]]
        correspondance = [ID for ID in list(range(len(all_cnts[step][0][0])))]
        next_ID = len(all_cnts[step][0][0])

        print("Step 2/4")
        for z in range(len(self.photos) - 1):
            print(str(round(z / len(self.photos) * 100, 2)) + "%")
            cnts_low = all_cnts[step][z][0]
            cnts_up = all_cnts[step][z + 1][0]

            new_correspondance = []
            cnts_long_asso_next = [np.nan for i in cnts_long_asso[z]]

            for new_cnt in range(len(cnts_up)):
                found = False

                M = cv2.moments(cnts_up[new_cnt])
                cx_new = int(M['m10'] / M['m00'])
                cy_new = int(M['m01'] / M['m00'])

                for old_cnt in range(len(cnts_low)):
                    M = cv2.moments(cnts_low[old_cnt])
                    cx_old = int(M['m10'] / M['m00'])
                    cy_old = int(M['m01'] / M['m00'])
                    res_new_in = cv2.pointPolygonTest(cnts_low[old_cnt], (int(cx_new), int(cy_new)), True)
                    res_old_in = cv2.pointPolygonTest(cnts_up[new_cnt], (int(cx_old), int(cy_old)), True)
                    if res_new_in >= -1 or res_old_in >= -1 :
                        asso_no_rep=[[asso[0],asso[1],asso[2]] for asso in association]
                        if [z, z + 1, old_cnt] not in asso_no_rep:
                            association.append([z, z + 1, old_cnt, new_cnt])
                            cnts_long_asso_next[correspondance[old_cnt]] = new_cnt
                            new_correspondance.append(correspondance[old_cnt])
                            found = True
                            break


                if not found:
                    for i in range(len(cnts_long_asso)):
                        cnts_long_asso[i].append(np.nan)
                    new_correspondance.append(next_ID)
                    cnts_long_asso_next.append(new_cnt)
                    association.append([z, z + 1, np.nan, new_cnt])
                    next_ID += 1

            correspondance = new_correspondance
            cnts_long_asso.append(cnts_long_asso_next)

        print("Step 3/4")
        cnts_long_asso = np.array(cnts_long_asso, dtype=float)

        self.saved_imgs_with_cnts = saved_imgs.copy()
        self.list_cnts=[]
        for layer in range(len(self.saved_imgs_with_cnts)):
            self.saved_imgs_with_cnts[layer] = cv2.cvtColor(self.saved_imgs_with_cnts[layer], cv2.COLOR_GRAY2RGB)
            self.list_cnts.append(0)

        print("Step 4/4")
        summary_micros = []
        self.first = None
        for micro in range(len(cnts_long_asso[0, :])):
            print(str(round(micro / len(cnts_long_asso[0, :]) * 100, 2)) + "%")
            presence = np.where(~np.isnan(cnts_long_asso[:, micro]))
            Xs_T = []
            Ys_T = []
            Zs_T = []

            color_H=np.random.uniform(0,1)
            color_S = np.random.uniform(0.5, 1)
            color_V = np.random.uniform(0.75, 1)
            color = colorsys.hsv_to_rgb(color_H, color_S, color_V)


            color_BGR = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
            color_RGB = (int(color[2]*255), int(color[1]*255), int(color[0]*255))

            if len(presence[0])>1:
                for layer in presence[0]:
                    nb_pts = len(all_cnts[0][layer][0][int(cnts_long_asso[layer, micro])][:, 0, 1])
                    Xs_T = Xs_T + (all_cnts[0][layer][0][int(cnts_long_asso[layer, micro])][:, 0, 0]).tolist()
                    Ys_T = Ys_T + (all_cnts[0][layer][0][int(cnts_long_asso[layer, micro])][:, 0, 1]).tolist()
                    Zs_T = Zs_T + ([layer] * nb_pts)

                if len(Xs_T) > 2:
                    if self.first==None or self.first>layer:
                        self.first=layer
                    Xs_T = [X * 0.062148056940223 for X in Xs_T]
                    Ys_T = [Y * 0.062148056940223 for Y in Ys_T]
                    Zs_T = [Z * 0.5 for Z in Zs_T]
                    summary_micros.append([Xs_T, Ys_T, Zs_T, (np.mean(Xs_T), np.mean(Ys_T), np.mean(Zs_T)), color_RGB])
                    for layer in presence[0]:
                        self.saved_imgs_with_cnts[layer] = cv2.drawContours(self.saved_imgs_with_cnts[layer], [all_cnts[0][layer][0][int(cnts_long_asso[layer, micro])]], -1, color_BGR, 1)
                        self.list_cnts[layer]+=len([all_cnts[0][layer][0][int(cnts_long_asso[layer, micro])]])
        # Visualisation
        # points is a 3D numpy array (n_points, 3) coordinates of a sphere
        self.plotter = pv.Plotter()
        # Iterate over micros
        for micro in range(len(summary_micros)):
            points = np.column_stack([summary_micros[micro][0], summary_micros[micro][1], summary_micros[micro][2]])
            points[:,2]=points[:,2]-self.first*0.5
            # Perform Delaunay triangulation for non-flat shapes
            cloud = pv.PolyData(points)
            volume = cloud.delaunay_3d(alpha=1.0)
            shell = volume.extract_geometry()

            self.plotter.add_mesh(shell, color=summary_micros[micro][4], opacity=1)

        self.plotter.show(interactive_update=True)
        self.show_rect(self.first)

        Surface=photos[0].shape[0]*photos[0].shape[1]


        Volume=Surface * 0.062148056940223 * 0.062148056940223 * (0.5)

        Density=len(summary_micros) / Volume

        self.parent.update_results(len(summary_micros),Volume,Density)


    def show_rect(self, pos):
        try:
            self.plotter.remove_actor(self.plan)
        except:
            pass
        pointa = [0.0, 0.0, (pos-self.first) * 0.5]
        pointb = [self.saved_imgs_with_cnts[0].shape[0]* 0.062148056940223, self.saved_imgs_with_cnts[0].shape[1]* 0.062148056940223, (pos-self.first) * 0.5]
        pointc = [0.0, self.saved_imgs_with_cnts[0].shape[1]* 0.062148056940223, (pos-self.first) * 0.5]
        rectangle = pv.Rectangle([pointa, pointb, pointc])
        self.plan = self.plotter.add_mesh(rectangle, color="red", opacity=0.3)
        self.plotter.update()

    def show_img(self, pos):
        image_cv2=self.saved_imgs_with_cnts[pos]
        image_cv2=cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
        self.show_rect(pos)
        return(image_cv2, self.list_cnts[pos])





