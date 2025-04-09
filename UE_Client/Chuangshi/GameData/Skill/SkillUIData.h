#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "SkillUIData.generated.h"

/**
* 文件名称：SkillUIData.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-07-07
*/


//界面使用的技能学习数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILLLEARN_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString ID;
	///技能名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString UName;
	///技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 Level = 0;
	///需求等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 ReqLevel = 0;
	///需求潜能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 ReqPotential = 0;
	///上一等级技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 ReqSkill = 0;
	///下一等级技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 NextLevelID = 0;
	///技能类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString SkillType;
	///技能类型：0（通用技能），1（心法技能）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 SkillClass = 0;
	///需求金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 Money = 0;	
	///材料1 id
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 material_1;
	///材料1 amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 mNum_1;
	///材料2 id
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 material_2;
	///材料2 amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 mNum_2;
	///材料3 id
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 material_3;
	///材料3 amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 mNum_3;
	///预留
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString Param1;
	///预留
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString Param2;
	///预留
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString Param3;
};

//界面使用的技能树数据 配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILLTREE_INFO : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString skillID;
	///技能名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString skillName;
	///职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		TArray<int> Class;
	///显示类型（UI显示用）：0（基础），1（天怒/幻剑/九幽/寒霜 心法），2（神威/天剑/雷鸣/神逸 心法），3（轻功）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 type = 0;
	///行，从1开始（一定要配，且同type的技能配置rowIndex和colIndex不能完全一致，不然会崩）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 rowIndex = 0;
	///列，从1开始（一定要配，且同type的技能配置rowIndex和colIndex不能完全一致，不然会崩）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 colIndex = 0;
	///最大技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 maxSkillLevel = 0;
	///是否能拖拽到技能栏，0不能，1能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 bCanDrag = 0;
	///是否能拖拽到自动战斗栏，0不能，1能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 CanDragToAuto = 0;
	///容器ID（链接 FQUICKSKILL_CONFIG）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 QuickID;
};


//界面使用的技能树数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILLTREEUI_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString skillID;
	///显示类型：0（基础），1（天怒 / 幻剑 / 九幽 / 寒霜 心法），2（神威 / 天剑 / 雷鸣 / 神逸 心法），3（轻功）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 Type = 0;
	///行，从1开始
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 RowIndex = 0;
	///列，从1开始
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 ColIndex = 0;
	///技能ICON
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		UTexture2D* icon = 0;
	///技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 SkillLevel = 0;
	///最大技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 MaxSkillLevel = 0;
	///容器ID（链接 FQUICKSKILL_CONFIG）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 QuickID;
};

//界面使用的被动技能表数据结构
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_PASSIVE_TREE_CONFIG : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeConfig")
		FString skillID;
	///技能名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeConfig")
		FString skillName;
	///职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeConfig")
		TArray<int> Class;
	///最大技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeConfig")
		int32 MaxSkillLevel = 0;
	///1道纹，2法印
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeConfig")
		int32 PassiveSkillType = 1;
	///位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeConfig")
		int32 Index = 0;
};

//界面使用的被动技能数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_PASSIVE_TREE_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeData")
		FString skillID;
	///技能ICON
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeData")
		UTexture2D* icon = 0;
	///技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeData")
		int32 SkillLevel = 0;
	///最大技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeData")
		int32 MaxSkillLevel = 0;
	///1道纹，2法印
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeData")
		int32 PassiveSkillType = 1;
	///位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillPassiveTreeData")
		int32 Index = 0;
};

//行为技能数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FACTIONSKILL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString skillID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString actionName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		UTexture2D* icon;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString description;
};


//技能导师数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILLTEACHER_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 npcId = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString npcName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 skillID = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString skillName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 Class = 0;
};

//被动技能栏配置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPASSIVESKILLBAR_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 id = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		uint8 isLock;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 level;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 money;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 xianshi;
	///材料1 id
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 material_1;
	///材料1 amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 mNum_1;
	///材料2 id
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 material_2;
	///材料2 amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 mNum_2;
	///材料3 id
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 material_3;
	///材料3 amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 mNum_3;
};

//界面使用的被动技能学习数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_PASSIVE_LEARN_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString ID;
	///技能名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString UName;
	///技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 Level = 0;
	///技能学习所需等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 ReqLevel = 0;
	///技能学习所需潜能值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 ReqPotential = 0;
	///学习该技能的前置所需技能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 ReqSkill = 0;
	///学习该技能所需金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 Money = 0;
	///技能书
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString SkillBook;
	///材料1，ItemID|Amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString Material_1;
	///材料2，ItemID|Amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString Material_2;
	///材料3，ItemID|Amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString Material_3;
	///该技能下一级的id
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 NextLevelID = 0;
	///激活持有效果
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 ActHoldEffectID = 0;
	///激活效果
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 ActEffectID = 0;
	///休眠效果
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		int32 SleepEffectID = 0;
	///预留
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString Param1;
	///预留
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString Param2;
	///预留
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillUIData")
		FString Param3;
};

//界面使用的神通技能数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_SHEN_TONG_TREE_CONFIG : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillShenTongTreeConfig")
		FString SkillID;
	///位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillShenTongTreeConfig")
		int32 Index = 0;
	///技能来源
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillShenTongTreeConfig")
		FString Access;
	///容器ID（链接 FQUICKSKILL_CONFIG）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillShenTongTreeConfig")
		int32 QuickID;
};

//界面使用传承技能学习表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_CHUANCHENG_LEARN_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		FString ID;
	///技能名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		FString UName;
	///技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		int32 Level = 0;
	///技能学习所需等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		int32 ReqLevel = 0;
	///技能学习所需潜能值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		int32 ReqPotential = 0;
	///学习该技能的前置所需技能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		int32 ReqSkill = 0;
	///学习该技能所需金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		int32 Money = 0;
	///该技能下一级的id
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		int32 NextLevelID = 0;
};

//界面使用的传承技能树
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_CHUANCHENG_TREE_CONFIG : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		int32 skillID;
	///技能名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		FString skillName;
	///职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		TArray<int> Class;
	///最大技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		int32 MaxSkillLevel = 0;
	///位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		int32 Index = 0;
	///获取途径
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ChuanChengSkillUIData")
		FString Access;
};

//界面使用的幻兽技能学习数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPET_SKILL_PASSIVE_LEARN_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PetSkillLearnConfig")
		FString ID;
	///技能类型 1:主动技能 2：被动技能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PetSkillLearnConfig")
		int32 SkillType = 1;
	///技能名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PetSkillLearnConfig")
		FString UName;
	///技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PetSkillLearnConfig")
		int32 Level = 0;
	///技能学习所需等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PetSkillLearnConfig")
		int32 ReqLevel = 0;
	///技能学习所需潜能值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PetSkillLearnConfig")
		int32 ReqPotential = 0;
	///学习该技能的前置所需技能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PetSkillLearnConfig")
		int32 ReqSkill = 0;
	///学习该技能所需金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PetSkillLearnConfig")
		int32 Money = 0;
	///技能书
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PetSkillLearnConfig")
		FString SkillBook;
	///下一级技能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PetSkillLearnConfig")
		int32 NextLevelID = 0;
};