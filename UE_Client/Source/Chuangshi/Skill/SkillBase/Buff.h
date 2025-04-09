#pragma once
#include "CoreMinimal.h"
#include "HitDefine.h"
#include "ObjectCondition.h"
#include "EventDefine.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/CS3Object.h"
#include "GameData/Skill/BuffDataType.h"
#include "GameData/Skill/BuffData.h"
#include "GameData/Skill/BuffTableData.h"
#include "Skill/Effect/EffectSkillBase.h"
#include "Skill/Effect/HoldEffect/HoldEffect.h"

#include "Buff.generated.h"


UCLASS(BlueprintType)
class CHUANGSHI_API UBuff :public UCS3Object
{
	GENERATED_BODY()
public:
	UBuff();
	~UBuff();

public:
	/*初始化buff数据*/
	virtual void init(FString BuffID, const FBUFF_TABLE_DATA* dictDat);

	/*用于给目标施加一个buff，所有的buff的接收都必须通过此接口，
		此接口必须判断接收者是否为realEntity*/
	virtual bool receive(CS3Entity* caster , CS3Entity* receiver);

	/*通过了免疫、替换等等等的拦截，真正要加buff*/
	virtual bool receiveSuccess(CS3Entity* caster, CS3Entity* receiver);

	/*添加检测*/
	virtual bool addBuffCheck(CS3Entity* caster, CS3Entity* receiver);

	/*效果开始*/
	virtual void doBegin(CS3Entity* receiver, UBuffDataType* buffData);

	/*上线重新加载buff*/
	virtual void doReload(CS3Entity* receiver, UBuffDataType* buffData);

	/*效果结束*/
	virtual void doEnd(CS3Entity* receiver, UBuffDataType* buffData, BUFF_END_RESON reason);

	/*清除Buff数据*/
	virtual void doClear(CS3Entity* receiver, UBuffDataType* buffData, BUFF_END_RESON reason);

	/*加载持有效果*/
	virtual void addHoldEffect(CS3Entity* receiver, UBuffDataType* buffData ,bool isReloadBuff = false);

	/*加载持有效果*/
	virtual void removeHoldEffect(CS3Entity* receiver, UBuffDataType* buffData);

	/*加载持有效果*/
	virtual void onClientActorCreate(CS3Entity* receiver, UBuffDataType* buffData);

	/*中断*/
	virtual	void doInterrupt(CS3Entity* receiver, UBuffDataType* buffData);

	/*处理周期*/
	virtual	void doLoop(CS3Entity* receiver, UBuffDataType* buffData);

	/*获得打击*/
	virtual UBuffHitDefine* getHit(FString attrName, int32 index);

	/*周期打击*/
	virtual	void doLoopHit(CS3Entity* receiver, UBuffDataType* buffData);

	/*开始打击*/
	virtual	void doBeginHit(CS3Entity* receiver, UBuffDataType* buffData);

	/*结束打击*/
	virtual	void doEndHit(CS3Entity* receiver, UBuffDataType* buffData);

	/*中断打击*/
	virtual void doInterruptHit(CS3Entity* receiver, UBuffDataType* buffData);

	/*叠加*/
	virtual	void doStack(CS3Entity* receiver, UBuffDataType* buffData);

	/*注册事件*/
	virtual	void registerEvent(CS3Entity* receiver, UBuffDataType* buffData);

	/*删除事件*/
	virtual	void unRegisterEvent(CS3Entity* receiver, UBuffDataType* buffData);

	/*触发受术者buff事件*/
	virtual void triggerBuffEvent(CS3Entity* receiver, ENUM_SKILL_EVENT eventType, int32 triggerID, UBuffDataType * buffData, TMap<FString, FVariant> pDict);

	/*触发施法者buff事件*/
	virtual void triggerCasterBuffEvent(CS3Entity* receiver, ENUM_SKILL_EVENT eventType, int32 triggerID, UBuffDataType * buffData, TMap<FString, FVariant> pDict);

	/*创建新的buff数据*/
	virtual UBuffDataType* getNewBuffData(CS3Entity* caster, CS3Entity* receiver);

	/*获取buff剩余时间*/
	float getBuffRemainTime(UBuffDataType* buffData);

	/*根据持续时间计算结束时间*/
	int64 calculateEndTime(float holdTime);

	/*检查是否已超时*/
	virtual bool isTimeout(UBuffDataType* buffData);

	/*获得脚本类型*/
	FString getScriptType();

	/*获得ID*/
	int32 getID();

	/*获得Buff名称*/
	FString getBuffName();

	/*获取开关*/
	ACTION_FLAG getActForbid();

	/*获取保存类型*/
	ENUM_BUFF_SAVE_TYPE getSaveType();

	/*获取持续时间*/
	float getHoldTime();

	/*获取周期时间*/
	float getLoopTime();

	/*是否持有某效果*/
	bool isHoldEffect(ENUM_HOLD_EFFECT_TYPE effectName);

protected:
	bool isInterruptBuff;
	FString _buffName;
	FString _className;
	int32 _id;
	float _holdTime;
	float _loopTime;
	FString _buffEffect;
	FString _buffSound;
	TArray<FString> _buffAction;
	TArray<FString> _buffActionBeginTime;
	TArray<ENUM_HOLD_EFFECT_TYPE> _holdEffectNames;	///<持有效果名字
	ACTION_FLAG _actForbid;
	ENUM_BUFF_SAVE_TYPE _saveType;		///<下线保存类型
	UPROPERTY()
	UBuffReplaceCondition * _replaceCondition;  ///<置换条件
	UPROPERTY()
	TArray<UEffectSkillBase*> _replaceEffectList; ///<置换效果列表
	UPROPERTY()
	UBuffExtraCondition * _extraCondition;		///<额外条件
	UPROPERTY()
	TArray<UEffectSkillBase*> _extraEffectList; ///<额外效果列表
	UPROPERTY()
	TArray<UHoldEffect*> _holdEffectList;	///<持有效果列表
	UPROPERTY()
	UReceiverEventDefine* _targetInterruptEvent;	///<受术者中断事件
	UPROPERTY()
	UEventDefine* _casterInterruptEvent;			///<施法者中断事件
};


