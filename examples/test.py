import sys
import signal
import time


def signal_handler(sig, frame):
    print('Ląduj')
    sys.exit(0)


def main():
    print('start')


def main2():
    print('lad')


i = 0
signal.signal(signal.SIGINT, signal_handler)
main()
time.sleep(2)
main2()

time.sleep(7)
