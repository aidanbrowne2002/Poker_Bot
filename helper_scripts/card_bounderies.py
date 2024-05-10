import cv2
import numpy as np

IMG_BOUNDARIES = {
    "c1" : (216,158,11,30),
    "c2" : (259,158,11,30),
    "c3" : (302,158,11,30),
    "c4" : (345,158,11,30),
    "c5" : (389,158,11,30),
    "h1" : (282,299,11,30),
    "h2" : (323,299,11,30)
}

class VideoFeeds:
    def __init__(self) -> None:
        self.img = cv2.VideoCapture(0)
        self.img_feeds = {}

    def get_feeds(self) -> dict[np.ndarray]:
        _, frame = self.img.read()

        for n, cord in IMG_BOUNDARIES.items():
            x1, y1, w1, h1 = cord
            self.img_feeds[n] = frame[y1: y1+h1, x1:x1+w1]

        return self.img_feeds

    def display_dict(self, dict_frame) -> bool:
        for frame in dict_frame:
            cv2.imshow(frame, dict_frame[frame])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True

    def save_feed(self, name, feed):
        if len(feed.shape) == 3:
            feed = cv2.cvtColor(feed, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(name+'.jpg', feed)

    def win_size(self) -> tuple[int, int]:
        width = int(self.img.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.img.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height

    def spec_feed(self, x,y,w,h) -> np.ndarray:
        _, frame = self.img.read()

        if x and y and w and h:
            return frame[y: y+h, x:x+w]

    def destroy(self) -> None:
        self.img.release()
        cv2.destroyAllWindows()
