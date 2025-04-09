#include "Buff.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/BuffManager.h"
#include "Manager/TimeManager.h"
#include "Skill/EffectLoader.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Interface/StateInterface.h"
#include "Interface/SkillInterface.h"
#include "CS3Base/GameObject.h"

CONTROL_COMPILE_OPTIMIZE_START
UBuff::UBuff()
{
	_className = "Buff";
	isInterruptBuff = true;
	_buffName = "";
	_id = 0;
	_holdTime = 0.0;
	_buffEffect = "";
	_buffSound = "";
	_actForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	_saveType = ENUM_BUFF_SAVE_TYPE::NotSave;
	_replaceCondition = NewObject<UBuffReplaceCondition>();
	_extraCondition = NewObject<UBuffExtraCondition>();
	_casterInterruptEvent = NewObject<UEventDefine>();
	_targetInterruptEvent = NewObject<UReceiverEventDefine>();
}

UBuff::~UBuff()
{
}

void UBuff::init(FString BuffID, const FBUFF_TABLE_DATA * dictDat)
{
	_id = FSTRING_TO_INT(BuffID);
	_buffName = dictDat->BuffName;
	_holdTime = dictDat->HoldTime;
	_loopTime = dictDat->LoopTime;
	if (_holdTime > 0 && _holdTime < 0.1)
	{
		_holdTime = 0.1;
	}
	_buffEffect = dictDat->BuffEffect;
	_buffSound = dictDat->BuffSound;
	_actForbid = dictDat->TargetActForbid;
	_saveType = dictDat->SaveType;
	if (dictDat->ReplaceCondition.Num() > 0)
	{
		_replaceCondition->init(dictDat->ReplaceCondition);
	}
	for (auto i : dictDat->ReplaceEffectList)
	{
		UEffectSkillBase* effect = nullptr;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->EffectLoader))
		{
			effect = UUECS3GameInstance::Instance->EffectLoader->createEffect(i, nullptr);
		}
		if (nullptr != effect)
		{
			_replaceEffectList.Add(effect);
		}
	}
	if (dictDat->ExtraCondition.Num() > 0)
	{
		_extraCondition->init(dictDat->ExtraCondition);
	}
	for (auto i : dictDat->ExtraEffectList)
	{
		UEffectSkillBase* effect = nullptr;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->EffectLoader))
		{
			effect = UUECS3GameInstance::Instance->EffectLoader->createEffect(i, nullptr);
		}
		if (nullptr != effect)
		{
			_extraEffectList.Add(effect);
		}
	}

	for (auto i : dictDat->HoldEffectList)
	{
		UHoldEffect* holdEffect = nullptr;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->EffectLoader))
		{
			holdEffect = UUECS3GameInstance::Instance->EffectLoader->createHoldEffect(i, nullptr);
		}
		if (nullptr != holdEffect)
		{
			_holdEffectList.Add(holdEffect);
			_holdEffectNames.Add(i.HitEffectType);
		}
	}
	_casterInterruptEvent->init(dictDat->CasterInterruptBuffEvent);
	_targetInterruptEvent->init(dictDat->TargetInterruptBuffEvent);
	TArray<FString> ActionInfos = UGolbalBPFunctionLibrary::SplitString(dictDat->BuffAction);
	for (auto i : ActionInfos)
	{
		TArray<FString> actionInfo = UGolbalBPFunctionLibrary::SplitString(i, false, ":");
		if (actionInfo.Num() > 1)
		{
			_buffAction.Add(actionInfo[0]);
			_buffActionBeginTime.Add(actionInfo[1]);
		}
		else {
			_buffAction.Add(actionInfo[0]);
			_buffActionBeginTime.Add("0.0");
		}
	}
}

bool UBuff::receive(CS3Entity * caster, CS3Entity * receiver)
{
	if (!addBuffCheck(caster, receiver))
	{
		return false;
	}
	//替换效果
	if (_replaceCondition->valid(caster, receiver, true) == (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		for (auto effect : _replaceEffectList)
		{
			if (effect->canEffect(nullptr, caster, receiver))
			{
				effect->onReceive(nullptr, caster, receiver);
			}
		}
		return false;
	}
	receiveSuccess(caster, receiver);
	return true;
}

bool UBuff::receiveSuccess(CS3Entity * caster, CS3Entity * receiver)
{
	//额外效果
	if (_extraCondition->valid(caster, receiver, true) == (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		for (auto effect : _extraEffectList)
		{
			if (effect->canEffect(nullptr, caster, receiver))
			{
				effect->onReceive(nullptr, caster, receiver);
			}
		}
	}
	UBuffDataType * buffData = getNewBuffData(caster, receiver);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface) )
	{
		CSkillInterface->onAddBuff(buffData);
	}
	return true;
}

