from pyzbar import pyzbar
import cv2
from PIL import Image
from picamera import PiCamera


def decode(image):
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # draw the barcode
        # print("detected barcode:", obj)
        # image = draw_barcode(obj, image)
        # print barcode type & data
        return obj.type, obj.data

    return None


def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    # uncomment above and comment below if you want to draw a polygon and not a rectangle
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                          (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                          color=(0, 255, 0),
                          thickness=5)
    return image


def capture():
    camera = PiCamera()
    camera.capture('/home/alvin/PycharmProjects/pythonProject/venv/picture.png')
    camera.close()


def barcode_scan():
    capture()
    img = cv2.imread("picture.png")
    img = decode(img)
    return img


#print(barcode_scan())
