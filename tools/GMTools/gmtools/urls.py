# -*- coding: utf-8 -*-


from django.conf.urls import url
from . import views
from .luoCode import login
from .luoCode import userMgr
from .luoCode import mailMgr, queryMgr, roleMgr, accountMgr, activityMgr, itemMgr, mailMgr, server, noticeMgr, DataMonitor


activityInstance = activityMgr.g_activityInstance
loginInstannce = login.g_loginInstance
userInstance = userMgr.g_userInstance
mailInstance = mailMgr.g_mailInstance
queryInstance = queryMgr.g_queryInstance
roleInstance = roleMgr.g_roleInstance
itemInstance = itemMgr.g_itemInstance
accountInstance = accountMgr.g_accountInstance
serverInstance = server.g_serverInstance
indexInstance = views.g_IndexInstance
noticeInstance = noticeMgr.g_noticeInstance
dataMonitorInstance = DataMonitor.g_dataMonitorInstance

urlpatterns = [
    url( r"^$", indexInstance.index, name = "index" ),
    url( r"^index", indexInstance.index, name = "index" ),

    #修改服务器
    url( r"^server_change/$", serverInstance.server_change, name = "server_change" ),
    
    #登录
    url( r"^login$", loginInstannce.login, name = "login" ),
    url( r"^logout/$", loginInstannce.logout, name = "logout" ),

    #用户管理
    url( r"^user_manage/$", userInstance.user_manage, name = "user_manage" ),
    url( r"^user_manage/new/$", userInstance.user_manage_new, name = "user_manage_new" ),
    url( r"^user_manage/new/create/$", userInstance.user_manage_new_create, name = "user_manage_new_create" ),
    url( r"^user_manage/edit/(?P<dbid>[0-9]+)/$", userInstance.user_manage_edit, name = "user_manage_edit" ),
    url( r"^user_manage/delete/(?P<dbid>[0-9]+)/$", userInstance.user_manage_delete, name = "user_manage_delete" ),
    url( r"^user_manage/password/(?P<dbid>[0-9]+)/$", userInstance.user_manage_password, name = "user_manage_password" ),
    
    #游戏账号管理
    url(r"^account/$", accountInstance.account, name = "account"),
    url(r"^account/lock/$", accountInstance.lock, name = "lock"),
    url(r"^account/lock_batch/$", accountInstance.lock_batch, name = "lock_batch"),
    url(r"^account/unlock/$", accountInstance.unlock, name = "unlock"),
    url(r"^account/unlock_batch/$", accountInstance.unlock_batch, name = "unlock_batch"),
    url(r"^account/query_info/$", accountInstance.account_query_info, name = "query_info"),
    url(r"^account/trusteeship/base$", accountInstance.account_trusteeship_base, name = "account_trusteeship_base"),
    url(r"^account/trusteeship/query$", accountInstance.account_trusteeship_query, name = "account_trusteeship_query"),
    url(r"^account/trusteeship/$", accountInstance.account_trusteeship, name = "account_trusteeship"),
    url(r"^account/trusteeship/action/$", accountInstance.account_trusteeship_action, name = "account_trusteeship_action"),
    url(r"^account/state/query$", accountInstance.account_state_query, name = "account_state_query"),
    url(r"^account/state/exportdata/$", accountInstance.account_state_export_data, name = "account_state_export_data"),
    url(r"^account/state/query/action/$", accountInstance.queryAccountStateInfo, name = "queryAccountStateInfo"),

    #角色管理
    url(r"^role/$", roleInstance.role, name = "role" ),
    url(r"^role/kick/$", roleInstance.role_kick, name = "role_kick" ),
    url(r"^role/chat/ungag$", roleInstance.role_chat_unLockGag, name = "role_chat_unLockGag" ),
    url(r"^role/chat/gag$", roleInstance.role_chat_gag, name = "role_chat_gag" ),
    url(r"^role/query_info/$", roleInstance.role_query_info, name = "role_query_info" ),
    url(r"^role/query_activity/$", roleInstance.role_query_activity, name = "role_query_activity" ),
    url(r"^role/query_coin/$", roleInstance.role_query_coin, name = "role_query_coin" ),
    url(r"^role/query_pet/$", roleInstance.role_query_pet, name = "role_query_pet" ),
    url(r"^role/query_item/$", roleInstance.role_query_item, name = "role_query_item"),
    url(r"^role/role_freeze/$", roleInstance.role_freeze, name = "role_freeze"),
    url(r"^role/role_unfreeze/$", roleInstance.role_unfreeze, name = "role_unfreeze"),
    url(r"^role/trantorevivepos/$", roleInstance.role_tranToRevivePosition, name = "role_tranToRevivePosition"),

    #活动管理
    url(r"^activity/$", activityInstance.activity_manage, name = "activity_manage"),
    url(r"^activity/action/$", activityInstance.activity_action, name = "activity_action"),
    url(r"^activity/delete/$", activityInstance.activity_delete, name = "activity_delete"),
    #url(r"^activity/open/$", activityMgr.activity_open, name = "activity_open" ),
    #url(r"^activity/close/$", activityMgr.activity_close, name = "activity_close" ),
    #url(r"^activity/cancel/$", activityMgr.activity_cancel, name = "activity_cancel" ),
    #url(r"^activity/cancel/send/$", activityMgr.activity_cancel_send, name = "activity_cancel_send" ),

    #物品管理
    url(r"^item/$", itemInstance.item, name="item"),
    url(r"^item/item_query/$", itemInstance.item_query, name="item_query"),
    url(r"^item/item_issue/$", itemInstance.item_issue, name="item_issue"),
    url(r"^item/item_issue/result/$", itemInstance.item_issue_result, name="item_issue_result"),
    url(r"^item/item_issue/application/$", itemInstance.item_issue_application, name="item_issue_application"),
    url(r"^item/item_issue/query_awards/$", itemInstance.item_issue_queryAwards, name="item_issue_queryAwards"),
    url(r"^item/item_issue/query_awardRoleInfo/$", itemInstance.item_issue_queryAwardRoleInfo, name="item_issue_queryAwardRoleInfo"),
    url(r"^item/item_issue/delete_application/$", itemInstance.item_issue_deleteApplication, name="item_issue_deleteApplication"),
    url(r"^item/item_issue/award_record_edit/$", itemInstance.item_issue_awardRecordEdit, name="item_issue_awardRecordEdit"),


    #y邮件管理
    url(r"^mail/$", mailInstance.mail, name="mail"),
    url(r"^mail/send/$", mailInstance.mail_send, name="mail_send"),
    url(r"^mail/send/result$", mailInstance.mail_send_result, name="mail_send_result"),

    #查询
    url( r"^query/$", queryInstance.query, name = "query" ),
    url( r"^query/role_upgrade/$", queryInstance.query_role_upgrade, name = "query_role_upgrade" ),
    url( r"^query/role_upgrade/result$", queryInstance.query_role_upgrade_result, name = "query_role_upgrade_result" ),
    url( r"^query/role_skillLearn/$", queryInstance.query_role_skill_learn, name = "query_role_skill_learn" ),
    url( r"^query/role_mail/$", queryInstance.query_role_mail, name = "query_role_mail" ),
    url( r"^query/role_vend/$", queryInstance.query_role_vend, name = "query_role_vend" ),
    url( r"^query/role_item/$", queryInstance.query_role_item, name = "query_role_item" ),
    url( r"^query/role_itemRecord/$", queryInstance.query_role_itemRecord, name = "query_role_itemRecord" ),
    url( r"^query/role_position/$", queryInstance.query_role_position, name = "query_role_position" ),
    url( r"^query/role_equip/$", queryInstance.query_role_equip, name = "query_role_equip" ),
    url( r"^query/role_attribute/$", queryInstance.query_role_attribute, name = "query_role_attribute" ),
    url( r"^query/role_task/$", queryInstance.query_role_task, name = "query_role_task" ),
    url( r"^query/role_money/$", queryInstance.query_role_money, name = "query_role_money" ),
    url( r"^query/role_recharge/$", queryInstance.query_role_recharge, name = "query_role_recharge" ),

    #公告管理
    url( r"^notice/$", noticeInstance.noticeBase, name = "noticeBase" ),
    url( r"^notice/instantnotice/$", noticeInstance.noticeInstant, name = "noticeInstant" ),
    url( r"^notice/timingnotice/$", noticeInstance.noticeTiming, name = "noticeTiming" ),
    url( r"^notice/multiplenotice/$", noticeInstance.noticeMultiple, name = "noticeMultiple" ),
    url( r"^notice/delete/$", noticeInstance.notice_delete, name = "notice_delete"),
    
    #数据监控
    url( r"^datamonitor/$", dataMonitorInstance.dataMonitorBase, name = "dataMonitorBase" ),
    url( r"^datamonitor/onlinedata/$", dataMonitorInstance.onLineData, name = "onLineData" ),
    url( r"^datamonitor/onlinedata/query/$", dataMonitorInstance.onLineDataQuery, name = "onLineDataQuery" ),
    url( r"^datamonitor/chargedata/$", dataMonitorInstance.chargeData, name = "chargeData" ),
    url( r"^datamonitor/chargedata/totalquery/$", dataMonitorInstance.chargeDataTotalquery, name = "chargeDataTotalQuery" ),
    url( r"^datamonitor/chargedata/ordersquery/$", dataMonitorInstance.chargeDataOrdersQuery, name = "chargeDataOrdersQuery" ),
    url( r"^datamonitor/coindata/$", dataMonitorInstance.coinData, name = "coinData" ),
    url( r"^datamonitor/coindata/query/$", dataMonitorInstance.coinDataQuery, name = "coinDataQuery" ),
    url( r"^datamonitor/costdata/$", dataMonitorInstance.costData, name = "costData" ),
    url( r"^datamonitor/costdata/totalquery/$", dataMonitorInstance.costDataTotalQuery, name = "costDataTotalQuery" ),
    url( r"^datamonitor/costdata/singlequery/$", dataMonitorInstance.costDataSingleQuery, name = "costDataSingleQuery" ),
    
]