bool UBuff::addBuffCheck(CS3Entity * caster, CS3Entity * receiver)
{
	//是否有禁止标记
	if (_actForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		UStateInterface * StateInterface = ((GameObject*)receiver)->Interface_Cache.StateInterface;
		if (IsValid(StateInterface) && StateInterface->IsActionForbid(_actForbid))
		{
			return false;
		}
	}

	return true;
}

void UBuff::doBegin(CS3Entity * receiver, UBuffDataType * buffData)
{
	isInterruptBuff = false;
	bool isHit = true;
	registerEvent(receiver, buffData);
	addHoldEffect(receiver, buffData);
	int32 ActionIndex = 0;
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->triggerEventBuffAdd(this);
		CSkillInterface->setActionIndex();
		ActionIndex = CSkillInterface->getActionIndex();
		CSkillInterface->BroadcastPlayBuffEffect(buffData->index, buffData->casterID, ActionIndex, _buffAction, _buffActionBeginTime, _buffEffect, _buffSound);
	}
	USkillInterface *SkillInterface = ((GameObject*)receiver)->Interface_Cache.SkillInterface;
	if (IsValid(SkillInterface))
	{
		SkillInterface->PlayBuffEffect(buffData->index, buffData->casterID, ActionIndex, _buffAction, _buffActionBeginTime, _buffEffect, _buffSound);
	}
	if (isInterruptBuff)
	{
		doInterrupt(receiver, buffData);
	}
	isInterruptBuff = true;
	if (isHit)
	{
		doBeginHit(receiver, buffData);
	}
}

void UBuff::doReload(CS3Entity * receiver, UBuffDataType * buffData)
{
	registerEvent(receiver, buffData);
	if (buffData->casterIsSelf)
	{
		buffData->casterID = receiver->ID();
	}
	int32 ActionIndex = 0;
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->setActionIndex();
		ActionIndex = CSkillInterface->getActionIndex();
		CSkillInterface->BroadcastPlayBuffEffect(buffData->index, buffData->casterID, ActionIndex, _buffAction, _buffActionBeginTime, _buffEffect, _buffSound);
	}
	addHoldEffect(receiver, buffData, true);
	USkillInterface *SkillInterface = ((GameObject*)receiver)->Interface_Cache.SkillInterface;
	if (IsValid(SkillInterface))
	{
		SkillInterface->PlayBuffEffect(buffData->index, buffData->casterID, ActionIndex, _buffAction, _buffActionBeginTime, _buffEffect, _buffSound);
	}
}

void UBuff::doEnd(CS3Entity * receiver, UBuffDataType * buffData, BUFF_END_RESON reason)
{
	if (nullptr == receiver)
	{
		return;
	}
	if (reason == BUFF_END_RESON::BUFF_END_RESON_BY_TIME_OVER)
	{
		doEndHit(receiver, buffData);
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->triggerEventBuffRemove(this);
	}
	removeHoldEffect(receiver, buffData);
	unRegisterEvent(receiver, buffData);
	doClear(receiver, buffData, reason);
}

void UBuff::doClear(CS3Entity * receiver, UBuffDataType * buffData, BUFF_END_RESON reason)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->clearBuff(buffData, reason);
	}
}

void UBuff::addHoldEffect(CS3Entity * receiver, UBuffDataType * buffData, bool isReloadBuff)
{
	CS3Entity* caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(buffData->casterID);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	int32 index = 0;
	for (auto effect : _holdEffectList)
	{
		if (effect->canEffect(caster, receiver))
		{
			UHoldEffectDataType * effectData = effect->getNewEffectData(caster, receiver);
			effectData->index = CSkillInterface->getNewHoldEffectIndex();
			effectData->sourceType = HOLD_EFFECT_SOURCE_TYPE::HOLD_EFFECT_SOURCE_TYPE_BUFF;
			effectData->sourceID = getID();
			effectData->configIndex = index;
			effectData->casterID = caster != nullptr ? buffData->casterID : 0;
			effectData->buffIndex = buffData->index;
			CSkillInterface->addHoldEffectData(effectData);
			effect->onBegin(effectData, receiver);
		}
		++index;
	}
}

