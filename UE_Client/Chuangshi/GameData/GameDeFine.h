#pragma once

/**
* 文件名称：GameDeFine.h
* 功能说明：游戏的全局性定义
* 文件作者：ranxuanwen
* 目前维护：wuxiaoou
* 创建时间：2016-10-31
*/


///游戏状态
UENUM(Blueprintable)
enum class EGameStatus : uint8
{
	///账号登录
	Login = 1,
	///角色选择
	SelectRole = 2,
	///阵营选择
	SelectCamp = 3,
	///角色创建
	CreateRole = 4,
	///角色捏脸
	Personalize = 5,
	///场景加载
	Teleport = 6,
	///游戏世界
	InWorld = 7,
	///离线状态
	Logoff = 8,
	///角色更衣
	ChangeClothes = 9
};

///登录阶段
UENUM(Blueprintable)
enum class ELoginStage : uint8
{
	///未登录阶段
	StageNoLogin = 1,
	///尝试登录阶段（新增）
	StageTryLogin,
	///账号登录阶段
	StageAccountLogin,
	///角色登录阶段
	StageRoleLogin
};

///单位的基本状态
UENUM(BlueprintType)
enum class ENTITY_STATE : uint8
{
	///0-未决状态（服务器在传送完就会改成普通状态，基本不能应用于客户端检测）
	EntityStatePead			= 0 UMETA(DisplayName = "EntityStatePead"),
	///1-普通状态
	EntityStateFree			= 1 UMETA(DisplayName = "EntityStateFree"),
	///2-警戒状态
	EntityStateWarn			= 2 UMETA(DisplayName = "EntityStateWarn"),
	///3-战斗状态
	EntityStateFight		= 3 UMETA(DisplayName = "EntityStateFight"),
	///4-死亡状态
	EntityStateDead			= 4 UMETA(DisplayName = "EntityStateDead"),
	///5-重置状态（怪物特有）
	EntityStateReset		= 5 UMETA(DisplayName = "EntityStateReset"),
	///6-表演状态（怪物特有）
	EntityStateShow			= 6 UMETA(DisplayName = "EntityStateShow"),
	///7-摆摊状态
	EntityStateStall		= 7 UMETA(DisplayName = "EntityStateStall"),
	///8-稳定状态
	EntityStateStable		= 8 UMETA(DisplayName = "EntityStateStable"),
	///状态最大值（高于此值视为无效状态）
	EntityStateMax			= 9 UMETA(DisplayName = "EntityStateMax"),
};

UENUM(BlueprintType)
enum class EQUIP_PART : uint8
{
	///
	EQUIP_BODY	= 10 UMETA(DisplayName = "EQUIP_BODY"),
	///
	EQUIP_HEAD	= 11 UMETA(DisplayName = "EntityStateFight"),
	///
	EQUIP_SUIT	= 12 UMETA(DisplayName = "EntityStateReset"),
	///
	EQUIP_HAIR	= 13 UMETA(DisplayName = "EntityStateDead"),
	///
	EQUIP_COAT	= 21 UMETA(DisplayName = "EntityStateMax"),
};

UENUM(BlueprintType)
enum class GROUP_END_TYPE : uint8
{
	///无限制
	GROUP_END_TIME_NONE					= 0 UMETA(DisplayName = "GROUP_END_TIME_NONE"),
	///30天
	GROUP_END_TIME_ONE_MONTH			= 1 UMETA(DisplayName = "GROUP_END_TIME_ONE_MONTH"),
	///60天
	GROUP_END_TIME_TWO_MONTH			= 2 UMETA(DisplayName = "GROUP_END_TIME_TWO_MONTH"),
	///90天
	GROUP_END_TIME_THREE_MONTH			= 3 UMETA(DisplayName = "GROUP_END_TIME_THREE_MONTH"),
};

UENUM(BlueprintType)
enum class ACTION_FLAG : uint8
{
	///0-禁止移动（只限制主动位移，不限制受击等被迫位移）
	ACTION_FORBID_MOVE					= 0 UMETA(DisplayName = "ForbidMove"),
	///1-禁止施法
	ACTION_FORBID_SPELL					= 1 UMETA(DisplayName = "ForbidSpell"),
	///2-禁止使用道具
	ACTION_FORBID_USE_ITEM				= 2 UMETA(DisplayName = "ForbidItem"),
	///3-禁止受击
	ACTION_FORBID_BE_ATTACK				= 3 UMETA(DisplayName = "ForbidBeAttack"),
	///4-禁止攻击（普通物理攻击）
	ACTION_FORBID_ATTACK				= 4 UMETA(DisplayName = "ForbidAttack"),
	///5-禁止跳跃
	ACTION_FORBID_JUMP					= 5 UMETA(DisplayName = "ForbidJump"),
	///6-禁止装备物品
	ACTION_FORBID_WIELD					= 6 UMETA(DisplayName = "ForbidWield"),
	///7-禁止聊天
	ACTION_FORBID_CHAT					= 7 UMETA(DisplayName = "ForbidChat"),
	///8-禁止与NPC对话
	ACTION_FORBID_TALK					= 8 UMETA(DisplayName = "ForbidTalk"),
	///9-禁止被动技能触发
	ACTION_FORBID_TRIGGER_PASSIVE		= 9 UMETA(DisplayName = "ForbidTriggerPassiveSkill"),
	///10-禁止被击退
	ACTION_FORBID_BE_HIT_BACK			= 10 UMETA(DisplayName = "ForbidBeHitBack"),
	///11-禁止变身
	ACTION_FORBID_CHANGE_BODY			= 11 UMETA(DisplayName = "ForbidChangeBody"),
	///12-禁止变换姿势
	ACTION_FORBID_CHANGE_POSTURE		= 12 UMETA(DisplayName = "ForbidChangePosture"),
	///13-禁止召唤幻兽
	ACTION_FORBID_CONJURE_PET			= 13 UMETA(DisplayName = "ForbidConjurePet"),
	///14-禁止改变朝向（移动时的朝向不影响）
	ACTION_FORBID_TRANSLATE_DIRECTION	= 14 UMETA(DisplayName = "ForbidTranslateDirection"),
	///15-禁止紧急回避
	ACTION_FORBID_EMERGENCY_EXIT		= 15 UMETA(DisplayName = "ForbidEmergencyExit"),
	///16-禁止上马
	ACTION_FORBID_MOUNT_PET				= 16 UMETA(DisplayName = "ForbidMountPet"),
	///17-禁止控制
	ACTION_FORBID_BE_CONTROL			= 17 UMETA(DisplayName = "ForbidBeControl"),
	///18-禁止被良性增益
	ACTION_FORBID_BE_IMPRESS			= 18 UMETA(DisplayName = "ForbidBeImpress"),
	///19-禁止被恶性减损
	ACTION_FORBID_BE_DEPRESS			= 19 UMETA(DisplayName = "ForbidBeDepress"),
	///20-禁止心智失常
	ACTION_FORBID_INSANE				= 19 UMETA(DisplayName = "ForbidInsane"),
	///无条件
	ACTION_FORBID_NONE					= 255 UMETA(DisplayName = "ForbidNone"),
};

UENUM(BlueprintType)
enum class TRADE_STATE : uint8
{
	///0-没有交易
	TRADE_STATE_NULL		= 0 UMETA(DisplayName = "Null"),
	///1-正在申请交易
	TRADE_STATE_INVITE		= 1 UMETA(DisplayName = "Invite"),
	///2-被申请交易
	TRADE_STATE_WAIT		= 2 UMETA(DisplayName = "Wait"),
	///3-交易开始
	TRADE_STATE_BEGIN		= 3 UMETA(DisplayName = "Begin"),
	///4-交易物品锁定
	TRADE_STATE_LOCK		= 4 UMETA(DisplayName = "Lock"),
	///5-物品交换
	TRADE_STATE_SURE		= 5 UMETA(DisplayName = "Sure"),
};

UENUM(BlueprintType)
enum class QUEST_TYPE : uint8
{
	///1-主线任务
	QUEST_TYPE_MAILLINE 	= 1 UMETA(DisplayName = "MailLine"),
	///2-支线任务
	QUEST_TYPE_BRANCH		= 2 UMETA(DisplayName = "Branch"),
	///3-日常任务
	QUEST_TYPE_DAILY		= 3 UMETA(DisplayName = "Daily"),
	///4-环任务
	QUEST_TYPE_LOOP			= 4 UMETA(DisplayName = "Loop"),
	///5-金树种子
	QUEST_TYPE_JSZZ			= 5 UMETA(DisplayName = "JSZZ"),
	///6-通天塔
	QUEST_TYPE_TTD			= 6 UMETA(DisplayName = "TTD"),
	///7-奇缘
	QUEST_TYPE_QIYUAN		= 7 UMETA(DisplayName = "QiYuan"),
};

UENUM(BlueprintType)
enum class QUEST_STATE : uint8
{	
	///1-任务未做过（任务未接受：包含达到接受任务条件但未接受、未达到接受任务条件）
	QUEST_NOT_ACCEPT		= 1 UMETA(DisplayName = "NotAcceptQuest"),
	///2-任务已完成（任务已接受，且任务目标全部达成）
	QUEST_IS_DONE			= 2 UMETA(DisplayName = "QuestIsDone"),
	///3-任务未完成（任务已接受，但任务目标未全部达成）
	QUEST_NOT_DONE			= 3 UMETA(DisplayName = "QuestNotDone"),
	///4-任务已做过（任务已完成，并提交了任务）
	QUEST_HAD_FINISH		= 4 UMETA(DisplayName = "QuestHadFinish"),
};

UENUM(BlueprintType)
enum class NPC_QUEST_SIGN_TYPE : uint8
{
	///0-无可接任务
	SIGN_NO_ACCEPT			= 0 UMETA(DisplayName = "SignNoQuest"),
	///1-任务可接
	SIGN_NOT_ACCEPT			= 1 UMETA(DisplayName = "SignNotAccept"),
	///2-任务可提交
	SIGN_IS_DONE			= 2 UMETA(DisplayName = "SignIsDone"),
	///3-任务未完成
	SIGN_NOT_DONE			= 3 UMETA(DisplayName = "SignNotDone"),
};

UENUM(BlueprintType)
enum class QUEST_TASK_STATE : uint8
{
	///2-任务目标已完成
	TASK_IS_DONE			= 2 UMETA(DisplayName = "TaskIsDone"),
	///3-任务目标未完成
	TASK_NOT_DONE			= 3 UMETA(DisplayName = "TaskNotDone"),
};

UENUM(BlueprintType)
enum class ROLE_FLAG : uint8
{
	///1-观察者标志位
	ROLE_FLAG_WATCHER		= 1 UMETA(DisplayName = "RoleFlagWatcher"),
	///2-队伍标志位
	ROLE_FLAG_TEAMMING		= 2 UMETA(DisplayName = "RoleFlagTeamming"),
};

UENUM(BlueprintType)
enum class ENTITY_FLAG : uint8
{	
	FLAG_RELATION_ENEMY_TO_ROLE			= 1 UMETA(DisplayName = "EnemyToRole"),				///1-怪物和玩家可以互相攻击
	FLAG_RELATION_NORMAL_TO_ROLE		= 2 UMETA(DisplayName = "NormalToRole"),			///2-怪物和玩家不可以互相攻击
	FLAG_RELATION_ENEMY_TO_MONSTER		= 3 UMETA(DisplayName = "EnemyToMonster"),			///3-怪物和怪物可以互相攻击
	FLAG_RELATION_NORMAL_TO_MONSTER		= 4 UMETA(DisplayName = "NormalToMonster"),			///4-怪物和怪物不可以互相攻击

