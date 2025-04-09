#pragma once
#include "EffectSkillBase.h"
#include "EffectAction.generated.h"

/*
* 文件名称：EffectAction.h
* 功能说明：受击表现效果（受击动作、光效、音效）
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UEffectAction : public UEffectSkillBase
{
	GENERATED_BODY()
public:
	UEffectAction();
	~UEffectAction();

public:
	/*读取技能配置*/
	virtual void init(FHIT_EFFECT dictDat, USkill* skill);
	/*接受效果*/
	virtual void onReceive(USkill* skill, CS3Entity* caster, CS3Entity* receiver);

private:
	TArray<FString> _actionID;
	TArray<FString> _actionBeginTime;
	FString _effectID;
	FString _soundID;
	bool _isLocal = false;
};

