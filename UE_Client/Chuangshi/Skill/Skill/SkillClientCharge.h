#pragma once
#include "CoreMinimal.h"
#include "Skill/Skill/CombatSkillClient.h"
#include "SkillClientCharge.generated.h"

/*
* 文件名称：SkillClientCharge.h
* 功能说明：客户端怪物冲锋技能
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-11
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USkillClientCharge :public UCombatSkillClient
{
	GENERATED_BODY()
public:
	USkillClientCharge();
	~USkillClientCharge();

public:
	/*初始化技能数据*/
	virtual void init(FString SkillId, const FSKILL_TABLE_DATA* dictDat);

	/*施放技能*/
	virtual void cast(CS3Entity* caster, USkillTargetObjImpl* target);

	/*技能结束*/
	virtual void onSkillEnd(CS3Entity* caster, USkillTargetObjImpl* target, bool castResult);

private:
	float casterMoveSpeed = 0.0;     //冲刺速度
	float casterMoveDistance = 0.0;  //冲刺距离
};