	FLAG_AI_TICK						= 7 UMETA(DisplayName = "AITick"),					///7-不在玩家AOI范围内也可以开始AITick
	FLAG_UNVISIBLE						= 8 UMETA(DisplayName = "UnVisible"),				///8-对象不可见
	FLAG_CAN_FLY						= 9 UMETA(DisplayName = "CanFly"),					///9-对象可浮空
	FLAG_CANT_MOVE_AND_ROTATE			= 10 UMETA(DisplayName = "CanNotMoveAndRotate"),	///10-不能移动和转向
	FLAG_CANT_SELECTED					= 11 UMETA(DisplayName = "CanNotSelected"),			///11-不能被选中
	FLAG_OPEN_COLLISION					= 12 UMETA(DisplayName = "OpenCollision"),			///12-开启全部碰撞
	FLAG_HIDE_FLOAT_NAME				= 13 UMETA(DisplayName = "HideFloatName"),			///13-屏蔽头顶名字
	FLAG_HIDE_FLOAT_HPBAR				= 14 UMETA(DisplayName = "HideFloatHPBar"),			///14-屏蔽头顶血条
	FLAG_HIDE_FLOAT_LEVEL				= 15 UMETA(DisplayName = "HideFloatLevel"),			///15-屏蔽头顶等级
	FLAG_SHOW_FLOAT_NAME				= 16 UMETA(DisplayName = "ShowFloatName"),			///16-显示头顶名字
	FLAG_SHOW_FLOAT_HPBAR				= 17 UMETA(DisplayName = "ShowFloatHPBar"),			///17-显示头顶血条
	FLAG_SHOW_FLOAT_LEVEL				= 18 UMETA(DisplayName = "ShowFloatLevel"),			///18-显示头顶等级
	FLAG_WANDER							= 19 UMETA(DisplayName = "Wander"),					///19-游荡
	FLAG_RELATION_EMENY_TO_ROLE			= 20 UMETA(DisplayName = "RelationEmenyToRole"),	///20-陷阱单向敌对玩家
	FLAG_RELATION_FRIEND_TO_ROLE		= 21 UMETA(DisplayName = "RelationFirendToRole"),	///21-陷阱单向友好玩家
	FLAG_USE_SERVER_FLAG				= 22 UMETA(DisplayName = "UseServerFlag"),			///22-使用服务器追击
	FLAG_CLOSE_COLLISION				= 23 UMETA(DisplayName = "CloseCollision"),			///23-关闭全部碰撞
	FLAG_MESH_COLLISION					= 24 UMETA(DisplayName = "MeshCollision"),			///24-开启mesh和staticmesh的碰撞
	FLAG_STOP_BULLET					= 25 UMETA(DisplayName = "StopBullet"),				///25-子弹杀手
	FLAG_SHOW_FLOAT_DAMAGEBAR			= 26 UMETA(DisplayName = "ShowFloatDamageBar"),		///26-显示头顶伤害进度条
	FLAG_OPEN_CAMERA_COLLISION			= 28 UMETA(DisplayName = "OpenCameraCollision"),	///28-开启摄像机碰撞
	FLAG_NOT_RESET_SPAWNDIR				= 29 UMETA(DisplayName = "OpenCameraCollision"),	///29-回走结束不重置出生点朝向
	FLAG_CAN_BE_TREAD					= 30 UMETA(DisplayName = "CanStand"),				///30-玩家是否站立里
	FLAG_OPEN_GROUND_TRACE_COLLISION_CHANNEL = 31 UMETA(DisplayName = "OpenGroundTrace"),	///31-开启光线碰撞通道-地面（用来做entity可以站上去表现）
};

UENUM(BlueprintType)
enum class REWARED_TYPE : uint8
{
	REWARD_TYPE_MONEY					= 1 UMETA(DisplayName = "REWARD_MONEY"),			///金币奖励
	REWARD_TYPE_EXP						= 2 UMETA(DisplayName = "REWARD_EXP"),				///经验奖励
	REWARD_TYPE_ITEM					= 3 UMETA(DisplayName = "REWARD_ITEM"),				///物品奖励
	REWARD_TYPE_SKILL					= 4 UMETA(DisplayName = "REWARD_SKILL"),			///技能奖励
	REWARD_TYPE_XIUWEI					= 5 UMETA(DisplayName = "REWARD_XIUWEI"),			///修为奖励
	REWARD_TYPE_POTENTIAL				= 6 UMETA(DisplayName = "REWARD_POTENTIAL"),		///潜能奖励
	REWARD_TYPE_ITEM_CHOOSE				= 7 UMETA(DisplayName = "REWARD_ITEM_CHOOSE"),		///可选物品奖励
	REWARD_TYPE_TITLE					= 8 UMETA(DisplayName = "REWARD_TYPE_TITLE"),		///称号奖励
	REWARD_TYPE_CONTRIBUTE				= 9	UMETA(DisplayName = "REWARD_TYPE_CONTRIBUTE"),	///帮贡奖励
	REWARD_TYPE_TONG_MONEY				= 10 UMETA(DisplayName = "REWARD_TYPE_TONG_MONEY"),	///帮会资金奖励
	REWARD_TYPE_REWARD_ID				= 11 UMETA(DisplayName = "REWARD_TYPE_REWARD_ID"),	///根据奖励ID奖励
	REWARD_TYPE_BARRACKS_EXP			= 12 UMETA(DisplayName = "REWARD_TYPE_BARRACKS_EXP"),///养兵经验奖励
};

UENUM(BlueprintType)
enum class RELATION_SHIP : uint8
{
	ROLE_RELATION_FRIEND				= 0 UMETA(DisplayName = "FRIEND"),					///好友
	ROLE_RELATION_BLACKLIST				= 1 UMETA(DisplayName = "BLACKLIST"),				///黑名单
	ROLE_RELATION_FOE					= 2 UMETA(DisplayName = "FOE"),						///仇人
	ROLE_RELATION_LAST_CHAT				= 3 UMETA(DisplayName = "LASTCHAT"),				///最近联系人
};


UENUM(BlueprintType)
enum class ADD_ITEM_REASON : uint8
{
	ITEM_ADD_BY_PICKUP			= 0 UMETA(DisplayName = "ITEM_ADD_BY_PICKUP"),	///拾取增加物品
	ITEM_ADD_BY_SYS				= 1 UMETA(DisplayName = "ITEM_ADD_BY_SYS"),	///系统赠送
	ITEM_ADD_BY_NPCTRADE		= 2 UMETA(DisplayName = "ITEM_ADD_BY_NPCTRADE"),	///NPC处购买
	ITEM_ADD_BY_ROLETRADE		= 3 UMETA(DisplayName = "ITEM_ADD_BY_ROLETRADE"),	///玩家交易
	ITEM_ADD_BY_QUEST			= 4 UMETA(DisplayName = "ITEM_ADD_BY_QUEST"),	///任务奖励获得物品
	ITEM_ADD_BY_QUESTACTION		= 5 UMETA(DisplayName = "ITEM_ADD_BY_QUESTACTION"),	///任务行为获得物品
	ITEM_ADD_BY_GM_COMMAND		= 6 UMETA(DisplayName = "ITEM_ADD_BY_GM_COMMAND"),	///GM添加物品
	ITEM_ADD_BY_SKILL			= 7 UMETA(DisplayName = "ITEM_ADD_BY_SKILL"),	///技能添加物品
	ITEM_ADD_BY_BORN_GAIN		= 8 UMETA(DisplayName = "ITEM_ADD_BY_BORN_GAIN"),	///出生赋值
	ITEM_ADD_BY_ADDCHECK		= 9 UMETA(DisplayName = "ITEM_ADD_BY_ADDCHECK"),	///添加物品检测，并不会添加物品
	ITEM_ADD_BY_STALLTRADE		= 10 UMETA(DisplayName = "ITEM_ADD_BY_STALLTRADE"),	///摆摊
	ITEM_ADD_BY_USE_GIFT_ITEM	= 11 UMETA(DisplayName = "ITEM_ADD_BY_USE_GIFT_ITEM"),	///打开礼包
	ITEM_ADD_BY_SHOPMALLTRADE	= 12 UMETA(DisplayName = "ITEM_ADD_BY_SHOPMALLTRADE"),	///商城处购买
	ITEM_ADD_BY_OPEN_SPELLBOX	= 13 UMETA(DisplayName = "ITEM_ADD_BY_OPEN_SPELLBOX"),	///打开宝箱
	ITEM_ADD_BY_SPELLBOX_KEY	= 14 UMETA(DisplayName = "ITEM_ADD_BY_SPELLBOX_KEY"),	///特殊获得宝箱钥匙
	ITEM_ADD_BY_SPACE_ACTION	= 15 UMETA(DisplayName = "ITEM_ADD_BY_SPACE_ACTION"),	///副本行为
	ITEM_ADD_BY_SPACE_SENTLEMENT = 16 UMETA(DisplayName = "ITEM_ADD_BY_SPACE_SENTLEMENT"),	///副本结算
	ITEM_ADD_BY_TONG_STORE		= 17 UMETA(DisplayName = "ITEM_ADD_BY_TONG_STORE"),	///帮会仓库
	ITEM_ADD_BY_TONG_SALARY		= 18 UMETA(DisplayName = "ITEM_ADD_BY_TONG_SALARY"),	///帮会俸禄
	ITEM_ADD_BY_STORE			= 19 UMETA(DisplayName = "ITEM_ADD_BY_STORE"),	///个人仓库取物品
	ITEM_ADD_BY_MAIL			= 20 UMETA(DisplayName = "ITEM_ADD_BY_MAIL"),	///邮件
	ITEM_ADD_BY_NEW_PLAYER_GIFT	= 21 UMETA(DisplayName = "ITEM_ADD_BY_NEW_PLAYER_GIFT"),	///新手奖励
	ITEM_ADD_BY_SIGN_IN_GIFT	= 22 UMETA(DisplayName = "ITEM_ADD_BY_SIGN_IN_GIFT"),	///签到奖励
	ITEM_ADD_BY_SPLIT			= 23 UMETA(DisplayName = "ITEM_ADD_BY_SPLIT"),	///分割物品
	ITEM_ADD_BY_COMPOSE			= 24 UMETA(DisplayName = "ITEM_ADD_BY_COMPOSE"),	///打造装备
	ITEM_ADD_BY_TAKEPRESENT		= 25 UMETA(DisplayName = "ITEM_ADD_BY_TAKEPRESENT"),	///运营活动奖励，当前包括来自于“custom_ChargePresentUnite”和“custom_ItemAwards”表的奖励。
	ITEM_ADD_BY_EVOULATION_PET	= 26 UMETA(DisplayName = "ITEM_ADD_BY_EVOULATION_PET"),	///原兽进化得幻兽蛋
	ITEM_ADD_BY_STORE_TOOL		= 27 UMETA(DisplayName = "ITEM_ADD_BY_STORE_TOOL"),	///从轮回秘境储物柜取物品
	ITEM_ADD_BY_ADD_JADE		= 28 UMETA(DisplayName = "ITEM_ADD_BY_ADD_JADE"),	///玲珑玉令获得
	ITEM_ADD_BY_MONSTER_AI		= 29 UMETA(DisplayName = "ITEM_ADD_BY_MONSTER_AI"),	///ai添加物品
};

UENUM(BlueprintType)
enum class QUALITY : uint8
{
	QUALITY_WHITE						= 1 UMETA(DisplayName = "QUALITY_WHITE"),			///白色
	QUALITY_BLUE						= 2 UMETA(DisplayName = "QUALITY_BLUE"),			///蓝色
	QUALITY_GOLD						= 3 UMETA(DisplayName = "QUALITY_GOLD"),			///金色
	QUALITY_PINK						= 4 UMETA(DisplayName = "QUALITY_PINK"),			///粉色
	QUALITY_GREEN						= 5 UMETA(DisplayName = "QUALITY_GREEN"),			///地阶绿色
	QUALITY_GREEN_TIAN					= 6 UMETA(DisplayName = "QUALITY_GREEN_TIAN"),		///天阶绿色
	QUALITY_GREEN_SHENG					= 7 UMETA(DisplayName = "QUALITY_GREEN_SHENG"),		///圣阶绿色
	QUALITY_GREEN_SHEN					= 8 UMETA(DisplayName = "QUALITY_GREEN_SHEN"),		/// 王道神兵（装备专属）
};

UENUM(BlueprintType)
enum class MOVETYPE : uint8
{
	MOVETYPE_STOP						= 0 UMETA(DisplayName = "MOVETYPE_STOP"),						///处于没有移动中
	MOVETYPE_NAVIGATE_POINT				= 1 UMETA(DisplayName = "MOVE_TYPE_NAVIGATE_POINT"),			///处于向指定点移动
	MOVETYPE_MOVE_POINT					= 2	UMETA(DisplayName = "MOVE_TYPE_MOVE_POINT"),				///处于向指定点移动
	MOVETYPE_CHASE						= 3	UMETA(DisplayName = "MOVE_TYPE_CHASE"),						///处于追击目标移动
	MOVETYPE_PATROL						= 4	UMETA(DisplayName = "MOVE_TYPE_PATROL"),					///处于巡逻移动
	MOVETYPE_RANDOM						= 5	UMETA(DisplayName = "MOVE_TYPE_RANDOM"),					///处于随机移动
	MOVETYPE_WANDER						= 6	UMETA(DisplayName = "MOVE_TYPE_WANDER"),					///处于游荡移动
	MOVETYPE_WALK_AROUND				= 7 UMETA(DisplayName = "MOVE_TYPE_WALK_AROUND"),				///处于游走移动
	MOVETYPE_CHARGE						= 8 UMETA(DisplayName = "MOVE_TYPE_CHARGE"),					///处于冲锋移动
	MOVETYPE_GOBACK						= 9	UMETA(DisplayName = "MOVE_TYPE_GOBACK"),					///处于回走移动
	MOVETYPE_LOOP_ROTATOR				= 10 UMETA(DisplayName = "MOVE_TYPE_LOOP_ROTATOR"),				///转圈
	MOVETYPE_SKILL_CHASE				= 11 UMETA(DisplayName = "MOVE_TYPE_SKILL_CHASE"),				///处于使用技能跟随移动
	MOVETYPE_HIT_BACK					= 12 UMETA(DisplayName = "MOVE_TYPE_HIT_BACK"),					///被击飞、击退
	MOVETYPE_RANDOM_CHOICE_FORM_LIST	= 13 UMETA(DisplayName = "MOVE_TYPE_RANDOM_CHOICE_FORM_LIST"),	///从列表里随机取点移动
	MOVETYPE_FIGHT_DISPERSE				= 14 UMETA(DisplayName = "MOVE_TYPE_FIGHT_DISPERSE"),			///小怪物追击及散开表现
	MOVETYPE_JUMP						= 15 UMETA(DisplayName = "MOVE_TYPE_JUMP"),						///跳跃移动
	MOVETYPE_CHASE_CLIENT				= 16 UMETA(DisplayName = "MOVE_TYPE_CHASE_CLIENT"),				///同步客户端位置的追击移动
	MOVE_TYPE_SKILL_JUMP				= 24 UMETA(DisplayName = "MOVE_TYPE_SKILL_JUMP"),				///跳扑技能移动
};

