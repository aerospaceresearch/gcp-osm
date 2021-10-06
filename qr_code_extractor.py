import cv2


def get_qr_data(file, debug_show_image=False):
    position_marker_coordinates = None
    max_pixels = 600
    input_image = cv2.imread(file, cv2.IMREAD_COLOR)
    payload, bounding_box, rectified_image = cv2.QRCodeDetector().detectAndDecode(input_image)

    if len(payload) > 0:
        position_marker_coordinates = get_position_marker_coordinates(input_image)

        if debug_show_image:
            cv2.circle(input_image, position_marker_coordinates, 10, (0, 255, 0), -1)

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


def get_position_marker_coordinates(input_image):
    threshed_img = cv2.threshold(cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY), 60, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    for c in contours:
        # compute the center of the contour
        M = cv2.moments(c)
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])
    return center_x, center_y


if __name__ == '__main__':
    '''imported'''
