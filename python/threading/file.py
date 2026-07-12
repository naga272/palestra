import threading
import time


def main(counter):
    print(counter)


if __name__ == "__main__":
    start = time.time()
    threads = []
    for i in range(999):
        t = threading.Thread(target=main, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("fine: ", time.time() - start)
