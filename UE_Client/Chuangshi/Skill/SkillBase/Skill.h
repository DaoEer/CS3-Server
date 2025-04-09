#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "SkillTargetObjImpl.h"
#include "RequireDefine.h"
#include "ObjectCondition.h"
#include "HitDefine.h"
#include "ObjectDefine.h"
#include "EventDefine.h"
#include "GameData/GameDeFine.h"
#include "GameData/Skill/SkillData.h"
#include "GameData/Skill/SkillTableData.h"
#include "GameData/Skill/HoldEffectDataType.h"
#include "Skill/Effect/HoldEffect/HoldEffect.h"
#include "Skill.generated.h"

/*
* 文件名称：Skill.h
* 功能说明：技能类
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USkill :public UCS3Object
{
	GENERATED_BODY()
public:
	USkill();
	~USkill();

public:
	/*初始化技能数据*/
	virtual void init(FString SkillId, const FSKILL_TABLE_DATA* dictDat);

	/*检查技能是否可以使用*/
	virtual int32 useableCheck(CS3Entity* caster, USkillTargetObjImpl* target);

	/*施放技能*/
	virtual int32 useSkill(CS3Entity* caster, USkillTargetObjImpl* target);

	/*通过检查后使用技能*/
	virtual void use(CS3Entity* caster, USkillTargetObjImpl* target);

	/*施放技能*/
	virtual void cast(CS3Entity* caster, USkillTargetObjImpl* target);
	
	/*技能开始*/
	virtual void onSkillBegin(CS3Entity* caster, USkillTargetObjImpl* target);

	/*技能打击*/
	virtual void onSkillHit(INT32 casterID, USkillTargetObjImpl* target, int32 hitTime);

	/*技能抵达*/
	virtual void onArrive(CS3Entity* caster, USkillTargetObjImpl* target, int32 hitTime, int32 index);

	/*加载持有效果*/
	virtual void addHoldEffect(CS3Entity* caster);

	/*技能结束*/
	virtual void onSkillEnd(CS3Entity* caster, USkillTargetObjImpl* target, bool castResult);

	/*移除持有效果*/
	virtual void removeHoldEffect(CS3Entity* caster);

	/*能否中断*/
	virtual bool canInterrupt(CS3Entity* caster, int32 reason);

	/*中断*/
	virtual void interrupt(CS3Entity* caster, int32 reason, USkillTargetObjImpl* target = nullptr);

	/*处理中断的一些逻辑*/
	virtual void interruptSkill(CS3Entity* caster, int32 reason);
	 
	/*注册中断事件*/
	virtual void registerSkillEvent(CS3Entity* caster, USkillTargetObjImpl* target);

	/*取消中断事件*/
	virtual void unRegisterSkillEvent(CS3Entity* caster);

	/*触发技能事件*/
	virtual void triggerSkillEvent(CS3Entity* caster, ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict);

	/*触发受术目标事件*/
	virtual void triggerReceiverSkillEvent(CS3Entity* caster, CS3Entity* receiver, ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict);

	/*校验技能是否可以施展。*/
	virtual int32 castValidCheck(CS3Entity* caster, CS3Entity* target);

	/*检查施法目标是否满足吟唱条件*/
	virtual int32 targetValidCheck(CS3Entity* caster, USkillTargetObjImpl* target);

	/*是否是瞬发技能*/
	virtual bool isInstantSkill();

	/*是否是被动技能*/
	bool isPassiveSkill();

	/*施法者技能是否在冷却中*/
	bool isCasterCooldown(CS3Entity* caster);

	/*技能目标是否在冷却中*/
	bool isTargetCooldown(USkillTargetObjImpl* target);

	/*检测施法者消耗是否够*/
	int32 checkCasterRequire(CS3Entity* caster);

	/*检测技能目标消耗是否够*/
	int32 checkTargetRequire(USkillTargetObjImpl* target);

	/*处理施法者消耗*/
	void doCasterRequire(CS3Entity* caster);

	/*处理技能目标消耗*/
	void doTargetRequire(USkillTargetObjImpl* target);

	/*获取施法目标类型*/
	ENUM_CAST_TARGET_TYPE getTargetType();

	/*取得法术施法目标对像。*/
	UTargetBase *getCastObject();

	/*获得技能ID*/
	int32 getID();

	ACTION_FLAG getCasterActForbid();

	/*获得打击*/
	USkillHitDefine * getHit(int32 hitTime, int32 index);

	/*获得施法距离*/
	float getCastRangeMax();

	/*获取技能总时间*/
	float getSkillTotalTime();

	/*适配技能目标*/
	USkillTargetObjImpl* adaptiveTarget(CS3Entity* caster, USkillTargetObjImpl* target);
	
	/*获得脚本类型*/
	FString getScriptType();

	/*	随机获取圆内的位置   pos 为圆心,radius 为半径*/
	FVector getPositionByCircular(FVector pos, float radius);
protected:
	bool _isPassiveSkill = false; //是否被动技能
	int32 _id = 0;  //技能ID
	FString _name = ""; //技能名称
	bool _isInstantSkill = false;
	int32 _level = 0;
	ACTION_FLAG _casterActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	ACTION_FLAG _targetActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	ENUM_CAST_TARGET_TYPE _targetType = ENUM_CAST_TARGET_TYPE::TargetNothing;
	bool _isTurnToTarget = false;
	ENUM_CAST_COLLISION_TYPE _collisionType = ENUM_CAST_COLLISION_TYPE::COLLISION_DEFAULT;
	float _castRangeMax = 0.0;
	float _reTargetRadius = 0.0;
	UPROPERTY()
	TArray<UHoldEffect*> _holdEffectList; //需要实例化
	UPROPERTY()
	TMap<int32, float> _casterCoolDown; //施法者技能冷却
	UPROPERTY()
	TMap<int32, float> _targetCoolDown; //受术者技能冷却
	UPROPERTY()
	URequireDefine* _casterRequire; //施法者施放消耗
	UPROPERTY()
	URequireDefine* _targetRequire; //受术者施放消耗
	UPROPERTY()
	UObjectCondition * _casterCondition;
	UPROPERTY()
	UObjectCondition * _targetCondition;
	UPROPERTY()
	UTargetBase* _castObject;
	UPROPERTY()
	USkillHitData* _hitData;
	UPROPERTY()
	UEventDefine* _interruptEvent;
	UPROPERTY()
	UReceiverEventDefine* _receiverInterruptEvent;
	UPROPERTY()
	TArray<FString> _casterActionID;
	UPROPERTY()
	TArray<FString> _casterActionBeginTime;
	UPROPERTY()
	TArray<FString> _targetActionID;
	UPROPERTY()
	TArray<FString> _targetActionBeginTime;
};
