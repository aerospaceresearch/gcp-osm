import cv2


def get_qr_data(file, debug_show_image=False):
    position_marker_coordinates = None
    max_pixels = 600
    input_image = cv2.imread(file, cv2.IMREAD_COLOR)
    payload, bounding_box, rectified_image = cv2.QRCodeDetector().detectAndDecode(input_image)

    if len(payload) > 0:
        position_marker_coordinates = get_position_marker_coordinates(input_image, bounding_box)

        if debug_show_image:
            output_image = input_image.copy()

            for v in bounding_box[0]:
                cv2.circle(output_image, [int(val) for val in v], 15, (0, 0, 255), -1)

            base = output_image.shape[0]
            if base < output_image.shape[1]:
                base = output_image.shape[1]

            if max_pixels > output_image.shape[0] and max_pixels > output_image.shape[1]:
                scale_percent = 100.0  # percent of original size
            else:
                scale_percent = max_pixels / base * 100.0

            width = int(input_image.shape[1] * scale_percent / 100)
            height = int(input_image.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            resized_image = cv2.resize(output_image, dim, interpolation=cv2.INTER_AREA)

            cv2.imshow("highlighted image", resized_image)
            cv2.waitKey(0)

    return payload, position_marker_coordinates


def get_position_marker_coordinates(input_image, bounding_box):
    x1 = int(bounding_box[0][0][0])
    y1 = int(bounding_box[0][0][1])
    x2 = int(bounding_box[0][1][0])
    y2 = int(bounding_box[0][1][1])
    x3 = int(bounding_box[0][2][0])
    y3 = int(bounding_box[0][2][1])
    x4 = int(bounding_box[0][3][0])
    y4 = int(bounding_box[0][3][1])

    top_left_x = min([x1, x2, x3, x4])
    top_left_y = min([y1, y2, y3, y4])
    bot_right_x = max([x1, x2, x3, x4])
    bot_right_y = max([y1, y2, y3, y4])

    bot_right_x = int((bot_right_x - top_left_x) / 3) + top_left_x
    bot_right_y = int((bot_right_y - top_left_y) / 3) + top_left_y

    cropped_image = input_image[top_left_y:bot_right_y + 1, top_left_x:bot_right_x + 1]

    cv2.imshow("asdf", cropped_image)
    cv2.waitKey(0)

    gray = cv2.cvtColor(cropped_image.copy(), cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    center_id = [i for i, x in enumerate(hierarchy[0]) if x[2] < 0][0]

    cv2.drawContours(cropped_image, contours[center_id], -1, (0, 255, 0), 3)

    M = cv2.moments(contours[center_id])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.circle(cropped_image, (cX, cY), 15, (255, 255, 0), -1)

    return cX, cY


if __name__ == '__main__':
    '''imported'''