void UBuff::removeHoldEffect(CS3Entity * receiver, UBuffDataType * buffData)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	TArray<UHoldEffectDataType*> holdEffectData = CSkillInterface->GetHoldEffectData();
	int32 index = 0;
	for (auto effect : _holdEffectList)
	{
		for (auto effectData : holdEffectData)
		{
			if (effectData->sourceType == HOLD_EFFECT_SOURCE_TYPE::HOLD_EFFECT_SOURCE_TYPE_BUFF &&
				effectData->configIndex == index && effectData->buffIndex == buffData->index)
			{
				effect->onEnd(effectData, receiver);
				CSkillInterface->removeHoldEffectData(effectData->index);
			}
		}
	}
}

void UBuff::onClientActorCreate(CS3Entity * receiver, UBuffDataType * buffData)
{

}

void UBuff::doInterrupt(CS3Entity * receiver, UBuffDataType * buffData)
{
	if (isInterruptBuff)
	{
		doInterruptHit(receiver, buffData);
	} else {
		isInterruptBuff = true;
	}
}

void UBuff::doLoop(CS3Entity * receiver, UBuffDataType * buffData)
{
	doLoopHit(receiver, buffData);
}

UBuffHitDefine * UBuff::getHit(FString attrName, int32 index)
{
	return nullptr;
}

void UBuff::doLoopHit(CS3Entity * receiver, UBuffDataType * buffData)
{
}

void UBuff::doBeginHit(CS3Entity * receiver, UBuffDataType * buffData)
{
}

void UBuff::doEndHit(CS3Entity * receiver, UBuffDataType * buffData)
{
}

void UBuff::doInterruptHit(CS3Entity * receiver, UBuffDataType * buffData)
{

}

void UBuff::doStack(CS3Entity * receiver, UBuffDataType * buffData)
{
}

void UBuff::registerEvent(CS3Entity * receiver, UBuffDataType * buffData)
{
	CS3Entity* caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(buffData->casterID);
	_targetInterruptEvent->registerBuffEvent(buffData, receiver);
	_casterInterruptEvent->registerBuffEvent(buffData, caster, receiver);

	if (_actForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
		if (!IsValid(CSkillInterface))
		{
			CSkillInterface->registerBuffEvent(ENUM_SKILL_EVENT::ActWorldChangeEvent, buffData->index);
		}
	}
}

void UBuff::unRegisterEvent(CS3Entity * receiver, UBuffDataType * buffData)
{
	CS3Entity* caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(buffData->casterID);
	_targetInterruptEvent->unRegisterBuffEvent(buffData, receiver);
	_casterInterruptEvent->unRegisterBuffEvent(buffData, caster, receiver);

	if (_actForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
		if (!IsValid(CSkillInterface))
		{
			CSkillInterface->unRegisterBuffEvent(ENUM_SKILL_EVENT::ActWorldChangeEvent, buffData->index);
		}
	}
}

void UBuff::triggerBuffEvent(CS3Entity * receiver, ENUM_SKILL_EVENT eventType, int32 triggerID, UBuffDataType * buffData, TMap<FString, FVariant> pDict)
{
	if (eventType == ENUM_SKILL_EVENT::ActWorldChangeEvent)
	{
		ACTION_FLAG actWord = ACTION_FLAG::ACTION_FORBID_NONE;
		if (pDict.Contains("actWord"))
		{
			actWord = (ACTION_FLAG)pDict["actWord"].GetValue<int32>();
		}
		bool disabled = true;
		if (pDict.Contains("disabled"))
		{
			disabled = pDict["disabled"].GetValue<bool>();
		}
		if (actWord == _actForbid && disabled)
		{
			UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
			if (!IsValid(CSkillInterface))
			{
				CSkillInterface->removeBuff( buffData->index);
			}
			doInterrupt(receiver, buffData);
		}
	}

	if (_targetInterruptEvent->canTriggerEvent(eventType, pDict))
	{
		if (eventType == ENUM_SKILL_EVENT::InitiaiveStopBuffEvent)
		{
			int32 eventBuffIndex = 0;
			if (pDict.Contains("eventBuffIndex"))
			{
				eventBuffIndex = pDict["eventBuffIndex"].GetValue<int32>();
			}
			if (eventBuffIndex == buffData->index)
			{
				UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
				if (!IsValid(CSkillInterface))
				{
					CSkillInterface->removeBuff(buffData->index);
				}
				doInterrupt(receiver, buffData);
			}
		}else{
			UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
			if (!IsValid(CSkillInterface))
			{
				CSkillInterface->removeBuff(buffData->index);
			}
			doInterrupt(receiver, buffData);
		}
	}
}

