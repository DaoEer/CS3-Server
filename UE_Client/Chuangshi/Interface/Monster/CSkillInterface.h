// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Skill/HoldEffectDataType.h"
#include "GameData/Skill/BuffDataType.h"
#include "GameData/Skill/SkillData.h"
#include "GameData/Skill/BuffData.h"
#include "GameData/Skill/SkillTableData.h"
#include "Skill/Effect/HoldEffect/HoldEffect.h"
#include "SKill/SkillBase/SkillTargetObjImpl.h"


#include "CSkillInterface.generated.h"


/**
 * 
 */

class USkill;
class UBuff;

USTRUCT(BlueprintType)
struct CHUANGSHI_API FINT32_INT32
{
	GENERATED_BODY();
public:
	UPROPERTY()
		int32 Num1;
	UPROPERTY()
		int32 Num2;
	bool operator== (const FINT32_INT32& other)
	{
		return (Num1 == other.Num1 && Num2 == other.Num2);
	}
};

UCLASS()
class CHUANGSHI_API UCSkillInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UCSkillInterface();
	~UCSkillInterface(){};
	static FString GetName() { return TEXT("CSkillInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_CSkillInterface.BP_CSkillInterface_C'"); } //获取蓝图对象路径


	virtual void BeginDestroy()override;
public:

#pragma region	技能流程
	/*申请向entity施放客户端技能*/
	void RequestUseCSkillToEntity(int32 skillID, int32 targetID);

	/*申请向位置施放客户端技能*/
	void RequestUseCSkillToPosition(int32 skillID, FVector position);

	/*向entity施放客户端技能*/
	int32 useCSkillToEntity(int32 skillID, int32 targetID);

	/*向位置施放客户端技能*/
	int32 useCSkillToPosition(int32 skillID, FVector position);

	/*技能开始*/
	void onSkillBegin( USkill * skill, USkillTargetObjImpl * target);

	/*技能结束*/
	void onSkillEnd( USkill * skill, bool castResult);

	/*触发施法者“施展开始时”*/
	void triggerEventSkillBegin(USkill * skill);

	/*触发施法者“施展结束时”*/
	void triggerEventSkillEnd(USkill * skill);

	/*中断法术的施放*/
	void interruptSkill(int32 reason);

	/*当施法被打断时的通知*/
	void onSkillInterrupted(int32 skillID, int32 reason);

	/*中断瞬发的施放*/
	void interruptInstantSkill(USkill * skill, int32 reason);

	/*设置受术目标ID*/
	void setReceiverID(int32 id);

	void casterSkillEnd( USkill * skill);

	void onCasterSkillEnd(int32 casterID, int32 skillID);

	/*技能中断标识*/
	void setIsInterruptSkill(int32 skillID, bool value);

	/*判断是否有技能中断标识*/
	bool IsInterruptSkill(int32 skillID);

	/*瞬发技能中断标识*/
	void setIsInterruptInstantSkill(int32 skillID, bool value);

	/*判断是否有瞬发技能中断标识*/
	bool IsInterruptInstantSkill(int32 skillID);

	/*是否正在施法中*/
	bool isCastingSkill();

	/*获取正在施放的技能ID*/
	int32 getCastingSkill();

	/*设置连续动作标识*/
	void setActionIndex();

	/*获得连续动作标识*/
	int32 getActionIndex();

	/*设置技能连续动作标识*/
	void setSkillActionIndex(int32 skillID, int32 ActionIndex);

	/*获得技能连续动作标识*/
	int32 getSkillActionIndex(int32 skillID);

	/*移除技能连续动作标识*/
	void removeSkillActionIndex(int32 skillID);

	/*引导过程 吟唱（只是表现功能，非吟唱技能）*/
	void intonateSpell(float intonateTime, int32 skillID);

	/*引导 吟唱结束*/
	void intonateSpellOver();

	/*技能转向*/
	void turnToSkillTarget(USkillTargetObjImpl * target);

	void CSkill_onClientActorCreate();
#pragma endregion

