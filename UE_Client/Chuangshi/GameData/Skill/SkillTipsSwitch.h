#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "SkillTipsSwitch.generated.h"

/**
* 文件名称：SkillTipsSwitch.h
* 功能说明：技能详细tips开关
* 文件作者：zhuangzhenguo
* 目前维护：zhuangzhenguo
* 创建时间：2019-09-11
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSkill_Tips_Switch : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:

	///是否开启详细tips显示
	///	0：不显示提示
	///	1：显示提示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Skill_Tips_Switch", DisplayName = "IsShowTips")
		int32  UIsShowTips = 0;
	///是否是门派技能
	///	0：不是门派技能
	///	1：是门派技能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "Skill_Tips_Switch", DisplayName = "IsGuildSkill")
		int32  UIsGuildSkill = 0;
};