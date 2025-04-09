# -*- coding: utf-8 -*-

from . import csdefine, tooldefine

OPERATION_SUCCEED       = "操作成功"
CHANGE_SERVER_FAILED       = "切换服务器失败，%s服务器连接不上，请检查服务器启动情况以及数据库连接情况"
#--------------------------
#账号
#--------------------------
#账号管理
USER_MANAGE_GRADE_NOT_ENOUGH			= "你没有权限管理这个页面!"
USER_NAME_ERROR							= "错误：用户账号或用户名不能为空"
USER_MANAGE_ID_NOT_EXIST                = "错误：无效的管理员用户"
USER_TWO_PWD_DIFFER		            	= "错误：两次密码不一致"
SUPER_ADMIN_NUM_MAX		            	= "错误：超级管理员人数已到达最大值"
USER_GRADE_NOT_ENOUGH            	= "错误：权限不足"
USER_CHANGE_LEVEl_ERROR            	= "错误：等级错误"
USER_ID_IS_EXISTS            	= "错误：用户【%s】已存在"

#创建账号
USER_CREATE_PWD_ERROR			= "错误：密码不能为空"
USER_CREATE_GRAGE_NO			= "错误：普通账号必须有一项权限"
USER_CREATE_SUCCEED		    	= "用户新建成功！"
USER_CREATE_USER_NAME_EXIST     = "错误：用户【%s：%s】已存在"
USER_CREATE_NEED_SELECT_USET_TYPE     = "错误：请选择账号类型"

#编辑账号
USER_EDIT_USER_INVALID			= "错误：该用户无效"
USER_EDIT_SUCCEED				= "管理员账户编辑成功，用户名为 【 %s 】"

#删除账号
USER_DELETE_SUCCEED             = "账号【%s】删除成功"

#密码修改
USER_PASSWORD_OLD_PWD_ERROR     = "错误：原密码不正确！"
USER_PASSWORD_MODIFY_SUCCEED    = "密码修改成功！"

#服务器连接
BASE_CONNECT_FAILED             = "错误：连接baseapp服务器失败（%s：%s）！"
BASE_CONNECT_SUCCEED            = "连接成功！"

#数据处理
MSG_MGR_RECV_FORMAT_ERROR       = "错误：服务器返回数据格式不正确"
MSG_MGR_RECV_CONNECT_BY_CLOSE_ERROR       = "错误：连接被关闭，可能是上一次查询没有返回导致"
MSG_MGR_RECV_EXCEPTION_ERROR       = "错误：接收数据异常"

#查询
QUERY_SELECT_FIELD              = "错误：请填写完整的查询条件"
QUERY_DATA_FIELD              = "提示：未查询到相关记录"
QUERY_TIME_FORMAT_ERROR              = "错误：请选择正确的日期及时间区间"


#物品
ITEM_FORMAT_ERROR               = "错误：物品数据格式不对"
AWARD_SUBMIT_SUCCEED       ="申请提交成功"
AWARD_SUBMIT_ERROR       ="奖励发放失败"
AWARD_RETURN_SUCCEED       ="申请已被退回"
AWARD_DELETE_SUCCEED       ="申请已被删除"

#禁言
CHAT_INPUT_TIME                 = "错误：请输入禁言时长"
CHAT_NEED_SELECT                = "错误：请选择聊天频道"

#活动
ACTIVITY_START_TIME_ERROR       = "错误：活动开启时间格式错误，正确格式为（year-month-day hour:minute:second）"
ACTIVITY_START_TIME_NOT_INPUT   = "错误：请输入活动时间，格式为（year-month-day hour:minute:second）"
ACTIVITY_START_SUCCEED_NOW      = "活动已经开启"
ACTIVITY_START_SUCCEED_DELAY    = "活动将会在【%s】开启"
ACTIVITY_START_SUCCEED_DELAY_TIME_ERROR    = "错误：所选时间点已过"
ACTIVITY_END_SUCCEED            = "活动已关闭"
ACTIVITY_NO_END_METHOD            = "该活动不支持关闭功能"

