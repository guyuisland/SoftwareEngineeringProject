import pymysql
import datetime


class Db:
    # 初始化数据库连接
    def __init__(self):
        self.co = pymysql.connect(host="127.0.0.1", user="root", password="szyxwd", database="billsys", charset="utf8")

    # 在userinfo表中创建新用户，如果存在同名用户，则修改该用户。
    def createUser(self, name: str, identity: int, roomnum: int):
        # 新建账号信息：name名字、identity身份标识、roomnum房间号
        cursor = self.co.cursor()
        sql1 = "select* from userinfo where name='%s'" % name
        cursor.execute(sql1)
        res = cursor.fetchone()
        if (res):
            sql2 = "update userinfo set identity=%d,roomnum=%d where name='%s'" % (identity, roomnum, name)
        else:
            sql2 = "insert into userinfo(id,name,identity,roomnum)  \
             values(%s,%s,%d,%d)" % ("id", name, identity, roomnum)
        try:
            cursor.execute(sql2)
            self.co.commit()
            print("用户" + str(id) + "新建成功")
        except:
            self.co.rollback()
            print("用户" + str(id) + "新建失败")
        cursor.close()

    # 在uselog表中创建新的使用记录
    def createLog(self, id: int, roomnum: int, start_temp: float, end_temp: float,
                  start_time: datetime, end_time: datetime, windspeed: int, price: float):
        cursor = self.co.cursor()
        start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "insert into uselog(id,roomnum,start_temp,end_temp," \
              "start_time,end_time,windspeed,price)  \
               values(%d, %d, %f, %f,'%s','%s', %d, %f)" % \
              (id, roomnum, start_temp, end_temp, start_time, end_time, windspeed, price)
        try:
            cursor.execute(sql)
            self.co.commit()
            print("记录存储成功")
        except:
            self.co.rollback()
            print("记录存储失败")
        cursor.close()

    # 每分钟实时存储各房间的状态信息流，以备管理员检查（管理员线程可能无法与用户线程频繁地交换数据）
    def createStream(self, id: int, roomnum: int, cur_temp: float, windspeed: int, cur_price: float,
                     cur_time: datetime):
        cursor = self.co.cursor()
        cur_time = cur_time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "insert into logstream(id,roomnum,cur_temp,windspeed,cur_price,cur_time)" \
              "values(%d, %d, %f, %d, %f, '%s')" % (id, roomnum, cur_temp, windspeed, cur_price, cur_time)
        try:
            cursor.execute(sql)
            self.co.commit()
            print("记录存储成功")
        except:
            self.co.rollback()
            print("记录存储失败")
        cursor.close()

    # 默认id1<=id2,遍历userinfo表，打印id值在id1~id2之间的用户信息
    def printInfoById(self, id1: int, id2: int):
        cursor = self.co.cursor()
        if (id1 == id2):
            sql = "select* from userinfo where id=%d" % id1
        else:
            sql = "select* from userinfo where id>=%d and id<=%d" % (id1, id2)
        cursor.execute(sql)
        res = cursor.fetchall()
        # if (res):
        #    print("账户信息：")
        # for i in res:
        #    print(i)
        cursor.close()
        return res

    # 遍历userinfo表,通过name值打印用户信息
    def printInfoByName(self, name: str):
        cursor = self.co.cursor()
        sql = "select* from userinfo where name='%s'" % name
        cursor.execute(sql)
        res = cursor.fetchone()
        # if(res):
        #    print("账户信息：")
        # print(res)
        cursor.close()
        return res

    # 默认id1<=id2,遍历userinfo表，打印id值在id1~id2之间的用户使用记录
    def printLogById(self, id1: int, id2: int):
        cursor = self.co.cursor()
        if (id1 == id2):
            sql = "select* from uselog where id=%d" % id1
        else:
            sql = "select* from uselog where id>=%d and id<=%d" % (id1, id2)
        cursor.execute(sql)
        res = cursor.fetchall()
        if (res):
            print("用户" + str(id) + "使用记录为：")
        # for i in res:
        #    print(i)
        cursor.close()
        return res

    # 遍历userinfo表,通过name值打印用户使用记录
    def printLogByTime(self, start_time, end_time):
        cursor = self.co.cursor()
        sql = "select* from uselog where start_time>='%s' and end_time<='%s'" \
              % (start_time, end_time)
        cursor.execute(sql)
        res = cursor.fetchall()
        if (res):
            print("从" + str(start_time) + "到" + str(end_time) + "使用记录为：")
        # for i in res:
        #    print(i)
        cursor.close()
        return res

    # 根据房间号从实时数据流中返回最新状态
    def getStreamByRoom(self, roomnum: int):
        cursor = self.co.cursor()
        sql = "select A.* from logstream as A, " \
              "(select roomnum, max(cur_time) max_t from logstream group by roomnum) as B" \
              " where A.cur_time = B.max_t and B.roomnum=%d " \
              % (roomnum)
        cursor.execute(sql)
        res = cursor.fetchone()
        print(res)
        cursor.close()
        return res

    # 根据用户id，打印其记录的花费和
    def getPriceById(self, id: int) -> float:
        cursor = self.co.cursor()
        sql = "select roomnum, sum(price) from uselog where id=%d group by roomnum" % id
        cursor.execute(sql)
        res = cursor.fetchone()
        cursor.close()
        # print(res)
        return res[1]

    # TODO

# if __name__ == '__main__':
#     s=Db()
#     s.co=pymysql.connect(host="127.0.0.1", user="root", password="szyxwd", database="billsys", charset="utf8")
#     #s.printInfoByName("harry")
#     #s.createUser("harry",1,16)
#     #s.printInfoById(1,1)
#     #s.getPriceById(1)
#     t1 = datetime.datetime.now()
#     s.createStream(7,2,27.5,2,71,t1)
#     s.getStreamByRoom(2)
#     #time.sleep(1)
#     #t2 = datetime.datetime.now()
#     #s.createLog(1,11,29,25.5,t1,t2,2,0)
#     #s.printLogById(1,7)
#     s.co.close()