#pragma region buff流程
	
	UBuffDataType* getBuffData(int32 index);

	UBuff* getBuff(int32 buffID);

	/*添加buff*/
	bool addBuff(CS3Entity* caster, int32 buffID);

	/*添加服务器buff*/
	void AddSeverBuff(CS3Entity* caster, int32 buffID);

	/*添加一个Buff*/
	void onAddBuff(UBuffDataType* buffData);

	/*上线重新加载buff*/
	void reloadBuff(int32 buffIndex, BUFF_END_RESON reason = BUFF_END_RESON::BUFF_END_RESON_BY_INTERRUPT);

	/*停止buff效果*/
	void stopBuff(UBuffDataType* buffData, BUFF_END_RESON reason = BUFF_END_RESON::BUFF_END_RESON_BY_INTERRUPT);

	/*清除buff数据*/
	void clearBuff(UBuffDataType* buffData, BUFF_END_RESON reason);

	/*产生一个新的buffindex*/
	int32 newBuffIndex();

	/*通知客户端添加buff*/
	void notifyClientAddBuff(UBuffDataType* buffData, float buffHoldTime, float buffRemainTime);

	/*通知客户端删除buff*/
	void notifyClientRemoveBuff(UBuffDataType* buffData);

	/*移除所有的buff*/
	void removeAllBuff();

	/*移除一个buff*/
	bool removeBuff(int32 buffIndex, BUFF_END_RESON reason = BUFF_END_RESON::BUFF_END_RESON_BY_INTERRUPT);

	/*buff时间结束*/
	void timeOverEndBuff(int32 buffIndex);

	/*通过id移除buff*/
	bool removeBuffByID(int32 buffID, BUFF_END_RESON reason = BUFF_END_RESON::BUFF_END_RESON_BY_INTERRUPT);

	/*通过index移除buff*/
	bool removeBuffByIndex(int32 buffIndex, BUFF_END_RESON reason = BUFF_END_RESON::BUFF_END_RESON_BY_INTERRUPT);

	/*通过持有效果移除buff*/
	void removeBuffByEffect(ENUM_HOLD_EFFECT_TYPE holdEffectName);

	/*触发施法者“获得Buff时事件”*/
	void triggerEventBuffAdd(UBuff* buff);

	/*触发施法者“失去Buff时事件”*/
	void triggerEventBuffRemove(UBuff* buff);

	/*接受buff打击效果*/
	void receiveBuffHit(int32 casterID, int32 buffID, FString attrName, int32 index);

	/*查找指定类型的所有buff索引。 通过BUFFID寻找*/
	TArray<int32> findBuffsByBuffID(int32 buffID);

	/*查找指定脚本的buff*/
	TArray<int32> findBuffsByBuffScript(FString buffScript);

	TMap<int32, UBuffDataType*> getAttrBuffs();

	/*同步添加buff数据到服务器*/
	void SynClientAddBuff(UBuffDataType* buffData);

	/*同步移除buff数据到服务器*/
	void SynClientRemoveBuff(int32 buffIndex);
#pragma endregion

#pragma region buff的tick
	/*刷新buff结束定时器*/
	void buffHoldTimerRefresh();

	/*添加buff Tick*/
	void addBuffHoldTick();

	/*结束定时器回调*/
	void onBuffHoldTick();
#pragma endregion

