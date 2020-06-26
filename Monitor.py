from ServerOperation import *
import threading
from threading import Thread
import time

from DataBase import *
import pymysql

AuthorityInfoPath = "Info\\Authority.xlsx"  # 存放管理员和经理密码的表格


class Administrator:  # 管理员
    # 已经确定不需要登录功能

    def GetTime(self):  # 获取当前系统时间
        pass

    def ShowRunInfo(self):  # 打印当前所有房间的信息
        # print("我是管理员")
        time.sleep(5)

    def run(self):  # 运行总函数
        print("管理员登录界面已启动")
        while True:
            self.ShowRunInfo()


class Manager(Administrator):  # 经理
    def PrintDetail(self):  # 打印当日指定时间的详单
        pass

    def run(self):
        print("经理登录界面已启动....")


class Waitor(Administrator):  # 前台
    def PrintBill(self):  # 打印账单
        pass

    def run(self):
        print("前台登录界面已启动,,,")


class Login:

    def ServerRun(self):
        run = ServerData()  # (database, app)
        MonitorThread = Thread(target=self.FirstUIDeal)
        MonitorThread.setDaemon(True)
        MonitorThread.start()
        run.SocketStart()

    def FirstUIDeal(self):
        waitor = Waitor()
        waitor_thread = threading.Thread(target=waitor.run)
        waitor_thread.setDaemon(True)
        waitor_thread.start()
        manager = Manager()
        manager_thread = threading.Thread(target=manager.run)
        manager_thread.setDaemon(True)
        manager_thread.start()
        administrator = Administrator()
        admin_thread = threading.Thread(target=administrator.run)
        admin_thread.setDaemon(True)
        admin_thread.start()


# test = Login()
# test.ServerRun()


if __name__ == '__main__':

    app = None
#    database = Db()
#    database.co = pymysql.connect(host="127.0.0.1", user="root", password="szyxwd", database="billsys", charset="utf8")
    server = Login()
    client = Room()
    server.ServerRun()


'''
管理员界面：只显示所有房间的计费，温度，送风信息
前台界面：多出一个打印指定房间详单的按钮
经理界面：多出一个打印指定时间段内所有房间使用的信息的按钮
'''
