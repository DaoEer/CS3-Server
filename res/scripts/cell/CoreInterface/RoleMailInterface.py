# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import csstatus
import csconst
import KBEngine
import json
import ItemFactory


class RoleMailInterface:
    """
    玩家邮件接口
    """

    def __init__(self):
        """
        """
        pass

    def mail_send(self, receiverName, title, content, receiverBase):
        """
        玩家寄信，此接口由base调用，也就是说发送邮件的过程是client -> base -> cell -> mailmanager,
        使用此流程而不使用client -> cell -> mailmanager是因为发送邮件时需要确认收信者是存在的。

        receiverName 收信人名字
        title 标题
        content 内容
        receiverBase 收信人的baseMailBox
        """
        # 付邮资
        if self.subBindMoney(csconst.MAIL_SEND_COST, csdefine.MONEY_SUB_REASON_PAY_FOR_MAIL_BILL) == False:
            self.statusMessage(csstatus.MAIL_SEND_HAS_NOT_ENOUGH_MONEY, "")
            return

        KBEngine.globalData["MailManager"].sendWithMailbox(self.base, receiverBase, receiverName,
                                                           csdefine.MAIL_SENDER_TYPE_PLAYER, self.getName(), title,
                                                           content, 0, 0, [], 0, 0)

    # -----------------------------------提取邮件--------------------------
    def CELL_extractMail(self, srcEntityID, mailIDs):
        """
        exposed method
        提取附件
        """
        if not self.validateClientCall(srcEntityID):
            return
        if self.isKitBagLock():
            self.statusMessage(csstatus.CIB_MSG_KITBAG_LOCKED, "")
            return
        for mailID in mailIDs:
            self.base.extractOneMail(int(mailID))

    def extractMailCB(self, mailID, money, itemList, bindMoney):
        """
        获取邮件附带金钱、物品
        过程：邮件金钱数据是由玩家base发送过来的。接着在这里进行正式获得处理。并且还需要在正式获得后，到base和数据库分别记录。
        """
        # 金钱是否超过最高限定
        if money != 0 and self.addMoney(money, csdefine.MONEY_ADD_REASON_MAIL) == False:
            self.base.extractMailState(mailID, False)
            return

        if bindMoney != 0 and not self.addBindMoney(bindMoney, csdefine.MONEY_ADD_REASON_MAIL):
            self.base.extractMailState(mailID, False)
            return

        result = self.addItemList(itemList, csdefine.ITEM_ADD_BY_MAIL)
        if result != csstatus.ITEM_GO_ON:
            self.statusMessage(csstatus.STORE_BAG_HAS_ENOUGH)
            self.base.extractMailState(mailID, False)
            return

        self.base.extractMailState(mailID, True)
