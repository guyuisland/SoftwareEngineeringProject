from PyQt5.Qt import *
from CustomerView import Ui_Form
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import time

BasicInfo = {"Temperature":26, "TemperatureSet":26, "Mode":1, "isRun":0, "WindSpeed":1, "Cost":0, "ID": "test", "choose_change":-1, "Temp_change":-1}
# choose_change = -1
RUNCHANGE = 4
TEMSET_CHANGE = 2
WIND_CHANGE = 1
MODE_CHANGE = 3

def translate_mode(mode):  # 翻译Mode的类型
    if mode == 1:
        return "制冷"
    else:
        return "制热"

def translate_wind(wind):
    if wind == 1 or wind == -1:
        return "低风"
    elif wind == 2 or wind == -2:
        return "中风"
    else:
        return "高风"

class customer_window(QtWidgets.QWidget, Ui_Form):

    global RUNCHANGE
    global TEMSET_CHANGE
    global MODE_CHANGE
    global WIND_CHANGE
    global BasicInfo

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.isRun = 0
        self.WindSpeed = 0
        thread = Thread(target=self.InfoShow)
        thread.setDaemon(True)
        thread.start()

    def InfoShow(self):
        while True:
            if BasicInfo["isRun"] == 1:
                self.tar_temp.setText(str(BasicInfo["TemperatureSet"]))
                self.tar_speed.setText(translate_wind(BasicInfo["WindSpeed"]))
                self.cost.setText(str(BasicInfo["Cost"]))
                self.cur_temp.setText(str(BasicInfo["Temperature"]))
                self.room_num.setText(str(BasicInfo["ID"]))
                self.cur_speed.setText(translate_wind(BasicInfo["WindSpeed"]))
                self.mode.setText(translate_mode(BasicInfo["Mode"]))
                # print("QT这边的Wind情况：", BasicInfo["WindSpeed"])
                time.sleep(2)

    def switch_click(self):
        if BasicInfo["isRun"] == 0:
            # print("开机")
            self.tar_temp.setText("25")
            self.mode.setText("制冷")
            self.tar_speed.setText("低风")
            self.cur_temp.setText("30")
            self.cur_speed.setText("低风")
            self.cost.setText("0")
            self.isRun = 1
            BasicInfo["isRun"] = 1
        else:
            # print("关机")
            self.tar_temp.setText("")
            self.mode.setText("")
            self.tar_speed.setText("")
            self.cur_temp.setText("")
            self.cur_speed.setText("")
            self.isRun = 0
            BasicInfo["isRun"] = 0
        BasicInfo["choose_change"] = RUNCHANGE

    def button_plus_click(self):
        if BasicInfo["isRun"] == 1:
            cur = BasicInfo["TemperatureSet"]
            if BasicInfo["Mode"] == 1 and cur < 25:
                cur += 1
            elif BasicInfo["Mode"] == 0 and cur < 30:
                cur += 1
            else:
                pass
            BasicInfo["TemperatureSet"] = cur
            self.tar_temp.setText(str(cur))
            BasicInfo["choose_change"] = TEMSET_CHANGE

    def button_sub_click(self):
        if BasicInfo["isRun"] == 1:
            cur = BasicInfo["TemperatureSet"]
            if BasicInfo["Mode"] == 1 and cur > 18:
                cur -= 1
            elif BasicInfo["Mode"] == 0 and cur > 25:
                cur -= 1
            else:
                pass
            BasicInfo["TemperatureSet"] = cur
            self.tar_temp.setText(str(cur))
            BasicInfo["choose_change"] = TEMSET_CHANGE

    def button_mode_click(self):
        if BasicInfo["isRun"] == 1:
            # print("更改模式")
            if BasicInfo["Mode"] == 0:
                self.mode.setText("制冷")
                BasicInfo["Mode"] = 1
            else:
                self.mode.setText("制热")
                BasicInfo["Mode"] = 0
            self.tar_temp.setText("25")
            BasicInfo["TemperatureSet"] = 25
            BasicInfo["choose_change"] = MODE_CHANGE

    def button_speed_click(self):
        if BasicInfo["isRun"] == 1:
            if BasicInfo["WindSpeed"] == 1:
                BasicInfo["WindSpeed"] = 2
                self.tar_speed.setText("中风")
            elif BasicInfo["WindSpeed"] == 2:
                BasicInfo["WindSpeed"] = 3
                self.tar_speed.setText("高风")
            else:
                BasicInfo["WindSpeed"] = 1
                self.tar_speed.setText("低风")
            BasicInfo["choose_change"] = WIND_CHANGE


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = customer_window()
#     window.show()
#     sys.exit(app.exec_())


'''
房间UI界面包含的信息和按键：
按键类：升温，降温，模式，退房，关机/开机，风速（每次调解是mod）
显示的信息：实时温度，设定温度，设定风速，实际风速（低中高和停止送风），计费信息，制冷制热模式
'''
