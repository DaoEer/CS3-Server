#pragma once

#include "CoreMinimal.h"
#include "GameDeFine.h"
/**
* 文件名称：ConstData.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：All
* 创建时间：2017-08-17
*/

/************************************************************************/
/* 游戏全局常量定义                                                     */
/************************************************************************/

const float AUTO_NAVIGATE_GUIDE_DISTANCE = 300.0f;	//<每个路点相隔的距离
const int AUTO_NAVIGATE_GUIDE_SHOW_EFFECT_NUM = 5;	//<显示的贴画效果的个数
const float AUTO_NAVIGATE_GUIDE_POINT_CHECK_DISTANCE = 300.0f;	//<检测玩家靠近多近就消失的距离
const FString AUTO_NAVIGATE_GUIDE_EFFECTID_LIST[2] = { TEXT("100087"), TEXT("100656") };//<寻路路点效果ID列表，普通材质使用第一个，半透明材质使用第二个
const FString AUTO_NAVIGATE_GUIDE_EFFECTID = TEXT("101482");//<寻路路点效果ID
const float QUEST_NAVIGATE_FIND_RANGE = 10 * 100.0f;	//任务寻路查找范围
const float QUEST_NAVIGATE_GOSSIP_DISTANCE = 2;	//任务靠近以后对话距离
const float AUTO_NAVIGATE_WATER_JUMP_PROBABILITY = 0.8f;		//自动寻路水面跳跃概率
const float AUTO_NAVIGATE_WATER_JUMP_CHECK_TIME = 8.0f;			//自动寻路水面跳跃检测频率
const float AUTO_NAVIGATE_PLAYER_NEARBY_DISTANCE = 1.5f;		//<自动寻路玩家靠近距离，单位m

const int STAND_ONE_SECTION_JUMP_SKILLID = 240000001;			// 站立一段跳技能ID
const int MOVE_ONE_SECTION_JUMP_SKILLID = 240001001;			// 前进一段跳技能ID
const int TWO_SECTION_JUMP_SKILLID = 240002001;					// 二段跳技能ID
const int THREE_SECTION_JUMP_SKILLID = 240003001;				// 三段跳技能ID
const int ONE_JUMP_HEIGHT = 300;				// 一段跳高度
const int TWO_JUMP_HEIGHT = 300;				// 二段跳高度
const int THREE_JUMP_HEIGHT = 400;				// 三段跳高度

const int32 AUTO_NAVIGATE_MAX_SEARCH_DISTANCE = 50.0f * 100.0f;		// 路点搜寻最大距离
const int32 AUTO_NAVIGATE_DIRECT_ARRIVE_DISTANCE = 5.0f * 100.0f;		// 配置路线到最终点直接可达最大距离
const int32 AUTO_NAVIGATE_PATH_START_OR_END_DISTANCE = 1.0f * 100.0f;	// 配置路线到起始点或者是最终点差距
const int32 AUTO_NAVIGATE_MIN_DISTANCE = 10.0f;		//路点之间最小差距，小于这个值，认为是同一个点

const float AUTO_ATTACK_FRIEND_ENTITY_CHECK_TIME = 1.0f;		// 检测攻击友方entity的频率

const FString CARRIER_ID = FString(TEXT("10001"));				// 飞剑carried表id

const int32 SHIELD_MAX_ROW_LENGTH = 1500;						// 屏蔽字最大行长度

const int32 TONG_CREATE_NEED_MONEY = 10000;					// 创建帮会需要消耗10000铜
const int32 TONG_CREATE_MIX_LEVEL = 20;							// 创建帮会最低等级
const int32 TONG_CREATE_MIX_JINJIELEVEL = 4;					// 创建帮会玩家境界等级必须达到4级
const int32 TONG_JOIN_MIX_LEVEL = 20;							// 加入帮会最低等级
const int32 APPLY_JOIN_MAX_LIST = 10;							// 申请入帮会的最大数
const int32 REQUEST_TONG_JOIN_TIME = 5;							// 5分钟最小间隔请求服务器时间
const int32 REQUEST_TONG_EVENT_TIME = 5;						// 5分钟最小间隔请求服务器时间
const FString TONG_SHOPID = FString(TEXT("TongShop"));			// 帮会商店ID
const FString TONG_PLUNDER_SHOPID = FString(TEXT("TongPlunderShop"));			// 帮会商店帮会掠夺战分页商店ID

const int32 RELATION_CATALOG_TYPE_FOE_LIST = -2;				// 不友好（仇人）
const int32 RELATION_CATALOG_TYPE_BLEACK_LIST = -1;				// 黑名单分组(不用define，是因为玩家可以自己添加)
const int32 RELATION_CATALOG_TYPE_LASTTIME_LIST = 0;			// 最近联系人分组
const int32 RELATION_CATALOG_TYPE_FRIEND_LIST = 1;				// 好友分组

