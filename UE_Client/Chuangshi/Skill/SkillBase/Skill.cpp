#include "Skill.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/SkillManager.h"
#include "Manager/BuffManager.h"
#include "Manager/TimeManager.h"
#include "Skill/EffectLoader.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Interface/StateInterface.h"
#include "Interface/SkillInterface.h"
#include "CS3Base/GameObject.h"

CONTROL_COMPILE_OPTIMIZE_START

USkill::USkill()
{
	_casterRequire = NewObject<URequireDefine>();
	_targetRequire = NewObject<URequireDefine>();
	_casterCondition = NewObject<UObjectCondition>();
	_targetCondition = NewObject<UObjectCondition>();
	_hitData = NewObject<USkillHitData>();
	_interruptEvent = NewObject<UEventDefine>();
	_receiverInterruptEvent = NewObject<UReceiverEventDefine>();
}


USkill::~USkill()
{
}

void USkill::init(FString SkillId, const FSKILL_TABLE_DATA* dictDat)
{
	_id = FSTRING_TO_INT(SkillId);
	_name = dictDat->SkillName;
	_level = dictDat->SkillLevel;
	_targetType = dictDat->TargetType;
	_isTurnToTarget = dictDat->IsTurnToTarget;
	_collisionType = dictDat->CollisionType;
	_casterActForbid = dictDat->CasterActForbid;
	_targetActForbid = dictDat->TargetActForbid;
	_castRangeMax = dictDat->CastRangeMax *100;
	for (auto effectData : dictDat->CasterHoldEffectList)
	{
		UHoldEffect* holdEffect = nullptr;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->EffectLoader))
		{
			holdEffect = UUECS3GameInstance::Instance->EffectLoader->createHoldEffect(effectData, this);
		}
		if (nullptr != holdEffect)
		{
			_holdEffectList.Add(holdEffect);
		}
	}

	for (auto cdata : dictDat->CasterCoolDown)
	{
		_casterCoolDown.Add(cdata.CooldownId, cdata.CoolDownTime);
	}
	for (auto cdata : dictDat->TargetCoolDown)
	{
		_targetCoolDown.Add(cdata.CooldownId, cdata.CoolDownTime);
	}
	if (dictDat->CasterRequireDefine.Num()>0)
	{
		_casterRequire->load(dictDat->CasterRequireDefine);
	}
	if (dictDat->TargetRequireDefine.Num() > 0)
	{
		_targetRequire->load(dictDat->TargetRequireDefine);
	}
	if (dictDat->CasterCondition.Num() > 0)
	{
		_casterCondition->init(dictDat->CasterCondition);
	}
	if (dictDat->TargetCondition.Num() > 0)
	{
		_targetCondition->init(dictDat->TargetCondition);
	}
	_castObject = ObjectDefineNewInstance(_targetType);
	_castObject->init(dictDat);
	_hitData->init(dictDat->HitList, this);
	_interruptEvent->init(dictDat->CasterInterruptSkillEvent);
	if (_targetType != ENUM_CAST_TARGET_TYPE::TargetPosition)
	{
		_receiverInterruptEvent->init(dictDat->TargetInterruptSkillEvent);
	}

	TArray<FString> casterActionInfos = UGolbalBPFunctionLibrary::SplitString(dictDat->CasterCastActionId);
	for (auto i : casterActionInfos)
	{
		TArray<FString> actionInfo = UGolbalBPFunctionLibrary::SplitString(i, false, ":");
		if (actionInfo.Num() > 1)
		{
			_casterActionID.Add(actionInfo[0]);
			_casterActionBeginTime.Add(actionInfo[1]);
		}else{
			_casterActionID.Add(actionInfo[0]);
			_casterActionBeginTime.Add("0.0");
		}
	}

	TArray<FString> targetActionInfos = UGolbalBPFunctionLibrary::SplitString(dictDat->TargetCastActionId);
	for (auto i : targetActionInfos)
	{
		TArray<FString> actionInfo = UGolbalBPFunctionLibrary::SplitString(i, false, ":");
		if (actionInfo.Num() > 1)
		{
			_targetActionID.Add(actionInfo[0]);
			_targetActionBeginTime.Add(actionInfo[1]);
		}else{
			_targetActionID.Add(actionInfo[0]);
			_targetActionBeginTime.Add("0.0");
		}
	}

	//标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）
	if (dictDat->Param5 != "")
	{
		TArray<FString> Param5 = UGolbalBPFunctionLibrary::SplitString(dictDat->Param5);
		for (auto i : Param5)
		{
			TArray<FString> List = UGolbalBPFunctionLibrary::SplitString(i, false, TEXT(":"));
			if (List[0] == "IsReTPRandom")
			{
				_reTargetRadius = FSTRING_TO_FLOAT(List[1]);
			}
		}
	}
}


