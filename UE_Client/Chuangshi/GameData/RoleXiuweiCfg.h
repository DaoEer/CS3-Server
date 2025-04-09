#pragma once

#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "RoleXiuweiCfg.generated.h"

/**
* 文件名称：RoleXiuweiCfg.h
* 功能说明：修为配置表

* 文件作者：zhangdan
* 目录维护：zhangdan
* 创建时间：2017-06-08
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRoleXiuweiCfg : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//修为等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 XiuweiLevel = 0;
	//对应玩家等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 PlayerLevel = 0;
	//修为值
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Xiuwei = 0;
	//外功
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Damage = 0;
	//内功
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MagicDamage = 0;
	//外功防御
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Armor = 0;
	//内功防御
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MagicArmor = 0;
	//增加血量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 HP = 0;
	//法力值
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MP = 0;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRoleXiuweiUICfg : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//仙道修为境界UI
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> ImageTaoism;
	//魔道修为境界UI
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> ImageDemon;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		bool bHasError = false;

		if (ImageTaoism.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(ImageTaoism.ToString()))
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ImageTaoism\" resource does not exist"));
			}
		}
		else
		{
			bHasError = true;
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ImageTaoism\" config is None"));
		}
		if (ImageDemon.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(ImageDemon.ToString()))
			{
				ResultInfo.Result = Error;
				if (bHasError)
				{
					ResultInfo.CheckLog += FString::Printf(TEXT("; \"ImageDemon\" resource does not exist"));
				}
				else
				{
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ImageDemon\" resource does not exist"));
				}
			}
		}
		else
		{
			ResultInfo.Result = Error;
			if (bHasError)
			{
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"ImageDemon\" resource does not exist"));
			}
			else
			{
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ImageDemon\" config is None"));
			}
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRoleXiuweiIconAndBtnCfg : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//仙道修为境界
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString StageTaoism;
	//仙道Icon
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> TaoismIcon;
	//仙道按钮Normal状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> TaoismNormal;
	//仙道按钮Hovered状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> TaoismHovered;
	//仙道按钮Pressed状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> TaoismPressed;
	//仙道按钮Disabled状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> TaoismDisabled;
	//仙道按钮Selected状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> TaoismSelected;
	//魔道修为境界
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString StageDemon;
	//魔道Icon
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> DemonIcon;
	//魔道按钮Normal状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> DemonNormal;
	//魔道按钮Hovered状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> DemonHovered;
	//魔道按钮Pressed状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> DemonPressed;
	//魔道按钮Disabled状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> DemonDisabled;
	//魔道按钮Selected状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> DemonSelected;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRoleJingjieCfg : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//境界等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 jingjieLevel = 0;
	//修为等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 xiuweiLevel = 0;
	//境界层次名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Stage_layers;
	//仙道境界阶段
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString stage_taoism;
	//魔道境界阶段
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString stage_demon;
};