const int32 EQUIP_SHUFFLE_MIX_LEVEL = 30;						// 装备洗练最小等级
const int32 EQUIP_RECAST_MIX_LEVEL = 30;						// 装备重铸最小等级

const int32 COMMON_BAG_START = 64;						// 普通背包起始位置
const int32 COMMON_BAG_CAPACITY = 48;					// 默认开启普通背包格子数
const int32 COMMON_BAG_LOCK_CAPACITY = 72;				// 道具背包可解锁数量

const int32 QUEST_BAG_CAPACITY = 48;						// 任务背包容量
const int32 CRYSTAL_BAG_CAPACITY = 80;					// 晶核背包容量

const int32 STORE_CAPACITY = 100;						// 默认仓库容量
const int32 STORE_LOCK_CAPACITY = 100;					// 仓库锁定容量

const int32 TONG_CAPACITY = 480;						// 帮会仓库容量
const int32 SPACE_COPY_BAG_CAPACITY = 24;				// 副本背包容量
const int32 SPACE_COPY_YXLM1_BAG_CAPACITY = 4;			// 副本英雄联盟背包1容量
const int32 SPACE_COPY_YXLM_BAG_OTHER_CAPACITY = 1;		// 副本英雄联盟其他背包容量

const int32 STORE_LOCKERS_CAPACITY = 30;				// 轮回秘境储物柜 默认仓库容量
const int32 STORE_LOCKERS_LOCK_CAPACITY = 70;			// 轮回秘境储物柜 锁定容量
const int32 BAG_WORK_SHOP_LOCKERS_START = 1023;			// 工具储物柜开始位置
const int32 BAG_ALCHEMIST_LOCKERS_START = 1123;			// 乾坤鼎储物柜开始位置

const int32 STORE_APPEARANCE_CAPACITY = 500;			// 外观隐藏背包容量
const int32 BAG_APPEARANCES_START = 1223;			// 外观隐藏背包开始位置


const float RESURRECTION_PANEL_OPEN_TIME = 3.0f;		// 死亡后弹出死亡面板间隔时间
const float AUTO_REVIVE_DELAY_TIME = 5.0f;				// 自动复活的延迟时间

const int32 GAME_RANKING_PAGE_NUM = 10;					// 排行榜每页显示数量

const float TEAM_FOLLOW_DETECT_TICK = 0.05;				/// 组队跟随侦测时间间隔
const float TEAM_FOLLOW_WAIT_TIME = 8.0;				/// N秒内找不到队长则退出跟随
const float TEAM_FOLLOW_KEEP_DISTANCE = 3.0;			/// 跟随与队长保持的距离
const float TEAM_FOLLOW_DISTANCE = 15.0;				/// 队伍跟随有效距离

const float SKILL_CAST_RANGE_MAX = 99999999.0;				/// 最大施法距离

#pragma region ResourceLoadPriority
const int32 RESOURCE_LOAD_DISTANCE[3] = { 1000, 3000, 5000 };
#pragma endregion

///各职业技能心法ID数据
const TMap<int32, TArray<int32>> PROFESSION_POSTURE_MAP = { {1,{190101001, 190201001}},{2,{200101001, 200201001}},{3,{210101001, 210201001}},{4,{220101001, 220201001}} };

///技能目标类型筛选的参数选项清单
const TMap<ENTITY_TYPE, FString> ENTITY_TYPE_DICT = { {ENTITY_TYPE::ENTITY_FLAG_ROLE,TEXT("Role")}, {ENTITY_TYPE::ENTITY_FLAG_MONSTER,TEXT("Monster")}, {ENTITY_TYPE::ENTITY_FLAG_SPELL,TEXT("SpellBox")},
											{ENTITY_TYPE::ENTITY_FLAG_TRAP,TEXT("Trap")}, {ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET,TEXT("Pet")} };


/// 基础属性对应关系
const TMap<int32, FString>PROPERTYIDTOSTR = {{30001,"corporeity"}, {30002,"strength"}, {30003,"intellect"}, {30004,"discern"},
											{30005,"dexterity"}, {30006,"HP_Max"}, {30007,"MP_Max"}, {30008,"damage"}, {30009,"magic_damage"},
											{30010,"armor"},{30001,"corporeity"}, {30001,"corporeity"}, {30001,"corporeity"}, 
											{30001,"corporeity"}, {30001,"corporeity"}, {30001,"corporeity"} };

// 原兽刷新兽栏中心
const TArray<FVector> ORIGIN_PET_SPAWN_POS = { FVector(-6350.000000, 1050.000000, 11356.000000), FVector(-6350.000000, 1850.000000, 11356.000000),
											FVector(-7050.000000, 1050.000000, 11356.000000), FVector(-7050.000000, 1850.000000, 11356.000000),
											FVector(-7750.000000, 1050.000000, 11356.000000), FVector( -7750.000000, 1850.000000, 11356.000000) };
