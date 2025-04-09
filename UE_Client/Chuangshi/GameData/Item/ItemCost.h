#pragma once
#include "GameData/CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "ItemCost.generated.h"

/**
* 文件名称：ItemCost.h
* 功能说明：装备相关消耗
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018-05-31
*/

/************************************************************************/
/*装备洗练消耗		                                                    */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FShuffleCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<等级区间（级）
	///	如：“20-29”代表“等级大于等于20，并小于等于29”
	UPROPERTY(BlueprintReadOnly)
		FString MinMaxLv;
	///<锁定属性数量
	UPROPERTY(BlueprintReadOnly)
		int32 LockProNum = 0;
	///<血符数量
	UPROPERTY(BlueprintReadOnly)
		int32 BloodFu = 0;
	///<洗练石数量
	UPROPERTY(BlueprintReadOnly)
		int32 WashStone = 0;
	///<消耗金钱数量（铜）
	UPROPERTY(BlueprintReadOnly)
		int32 MoneyCost = 0;
	///<元宝消耗（替代洗练石）
	UPROPERTY(BlueprintReadOnly)
		int32 YBReplaceStone = 0;
	///<元宝消耗（替代血符）
	UPROPERTY(BlueprintReadOnly)
		int32 YBReplaceFu = 0;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		FString Left;
		FString Right;
		MinMaxLv.Split(TEXT("-"), &Left, &Right);
		if (FSTRING_TO_INT(Left) == 0 || FSTRING_TO_INT(Right) == 0)
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"MinMaxLv\" config error"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};


/************************************************************************/
/*装备重铸消耗		                                                    */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FRecastCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<等级区间（级）
	///	如：“20-29”代表“等级大于等于20，并小于等于29”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString MinMaxLv;
	///<保护属性数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ProtectProNum = 0;
	///<重铸保护符数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 RecastFu = 0;
	///<重铸宝珠数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 RecastStone = 0;
	///<消耗金钱数量（铜）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MoneyCost = 0;
	///<元宝消耗（替代重铸宝珠）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 YBReplaceStone = 0;
	///<元宝消耗（替代重铸保护符）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 YBReplaceFu = 0;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		FString Left;
		FString Right;
		MinMaxLv.Split(TEXT("-"), &Left, &Right);
		if (FSTRING_TO_INT(Left) == 0 || FSTRING_TO_INT(Right) == 0)
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"MinMaxLv\" config error"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/************************************************************************/
/*装备打造消耗		                                                    */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FEquipComposeCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<金钱消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 money;
	///<白装equipID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 srcEquip;
	///<材料1 id
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 material_1;
	///<材料1 amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 mNum_1;
	///<材料2 id
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 material_2;
	///<材料2 amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 mNum_2;
	///<材料3 id
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 material_3;
	///<材料3 amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 mNum_3;
	///<材料4 id
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 material_4;
	///<材料4 amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 mNum_4;
};

/************************************************************************/
/* 王道神兵 条件	                                                    */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FKingCraftEquipCondition : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///装备等级区间筛选条件（@CST-12533）
	///	如：“20-29”，代表“要求装备的物品等级，≥20且≤29”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString MinMaxLv;
	///装备职业要求筛选条件（@CST-12533）
	///	1：战士（即要求装备的职业需求，是"1"）
	///	2：剑客
	///	3：链刃
	///	4：法师
	///	0：全部（即要求装备的职业需求，是"1|2|3|4"）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Class = 0;
	///装备部位筛选条件（@CST-12533）
	///		20：帽子（@ItemTypeEnum.EQUIP_HAT）
	///		21：上衣，衣服
	///		22：护腕
	///		23：手套
	///		24：腰带
	///		25：裤子
	///		26：鞋子
	///		27：项链
	///		28：左手戒指
	///		31：双手武器
	///		32：左手武器
	///		33：右手武器
	///注意：
	///	①此处不是装备配置的“物品类型”，而是装备部位定义的枚举
	///	②建议后续改为“物品类型”，无需策划区分哪种武器、哪边的戒指等
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ModelPart = 0;
	///蜕化条件：强化金星数量要求（@CST-12533）
	///	如：“5”，代表“要求5颗金星”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 NeedStar = 0;
	///蜕化条件：附加属性类型要求列表1（@CST-12533）
	///	如：“30001|30002|30003|30004|30005”，代表“根骨、筋力、内力、洞察、身法”
	///注意：
	///	①两个类型列表，满足其中任何一个都可以
	///	②若只填两个，代表“只要求有两个属性”；若填六个，代表“只有五条属性肯定满足不了”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> NeedPropertys1;
	///蜕化条件：附加属性类型要求列表2（@CST-12533）
	///	同上
	///注意：
	///	①两个类型列表，满足其中任何一个都可以
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> NeedPropertys2;
	///蜕化条件：附加属性类型数值要求（@CST-12533）
	///	如：“80”，代表“要求每条附加属性的数值都达到该属性的上限的，80%”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 UpperPercent = 0;
};