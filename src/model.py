from time import sleep

class Model:
    def __init__(self):
        self.sleeptime = 1

    def run(self):
        while True:
            sleep(self.sleeptime)

def main():
    pass

if __name__ == "__main__":
    main()