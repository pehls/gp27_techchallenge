import os
from time import sleep, time, strftime, gmtime
from datetime import datetime

# @profile
def main():
    startTime = time()
    print("-="*30)
    print(f'---- Started at {datetime.now()}')
    print("-="*30)
    os.system('python src\\data\\001_get_raw_data.py')
    elapsed_time = time() - startTime
    print("-="*30)
    print(f"---- Execution time: {strftime('%H:%M:%S', gmtime(elapsed_time))}")
    print("-="*30)


if __name__ == '__main__':
    main()