import cv2
import numpy as np
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt

def get_qr_data(file, debug_show_image=False):
    position_marker_coordinates = None
    max_pixels = 600
    input_image = cv2.imread(file, cv2.IMREAD_COLOR)
    payload, bounding_box, rectified_image = cv2.QRCodeDetector().detectAndDecode(input_image)


    if len(payload) > 0:
        position_marker_coordinates = get_position_marker_coordinates(bounding_box)

        # get the corner pixel of the qr image
        x_min = int(np.floor(np.min(bounding_box[0][:, 1]))) - 10
        x_max = int(np.ceil(np.max(bounding_box[0][:, 1])))  + 10
        y_min = int(np.floor(np.min(bounding_box[0][:, 0]))) - 10
        y_max = int(np.ceil(np.max(bounding_box[0][:, 0])))  + 10

        qr_image = input_image[x_min: x_max, y_min : y_max]

        # converting the image to grey image for better contrast
        img_gray = cv2.cvtColor(qr_image, cv2.COLOR_BGR2GRAY)
        ret, img_gray = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)


        # get all the clusters in the original black and white qr-code image
        label_img = label(img_gray)
        regions = regionprops(label_img)

        # get all the clusters in the inverted black and white qr-code image
        img_gray_invert = cv2.bitwise_not(img_gray)
        label_img_invert = label(img_gray_invert)
        regions_invert = regionprops(label_img_invert)



        # get the diagonal from the center bobble to the other corner without bobble
        diagonal_x1 = [int(bounding_box[0][0][0])-y_min, int(bounding_box[0][2][0])-y_min]
        diagonal_y1 = [int(bounding_box[0][0][1])-x_min, int(bounding_box[0][2][1])-x_min]

        diagonal_m1 = ((int(bounding_box[0][2][1])-x_min) - (int(bounding_box[0][0][1])-x_min)) /\
            ((int(bounding_box[0][2][0])-y_min) - (int(bounding_box[0][0][0])-y_min))

        diagonal_b1 = (int(bounding_box[0][2][1])-x_min) - diagonal_m1 * (int(bounding_box[0][2][0])-y_min)

        dia_x1 = []
        dia_y1 = []
        for i in range(y_max - y_min):
            dia_x1.append(i)
            dia_y1.append(diagonal_m1*i+diagonal_b1)


        # get the diagonal from the left down bobble to the other corner with right up bobble
        diagonal_x3 = [int(bounding_box[0][1][0])-y_min, int(bounding_box[0][3][0])-y_min]
        diagonal_y3 = [int(bounding_box[0][1][1])-x_min, int(bounding_box[0][3][1])-x_min]

        diagonal_m3 = ((int(bounding_box[0][3][1])-x_min) - (int(bounding_box[0][1][1])-x_min)) /\
            ((int(bounding_box[0][3][0])-y_min) - (int(bounding_box[0][1][0])-y_min))

        diagonal_b3 = (int(bounding_box[0][3][1])-x_min) - diagonal_m3 * (int(bounding_box[0][3][0])-y_min)

        dia_x3 = []
        dia_y3 = []
        for i in range(y_max - y_min):
            dia_x3.append(i)
            dia_y3.append(diagonal_m3*i+diagonal_b3)


        # put all the cluster IDs along the first diagonal
        signal1 = []
        for i in range(len(dia_x1)):
            if dia_y1[i] >= 0 and dia_y1[i] < x_max - x_min:
                signal1.append(label_img_invert[int(dia_y1[i])][int(dia_x1[i])])

        # put all the cluster IDs along the second diagonal
        signal3 = []
        for i in range(len(dia_x3)):
            if dia_y3[i] >= 0 and dia_y3[i] < x_max - x_min:
                signal3.append(label_img_invert[int(dia_y3[i])][int(dia_x3[i])])


        # find the center bobble. that is the cluster after the 2nd cluster ID change
        found1 = 0
        index1 = 0
        index1_b4 = -1
        for i in range(len(signal1)):
            if signal1[i] != 0 and index1_b4 != signal1[i]:
                found1 += 1

            if found1 == 2:
                index1 = signal1[i]
                break

            index1_b4 = signal1[i]

        x1, y1 = regions_invert[index1-1].centroid
        area1 = regions_invert[index1-1].area

        cv2.circle(input_image, [y_min + int(y1), x_min + int(x1)], 30, (0, 255, 255), -1)


        # find the left down bobble. that is the cluster after the 2nd cluster ID change
        found2 = 0
        index2 = 0
        index2_b4 = -1
        for i in range(len(signal3)):
            if signal3[i] != 0 and index2_b4 != signal3[i]:
                found2 += 1

            if found2 == 2:
                index2 = signal3[i]
                break

            index2_b4 = signal3[i]

        x2, y2 = regions_invert[index2-1].centroid
        area2 = regions_invert[index2-1].area

        cv2.circle(input_image, [y_min + int(y2), x_min + int(x2)], 30, (255, 255, 0), -1)


        # find the righ up bobble. that is the cluster after the 2nd cluster ID change
        found3 = 0
        index3 = 0
        index3_b4 = -1
        for i in range(len(signal3)):
            if signal3[len(signal3) - i - 1] != 0 and index3_b4 != signal3[len(signal3) - i - 1]:
                found3 += 1

            if found3 == 2:
                index3 = signal3[len(signal3) - i - 1]
                break

            index3_b4 = signal3[len(signal3) - i - 1]

        x3, y3 = regions_invert[index3-1].centroid
        area3 = regions_invert[index3-1].area

        cv2.circle(input_image, [y_min + int(y3), x_min + int(x3)], 30, (255, 0, 255), -1)









        if debug_show_image:

            plt.imshow(label_img_invert)
            plt.plot(diagonal_x1, diagonal_y1, "o-")
            plt.plot(diagonal_x3, diagonal_y3, "o-")
            plt.plot(y1, x1, "*")
            plt.plot(y2, x2, "*")
            plt.plot(y3, x3, "*")
            plt.show()

            plt.imshow(label_img)
            plt.plot(diagonal_x1, diagonal_y1, "o-")
            plt.plot(diagonal_x3, diagonal_y3, "o-")
            plt.plot(y1, x1, "*")
            plt.plot(y2, x2, "*")
            plt.plot(y3, x3, "*")

            # finding the smallest bobble, the 4th bobble
            for i in range(len(regions_invert)):
                if regions_invert[i].area > (area1 + area2 + area3) / 3 / 13 and \
                        regions_invert[i].area < (area1 + area2 + area3) / 3 / 6:

                    xm, ym = regions_invert[i].centroid

                    plt.plot(ym, xm, "o")


            plt.title("cluster id on qr-code, diagonals and position markers")
            plt.show()

            plt.plot(signal1, label="diagonal 1")
            plt.plot(signal3, label="diagonal 2")
            plt.xlabel("x position via diagonal")
            plt.ylabel("cluster id for pixel on diagonal")
            plt.grid()
            plt.legend()
            plt.show()


            
            cv2.circle(input_image, position_marker_coordinates, 10, (0, 0, 255), -1)

            base = input_image.shape[0]
            if base < input_image.shape[1]:
                base = input_image.shape[1]

            if max_pixels > input_image.shape[0] and max_pixels > input_image.shape[1]:
                scale_percent = 100.0  # percent of original size
            else:
                scale_percent = max_pixels / base * 100.0

            width = int(input_image.shape[1] * scale_percent / 100)
            height = int(input_image.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            resized = cv2.resize(input_image, dim, interpolation=cv2.INTER_AREA)

            cv2.imshow("highlighted image", resized)
            cv2.waitKey(0)

    return payload, position_marker_coordinates


def get_position_marker_coordinates(bounding_box):
    upper_left_x = int(bounding_box[0][0][0])
    upper_left_y = int(bounding_box[0][0][1])

    lower_right_x = int(bounding_box[0][2][0])
    lower_right_y = int(bounding_box[0][2][1])

    # TODO the detection of the position marker can be optimized by using contours
    center_x = upper_left_x + int((lower_right_x - upper_left_x) / 25 * 3)
    center_y = upper_left_y + int((lower_right_y - upper_left_y) / 25 * 3)

    return center_x, center_y


if __name__ == '__main__':
    '''imported'''