UENUM(BlueprintType)
enum class EFFECT_STATE : uint8
{
	///0-眩晕效果
	EFFECT_STATE_DIZZY					= 0	UMETA(DisplayName = "EffectStateDizzy"),
	///1-霸体效果
	EFFECT_STATE_UNCONTROLLABLE			= 1	UMETA(DisplayName = "EffectStateUnControllable"),
	///2-无敌效果
	EFFECT_STATE_INVINCIBLE				= 2	UMETA(DisplayName = "EffectStateInvincible"),
	///3-受击中效果
	EFFECT_STATE_HIT_BACK				= 3	UMETA(DisplayName = "EffectStateHitBack"),
	///4-定身效果
	EFFECT_STATE_FIX					= 4 UMETA(DisplayName = "EffectStateFix"),
	///5-睡眠效果
	EFFECT_STATE_SLEEP					= 5 UMETA(DisplayName = "EffectStateSleep"),
	///6-缠绕效果
	EFFECT_STATE_WIND					= 6 UMETA(DisplayName = "EffectStateWind"),
	///7-保护效果
	EFFECT_STATE_PROTECT				= 7 UMETA(DisplayName = "EffectStateProtect"),
	///8-跟随效果（包括组队跟随和队友跟随）
	EFFECT_STATE_FOLLOW					= 8 UMETA(DisplayName = "EffectStateFollow"),
	///9-混乱效果
	EFFECT_STATE_CONFUSION				= 9 UMETA(DisplayName = "EffectStateConfusion"),
	///10-不屈效果
	EFFECT_STATE_UNYIELDING				= 10 UMETA(DisplayName = "EffectStateUnyielding"),
	///11-冻结效果
	EFFECT_STATE_FREEZE					= 11 UMETA(DisplayName = "EffectStateFreeze"),
	///12-表演效果
	EFFECT_STATE_SHOW					= 12 UMETA(DisplayName = "EffectStateShow"),
	///13-隐身效果
	EFFECT_STATE_HIDE					= 13 UMETA(DisplayName = "EffectStateHide"),
	///14-镜头剧情效果
	EFFECT_STATE_STORY					= 14 UMETA(DisplayName = "EffectStateStory"),
	///状态上限（无效，请勿选择）
	EFFECT_STATE_NULL					= 15 UMETA(DisplayName = "EffectStateNull"),
};

UENUM(BlueprintType)
enum class JUMP_SHOW_STATE : uint8
{
	JUMP_SHOW_STATE_STAND				= 0	UMETA(DisplayName = "JUMP_SHOW_STATE_STAND"),				///0-非跳跃状态
	JUMP_SHOW_STATE_SJUMP				= 1	UMETA(DisplayName = "JUMP_SHOW_STATE_SJUMP"),				///1-原地起跳跃状态
	JUMP_SHOW_STATE_MJUMP				= 2	UMETA(DisplayName = "JUMP_SHOW_STATE_MJUMP"),				///2-跑着起跳跃状态
	JUMP_SHOW_STATE_TWO_SJUMP			= 3	UMETA(DisplayName = "JUMP_SHOW_STATE_TWO_SJUMP"),			///3-二段原地起跳跃状态
	JUMP_SHOW_STATE_TWO_MJUMP			= 4	UMETA(DisplayName = "JUMP_SHOW_STATE_TWO_MJUMP"),			///4-二段跑着起跳跃状态
	JUMP_SHOW_STATE_THREE_SJUMP			= 5	UMETA(DisplayName = "JUMP_SHOW_STATE_THREE_SJUMP"),			///5-三段原地起跳跃状态
	JUMP_SHOW_STATE_THREE_MJUMP			= 6	UMETA(DisplayName = "JUMP_SHOW_STATE_THREE_MJUMP"),			///6-三段跑着起跳跃状态
	JUMP_SHOW_STATE_AIR_UP				= 7	UMETA(DisplayName = "JUMP_SHOW_STATE_AIR_UP"),				///7-上升状态
	JUMP_SHOW_STATE_AIR_DOWN			= 8	UMETA(DisplayName = "JUMP_SHOW_STATE_AIR_DOWN"),			///8-下降状态
	JUMP_SHOW_STATE_SLAND				= 9	UMETA(DisplayName = "JUMP_SHOW_STATE_SLAND"),				///9-原地着陆状态
	JUMP_SHOW_STATE_MLAND				= 10	UMETA(DisplayName = "JUMP_SHOW_STATE_MLAND"),			///10-跑着着陆状态
	JUMP_SHOW_STATE_FLOAT				= 11	UMETA(DisplayName = "JUMP_SHOW_STATE_FLOAT"),			///11-浮空状态
	JUMP_SHOW_STATE_PASSIVE				= 12	UMETA(DisplayName = "JUMP_SHOW_STATE_PASSIVE"),			///12-被动跳跃状态
};

UENUM(BlueprintType)
enum class CLIMB_LADDER_STATE : uint8
{
	CLIMB_LADDER_STATE_STAND			 = 0	UMETA(DisplayName = "CLIMB_LADDER_STATE_ENTER_ZONE"),	  ///0-非攀爬梯子状态
	CLIMB_LADDER_STATE_ENTER_ZONE		 = 1	UMETA(DisplayName = "CLIMB_LADDER_STATE_ENTER_ZONE"),	  ///0-进入梯子区域
	CLIMB_LADDER_STATE_ENTER_BOTTOM		 = 2	UMETA(DisplayName = "CLIMB_LADDER_STATE_ENTER_BOTTOM"),	  ///1-底部进入梯子
	CLIMB_LADDER_STATE_EXIT_BOTTOM		 = 3	UMETA(DisplayName = "CLIMB_LADDER_STATE_EXIT_BOTTOM"),	  ///2-底部离开梯子
	CLIMB_LADDER_STATE_EXIT_TOP			 = 4	UMETA(DisplayName = "CLIMB_LADDER_STATE_EXIT_TOP"),		  ///3-顶部离开梯子
	CLIMB_LADDER_STATE_MOVE				 = 5	UMETA(DisplayName = "CLIMB_LADDER_STATE_MOVE"),			  ///4-中间攀爬移动
	CLIMB_LADDER_STATE_FALL_EXIT		 = 6	UMETA(DisplayName = "CLIMB_LADDER_STATE_FALL_EXIT"),	  ///5-从梯子上掉落离开
	CLIMB_LADDER_STATE_FALL_EXIT_LAND	 = 7	UMETA(DisplayName = "CLIMB_LADDER_STATE_FALL_EXIT_LAND"), ///6-从梯子上掉落着陆
};

UENUM(BlueprintType)
enum class COLLISION_TYPE : uint8
{
	COLLISION_DEFAULT					= 0 UMETA(DisplayName = "COLLISION_DEFAULT"),					///0-默认碰撞
	COLLISION_ENEMY						= 1 UMETA(DisplayName = "COLLISION_ENEMY"),						///1-碰撞敌对
};

UENUM(BlueprintType)
enum class COMBAT_RELATION : uint8
{
	COMBAT_RELATION_DEFAULT				= 0 UMETA(DisplayName = "COMBAT_RELATION_DEFAULT"),				///0-未设置
	COMBAT_RELATION_NORMAL				= 1 UMETA(DisplayName = "COMBAT_RELATION_NORMAL"),				///1-友好关系
	COMBAT_RELATION_ENEMY				= 2 UMETA(DisplayName = "COMBAT_RELATION_ENEMY"),				///2-敌对关系
	COMBAT_RELATION_NEUTRALLY			= 3 UMETA(DisplayName = "COMBAT_RELATION_NEUTRALLY"),			///3-中立
	COMBAT_RELATION_NONE				= 4 UMETA(DisplayName = "COMBAT_RELATION_NONE"),				///4-无任何关系
};

UENUM(BlueprintType)
enum class ENTITY_TYPE : uint8
{
	ENTITY_FLAG_UNKNOWN					= 0 UMETA(DisplayName = "ENTITY_FLAG_UNKNOWN"),					///0-未知（未设置）
	ENTITY_FLAG_ROLE					= 1 UMETA(DisplayName = "ENTITY_FLAG_ROLE"),					///1-角色
	ENTITY_FLAG_SPACE					= 2 UMETA(DisplayName = "ENTITY_FLAG_SPACE"),					///2-空间
	ENTITY_FLAG_MONSTER					= 3 UMETA(DisplayName = "ENTITY_FLAG_MONSTER"),					///3-怪物
	ENTITY_FLAG_NPC						= 4 UMETA(DisplayName = "ENTITY_FLAG_NPC"),						///4-NPC
	ENTITY_FLAG_DOOR					= 5 UMETA(DisplayName = "ENTITY_FLAG_DOOR"),					///5-传送门
	ENTITY_FLAG_SPELL					= 6 UMETA(DisplayName = "ENTITY_FLAG_SPELL"),					///6-施法箱子
	ENTITY_FLAG_TRAP					= 7 UMETA(DisplayName = "ENTITY_FLAG_TRAP"),					///7-陷阱
	ENTITY_FLAG_PLATFORM				= 8 UMETA(DisplayName = "ENTITY_FLAG_PLATFORM"),				///8-移动平台
	ENTITY_FLAG_VEHICLEPET				= 9 UMETA(DisplayName = "ENTITY_FLAG_VEHICLEPET"),				///9-幻兽
	ENTITY_FLAG_DROP_BOX				= 10 UMETA(DisplayName = "ENTITY_FLAG_DROP_BOX"),				///10-掉落箱子
	ENTITY_FLAG_GHOST_RECEIVER			= 11 UMETA(DisplayName = "ENTITY_FLAG_GHOST_RECEIVER"),			///11-技能ghost受术者（Ghost）
	ENTITY_FLAG_TELEPORTSTONE			= 12 UMETA(DisplayName = "ENTITY_FLAG_TELEPORTSTONE"),			///12-传送石
};

