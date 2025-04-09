#pragma once
#include "EffectSkillBase.h"
#include "EffectDamage.generated.h"

/*
* 文件名称：EffectDamage.h
* 功能说明：真实伤害效果
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UEffectDamage : public UEffectSkillBase
{
	GENERATED_BODY()
public:
	UEffectDamage();
	~UEffectDamage();

public:
	/*读取技能配置*/
	virtual void init(FHIT_EFFECT dictDat, USkill* skill);
	/*效果添加检测*/
	virtual bool canEffect(USkill* skill, CS3Entity* caster, CS3Entity* receiver);
	/*接受效果*/
	virtual void onReceive(USkill* skill, CS3Entity* caster, CS3Entity* receiver);

private:
	int32 _damageValue = 0;
	float _percent = 0.0;
	int32 _deadEffect = 0;
	bool _isSkipEvent = false;
};

