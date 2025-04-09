# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from CoreObject.MgrPersistentObject import MgrPersistentObject
import KST
import csstatus
import json

class GMNoticeManager(MgrPersistentObject):

    """GM工具公告管理器"""
    def __init__(self):
        MgrPersistentObject.__init__(self)
        self.isLoading = True #用来标记是否在服务器启动过程，防止加载数据时公告数据重复添加到数据库
        self.noticeIndex = 0  # 生成公告ID的索引
        self.gmTimerArg = {}  # 公告计时器表，以公告ID为键保存一组公告的所有计时器的ArgValue {1:{12:12,13:13}}
        self.noticeSchemes = {} #格式{ 触发时间：{公告id：[公告名,单条间隔时间，组间隔时间，次数，公告内容] },}
        self.crondMgr = KBEngine.globalData["CrondManager"]
        self.init()


    def init(self):
        """创建或者加载数据库的公告数据"""
        self.createRecord()
        self.queryAllRecord()


    def load(self,noticeResult):
        for result in noticeResult:
            triggerTime = result[1].decode('utf-8')
            noticeName = result[2].decode('utf-8')
            intervalTime = int(result[3].decode('utf-8'))
            groupTime = int(result[4].decode('utf-8'))
            count = int(result[5].decode('utf-8'))
            msg = result[6].decode('utf-8')
            if not msg:
                return
            msgList = msg.split("|")
            if len(msgList) > 1:
                self.addGMSchemeGroupNotice(noticeName, triggerTime, intervalTime, groupTime, count, msgList)
            else:
                self.addGMSchemeNotice(noticeName, triggerTime, intervalTime, count, msgList[0])
        self.onCompleteInit()
        self.isLoading = False


    def genNoticeID(self):
        """
        生成公告ID
        """
        self.noticeIndex += 1
        return self.noticeIndex



    def addGMNotice(self,intervalTime, count, msg,fileno):
        """
        define method
         GM工具添加一个即时公告的接口
        :param intervalTime:单次公告的间隔时间
        :param count:公告发送次数
        :param msg:公告内容
        :return:返回公告ID
        """
        noticeID = self.genNoticeID()
        for i in range(count):
            if i == 0:
                timerArg = self.addTimerCallBack(intervalTime * i, "sendWorldNotice", (msg,))
                self.gmTimerArg[noticeID] = {timerArg: timerArg}
                continue

            timerArg = self.addTimerCallBack(intervalTime * i, "sendWorldNotice", (msg,))
            self.gmTimerArg[noticeID][timerArg] = timerArg
        message = {"state": "success"}
        self.onOperationCB(message, fileno)




    def addGMSchemeNotice(self, schemeName, triggerTime, intervalTime, count, msg, fileno = -1):
        """
        define method
        GM工具添加定时公告的接口
        :param schemeName:利用Shceme实现指定时间触发
        :param triggerTime:指定的触发时间，like as: 0-59/2 0-23 1-31 1-12 0-7
        :param intervalTime:发送公告的间隔时间
        :param count:发送公告的次数
        :param msg:公告的内容
        :return:返回公告ID，返回None为添加失败
        """


        if triggerTime in self.noticeSchemes:
            KBEDebug.INFO_MSG("this time(%s) has a notice！" % triggerTime)
            if fileno >= 0:
                message = {"state": "fault", "message": "this time(%s) has a notice！" % triggerTime}
                self.onOperationCB(message, fileno)
            return
        noticeID = self.genNoticeID()
        msgList = [msg]
        if not self.isLoading:
            self.addRecord(schemeName, triggerTime, intervalTime, 0, count, msgList)
        self.noticeSchemes[triggerTime] = {noticeID: [schemeName, intervalTime, 0, count, msgList]}
        noticeKey = "GMNotice_%s" % noticeID
        self.crondMgr.addScheme(noticeKey, triggerTime, self, "addSchemeNotice", 1, (intervalTime, count, msg, noticeID))
        if fileno >= 0:
            message = {"state": "success"}
            self.onOperationCB(message, fileno)



    def addSchemeNotice(self, cmd, *noticeInfo):
        """
        """
        intervalTime,count,msg,noticeID = noticeInfo[0]
        for i in range(count):
            if i == 0:
                timerArg = self.addTimerCallBack(intervalTime * i, "sendWorldNotice", (msg,))
                self.gmTimerArg[noticeID] = {timerArg: timerArg}
                continue

            timerArg = self.addTimerCallBack(intervalTime * i, "sendWorldNotice", (msg,))
            self.gmTimerArg[noticeID][timerArg] = timerArg




    def addGMSchemeGroupNotice(self, schemeName, triggerTime, singleTime, groupTime, count, msgList, fileno = -1):
        """
        define method
        GM工具添加一组定时公告的接口（多条公告）
        :param schemeName: 利用Shceme实现指定时间触发
        :param triggerTime: 指定的触发时间，like as: 0-59/2 0-23 1-31 1-12 0-7
        :param singleTime: 一组公告中单条公告的间隔时间
        :param groupTime: 发送每组公告之间的间隔时间
        :param count: 这组公告的发送次数
        :param msgList: 公告内容的列表
        :return: 返回公告ID，返回None为添加失败
        """
        if not triggerTime:         #接收的时间参数为空串，立即发送
            noticeID = self.genNoticeID()
            self.addTimerCallBack(0, "addGMGroupNotice", ((singleTime, groupTime, count, msgList, noticeID),))
            message = {"state": "success"}
            self.onOperationCB(message, fileno)
            return

        if triggerTime in self.noticeSchemes:
            KBEDebug.INFO_MSG("this time(%s) has a notice！" % triggerTime)
            if fileno >= 0:
                message = {"state": "fault", "message": "this time(%s) has a notice！" % triggerTime}
                self.onOperationCB(message, fileno)
            return
        noticeID = self.genNoticeID()
        if not self.isLoading:
            self.addRecord(schemeName, triggerTime, singleTime, groupTime, count, msgList)
        self.noticeSchemes[triggerTime] = {noticeID: [schemeName, singleTime, groupTime, count, msgList]}
        noticeKey = "GMNotice_%s" % noticeID
        self.crondMgr.addScheme(noticeKey, triggerTime, self, "addGMGroupNotice", 1, (singleTime, groupTime, count, msgList, noticeID))
        if fileno >= 0:
            message = {"state": "success"}
            self.onOperationCB(message, fileno)


    def addGMGroupNotice(self, cmd, *noticeInfo):
        """添加一组内容不同公告的计时器（多条公告功能）"""

        singleTime, groupTime, count, msgList, noticeID = noticeInfo[0]
        singleTimes = singleTime * (len(msgList) - 1)
        for i in range(count):
            if i == 0:
                timerArg = self.addTimerCallBack((singleTimes + groupTime) * i, "sendWorldGroupMsg",(singleTime, noticeID, msgList))
                self.gmTimerArg[noticeID] = {timerArg: timerArg}
                continue

            timerArg = self.addTimerCallBack((singleTimes + groupTime) * i, "sendWorldGroupMsg",(singleTime, noticeID, msgList))
            self.gmTimerArg[noticeID][timerArg] = timerArg



    def delGMNotice(self, timerNoticeID):
        """
        define method
        GM工具删除即时公告的接口，即时公告在所有计时器触发完后会自动删除
        :param timerNoticeID:公告的ID
        :return:
        """
        if timerNoticeID not in self.gmTimerArg:
            return            #"Notice had deleted or not existed!"
        for timerArg in self.gmTimerArg[timerNoticeID]:
            self.popTimer(timerArg)
        del self.gmTimerArg[timerNoticeID]
        #return "delete success!"


    def delGMSchemeNotice(self, triggerTime, timerNoticeID,fileno):
        """
        define method
        GM工具删除定时公告与一组定时公告（多条公告）的接口
        :param schemeName:公告的Shceme名称
        :param triggerTime:指定的触发时间，like as: 0-59/2 0-23 1-31 1-12 0-7
        :param timerNoticeID:公告的ID
        :return:
        """
        if triggerTime not in self.noticeSchemes:
            KBEDebug.INFO_MSG("this notice is not exist!(triggerTime=%s)" % triggerTime)
            message = {"state": "fault", "message": "this notice is not exist!(triggerTime=%s)" % triggerTime}
            self.onOperationCB(message, fileno)
            return
        noticeKey = "GMNotice_%s" % timerNoticeID
        if self.crondMgr.isInSchemes(noticeKey, triggerTime):
            self.crondMgr.removeScheme(noticeKey, triggerTime)
        del self.noticeSchemes[triggerTime]
        self.delRecord(triggerTime)
        if timerNoticeID in self.gmTimerArg:
            self.delGMNotice(timerNoticeID)
        message = {"state": "success"}
        self.onOperationCB(message, fileno)



    def onTimer(self, tid, userArg):  # 对公告计时器触发时计时器字典中保存的信息进行处理，删除已触发的计时器信息
        self.timerBaseExt.onTimer(self, tid, userArg)
        for timerArg in list(self.gmTimerArg.items()):
            if userArg in timerArg[1]:
                del timerArg[1][userArg]
            if not timerArg[1]:
                self.delGMNotice(timerArg[0])  # 计时器触发，删除字典中保存得计时器信息，当为空时删除这个字典
                for notice in list(self.noticeSchemes.items()):
                    if timerArg[0] in notice[1]:
                        del self.noticeSchemes[notice[0]]
                        self.delRecord(notice[0])     #删除数据库记录



    def sendWorldGroupMsg(self, singleTime, noticeID, msgList):
        """
        发送一组内容不同的公告
        """
        for index, msg in enumerate(msgList):
            timerArg = self.addTimerCallBack(singleTime * index, "sendWorldNotice", (msg,))
            self.gmTimerArg[noticeID][timerArg] = timerArg


    def sendWorldNotice(self, msg):
        """
        发送单条公告
        """
        KST.g_baseAppEntity.globalWold(csstatus.GMTOOLS_ADD_CUSTOM_NOTICE, msg)


    def GMQueryAllNotices(self,fileno):
        """查询所有公告数据返回gm工具客户端"""
        self.onOperationCB(self.noticeSchemes, fileno)


    def onOperationCB(self,msg,fileno):
        message = json.dumps(msg)
        KBEngine.globalData["GMToolsManager"].onSendMsg(message, fileno)

    def globalWorld(self, messageType, message):
        KST.g_baseAppEntity.globalWold(messageType, message)



    def createRecord(self):

        def callback(result, rows, insertid, errstr):
            if errstr:
                KBEDebug.ERROR_MSG("create custom_notice table fail! %s" % errstr)

        sql= """CREATE TABLE IF NOT EXISTS `custom_notice` ( 
        `id`					int unsigned not null auto_increment,
        `triggerTime`                   Char(50),
        `noticeName`					Char(50),
        `intervalTime`                  INT ,
        `GroupTime`                     INT , 
        `count`                         INT ,
        `msg`                           VARCHAR(2048),
        primary key(`id`)
        ) ENGINE=InnoDB;"""

        KBEngine.executeRawDatabaseCommand(sql, callback)


    def queryAllRecord(self):
        def callback1(result, rows, insertid, errstr):
            if result:      #第一次创建数据库表，可能表还没创建好，数据库表没有数据，不需要从数据库加载公告数据
                sql2 = "SELECT * FROM `custom_notice`"
                KBEngine.executeRawDatabaseCommand(sql2, callback2)
                return
            self.onCompleteInit()
            self.isLoading = False

        def callback2(result, rows, insertid, errstr):
            if errstr:
                KBEDebug.ERROR_MSG("query custom_notice table fail! %s" % errstr)
                self.onCompleteInit()
                self.isLoading = False
                return
            self.load(result)

        sql1 = "SELECT table_name FROM information_schema.tables WHERE table_name ='custom_notice'"
        KBEngine.executeRawDatabaseCommand(sql1, callback1)



    def addRecord(self,schemeName, triggerTime, intervalTime, groupTime, count,msgList):
        content = ""
        i = 1
        length = len(msgList)
        for msg in msgList:
            if(i == length):
                content += msg
            else:
                content += msg+"|"
            i += 1
        def callback(result, rows, insertid, errstr):
            if errstr:
                KBEDebug.ERROR_MSG("insert  custom_notice raw fail! %s" % errstr)

        sql = "insert into `custom_notice` (`triggerTime` ,`noticeName`, `intervalTime`, `GroupTime`,`count`,`msg`) values ('%s','%s',%d,%d,%d,'%s')" %(triggerTime, schemeName, intervalTime, groupTime, count, content)
        KBEngine.executeRawDatabaseCommand(sql, callback)


    def delRecord(self,triggerTime):
        def callback(result, rows, insertid, errstr):
            if errstr:
                KBEDebug.ERROR_MSG("del custom_notice  raw fail! %s" % errstr)

        sql = "DELETE FROM `%s` WHERE `triggerTime`= '%s' " % ("custom_notice", triggerTime)
        KBEngine.executeRawDatabaseCommand(sql, callback)