UENUM(BlueprintType)
enum class ENTITY_TYPE_EXT :uint8
{
	ENTITY_FLAG_EXT_UNKNOWN						= 0 UMETA(DisplayName = "ENTITY_FLAG_EXT_UNKNOWN"),					///未设置
	ENTITY_FLAG_EXT_ROLE						= 1 UMETA(DisplayName = "ENTITY_FLAG_EXT_ROLE"),					///角色（Role）
	ENTITY_FLAG_EXT_SPACE		 				= 2 UMETA(DisplayName = "ENTITY_FLAG_EXT_SPACE"),					///空间
	ENTITY_FLAG_EXT_MONSTER						= 3 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER"),					///怪物（Monster）
	ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN			= 4 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN"),		///替身怪物（MonsterExtTISHEN）
	ENTITY_FLAG_EXT_NPC							= 5 UMETA(DisplayName = "ENTITY_FLAG_EXT_NPC"),						///NPC
	ENTITY_FLAG_EXT_DOOR						= 6 UMETA(DisplayName = "ENTITY_FLAG_EXT_DOOR"),					///传送门
	ENTITY_FLAG_EXT_SPELL						= 7 UMETA(DisplayName = "ENTITY_FLAG_EXT_SPELL"),					///施法箱子（SpellBox）
	ENTITY_FLAG_EXT_TRAP						= 8 UMETA(DisplayName = "ENTITY_FLAG_EXT_TRAP"),					///陷阱（Trap）
	ENTITY_FLAG_EXT_CLIENT_TRIGGER_TRAP			= 9 UMETA(DisplayName = "ENTITY_FLAG_EXT_CLIENT_TRIGGER_TRAP"),		///客户端陷阱
	ENTITY_FLAG_EXT_PLATFORM					= 10 UMETA(DisplayName = "ENTITY_FLAG_EXT_PLATFORM"),				///移动平台
	ENTITY_FLAG_EXT_VEHICLEPET					= 11 UMETA(DisplayName = "ENTITY_FLAG_EXT_VEHICLEPET"),				///幻兽（Pet）
	ENTITY_FLAG_EXT_DROP_BOX					= 12 UMETA(DisplayName = "ENTITY_FLAG_EXT_DROP_BOX"),				///掉落箱子
	ENTITY_FLAG_EXT_GHOST_RECEIVER				= 13 UMETA(DisplayName = "ENTITY_FLAG_EXT_GHOST_RECEIVER"),			///技能ghost受术者（Ghost）
	ENTITY_FLAG_EXT_TELEPORTSTONE				= 14 UMETA(DisplayName = "ENTITY_FLAG_EXT_TELEPORTSTONE"),			///传送石
	ENTITY_FLAG_EXT_MOVE_TRAP					= 15 UMETA(DisplayName = "ENTITY_FLAG_EXT_MOVE_TRAP"),				///MoveTrap
	ENTITY_FLAG_EXT_MONSTER_EXT_YXLMSoldier		= 16 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_YXLMSoldier"),///英雄联盟的小兵
	ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE			= 17 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE"),	///客户端往服务器同步位置的Monster
	ENTITY_FLAG_EXT_MONSTER_EXT_JUMP			= 18 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_JUMP"),		///跳跃怪物
	ENTITY_FLAG_EXT_MONSTER_EXT_INTERACTIVE		= 20 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_CLICK"),		///可交互怪
	ENTITY_FLAG_EXT_MONSTER_EXT_SFMJ			= 21 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_SFMJ"),		///神风秘境，F键交互怪物
	ENTITY_FLAG_EXT_MONSTER_EXT_YCJMD			= 22 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_YCJMD"),		///勇闯绝命岛，Boss
	ENTITY_FLAG_MONSTER_FOLLOW_ROLE				= 23 UMETA(DisplayName = "ENTITY_FLAG_MONSTER_FOLLOW_ROLE"),		///客户端AI测试怪（跟随玩家）
	ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT			= 24 UMETA(DisplayName = "ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT"),		///客户端控制怪物
	ENTITY_FLAG_EXT_MONSTER_EXT_QQRYJ			= 25 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_QQRYJ"),		///巧取熔岩晶怪物
	ENTITY_FLAG_EXT_MONSTER_EXT_ATTACK_LADDER   = 26 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_ATTACK_LADDER"),///攻城梯
	ENTITY_FLAG_EXT_MONSTER_EXT_AERIAL_LADDER   = 27 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_AERIAL_LADDER"),///云梯
	ENTITY_FLAG_EXT_MONSTER_EXT_ORIGIN_PET		= 28 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_ORIGIN_PET"),///原兽
	ENTITY_FLAG_EXT_MONSTER_OPTIMIZE			= 29 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_OPTIMIZE"),		///优化行为怪物
	ENTITY_FLAG_EXT_MONSTER_EXT_COLLISION_CAR	= 30 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_COLLISION_CAR"),///撞车
	ENTITY_FLAG_EXT_TRAP_BATTLEFLAG				= 31 UMETA(DisplayName = "ENTITY_FLAG_EXT_TRAP_BATTLEFLAG"),///战旗
	ENTITY_FLAG_EXT_MONSTER_COMMANDER			= 32 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_COMMANDER"),///指挥官类型小怪
	ENTITY_FLAG_EXT_MONSTER_SOLDIER				= 33 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_SOLDIER"),///士兵小怪
	ENTITY_FLAG_EXT_TRAP_BARRACKS				= 34 UMETA(DisplayName = "ENTITY_FLAG_EXT_TRAP_BARRACKS"),///兵营
	ENTITY_FLAG_EXT_NPC_TRAINSOLDIERGROUND		= 35 UMETA(DisplayName = "ENTITY_FLAG_EXT_NPC_TRAINSOLDIERGROUND"),///练兵场
	ENTITY_FLAG_EXT_MONSTER_EXT_MENU			= 36 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_MENU"),///带标签菜单怪物
	ENTITY_FLAG_EXT_MONSTER_EXT_JDCY			= 37 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_JDCY"),///禁地采药怪物
	ENTITY_FLAG_EXT_MONSTER_EXT_BATTERY			= 38 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_BATTERY"),///火炮
	ENTITY_FLAG_EXT_MONSTER_EXT_CALL			= 39 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_CALL"),///callMonster
	ENTITY_FLAG_EXT_MONSTER_EXT_COVER			= 40 UMETA(DisplayName = "ENTITY_FLAG_EXT_MONSTER_EXT_COVER"),///轮回秘境保护罩
	ENTITY_FLAG_EXT_FENSHEN						= 41 UMETA(DisplayName = "ENTITY_FLAG_EXT_FENSHEN"),///分身怪物
	ENTITY_FLAG_EXT_TONG_DROPBOX				= 42 UMETA(DisplayName = "ENTITY_FLAG_EXT_TONG_DROPBOX"),///帮会宝箱
	ENTITY_FLAG_EXT_TEAM_DROPBOX				= 43 UMETA(DisplayName = "ENTITY_FLAG_EXT_TEAM_DROPBOX"),///队伍宝箱
};

///客户端actor显示规则
UENUM(BlueprintType)
enum class VISIBLE_RULE : uint8
{
	///1-标志位显示规则
	VISIBLE_RULE_BY_FLAG				= 1 UMETA(DisplayName = "VISIBLE_RULE_BY_FLAG"),
	///2-玩家标志位显示规则
	VISIBLE_RULE_BY_ROLE_FLAG			= 2 UMETA(DisplayName = "VISIBLE_RULE_BY_ROLE_FLAG"),
	///3-剧情模式显示规则
	VISIBLE_RULE_BY_STORY				= 3 UMETA(DisplayName = "VISIBLE_RULE_BY_STORY"),
	///4-死亡效果显示规则
	VISIBLE_RULE_BY_DEAD_EFFECT			= 4	UMETA(DisplayName = "VISIBLE_RULE_BY_DEAD_EFFECT"),
	///5-SpellBox死亡不销毁，用隐藏模型代替
	VISIBLE_RULE_BY_BOX_DIE				= 5	UMETA(DisplayName = "VISIBLE_RULE_BY_BOX_DIE"),
	///6-DropBox显示规则
	VISIBLE_RULE_BY_DROP_BOX			= 6	UMETA(DisplayName = "VISIBLE_RULE_BY_DROP_BOX"),
	///7-任务显示规则
	VISIBLE_RULE_BY_QUEST				= 7	UMETA(DisplayName = "VISIBLE_RULE_BY_QUEST"),
	///8-BUFF显示规则
	VISIBLE_RULE_BY_BUFF				= 8 UMETA(DisplayName = "VISIBLE_RULE_BY_BUFF"),
	///9-玩家未决状态不可交互，隐藏模型
	VISIBLE_RULE_BY_ROLE_PENDING		= 9 UMETA(DisplayName = "VISIBLE_RULE_BY_ROLE_PENDING"),
	///10-怪物未决状态不可交互，隐藏模型
	VISIBLE_RULE_BY_MONSTER_PENDING		= 10 UMETA(DisplayName = "VISIBLE_RULE_BY_MONSTER_PENDING"),
	///11-幻兽未决状态不可交互，隐藏模型
	VISIBLE_RULE_BY_VEHICLE_PET_PENDING	= 11 UMETA(DisplayName = "VISIBLE_RULE_BY_VEHICLE_PET_PENDING"),
	///12-隐身效果显示规则（@CST-9111）
	VISIBLE_RULE_BY_BUFF_HIDE			= 12 UMETA(DisplayName = "VISIBLE_RULE_BY_BUFF_HIDE"),
	///13-飞行模式显示规则
	VISIBLE_RULE_BY_FLY					= 13 UMETA(DisplayName = "VISIBLE_RULE_BY_FLY"),
	///15-BuffTransparency半透明Buff显示规则
	VISIBLE_RULE_BY_BUFF_TRANSPARENCY	 UMETA(DisplayName = "VISIBLE_RULE_BY_BUFF_TRANSPARENCY"),
	///16-跳伞显示规则
	VISIBLE_RULE_BY_SKYDIVING			UMETA(DisplayName = "VISIBLE_RULE_BY_SKYDIVING"),
	///17-陷阱符玉规则
	VISIBLE_RULE_BY_TRAP_SYMBOL			UMETA(DisplayName = "VISIBLE_RULE_BY_TRAP_SYMBOL"),
};

UENUM(BlueprintType)
enum class VISIBLE_TYPE : uint8	///显示类型优先级从低到高
{
	VISIBLE_TYPE_TRUE					= 0 UMETA(DisplayName = "VISIBLE_TYPE_TRUE"),					///0-默认可见
	VISIBLE_TYPE_TRANSLUCENT			 UMETA(DisplayName = "VISIBLE_TYPE_TRANSLUCENT"),			///1-标志位半透明
	VISIBLE_TYPE_FlAG_FALSE				 UMETA(DisplayName = "VISIBLE_TYPE_FlAG_FALSE"),				///2-标志位不可见
	VISIBLE_TYPE_QUEST_TRUE				 UMETA(DisplayName = "VISIBLE_TYPE_QUEST_TRUE"),				///3-任务可见
	VISIBLE_TYPE_DEAD_FALSE				 UMETA(DisplayName = "VISIBLE_TYPE_DEAD_FALSE"),				///5-死亡不可见
	VISIBLE_TYPE_EFFECT_HIDE_TRANSLUCENT	 UMETA(DisplayName = "VISIBLE_TYPE_EFFECT_HIDE_TRANSLUCENT"),///6-隐身友好半透明
	VISIBLE_TYPE_EFFECT_HIDE_FALSE		 UMETA(DisplayName = "VISIBLE_TYPE_EFFECT_HIDE_FALSE"),		///7-隐身敌对不可见
	VISIBLE_TYPE_QUEST_FALSE			 UMETA(DisplayName = "VISIBLE_TYPE_QUEST_FALSE"),			///8-任务不可见
	VISIBLE_TYPE_BUFF_FALSE				 UMETA(DisplayName = "VISIBLE_TYPE_BUFF_FALSE"),				///9-Buff不可见
	VISIBLE_TYPE_BUFF_TRUE				 UMETA(DisplayName = "VISIBLE_TYPE_BUFF_TRUE"),				///10-Buff可见
	VISIBLE_TYPE_STORY_FALSE			 UMETA(DisplayName = "VISIBLE_TYPE_STORY_FALSE"),			///11-镜头不可见
	VISIBLE_TYPE_BOX_DIE_FALSE			 UMETA(DisplayName = "VISIBLE_TYPE_BOX_DIE_FALSE"),			///12-SpellBox死亡不可见
	VISIBLE_TYPE_DROP_BOX_FALSE			 UMETA(DisplayName = "VISIBLE_TYPE_DROP_BOX_FALSE"),		///13-DropBox
	VISIBLE_TYPE_PENGIND_FALSE			 UMETA(DisplayName = "VISIBLE_TYPE_PENGIND_FALSE"),			///14-未决状态不可见
	VISIBLE_TYPE_BUFF_TRANSLUCENT		 UMETA(DisplayName = "VISIBLE_TYPE_BUFF_TRANSLUCENT"),		///15-Buff半透明
	VISIBLE_TYPE_SKYDIVING_FALSE		 UMETA(DisplayName = "VISIBLE_TYPE_SKYDIVING_FALSE"),		///16-跳伞状态不可见
	VISIBLE_TYPE_TRAP_SYMBOL_TRUE		 UMETA(DisplayName = "VISIBLE_TYPE_TRAP_SYMBOL_TRUE"),		///17-陷阱符玉，召唤的玩家可见
	VISIBLE_TYPE_TRAP_SYMBOL_FALSE		 UMETA(DisplayName = "VISIBLE_TYPE_TRAP_SYMBOL_FALSE"),		///18-陷阱符玉，其他玩家不可见
};

UENUM(BlueprintType)
enum class VISIBLE_STYLE : uint8
{
	VISIBLE_STYLE_TRUE					= 0 UMETA(DisplayName = "VISIBLE_STYLE_TRUE"),					///0-模型可见
	VISIBLE_STYLE_TRANSLUCENT			= 1 UMETA(DisplayName = "VISIBLE_STYLE_TRANSLUCENT"),			///1-隐身可见(半透明)
	VISIBLE_STYLE_TRANSLUCENT_FALSE		= 2 UMETA(DisplayName = "VISIBLE_STYLE_TRANSLUCENT_FALSE"),		///2-隐身不可见
	VISIBLE_STYLE_FALSE					= 3	UMETA(DisplayName = "VISIBLE_STYLE_FALSE"),					///3-模型不可见
	VISIBLE_STYLE_TRANSLUCENT_VALUE		= 4 UMETA(DisplayName = "VISIBLE_STYLE_TRANSLUCENT_VALUE"),		///4-半透明可见（半透明）
};