#pragma region	技能事件

	/*施法者技能事件注册*/
	void registerSkillEvent(ENUM_SKILL_EVENT eventType, int32 skillID);

	/*施法者技能事件删除*/
	void unRegisterSkillEvent(ENUM_SKILL_EVENT eventType, int32 skillID);

	/*受术目标技能事件注册(仅支持技能目标类型为entity)*/
	void registerReceiverSkillEvent(ENUM_SKILL_EVENT eventType, int32 entityID, int32 skillID);

	/*受术目标技能事件删除(仅支持技能目标类型为entity)*/
	void unRegisterReceiverSkillEvent(ENUM_SKILL_EVENT eventType, int32 entityID, int32 skillID);

	/*施法者buff事件注册*/
	void registerCasterBuffEvent(ENUM_SKILL_EVENT eventType, int32 entityID, int32 index);

	void unRegisterCasterBuffEvent(ENUM_SKILL_EVENT eventType, int32 entityID, int32 index);

	/*受术者buff事件注册*/
	void registerBuffEvent(ENUM_SKILL_EVENT eventType, int32 index);

	void unRegisterBuffEvent(ENUM_SKILL_EVENT eventType, int32 index);

	/*触发技能事件*/
	void triggerSkillEvent(ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict);

	/*触发施法者技能事件*/
	void triggerCasterSkillEventList(ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict);

	/*触发受术者技能事件*/
	void triggerReceiverSkillEventList(ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict);

	/*触发受术者buff事件*/
	void triggerReceiverBuffEventList(ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict);

	/*触发施法者buff事件*/
	void triggerCasterBuffEventList(ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict);

	/*触发施法者buff事*/
	void triggerCasterBuffEvent(ENUM_SKILL_EVENT eventType, int32 buffIndex, int32 triggerID, TMap<FString, FVariant> pDict);
#pragma endregion

#pragma region buff叠加相关
	/*叠加buff*/
	void stackBuff(int32 buffIndex);

	/*重置持续时间*/
	void resetBuffEndTime(int32 buffIndex);

	/*重置buff持续时间回调*/
	void onResetBuffEndTime(int32 buffIndex, float buffTime);
#pragma endregion

#pragma region 客户端技能效果结算
	/*客户端申请接受伤害*/
	void receiveDamage(int32 casterID, int32 skillID, int32 damageType, int32 damage, int32 isCritical, int32 isParry, int32 deadEffect, int32 actForbid);

	/*加血效果*/
	void CSkillSetHP(int32 value);

	/*客户端技能申请创建entity*/
	void CSkillCreateEntityByScriptID(FString scriptID, FVector position, FVector direction);

	/*接受罡气伤害*/
	void CSkillGangQiDamage(int32 casterID, int32 skillGangQiValue, float skillGangQiRadio);
#pragma endregion

#pragma region 客户端持有效果结算
	/*添加动作限制字*/
	void CSkillAddActCounters(TArray<int32> actList);

	/*移除动作限制字*/
	void CSkillRemoveActCounters(TArray<int32> actList);

	/*添加效果状态*/
	void CSkillAddEffectState(EFFECT_STATE EffectState);

	/*移除效果状态*/
	void CSkillRemoveEffectState(EFFECT_STATE EffectState);

	/*战斗属性增益\减益*/
	void CSkillEffectAddAttr(TArray<int32> propertiesList, int32 attrPercent, int32 attrValue);
#pragma endregion

#pragma region 客户端技能扩展脚本结算
	/*冲锋技能冲锋结算*/
	void CSkillClientCharge(FVector desPosition, FVector direction, float casterMoveSpeed, bool ischangeDirection);

	/*跳扑技能结算*/
	void CSkillClientJump(FVector desPosition, float moveSpeed, float delayTime);

	/*客户端技能停止移动*/
	void CSkillStopMove(MOVETYPE type);

	/*客户端技能闪避*/
	void CSkillOnDodgeSkillHit(int32 CasterID);
#pragma endregion

#pragma region 客户端技能消耗结算
	/*设置MP*/
	void CSkillSetMP(int32 value);

	/*消耗罡气*/
	void CSkillRecvGangQi(int32 value);

	/*消耗物品*/
	void CSkillRequireItem(int32 itemID, int32 amount );
#pragma endregion

#pragma region 技能CD
	/*设置CD*/
	void setCooldown(TMap<int32, float> cooldownDict);

	/*增/减CD*/
	void changeCooldown(TMap<int32, float> paramDict);

	/*获取冷却时间*/
	TArray<FSKILL_UPDATE_COOL_DOWN> getCooldown();

	/*更新冷却时间数据到客户端*/
	void updateCooldownToClient(TMap<int32, float> cooldownDict);
#pragma endregion

