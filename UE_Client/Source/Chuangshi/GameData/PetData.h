#pragma once
#include "CoreMinimal.h"
#include <functional>
#include "CsvTableRowBase.h"
#include "CharacterData.h"
#include "BehaviorTree/BehaviorTree.h"
#include "PetData.generated.h"

/**
* 文件名称：PetData.h
* 功能说明：人物数据对象相关
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2016-09-02
*/

/// 种族枚举
UENUM(BlueprintType)
enum class PET_PROFESSION_ENUM : uint8
{
	//狼族
	PET_PROFESSION_LANG = 1 UMETA(DisplayName = "PetProfessionLang"),
	//虎族
	PET_PROFESSION_LAO_HU = 2 UMETA(DisplayName = "PetProfessionLaoHu"),
	//禽族
	PET_PROFESSION_QIN = 3 UMETA(DisplayName = "PetProfessionQin"),
	//狐族
	PET_PROFESSION_HU_LI = 4 UMETA(DisplayName = "PetProfessionHuLi"),
	PET_PROFESSION_NULL = 5 UMETA(DisplayName = ""),
};

/** 幻兽结构体对象 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPET_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///默认名字
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FPET_DATA", DisplayName = "Uname")
		FString Uname;
	///种族
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FPET_DATA", DisplayName = "profession")
		PET_PROFESSION_ENUM profession;
	///骑乘姿态
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FPET_DATA", DisplayName = "RidePosture")
		RIDE_POSTURE_ENUM RidePosture;
	///族类
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "race")
		int32 race;
	///携带等级
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "takeLevel")
		int32 takeLevel;
	///类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "combatType")
		int32 combatType;
	///幻兽模型id
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "ModelNumber")
		FString ModelNumber;
	///幻兽模型大小倍率
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "ModelScale")
		float ModelScale;
	///幻兽头像
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "icon")
		FString icon;
	///原兽模型id
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "OriginModelNumber")
		FString OriginModelNumber;
	///原兽模型大小倍率
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "OriginModelScale")
		float OriginModelScale;
	///食材类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "foodType")
		int32 foodType;
	///骑宠的模型ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "vehicleModelNum")
		FString vehicleModelNum;
	///载具ID[关联配置DT_CarrierCfg首行字段]
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "CarrierId")
		FString CarrierId;
	///凡兽主动技能
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FPET_DATA", DisplayName = "Skills_1")
		FString Skills_1;
	///灵兽主动技能
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FPET_DATA", DisplayName = "Skills_2")
		FString Skills_2;
	///仙兽主动技能
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FPET_DATA", DisplayName = "Skills_3")
		FString Skills_3;
	///圣兽主动技能
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FPET_DATA", DisplayName = "Skills_3")
		FString Skills_4;
	///神兽主动技能
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FPET_DATA", DisplayName = "Skills_4")
		FString Skills_5;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool UnameResult = !Uname.TrimStartAndEnd().IsEmpty();
		bool professionResult = profession >= (PET_PROFESSION_ENUM)1 && profession <= (PET_PROFESSION_ENUM)5;
		bool RidePostureResult = RidePosture >= (RIDE_POSTURE_ENUM)0 && RidePosture <= (RIDE_POSTURE_ENUM)4;
		bool raceResult = race > 0;
		bool takeLevelResult = takeLevel >= 1;
		bool iconResult = !icon.TrimStartAndEnd().IsEmpty();
		bool vehicleModelNumResult = !vehicleModelNum.TrimStartAndEnd().IsEmpty();
		if (!UnameResult) ResultInfo.CheckLog += FString::Printf(TEXT("Uname cannot be empty!  "));
		if (!professionResult) ResultInfo.CheckLog += FString::Printf(TEXT("profession is config error!  "));
		if (!RidePostureResult) ResultInfo.CheckLog += FString::Printf(TEXT("RidePosture is config error!  "));
		if (!raceResult) ResultInfo.CheckLog += FString::Printf(TEXT("race: \"%d\" is config error!  "), race);
		if (!takeLevelResult) ResultInfo.CheckLog += FString::Printf(TEXT("takeLevel:  \"%d\" is config error!  "), takeLevel);
		if (!iconResult) ResultInfo.CheckLog += FString::Printf(TEXT("icon cannot be empty!  "));
		if (!vehicleModelNumResult) ResultInfo.CheckLog += FString::Printf(TEXT("vehicleModelNum cannot be empty!  "));
		bool Skills_1Result = checkSkills(ResultInfo, FString("Skills_1"), Skills_1);
		bool Skills_2Result = checkSkills(ResultInfo, FString("Skills_2"), Skills_2);
		bool Skills_3Result = checkSkills(ResultInfo, FString("Skills_3"), Skills_3);
		bool Skills_4Result = checkSkills(ResultInfo, FString("Skills_4"), Skills_4);
		bool Skills_5Result = checkSkills(ResultInfo, FString("Skills_5"), Skills_5);
		if (UnameResult && professionResult && RidePostureResult && raceResult && takeLevelResult && iconResult && vehicleModelNumResult && Skills_1Result && Skills_2Result && Skills_3Result && Skills_4Result && Skills_5Result)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
	bool checkSkills(RowCheckResultInfo& ResultInfo, FString SkillsName, FString Skills)
	{
		if (Skills.TrimStartAndEnd().IsEmpty())
		{
			ResultInfo.CheckLog += FString::Printf(TEXT("%s cannot be empty!  "), *SkillsName);
			return false;
		}
		else
		{
			for (auto datas : SplitString(Skills, false, TEXT("|")))
			{
				for (auto data : SplitString(datas, false, TEXT(":")))
				{
					if (!data.TrimStartAndEnd().IsNumeric())
					{
						ResultInfo.CheckLog += FString::Printf(TEXT("%s: \"%s\" is config error!  "), *SkillsName, *Skills);
						return false;
					}
				}
			}
		}
		return true;
	};
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FPET_POTENTIAL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///幻兽阶次
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPET_POTENTIAL_DATA", DisplayName = "Step")
		int32 Step = 0;
	///幻兽品质
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPET_POTENTIAL_DATA", DisplayName = "Pet_Quality")
		int32 Pet_Quality = 0;
	///移动速度加成比
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PET_POTENTIAL_DATA", DisplayName = "SpeedPercent")
		int32 SpeedPercent = 0;
	///原兽升阶消耗经验
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPET_POTENTIAL_DATA", DisplayName = "NeedExp")
		int32 NeedExp = 0;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		if (Step > 0 && Pet_Quality > 0)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			if (!(Step > 0)) ResultInfo.CheckLog += FString::Printf(TEXT("Step value must be greater than 0!  "));
			if (!(Pet_Quality > 0)) ResultInfo.CheckLog += FString::Printf(TEXT("Pet_Quality value must be greater than 0!  "));
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	};
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FPET_CORRLEVEL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///幻兽阶次
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPET_CORRLEVEL_DATA", DisplayName = "Step")
		int32 Step = 0;
	///幻兽品质
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPET_CORRLEVEL_DATA", DisplayName = "CorrLevel")
		int32 CorrLevel = 0;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		if (Step > 0 && CorrLevel > 0)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			if (!(Step > 0)) ResultInfo.CheckLog += FString::Printf(TEXT("Step value must be greater than 0!  "));
			if (!(CorrLevel > 0)) ResultInfo.CheckLog += FString::Printf(TEXT("CorrLevel value must be greater than 0!  "));
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	};
};

// 幻兽驯养消耗
USTRUCT(BlueprintType)
struct CHUANGSHI_API FFEED_PET_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///食材数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 FoodNum;
	///幻兽品质
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 quality;
	///金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 money;
	///潜能
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 potential;

};

/** 幻兽3D模型配置 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPET_MODEL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///幻兽名字（供策划备注，无具体功能）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FPET_MODEL_DATA", DisplayName = "UName")
		FString UName = TEXT("");
	///摄像机变形（可以调整摄像机的位置、旋转；调整摄像机的大小不影响表现）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPET_MODEL_DATA", DisplayName = "Transform")
		FTransform Transform;
	///摄像机FOV（可以调整摄像机的视场角，角度越大形变越大，可以用以调整近景人像表现）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPET_MODEL_DATA", DisplayName = "FOVAngle")
		float FOVAngle = 0.0f;
};

/** 幻兽 神通AI 表现 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPET_ST_AI_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///幻兽AI树
	///①BT_PetSTCommon（幻兽神通技能“魔狼啸月”用，替换技能列表的表现）
	///	技能列表：替换AI状态下，使用此技能列表，替代单位原本的技能列表
	///	参数1~4：无
	///②BT_PetSTWithOutSkillAssist（幻兽神通技能“天香国色”用，变身表现）
	///	技能列表：替换AI状态下，使用此技能列表，替代单位原本的技能列表
	///	参数1：搜索目标时，排除拥有此BuffID的单位（@DT_BuffCfg）
	///	参数2：圆形搜索范围距离上限（厘米）
	///	参数3~4：无
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SHENGTONG_AI_DATA", DisplayName = "AI Tree")
		TSoftObjectPtr<UBehaviorTree> PetAITree;
	///技能列表，供AI行为树使用（@DT_SkillCfg）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SHENGTONG_AI_DATA", DisplayName = "SkillArr")
		TArray<int32> SkillArr;
	///通用扩展参数1（整型）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SHENGTONG_AI_DATA", DisplayName = "Param1")
		int32 Param1;
	///通用扩展参数2（整型）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SHENGTONG_AI_DATA", DisplayName = "Param2")
		int32 Param2;
	///通用扩展参数3（文本）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SHENGTONG_AI_DATA", DisplayName = "Param3")
		FString Param3;
	///通用扩展参数4（文本）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SHENGTONG_AI_DATA", DisplayName = "Param4")
		FString Param4;
	///备注
	///	没有任何功能，仅供策划记录及查看
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SHENGTONG_AI_DATA", DisplayName = "备注")
		FString temp;
};