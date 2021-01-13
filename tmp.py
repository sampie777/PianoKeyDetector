import cv2
import numpy as np


def ndarray_to_string(array: np.ndarray) -> str:
    return "[{}]".format(', '.join(str(list(e)) for e in array))


def main():
    image = cv2.imread("/home/prive/Downloads/easy-things-to-draw-hand-1024x5762.jpg", cv2.IMREAD_GRAYSCALE)

    image = ~image

    image = cv2.GaussianBlur(image, (21, 21), 0)
    image = cv2.threshold(image, 20, 255, cv2.THRESH_BINARY)[1]

    contours, hierarchy = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        print("No contours found")
        return
    print("{} contours found".format(len(contours)))

    maxValue = [0, 0]
    for point in contours[0]:
        maxValue[0] = max(maxValue[0], point[0][0])
        maxValue[1] = max(maxValue[1], point[0][1])

    print("MaxValue: {}".format(maxValue))

    factor = 300 / maxValue[0]

    contour = contours[0] * 300 / maxValue[0]

    prev_point = contour[-1]
    print("arrayOf(", end="")
    for i, point in enumerate(contour):
        if i % 5 != 0:
            continue

        # print("[{}, {}]".format(round(point[0][0] * factor), round(point[0][1] * factor)))
        print("arrayOf({}, {}),".format(round(point[0][1] / 10, 1), round(point[0][0] / 10, 1)), end=" ")

        cv2.line(image, (round(prev_point[0][0]), round(prev_point[0][1])),
                 (round(point[0][0]), round(point[0][1])), 255, 1)

        prev_point = point
    print(")")

    # for contour in contours:
    # cv2.drawContours(image, [contour], 0, 255, 20)

    cv2.imshow("Image", image)
    cv2.waitKey(10000)


if __name__ == "__main__":
    main()
