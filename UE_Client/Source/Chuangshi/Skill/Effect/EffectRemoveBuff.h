#pragma once
#include "EffectSkillBase.h"
#include "EffectRemoveBuff.generated.h"

/*
* 文件名称：EffectRemoveBuff.h
* 功能说明：移除buff效果（可扩展多种移除方式
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UEffectRemoveBuff : public UEffectSkillBase
{
	GENERATED_BODY()
public:
	UEffectRemoveBuff();
	~UEffectRemoveBuff();

public:
	/*读取技能配置*/
	virtual void init(FHIT_EFFECT dictDat, USkill* skill);

	/*接受效果*/
	virtual void onReceive(USkill* skill, CS3Entity* caster, CS3Entity* receiver);

private:
	TArray<int32> _buffIdList;
};

