#pragma once

#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "ShenTongSkill.generated.h"

/**
* 文件名称：ShenTongSkill.h
* 功能说明：神通技能
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2019-03-22
*/

/*神通精研配置表*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FShenTongSkillComminution : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SkillID")
		int32 SkillID;
	///下一级技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NextSKillID")
		int32 NextSKillID;
	///升级所需经验
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NeedExp")
		int32 NeedExp;
	///升级所需潜能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NeedPotential")
		int32 NeedPotential;
	///升级所需金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NeedMoney")
		int32 NeedMoney;
};