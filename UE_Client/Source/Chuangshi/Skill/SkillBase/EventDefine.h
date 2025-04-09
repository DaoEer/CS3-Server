#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/GameDeFine.h"
#include "GameData/Skill/BuffDataType.h"
#include "GameData/Skill/SkillTableData.h"
#include "SkillTargetObjImpl.h"
#include "EventDefine.generated.h"

/*
* 文件名称：EventDefine.h
* 功能说明：技能事件类
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

class USkill;
/*基类*/
UCLASS(BlueprintType)
class CHUANGSHI_API UBaseEvent :public UCS3Object
{
	GENERATED_BODY()
public:
	UBaseEvent();
	~UBaseEvent();
public:
	virtual void init(FSKILL_EVENT args);
	virtual bool canTriggerEvent(TMap<FString, FVariant> pDict);

protected:
	ENUM_SKILL_EVENT eventType;
};

/*死亡事件*/
UCLASS(BlueprintType)
class CHUANGSHI_API UOnDieEvent :public UBaseEvent
{
	GENERATED_BODY()
public:
	UOnDieEvent();
	~UOnDieEvent();
public:
	virtual void init(FSKILL_EVENT args);
	virtual bool canTriggerEvent(TMap<FString, FVariant> pDict);

private:
	ACTION_FLAG _actForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	int32 _type = NULL;
};

/*基础状态发送改变*/
UCLASS(BlueprintType)
class CHUANGSHI_API UStateChangeEvent :public UBaseEvent
{
	GENERATED_BODY()
public:
	UStateChangeEvent();
	~UStateChangeEvent();
public:
	virtual void init(FSKILL_EVENT args);
	virtual bool canTriggerEvent(TMap<FString, FVariant> pDict);

private:
	int32 _oldState = NULL;
	int32 _newState = NULL;;
};

/*技能开关状态改变*/
UCLASS(BlueprintType)
class CHUANGSHI_API UActWorldChangeEvent :public UBaseEvent
{
	GENERATED_BODY()
public:
	UActWorldChangeEvent();
	~UActWorldChangeEvent();

public:
	virtual void init(FSKILL_EVENT args);
	virtual bool canTriggerEvent(TMap<FString, FVariant> pDict);
private:
	ACTION_FLAG _actWord = ACTION_FLAG::ACTION_FORBID_NONE;
	bool _disable = NULL;
};

/*技能开关状态改变*/
UCLASS(BlueprintType)
class CHUANGSHI_API UEffectStateChangeEvent :public UBaseEvent
{
	GENERATED_BODY()
public:
	UEffectStateChangeEvent();
	~UEffectStateChangeEvent();

public:
	virtual void init(FSKILL_EVENT args);
	virtual bool canTriggerEvent(TMap<FString, FVariant> pDict);

private:
	EFFECT_STATE _effectState = EFFECT_STATE::EFFECT_STATE_NULL;
	bool _disable = NULL;
};


/*自定义事件*/
UCLASS(BlueprintType)
class CHUANGSHI_API UCustomEvent :public UBaseEvent
{
	GENERATED_BODY()
public:
	UCustomEvent();
	~UCustomEvent();

public:
	virtual void init(FSKILL_EVENT args);
	virtual bool canTriggerEvent(TMap<FString, FVariant> pDict);

private:
	int32 _id = NULL;
	ACTION_FLAG _actWord = ACTION_FLAG::ACTION_FORBID_NONE;
};

/*技能流程事件*/
UCLASS(BlueprintType)
class CHUANGSHI_API USkillEvent :public UBaseEvent
{
	GENERATED_BODY()
public:
	USkillEvent();
	~USkillEvent();

public:
	virtual void init(FSKILL_EVENT args);
	virtual bool canTriggerEvent(TMap<FString, FVariant> pDict);

protected:
	ACTION_FLAG _actForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	int32 _type = NULL;
	int32 _skillID = NULL;
};