int32 USkill::useableCheck(CS3Entity* caster, USkillTargetObjImpl* target)
{
	/*未完待续*/

	//施法者是否有禁止标记
	if (_casterActForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		UStateInterface * StateInterface = ((GameObject*)caster)->Interface_Cache.StateInterface;
		if (IsValid(StateInterface) && StateInterface->IsActionForbid(_casterActForbid))
		{
			return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
		}
	}

	//技能目标是否有禁止标记
	if (_targetActForbid != ACTION_FLAG::ACTION_FORBID_NONE && target->getType()== SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_ENTITY)
	{
		UStateInterface * StateInterface = ((GameObject*)target->getObject())->Interface_Cache.StateInterface;
		if (IsValid(StateInterface) && StateInterface->IsActionForbid(_targetActForbid))
		{
			return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
		}

	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));

	//检测当前是否正在释放技能
	if (IsValid(CSkillInterface) && CSkillInterface->isCastingSkill())
	{
		return (int32)SKILL_MESSAGE::SKILL_IS_CASTING;
	}
	//检查技能cooldown
	if (isCasterCooldown(caster))
	{
		return (int32)SKILL_MESSAGE::SKILL_NOT_READY;
	}

	//检查技能cooldown
	if (target->getType() == SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_ENTITY)
	{
		if (isTargetCooldown(target))
		{
			return (int32)SKILL_MESSAGE::SKILL_TARGET_NOT_READY;
		}
	}

	//施法需求检查
	int state = checkCasterRequire(caster);
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		return state;
	}

	//施法目标需求检查
	//if (target->getType() == SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_ENTITY)
	//{
	///	state = checkTargetRequire(target);
	//	if ( state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	//	{
	//		return state;
	//	}
	//}

	//施法者检查
	state = castValidCheck(caster, caster);
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		return state;
	}

	//施法目标检查
	state = targetValidCheck(caster, target);
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		return state;
	}

	//检查目标是否符合法术施展
	state = getCastObject()->CastValid(caster, target);
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		return state;
	}
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

int32 USkill::useSkill(CS3Entity * caster, USkillTargetObjImpl * target)
{
	/*未完待续*/
	target = adaptiveTarget(caster, target);
	if (target == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_FAILED;
	}
	int32 state = useableCheck(caster, target);
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		return state;
	}
	use(caster, target);
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

void USkill::use(CS3Entity * caster, USkillTargetObjImpl * target)
{
	if (_isTurnToTarget)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->turnToSkillTarget(target);
		}
	}
	cast(caster, target);
}

