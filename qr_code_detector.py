import cv2
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import os
import zxing

def get_qr_codes(file):

    # todo here we could implement more color manipulation to search again in the same image with different threshold
    im_color = cv2.imread(file, cv2.IMREAD_COLOR)
    im_gray = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)
    image_threshold = 128 #  int(np.max(im_gray))-25
    ret, im_thresh = cv2.threshold(im_gray, image_threshold, 255, cv2.THRESH_BINARY)  #, 255, cv2.THRESH_BINARY)

    code_detection = decode(im_thresh, symbols=[ZBarSymbol.QRCODE])
    # https://github.com/NaturalHistoryMuseum/pyzbar/issues/29
    # when symbols=[ZBarSymbol.QRCODE], it checks for all code formats, including barcodes
    # instead of im_thresh, also Image.open(file)

    found_qr_codes = []
    if len(code_detection) > 0:
        for code in code_detection:
            found_qr_codes.append(two_step_detection(im_thresh, code))
        return found_qr_codes

    else:
        print("haven't found any qr-codes in the whole image")
        return [[False, None, None]]

def two_step_detection(im_thresh, code):
    tmp_path = "tmp" + os.sep
    create_dir(tmp_path)
    tmp_file_name = tmp_path + "temporary_file.jpg"

    # zbar and boundaries generation
    edge_1 = int(code.rect.height * 0.08)
    corner_top = code.rect.top - edge_1
    if corner_top < 0:
        corner_top = 0

    corner_bottom = code.rect.top + code.rect.height + edge_1
    if corner_bottom >= len(im_thresh):
        corner_bottom = len(im_thresh) - 1

    edge_2 = int(code.rect.width * 0.08)
    corner_left = code.rect.left - edge_2
    if corner_left < 0 :
        corner_left = 0

    corner_right = code.rect.left + code.rect.width + edge_2
    if corner_right >= len(im_thresh[0]):
        corner_right = len(im_thresh[0]) - 1

    # zxing needs an image file, so we store one temporary one for it
    cv2.imwrite(tmp_file_name, im_thresh[corner_top : corner_bottom, corner_left : corner_right])

    # zxing doesn't like windows separator and other strange characters, so we just change it
    reader = zxing.BarCodeReader()
    barcode = reader.decode(tmp_file_name) # filename, try_harder, does not handle exceptions yet, when the file is NOT an image

    if barcode is not None and barcode.format is not None:
        valid = barcode.format is not None and barcode.format == "QR_CODE"
        content = barcode.parsed
        point = [corner_left + barcode.points[1][0], corner_top + barcode.points[1][1]]
        return [valid, content, point]
    else:
        return [False,None,None]

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == '__main__':
    '''imported'''
