#pragma once
#include "EffectSkillBase.h"
#include "EffectAddHP.generated.h"

/*
* 文件名称：EffectAddHP.h
* 功能说明：加血效果
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UEffectAddHP : public UEffectSkillBase
{
	GENERATED_BODY()
public:
	UEffectAddHP();
	~UEffectAddHP();

public:
	/*读取技能配置*/
	virtual void init(FHIT_EFFECT dictDat, USkill* skill);
	/*效果添加检测*/
	virtual bool canEffect(USkill* skill, CS3Entity* caster, CS3Entity* receiver);
	/*接受效果*/
	virtual void onReceive(USkill* skill, CS3Entity* caster, CS3Entity* receiver);

private:
	int32 _addValue = 0;
	float _percent = 0.0;
	bool _isSkipEvent = false;
};


