#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "../CsvTableRowBase.h"
#include "Engine/EngineTypes.h"
#include "QuickSkillData.generated.h"

/**
* 文件名称：QuickSkillData.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2020-07-18
*/

//快捷栏技能类型
UENUM(BlueprintType)
enum class QUICK_SKILL_TYPE : uint8
{
	///普通技能
	QUICK_SKILL_TYPE_NORMAL = 0,
	///等级切换
	QUICK_SKILL_TYPE_LEVEL = 1,
	///连携切换
	QUICK_SKILL_TYPE_STAGE = 2,
};

/**
 * 快捷栏Item结构体
 */
USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FQB_ITEM
{
	GENERATED_USTRUCT_BODY()
	//快捷栏索引
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		int32 SlotIndex;
	//容器ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		int32 QuickID;
	//类型：0（普通技能），1（等级切换），2（连携切换）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		QUICK_SKILL_TYPE QuickType;
	//快捷栏类型（ConstDataBP.h有定义）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		int32 QbType;
	//快捷栏技能ID或物品ID（原ID）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		int32 QbID;
	//快捷栏的幻兽UID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		FString PetUid;
	//快捷栏物品绑定类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		int32 BindType;
	//连携剩余持续时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		int32 RemainHoldTime;
	//连携技能持续总时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		int32 TotalHoldTime;
	//当前分段编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		int32 CurrStage;
	//当前技能ID（普通技能ID或物品ID、进阶后的技能ID、连携当前分段技能ID）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "QB_ITEM")
		int32 CurrQbID;

	FORCEINLINE bool operator==(const FQB_ITEM& other) const
	{
		if (other.SlotIndex == this->SlotIndex)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};

/*快捷栏容器 切换技能参数
*Type = 1（等级切换）：Param1（主动技能等级）、Param2（被动技能等级）、SkillID（切换主动技能ID）
*Type = 2（连携切换）：Param1（分段持续时间）、Param2（无）、SkillID（分段技能ID）
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FQUICKSKIL_SWITCH_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///切换参数1
	///Type = 1（等级切换）：Param1（主动技能等级）
	///Type = 2（连携切换）：Param1（分段持续时间）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig")
		FString Param1;
	///切换参数2
	///Type = 1（等级切换）：Param2（被动技能等级）
	///Type = 2（连携切换）：Param2（无）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig")
		FString Param2;
	///切换后的技能ID
	///Type = 1（等级切换）：SkillID（切换主动技能ID）
	///Type = 2（连携切换）：SkillID（分段技能ID）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig")
		FString SkillID;
};

//快捷栏容器 配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FQUICKSKILL_CONFIG : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///容器ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig")
		int32 QuickID;
	///类型：0（普通技能），1（等级切换），2（连携切换）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig")
		int32 Type = 0;
	///切换技能参数
	///Type = 1（等级切换）：Param1（主动技能等级）、Param2（被动技能等级）、SkillID（切换主动技能ID）
	///Type = 2（连携切换）：Param1（分段持续时间）、Param2（无）、SkillID（分段技能ID）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig")
		TArray<FQUICKSKIL_SWITCH_DATA> QuickSkillData;
	///备注
	///	没有任何功能，仅供策划记录及查看
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig", DisplayName = "备注")
		FString Remarks;
};

//快捷栏技能连携状态
USTRUCT(BlueprintType)
struct CHUANGSHI_API FQUICKSKIL_STATE_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///容器ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig")
		int32 QuickID;
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig")
		FString SkillID;
	///分段编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig")
		int32 Stage;
	///持续时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickSkillConfig")
		float HoldTime;
};

//被动技能持有进阶效果
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_PASSIVE_HOLD_EFFECT_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///容器ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PassiveSkillHoldEffect")
		int32 QuickID;
	///被动技能进阶等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PassiveSkillHoldEffect")
		int32 PassiveSkillLevel;
	///主动技能进阶等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PassiveSkillHoldEffect")
		int32 SkillLevel;
};