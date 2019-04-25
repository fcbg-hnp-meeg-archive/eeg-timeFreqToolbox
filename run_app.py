import sys
import os
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QIcon
from app.time_freq import TimeFreq

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

print('CURRENT DIRECTORY FOLDER : ', os.getcwd())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = TimeFreq()
    main.show()
    sys.exit(app.exec_())