UENUM(BlueprintType)
enum class SPELL_BOX_LISTEN_EVENT : uint8
{
	EVENT_QUEST_CHANGE					= 1 UMETA(DisplayName = "EVENT_QUEST_CHANGE"),					///任务状态改变
	EVENT_ADD_ITEM						= 2 UMETA(DisplayName = "EVENT_ADD_ITEM"),						///获得物品
	EVENT_KILL_BOSS						= 3 UMETA(DisplayName = "EVENT_KILL_BOSS"),						///击杀Boss
	EVENT_SPACE_STAGE_COMPLETE			= 4 UMETA(DisplayName = "EVENT_SPACE_STAGE_COMPLETE"),			///副本某阶段已完成
	EVENT_IS_CAPTAIN					= 5 UMETA(DisplayName = "EVENT_IS_CAPTAIN"),					///成为队长或卸任队长
	EVENT_HAS_BUFF						= 6 UMETA(DisplayName = "EVENT_HAS_BUFF"),						///有或无某些Buff
	EVENT_IS_INTERACT					= 7 UMETA(DisplayName = "EVENT_IS_INTERACT"),					///是否可多人同时交互
	EVENT_HAS_ENTITY					= 8	UMETA(DisplayName = "EVENT_HAS_ENTITY"),					///是否某个Entity存在或存活
	EVENT_HAS_CAMP_GOSSIP				= 9 UMETA(DisplayName = "EVENT_HAS_CAMP_GOSSIP"),				///是否已与该阵营的玩家交互
	EVENT_IS_THIS_CAMP					= 10 UMETA(DisplayName = "EVENT_IS_THIS_CAMP"),					///是否为该阵营的玩家
	SPELL_BOX_LISTEN_EVENT_NOT_IN_AREA	= 11 UMETA(DisplayName = "SPELL_BOX_LISTEN_EVENT_NOT_IN_AREA"),			///
	SPELL_BOX_LISTEN_EVENT_BXZZ			= 12 UMETA(DisplayName = "SPELL_BOX_LISTEN_EVENT_BXZZ"),				///哨塔是否可交互（@CST-4056，冰雪之战）
	SPELL_BOX_LISTEN_EVENT_HAS_NOTIFY	= 13 UMETA(DisplayName = "SPELL_BOX_LISTEN_EVENT_HAS_NOTIFY"),			///是否接受过某副本通知
	SPELL_BOX_LISTEN_EVENT_CREATOR		= 14 UMETA(DisplayName = "SPELL_BOX_LISTEN_EVENT_CREATOR"),				///针对专属spellBox，创建者才可以交互（@CST-5772）
	SPELL_BOX_LISTEN_EVENT_HAS_TONG_GOSSIP=15 UMETA(DisplayName = "SPELL_BOX_LISTEN_EVENT_HAS_TONG_GOSSIP"),	///是否没有与某个帮会玩家交互
	SPELL_BOX_LISTEN_EVENT_ROLE_IS_INTERACT=16 UMETA(DisplayName = "SPELL_BOX_LISTEN_EVENT_ROLE_IS_INTERACT"),	///玩家是否有正在交互的SpellBoxPickItem
};

UENUM(BlueprintType)
enum class HIT_STATE : uint8
{
	HIT_STATE_NONE						= 0 UMETA(DisplayName = "HIT_STATE_NONE"),						///无受击
	HIT_STATE_BACK						= 1 UMETA(DisplayName = "HIT_STATE_BACK"),						///受击击退
};

UENUM(BlueprintType)
enum class CHANGE_CHARACTER_MOVEMENT_TYPE : uint8
{
	CHANGE_CHARACTER_MOVEMENT_TYPE_SPACE_COPY	= 1 UMETA(DisplayName = "CHANGE_CHARACTER_MOVEMENT_TYPE_SPACE_COPY"),	///1-副本改变移动方式
	CHANGE_CHARACTER_MOVEMENT_TYPE_JUMP			= 2 UMETA(DisplayName = "CHANGE_CHARACTER_MOVEMENT_TYPE_JUMP"),			///2-跳跃改变移动方式
};

///取消组队跟随原因
UENUM(BlueprintType)
enum class TEAM_FOLLOW_FAILURE_REASON : uint8
{
	REASON_ENTITY_INVALID				= 1 UMETA(DisplayName = "REASON_CANT_FIND_TARGET_ENTITY"),		///不合法（找不到目标或者卡住）
	REASON_TO_FAR_TO_LEADER				= 2 UMETA(DisplayName = "REASON_ACTOR_TO_FAR"),					///距离领导者太远
	REASON_ACTIVE_CANCEL				= 3 UMETA(DisplayName = "REASON_ACTIVE_CANCEL"),				///主动取消
	REASON_STATE_LIMIT					= 4 UMETA(DisplayName = "REASON_STATE_LIMIT"),					///状态限制（如死亡、被定身等）
};

UENUM(BlueprintType)
enum class AREA_LIGHT_WALL_TYPE_ENUM : uint8
{
	///位面光墙
	AreaLightWall			= 0 UMETA(DisplayName = "AreaLightWall"),
	///Boss光墙
	BossLightWall			= 1 UMETA(DisplayName = "BossLightWall"),
	///区域阻挡光墙
	TerrainLightWall		= 2 UMETA(DisplayName = "TerrainLightWall"),
	///普通区域墙(不阻挡)
	NormalAreaWall			= 3 UMETA(DisplayName = "NormalAreaWall"),
};

UENUM(BlueprintType)
enum class WATER_TYPE_ENUM : uint8
{
	///可站立水面
	WATER_CAN_STEPON		= 0 UMETA(DisplayName = "WATER_CAN_STEPON"),
	///不可站立水面
	WATER_NOT_STEPON		= 1 UMETA(DisplayName = "WATER_NOT_STEPON"),
};

UENUM(BlueprintType)
enum class ENUM_SPACE_TYPE : uint8
{
	SPACE_TYPE_NORMAL					= 0 UMETA(DisplayName = "SPACE_TYPE_NORMAL"),					///缺省值
	SPACE_TYPE_MULTILINE				= 1 UMETA(DisplayName = "SPACE_TYPE_MULTILINE"),				///多线地图
	SPACE_TYPE_PLANE					= 2 UMETA(DisplayName = "SPACE_TYPE_PLANE"),					///位面
	SPACE_TYPE_COPY						= 3 UMETA(DisplayName = "SPACE_TYPE_COPY"),						///副本
	SPACE_TYPE_POTENTIAL				= 4 UMETA(DisplayName = "SPACE_TYPE_POTENTIAL"),				///潜能副本
	SPACE_TYPE_CHUAN_CHENG				= 5 UMETA(DisplayName = "SPACE_TYPE_CHUAN_CHENG"),				///传承副本
	SPACE_TYPE_STORY_COPY				= 6 UMETA(DisplayName = "SPACE_TYPE_STORY_COPY"),				///剧情副本
	SPACE_TYPE_JAIL						= 7 UMETA(DisplayName = "SPACE_TYPE_JAIL"),						///监狱
	SPACE_TYPE_TONG						= 8 UMETA(DisplayName = "SPACE_TYPE_TONG"),						///帮会地图
	SPACE_TYPE_HOME_BARRACKS			= 9 UMETA(DisplayName = "SPACE_TYPE_HOME_BARRACKS"),			///帮会争霸大本营
	SPACE_TYPE_TONG_TIAN_TA				= 10 UMETA(DisplayName = "SPACE_TYPE_TONG_TIAN_TA"),			///通天塔副本
	SPACE_TYPE_DONG_FU					= 11 UMETA(DisplayName = "SPACE_TYPE_DONG_FU"),					///洞府
	SPACE_TYPE_JSSLC_CHANCE_COPY		= 12 UMETA(DisplayName = "SPACE_TYPE_JSSLC_CHANCE_COPY"),		///晶石狩猎场机缘副本
};

UENUM(BlueprintType)
enum class SPACE_AREA_TYPE : uint8
{
	SPACE_AREA_TYPE_NONE				= 0 UMETA(DisplayName = "SPACE_AREA_TYPE_NONE"),				///缺省值
	SPACE_AREA_TYPE_SUB					= 1 UMETA(DisplayName = "SPACE_AREA_TYPE_SUB"),					///子区域
	SPACE_AREA_TYPE_WHOLE				= 2 UMETA(DisplayName = "SPACE_AREA_TYPE_WHOLE"),				///大地图区域
	SPACE_AREA_TYPE_PLANE				= 3 UMETA(DisplayName = "SPACE_AREA_TYPE_PLANE"),				///位面区域
	SPACE_AREA_TYPE_SC_STORY			= 4 UMETA(DisplayName = "SPACE_AREA_TYPE_SC_STORY"),			///剧情副本类型
	SPACE_AREA_TYPE_SC_NORMAL			= 5 UMETA(DisplayName = "SPACE_AREA_TYPE_SC_NORMAL"),			///通用副本类型
};

UENUM(BlueprintType)
enum class ROLE_RELATION_RULE : uint8
{
	RELATION_RULE_CAMP = 1 UMETA(DisplayName = "RELATION_RULE_CAMP"),			///阵营决定PVP关系
	RELATION_RULE_PKMODE = 2 UMETA(DisplayName = "RELATION_RULE_PKMODE"),		///PK模式决定PVP关系
	RELATION_RULE_PEACE = 3 UMETA(DisplayName = "RELATION_RULE_PEACE"),			///与其他玩家完全友好
	ROLE_RELATION_RULE_ENEMY = 4 UMETA(DisplayName = "ROLE_RELATION_RULE_ENEMY"),						///与其他玩家都敌对
	ROLE_RELATION_RULE_TONG_STARCRAFT = 5 UMETA(DisplayName = "ROLE_RELATION_RULE_TONG_STARCRAFT"),		///用于帮会之间战斗，不同帮会之间敌对
	ROLE_RELATION_RULE_TEAM_STARCRAFT = 6 UMETA(DisplayName = "ROLE_RELATION_RULE_TONG_STARCRAFT"),		///用于队伍之间战斗，不同队伍之间敌对
	ROLE_RELATION_RULE_BLONG_SIDE = 7 UMETA(DisplayName = "ROLE_RELATION_RULE_BLONG_SIDE"), /// 用于攻守战
	ROLE_RELATION_RULE_LHMJ = 8 UMETA(DisplayName = "ROLE_RELATION_RULE_LHMJ"), /// 轮回秘境
};

UENUM(BlueprintType)
enum class ROLE_PK_MODE : uint8
{
	///和平模式
	PK_MODE_PEACE = 1 UMETA(DisplayName = "PK_MODE_PEACE"),
	///阵营模式
	PK_MODE_CAMP = 2 UMETA(DisplayName = "PK_MODE_CAMP"),
	///善恶模式
	PK_MODE_RIGHTFUL = 3 UMETA(DisplayName = "PK_MODE_RIGHTFUL"),
	///杀戮模式
	PK_MODE_SLAUGHTER = 4 UMETA(DisplayName = "PK_MODE_SLAUGHTER"),
};

/**
* 菜单选项样式
*/
UENUM(BlueprintType)
enum class MENU_ITEM_STYLE : uint8
{
	///普通文字样式
	COMMON_TEXT = 0 UMETA(DisplayName = "COMMON"),
	///可选样式
	CHECKABLE_BOX = 1 UMETA(DisplayName = "CHECKABLE"),
	///图片按钮样式
	IMAGE_BUTTON = 2 UMETA(DisplayName = "IMAGE"),
};

/**
* character类型
*/
UENUM(BlueprintType)
enum class CHARACTER_TYPE : uint8
{
	///玩家
	PLAYER_CHARACTER = 0 UMETA(DisplayName = "PLAYER_CHARACTER"),
	///NPC
	NPC_CHARACTER = 1 UMETA(DisplayName = "NPC_CHARACTER"),
	///怪物
	MONSTER_CHARACTER = 2 UMETA(DisplayName = "MONSTER_CHARACTER"),
	///掉落宝箱
	DROPBOX_CHARACTER = 3 UMETA(DisplayName = "DROPBOX_CHARACTER"),
	///幻兽
	PET_CHARACTER = 4 UMETA(DisplayName = "PET_CHARACTER"),
	///骑乘
	RIDER_CHARACTER = 5 UMETA(DisplayName = "RIDER_CHARACTER"),
	///场景物件
	SPELL_CHARACTER = 6 UMETA(DisplayName = "SPELL_CHARACTER"),
	///玩家替身怪物
	TISHEN_MONSTER = 7 UMETA(DisplayName = "TISHEN_MONSTER"),
	///上古秘阵特殊怪物
	MIZHEN_MONSTER = 8 UMETA(DisplayName = "MIZHEN_MONSTER"),
	///可回收怪物
	RECOVERY_MONSTER = 9 UMETA(DisplayName = "RECOVERY_MONSTER"),
};