void UBuff::triggerCasterBuffEvent(CS3Entity * receiver, ENUM_SKILL_EVENT eventType, int32 triggerID, UBuffDataType * buffData, TMap<FString, FVariant> pDict)
{

	if (_casterInterruptEvent->canTriggerEvent(eventType, pDict))
	{
		if (eventType == ENUM_SKILL_EVENT::InitiaiveStopBuffEvent)
		{
			int32 eventBuffIndex = 0;
			if (pDict.Contains("eventBuffIndex"))
			{
				eventBuffIndex = pDict["eventBuffIndex"].GetValue<int32>();
			}
			if (eventBuffIndex == buffData->index)
			{
				UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
				if (!IsValid(CSkillInterface))
				{
					CSkillInterface->removeBuff(buffData->index);
				}
				doInterrupt(receiver, buffData);
			}
		}
		else {
			UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
			if (!IsValid(CSkillInterface))
			{
				CSkillInterface->removeBuff(buffData->index);
			}
			doInterrupt(receiver, buffData);
		}
	}
}



UBuffDataType * UBuff::getNewBuffData(CS3Entity * caster, CS3Entity * receiver)
{
	UBuffDataType* newBuffData = NewObject<UBuffDataType>();
	newBuffData->buffID = getID();
	newBuffData->holdTime = getHoldTime();
	newBuffData->endTime = calculateEndTime(newBuffData->holdTime);
	newBuffData->className = _className;
	newBuffData->casterID = caster->ID();
	if (caster->ID() == receiver->ID())
	{
		newBuffData->casterIsSelf = 1;
	}
	return newBuffData;
}

float UBuff::getBuffRemainTime(UBuffDataType * buffData)
{
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	int64 currTime = TimeManager->GetMultipleClientTime();
	float RemainTime = (buffData->endTime - currTime) / (float)TIME_ENLARGE_MULTIPLE;
	return RemainTime;
}

int64 UBuff::calculateEndTime(float holdTime)
{
	if (holdTime < 0.0)
	{
		return 0;
	}
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	int64 currTime = TimeManager->GetMultipleClientTime();
	/*四舍五入保留一位小数*/
	holdTime = round(holdTime * 10) / 10.0;
	int64 EndTime = currTime + (int64)(holdTime * TIME_ENLARGE_MULTIPLE);
	return EndTime;
}

bool UBuff::isTimeout(UBuffDataType * buffData)
{
	if (buffData->holdTime < 0.0)
	{
		return false;
	}
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	int64 currTime = TimeManager->GetMultipleClientTime();
	return (currTime + (int64)(0.1 * TIME_ENLARGE_MULTIPLE)) > buffData->endTime;
}

FString UBuff::getScriptType()
{
	return "buff";
}

int32 UBuff::getID()
{
	return _id;
}

FString UBuff::getBuffName()
{
	return _buffName;
}

ACTION_FLAG UBuff::getActForbid()
{
	return _actForbid;
}

ENUM_BUFF_SAVE_TYPE UBuff::getSaveType()
{
	return _saveType;
}

float UBuff::getHoldTime()
{
	return _holdTime;
}

float UBuff::getLoopTime()
{
	return _loopTime;
}

bool UBuff::isHoldEffect(ENUM_HOLD_EFFECT_TYPE effectName)
{
	return _holdEffectNames.Contains(effectName);
}

CONTROL_COMPILE_OPTIMIZE_END