// 原兽逃跑位置
const TArray<FVector> ORIGIN_PET_RUN_POS = { FVector(-6325.0, 1431.0, 11356.0), FVector(-6978.0, 1434.0, 11356.0),FVector(-7696.0, 1414.0, 11356.0) };
const FVector ORIGIN_PET_RUN_LAST_POS = FVector(-5719.0, 1436.0, 11356.0);

// 灵田刷新位置
const TArray<FVector> LHMJ_LING_TIAN_POS = { FVector(210.0,190.0,-95.0), FVector(60.0,190.0,-95.0),
											FVector(210.0,-190.0,-95.0), FVector(60.0,-190.0,-95.0) };

// 灵田模型
const FString LHMJ_LING_TIAN_MODEL = TEXT("SM_ZW0436");

//灵田 scriptID
const TMap<int32, FString> LHMJ_LT_SCRIPTS = { {0,"40000938"},{1,"40000939"},{2,"40000940"},{3,"40000941"} };

// 武器部位
const TArray<int32> EQUIP_WEAPON = { 31,32,33 };
// 防具部位
const TArray<int32> EQUIP_ARMOR = { 20,21,22,23,24,25,26,34 };
// 饰品
const TArray<int32> EQUIP_JEWELRY = { 27,28,29 };

// 练兵任务 系统刷新时间
const TArray<int32> TRAIN_GQUEST_REFRESH_TIME = { 11, 16 ,20 };

// 轮回秘境 界面一页显示多少 洞府 对应服务器 Const.LHMJ_DONG_FU_SHOW_ENTRY
const int32 LHMJ_DONG_FU_SHOW_ENTRY = 10;
// 轮回秘境大地图scriptID
const FString LUN_HUI_MI_JIN_SCRIPTID = "L_LHMJ_1";
// 洞府scriptID
const TMap<int32, FString> DONG_FU_SCRIPTIDS_MAP = { {1, "L_LHMJDF"}, {3, "L_LHMJDF2"} };

// 帮会建筑命名
const TMap<TONG_BUILD_TYPE, FString> TONG_BUILD_NAMES = {
	{TONG_BUILD_TYPE::TONG_BUILDING_TYPE_YSDT, TEXT("议事大厅")},{TONG_BUILD_TYPE::TONG_BUILDING_TYPE_SSD, TEXT("神兽殿")},
	{TONG_BUILD_TYPE::TONG_BUILDING_TYPE_CK, TEXT("仓库")},{TONG_BUILD_TYPE::TONG_BUILDING_TYPE_TJP, TEXT("铁匠铺")},
	{TONG_BUILD_TYPE::TONG_BUILDING_TYPE_SD, TEXT("商店")},{TONG_BUILD_TYPE::TONG_BUILDING_TYPE_YJY, TEXT("研究院")} };

// 王道神兵前缀
const FString KingCraft_Prefix = TEXT("神兵");

// 帮会宝箱打开效果ID
const FString Tong_DropBox_OpenEffectID = TEXT("103088");
const FString Tong_DropBox_StayEffectID = TEXT("103088_3");
// 帮会宝箱物品确定归属后飞行效果
const FString Tong_DropBox_FlyEffectID = TEXT("103088_1");

// 勇闯绝命岛
// 飞行器 骑乘ID
const FString Parachute_CarrierID = TEXT("10040");
// 飞行器左右光效
const FString Parachute_RCarrierParticleID = TEXT("103093_1");
const FString Parachute_LCarrierParticleID = TEXT("103093_2");
// 风声
const FString Parachute_WindVoiceID = TEXT("S001086");
// 开降落伞的声音
const FString Parachute_OpenVoiceID = TEXT("S001087");
// 降落伞背包
const FName Parachute_BagID = TEXT("YCJMD_ParachuteBag");
// 下落的云雾效果
const FString Parachute_YunParticleID = TEXT("103093");
// 开伞动作
const FName Parachute_OpenActionID = TEXT("OpenParachute");
// 准备着落动作
const FName Parachute_ReadyLandActionID = TEXT("ReadyLand");
// 着落动作
const FName Parachute_LandActionID = TEXT("SkyDivingLand");
// 性别对应跳伞下落的动作资源表
const TMap<uint8, FString> Parachute_SexActionTable = { {1, "SK_PC_M_YCJMDParachute"},{2,"SK_PC_F_YCJMDParachute"} };
// 大荒战场头顶UI显示距离
const float YCJMD_HeadUIShowDist_Far = 12000;//头顶信息可显示的最大距离
const float YCJMD_HeadUIShowDist_Near = 2500;//头顶信息换成小图标的距离

const FVector CONST_COLOR_RED = FVector(3.5f, 0.f, 0.f);
const FVector CONST_COLOR_BLUE = FVector(0.f, 0.f, 3.5f);
