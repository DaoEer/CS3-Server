#pragma once
#include "CoreMinimal.h"
#include "GameData/Skill/SkillTableData.h"
#include "Skill/SkillBase/Skill.h"
#include "Skill/Effect/EffectSkillBase.h"
#include "EffectLoader.generated.h"

/*
* 文件名称：EffectLoader.h
* 功能说明：效果实例创建文件
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UEffectLoader :public UCS3Object
{
	GENERATED_BODY()
public:
	~UEffectLoader();
	/*获得/创建单例*/
	static UEffectLoader* GetInstance();

	UEffectSkillBase* createEffect(FHIT_EFFECT effectData, USkill* skill);

	UHoldEffect* createHoldEffect(FHOLD_EFFECT effectData, USkill* skill);


private:
	UEffectLoader();

};

