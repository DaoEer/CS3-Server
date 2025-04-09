#pragma once
#include "EffectSkillBase.h"
#include "EffectCreateEntity.generated.h"

/*
* 文件名称：EffectCreateEntity.h
* 功能说明：目标位置创建entity
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UEffectCreateEntity : public UEffectSkillBase
{
	GENERATED_BODY()
public:
	UEffectCreateEntity();
	~UEffectCreateEntity();

public:
	/*读取技能配置*/
	virtual void init(FHIT_EFFECT dictDat, USkill* skill);

	/*接受效果*/
	virtual void onReceive(USkill* skill, CS3Entity* caster, CS3Entity* receiver);

private:
	FString _scriptID;
	float _offsetFront = 0.0;
	float _offsetLeft = 0.0;
};

