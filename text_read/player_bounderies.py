import cv2
import numpy as np

PLAYERS = {'p1': (13, 214, 208, 78),
           'p2': (32, 69, 208, 95),
           'p3': (216, 24, 208, 95),
           'p4': (382, 66, 228, 78),
           'p5': (402, 217, 228, 78)
           }

BOUNDERIES = {'p1': [[(6,28),(86,47)], [(126,28),(207,44)], (99,9)],
#[Name, Bid, Fold] -> (Top left, Bottom right), (Top left, Bottom right), (x,y)
              'p2': [[(4,23),(93,43)], [(111,68), (204,68)], (96,4)],
              'p3': [[(44,24),(121,43)], [(104,70),(190,83)], (128,2)],
              'p4': [[(132,29),(225,49)], [(3,60),(105,74)], (186,7)],
              'p5': [[(134,24),(223,46)], [(7,26),(98,41)], (143,6)]}

POT = (281, 138, 83, 15)

class Reader:
    def __init__(self) -> None:
        self.img = cv2.VideoCapture(0)
        self.table_feed = {}

    def get_feeds(self) -> dict[np.ndarray]:
        _, frame = self.img.read()

        for n, cord in PLAYERS.items():
            x1, y1, w1, h1 = cord
            self.table_feed[n] = frame[y1: y1+h1, x1:x1+w1]

        x1, y1, w1, h1 = POT
        self.table_feed['pot'] = frame[y1: y1+h1, x1:x1+w1]

        return self.table_feed

    def display_dict(self, dict_frame) -> bool:
        for n, f in dict_frame.items():
            cv2.namedWindow(n)
            cv2.imshow(n, f)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True

    def win_size(self) -> tuple[int, int]:
        width = int(self.img.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.img.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height

    def spec_feed(self, x,y,w,h) -> np.ndarray:
        _, frame = self.img.read()

        if x and y and w and h:
            return frame[y: y+h, x:x+w]