void USkill::cast(CS3Entity * caster, USkillTargetObjImpl * target)
{
	if (!caster)
	{
		return;
	}
	if (!target)
	{
		return;
	}
	registerSkillEvent(caster, target);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}

	if (_casterCoolDown.Num() > 0)
	{	
		CSkillInterface->setCooldown(_casterCoolDown);
	}

	// 处理消耗
	doCasterRequire(caster);

	//通知客户端释放技能，播放动作等
	int32 ActionIndex = 0;
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->setActionIndex();
		ActionIndex = CSkillInterface->getActionIndex();
	}
	USkillInterface *SkillInterface = ((GameObject*)caster)->Interface_Cache.SkillInterface;
	if (_targetType == ENUM_CAST_TARGET_TYPE::TargetPosition)
	{
		FVector position = target->getObjectPosition();
		if (_reTargetRadius > 0.0)
		{
			position = getPositionByCircular(position, _reTargetRadius);
		}
		if (IsValid(SkillInterface))
		{
			SkillInterface->CastSkillToPosition(_id, int(isInstantSkill()), position.X, position.Y, position.Z, _casterActionID, _casterActionBeginTime, ActionIndex, caster->ID());
		}
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->BroadcastCSkillToPosition(_id, int(isInstantSkill()), position.X, position.Y, position.Z, _casterActionID, _casterActionBeginTime, ActionIndex, caster->ID());
		}
	}else{
		if (IsValid(SkillInterface))
		{
			SkillInterface->CastSkillToTarget(_id, int(isInstantSkill()), target->getObject()->ID(), _casterActionID, _casterActionBeginTime, ActionIndex, caster->ID());
		}
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->BroadcastCSkillToTarget(_id, int(isInstantSkill()), target->getObject()->ID(), _casterActionID, _casterActionBeginTime, ActionIndex, caster->ID());
		}
	}
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->setSkillActionIndex(getID(), ActionIndex);
	}

	onSkillBegin(caster, target);
}

void USkill::onSkillBegin(CS3Entity * caster, USkillTargetObjImpl * target)
{
	/*未完待续*/
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->onSkillBegin(this, target);
	}
	target->onSkillBegin(caster);
	bool isHit = true;
	addHoldEffect(caster);

	if (IsValid(CSkillInterface))
	{
		CSkillInterface->triggerEventSkillBegin(this);
	}

	if (IsValid(CSkillInterface) && CSkillInterface->IsInterruptSkill(getID()))
	{
		CSkillInterface->interruptSkill((int32)SKILL_MESSAGE::SKILL_CAST_FAILED);
		isHit = false;
	}

	if (IsValid(CSkillInterface))
	{
		CSkillInterface->setIsInterruptSkill(getID(), true);
	}

	if (isHit)
	{
		_hitData->begin(this, caster, target);
	}
}

void USkill::onSkillHit(INT32 casterID, USkillTargetObjImpl * target, int32 hitTime)
{
	CS3Entity * caster = (CS3Entity *)UGolbalBPFunctionLibrary::FindEntity(casterID);
	if (caster)
	{
		_hitData->onHit(this, caster, target, hitTime);
	}
	
}

void USkill::onArrive(CS3Entity * caster, USkillTargetObjImpl * target, int32 hitTime, int32 index)
{
	_hitData->onHitArrive(this, caster, target, hitTime, index);
}

void USkill::addHoldEffect(CS3Entity * caster )
{
	for (int32 i = 0; i < _holdEffectList.Num(); ++i)
	{
		if (_holdEffectList[i]->canEffect(caster, caster))
		{
			UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
			UHoldEffectDataType * effectData = _holdEffectList[i]->getNewEffectData(caster, caster);
			effectData->index = CSkillInterface->getNewHoldEffectIndex();
			effectData->sourceType = HOLD_EFFECT_SOURCE_TYPE::HOLD_EFFECT_SOURCE_TYPE_SKILL;
			effectData->sourceID = getID();
			effectData->configIndex = i;
			effectData->casterID = caster->ID();
			CSkillInterface->addHoldEffectData(effectData);
			_holdEffectList[i]->onBegin(effectData, caster);
		}
	}
}

void USkill::onSkillEnd(CS3Entity * caster, USkillTargetObjImpl * target, bool castResult)
{
	/*未完待续*/
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->onSkillEnd(this, castResult);
		CSkillInterface->setIsInterruptSkill(getID(), false);
	}
	removeHoldEffect(caster);
	unRegisterSkillEvent(caster);
	if (target != nullptr)
	{
		target->RemoveFromRoot();
	}
}

