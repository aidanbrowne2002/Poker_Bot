import cv2
import player_bounderies as pb
import numpy

def mouseclick(event, x,y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"{x}, {y}")

def get_pixel_colour(frame, cord):
    x,y = cord
    print(frame[y, x])

def main():
    img = cv2.VideoCapture(0)

    cv2.namedWindow('Video')
    # cv2.setMouseCallback('Video', mouseclick)
    # cords = [(99, 9),(96, 4),(128, 2),(186, 7),(143, 6)]
    cords = (420, 425, 113, 62)
    x1,y1,w1,h1 = cords
    contour = []
    while True:
        _, frame = img.read()
        frame = frame[y1: y1+h1, x1:x1+w1]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 39, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:
            size = cv2.contourArea(i)
            if size > 4000 and size < 5000:
                contour = [i]

        cv2.imshow('Video', cv2.drawContours(frame, contour, -1, (0,255,0), 1))
        # cv2.imshow('Video',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # print(len(contours[0]))
    # get_pixel_colour(binary, cords)
    # img.release()
    # cv2.destroyAllWindows()
main()
