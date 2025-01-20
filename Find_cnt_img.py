import cv2
import numpy as np

def find_cnts(range_thresh, image, minimum_surface,maximum_surface, dilation, thresh_method):
    thresh_cnts=[]
    first=True
    kernel = np.ones((3,3), np.uint8)

    if thresh_method==1:
        range_thresh=[range_thresh[len(range_thresh)-1]]

    for thresh in range_thresh:
        np_image = image.copy()

        #cv2.imshow("Original",cv2.resize(np_image,(int(np_image.shape[0]*3), int(np_image.shape[1]*3))))
        ret, np_image = cv2.threshold(np_image, thresh, 255, cv2.THRESH_BINARY)

        if dilation>0:
            np_image = cv2.dilate(np_image,kernel,iterations=dilation)

        else:
            np_image = cv2.erode(np_image,kernel,iterations=-dilation)

        cnts, hier = cv2.findContours(np_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


        if first:
            for cnt in range(len(cnts)):
                surface=cv2.contourArea(cnts[cnt])
                if surface >= minimum_surface and surface <=maximum_surface:
                    thresh_cnts=thresh_cnts+[cnts[cnt]]
        else:
            Cnt_ass = [[] for a in range(len(cnts))]
            for new_cnt_id in range(len(cnts)):
                surface = cv2.contourArea(cnts[new_cnt_id])
                if surface >= minimum_surface and surface <=maximum_surface:
                    associated = False
                    for old_cnt_id in range(len(thresh_cnts)):
                        try:
                            M = cv2.moments(thresh_cnts[old_cnt_id])
                            cX = int(M["m10"] / M["m00"])
                            cY = int(M["m01"] / M["m00"])
                        except:
                            cX = int(np.mean(thresh_cnts[old_cnt_id][0][:, 0]))
                            cY = int(np.mean(thresh_cnts[old_cnt_id][0][:, 1]))

                        res = cv2.pointPolygonTest(cnts[new_cnt_id], (cX, cY), True)

                        if res >= -1:
                            Cnt_ass[new_cnt_id].append(old_cnt_id)
                            associated = True

                    if not associated:
                        Cnt_ass[new_cnt_id].append(-1)

                else:
                    Cnt_ass[new_cnt_id].append(-2)

            for C in range(len(Cnt_ass)):
                if Cnt_ass[C][0]==-1:
                    thresh_cnts.append(cnts[C])
                elif len(Cnt_ass[C])==1 and Cnt_ass[C][0]!=-2:
                    thresh_cnts[Cnt_ass[C][0]]=cnts[C]

        first = False

    '''
    np_image= cv2.drawContours(np_image,thresh_cnts,-1,150,-1)
    cv2.imshow("W", cv2.resize(np_image,(int(np_image.shape[0]*3), int(np_image.shape[1]*3))))
    cv2.waitKey()
    '''
    return(thresh_cnts)


