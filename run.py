import multiprocessing


# Process 1
def startKrishna():
    print("Process 1 is running.")
    from main import start

    start()


# Process 2
def listenHotword():
    print("Process 2 is running.")
    from engine.features import hotword

    hotword()


# ✅ MUST be outside functions
if __name__ == "__main__":
    p1 = multiprocessing.Process(target=startKrishna)
    p2 = multiprocessing.Process(target=listenHotword)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("System stopped")