#pragma region 技能打击相关
	/*添加技能打击timer*/
	void addSkillHitTimer(float delayTime, USkill * skill, CS3Entity *caster,  USkillTargetObjImpl * target, int32 hitTime);

	/*删除技能打击timer*/
	void delSkillHitTimer(int32 SKillID);

	/*接受技能打击效果*/
	int32 receiveSkillHit(CS3Entity *caster, CS3Entity *receiver, int32 skillID, int32 hitTime, int32 Index);
#pragma endregion

#pragma region 持续效果相关
	/*获取一个新的固定ID的持有效果的index*/
	int32 getNewHoldEffectIndex();

	/*添加持续效果数据*/
	void addHoldEffectData(UHoldEffectDataType * effectData);

	/*移除持有效果数据*/
	void removeHoldEffectData(int32 index);

	TArray<UHoldEffectDataType *> GetHoldEffectData();
#pragma endregion

#pragma region 吟唱技能
	/*设置吟唱技能的技能目标*/
	void SetSkillSingTarget(int32 key, USkillTargetObjImpl * value);

	/*查询吟唱技能的技能目标*/
	USkillTargetObjImpl* GetSkillSingTarget(int32 key);

	/*移除吟唱技能的技能目标*/
	void RemoveSkillSingTarget(int32 key);
#pragma endregion

#pragma region 技能的效果广播(暂定方案)
	/**
	*Define method
	*广播对位置正式施法（使用技能）S2C
	*
	*@param  skillID 释放的技能ID
	*@param  PosX 位置X
	*@param  PosY 位置Y
	*@param  PosZ 位置Z
	*@param ActionID 动作ID
	*@param BeginTime 动作起始时间
	*@param CasterID 施法者ID
	*
	*@return 无
	*/
	void BroadcastCSkillToPosition(int32 SkillID, uint8 isInstantSkill, const float PosX, const float PosY,
		float PosZ, TArray<FString> ActionID, TArray<FString> BeginTime,int32 ActionIndex, int32 CasterID);

	/**
	*Define method
	*广播对目标正式施法（使用技能）S2C
	*
	*@param SkillID 释放的技能ID
	*@param targetID 目标对象ID
	*@param ActionID 动作ID
	*@param BeginTime 动作起始时间
	*@param actionIndex 动作标识号
	*@param CasterID 施法者ID
	*@return 无
	*/
	void BroadcastCSkillToTarget(int32  SkillID, uint8 isInstantSkill, int32  TargetID,
		TArray<FString> ActionID, TArray<FString> BeginTime, int32 ActionIndex, int32 CasterID);

	/**
	*Define method
	*广播技能中断S2C
	*
	*@param SkillID 释放的技能ID
	*@param Reason 技能中断Reason
	*@param actionIndex 动作标识号
	*
	*@return 无
	*/
	void BroadcastCSkillInterrupted(int32 SkillID, int32 Reason, int32 ActionIndex);

	/**
	*Define method
	*广播受击播放动作光效（使用技能）S2C
	*@param CasterID 施放者ID
	*@param targetID 目标对象ID
	*@param actionIndex 动作标识号
	*@param ActionID 动作ID
	*@param EffectID 光效ID
	*@param SoundID 声音ID
	*@param BeginTime 动作起始时间
	*
	*@return 无
	*/
	void BroadcastBeHitPlayEffect(int32 CasterID, int32 TargetID, int32 ActionIndex,
		TArray<FString> ActionID, FString EffectID, FString SoundID, TArray<FString> BeginTime);

	/**
	*Define method
	*广播持有效果HoldEffectPlayEffect播放动作光效声音（使用技能）S2C
	*
	*@param EffectIndex 持有效果索引
	*@param actionIndex 动作标识号
	*@param ActionID 动作ID
	*@param EffectID 光效ID
	*@param SoundID 声音ID
	*@param BeginTime 动作起始时间
	*
	*@return 无
	*/
	void BroadcastHoldEffectPlayEffect(int32 CasterID, int32 EffectIndex, int32 ActionIndex,
		TArray<FString> ActionID, FString EffectID, FString SoundID, TArray<FString> BeginTime);
	/**
	*Define method
	*广播持有效果HoldEffectPlayEffect结束S2C
	*
	*
	*@param EffectIndex 持有效果索引
	*@param actionIndex 动作标识号
	*
	*@return 无
	*/
	void BroadcastHoldEffectEndEffect(int32 EffectIndex, const int32 ActionIndex);

	/**
	*广播开始Buff效果
	*
	*@param BuffIndex buff 下标
	*@param CasterID buff 施法者
	*@param actionIndex 动作标识号
	*@param ActionID buff动作
	*@param BeginTime 动作起始时间
	*@param EffectID buff光效
	*@param Sound buff声音
	*
	*@return 无
	*/
	void BroadcastPlayBuffEffect(int32 BuffIndex, int32 CasterID, int32 ActionIndex,
		TArray<FString> ActionID, TArray<FString> BeginTime, FString EffectID, FString SoundID);

	/*广播新增一个buff*/
	void BroadcastAddBuff(int32 BuffIndex, int32 BuffID, FString BuffScript, int32 CasterID,
		float BuffTotalTime, FString EndTime, int32 Layer);

	/*广播移除一个buff*/
	void BroadcastRemoveBuff(int32 BuffIndex);

	void BroadcastOnBuffLayerChange(int32 BuffIndex, int32 layer);
