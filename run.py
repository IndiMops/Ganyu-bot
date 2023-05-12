import threading
import subprocess

def run_file1():
    subprocess.call(['python', 'main.py'])

def run_file2():
    subprocess.call(['python', 'website/app.py'])

if __name__ == '__main__':
    thread1 = threading.Thread(target=run_file1)
    thread2 = threading.Thread(target=run_file2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
