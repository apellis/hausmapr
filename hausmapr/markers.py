"""Generate a printable ChArUco calibration board used as a scale reference in photos."""

import cv2
from PIL import Image

DPI = 300
LETTER_IN = (8.5, 11.0)
SQUARES_X, SQUARES_Y = 6, 8
SQUARE_MM, MARKER_MM = 25.0, 18.0
DICTIONARY = cv2.aruco.DICT_5X5_100


def board():
    dictionary = cv2.aruco.getPredefinedDictionary(DICTIONARY)
    return cv2.aruco.CharucoBoard(
        (SQUARES_X, SQUARES_Y), SQUARE_MM / 1000.0, MARKER_MM / 1000.0, dictionary
    )


def render_letter_pdf(path):
    px_per_mm = DPI / 25.4
    board_px = (round(SQUARES_X * SQUARE_MM * px_per_mm), round(SQUARES_Y * SQUARE_MM * px_per_mm))
    art = board().generateImage(board_px, marginSize=0, borderBits=1)

    page = Image.new("L", (round(LETTER_IN[0] * DPI), round(LETTER_IN[1] * DPI)), 255)
    page.paste(Image.fromarray(art), ((page.width - board_px[0]) // 2, (page.height - board_px[1]) // 2))
    page.save(path, "PDF", resolution=DPI)
    return board_px
