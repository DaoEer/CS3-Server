#pragma once
#include "EffectSkillBase.h"
#include "EffectClientNormalDamage1.generated.h"

/*
* 文件名称：EffectNormalDamage.h
* 功能说明：标准伤害效果简单版
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2020-8-20
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UEffectClientNormalDamage1 : public UEffectSkillBase
{
	GENERATED_BODY()
public:
	UEffectClientNormalDamage1();
	~UEffectClientNormalDamage1();

public:
	/*读取技能配置*/
	virtual void init(FHIT_EFFECT dictDat, USkill* skill);
	/*效果添加检测*/
	virtual bool canEffect(USkill* skill, CS3Entity* caster, CS3Entity* receiver);
	/*接受效果*/
	virtual void onReceive(USkill* skill, CS3Entity* caster, CS3Entity* receiver);


private:
	int32 CustomAttrC(FString propertyStr, int32 propertyValue);

	int32 CustomAttrR(FString propertyStr, int32 propertyValue);

private:
	int32 _damageType = 1;  ///<伤害类型
	float _skillRadio = 0.0;  ///<技能效率
	int32 _skillValue = 0;    ///<技能固定值
	int32 _deadEffect = 0;      ///<死亡时，是否播放特殊效果（暴尸）
	bool _isSkipEvent = false;
	TMap<FString, int32> _customAttrC;  ///<施法者属性修正列表
	TMap<FString, int32> _customAttrR;  ///<受术者属性修正列表
};