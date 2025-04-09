// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "UObject/NoExportTypes.h"
#include "GameData/GameDeFine.h"
#include "ConstDataBP.generated.h"

/**
* 文件名称：ConstDataBP.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-04-06
*/

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UConstDataBP : public UObject
{
	GENERATED_BODY()

public:
	UConstDataBP();

	static UConstDataBP* GetInstance();

	///登录关卡
	UPROPERTY(BlueprintReadOnly, Category = "Level")
		FString LOGIN_LEVEL = TEXT("L_LoginTest");
	///角色选择关卡
	UPROPERTY(BlueprintReadOnly, Category = "Level")
		FString SELECT_ROLE_LEVEL = TEXT("L_Login_2S");
	///角色选择关卡
	UPROPERTY(BlueprintReadOnly, Category = "Level")
		FString CREATE_ROLE_LEVEL = TEXT("L_Login_C");
	///阵营选择关卡
	UPROPERTY(BlueprintReadOnly, Category = "Level")
		FString SELECT_CAMP_LEVEL = TEXT("L_ZYXZ");

	///阵营关系
	UPROPERTY(BlueprintReadOnly, Category = "Level")
		TMap<FString, COMBAT_RELATION> CAMP_RELATION_MAP;

	///快捷栏类型QbType（空快捷项）<服务器的csdfine文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_ITEM_NONE = 0;

	///快捷栏类型QbType（玩家技能快捷项）<服务器的csdfine文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_ITEM_SKILL = 1;

	///快捷栏类型QbType（装备中的道具）<服务器的csdfine文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_ITEM_EQUIP = 2;

	///快捷栏类型QbType（背包中的物品道具快捷项）<服务器的csdfine文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_ITEM_KITBAG = 3;

	///快捷栏类型QbType（幻兽技能快捷项）<服务器的csdfine文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_ITEM_PET_SKILL = 4;

	///快捷栏类型QbType（幻兽头像快捷项）<服务器的csdfine文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_ITEM_PET_HEAD = 5;

	///快捷栏类型QbType（幻兽神通技能快捷项）<服务器的csdfine文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_ITEM_PET_SHENTONG_SKILL = 6;

	///快捷栏类型QbType（玩家神通技能快捷项）<服务器的csdfine文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_ITEM_SHENTONG_SKILL = 7;

	///玩家快捷栏初始索引（0-29）
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_IDX_ROLE_QUICK_SHORTCUT_BAR = 0;

	///玩家自动战斗栏初始索引（30-34）
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_IDX_ROLE_AUTO_BATTLE_BAR = 30;

	///幻兽技能快捷栏初始索引（50-54）
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_IDX_PET_SKILL_BAR = 50;

	///幻兽药品快捷栏初始索引（55-56）
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_IDX_PET_DRUG_BAR = 55;

	///玩家额外快捷栏初始索引（60-74）
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_1 = 60;

	///玩家额外快捷栏初始索引（75-89）
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_2 = 75;
	
	///临时装备背包起始位置<服务器的ItemTypeEnum.py文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 BAG_TEMP_EQUIP_START = 1723;
	///CST-12212 吃鸡装备 武器位置<服务器的ItemTypeEnum.py文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 EQUIP_WEAPON_YCJMD = BAG_TEMP_EQUIP_START + 0;
	///CST-12212 吃鸡装备 帽子位置<服务器的ItemTypeEnum.py文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 EQUIP_HAT_YCJMD = BAG_TEMP_EQUIP_START + 1;
	///CST-12212 吃鸡装备 衣服位置<服务器的ItemTypeEnum.py文件有对应配置>
	UPROPERTY(BlueprintReadOnly, Category = "QuickBarInterface")
		int32 EQUIP_COAT_YCJMD = BAG_TEMP_EQUIP_START + 2;

	///橙名杀气值
	UPROPERTY(BlueprintReadOnly, Category = "Game|Player")
	int32 KV_ORANGE_NAME = 1;

	///红名杀气值
	UPROPERTY(BlueprintReadOnly, Category = "Game|Player")
	int32 KV_RED_NAME = 40;

	///pk保护等级
	UPROPERTY(BlueprintReadOnly, Category = "Game|Player")
	int32 PK_PROTECT_LEVEL = 30;

	///通过神行石传送
	UPROPERTY(BlueprintReadOnly, Category = "Teleport")
		int32 TELEPORT_BY_TELEPORTSTONE = 0;

	///通过消耗金钱传送（预留）
	UPROPERTY(BlueprintReadOnly, Category = "Teleport")
		int32 TELEPORT_BY_MONEY = 1;

	///无条件（指消耗物品或借助神行石）传送
	UPROPERTY(BlueprintReadOnly, Category = "Teleport")
		int32 TELEPORT_BY_NONE = 2;

	///神行石ID
	UPROPERTY(BlueprintReadOnly, Category = "Teleport")
		int32 TELEPORT_STONE_ID = 205010002;

	///关系聊天界面最大保存聊天记录数量
	UPROPERTY(BlueprintReadOnly, Category = "Teleport")
		int32 RELATION_CHAT_LOG_MAX_NUM = 200;

	///关系聊天界面保存聊天记录最久期限（天）
	UPROPERTY(BlueprintReadOnly, Category = "Teleport")
		int32 RELATION_CHAT_LOG_LONGEST_TIME = 7;

	///白色龙珠ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 WHITE_DRAGONBALL_ID = 203010004;

	///五彩龙珠ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 THEFIVECOLOURS_DRAGONBALL_ID = 203010005;

	///超级龙珠ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 SUPER_DRAGONBALL_ID = 203010006;

	///白色玄晶ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 WHITE_EBONY_ID = 203010001;

	///五彩玄晶ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 THEFIVECOLOURS_EBONY_ID = 203010002;

	///超级玄晶ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 SUPER_EBONY_ID = 203010003;

	///白色晶石ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 WHITE_SPAR_ID = 203010007;

	///五彩晶石ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 THEFIVECOLOURS_SPAR_ID = 203010008;

	///超级晶石ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 SUPER_SPAR_ID = 203010009;

	///回火符ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 TEMPERING_SIGN_ID = 203010010;

	///正阳符ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 ZHENGYANG_SIGN_ID = 203010011;

	///北斗符ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 BIGDIPPER_SIGN_ID = 203010012;

	///血符ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 BLOOD_SIGN_ID = 203010013;

	///重铸保护符ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 RECASTINGPROTECTION_SIGN_ID = 203010014;

	///洗练石ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 SOPHISTICATION_STONE_ID = 203010015;

	///重铸宝珠ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 RECAST_BAOZHU_ID = 203010016;

	///魂珠ID
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 SOUL_BEAD_ID = 204020005;

	///漓泉水
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 LIQUAN_WATER_ID = 203010017;

	///砥石
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 WHETSTONE_ID = 203010018;

	///金蚕丝
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 GOLDEN_SILK_ID = 203010019;

	///汞砂
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 MERCURY_SAND_ID = 203010020;

	///祈福香
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 PRAY_INCENSE_ID = 203010021;

	///勇闯绝命岛能量
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 YCJMD_ENERGY_ID = 302010080;
	
	///玲珑玉令
	UPROPERTY(BlueprintReadOnly, Category = "SpecialItem")
		int32 LHMJ_LINGLONGYULING_ID = 303020004;

	///购物车容量
	UPROPERTY(BlueprintReadOnly, Category = "RoleStoreInterface")
		int32 STORE_CART_CAPACIYT = 20;
	
	///帮会等级上限
	UPROPERTY(BlueprintReadOnly, Category = "RoleStoreInterface")
		int32 TONG_LEVEL_MAX = 5;


	///玩家关系规则与关系判断类的对应关系
	TMap<ROLE_RELATION_RULE, FString> ROLE_RELATION_RULE_TO_REL_CLS;

/**
private:
	static UConstData* Instance;*/

};