void USkill::removeHoldEffect(CS3Entity * caster)
{
	TArray<UHoldEffectDataType *> holdEffectDatas;
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		holdEffectDatas = CSkillInterface->GetHoldEffectData();
	}
	 
	for (int32 i = 0; i < _holdEffectList.Num(); ++i)
	{
		for (auto effectData : holdEffectDatas)
		{
			if (effectData->sourceType == HOLD_EFFECT_SOURCE_TYPE::HOLD_EFFECT_SOURCE_TYPE_SKILL && effectData->configIndex == i )
			{
				_holdEffectList[i]->onEnd(effectData, caster);
				if (IsValid(CSkillInterface))
				{
					CSkillInterface->removeHoldEffectData(effectData->index);
				}
			}
		}
	}
}

bool USkill::canInterrupt(CS3Entity * caster, int32 reason)
{
	return true;
}

void USkill::interrupt(CS3Entity * caster, int32 reason, USkillTargetObjImpl * target)
{
	/*未完待续*/
	if (!canInterrupt(caster, reason))
	{
		return;
	}
	onSkillEnd(caster, target, false);
	/*处理中断技能动作*/
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	int32 ActionIndex = 0;
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->onSkillInterrupted(getID(), reason);
		ActionIndex = CSkillInterface->getSkillActionIndex(getID());
	}
	USkillInterface *SkillInterface = ((GameObject*)caster)->Interface_Cache.SkillInterface;
	if (IsValid(SkillInterface))
	{
		SkillInterface->SkillInterrupted(getID(), reason, ActionIndex);
	}
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->BroadcastCSkillInterrupted(getID(), reason, ActionIndex);
		CSkillInterface->removeSkillActionIndex(getID());
	}
}

void USkill::interruptSkill(CS3Entity * caster, int32 reason)
{
	/*未完待续*/
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		if (CSkillInterface->IsInterruptInstantSkill(getID()))
		{
			CSkillInterface->interruptSkill(reason);
		}else{
			CSkillInterface->setIsInterruptInstantSkill(getID(), true);
		}
	}

}

void USkill::registerSkillEvent(CS3Entity * caster, USkillTargetObjImpl * target)
{
	_interruptEvent->registerEvent(this, caster);
	_receiverInterruptEvent->registerEvent(this, caster, target);
	if (_casterActForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->registerSkillEvent(ENUM_SKILL_EVENT::ActWorldChangeEvent, getID());
		}
	}
}

void USkill::unRegisterSkillEvent(CS3Entity * caster)
{
	_interruptEvent->unRegisterEvent(this, caster);
	if (_casterActForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->unRegisterSkillEvent(ENUM_SKILL_EVENT::ActWorldChangeEvent, getID());
		}
	}
}

void USkill::triggerSkillEvent(CS3Entity * caster, ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict)
{
	int32 castingSkillID = 0;
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));

	if (IsValid(CSkillInterface))
	{
		castingSkillID = CSkillInterface->getCastingSkill();
	}

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
		if (actWord == _casterActForbid && disabled && castingSkillID == getID())
		{
			interruptSkill(caster, (int32)SKILL_MESSAGE::SKILL_CAST_FAILED);
		}
	}
	if (_interruptEvent->canTriggerEvent(eventType, pDict) && castingSkillID == getID())
	{
		interruptSkill(caster, (int32)SKILL_MESSAGE::SKILL_CAST_FAILED);
	}
}

void USkill::triggerReceiverSkillEvent(CS3Entity * caster, CS3Entity * receiver, ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		int32 castingSkillID = CSkillInterface->getCastingSkill();
		if (_receiverInterruptEvent->canTriggerEvent(eventType, pDict) && castingSkillID == getID())
		{
			CSkillInterface->interruptSkill((int32)SKILL_MESSAGE::SKILL_CAST_FAILED);
		}
	}
}

int32 USkill::castValidCheck(CS3Entity * caster, CS3Entity * target)
{
	return _casterCondition->valid(caster, target, true);
}

int32 USkill::targetValidCheck(CS3Entity * caster, USkillTargetObjImpl * target)
{
	if (target->getType() == SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_POSITION && _targetCondition->isHasConditions())
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	return _targetCondition->valid(caster, target->getObject(), false);
}

bool USkill::isInstantSkill()
{
	return false;
}

bool USkill::isPassiveSkill()
{
	return _isPassiveSkill;
}

