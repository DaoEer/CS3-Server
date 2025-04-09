# -*- coding: utf-8 -*-


from django.db import models
import time

# Create your models here.


class GMUser( models.Model ):
	class Meta:
		db_table = "gm_user"
	id = models.AutoField(primary_key = True)		#id，主键
	userID = models.CharField( max_length = 128, default = "", help_text = "用户账户ID", db_index = True )
	userName = models.CharField( max_length = 128, default = "", help_text = "用户名", db_index = True )
	password = models.CharField( max_length = 128, default = "", help_text = "密码" )
	level = models.IntegerField(default=3) #用户等级


class GMAwardRecord(models.Model):
	class Meta:
		db_table = "gm_awardRecord"
	id = models.AutoField(primary_key=True)		#id，主键
	applicationTime = models.CharField(max_length=128, default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))		#申请时间
	award_targetType = models.CharField(max_length=1280, default="")		#发奖对象类型
	award_title = models.CharField(max_length=30, default="")		#奖励标题
	award_reason = models.CharField(max_length=128, default="")		#发奖原因
	award_roleList = models.CharField(max_length=1280, default="")		#发奖名单
	award_itemList = models.CharField(max_length=128, default="")		#奖励列表
	applicant = models.CharField(max_length=30, default="")		#申请人
	sendState = models.SmallIntegerField(default=0)		#发送状态 0:待审核 1:发放完成 2:退回申请


class GMLog(models.Model):
	class Meta:
		# 此类可以当做父类，被其他model继承。字段自动过度给，继承的model
		abstract = True  # 【django以后做数据库迁移时， 不再为GMLog类创建相关的表以及表结构了】
	id = models.AutoField(primary_key = True)		#id，主键
	updateTime = models.DateTimeField( auto_now_add=True, help_text = "记录时间") #auto_now_add=True，自动添加到系统
	serverKey = models.CharField( max_length = 128, default = "", help_text = "服务器key")
	serverName = models.CharField( max_length = 128, default = "", help_text = "服务器名字")
	userID = models.CharField( max_length = 128, default = "", help_text = "操作者用户账号", db_index = True )
	userLevel = models.IntegerField( default = 0, help_text = "操作者用户等级" )
	actionType = models.IntegerField( default = 0, help_text = "操作类型" )
	
	
class GMUserLog(GMLog):
	class Meta:
		db_table = "gm_user_log"
	targetUserID = models.CharField( max_length = 128, default = "", help_text = "操作对象")
	targetUserLevel = models.IntegerField( default = 0, help_text = "操作对象等级" )
	param1 = models.CharField( max_length = 128, default = "", help_text = "扩展参数1")
	param2 = models.CharField( max_length = 128, default = "", help_text = "扩展参数2")
	param3 = models.CharField( max_length = 128, default = "", help_text = "扩展参数3")
	
	
class GMAccountMgrLog(GMLog):
	class Meta:
		db_table = "gm_acc_mgr_log"
	targetAccount = models.CharField( max_length = 128, default = "", help_text = "操作账号")
	param1 = models.CharField( max_length = 128, default = "", help_text = "扩展参数1")
	param2 = models.CharField( max_length = 128, default = "", help_text = "扩展参数2")
	param3 = models.CharField( max_length = 128, default = "", help_text = "扩展参数3")
	
	
class GMRoleMgrLog(GMLog):
	class Meta:
		db_table = "gm_role_mgr_log"
	targetRole = models.CharField( max_length = 128, default = "", help_text = "操作角色")
	param1 = models.CharField( max_length = 128, default = "", help_text = "扩展参数1")
	param2 = models.CharField( max_length = 128, default = "", help_text = "扩展参数2")
	param3 = models.CharField( max_length = 128, default = "", help_text = "扩展参数3")
	
	
class GMActivityMgrInfo(GMLog):
	class Meta:
		db_table = "gm_activity_log"
	activityKey = models.CharField( max_length = 128, default = "", help_text = "活动key")
	activityName = models.CharField( max_length = 128, default = "", help_text = "活动名字")
	param1 = models.CharField( max_length = 128, default = "", help_text = "扩展参数1")


class GMItemMgrLog(GMLog):
	class Meta:
		db_table = "gm_item_mgr_log"
	targetType = models.IntegerField(default = 0, help_text = "公告次数")
	roleList = models.TextField(default = "", help_text = "玩家信息")
	itemList = models.CharField( max_length = 128, default = "", help_text = "物品信息")
	title = models.CharField( max_length = 128, default = "", help_text = "标题")
	content = models.CharField( max_length = 255, default = "", help_text = "内容")
	param1 = models.CharField( max_length = 128, default = "", help_text = "扩展参数1")
	param2 = models.CharField( max_length = 128, default = "", help_text = "扩展参数2")
	param3 = models.CharField( max_length = 128, default = "", help_text = "扩展参数3")
	
	
class GMMailMgrLog(GMLog):
	class Meta:
		db_table = "gm_mail_mgr_log"
	targetType = models.IntegerField(default = 0, help_text = "公告次数")
	roleList = models.TextField(default = "", help_text = "玩家信息")
	itemList = models.CharField( max_length = 128, default = "", help_text = "物品信息")
	title = models.CharField( max_length = 128, default = "", help_text = "标题")
	content = models.CharField( max_length = 255, default = "", help_text = "内容")
	moneyAmount = models.IntegerField(default = 0, help_text = "公告间隔时间")
	
	
class GMNoticeMgrLog(GMLog):
	class Meta:
		db_table = "gm_notice_mgr_log"
	noticeTimes = models.IntegerField(default = 0, help_text = "公告次数")
	intervalTime = models.IntegerField(default = 0, help_text = "公告间隔时间")
	title = models.CharField( max_length = 128, default = "", help_text = "标题")
	content = models.TextField(default = "", help_text = "内容") #多条功能内容可能比较多
	param1 = models.CharField( max_length = 128, default = "", help_text = "扩展参数1")
	param2 = models.CharField( max_length = 128, default = "", help_text = "扩展参数2")
	param3 = models.CharField( max_length = 128, default = "", help_text = "扩展参数3")
	
	