#pragma once

/**
* 文件名称：ItemEnum.h
* 功能说明：物品相关枚举
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-01-11
*/

UENUM(BlueprintType)
enum class EINITBINDTYPE : uint8
{
	//无绑定
	NONE_BIND = 0 UMETA(DisplayName = "NONE_BIND"),
	//拾取绑定
	PICKUP_BIND = 1 UMETA(DisplayName = "PICKUP_BIND"),
	//装备绑定
	EQUIP_BIND = 2 UMETA(DisplayName = "EQUIP_BIND"),
	//默认绑定
	IS_BIND = 3 UMETA(DisplayName = "IS_BIND"),
};

UENUM(BlueprintType)
enum class EBINDTYPE : uint8
{
	//不绑定
	BIND_NONE = 0 UMETA(DisplayName = "BIND_NONE"),
	//绑定
	BINDED = 1 UMETA(DisplayName = "BINDED"),

};
UENUM(BlueprintType)
enum class ITEM_USE_AMOUTN_REFRESH_TYPE : uint8
{
	//永久
	ITEM_USE_AMOUTN_REFRESH_TYPE_FOREVER = 1 UMETA(DisplayName = "ITEM_USE_AMOUTN_REFRESH_TYPE_FOREVER"),
	//每天
	ITEM_USE_AMOUTN_REFRESH_TYPE_DAY = 2 UMETA(DisplayName = "ITEM_USE_AMOUTN_REFRESH_TYPE_DAY"),
	//每周
	ITEM_USE_AMOUTN_REFRESH_TYPE_WEEK = 3 UMETA(DisplayName = "ITEM_USE_AMOUTN_REFRESH_TYPE_WEEK"),
	//每月
	ITEM_USE_AMOUTN_REFRESH_TYPE_MONTH = 4 UMETA(DisplayName = "ITEM_USE_AMOUTN_REFRESH_TYPE_MONTH"),
};


// 物品大类，此枚举根据策划配置定义（D_ItemTypeInfoCfg），不能私自定义
enum class ITEM_TYPE : uint16
{
	// 默认
	ITEM_TYPE_DEFAULT = 0,
	// 武器
	ITEM_TYPE_WEAPON = 10001,
	// 帽子
	ITEM_TYPE_HAT = 10002,
	// 衣服
	ITEM_TYPE_COAT = 10003,
	// 裤子
	ITEM_TYPE_PANTS = 10004,
	// 腰带
	ITEM_TYPE_BELT = 10005,
	// 护腕
	TEM_TYPE_WRIST = 10006,
	// 手套
	ITEM_TYPE_GLOVES = 10007,
	// 鞋子
	ITEM_TYPE_SHOES = 10008,
	// 项链
	ITEM_TYPE_NECKLACE = 10009,
	// 戒指
	ITEM_TYPE_RING = 10010,
	// 时装
	ITEM_TYPE_FASHION = 10011,
	// 杂物
	ITEM_TYPE_VARIA = 20001,
	// 气血药
	ITEM_TYPE_BDRUG = 20002,
	// 内息药
	ITEM_TYPE_EDRUG = 20003,
	// 幻兽气血药
	ITEM_TYPE_PBDRUG = 20004,
	// 幻兽内息药
	ITEM_TYPE_PEDRUG = 20005,
	// 幻兽蛋
	ITEM_TYPE_PETEGG = 20006,
	// 系统功能
	ITEM_TYPE_SYSTEM = 20007,
	// 晶核
	ITEM_TYPE_SPAR = 20008,
	// 材料
	ITEM_TYPE_MATERIAL = 20009,
	// 卷轴
	ITEM_TYPE_SCROLL = 20010,
	// 符咒
	ITEM_TYPE_CHARM = 20011,
	// 礼包
	ITEM_TYPE_GIFT = 20012,
	// 幻兽被动技能书
	ITEM_TYPE_PPSKILL = 20013,
	// 任务物品
	ITEM_TYPE_QUEST = 30001,
	// 活动物品
	ITEM_TYPE_ACTIVE = 30002,
	// 副本物品
	ITEM_TYPE_COPY = 30003,
	// 半成品装备
	ITEM_TYPE_PART_EQUIP = 30010,
	// 图纸
	ITEM_TYPE_BPRINT = 30011,
	// 玲珑玉令
	ITEM_TYPE_JADE = 30012,

};


//格子在背包对应的位置
/**
UENUM(BlueprintType)
enum class Equip_Solt_Index_In_Bag: uint8
{
	///裸体-身体(其它部位包含在身体中)
	MODEL_PART_BODYS = 10 UMETA(DisplayName = "MODEL_PART_BODYS"),
	///裸体-头部
	MODEL_PART_HEADS = 11 UMETA(DisplayName = "MODEL_PART_HEADS"),
	///套装
	MODEL_PART_SUITS = 12 UMETA(DisplayName = "MODEL_PART_SUITS"),
	///头发
	MODEL_PART_HAIRS = 13 UMETA(DisplayName = "MODEL_PART_HAIRS"),
	///头饰
	MODEL_PART_ADORN = 14 UMETA(DisplayName = "MODEL_PART_ADORN"),
	///帽子
	MODEL_PART_HAT	 = 20 UMETA(DisplayName = "MODEL_PART_HAT"),
	///上衣
	MODEL_PART_COATS = 21 UMETA(DisplayName = "MODEL_PART_COATS"),
	///护腕
	MODEL_PART_WRIST = 22 UMETA(DisplayName = "MODEL_PART_WRIST"),
	///手套
	MODEL_PART_HAND = 23 UMETA(DisplayName = "MODEL_PART_HAND"),
	///腰带
	MODEL_PART_WAIST = 24 UMETA(DisplayName = "MODEL_PART_WAIST"),

	///裤子
	MODEL_PART_PANTS = 25 UMETA(DisplayName = "MODEL_PART_PANTS"),

	///鞋子
	MODEL_PART_SHOES = 26 UMETA(DisplayName = "MODEL_PART_SHOES"),

	///项链
	MODEL_PART_NECKLACE = 27 UMETA(DisplayName = "MODEL_PART_NECKLACE"),

	///左手戒指
	MODEL_PART_LHAND_RING = 28 UMETA(DisplayName = "MODEL_PART_LHAND_RING"),

	///右手戒指
	MODEL_PART_RHAND_RING = 29 UMETA(DisplayName = "MODEL_PART_RHAND_RING"),

	///武器-双手
	MODEL_PART_BHADN_WEAPON = 31 UMETA(DisplayName = "MODEL_PART_BHADN_WEAPON"),

	///武器-左手
	MODEL_PART_LHAND_WEAPON = 32 UMETA(DisplayName = "MODEL_PART_LHAND_WEAPON"),

	///武器-右手
	MODEL_PART_RHAND_WEAPON = 33 UMETA(DisplayName = "MODEL_PART_RHAND_WEAPON"),

	///披风
	MODEL_PART_CLOAK = 63 UMETA(DisplayName = "MODEL_PART_CLOAK"),
};
*/