bool USkill::isCasterCooldown(CS3Entity * caster)
{
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	int64 currTime = TimeManager->GetMultipleClientTime();
	TArray<FSKILL_UPDATE_COOL_DOWN> CoolDowns;
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CoolDowns = CSkillInterface->getCooldown();
	}
	for (auto i : _casterCoolDown)
	{
		for (auto CoolDown: CoolDowns)
		{
			if (CoolDown.CooldownId == i.Key && (CoolDown.EndTime - currTime) > int64(0.1 * TIME_ENLARGE_MULTIPLE))
			{
				return true;
			}
		}
	}
	return false;
}

bool USkill::isTargetCooldown(USkillTargetObjImpl * target)
{
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	int64 currTime = TimeManager->GetMultipleClientTime();
	TArray<FSKILL_UPDATE_COOL_DOWN> CoolDowns;
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), target->getObject()->ID()));
	if (IsValid(CSkillInterface))
	{
		CoolDowns = CSkillInterface->getCooldown();
	}
	for (auto i : _casterCoolDown)
	{
		for (auto CoolDown : CoolDowns)
		{
			if (CoolDown.CooldownId == i.Key && (CoolDown.EndTime - currTime) > int64(0.1 * TIME_ENLARGE_MULTIPLE))
			{
				return true;
			}
		}
	}
	return false;
}

int32 USkill::checkCasterRequire(CS3Entity * caster)
{
	return _casterRequire->validObject(caster, this);
}

int32 USkill::checkTargetRequire(USkillTargetObjImpl * target)
{
	return _targetRequire->validObject(target->getObject(), this);
}

void USkill::doCasterRequire(CS3Entity * caster)
{
	_casterRequire->pay(caster, this);
}

void USkill::doTargetRequire(USkillTargetObjImpl * target)
{

}

ENUM_CAST_TARGET_TYPE USkill::getTargetType()
{
	return _targetType;
}

UTargetBase * USkill::getCastObject()
{
	return _castObject;
}

int32 USkill::getID()
{
	return _id;
}

ACTION_FLAG USkill::getCasterActForbid()
{
	return _casterActForbid;
}

USkillHitDefine * USkill::getHit(int32 hitTime, int32 index)
{

	return _hitData->getHit(hitTime, index);
}

float USkill::getCastRangeMax()
{
	return _castRangeMax;
}

float USkill::getSkillTotalTime()
{
	return _hitData->getTotalTime();
}

USkillTargetObjImpl * USkill::adaptiveTarget(CS3Entity * caster, USkillTargetObjImpl * target)
{
	if (_targetType == ENUM_CAST_TARGET_TYPE::TargetLock && target->getType() == SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_POSITION)
	{
		return nullptr;
	}
	else if (_targetType == ENUM_CAST_TARGET_TYPE::TargetPosition &&target->getType() == SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_ENTITY)
	{
		USkillTargetObjPosition* instance = NewObject<USkillTargetObjPosition>();
		instance->init(target->getObjectPosition());
		USkillTargetObjImpl* tempinstance = (USkillTargetObjImpl*)instance;
		tempinstance->AddToRoot();
		target->RemoveFromRoot();
		return tempinstance;
	}
	else if (_targetType == ENUM_CAST_TARGET_TYPE::TargetNothing)
	{
		USkillTargetObjEntity* instance = NewObject<USkillTargetObjEntity>();
		instance->init(caster);
		USkillTargetObjImpl* tempinstance = (USkillTargetObjImpl*)instance;
		tempinstance->AddToRoot();
		target->RemoveFromRoot();
		return tempinstance;
	}
	return target;
}

FString USkill::getScriptType()
{
	return "skill";
}

FVector USkill::getPositionByCircular(FVector pos, float radius)
{
	int32 temp = (int32)(radius * 100);
	int32 MulRradius = rand() % temp;
	int32 RAngle = rand() % 360;
	float Rradian = RAngle * PI / 180;
	FVector dstPos = FVector(pos.X + MulRradius * FMath::Cos(Rradian), pos.Y + MulRradius * FMath::Sin(Rradian), pos.Z);
	return dstPos;
}

CONTROL_COMPILE_OPTIMIZE_END