from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, qApp, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow,
                            QGridLayout, QStatusBar, QWidget, QStatusBar, QLineEdit)
from PyQt5.QtCore import QFile , Qt
from PyQt5.QtGui import QImage, QIcon, QPixmap, QIntValidator
import os, sys
from currency_converter import CurrencyConverter

try:
    from PyQt5.QtWinExtras import QtWin
    myappid = 'convert.images.python.program'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass

def resource_path(relative_path):
    """used by pyinstaller to see the relative path"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

logo = resource_path("./gui/CurrencyConverter.png")
guifile = resource_path("./gui/main.ui")
appbg = resource_path("./gui/bg.png")
c = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
currencyList = c.currencies


class GUI(QMainWindow):
    """main window used by the application"""
    def __init__(self):
        super(GUI, self).__init__()
        UIFile = QFile(guifile)
        UIFile.open(QFile.ReadOnly)
        uic.loadUi(UIFile, self)
        UIFile.close()

        currencyBg = QPixmap(appbg)
        self.appbg.setPixmap(currencyBg)

        self.resultLabel.setAlignment(Qt.AlignCenter)

        self.fromCurrency.addItems(currencyList)
        self.fromCurrency.setCurrentText("USD")
        self.fromCurrency.setStatusTip("Choose which currency to convert from!")
        self.toCurrency.addItems(currencyList)
        self.toCurrency.setStatusTip("Choose which currency you want to convert to!")
        self.toCurrency.setCurrentText("EUR")

        self.onlyInt = QIntValidator()
        self.amountLine.setValidator(self.onlyInt)
        self.amountLine.setStatusTip("Insert value then press ENTER or click ConvertCurrency!")

        self.amountLine.returnPressed.connect(self.cmdConvertCurrency)
        self.btnConvertCurrency.clicked.connect(self.cmdConvertCurrency)
        self.btnConvertCurrency.setStatusTip("Convert the amount to the new currency!")

    def cmdConvertCurrency(self):
        try:
            amount = self.amountLine.text()

            fromCurrency = self.fromCurrency.currentText()
            toCurrency = self.toCurrency.currentText()

            result = c.convert(int(amount), fromCurrency, toCurrency)
            self.resultLabel.setText(f"{str(round(result,2))} {toCurrency}")
        except c.RateNotFoundError:
            pass

style = '''
QMenuBar,
QPushButton,
QComboBox,
QLineEdit,
QMessageBox QPushButton {
    background-color: #eeeeee;
    border: 3px;
    border-color: #000000;
}

QPushButton:focus,
QLineEdit:focus,
QComboBox:focus {
    color: #000000;
    selection-background-color: #222831;
    background-color: #FFFFFF;
    border: none;
}  

QLabel {
    color: #eeeeee;
}

QComboBox QAbstractItemView {
    selection-color: #FED369;
    selection-background-color: #222831;
    background-color: #eeeeee;
}

QPushButton:hover,
QLineEdit:hover,
QComboBox:hover,
QMessageBox QPushButton {
    color: #000000;
    selection-background-color: #222831;
    background-color: #FFFFFF;
}  
QPushButton:pressed {
    color: #000000;
    background-color: #FFFFFF;
}  
'''


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(logo))
app.setStyleSheet(style) 
window = GUI()
window.show()
app.exec_()