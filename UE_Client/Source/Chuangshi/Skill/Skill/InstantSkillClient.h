#pragma once
#include "CoreMinimal.h"
#include "Skill/SkillBase/Skill.h"
#include "InstantSkillClient.generated.h"

/*
* 文件名称：InstantSkillClient.h
* 功能说明：客户端瞬发技能
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-11
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UInstantSkillClient :public USkill
{
	GENERATED_BODY()
public:
	UInstantSkillClient();
	~UInstantSkillClient();


public:
	/*检查技能是否可以使用*/
	virtual int32 useableCheck(CS3Entity* caster, USkillTargetObjImpl* target);

	/*技能开始*/
	virtual void onSkillBegin(CS3Entity* caster, USkillTargetObjImpl* target);

	/*技能结束*/
	virtual void onSkillEnd(CS3Entity* caster, USkillTargetObjImpl* target, bool castResult);

	/*触发技能事件*/
	virtual void triggerSkillEvent(CS3Entity* caster, ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict);

	/*触发受术目标事件*/
	virtual void triggerReceiverSkillEvent(CS3Entity* caster, CS3Entity* receiver, ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict);

	/*判断是否是瞬发技能*/
	virtual bool isInstantSkill();
private:

};