/**
* 帮会权限
*/
UENUM(BlueprintType)
enum class TONG_GRADE_TYPE : uint8
{
	///邀请入帮
	TONG_GRADE_INVITE = 0 UMETA(DisplayName = "TONG_GRADE_INVITE"),
	///申请管理
	TONG_GRADE_REQUEST = 1 UMETA(DisplayName = "TONG_GRADE_REQUEST"),
	///踢出帮会
	TONG_GRADE_KICK = 2 UMETA(DisplayName = "TONG_GRADE_KICK"),
	///任免职位
	TONG_GRADE_APPOINT = 3 UMETA(DisplayName = "TONG_GRADE_APPOINT"),
	///发布公告
	TONG_GRADE_NOTICE = 4 UMETA(DisplayName = "TONG_GRADE_NOTICE"),
	///禁言
	TONG_GRADE_SHUTUP = 5 UMETA(DisplayName = "TONG_GRADE_SHUTUP"),
	///帮会任务
	TONG_GRADE_QUEST = 6 UMETA(DisplayName = "TONG_GRADE_QUEST"),
	///技能研发
	TONG_GRADE_DEVELOP = 7 UMETA(DisplayName = "TONG_GRADE_DEVELOP"),
	///帮会神兽
	TONG_GRADE_NAGUAL = 8 UMETA(DisplayName = "TONG_GRADE_NAGUAL"),
	///帮会建筑
	TONG_GRADE_BUILDING = 9 UMETA(DisplayName = "TONG_GRADE_BUILDING"),
	///同盟管理
	TONG_GRADE_ALLY = 10 UMETA(DisplayName = "TONG_GRADE_ALLY"),
	///群发邮件
	TONG_GRADE_MAIL = 11 UMETA(DisplayName = "TONG_GRADE_MAIL"),
	///帮众召集
	TONG_GRADE_CONVENE = 12 UMETA(DisplayName = "TONG_GRADE_CONVENE"),
	///帮会掠夺
	TONG_GRADE_ROB = 13 UMETA(DisplayName = "TONG_GRADE_ROB"),
	///帮会资金
	TONG_GRADE_MONEY = 14 UMETA(DisplayName = "TONG_GRADE_MONEY"),
	///帮会仓库
	TONG_GRADE_STORAGE = 15 UMETA(DisplayName = "TONG_GRADE_STORAGE"),
	///更改职位名称
	TONG_GRADE_RENAME = 16 UMETA(DisplayName = "TONG_GRADE_RENAME"),
	///帮会升级
	TONG_GRADE_UPGRADE = 17 UMETA(DisplayName = "TONG_GRADE_UPGRADE"),
	///帮会升级
	TONG_GRADE_SIGNUP_BHZB = 18 UMETA(DisplayName = "TONG_GRADE_SIGNUP_BHZB"),
};

/**
* 帮会职称
*/
UENUM(BlueprintType)
enum class TONG_TITLE_TYPE : uint8
{
	///帮主
	TONG_TITLE_1 = 0 UMETA(DisplayName = "TONG_TITLE_1"),
	///副帮主
	TONG_TITLE_2 = 1 UMETA(DisplayName = "TONG_TITLE_2"),
	///军师
	TONG_TITLE_3 = 2 UMETA(DisplayName = "TONG_TITLE_3"),
	///长老
	TONG_TITLE_4 = 3 UMETA(DisplayName = "TONG_TITLE_4"),
	///5星帮众
	TONG_TITLE_5 = 4 UMETA(DisplayName = "TONG_TITLE_5"),
	///4星帮众
	TONG_TITLE_6 = 5 UMETA(DisplayName = "TONG_TITLE_6"),
	///3星帮众
	TONG_TITLE_7 = 6 UMETA(DisplayName = "TONG_TITLE_7"),
	///2星帮众
	TONG_TITLE_8 = 7 UMETA(DisplayName = "TONG_TITLE_8"),
	///1星帮众
	TONG_TITLE_9 = 8 UMETA(DisplayName = "TONG_TITLE_9"),
};

/**
* 帮会技能类型
*/
UENUM(BlueprintType)
enum class TONG_SKILL_TYPE : uint8
{
	///玩家技能
	TONG_SKILL_ROLE			= 1 UMETA(DisplayName = "TONG_SKILL_ROLE"),
	///幻兽技能
	TONG_SKILL_PET			= 2 UMETA(DisplayName = "TONG_SKILL_PET"),
};

/**
* 帮会建筑类型
*/
UENUM(BlueprintType)
enum class TONG_BUILD_TYPE : uint8
{	
	///议事大厅
	TONG_BUILDING_TYPE_YSDT	= 0 UMETA(DisplayName = "TONG_BUILDING_TYPE_YSDT"),
	///神兽殿
	TONG_BUILDING_TYPE_SSD	= 1 UMETA(DisplayName = "TONG_BUILDING_TYPE_SSD"),
	///仓库
	TONG_BUILDING_TYPE_CK	= 2 UMETA(DisplayName = "TONG_BUILDING_TYPE_CK"),
	///铁匠铺
	TONG_BUILDING_TYPE_TJP	= 3 UMETA(DisplayName = "TONG_BUILDING_TYPE_TJP"),
	///商店
	TONG_BUILDING_TYPE_SD	= 4 UMETA(DisplayName = "TONG_BUILDING_TYPE_SD"),
	///研究院
	TONG_BUILDING_TYPE_YJY	= 5 UMETA(DisplayName = "TONG_BUILDING_TYPE_YJY"),
	///最大值
	TONG_BUILDING_TYPE_MAX	= 6 UMETA(DisplayName = "TONG_BUILDING_TYPE_MAX"),
};

UENUM(BlueprintType)
enum class TONG_EVENT_SET_TYPE : uint8
{
	///帮会特殊事件
	TONG_SPECIAL_EVENT		= 0 UMETA(DisplayName = "TONG_SPECIAL_EVENT"),
	///帮会升级
	TONG_UPGRADE			= 1 UMETA(DisplayName = "TONG_UPGRADE"),
	///职位变动
	TONG_DUTY_CHANGED		= 2 UMETA(DisplayName = "TONG_DUTY_CHANGED"),
	///成员加入
	TONG_MEMBER_JOIN		= 3 UMETA(DisplayName = "TONG_MEMBER_JOIN"),
	///成员离开
	TONG_MEMBER_LEAVE		= 4 UMETA(DisplayName = "TONG_MEMBER_LEAVE"),
	///资金捐献
	TONG_FUND_DONATION		= 5 UMETA(DisplayName = "TONG_FUND_DONATION"),
	///建筑升级
	TONG_BUILDING_UPGRADE	= 6 UMETA(DisplayName = "TONG_BUILDING_UPGRADE"),
	///技能研发
	TONG_SKILL_DEVELOPMENT	= 7 UMETA(DisplayName = "TONG_SKILL_DEVELOPMENT"),
	///日常维护
	TONG_DAILY_MAINTENANCE	= 8 UMETA(DisplayName = "TONG_DAILY_MAINTENANCE"),
	///资金分配
	TONG_FUND_ALLOCATION	= 9 UMETA(DisplayName = "TONG_FUND_ALLOCATION"),
};

UENUM(BlueprintType)
enum class TONG_EVENT_TYPE : uint8
{
	///帮会加入事件
	TONG_EVENT_JOIN = 0 UMETA(DisplayName = "TONG_EVENT_JOIN"),
	///帮会创建事件
	TONG_EVENT_CREATE = 1 UMETA(DisplayName = "TONG_EVENT_CREATE"),
	///帮会离开事件
	TONG_EVENT_LEAVE = 2 UMETA(DisplayName = "TONG_EVENT_LEAVE"),
	///帮会踢人事件
	TONG_EVENT_TICK = 3 UMETA(DisplayName = "TONG_EVENT_TICK"),
	///帮会任命事件
	TONG_EVENT_APPOINT = 4 UMETA(DisplayName = "TONG_EVENT_APPOINT"),
	///帮会罢免事件
	TONG_EVENT_RECALL = 5 UMETA(DisplayName = "TONG_EVENT_RECALL"),
	///帮会捐献事件
	TONG_EVENT_DONATE = 6 UMETA(DisplayName = "TONG_EVENT_DONATE"),
	///帮会扣除活跃度事件
	TONG_EVENT_SUB_ACTIVITY = 7 UMETA(DisplayName = "TONG_EVENT_SUB_ACTIVITY"),
	///帮会降级警告事件
	TONG_EVENT_DOWN_GRADE_NOTICE = 8 UMETA(DisplayName = "TONG_EVENT_DOWN_GRADE_NOTICE"),
	///帮会降级事件
	TONG_EVENT_DOWN_GRADE = 9 UMETA(DisplayName = "TONG_EVENT_DOWN_GRADE"),
	///帮会升级事件
	TONG_EVENT_UP_GRADE = 10 UMETA(DisplayName = "TONG_EVENT_UP_GRADE"),
	///帮会安全期警告事件
	TONG_EVENT_SAFE_TIME_NOTICE = 11 UMETA(DisplayName = "TONG_EVENT_SAFE_TIME_NOTICE"),
	///帮会禅让帮主事件
	TONG_EVENT_CHANGE_LEADER = 12 UMETA(DisplayName = "TONG_EVENT_CHANGE_LEADER"),
	///帮会建筑升级事件
	TONG_EVENT_UPGRADE_BUILD = 13 UMETA(DisplayName = "TONG_EVENT_UPGRADE_BUILD"),
	///帮会系统强制替换帮主事件
	TONG_EVENT_FORCE_CHANGE_LEADER = 14 UMETA(DisplayName = "TONG_EVENT_FORCE_CHANGE_LEADER"),
	///帮会技能研发开始事件
	TONG_EVENT_REASEARCH_SKILL_BEG = 15 UMETA(DisplayName = "TONG_EVENT_REASEARCH_SKILL_BEG"),
	///帮会技能研发成功事件
	TONG_EVENT_REASEARCH_SKILL_SUC = 16 UMETA(DisplayName = "TONG_EVENT_REASEARCH_SKILL_SUC"),
	///帮会7天保护期正常结束
	TONG_EVENT_PROTECT_DAY_OVER_NORMAL = 17 UMETA(DisplayName = "TONG_EVENT_PROTECT_DAY_OVER_NORMAL"),
	///帮会7天保护期提前结束
	TONG_EVENT_PROTECT_DAY_OVER_ADVAN = 18 UMETA(DisplayName = "TONG_EVENT_PROTECT_DAY_OVER_ADVAN"),
	///帮会升级后，获得1天保护期结束
	TONG_EVENT_PROTECT_DAY_OVER_ONE = 19 UMETA(DisplayName = "TONG_EVENT_PROTECT_DAY_OVER_ONE"),
	///一级帮会保护期减少事件
	TONG_EVENT_PROTECT_DAY_SUB_ONELEVEL = 20 UMETA(DisplayName = "TONG_EVENT_PROTECT_DAY_SUB_ONELEVEL"),
};

UENUM(BlueprintType)
enum class TONG_STORE_EVENT_TYPE : uint8
{
	///帮会仓库存物品事件
	TONG_STORE_EVENT_STORE = 0 UMETA(DisplayName = "TONG_STORE_EVENT_STORE"),
	///帮会仓库取物品事件
	TONG_STORE_EVENT_OBTAIN = 1 UMETA(DisplayName = "TONG_STORE_EVENT_OBTAIN"),
};
/**
* 复活方式
*/
UENUM(BlueprintType)
enum class REVIVE_TYPE : uint8
{
	///原地复活（消耗物品）
	REVIVE_ON_ORIGIN_BY_COST_ITEM = 0 UMETA(DisplayName = "REVIVE_ON_ORIGIN_BY_COST_ITEM"),
	///回城复活
	REVIVE_ON_CITY = 1 UMETA(DisplayName = "REVIVE_ON_CITY"),
	///复活到返回点
	REVIVE_ON_RETURN_POINT = 2 UMETA(DisplayName = "REVIVE_ON_RETURN_POINT"),
	///space文件中reviveScriptID配置的地图复活
	REVIVE_ON_REVIVE_SPACE = 3 UMETA(DisplayName = "REVIVE_ON_REVIVE_SPACE"),
	///副本复活（动态区域）
	REVIVE_ON_SPACE_COPY = 4 UMETA(DisplayName = "REVIVE_ON_SPACE_COPY"),
	///原地复活（消耗金钱）
	REVIVE_ON_ORIGIN_BY_COST_MONEY = 5 UMETA(DisplayName = "REVIVE_ON_ORIGIN_BY_COST_MONEY"),
	///复活点复活（灵脉战场，根据仙魔阵营选择复活点）
	REVIVE_ON_LING_MAI_COPY = 6 UMETA(DisplayName = "REVIVE_ON_LING_MAI_COPY"),
	///复活点复活（冰雪之战，根据仙魔阵营选择复活点）
	REVIVE_ON_FROZEN_FIGHT_COPY = 7 UMETA(DisplayName = "REVIVE_ON_FROZEN_FIGHT_COPY"),
	///帮会争霸第二场的复活方式
	REVIVE_ON_SECOND_TONG_STARCRAFT = 8 UMETA(DisplayName = "REVIVE_ON_SECOND_TONG_STARCRAFT"),
	///灵气迷宫复活方式
	REVIVE_ON_LING_QI = 9 UMETA(DisplayName = "REVIVE_ON_LING_QI"),
	///英雄王座复活方式
	REVIVE_ON_YXLM = 10 UMETA(DisplayName = "REVIVE_ON_YXLM"),
	///帮会争霸第三场的复活方式
	REVIVE_ON_THIRD_TONG_STARCRAFT = 11 UMETA(DisplayName = "REVIVE_ON_THIRD_TONG_STARCRAFT"),
	///金树种子复活方式
	REVIVE_ON_JSZZ = 12 UMETA(DisplayName = "REVIVE_ON_JSZZ"),
	///勇闯绝命岛复活方式
	REVIVE_ON_YCJMD = 13 UMETA(DisplayName = "REVIVE_ON_YCJMD"),
	///上古密阵复活方式
	REVIVE_ON_SGMZ = 14 UMETA(DisplayName = "REVIVE_ON_SGMZ"),
	///烽火连天复活方式
	REVIVE_ON_FHLT = 15 UMETA(DisplayName = "REVIVE_ON_FHLT"),
	///攻城战复活方式
	REVIVE_ON_GCZ = 16 UMETA(DisplayName = "REVIVE_ON_GCZ"),
	///高级练兵场PVP复活方式
	REVIVE_ON_HLBCPVP = 17 UMETA(DisplayName = "REVIVE_ON_HLBCPVP"),
	///练兵场PVP复活方式
	REVIVE_ON_LBCPVP = 18 UMETA(DisplayName = "REVIVE_ON_LBCPVP"),
	///轮回秘境复活方式
	REVIVE_ON_LHMJ = 19 UMETA(DisplayName = "REVIVE_ON_LHMJ"),
	///洞府复活方式
	REVIVE_ON_DONGFU = 20 UMETA(DisplayName = "REVIVE_ON_DONGFU"),
	///帮会掠夺复活方式
	REVIVE_ON_TONG_PLUNDER = 21 UMETA(DisplayName = "REVIVE_ON_TONG_PLUNDER"),
	///帮会争霸 据点争夺战 PVP 复活
	REVIVE_ON_BHZBPOINTWAR_PVP = 22 UMETA(DisplayName = "REVIVE_ON_BHZBPOINTWAR_PVP"),
};

