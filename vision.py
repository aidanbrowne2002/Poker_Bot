import cv2
import numpy as np

PLAYERS = {'p1': [(73, 244, 69, 15), (176, 242, 60, 15)], # [Name, bet] -> (x,y,w,h)
           'p2': [(91, 94, 69, 15), (170, 140, 60, 15)],
           'p3': [(273, 46, 69, 15), (318, 93, 60, 15)],
           'p4': [(484, 93, 69, 15), (392, 124, 60, 15)],
           'p5': [(501, 241, 69, 15), (393, 243, 60, 15)]
           }
POT = (319, 138, 29, 15)


class Reader:
    def __init__(self) -> None:
        self.pot_img = cv2.VideoCapture(1)
        self.table_feed = {}

    def get_feeds(self) -> dict[np.ndarray]:
        _, frame = self.pot_img.read()

        for n, cord in PLAYERS.items():
            x1, y1, w1, h1 = tuple(cord[0])
            x2, y2, w2, h2 = tuple(cord[1])
            self.table_feed[n] = [frame[y1: y1+h1, x1:x1+w1], frame[y2: y2+h2, x2:x2+w2]]

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
