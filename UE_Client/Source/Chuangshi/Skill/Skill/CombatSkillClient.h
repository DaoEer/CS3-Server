#pragma once
#include "CoreMinimal.h"
#include "Skill/SkillBase/Skill.h"
#include "CombatSkillClient.generated.h"

/*
* 文件名称：CombatSkillClient.h
* 功能说明：客户端引导技能
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-11
*/


UCLASS(BlueprintType)
class UCombatSkillClient :public USkill
{
	GENERATED_BODY()
public:
	UCombatSkillClient();
	~UCombatSkillClient();
public:
	/*初始化技能数据*/
	virtual void init(FString SkillId, const FSKILL_TABLE_DATA* dictDat);

	/*技能开始*/
	virtual void onSkillBegin(CS3Entity* caster, USkillTargetObjImpl* target);

	/*技能结束*/
	virtual void onSkillEnd(CS3Entity* caster, USkillTargetObjImpl* target, bool castResult);
protected:
	bool _isShowIntonateUI = false; //是否显示吟唱条界面
	FString _intonateName = ""; //吟唱名字
	FString _iconName = "";  //图标
};

