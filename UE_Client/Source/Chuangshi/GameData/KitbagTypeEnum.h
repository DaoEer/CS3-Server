#pragma once
#include "CoreMinimal.h"
#include "KitbagTypeEnum.generated.h"

/**
* 文件名称：KitbagTypeEnum.h
* 功能说明：背包枚举
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-01-17
*/

UENUM(Blueprintable)
enum class EKITBAGTYPE :uint8
{
	//装备
	EQUIP = 0 UMETA(DisplayName = "EQUIP"),
	//普通
	COMMON = 1 UMETA(DisplayName = "COMMON"),
	//任务
	QUEST = 2  UMETA(DisplayName = "QUEST"),
	//晶核
	CRYSTAL = 3 UMETA(DisplayName = "CRYSTAL"),
	//仓库
	STORE	= 4 UMETA(DisplayName = "STORE"),
	//帮会仓库
	TONG_STORE = 5 UMETA(DisplayName = "TONG_STORE"),
	//玩家副本专用背包
	SPACE_COPY_BAG = 6 UMETA(DisplayName = "SPACE_COPY_BAG"),
	//英雄联盟背包1
	BAG_SPACE_COPY_YXLM1 = 7 UMETA(DisplayName = "BAG_SPACE_COPY_YXLM1"),
	//英雄联盟背包2
	BAG_SPACE_COPY_YXLM2 = 8 UMETA(DisplayName = "BAG_SPACE_COPY_YXLM2"),
	//英雄联盟背包3
	BAG_SPACE_COPY_YXLM3 = 9 UMETA(DisplayName = "BAG_SPACE_COPY_YXLM3"),
	//英雄联盟背包4
	BAG_SPACE_COPY_YXLM4 = 10 UMETA(DisplayName = "BAG_SPACE_COPY_YXLM4"),
	//工坊储物柜
	BAG_TOOL = 11 UMETA(DisplayName = "BAG_TOOL"),
	//乾坤鼎储物柜
	BAG_TRIPOD = 12 UMETA(DisplayName = "BAG_TRIPOD"),
	//外观隐藏背包
	BAG_APPEARANCE = 13 UMETA(DisplayName = "BAG_APPEARANCE"),
	//临时装备背包 #CST - 12212 阵营竞技“大荒战场50人PVP”
	BAG_TEMP_EQUIP = 14 UMETA(DisplayName = "BAG_TEMP_EQUIP"),
};