#pragma endregion

#pragma region buff的扩展广播(暂定方案)

#pragma endregion

#pragma region 击退buff相关
	/*添加被击飞timer*/
	void addHitFlyTimer(float delayTime, int32 casterID, TArray<FString> actionID, FString effectID, FString soundID, TArray<FString> actionBeginTime);

	/*被击飞timer，用于击飞后起身*/
	void onHitFlyTimer(int32 casterID, TArray<FString> actionID, FString effectID, FString soundID, TArray<FString> actionBeginTime);

	/*取消起身timer*/
	void delHitFlyTimer();

	/*改变朝向*/
	void CSkillChangeDirection(FVector direction, int32 changeReason);
	
	/*开始击退*/
	void CSkillDoHitBack(int32 casterID, float moveSpeed, FVector desPosition, FString actionID, float actionBeginTime );

	/*结束击退*/
	void CSkillOnEndHitBack(int32 casterID, FString actionID, FString endActionID);
#pragma endregion
private:
	int32 castingSkillID = 0;
	int32 receiverID = 0;
	int32 lastHoldEffectIndex = 0;
	int32 actionIndex = 1000001;				///<连续动作标识,前面得留给号码留给服务器使用
	int32 lastBuffIndex = 1000001;
	int64 nextBuffEndTickValue = 0;			///<下一个结束time的时间
	FTimerHandle buffHoldTickTimerID;
	FTimerHandle hitFlyTimer;			///<被击飞timer
	TArray<int32> removeBuffList;
	TMap<int32, int32> skillActionIndex;
	TMap<int32, bool> isInterruptSkill;			 ///<技能中断标识
	TMap<int32, bool> isInterruptInstantSkill;  ///<瞬发技能中断标识
	TMap<ENUM_SKILL_EVENT, TArray<int32>> casterSkillEventList; ///<施法者事件列表
	TMap<ENUM_SKILL_EVENT, TArray<FINT32_INT32>> receiverSkillEventList; ///<受术者事件列表
	TMap<ENUM_SKILL_EVENT, TArray<int32>> receiverbuffEventList; ///<受术者buff事件列表
	TMap<ENUM_SKILL_EVENT, TArray<FINT32_INT32>> casterbuffEventList; ///<施法者buff事件列表
	TMap<int32, TArray<FTimerHandle>> SKillHitTimerHandles;  ///<技能打击Timer句柄

	UPROPERTY()
	TArray<FSKILL_UPDATE_COOL_DOWN> attrCooldowns;
	
	UPROPERTY()
	TArray<UHoldEffectDataType *> holdEffectData; ///<持有效果数据

	UPROPERTY()
	TMap<int32, USkillTargetObjImpl *>SkillSingTarget;  ///<吟唱技能的技能目标

	UPROPERTY()
	TArray<UBuffDataType*>cacheBuff;		  ///<排序好的buff缓存

	UPROPERTY()
	TMap<int32, UBuffDataType*> attrBuffs;     ///<buff数据
};