#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "AutomaticFightData.generated.h"

/**
* 文件名称：AutomaticFightData.h
* 功能说明：自动战斗数据
* 文件作者：YangHan
* 目前维护：wuxiaoou
* 创建时间：2017-09-14
*/

///打断自动战斗的种类
UENUM(BlueprintType)
enum class EBreakAutomaticType : uint8
{
	///默认打断
	NoneBreakType = 0 UMETA(DisplayName = "NoneBreakType"),
	///移动打断
	MoveBreakType = 1 UMETA(DisplayName = "MoveBreakType"),
	///死亡打断
	DeathBreakType = 2 UMETA(DisplayName = "DeathBreakType"),
	///替换技能栏打断
	StateBreakType = 3 UMETA(DisplayName = "StateBreakType"),

};

///能够使用的种类
UENUM(BlueprintType)
enum class EAutomaticPickupType : uint8
{
	///神阶绿色
	GreenShenType = 0 UMETA(DisplayName = "GreenShenType"),
	///圣阶绿色
	GreenShengType = 1 UMETA(DisplayName = "GreenShengType"),
	///天阶绿色
	GreenTianType = 2 UMETA(DisplayName = "GreenTianType"),
	///地阶绿色
	GreenType = 3 UMETA(DisplayName = "GreenType"),
	///粉色
	PinkType = 4 UMETA(DisplayName = "PinkType"),
	///金色
	GoldType = 5 UMETA(DisplayName = "GoldType"),
	///蓝色
	BlueType = 6 UMETA(DisplayName = "BlueType"),
	///白色
	WhiteType = 7 UMETA(DisplayName = "WhiteType"),
	///材料
	MaterialType = 8 UMETA(DisplayName = "MaterialType"),
	///晶核
	SparType = 9 UMETA(DisplayName = "SparType"),
	///符咒
	SpellType = 10 UMETA(DisplayName = "SpellType"),
	///卷轴
	ReelType = 11 UMETA(DisplayName = "ReelType"),
	///药品
	DrugType = 12 UMETA(DisplayName = "DrugType"),
	///任务
	QuestType = 13 UMETA(DisplayName = "QuestType"),
	///杂物
	DebrisType = 14 UMETA(DisplayName = "DebrisType"),
};

struct FAutoFightData
{
	EBreakAutomaticType BreakType = EBreakAutomaticType::NoneBreakType;
	FName LevelName = "";
	FString IdString = "";
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FAutomaticPickupData
{
	GENERATED_USTRUCT_BODY()

public:
	///拾取类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PickupType")
		EAutomaticPickupType PickupType = EAutomaticPickupType::BlueType;
	///是否自动拾取
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsAuto")
		bool IsAuto = true;
	///拾取名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PickupTypeName")
		FString PickupTypeName = "";
};

///@struct FAUTOFIGHTTTING_DATA 自动战斗设置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FAUTOFIGHTTTING_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///角色是否能自动加血
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AutoFightSettingData")
		bool IsAutoRoleAddHP;
	///角色需要加血的最低血量百分比
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AutoFightSettingData")
		float RoleAddHPPercentage;
	///角色是否能自动加蓝
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AutoFightSettingData")
		bool IsAutoRoleAddMP;
	///角色需要加蓝的最低蓝量百分比
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AutoFightSettingData")
		float RoleAddMPPercentage;
	///选择范围
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AutoFightSettingData")
		float FightRange;
	///是否能自动组队
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AutoFightSettingData")
		bool IsAutoJoinTeam;
	///是否能自动复活
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AutoFightSettingData")
		bool IsAutoRevive;
	///自动拾取的类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AutoFightSettingData")
		TArray<FAutomaticPickupData> AutoPickupData;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnChangeAutoFightData, FAUTOFIGHTTTING_DATA, Data);