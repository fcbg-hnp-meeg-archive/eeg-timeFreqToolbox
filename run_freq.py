from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QIcon
import sys
import os

print('CURRENT DIRECTORY FOLDER : ', os.getcwd())

from app.time_freq import TimeFreq

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = TimeFreq()
    main.show()
    sys.exit(app.exec_())
