import cv2
import numpy as np
# from matplotlib import pyplot as plt
# image = cv2.imread("test2.jpg",0)
# image = cv2.resize(image, (480, 640))

# create a CLAHE object (Arguments are optional).
# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5,5))
# image = clahe.apply(image)
# cv2.imshow('Test',image)
# cv2.waitKey()
import os
import glob

files = glob.glob('CroppedImages/*')
for f in files:
    os.remove(f)
img_final = cv2.imread("equation.jpg")
size = (15,15)

img_final = cv2.resize(img_final, (480, 640))

cv2.imshow('Final Image',img_final)
# cv2.waitKey()
img2gray = cv2.cvtColor(img_final, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 40, 100, cv2.THRESH_BINARY)
image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
image_final2  = image_final
cv2.imshow('Image that is cropped from',image_final2)
cv2.waitKey()
image_final  = cv2.erode(image_final, kernel, iterations=3)


cv2.imshow('Image that is cropped from',image_final)
cv2.waitKey()

size2 = (15,15)
image_final2 = cv2.GaussianBlur(image_final2,size2,1)
image_final2 = cv2.adaptiveThreshold(image_final2,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,75,10)
image_final2 = cv2.bitwise_not(image_final2)
# kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
# image_final2  = cv2.dilate(image_final2, kernel, iterations=1)
cv2.imshow('Image that is cropped from',image_final2)
cv2.waitKey()

image = cv2.GaussianBlur(image_final,size,0)
image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,75,10)
image = cv2.bitwise_not(image)

kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
image  = cv2.dilate(image, kernel, iterations=2)

cv2.imshow('Image after Preprocessing',image)
cv2.waitKey()


# image  = cv2.erode(image, kernel, iterations=2)
# image  = cv2.dilate(image, kernel, iterations=1)
# cv2.imshow("eroded",image)
# cv2.waitKey()

_, contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)

index = 0
our_contours = []

for contour in contours:
    [x, y, w, h] = cv2.boundingRect(contour)
    our_contours.append([x, y, w, h])



our_contours.sort()

rec_file = []

for contour in our_contours:
    # get rectangle bounding contour
    [x, y, w, h] = contour
    # Don't plot small false positives that aren't text
    if w < 25 and h < 25:
        continue

    print h,y
    # draw rectangle around contour on original image
    cv2.rectangle(image,(x, y), (x + w, y + h), (255, 0, 255), 2)
    cropped = image_final2[y:y + h, x: x + w]

    # BLACK = [0, 0, 0]
    # if w > h:
    #     h1 = w/2
    #     cropped = cv2.copyMakeBorder(cropped,h1,h1,0,0,cv2.BORDER_REPLICATE)
    # if h > w:
    #     w1 = h/2
    #     cropped = cv2.copyMakeBorder(cropped,0,0,w1,w1,cv2.BORDER_REPLICATE)

    cropped = cv2.resize(cropped, (28,28), interpolation=cv2.INTER_LINEAR)


    s = 'CroppedImages/crop_' + str(index) + '.png'
    cv2.imwrite(s, cropped)
    cv2.imshow("Image",cropped)
    # cv2.imshow(s,cropped)
    index = index + 1
cv2.imshow("Contoured Image",image)
cv2.waitKey()