/*治疗事件*/
UCLASS(BlueprintType)
class CHUANGSHI_API UCureEvent :public USkillEvent
{
	GENERATED_BODY()
public:
	UCureEvent();
	~UCureEvent();

private:

};
/*伤害事件*/
UCLASS(BlueprintType)
class CHUANGSHI_API UHurtEvent :public UBaseEvent
{
	GENERATED_BODY()
public:
	UHurtEvent();
	~UHurtEvent();

public:
	virtual void init(FSKILL_EVENT args);
	virtual bool canTriggerEvent(TMap<FString, FVariant> pDict);

private:
	ACTION_FLAG _actForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	int32 _type = NULL;
	TArray<FString> _conditions;
};


/*技能主流程事件*/
UCLASS(BlueprintType)
class CHUANGSHI_API USkillProcessEvent :public USkillEvent
{
	GENERATED_BODY()
public:
	USkillProcessEvent();
	~USkillProcessEvent();

private:

};

/*buff主流程事件*/
UCLASS(BlueprintType)
class CHUANGSHI_API UBuffProcessEvent :public UBaseEvent
{
	GENERATED_BODY()
public:
	UBuffProcessEvent();
	~UBuffProcessEvent();

public:
	virtual void init(FSKILL_EVENT args);
	virtual bool canTriggerEvent(TMap<FString, FVariant> pDict);

protected:
	ACTION_FLAG _actForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	int32 _type = NULL;
	int32 _buffID = NULL;
};



USTRUCT(BlueprintType)
struct CHUANGSHI_API FEVENT_DATAS
{
	GENERATED_BODY();
public:
	UPROPERTY()
	TArray<UBaseEvent*> EventList;
};

/*施法者事件*/
UCLASS(BlueprintType)
class CHUANGSHI_API UEventDefine :public UCS3Object
{
	GENERATED_BODY()
public:
	UEventDefine();
	~UEventDefine();
public:
	/*加载数据*/
	void init(TArray<FSKILL_EVENT> datas);

	/*创建事件实例*/
	UBaseEvent* CreateEventInstance(FSKILL_EVENT data);

	/*注册技能事件*/
	void registerEvent(USkill* skill, CS3Entity* caster);

	/*删除技能事件*/
	void unRegisterEvent(USkill* skill, CS3Entity* caster);

	/*注册Buff事件*/
	void registerBuffEvent(UBuffDataType * buffData, CS3Entity* caster, CS3Entity* receiver);

	/*刪除Buff事件*/
	void unRegisterBuffEvent(UBuffDataType * buffData, CS3Entity* caster, CS3Entity* receiver);

	/*判断是能触发事件*/
	bool canTriggerEvent(ENUM_SKILL_EVENT eventType, TMap<FString, FVariant> pDict);

private:
	UPROPERTY()
	TMap<ENUM_SKILL_EVENT, FEVENT_DATAS> _eventList;
};


/*受术目标事件*/
UCLASS(BlueprintType)
class CHUANGSHI_API UReceiverEventDefine :public UCS3Object
{
	GENERATED_BODY()
public:
	UReceiverEventDefine();
	~UReceiverEventDefine();

public:
	void init(TArray<FSKILL_EVENT> datas);

	/*创建事件实例*/
	UBaseEvent* CreateEventInstance(FSKILL_EVENT data);

	/*注册技能事件 */
	void registerEvent(USkill* skill, CS3Entity* caster, USkillTargetObjImpl* target);

	/*注册Buff事件*/
	void registerBuffEvent(UBuffDataType * buffData, CS3Entity* receiver);

	/*刪除Buff事件*/
	void unRegisterBuffEvent(UBuffDataType * buffData, CS3Entity* receiver);

	/*判断是能触发事件*/
	bool canTriggerEvent(ENUM_SKILL_EVENT eventType, TMap<FString, FVariant> pDict);
private:
	UPROPERTY()
	TMap<ENUM_SKILL_EVENT, FEVENT_DATAS> _receiverEventList;
};