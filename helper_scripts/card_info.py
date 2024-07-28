import numpy as np
import cv2

class CardInfo:
    def __init__(self) -> None:
        self.warp: list[np.ndarray] = [] # flattened, grayed, blurred image
        self.rank_img: list[np.ndarray] = [] # Thresholded, sized image of card's rank
        self.suit_img: list[np.ndarray] = [] # Thresholded, sized image of card's suit
        self.best_rank_match: str = "Unknown" # Best rank match
        self.best_suit_match: str = "Unknown" # Best suit match
        self.rank_diff: int = 0 # Difference between rank image and best matched train rank image
        self.suit_diff: int = 0 # Difference between suit image and best matched train suit image

class TrainRanks:
    def __init__(self) -> None:
        self.img: list[np.ndarray] = []
        self.name: str = None

class TrainSuits:
    def __init__(self) -> None:
        self.img: list[np.ndarray] = []
        self.name: str = None

def load_ranks(filepath) -> list[np.ndarray]:
    train_ranks: list[str] = []

    for i, rank in enumerate(['two','three','four','five','six','seven',
                 'eight','nine','ten','jack','queen','king','ace']):
        train_ranks.append(TrainRanks())
        train_ranks[i].name = rank
        filename: str = rank + '.jpg'
        train_ranks[i].img = cv2.imread(filepath+filename, cv2.IMREAD_GRAYSCALE)

    return train_ranks

def load_suits(filepath) -> list[np.ndarray]:
    train_suits: list[str] = []

    for i, suit in enumerate(['spade_1','spade_2','spade_3','diamond_1','diamond_2','diamond_3',
                    'club_1','club_2','club_3','heart_1','heart_2','heart_3']):
        train_suits.append(TrainSuits())
        train_suits[i].name = suit
        filename: str = suit + '.jpg'
        train_suits[i].img = cv2.imread(filepath+filename, cv2.IMREAD_GRAYSCALE)

    return train_suits

def process(frame, thresh_level = 199) -> CardInfo:
    card_info = CardInfo()

    card_info.warp = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # Turn frame colour to gray
    zoom_img = cv2.resize(card_info.warp, (0, 0), fx=4, fy=4) # Get resize of image with rescale increase of 4*

    # Future use - used to get white_level of image
    # white_level = zoom_img[0, int(np.shape(frame)[1])] # h, w

    if thresh_level <= 0:
        thresh_level = 1
    _, query_thresh = cv2.threshold(zoom_img, thresh_level, 255, cv2.THRESH_BINARY_INV)

    card_ranks: np.ndarray = query_thresh[0:66, 0:40]
    card_suit: np.ndarray = query_thresh[65:129, 0:40]
    # Keep uncommented for - debug use only
    # return zoom_img
    # return query_thresh

    # Auto re-ajustable V
    countours_r, _ = cv2.findContours(card_ranks, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    countours_s, _ = cv2.findContours(card_suit, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    countours_r = sorted(countours_r, key=cv2.contourArea,reverse=True)
    countours_s = sorted(countours_s, key=cv2.contourArea,reverse=True)

    if countours_r and countours_s:
        x1,y1,w1,h1 = cv2.boundingRect(countours_r[0])
        x2,y2,w2,h2 = cv2.boundingRect(countours_s[0])
        resized_r = cv2.resize(card_ranks[y1:y1+h1, x1:x1+w1], (70, 125), 0, 0)
        resized_s = cv2.resize(card_suit[y2:y2+h2, x2:x2+w2], (70, 100), 0, 0)
        card_info.rank_img = resized_r
        card_info.suit_img = resized_s

    # Keep uncommented for - debug use only
    # return card_info.rank_img
    # return card_info.suit_img
    # return card_info.rank_img, card_info.suit_img
    return card_info

def match_card(card_info, t_ranks, t_suits) -> tuple[str, str, int, int]:
    best_rank_match_diff: int = 10000
    best_suit_match_diff: int = 10000
    best_rank_match_name: str = "Unknown"
    best_suit_match_name: str = "Unknown"

    if len(card_info.rank_img) != 0 and len(card_info.suit_img) != 0:
        for rank in t_ranks:
            diff_img: np.ndarray = cv2.absdiff(card_info.rank_img, rank.img)
            rank_diff: int = int(np.sum(diff_img)/255)

            if rank_diff < best_rank_match_diff:
                best_rank_diff_img = diff_img
                best_rank_match_diff = rank_diff
                best_rank_name = rank.name

        for suit in t_suits:
            diff_img: np.ndarray = cv2.absdiff(card_info.suit_img, suit.img)
            suit_diff: int = int(np.sum(diff_img)/255)

            if suit_diff < best_suit_match_diff:
                best_suit_diff_img = diff_img
                best_suit_match_diff = suit_diff
                best_suit_name = suit.name

    if best_rank_match_diff < 2000:
        best_rank_match_name = best_rank_name

    if best_suit_match_diff < 700:
        best_suit_match_name = best_suit_name

    return best_rank_match_name, best_suit_match_name
