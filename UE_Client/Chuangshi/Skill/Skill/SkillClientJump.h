#pragma once
#include "CoreMinimal.h"
#include "Skill/Skill/CombatSkillClient.h"
#include "SkillClientJump.generated.h"

/*
* 文件名称：SkillClientJump.h
* 功能说明：客户端跳扑技能
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-11
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USkillClientJump :public UCombatSkillClient
{
	GENERATED_BODY()
public:
	USkillClientJump();
	~USkillClientJump();

public:
	/*初始化技能数据*/
	virtual void init(FString SkillId, const FSKILL_TABLE_DATA* dictDat);

	/*检查技能是否可以使用*/
	virtual int32 useableCheck(CS3Entity* caster, USkillTargetObjImpl* target);

	/*施放技能*/
	virtual void cast(CS3Entity* caster, USkillTargetObjImpl* target);

	/*技能结束*/
	virtual void onSkillEnd(CS3Entity* caster, USkillTargetObjImpl* target, bool castResult);
private:
	float delayTime;
	float moveTime;
};

