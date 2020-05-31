import pymysql
import time
import datetime

class DataBase:
    co=pymysql.connect(host="127.0.0.1", user="root", password="szyxwd", database="billsys", charset="utf8")

    #在userinfo表中创建新用户，如果存在同名用户，则修改该用户。
    def createUser(self, name:str, identity:int, roomnum:int):
        #新建账号信息：name名字、identity身份标识、roomnum房间号
        cursor = self.co.cursor()
        sql1="select* from userinfo where name='%s'" % name
        cursor.execute(sql1)
        res=cursor.fetchone()
        if(res):
            sql2="update userinfo set identity=%d,roomnum=%d where name='%s'" % (identity,roomnum,name)
        else:
            sql2="insert into userinfo(id,name,identity,roomnum)  \
             values(%s,%s,%d,%d)" % ("id",name,identity,roomnum)
        try:
            cursor.execute(sql2)
            self.co.commit()
            print("用户"+str(id)+"新建成功")
        except:
            self.co.rollback()
            print("用户"+str(id)+"新建失败")
        cursor.close()

    #在uselog表中创建新的使用记录
    def createLog(self,id:int,roomnum:int,start_temp:float,end_temp:float,
                  start_time:datetime,end_time:datetime,windspeed:int,price:float):
        cursor = self.co.cursor()
        start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "insert into uselog(id,roomnum,start_temp,end_temp," \
              "start_time,end_time,windspeed,price)  \
               values(%d, %d, %f, %f,'%s','%s', %d, %f)" % \
              (id, roomnum, start_temp,end_temp,start_time,end_time,windspeed,price)
        try:
            cursor.execute(sql)
            self.co.commit()
            print("记录存储成功")
        except:
            self.co.rollback()
            print("记录存储失败")
        cursor.close()

    #默认id1<=id2,遍历userinfo表，打印id值在id1~id2之间的用户信息
    def printInfoById(self,id1:int,id2:int):
        cursor = self.co.cursor()
        if(id1==id2):
            sql = "select* from userinfo where id=%d" % id1
        else:
            sql = "select* from userinfo where id>=%d and id<=%d" % (id1,id2)
        cursor.execute(sql)
        res = cursor.fetchall()
        if (res):
            print("账户信息：")
        for i in res:
            print(i)
        cursor.close()

    #遍历userinfo表,通过name值打印用户信息
    def printInfoByName(self,name:str):
        cursor = self.co.cursor()
        sql = "select* from userinfo where name='%s'" % name
        cursor.execute(sql)
        res=cursor.fetchone()
        if(res):
            print("账户信息：")
        print(res)
        cursor.close()

    #默认id1<=id2,遍历userinfo表，打印id值在id1~id2之间的用户使用记录
    def printLogById(self,id1:int,id2:int):
        cursor = self.co.cursor()
        if (id1 == id2):
            sql = "select* from uselog where id=%d" % id1
        else:
            sql = "select* from uselog where id>=%d and id<=%d" % (id1, id2)
        cursor.execute(sql)
        res=cursor.fetchall()
        if(res):
            print("用户" + str(id) + "使用记录为：")
        for i in res:
            print(i)
        cursor.close()

    # 遍历userinfo表,通过name值打印用户使用记录
    def printLogByTime(self,start_time,end_time):
        cursor = self.co.cursor()
        sql = "select* from uselog where start_time>='%s' and end_time<='%s'"\
              % (start_time,end_time)
        cursor.execute(sql)
        res = cursor.fetchall()
        if(res):
            print("从" + str(start_time) + "到" + str(end_time) + "使用记录为：")
        for i in res:
            print(i)
        cursor.close()

    #根据用户id，打印其记录的花费和
    def getPriceById(self,id:int)->float:
        cursor = self.co.cursor()
        sql = "select roomnum, sum(price) from uselog where id=%d group by roomnum" % id
        cursor.execute(sql)
        res = cursor.fetchone()
        cursor.close()
        return res[1]




if __name__ == '__main__':
    s=DataBase()
    s.co=pymysql.connect(host="127.0.0.1", user="root", password="szyxwd", database="billsys", charset="utf8")
    #s.printInfoByName("harry")
    #s.createUser("harry",1,16)
    #s.printInfoById(1,1)
    s.getPriceById(1)
    #t1 = datetime.datetime.now()
    #time.sleep(1)
    #t2 = datetime.datetime.now()
    #s.createLog(1,11,29,25.5,t1,t2,2,0)
    #s.printLogById(1,7)
    s.co.close()