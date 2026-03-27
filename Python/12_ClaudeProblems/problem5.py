import multiprocessing


def generateSquare(n, q):
    q.put(n * n)


if __name__ == "__main__":
    q = multiprocessing.Queue()  # Correct Queue

    # Create processes
    p1 = multiprocessing.Process(target=generateSquare, args=(1, q))
    p2 = multiprocessing.Process(target=generateSquare, args=(2, q))
    p3 = multiprocessing.Process(target=generateSquare, args=(3, q))

    # Start processes
    p1.start()
    p2.start()
    p3.start()

    # Wait for processes to finish
    p1.join()
    p2.join()
    p3.join()

    # Collect all results
    results = []
    for _ in range(3):
        results.append(q.get())  # get each item

    print("From Main Process:")
    print("Datas are:", results)
