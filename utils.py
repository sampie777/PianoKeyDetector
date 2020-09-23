import cv2

from config import Config


def show_image(image, title: str = "Image", delay: int = Config.preview_frame_rate) -> bool:
    cv2.namedWindow(title, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(title, image)

    key = cv2.waitKey(delay)
    if key in [27, 13, 32]:
        return False
    return True
