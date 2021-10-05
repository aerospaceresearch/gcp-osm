import cv2


def get_qr_data(file, debug_show_image=False):
    position_marker_coordinates = None
    max_pixels = 600
    input_image = cv2.imread(file, cv2.IMREAD_COLOR)
    payload, bounding_box, rectified_image = cv2.QRCodeDetector().detectAndDecode(input_image)

    if len(payload) > 0:
        position_marker_coordinates = get_position_marker_coordinates(bounding_box)

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
