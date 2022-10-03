from PyQt5 import QtCore, QtGui, QtWidgets
from lab92 import Ui_MainWindow
import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
import serial
import time as tt

class mylab92class(Ui_MainWindow):
    def __init__(self) -> None:
        super().setupUi(MainWindow)
        self.ser=serial.Serial("COM7",9600)
        self.guiconnect()
        self.timer1init()
        self.timer2init()

    def timer1init(self):
        self.mytimer1 = QtCore.QTimer()
        self.mytimer1.timeout.connect(self.ReadSW)
        self.mytimer1.setInterval(300)    
        self.mytimer1.start()

    def timer2init(self):
        self.mytimer2 = QtCore.QTimer()
        self.mytimer2.timeout.connect(self.ReadADC)
        self.mytimer2.setInterval(200)    
        self.mytimer2.start()

    def ReadADC(self):
        self.ser.write('a'.encode())
        tt.sleep(0.1)
        self.adcvalue = self.ser.readline().strip().decode()
        self.adc.setText(self.adcvalue)

    def ReadSW(self):
        self.ser.write('e'.encode())
        tt.sleep(0.1)
        self.SWst = self.ser.readline().strip().decode()
        if self.SWst == '1':
            self.ledsts.setText("ON")
            self.ledsts.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.SWst == '0':
            self.ledsts.setText("OFF")
            self.ledsts.setStyleSheet("background-color: rgb(255, 0, 0);")

    def guiconnect(self):
        self.onbt.clicked.connect(self.onclick)
        self.offbt.clicked.connect(self.offclick)
        self.sld.sliderReleased.connect(self.sendPWM)
        self.runbt_2.clicked.connect(self.runclick)
        self.stopbt.clicked.connect(self.stopclick)

    def runclick(self):
        self.ser.write('y'.encode())
        self.onbt.setDisabled(False)
        self.offbt.setDisabled(False)
        self.sld.setDisabled(False)
    
    def stopclick(self):
        self.ser.write('x'.encode())
        self.mytimer1.stop()
        self.mytimer2.stop()
        self.onbt.setDisabled(True)
        self.offbt.setDisabled(True)
        self.sld.setDisabled(True)
    
    def sendPWM(self):
        self.sdval=self.sld.value()
        self.ser.write(('p'+str(self.sdval)).encode())
        tt.sleep(0.1)

    def onclick(self):
        self.ser.write('c'.encode())

    def offclick(self):
        self.ser.write('d'.encode())

# Comment


if __name__ == "__main__":
    mylab92 = mylab92class()
    MainWindow.show()
    sys.exit(app.exec_())

## giftnaaa