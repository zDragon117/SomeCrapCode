from threading import Timer
import argparse

globalIsOver = False

# Create the parser
my_parser = argparse.ArgumentParser()

# Add the arguments
my_parser.add_argument('timeout',
                       metavar='timeout',
                       type=float,
                       help='Countdown time')

# Execute the parse_args() method
args = my_parser.parse_args()


def run(timeout=30):
    timer(timeout)
    while True and not over():
        #Do something
        print ("start looping")
    print ('Exited run function.')


def timer(time):
    t = Timer(time, setOver)
    print ("timer started")
    t.start()


def setOver():
    global globalIsOver
    print ('\nSetting globalIsOver = True')
    globalIsOver = True


def over():
    global globalIsOver
    print ('returned = ' + str(globalIsOver))
    return globalIsOver


if __name__ == '__main__':
    run(args.timeout)