#pragma region ResourceLoadPriority
UENUM(BlueprintType)
enum class RESOURCE_LOAD_PRIORITY_TYPE : uint8
{
	RESOURCE_LOAD_PRIORITY_TYPE_PLAYER			= 0 UMETA(DisplayName = "RESOURCE_LOAD_PRIORITY_TYPE_PLAYER"),
	RESOURCE_LOAD_PRIORITY_TYPE_OTHER_ENTITY	= 1 UMETA(DisplayName = "RESOURCE_LOAD_PRIORITY_TYPE_OTHER_ENTITY"),
	RESOURCE_LOAD_PRIORITY_TYPE_SPACE_EFFECT	= 2 UMETA(DisplayName = "RESOURCE_LOAD_PRIORITY_TYPE_SPACE_EFFECT"),
	RESOURCE_LOAD_PRIORITY_TYPE_EFFECT			= 3 UMETA(DisplayName = "RESOURCE_LOAD_PRIORITY_TYPE_EFFECT"),
	RESOURCE_LOAD_PRIORITY_TYPE_STORY			= 4 UMETA(DisplayName = "RESOURCE_LOAD_PRIORITY_TYPE_STORY"),
	RESOURCE_LOAD_PRIORITY_TYPE_MEDIA			= 5 UMETA(DisplayName = "RESOURCE_LOAD_PRIORITY_TYPE_MEDIA"),
	
	RESOURCE_LOAD_PRIORITY_TYPE_DEFAULT			= 127 UMETA(DisplayName = "RESOURCE_LOAD_PRIORITY_TYPE_DEFAULT"),
};

#pragma endregion
/**
* 邮件发送类型
*/
UENUM(BlueprintType)
enum class MAIL_SEND_TYPE : uint8
{
	MAIL_SENDER_TYPE_PLAYER	= 1 UMETA(DisplayName = "MAIL_SENDER_TYPE_PLAYER"),
	MAIL_SENDER_TYPE_SYS	= 2 UMETA(DisplayName = "MAIL_SENDER_TYPE_SYS"),
};

/**
* 队伍拾取分配方式
*/
UENUM(BlueprintType)
enum class TEAM_PICKUP_TYPE : uint8
{
	TEAM_PICKUP_TYPE_NONE		= 0 UMETA(DisplayName = "TEAM_PICKUP_TYPE_NONE"),
	TEAM_PICKUP_TYPE_FREEDOM	= 1 UMETA(DisplayName = "TEAM_PICKUP_TYPE_FREEDOM"),	//自由拾取
	TEAM_PICKUP_TYPE_TEAM		= 2 UMETA(DisplayName = "TEAM_PICKUP_TYPE_TEAM"),		//队伍拾取（掷点分配）
	TEAM_PICKUP_TYPE_AUCTION	= 3 UMETA(DisplayName = "TEAM_PICKUP_TYPE_AUCTION"),	//竞拍分配
	TEAM_PICKUP_TYPE_CAPTAIN = 4 UMETA(DisplayName = "TEAM_PICKUP_TYPE_CAPTAIN"),	//队长分配
};

/**
* 帮会拾取分配方式
*/
UENUM(BlueprintType)
enum class TONG_PICKUP_TYPE : uint8
{
	TONG_PICKUP_TYPE_NONE = 0 UMETA(DisplayName = "TONG_PICKUP_TYPE_NONE"),
	TONG_PICKUP_TYPE_FREEDOM = 1 UMETA(DisplayName = "TONG_PICKUP_TYPE_FREEDOM"),	//自由拾取
	TONG_PICKUP_TYPE_RALLDOM = 2 UMETA(DisplayName = "TONG_PICKUP_TYPE_RALLDOM"),	//掷点分配
	TONG_PICKUP_TYPE_AUCTION = 3 UMETA(DisplayName = "TONG_PICKUP_TYPE_AUCTION"),	//竞拍分配
	TONG_PICKUP_TYPE_LEADER = 4 UMETA(DisplayName = "TONG_PICKUP_TYPE_LEADER"),		//帮主分配
};

#pragma region 商城
/**
* 商城类型
*/
UENUM(BlueprintType)
enum class STORE_TYPE : uint8
{
	///仙石商城
	STORE_TYPE_XIANSHI = 1 UMETA(DisplayName = "STORE_TYPE_XIANSHI"),
	///灵石商城
	STORE_TYPE_LINGSHI = 2 UMETA(DisplayName = "STORE_TYPE_LINGSHI"),
	///玄石商城
	STORE_TYPE_XUANSHI = 3 UMETA(DisplayName = "STORE_TYPE_XUANSHI"),
	///金钱商城
	STORE_TYPE_JINQIAN = 4 UMETA(DisplayName = "STORE_TYPE_JINQIAN"),
};

/**
* 商城商品类型（一级标签）
*/
UENUM(BlueprintType)
enum class STORE_GOODS_TYPE : uint8
{
	///首页
	STORE_GOODS_TYPE_HOME = 0 UMETA(DisplayName = "STORE_GOODS_TYPE_HOME"),
	///外观
	STORE_GOODS_TYPE_APPEARANCE = 1 UMETA(DisplayName = "STORE_GOODS_TYPE_APPEARANCE"),
	///坐骑
	STORE_GOODS_TYPE_PET = 2 UMETA(DisplayName = "STORE_GOODS_TYPE_PET"),
	///天才地宝
	STORE_GOODS_TYPE_SUNDRIES = 3 UMETA(DisplayName = "STORE_GOODS_TYPE_SUNDRIES"),
	///玄石专区
	STORE_GOODS_TYPE_XUANSHI = 4 UMETA(DisplayName = "STORE_GOODS_TYPE_XUANSHI"),
};
/**
* 商城物品类型（二级标签）
*/
UENUM(BlueprintType)
enum class STORE_ITEM_TYPE : uint8
{
	///衣服
	STORE_ITEM_TYPE_SPECIAL = 1,
	///发型
	STORE_ITEM_TYPE_HAIRS = 2,
	///头饰
	STORE_ITEM_TYPE_HEAD_ADORN = 3,
	///面饰
	STORE_ITEM_TYPE_FACE_ADORN = 4,
	///背饰
	STORE_ITEM_TYPE_BACK_ADORN = 5,
	///腰饰
	STORE_ITEM_TYPE_WAIST_ADORN = 6,
	///披风
	STORE_ITEM_TYPE_CLOAK = 7,
	///环身
	STORE_ITEM_TYPE_BODYS_LIGHT = 8,
	///光效
	STORE_ITEM_TYPE_EFFECT = 9,
	///秘宝
	STORE_ITEM_TYPE_MIBAO = 10,
	///杂货
	STORE_ITEM_TYPE_ZAHUO = 11,
	///点卡
	STORE_ITEM_TYPE_DIANKA = 12,
};

/**
* 商城商品状态
*/
UENUM(BlueprintType)
enum class STORE_GOODS_STATE : uint8
{
	STORE_GOODS_STATE_NONE = 0 UMETA(DisplayName = "STORE_GOODS_STATE_NONE"),
	///下架商品
	STORE_GOODS_STATE_SOLD_OUT = 1 UMETA(DisplayName = "STORE_GOODS_STATE_SOLD_OUT"),
	///新品商品
	STORE_GOODS_STATE_NEW_PRODUCT = 2 UMETA(DisplayName = "STORE_GOODS_STATE_NEW_PRODUCT"),
	///热销商品
	STORE_GOODS_STATE_HOT_SELL = 3 UMETA(DisplayName = "STORE_GOODS_STATE_HOT_SELL"),
};

/**
* 商城礼品盒状态
*/
UENUM(BlueprintType)
enum class STORE_GIFT_STATE : uint8
{
	///礼品默认状态
	STORE_GIFT_STATE_NONE = 0 UMETA(DisplayName = "STORE_GIFT_STATE_NONE"),
	///礼品已过期
	STORE_GIFT_STATE_OVERDUE = 1 UMETA(DisplayName = "STORE_GIFT_STATE_OVERDUE"),
	///礼品对方已接受
	STORE_GIFT_STATE_ACCEPT = 2 UMETA(DisplayName = "STORE_GIFT_STATE_ACCEPT"),
	///礼品对方已拒绝
	STORE_GIFT_STATE_REFUSE = 3 UMETA(DisplayName = "STORE_GIFT_STATE_REFUSE"),
	///礼品已取回
	STORE_GIFT_STATE_RECAPTION = 4 UMETA(DisplayName = "STORE_GIFT_STATE_RECAPTION"),
	///礼品已接受
	STORE_GIFT_STATE_SELF_ACCEPT = 5 UMETA(DisplayName = "STORE_GIFT_STATE_SELF_ACCEPT"),
	///礼品已拒绝
	STORE_GIFT_STATE_SELF_REFUSE = 6 UMETA(DisplayName = "STORE_GIFT_STATE_SELF_REFUSE"),
};
/**
* 商城外观商品状态
*/
UENUM(BlueprintType)
enum class STORE_APPEARANCE_STATE : uint8
{
	STORE_GOODS_STATE_NONE = 0 UMETA(DisplayName = "STORE_GOODS_STATE_NONE"),
	///已拥有未穿戴
	STORE_APPEARANCE_STATE_HAS = 1 UMETA(DisplayName = "STORE_APPEARANCE_STATE_HAS"),
	///已拥有已穿戴
	STORE_APPEARANCE_STATE_WEAR = 2 UMETA(DisplayName = "STORE_APPEARANCE_STATE_WEAR"),
	///未拥有
	STORE_APPEARANCE_STATE_HAS_NOT = 3 UMETA(DisplayName = "STORE_APPEARANCE_STATE_HAS_NOT"),
	///未拥有试穿状态
	STORE_APPEARANCE_STATE_TRY = 4 UMETA(DisplayName = "STORE_APPEARANCE_STATE_TRY"),
	///未拥有倒计时
	STORE_APPEARANCE_STATE_COUNTDOWN = 5 UMETA(DisplayName = "STORE_APPEARANCE_STATE_COUNTDOWN"),
	///已拥有倒计时
	STORE_APPEARANCE_STATE_HAS_COUNTDOWN = 6 UMETA(DisplayName = "STORE_APPEARANCE_STATE_HAS_COUNTDOWN"),
	///曾经拥有（已过期）
	STORE_APPEARANCE_STATE_EXPIRED = 7 UMETA(DisplayName = "STORE_APPEARANCE_STATE_EXPIRED"),
};
#pragma endregion
/**
* 自定义模板值（0-255）
*/
UENUM(BlueprintType)
enum class CUSTOM_DEPTH_STENCIL : uint8
{
	///默认模板值
	CUSTOM_DEPTH_STENCIL_NORMAL = 0,
	///玩家模板值
	CUSTOM_DEPTH_STENCIL_PLAYER = 1,
	///（选中）描边效果
	CUSTOM_DEPTH_STENCIL_OUTLINE = 2,
	///遮挡描边效果
	CUSTOM_DEPTH_STENCIL_OUTLINE_COVER = 3,
	///（五行画卷）描边效果
	CUSTOM_DEEPTH_STENCIL_WXHJ = 4,
};

