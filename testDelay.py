import time

def printDelay():
    print("before delay")
    time.sleep(120)
    print("after delay")

def main():
    printDelay()

if __name__ == '__main__':
    main()