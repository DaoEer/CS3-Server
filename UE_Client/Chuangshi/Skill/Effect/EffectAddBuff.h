#pragma once
#include "EffectSkillBase.h"
#include "EffectAddBuff.generated.h"

/*
* 文件名称：EffectAddBuff.h
* 功能说明：添加buff效果
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UEffectAddBuff : public UEffectSkillBase
{
	GENERATED_BODY()
public:
	UEffectAddBuff();
	~UEffectAddBuff();
public:
	/*读取技能配置*/
	virtual void init(FHIT_EFFECT dictDat, USkill* skill);

	/*接受效果*/
	virtual void onReceive(USkill* skill, CS3Entity* caster, CS3Entity* receiver);

private:
	int32 _buffID;
};

