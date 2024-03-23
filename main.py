import cv2 as cv
import numpy as np

# Прочитать видео
capture = cv.VideoCapture(1)
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
count = capture.get(cv.CAP_PROP_FRAME_COUNT)
fps = capture.get(cv.CAP_PROP_FPS)
print(height, width, count, fps)


def process(image, opt=1):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    line = cv.getStructuringElement(cv.MORPH_RECT, (15, 15), (-1, -1))
    #HSV зеленый диапазон
    mask = cv.inRange(hsv, (106, 84, 39), (123, 100, 100))
    # Открытая операция
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, line)

    # Извлечение контура, найти самый большой контур
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    index = -1
    max = 0
    for c in range(len(contours)):
        area = cv.contourArea(contours[c])
        if area > max:
            max = area
            index = c
    # Рисовать
    if index >= 0:
        rect = cv.minAreaRect(contours[index])
        # Подгонка эллипса
        cv.ellipse(image, rect, (255, 0, 0), 2, 8)
        # Позиционирование центральной точки
        cv.circle(image, (np.int32(rect[0][0]), np.int32(rect[0][1])), 2, (0, 255, 0), 2, 8, 0)
    return image

# Прокручивать каждый кадр
while(True):
    ret, frame = capture.read()
    if ret is True:
        cv.imshow("video-input", frame)
        result = process(frame)
        cv.imshow("result", result)
        c = cv.waitKey(50)
        if c == 27:  #ESC
            break
    else:
        break
cv.waitKey(0)
cv.destroyAllWindows()