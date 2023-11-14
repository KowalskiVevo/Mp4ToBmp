from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
import os
import cv2
import time

class Ui_MainWindow(object):
    # def echo(low_value, high_value):
    #     print(low_value, high_value)

    # Метод инициализации объектов GUI
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(470, 600)
        self.error_message_box = QMessageBox()
        self.error_message_box.setWindowTitle("Error")
        self.error_message_box.setIcon(QMessageBox.Critical)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 180, 171, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 320, 171, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(90, 430, 321, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(70, 30, 341, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 280, 341, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(150, 490, 171, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(100, 90, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.timeEdit_2 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_2.setGeometry(QtCore.QRect(250, 90, 118, 22))
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 60, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 90, 61, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 140, 71, 20))
        self.label_3.setObjectName("label_3")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(240, 140, 42, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1000)
        self.spinBox.setObjectName("spinBox")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(170, 400, 131, 20))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)

        self.pushButton.clicked.connect(self.getFileName)
        self.pushButton_2.clicked.connect(self.getDirName)
        self.pushButton_3.clicked.connect(self.convertMp4ToBMP)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Метод устанавливает текст и заголовки объектов GUI
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mp4ToBmp"))
        self.pushButton.setText(_translate("MainWindow", "Mp4 File"))
        self.pushButton_2.setText(_translate("MainWindow", "Output Dir"))
        self.lineEdit.setText(_translate("MainWindow", "Insert path to file"))
        self.lineEdit_2.setText(_translate("MainWindow", "Insert a directory to output an array of files"))
        self.pushButton_3.setText(_translate("MainWindow", "Convert"))
        self.timeEdit.setDisplayFormat(_translate("MainWindow", "H:mm:ss:zzz"))
        self.timeEdit_2.setDisplayFormat(_translate("MainWindow", "H:mm:ss:zzz"))
        self.label.setText(_translate("MainWindow", "Interval:"))
        self.label_2.setText(_translate("MainWindow", "—"))
        self.label_3.setText(_translate("MainWindow", "Frame step:"))
        self.label_4.setText(_translate("MainWindow", "Converting progress:"))
    
    # Метод выбора входного файла с расширением .mp4 для конвертирования
    def getFileName(self):
        file_filter = 'Mp4 files (*.mp4)'
        self.input_file = QFileDialog.getOpenFileName(
            caption = 'Select a data file',
            directory = os.getcwd(),
            filter = file_filter,
            initialFilter='Mp4 files (*.mp4)'
        )[0]
        print(self.input_file)
        self.lineEdit.setText(self.input_file)
        try:
            cap = cv2.VideoCapture(self.input_file)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count/fps
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"duration = {duration} seconds")
            print(f"fps = {fps}")
            print(f"length = {length}")
            self.timeEdit_2.setTime(QtCore.QTime(0,0,0).addMSecs(duration * 1000))
            #Время в миллисекундах
            print(QtCore.QTime(0,0,0).msecsTo(self.timeEdit_2.time()))
            cap.release()
        except ZeroDivisionError as err:
            print(err)
        except Exception as err:
            self.error_message_box.setText(f"Unexpected {err}, {type(err)}")
            self.error_message_box.exec_()
    
    # Метод диалога выбора выходной папки для хранения массива bmp
    def getDirName(self):
        self.output_dict = QFileDialog.getExistingDirectory(
            caption = 'Select a directory',
            directory = os.getcwd(),
            options = QFileDialog.ShowDirsOnly
        )
        print(self.input_file)
        self.lineEdit_2.setText(self.output_dict)
    
    # Метод обновления индикатора выполнения (прогресс бара)
    #
    # Так как скорость обработки быстрее, чем скорость обновления gui, то в функции была встроена задержка на 1 мс
    def updateProgressBar(self, val):
        self.progressBar.setProperty("value", val)
        time.sleep(0.001)
    
    # Метод конвертирования
    def convertMp4ToBMP(self):
        try:
            self.updateProgressBar(0)
            cap = cv2.VideoCapture(self.input_file)
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            #Устанавливаем интервал кадров
            pos_start = QtCore.QTime(0,0,0).msecsTo(self.timeEdit.time())
            pos_end = QtCore.QTime(0,0,0).msecsTo(self.timeEdit_2.time())
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    number_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES)); 
                    position_video = cap.get(cv2.CAP_PROP_POS_MSEC)

                    # сохраняем каждый N-й кадр в формате BMP в папку "frames"
                    if number_frame % self.spinBox.value() == 0 and position_video >= pos_start and position_video <= pos_end :
                        filename = f"frame_{number_frame}.bmp"
                        filepath = self.lineEdit_2.text() + '/' + filename
                        can_write = cv2.imwrite(filepath, frame)
                        if (can_write == False):
                            self.error_message_box.setText("An error occurred while writing the file")
                            self.error_message_box.exec_()
                            self.updateProgressBar(0)
                            break
                        self.updateProgressBar(int((number_frame / length) * 100))
                        # cv2.imshow('frame', frame)
                        # if cv2.waitKey(1) & 0xFF == ord('q'):
                        #     break
                    else:
                        if position_video > pos_end :
                            break
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()
            self.updateProgressBar(100)    
        except Exception as err:
            self.error_message_box.setText(f"Unexpected {err}, {type(err)}")
            self.error_message_box.exec_()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