#游戏账号
ACCOUNT_LOCK_NOT_TIME          = "错误：请输入封锁时长"
ACCOUNT_NOT_EXIST          = "错误：账号'%s'不存在"
ACCOUNT_TRUSTEESHIP_TIME_ERROR          = "错误：托管时长格式错误"
ACCOUNT_TRUSTEESHIP_PASSWORD_ERROR          = "错误：两次托管密码不一致"

#邮件管理
MAIL_SEND_SUCCESS	= "发送成功"
MAIL_SEND_NOT_ROLE_INFO	= "错误：请输入玩家信息"
MAIL_SEND_ITEM_INFO_FORMAT_ERROR	= "错误：物品数据信息格式错误"
MAIL_SEND_ITEM_INFO_NOT_DIGIT	= "错误：物品数据信息需要全部为数字"
MAIL_SEND_MONEY_NOT_DIGIT	= "错误：金钱数需要是整数"
MAIL_SEND_BIND_TYPE_ERROR	= "错误：绑定类型配置错误"
MAIL_SEND_ALL_NAME_ERROR = "发送失败，所有输入的玩家名字都不存在"
MAIL_SEND_PART_NAME_ERROR = "发送失败，部分玩家[ %s ]不存在"
MAIL_SEND_ITEM_ID_ALL_ERROR = "发放失败，所填物品不存在"
MAIL_SEND_ITEM_ID_PART_ERROR = "发送失败，部分物品[ %s ]不存在"
MAIL_SEND_ITEM_NUM_ERROR = "发放失败，当前最多支持发送4种物品"

#物品发放
ITEM_ISSUE_SUCCESS	= "发放成功"
ITEM_ISSUE_NOT_ROLE_INFO	= "错误：请输入玩家信息"
ITEM_ISSUE_NOT_ITME_INFO	= "错误：请输入物品数据信息"
ITEM_ISSUE_ITEM_INFO_FORMAT_ERROR	= "错误：物品数据信息格式错误"
ITEM_ISSUE_ITEM_INFO_NOT_DIGIT	= "错误：物品数据信息需要全部为数字"
ITEM_ISSUE_ALL_ROLE_ERROR = "错误：所有输入的玩家名字都不存在"
ITEM_ISSUE_PART_ROLE_ERROR = "发放失败，部分玩家[ %s ]不存在"
ITEM_ISSUE_ITEM_ID_ALL_ERROR = "发放失败，所填物品不存在"
ITEM_ISSUE_ITEM_ID_PART_ERROR = "发放失败，部分物品[ %s ]不存在"
ITEM_ISSUE_TITLE = "系统物品发放"

#玩家
ROLE_INFO_ERROR 	= "错误：未查到'%s'相关信息"
ROLE_INFO_NOT_EXIST 	= "错误：角色'%s'不存在"
ROLE_INFO_NOT_NAME_INPUT 	= "错误：请输入玩家名字"
ROLE_FREEZE_TIME_ERROR = "错误：角色冻结时长需为正数"

#公告
NOTICE_SEND_FIELD = "错误：请填写完整的发送条件"
NOTICE_SEND_NUMBER_INTERVAL_FORMAT_ERROR = "错误：发送次数或者间隔格式错误"
NOTICE_SEND_DATE_TIME_ERROR = "错误：定时发送时间不能早于当前时间"
NOTICE_CONTENT_LEN_ERROR = "错误：至少需要一条公告内容"


#消费监控
CHARGE_ORDER_QUERY_TYPE_ERROR = "错误：请选择查询方式"
CHARGE_ORDER_QUERY_ACCOUNT_NONE_ERROR = "错误：请输入账号名"
CHARGE_ORDER_QUERY_TOTALCHARGE_NONE_ERROR = "错误：请输入总充值额度"

COST_SINGLE_QUERY_TEXT_COND_ERROR = "错误：请选择查询方式"
COST_SINGLE_QUERY_TEXT_NONE_ERROR = "错误：请输入要查询的账号或者角色名字"
COST_SINGLE_QUERY_COIN_NONE_ERROR = "错误：请选择要查询的货币类型"