#pragma region 技能

/*技能目标类型*/
UENUM(BlueprintType)
enum class SKILL_TARGET_TYPE : uint8
{
	///无目标和位置
	SKILL_TARGET_OBJECT_NONE = 0,
	///技能目标是entity
	SKILL_TARGET_OBJECT_ENTITY = 1,
	///技能目标是位置
	SKILL_TARGET_OBJECT_POSITION= 2,
};

/*命中结果*/
UENUM(BlueprintType)
enum class SKILL_HIT_TYPE : uint8
{
	///命中成功
	SKILL_HIT_SUCCEED = 0,
	///命中失败
	SKILL_HIT_FAILED = 1,
	///命中错误
	SKILL_HIT_ERROR = 2,
};

/*技能消息提示*/
UENUM(BlueprintType)
enum class SKILL_MESSAGE : uint8
{
	///没有找到ID={0}的提示信息，确认输入
	DEFAULT_STATUS_MESSAGE = 1,
	///释放成功
	SKILL_GO_ON = 2,
	///无效的目标
	SKILL_CAST_ENTITY_ONLY = 3,
	///指定的技能不存在
	SKILL_NOT_EXIST = 4,
	///你无法执行该操作
	SKILL_UNKNOWN = 5,
	///技能冷却中
	SKILL_NOT_READY = 6,
	///您已经死亡,无法进行该操作
	SKILL_IN_DEAD = 7,
	///您现在无法使用技能
	SKILL_CANT_CAST = 8,
	///法力值不足
	SKILL_OUTOF_MP = 9,
	///请选择一个施法位置
	SKILL_MISS_POSITION = 10,
	///只能对一个位置施放
	SKILL_CAST_POSITION_ONLY = 11,
	///目标距离过远，请靠近后使用
	SKILL_TOO_FAR = 12,
	///距离目标太近
	SKILL_TOO_NEAR = 13,
	///没有找到施法目标
	SKILL_MISS_TARGET = 14,
	///只能对可攻击敌人施展
	SKILL_NOT_ENEMY_ENTITY = 15,
	///血量不足
	SKILL_OUTOF_HP = 16,
	///当前状态下,无法进行该操作
	SKILL_STATE_CANT_CAST = 17,
	///释放失败
	SKILL_CAST_FAILED = 18,
	///正在施法中，请稍后再试！
	SKILL_IS_CASTING = 19,
	///AI中断当前释放技能
	SKILL_AI_INTERRUPT = 20,
	///技能[{0}]施展成功！
	SKILL_CAST_SUCCESS = 23,
	///指定位置无效，请重新选择
	SKILL_CAST_POS_FAIL = 24,
	///罡气值不足
	SKILL_OUTOF_GANGQI = 25,
	///该地图不允许释放该技能
	SKILL_SPACE_FORBID = 26,
	///物品不足
	SKILL_OUTOF_ITEM = 27,
	///目标的法力值不足
	SKILL_TARGET_OUTOF_MP = 29,
	///目标的血量不足
	SKILL_TARGET_OUTOF_HP = 30,
	///目标的罡气值不足
	SKILL_TARGET_OUTOF_GANGQI = 31,
	///目标的物品不足
	SKILL_TARGET_OUTOF_ITEM = 32,
	///目标在当前状态下,无法进行该操作
	SKILL_TARGET_STATE_CANT_CAST = 33,
	///目标的技能冷却中
	SKILL_TARGET_NOT_READY = 34,
	///未中目标
	SKILL_OUT_RATE_FAIL = 35,
};

/*技能打击范围 单位基准*/
UENUM(BlueprintType)
enum class SKILL_HIT_AREA_UNIT : uint8
{
	///绝对坐标(0,0,0)
	SKILL_HIT_AREA_UNIT_ABSOLUTE = 0,
	///施法者单位
	SKILL_HIT_AREA_UNIT_CASTER = 1,
	///施法目标单位
	SKILL_HIT_AREA_UNIT_TARGET = 2,
};

/*技能打击范围 朝向基准*/
UENUM(BlueprintType)
enum class SKILL_HIT_AREA_DIRE : uint8
{
	///绝对方向(0,0,0)
	SKILL_HIT_AREA_DIRE_ABSOLUTE = 0,
	///施法者单位（当前朝向）
	SKILL_HIT_AREA_DIRE_CASTER = 1,
	///施法目标单位（当前朝向）
	SKILL_HIT_AREA_DIRE_TARGET = 2,
	///施法者→施法目标（2D朝向）
	SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET = 3,
	///施法目标→施法者（2D朝向）
	SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER = 4,
	///施法者→施法目标（3D朝向）
	SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET_3D = 5,
	///施法目标→施法者（3D朝向）
	SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER_3D = 6,
};

/*持有效果来源类型*/
UENUM(BlueprintType)
enum class HOLD_EFFECT_SOURCE_TYPE : uint8
{
	///SKILL
	HOLD_EFFECT_SOURCE_TYPE_SKILL = 1,
	///BUFF
	HOLD_EFFECT_SOURCE_TYPE_BUFF = 2,
	///固定ID
	HOLD_EFFECT_SOURCE_TYPE_FIX_ID = 3,
};

/*Buff结束的原因*/
UENUM(BlueprintType)
enum class BUFF_END_RESON : uint8
{
	///Buff持续时间结束
	BUFF_END_RESON_BY_TIME_OVER = 1,
	///Buff打断
	BUFF_END_RESON_BY_INTERRUPT = 2,
	///Buff顶替
	BUFF_END_RESON_BY_REPLACE = 3,
	///玩家下线
	BUFF_END_RESON_BY_OFFLINE = 4,
};

/*BuffHitBack击退类型*/
UENUM(BlueprintType)
enum class BUFF_HIT_TYPE : uint8
{
	///施法者当前方向
	BUFF_HIT_TYPE_CASTER_FORWARD = 0,
	///施法者反方向
	BUFF_HIT_TYPE_CASTER_REAR,
	///施法者->受术者当前方向
	BUFF_HIT_TYPE_CATORE_FORWARD,
	///施法者->受术者反方向
	BUFF_HIT_TYPE_CATORE_REAR,
	///受术者当前方向
	BUFF_HIT_TYPE_RECEIVER_FORWARD,
	///受术者反方向
	BUFF_HIT_TYPE_RECEIVER_REAR,
};

/*BuffHitBack目标朝向类型*/
UENUM(BlueprintType)
enum class BUFF_HIT_DIRECTION : uint8
{
	///施法者当前朝向
	BUFF_HIT_TYPE_CASTER_DIRECTION = 0,
	///施法者反朝向
	BUFF_HIT_TYPE_CASTER_RDIRECTION,
	///施法者->受术者当前朝向
	BUFF_HIT_TYPE_CATORE_DIRECTION,
	///施法者->受术者反朝向
	BUFF_HIT_TYPE_CATORE_RDIRECTION,
	///受术者当前朝向
	BUFF_HIT_TYPE_RECEIVER_DIRECTION,
	///受术者反朝向
	BUFF_HIT_TYPE_RECEIVER_RDIRECTION,
};

/**
* 跳伞状态
*/
UENUM(BlueprintType)
enum class PARACHUTE_STATE : uint8
{
	/// 正常状态
	PARACHUTE_STATE_NORMAL = 0 UMETA(DisplayName = "PARACHUTE_STATE_NORMAL"),
	/// 飞行器状态
	PARACHUTE_STATE_CARRIER = 1 UMETA(DisplayName = "PARACHUTE_STATE_CARRIER"),
	/// 自由下落状态
	PARACHUTE_STATE_FALL = 2 UMETA(DisplayName = "PARACHUTE_STATE_FALL"),
	/// 开伞状态
	PARACHUTE_STATE_OPEN = 3 UMETA(DisplayName = "PARACHUTE_STATE_OPEN"),
};

/**
* 归属类型
*/
UENUM(BlueprintType)
enum class BELONG_SIDE : uint8
{	
	/// 归属进攻方
	BELONG_SIDE_ATTACK = 0 UMETA(DisplayName = "BELONG_SIDE_ATTACK"),
	/// 归属防守方
	BELONG_SIDE_PROTECT = 1 UMETA(DisplayName = "BELONG_SIDE_PROTECT"),
};


UENUM(BlueprintType)
enum class CC_MODE_REASON : uint8
{
	///初始化控制模式
	CCM_INIT_CONTROLLER_MODE = 0 UMETA(DisplayName = "Init Controller Mode"),
	///选择ALT控制模式
	CCM_ALT_CONTOLLER_MODE = 1 UMETA(DisplayName = "Select ALT Controller Mode"),
	///选择Y控制模式
	CCM_Y_CONTROLLER_MODE = 2 UMETA(DisplayName = "Select Y Controller Mode"),
	///选择恢复控制模式
	CCM_RECOVERY_CONTROLLER_MODE = 3 UMETA(DisplayName = "Recovery Controller Mode"),
	///选择FromACTToALT控制模式
	CCM_ACTTOALT_CONTROLLER_MODE = 4 UMETA(DisplayName = "Select FromACTToALT Controller Mode"),
	///选择金丹控制模式
	CCM_JINDAN_CONTROLLER_MODE = 5 UMETA(DisplayName = "Select JINDAN Controller Mode"),	
	///选择YcjmdSkyCarrier控制模式
	CCM_YJSC_CONTROLLER_MODE = 6 UMETA(DisplayName = "Select YJSC Controller Mode"),
	///选择YcjmdParachute控制模式
	CCM_YJP_CONTROLLER_MODE = 7 UMETA(DisplayName = "Select YJP Controller Mode"),
	///选择Vehicle控制模式
	CCM_VEHICLE_CONTROLLER_MODE = 8 UMETA(DisplayName = "Select Vehicle Controller Mode"),
	///选择Gliding控制模式
	CCM_GLIDING_CONTROLLER_MODE = 9 UMETA(DisplayName = "Select Gliding Controller Mode"),
	///选择FlyDekuvery控制模式
	CCM_FLYDK_CONTROLLER_MODE = 10 UMETA(DisplayName = "Select FlyDekuvery Controller Mode"),
	///选择HeHua控制模式
	CCM_HEHUA_CONTROLLER_MODE = 11 UMETA(DisplayName = "Select HeHua Controller Mode"),
	///选择LeiZhen控制模式
	CCM_LEIZHEN_CONTROLLER_MODE = 12 UMETA(DisplayName = "Select LeiZhen Controller Mode"),
	///选择ShootMode控制模式
	CCM_SHOOTMODE_CONTROLLER_MODE = 13 UMETA(DisplayName = "Select ShootMode Controller Mode"),
	///选择ShenFengMiJing控制模式
	CCM_SFMJ_CONTROLLER_MODE = 14 UMETA(DisplayName = "Select ShenFengMiJing Controller Mode"),
	///选择ShenFengMiJing降落控制模式
	CCM_SFMJJL_CONTROLLER_MODE = 15 UMETA(DisplayName = "Select ShenFengMiJing JiangLuo Controller Mode"),
	///选择飞升控制模式
	CCM_GOUP_CONTROLLER_MODE = 16 UMETA(DisplayName = "Select GOUP Controller Mode"),
	///选择ArderMiJing控制模式
	CCM_AMJ_CONTROLLER_MODE = 17 UMETA(DisplayName = "Select ArderMiJing Controller Mode"),
	///选择Battery控制模式
	CCM_BATTERY_CONTROLLER_MODE = 18 UMETA(DisplayName = "Select Battery Controller Mode"),
	///选择GhostEye控制模式
	CCM_GHOSTEYE_CONTROLLER_MODE = 19 UMETA(DisplayName = "Select GhostEye Controller Mode"),
	///选择MoveVehicle控制模式
	CCM_MOVEVEHICLE_CONTROLLER_MODE = 20 UMETA(DisplayName = "Select MoveVehicle Controller Mode"),	
	///选择RotateRroundToTarget控制模式
	CCM_RRTT_CONTROLLER_MODE = 21 UMETA(DisplayName = "Select RotateRroundToTarget Controller Mode"),	
	///选择FuShen控制模式
	CCM_FUSHEN_CONTROLLER_MODE = 22 UMETA(DisplayName = "Select FuShen Controller Mode"),
	///选择UserSetting控制模式
	CCM_USERSETTING_CONTROLLER_MODE = 23 UMETA(DisplayName = "Select UserSetting Controller Mode"),
	///选择OperSetMode控制模式
	CCM_OPERSETMODE_CONTROLLER_MODE = 24 UMETA(DisplayName = "Select OperSetMode Controller Mode"),
	///选择回复配置的控制模式
	CCM_RECOVERY_SETTING_CONTROLLER_MODE = 25 UMETA(DisplayName = "Recovery Settging Controller Mode"),
	///选择练兵控制模式
	CCM_TRAIN_SOLDIER_MODE = 26 UMETA(DisplayName = "Train Soldier Controller Mode"),
};

#pragma endregion