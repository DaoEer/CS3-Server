#pragma once
#include "CoreMinimal.h"
#include "Skill/Skill/CombatSkillClient.h"
#include "SkillClientSing.generated.h"

/*
* 文件名称：SkillClientSing.h
* 功能说明：客户端吟唱技能
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-11
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USkillClientSing :public UCombatSkillClient
{
	GENERATED_BODY()
public:
	USkillClientSing();
	~USkillClientSing();
public:
	/*初始化技能数据*/
	virtual void init(FString SkillId, const FSKILL_TABLE_DATA* dictDat);

	/*施放技能*/
	virtual int32 useSkill(CS3Entity* caster, USkillTargetObjImpl* target);

	/*技能结束*/
	virtual void onSkillEnd(CS3Entity* caster, USkillTargetObjImpl* target, bool castResult);

	/*继续施放技能*/
	int32 continueCastSkill(CS3Entity* caster, USkillTargetObjImpl* target);

	/*设置技能申请目标*/
	void setSkillSingTarget(CS3Entity* caster, USkillTargetObjImpl* target);

	/*获得技能申请目标*/
	USkillTargetObjImpl* getSkillSingTarget(CS3Entity* caster);

	/*移除技能申请目标*/
	void removeSkillSingTarget(CS3Entity* caster);
private:
	int32 _endHitSkill = 0;
};