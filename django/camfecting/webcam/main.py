import threading
import requests
import cv2
import io


def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()

        if ret:
            _, buffer = cv2.imencode(
                ".jpg",
                frame,
                [
                    int(cv2.IMWRITE_JPEG_QUALITY),
                    60
                ]
            )
            files = {
                "image": (
                    "snapshot.jpg",
                    io.BytesIO(buffer.tobytes()),
                    "image/jpeg"
                )
            }

            threading.Thread(
                target=requests.post,
                args=("http://localhost:8000/upload/",),
                kwargs={"files": files}
            ).start()

    cap.release()


def do_something_else():
    print("hello world")
    while True:
        1


if __name__ == "__main__":
    demon = threading.Thread(target=main)
    demon.daemon = True
    demon.start()
    do_something_else()
