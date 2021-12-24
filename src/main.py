import os, sys
from files.interface import NetworkGraphApp
pwd = os.getcwd() + "/files"
sys.path.insert(0, pwd)


if __name__ == '__main__':
    ng = NetworkGraphApp()
    rt = ng.window_loop()
    rt.mainloop()