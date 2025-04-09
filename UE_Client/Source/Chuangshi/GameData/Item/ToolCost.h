#pragma once
#include "GameData/CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "ToolCost.generated.h"

/**
* 文件名称：ToolCost.h
* 功能说明：轮回秘境打造消耗
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-02-27
*/


/************************************************************************/
/*工具打造消耗		                                                    */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FToolComposeCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<工具ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 equipID;
	///<标签名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString labelName;
	///<需要工坊等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 needLevel;
	///<金钱消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 money;
	///<灵能消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 psionic;
	///<打造时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float useTime;
	///<材料{itemID:num}
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<int32, int32> material;
};

/************************************************************************/
/* 绿装打造消耗		                                                    */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FGreenEquipComposeCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<工具ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 equipID;
	///<标签名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString labelName;
	///<半成品装备ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 partEquipID;
	///<需要工坊等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 needLevel;
	///<金钱消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 money;
	///<打造时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float useTime;
	///<图纸ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 bluePrint;
	///<主材料{元素索引:itemID} （0：无，1：冰，2：火，3：玄， 4 ：雷。不同的元素，消耗不同的主材。元素由图纸决定）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<int32, int32> mainMaterial;
	///<主材消耗数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 mainMaterialNum;
	///<材料{itemID:num}
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<int32, int32> material;
};

/************************************************************************/
/*乾坤鼎打造消耗		                                                    */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTripodComposeCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<工具ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 equipID;
	///<标签名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString labelName;
	///<需要乾坤鼎等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 needLevel;
	///<金钱消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 money;
	///<灵能消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 psionic;
	///<打造时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float useTime;
	///<材料{itemID:num}
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<int32, int32> material;
};

/************************************************************************/
/* 打造消耗倍率配置表		                                            */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FForgeConsumeCfg : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<建筑等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level;
	///<仙府打造工具成功率
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 successRate;
	///<仙府打造绿装累加成功率
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 xf_SumSuccessRate;
	///<洞府打造绿装累加成功率
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 df_SumSuccessRate;
	///<高级洞府打造成功率
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 gjdf_SumSuccessRate;
	///<仙府消耗倍率
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 publicConsumeRate;
	///<高级洞府消耗倍率
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 highConsumeRate;
};

/************************************************************************/
/*熔炼消耗																*/
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMeltingEquipCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<图纸打造装备等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level;
	///<图纸打造装备等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 quality;
	///<熔炼装备等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 meltingLevel;
	///<熔炼装备品质
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 meltingQuality;
	///<增加成功率
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float successRate;
};

/************************************************************************/
/*打造列表类型	                                                    */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FWorkShopComposeCategory : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<打造类型（1工具，2绿装，3乾坤鼎）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ComposeType;
	///<名称（如弓、伐木斧等）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> CategoryNames;
};

/************************************************************************/
/* 套装前缀名称																*/
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSuitNameCfg : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<元素属性
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 suitIndex;
	///<元素名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString suitTitle;
	///<装备等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level;
	///<装备职业（可配置多个职业）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> professions;
	///<套装名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString suitName;
};

/// 轮回秘境占有地图类型
UENUM(BlueprintType)
enum class LHMJ_SPACE_TYPE :uint8
{
	// 无占有
	LHMJ_SPACE_TYPE_NONE,
	// 洞府（私有）
	LHMJ_SPACE_TYPE_PRIVATE,
	// 仙府（公有）
	LHMJ_SPACE_TYPE_PUBLIC,
	// 高级洞府
	LHMJ_SPACE_TYPE_HIGH_DF,

};

/// 轮回秘境建筑类型
UENUM(BlueprintType)
enum class LHMJ_BUILD_TYPE :uint8
{
	// 灵泉
	LHMJ_BUIILD_LING_QUAN = 1,
	// 工坊
	LHMJ_BUIILD_GONG_FANG = 2,
	// 乾坤鼎
	LHMJ_BUIILD_QIAN_KU_DING = 3,
	// 兽栏
	LHMJ_BUIILD_SHOU_LAN = 4,
	// 灵田
	LHMJ_BUIILD_LING_TIAN = 5,
};

/// 轮回秘境 洞府挑战状态
UENUM(BlueprintType)
enum class LHMJ_CHANLLENGE_TYPE :uint8
{
	// 无（还没到挑战时间）
	CHANLLENGE_TYPE_NONE,
	// 可挑战状态
	CHANLLENGE_TYPE_COMMON,
	// 已接受挑战
	CHANLLENGE_TYPE_ACCEPT,
	// 不可挑战
	CHANLLENGE_TYPE_CANNOT,
	// 修复中
	CHANLLENGE_TYPE_REPAIR,
};

// 洞府数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FDongFuData
{
	GENERATED_BODY()
public:
	///< 洞府类型（1：为洞府，3为高级洞府）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 dongFuType;
	///< 洞府标识（索引）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 group;
	///< 洞府开启的阵图物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 batteleID;
	///< 洞府等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level;
	///< 占领洞府的玩家名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString playerName;
	///< 洞府挑战状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		LHMJ_CHANLLENGE_TYPE challengeState;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FDongFuData_Map
{
	GENERATED_BODY()
public:
	///< 洞府数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FDongFuData> DongFuDatas;

	const int32 GetDongFuLevel(const int32& group)
	{
		for (auto data : DongFuDatas)
		{
			if (data.group == group)
			{
				return data.level;
			}
		}
		return 0;
	};

};