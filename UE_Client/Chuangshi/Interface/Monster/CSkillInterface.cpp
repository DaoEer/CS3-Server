// Fill out your copyright notice in the Description page of Project Settings.


#include "CSkillInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/GameDeFine.h"
#include "Interface/SkillInterface.h"
#include "Interface/GameObjectInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/TimeManager.h"
#include "Manager/MessageManager.h"
#include "Manager/BuffManager.h"
#include "SKill/SkillBase/Skill.h"
#include "SKill/SkillBase/Buff.h"
#include "Skill//SkillLoader.h"
#include "Skill/BuffLoader.h"
#include "Skill/EffectLoader.h"
#include "Skill/SkillBase/HitDefine.h"
#include "CS3Base/GameObject.h"
#include "Util/GlobalFunctions.h"
#include "BehaviourInterface.h"
#include "Entity/Monster/CMonster.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(UCSkillInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UCSkillInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UCSkillInterface::UCSkillInterface()
{
}

void UCSkillInterface::BeginDestroy()
{
	removeAllBuff();
	interruptSkill((int32)SKILL_MESSAGE::SKILL_CANT_CAST);
	Super::BeginDestroy();
}

void UCSkillInterface::RequestUseCSkillToEntity(int32 skillID, int32 targetID)
{
	int32 Message;
	Message = useCSkillToEntity(skillID, targetID);

	if (Message != (int32)SKILL_MESSAGE::SKILL_GO_ON && GetEntity()->IsPlayer())
	{
		UMessageManager* MessageManager = UUECS3GameInstance::Instance->MessageManager;
		MessageManager->ShowMessage(Message);

	}
}

void UCSkillInterface::RequestUseCSkillToPosition(int32 skillID, FVector position)
{
	int32 Message;
	Message = useCSkillToPosition(skillID, position);
	if (Message != (int32)SKILL_MESSAGE::SKILL_GO_ON && GetEntity()->IsPlayer())
	{
		UMessageManager* MessageManager = UUECS3GameInstance::Instance->MessageManager;
		MessageManager->ShowMessage(Message);

	}

}

int32 UCSkillInterface::useCSkillToEntity(int32 skillID, int32 targetID)
{
	int32 Message;
	int32 TargetID = targetID;
	USkill* skill = NULL;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillLoader))
	{
		skill = UUECS3GameInstance::Instance->SkillLoader->getSkillByID(skillID);
	}
	
	if (skill == nullptr || GetEntity()== nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_NOT_EXIST;
	}
	if (skill->getTargetType() == ENUM_CAST_TARGET_TYPE::TargetNothing)
	{
		TargetID = GetEntity()->ID();
	}

	CS3Entity* target= (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(TargetID);
	CS3Entity* caster = (CS3Entity*)GetEntity();
	if (!target || !caster)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	USkillTargetObjEntity* instance = NewObject<USkillTargetObjEntity>();
	instance->init(target);
	USkillTargetObjImpl* tempinstance = (USkillTargetObjImpl*)instance;
	tempinstance->AddToRoot();
	Message = skill->useSkill(caster, tempinstance);
	return Message;
}

int32 UCSkillInterface::useCSkillToPosition(int32 skillID, FVector position)
{
	USkill* skill = NULL;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillLoader))
	{
		skill = UUECS3GameInstance::Instance->SkillLoader->getSkillByID(skillID);
	}
	if (skill == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_NOT_EXIST;
	}
	USkillTargetObjPosition* instance = NewObject<USkillTargetObjPosition>();
	instance->init(position);
	USkillTargetObjImpl* tempinstance = (USkillTargetObjImpl*)instance;
	tempinstance->AddToRoot();
	return skill->useSkill((CS3Entity*)GetEntity(), tempinstance);
}

void UCSkillInterface::onSkillBegin(USkill * skill, USkillTargetObjImpl * target)
{
	if (!skill->isInstantSkill())
	{
		castingSkillID = skill->getID();
		USkillInterface *SkillInterface = ((GameObject*)GetEntity())->Interface_Cache.SkillInterface;
		if (IsValid(SkillInterface))
		{
			SkillInterface->SetCastingSkill(castingSkillID);
		}
	}
}

void UCSkillInterface::onSkillEnd( USkill * skill, bool castResult)
{
	triggerEventSkillEnd(skill);
	if (!skill->isInstantSkill())
	{
		castingSkillID = 0;
	}
	casterSkillEnd(skill);
	delSkillHitTimer(skill->getID());
	UBehaviourInterface *behInt = CS3::GetInterface< UBehaviourInterface >(EntityID);
	if (IsValid(behInt))
	{
		behInt->BehClientSpellOver(skill->getID());
	}

	if (GetEntity()->GetDefinedProperty(TEXT("entityFlagExt")).GetValue<uint8>() == uint8(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
		CMonster* pCMonster = (CMonster*)GetEntity();
		if (pCMonster)
		{
			pCMonster->onSkillEnd(skill, castResult);
		}
	}
}

void UCSkillInterface::triggerEventSkillBegin(USkill * skill)
{
	if (!skill->isPassiveSkill())
	{
		TMap<FString, FVariant> pDict;
		pDict.Add("actForbid", FVariant((int32)skill->getCasterActForbid()));
		pDict.Add("type", FVariant(1));
		pDict.Add("skillID", FVariant(skill->getID()));
		triggerSkillEvent(ENUM_SKILL_EVENT::SkillProcessEvent, GetEntity()->ID(), pDict);
	}
}

void UCSkillInterface::triggerEventSkillEnd(USkill * skill)
{
	if (!skill->isPassiveSkill())
	{
		TMap<FString, FVariant> pDict;
		pDict.Add("actForbid", FVariant((int32)skill->getCasterActForbid()));
		pDict.Add("type", FVariant(0));
		pDict.Add("skillID", FVariant(skill->getID()));
		triggerSkillEvent(ENUM_SKILL_EVENT::SkillProcessEvent, GetEntity()->ID(), pDict);
	}
}

void UCSkillInterface::interruptSkill(int32 reason)
{
	if (!isCastingSkill())
	{
		return;
	}
	USkill* skill = NULL;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillLoader))
	{
		skill = UUECS3GameInstance::Instance->SkillLoader->getSkillByID(castingSkillID);
	}
	if (skill == nullptr || GetEntity() == nullptr)
	{
		return;
	}
	skill->interrupt((CS3Entity*)GetEntity(), reason);
}

void UCSkillInterface::onSkillInterrupted(int32 skillID, int32 reason)
{
}

void UCSkillInterface::interruptInstantSkill(USkill * skill, int32 reason)
{
	skill->interrupt((CS3Entity*)GetEntity(), reason);
}

void UCSkillInterface::setReceiverID(int32 id)
{
	receiverID = id;
}

void UCSkillInterface::casterSkillEnd(USkill * skill)
{
	if (receiverID != 0)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiverID));
		if (IsValid(CSkillInterface))
		{
			
			CSkillInterface->onCasterSkillEnd(GetEntity()->ID(), skill->getID());
		}
		receiverID = 0;
	}
}

void UCSkillInterface::onCasterSkillEnd(int32 casterID, int32 skillID)
{
}

void UCSkillInterface::setIsInterruptSkill(int32 skillID, bool value)
{
	isInterruptSkill.Add(skillID, value);
}

bool UCSkillInterface::IsInterruptSkill(int32 skillID)
{
	if (isInterruptSkill.Contains(skillID))
	{
		return isInterruptSkill[skillID];
	}
	return false;
}

void UCSkillInterface::setIsInterruptInstantSkill(int32 skillID, bool value)
{
	isInterruptInstantSkill.Add(skillID, value);
}

bool UCSkillInterface::IsInterruptInstantSkill(int32 skillID)
{
	if (isInterruptInstantSkill.Contains(skillID))
	{
		return isInterruptInstantSkill[skillID];
	}
	return false;
}

bool UCSkillInterface::isCastingSkill()
{
	return castingSkillID != 0;
}

int32 UCSkillInterface::getCastingSkill()
{
	return castingSkillID;
}

void UCSkillInterface::setActionIndex()
{
	// 设置actionIndex范围在 1000001 ~ 3000000
	if (actionIndex < 1000001 || actionIndex > 3000000)
	{
		actionIndex = 1000000;
	}
	actionIndex += 1;
}

int32 UCSkillInterface::getActionIndex()
{
	return actionIndex;
}

void UCSkillInterface::setSkillActionIndex(int32 skillID, int32 ActionIndex)
{
	skillActionIndex.Add(skillID, ActionIndex);
}

int32 UCSkillInterface::getSkillActionIndex(int32 skillID)
{
	if (skillActionIndex.Contains(skillID))
	{
		skillActionIndex[skillID];
	}
	return 0;
}

void UCSkillInterface::removeSkillActionIndex(int32 skillID)
{
	if (skillActionIndex.Contains(skillID))
	{
		skillActionIndex.Remove(skillID);
	}
}

void UCSkillInterface::intonateSpell(float intonateTime, int32 skillID)
{
	UGameObjectInterface * Interface = ((GameObject*)GetEntity())->Interface_Cache.GameObjectInterface;
	if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		USkillInterface *SkillInterface = ((GameObject*)GetEntity())->Interface_Cache.SkillInterface;
		if (IsValid(SkillInterface))
		{
			SkillInterface->intonateSpell(intonateTime, skillID);
		}
	}
}

void UCSkillInterface::intonateSpellOver()
{
	UGameObjectInterface * Interface = ((GameObject*)GetEntity())->Interface_Cache.GameObjectInterface;
	if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		USkillInterface *SkillInterface = ((GameObject*)GetEntity())->Interface_Cache.SkillInterface;
		if (IsValid(SkillInterface))
		{
			SkillInterface->intonateSpellOver();
		}
	}
}

void UCSkillInterface::turnToSkillTarget(USkillTargetObjImpl * target)
{
	FVector TPosition = target->getObjectPosition();
	USkillInterface *SkillInterface = ((GameObject*)GetEntity())->Interface_Cache.SkillInterface;
	if (IsValid(SkillInterface))
	{
		SkillInterface->SkillTurnToPos(TPosition);
	}
	
}

void UCSkillInterface::CSkill_onClientActorCreate()
{
	KBEngine::Entity* entity = GetEntity();
	if (nullptr == entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkill_onClientActorCreate : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	entity->CellCall(TEXT("cSkill_onClientActorCreate"), Args);
}


UBuffDataType * UCSkillInterface::getBuffData(int32 index)
{
	if (attrBuffs.Contains(index))
	{
		return attrBuffs[index];
	}
	return nullptr;
}

UBuff * UCSkillInterface::getBuff(int32 buffID)
{
	UBuff* buff = nullptr;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->BuffLoader))
	{
		buff = UUECS3GameInstance::Instance->BuffLoader->getBuffByID(buffID);
	}
	return buff;
}

bool UCSkillInterface::addBuff(CS3Entity * caster, int32 buffID)
{
	UBuff* buff = getBuff(buffID);
	if (nullptr == buff)
	{
		AddSeverBuff(caster, buffID);
		return true;
	}
	if (nullptr == GetEntity())
	{
		return false;
	}
	if (buff->receive(caster, (CS3Entity*)GetEntity()))
	{
		return true;
	}
	return false;
}

void UCSkillInterface::AddSeverBuff(CS3Entity * caster, int32 buffID)
{
	KBEngine::Entity* entity = GetEntity();
	if (nullptr == entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::AddSeverBuff : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(caster->ID());
	Args.Add(buffID);
	entity->CellCall(TEXT("cSkillAddSeverBuff"), Args);
}

void UCSkillInterface::onAddBuff(UBuffDataType * buffData)
{
	UBuff* buff = getBuff(buffData->buffID);
	if (nullptr == buff)
	{
		CS3_Warning(TEXT("buffID = %d is not in config:"), buffData->buffID);
		return;
	}
	buffData->index = newBuffIndex();
	attrBuffs.Add(buffData->index, buffData);
	SynClientAddBuff(buffData);
	buff->doBegin((CS3Entity*)GetEntity(), buffData);
	if (buffData->holdTime != 0.0)
	{
		buffHoldTimerRefresh();
	} else {
		if (attrBuffs.Contains(buffData->index))
		{
			removeBuff(buffData->index, BUFF_END_RESON::BUFF_END_RESON_BY_TIME_OVER);
		}
	}
}

void UCSkillInterface::reloadBuff(int32 buffIndex, BUFF_END_RESON reason)
{
	UBuffDataType * buffData = getBuffData(buffIndex);
	UBuff* buff = getBuff(buffData->buffID);
	buff->doReload((CS3Entity*)GetEntity(), buffData);
	buffHoldTimerRefresh();
}

void UCSkillInterface::stopBuff(UBuffDataType * buffData, BUFF_END_RESON reason)
{
	UBuff* buff = getBuff(buffData->buffID);
	if (GetEntity() != nullptr)
	{
		buff->doEnd((CS3Entity*)GetEntity(), buffData, reason);
	}
}

void UCSkillInterface::clearBuff(UBuffDataType * buffData, BUFF_END_RESON reason)
{
	if (reason != BUFF_END_RESON::BUFF_END_RESON_BY_OFFLINE)
	{
		attrBuffs.Remove(buffData->index);
	}

	if (removeBuffList.Contains(buffData->index))
	{
		removeBuffList.Remove(buffData->index);
	}
	SynClientRemoveBuff(buffData->index);
}

int32 UCSkillInterface::newBuffIndex()
{
	///lastBuffIndex客户端的范围是1000001~2000000， 服务器的lastBuffIndex范围是0~1000000
	if (lastBuffIndex < 1000001 || lastBuffIndex>2000000)
	{
		lastBuffIndex = 1000001;
	}
	int32 index = lastBuffIndex;
	lastBuffIndex += 1;
	return index;
}

void UCSkillInterface::notifyClientAddBuff(UBuffDataType * buffData, float buffHoldTime, float buffRemainTime)
{
	BroadcastAddBuff(buffData->index, buffData->buffID, buffData->className, buffData->casterID, buffHoldTime, INT64_TO_FSTRING(buffData->endTime), buffData->layer);
}

void UCSkillInterface::notifyClientRemoveBuff(UBuffDataType * buffData)
{
	BroadcastRemoveBuff(buffData->index);
}

void UCSkillInterface::removeAllBuff()
{
	TArray<int32> buffIndexs;
	attrBuffs.GetKeys(buffIndexs);
	for (auto buffIndex : buffIndexs)
	{
		UBuffDataType * buffData = getBuffData(buffIndex);
		stopBuff(buffData);
	}
	buffHoldTimerRefresh();
}

bool UCSkillInterface::removeBuff(int32 buffIndex, BUFF_END_RESON reason)
{
	UBuffDataType * buffData = getBuffData(buffIndex);
	if (nullptr == buffData)
	{
		buffHoldTimerRefresh();
		return false;
	}
	stopBuff(buffData, reason);
	notifyClientRemoveBuff(buffData);
	buffHoldTimerRefresh();

	/*attrBuff数据同步到服务器*/
	

	return true;
}

void UCSkillInterface::timeOverEndBuff(int32 buffIndex)
{
	removeBuffByIndex(buffIndex, BUFF_END_RESON::BUFF_END_RESON_BY_TIME_OVER);
}

bool UCSkillInterface::removeBuffByID(int32 buffID, BUFF_END_RESON reason)
{
	bool isSucceed = true;
	TArray<UBuffDataType*> buffList;
	for (auto i : attrBuffs)
	{
		if (i.Value && i.Value->buffID == buffID)
		{
			buffList.Add(i.Value);
		}
	}

	if (buffList.Num() <= 0)
	{
		isSucceed = false;
	}

	for (auto buffData : buffList)
	{
		if (buffData->buffID == buffID)
		{
			if (!removeBuff(buffData->index, reason))
			{
				isSucceed = false;
			}
		}
	}
	return isSucceed;
}

bool UCSkillInterface::removeBuffByIndex(int32 buffIndex, BUFF_END_RESON reason)
{
	bool isSucceed = false;
	if (attrBuffs.Contains(buffIndex))
	{
		if (removeBuff(buffIndex, reason))
		{
			isSucceed = true;
		}
	}
	return isSucceed;
}

void UCSkillInterface::removeBuffByEffect(ENUM_HOLD_EFFECT_TYPE holdEffectName)
{
	TArray<int32> buffIndexs;
	attrBuffs.GetKeys(buffIndexs);
	for (auto index : buffIndexs)
	{
		UBuff* buff = getBuff(getBuffData(index)->buffID);
		if (buff->isHoldEffect(holdEffectName))
		{
			removeBuff(index);
		}
	}
}

void UCSkillInterface::triggerEventBuffAdd(UBuff * buff)
{
	TMap<FString, FVariant> pDict;
	pDict.Add("actForbid", FVariant((int32)buff->getActForbid()));
	pDict.Add("type", FVariant(1));
	pDict.Add("buffID", FVariant(buff->getID()));
	triggerSkillEvent(ENUM_SKILL_EVENT::BuffProcessEvent, GetEntity()->ID(), pDict);
}

void UCSkillInterface::triggerEventBuffRemove(UBuff * buff)
{
	TMap<FString, FVariant> pDict;
	pDict.Add("actForbid", FVariant((int32)buff->getActForbid()));
	pDict.Add("type", FVariant(0));
	pDict.Add("buffID", FVariant(buff->getID()));
	triggerSkillEvent(ENUM_SKILL_EVENT::BuffProcessEvent, GetEntity()->ID(), pDict);
}

void UCSkillInterface::receiveBuffHit(int32 casterID, int32 buffID, FString attrName, int32 index)
{
	CS3Entity* caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(casterID);
	UBuff* buff = getBuff(buffID);
	if (nullptr != buff && nullptr != caster)
	{
		UBuffHitDefine * hit = buff->getHit(attrName, index);
		if (nullptr != hit)
		{
			hit->receive(buff, caster, (CS3Entity*)GetEntity());
		}
	}
}

TArray<int32> UCSkillInterface::findBuffsByBuffID(int32 buffID)
{
	TArray<int32> buffs;
	for (auto i : attrBuffs)
	{
		if (i.Value->buffID == buffID)
		{
			buffs.Add(i.Key);
		}
	}
	return buffs;
}

TArray<int32> UCSkillInterface::findBuffsByBuffScript(FString buffScript)
{
	TArray<int32> buffs;
	for (auto i : attrBuffs)
	{
		if (i.Value->className == buffScript)
		{
			buffs.Add(i.Key);
		}
	}
	return buffs;
}

TMap<int32, UBuffDataType*> UCSkillInterface::getAttrBuffs()
{
	return attrBuffs;
}

void UCSkillInterface::SynClientAddBuff(UBuffDataType* buffData)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::SynClientAddBuff : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(buffData->index);
	Args.Add(buffData->buffID);
	Args.Add(buffData->holdTime);
	Args.Add(buffData->endTime);
	Args.Add(buffData->casterID);
	Args.Add(buffData->casterIsSelf);
	Args.Add(buffData->layer);
	Args.Add(buffData->className);
	entity->CellCall(TEXT("synClientAddBuff"), Args);
	
}

void UCSkillInterface::SynClientRemoveBuff(int32 buffIndex)
{
	KBEngine::Entity* entity = GetEntity();
	if (nullptr == entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::SynClientRemoveBuff : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(buffIndex);
	entity->CellCall(TEXT("synClientRemoveBuff"), Args);
}



void UCSkillInterface::buffHoldTimerRefresh()
{
	if (attrBuffs.Num() == 0)
	{
		cacheBuff.Empty();
		nextBuffEndTickValue = 0;
		return;
	}
	TArray<UBuffDataType*> buffList;
	for (auto i : attrBuffs)
	{
		if (i.Value->endTime > 0 && !removeBuffList.Contains(i.Value->index))
		{
			buffList.Add(i.Value);
		}
	}
	buffList.Sort([](UBuffDataType& buffData1, UBuffDataType& buffData2)
	{
		return buffData1.endTime < buffData2.endTime;
	});
	
	cacheBuff.Empty();
	for (auto i : buffList)
	{
		cacheBuff.Add(i);
	}

	if (buffList.Num() > 0)
	{
		nextBuffEndTickValue = buffList[0]->endTime;
	} else {
		nextBuffEndTickValue = 0;
	}
	if (nextBuffEndTickValue != 0)
	{
		addBuffHoldTick();
	}
}

void UCSkillInterface::addBuffHoldTick()
{
	if (buffHoldTickTimerID.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(buffHoldTickTimerID);
	}
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	int64 currTime = TimeManager->GetMultipleClientTime();
	//保留一位小数
	float nextTime = round(((nextBuffEndTickValue - currTime) * 10) / (float)TIME_ENLARGE_MULTIPLE) / 10.0f;
	if (nextTime > 0.1f)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, buffHoldTickTimerID, FTimerDelegate::CreateLambda([this]()
		{
			onBuffHoldTick();
		}), nextTime, false);
	} else {
		onBuffHoldTick();
	}
}

void UCSkillInterface::onBuffHoldTick()
{
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(buffHoldTickTimerID);
	TArray<UBuffDataType*> tempList;
	for (auto i : cacheBuff)
	{
		tempList.Add(i);
	}

	for (auto buffData : tempList)
	{
		if (buffData->endTime == 0)
		{
			continue;
		}
		if (!attrBuffs.Contains(buffData->index))
		{
			continue;
		}
		if (removeBuffList.Contains(buffData->index))
		{
			continue;
		}
		UBuff* buff = getBuff(buffData->buffID);
		if (buff->isTimeout(buffData))
		{
			removeBuffList.Add(buffData->index);
			timeOverEndBuff(buffData->index);

		}else {
			break;
		}
	}

	///防止定时器被刷新很快的时候，回调时间不对的问题,如果BUFF列表不为空，
	///而已定时器已经停止时，直接再进行一次刷新
	if (attrBuffs.Num() > 0 && !buffHoldTickTimerID.IsValid())
	{
		buffHoldTimerRefresh();
	}
}

void UCSkillInterface::registerSkillEvent(ENUM_SKILL_EVENT eventType, int32 skillID)
{
	if (!casterSkillEventList.Contains(eventType))
	{
		TArray<int32> Temp;
		casterSkillEventList.Add(eventType, Temp);
	}
	casterSkillEventList[eventType].Add(skillID);
}

void UCSkillInterface::unRegisterSkillEvent(ENUM_SKILL_EVENT eventType, int32 skillID)
{
	if (casterSkillEventList.Contains(eventType) && casterSkillEventList[eventType].Contains(skillID))
	{
		casterSkillEventList[eventType].Remove(skillID);
	}
}

void UCSkillInterface::registerReceiverSkillEvent(ENUM_SKILL_EVENT eventType, int32 entityID, int32 skillID)
{
	if (!receiverSkillEventList.Contains(eventType))
	{
		TArray<FINT32_INT32> Temps;
		receiverSkillEventList.Add(eventType, Temps);
	}
	FINT32_INT32 Temp;
	Temp.Num1 = entityID;
	Temp.Num2 = skillID;
	receiverSkillEventList[eventType].Add(Temp);
}

void UCSkillInterface::unRegisterReceiverSkillEvent(ENUM_SKILL_EVENT eventType, int32 entityID, int32 skillID)
{
	FINT32_INT32 Temp;
	Temp.Num1 = entityID;
	Temp.Num2 = skillID;
	for (auto i : receiverSkillEventList)
	{
		for (auto event : i.Value)
		{
			if (event == Temp)
			{
				receiverSkillEventList[eventType].Remove(event);
			}
		}
	}
}

void UCSkillInterface::registerCasterBuffEvent(ENUM_SKILL_EVENT eventType, int32 entityID, int32 index)
{
	if (!casterbuffEventList.Contains(eventType))
	{
		TArray<FINT32_INT32> Temps;
		casterbuffEventList.Add(eventType, Temps);
	}
	FINT32_INT32 Temp;
	Temp.Num1 = entityID;
	Temp.Num2 = index;
	casterbuffEventList[eventType].Add(Temp);
}

void UCSkillInterface::unRegisterCasterBuffEvent(ENUM_SKILL_EVENT eventType, int32 entityID, int32 index)
{
	FINT32_INT32 Temp;
	Temp.Num1 = entityID;
	Temp.Num2 = index;
	for (auto i : casterbuffEventList)
	{
		for (auto event : i.Value)
		{
			if (event == Temp)
			{
				casterbuffEventList[eventType].Remove(event);
			}
		}
	}
}

void UCSkillInterface::registerBuffEvent(ENUM_SKILL_EVENT eventType, int32 index)
{
	if (!receiverbuffEventList.Contains(eventType))
	{
		TArray<int32> Temp;
		receiverbuffEventList.Add(eventType, Temp);
	}
	receiverbuffEventList[eventType].Add(index);
}

void UCSkillInterface::unRegisterBuffEvent(ENUM_SKILL_EVENT eventType, int32 index)
{
	if (receiverbuffEventList.Contains(eventType) && receiverbuffEventList[eventType].Contains(index))
	{
		receiverbuffEventList[eventType].Remove(index);
	}
}

void UCSkillInterface::triggerSkillEvent(ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict)
{
	triggerCasterSkillEventList(eventType, triggerID, pDict);
	triggerReceiverSkillEventList(eventType, triggerID, pDict);
	triggerReceiverBuffEventList(eventType, triggerID, pDict);
	triggerCasterBuffEventList(eventType, triggerID, pDict);
}

void UCSkillInterface::triggerCasterSkillEventList(ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict)
{
	if (!casterSkillEventList.Contains(eventType))
	{
		return;
	}
	TArray<int32> TempList;
	for (auto i : casterSkillEventList[eventType])
	{
		TempList.Add(i);
	}
	for (auto skillID : TempList)
	{
		USkill* skill = NULL;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillLoader))
		{
			skill = UUECS3GameInstance::Instance->SkillLoader->getSkillByID(skillID);
		}
		if (skill == nullptr || GetEntity() == nullptr)
		{
			continue;
		}
		skill->triggerSkillEvent((CS3Entity*)GetEntity(), eventType, triggerID, pDict);
	}

}

void UCSkillInterface::triggerReceiverSkillEventList(ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict)
{
	if (!receiverSkillEventList.Contains(eventType))
	{
		return;
	}
	TArray<FINT32_INT32> TempList;
	for (auto i : receiverSkillEventList[eventType])
	{
		FINT32_INT32 Temp;
		Temp.Num1 = i.Num1;
		Temp.Num2 = i.Num2;
		TempList.Add(Temp);
	}
	for (auto i : TempList)
	{
		CS3Entity* caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(i.Num1);
		USkill* skill = NULL;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillLoader))
		{
			skill = UUECS3GameInstance::Instance->SkillLoader->getSkillByID(i.Num2);
		}
		if (skill == nullptr || GetEntity() == nullptr || caster == nullptr)
		{
			continue;
		}
		skill->triggerReceiverSkillEvent(caster, (CS3Entity*)GetEntity(), eventType, triggerID, pDict);
	}
}

void UCSkillInterface::triggerReceiverBuffEventList(ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict)
{
	if (!receiverbuffEventList.Contains(eventType))
	{
		return;
	}
	TArray<int32> TempList;
	for (auto i : receiverbuffEventList[eventType])
	{
		TempList.Add(i);
	}
	for (auto id : TempList)
	{
		UBuffDataType * buffData = getBuffData(id);
		if (buffData == nullptr || GetEntity() == nullptr)
		{
			continue;
		}
		UBuff* buff = getBuff(buffData->buffID);
		buff->triggerBuffEvent((CS3Entity*)GetEntity(), eventType, triggerID, buffData, pDict);
	}
}

void UCSkillInterface::triggerCasterBuffEventList(ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict)
{
	if (!casterbuffEventList.Contains(eventType))
	{
		return;
	}
	TArray<FINT32_INT32> TempList;
	for (auto i : casterbuffEventList[eventType])
	{
		FINT32_INT32 Temp;
		Temp.Num1 = i.Num1;
		Temp.Num2 = i.Num2;
		TempList.Add(Temp);
	}
	for (auto i : TempList)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), i.Num1));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->triggerCasterBuffEvent(eventType, i.Num2, triggerID, pDict);
		}
	}
}

void UCSkillInterface::triggerCasterBuffEvent(ENUM_SKILL_EVENT eventType, int32 buffIndex, int32 triggerID, TMap<FString, FVariant> pDict)
{
	UBuffDataType * buffData = getBuffData(buffIndex);
	if (buffData == nullptr || GetEntity() == nullptr)
	{
		return;
	}
	UBuff* buff = getBuff(buffData->buffID);
	buff->triggerCasterBuffEvent((CS3Entity*)GetEntity(), eventType, triggerID, buffData, pDict);
}

void UCSkillInterface::stackBuff(int32 buffIndex)
{
	for (auto i : attrBuffs)
	{
		if (i.Value->index != buffIndex)
		{
			continue;
		}
		UBuff* buff = getBuff(i.Value->buffID);
		buff->doStack((CS3Entity*)GetEntity(), i.Value);
	}
}

void UCSkillInterface::resetBuffEndTime(int32 buffIndex)
{
	for (auto i : attrBuffs)
	{
		if (i.Value->index != buffIndex)
		{
			continue;
		}
		UBuff* buff = getBuff(i.Value->buffID);
		i.Value->endTime = buff->calculateEndTime(i.Value->holdTime);
		onResetBuffEndTime(i.Value->index, i.Value->holdTime);
		buffHoldTimerRefresh();
	}
}

void UCSkillInterface::onResetBuffEndTime(int32 buffIndex, float buffTime)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::onResetBuffEndTime : entity!"));
		return;
	};

	KBEngine::FVariantArray Args;
	Args.Add(buffIndex);
	Args.Add(buffTime);
	entity->CellCall(TEXT("broadcastOnResetBuffEndTime"), Args);
}

void UCSkillInterface::receiveDamage(int32 casterID, int32 skillID, int32 damageType, int32 damage, int32 isCritical, int32 isParry, int32 deadEffect, int32 actForbid)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::receiveDamage : entity!"));
		return;
	};

	KBEngine::FVariantArray Args;
	Args.Add(casterID);
	Args.Add(skillID);
	Args.Add(damageType);
	Args.Add(damage);
	Args.Add(isCritical);
	Args.Add(isParry);
	Args.Add(deadEffect);
	Args.Add(actForbid);
	entity->CellCall(TEXT("cReceiveDamage"), Args);
}

void UCSkillInterface::CSkillSetHP(int32 value)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillSetHP : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(value);
	entity->CellCall(TEXT("cSkillSetHP"), Args);
}

void UCSkillInterface::CSkillCreateEntityByScriptID(FString scriptID, FVector position, FVector direction)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillCreateEntityByScriptID : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(scriptID);
	Args.Add(position);
	Args.Add(direction);
	entity->CellCall(TEXT("cSkillCreateEntityByScriptID"), Args);
}

void UCSkillInterface::CSkillGangQiDamage(int32 casterID, int32 skillGangQiValue, float skillGangQiRadio )
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillGangQiDamage : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(casterID);
	Args.Add(skillGangQiValue);
	Args.Add(skillGangQiRadio);
	entity->CellCall(TEXT("cSkillGangQiDamage"), Args);
}

void UCSkillInterface::CSkillAddActCounters(TArray<int32> actList)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillAddActCounters : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;	
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(actList));
	entity->CellCall(TEXT("cSkillAddActCounters"), Args);
}

void UCSkillInterface::CSkillRemoveActCounters(TArray<int32> actList)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillRemoveActCounters : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(actList));
	entity->CellCall(TEXT("cSkillRemoveActCounters"), Args);
}

void UCSkillInterface::CSkillAddEffectState(EFFECT_STATE EffectState)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillAddEffectState : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add((int32)EffectState);
	entity->CellCall(TEXT("cSkillAddEffectState"), Args);
}

void UCSkillInterface::CSkillRemoveEffectState(EFFECT_STATE EffectState)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillRemoveEffectState : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add((int32)EffectState);
	entity->CellCall(TEXT("cSkillRemoveEffectState"), Args);
}

void UCSkillInterface::CSkillEffectAddAttr(TArray<int32> propertiesList, int32 attrPercent, int32 attrValue)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillEffectAddAttr : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(propertiesList));
	Args.Add(attrPercent);
	Args.Add(attrValue);
	entity->CellCall(TEXT("cSkillEffectAddAttr"), Args);
}

void UCSkillInterface::CSkillClientCharge(FVector desPosition, FVector direction, float casterMoveSpeed, bool ischangeDirection)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillClientCharge : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(desPosition);
	Args.Add(direction);
	Args.Add(casterMoveSpeed);
	Args.Add(uint8(ischangeDirection));
	entity->CellCall(TEXT("cSkillClientCharge"), Args);
}

void UCSkillInterface::CSkillClientJump(FVector desPosition, float moveSpeed, float delayTime)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillClientJump : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(desPosition);
	Args.Add(moveSpeed);
	Args.Add(delayTime);
	entity->CellCall(TEXT("cSkillClientJump"), Args);
}

void UCSkillInterface::CSkillStopMove(MOVETYPE type)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillStopMove : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add((int32)type);
	entity->CellCall(TEXT("cSkillStopMove"), Args);
}

void UCSkillInterface::CSkillOnDodgeSkillHit(int32 CasterID)
{
	KBEngine::Entity* entity = GetEntity();
	if (nullptr == entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillOnDodgeSkillHit : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(CasterID);
	entity->CellCall(TEXT("cSkillOnDodgeSkillHit"), Args);
}

void UCSkillInterface::CSkillSetMP(int32 value)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillSetMP : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(value);
	entity->CellCall(TEXT("cSkillSetMP"), Args);
}

void UCSkillInterface::CSkillRecvGangQi(int32 value)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillSetMP : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(value);
	entity->CellCall(TEXT("cSkillRecvGangQi"), Args);
}

void UCSkillInterface::CSkillRequireItem(int32 itemID, int32 amount)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillSetMP : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(itemID);
	Args.Add(amount);
	entity->CellCall(TEXT("cSkillRequireItem"), Args);
}

void UCSkillInterface::setCooldown(TMap<int32, float> cooldownDict)
{
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	int64 currTime = TimeManager->GetMultipleClientTime();

	//清理失效的冷却时间
	TArray<FSKILL_UPDATE_COOL_DOWN> validList;
	for (auto attrCooldown: attrCooldowns)
	{
		if (attrCooldown.EndTime > currTime)
		{
			validList.Add(attrCooldown);
		}
	}
	attrCooldowns.Empty();
	attrCooldowns = validList;
	for (auto i : cooldownDict)
	{
		int64 newEndTime = currTime + int64(TIME_ENLARGE_MULTIPLE * i.Value);
		bool find = false;
		for (auto attrCooldown : attrCooldowns)
		{
			if (attrCooldown.CooldownId == i.Key)
			{
				find = true;
				if (attrCooldown.EndTime < newEndTime)
				{
					attrCooldown.EndTime = newEndTime;
					attrCooldown.PersistTime = i.Value;
				}
			}
		}
		if (!find)
		{
			FSKILL_UPDATE_COOL_DOWN Temp;
			Temp.CooldownId = i.Key;
			Temp.EndTime = newEndTime;
			Temp.PersistTime = i.Value;
			attrCooldowns.Add(Temp);
		}
	}
	updateCooldownToClient(cooldownDict);
}

void UCSkillInterface::changeCooldown(TMap<int32, float> paramDict)
{
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	int64 currTime = TimeManager->GetMultipleClientTime();
	//清理失效的冷却时间
	TArray<FSKILL_UPDATE_COOL_DOWN> validList;
	for (auto attrCooldown : attrCooldowns)
	{
		if (attrCooldown.EndTime > currTime)
		{
			validList.Add(attrCooldown);
		}
	}
	attrCooldowns.Empty();
	attrCooldowns = validList;
	for (auto i : paramDict)
	{
		//增加CD
		if (i.Value > 0.0)
		{
			bool hasCD = false;
			for (auto attrCooldown : attrCooldowns)
			{
				if (attrCooldown.CooldownId == i.Key)
				{
					hasCD = true;
					attrCooldown.EndTime += int64(TIME_ENLARGE_MULTIPLE * i.Value);
					//添加后剩余时间大于持续时间，则重新赋值持续时间
					float remainTime = (attrCooldown.EndTime - currTime) / (float)TIME_ENLARGE_MULTIPLE;
					if (remainTime > attrCooldown.PersistTime)
					{
						attrCooldown.PersistTime = remainTime;
					}
				}
			}
			if (!hasCD)
			{
				FSKILL_UPDATE_COOL_DOWN Temp;
				Temp.CooldownId = i.Key;
				Temp.EndTime = currTime + int64(TIME_ENLARGE_MULTIPLE * i.Value);
				Temp.PersistTime = i.Value;
				attrCooldowns.Add(Temp);
			}
		}
		else
		{
			//增加CD
			for (auto attrCooldown : attrCooldowns)
			{
				if (attrCooldown.CooldownId == i.Key)
				{
					int64 subNewTime = attrCooldown.EndTime - int64(TIME_ENLARGE_MULTIPLE * abs(i.Value));
					attrCooldown.EndTime = subNewTime > currTime ? subNewTime : currTime;
				}
			}
		}
	}
	updateCooldownToClient(paramDict);
}

TArray<FSKILL_UPDATE_COOL_DOWN> UCSkillInterface::getCooldown()
{
	return attrCooldowns;
}

void UCSkillInterface::updateCooldownToClient(TMap<int32, float> cooldownDict)
{
	if (cooldownDict.Num() == 0)
	{
		return;
	}
	TArray<FString> CooldownIDs;
	TArray<FString> EndTimes;
	TArray<FString> PersistTimes;
	for (auto attrCooldown : attrCooldowns)
	{
		if (cooldownDict.Contains(attrCooldown.CooldownId))
		{
			CooldownIDs.Add(INT_TO_FSTRING(attrCooldown.CooldownId));
			EndTimes.Add(INT64_TO_FSTRING(attrCooldown.EndTime));
			PersistTimes.Add(FLOAT_TO_FSTRING(attrCooldown.PersistTime));
		}
	}

	USkillInterface *SkillInterface = ((GameObject*)GetEntity())->Interface_Cache.SkillInterface;
	if (IsValid(SkillInterface))
	{
		SkillInterface->SetCastingSkill(castingSkillID);
	}
}

void UCSkillInterface::addSkillHitTimer(float delayTime, USkill * skill, CS3Entity *caster, USkillTargetObjImpl * target, int32 hitTime)
{
	if (delayTime <= 0.01)
	{
		skill->onSkillHit(caster->ID(), target, hitTime);
	}else {
		FTimerHandle TempTimerHandle;
		INT32 CasterID = caster->ID();
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, TempTimerHandle, FTimerDelegate::CreateLambda([skill, CasterID, target, hitTime]()
		{
			skill->onSkillHit(CasterID, target, hitTime);

		}), delayTime, false);
		if (!SKillHitTimerHandles.Contains(skill->getID()))
		{
			TArray<FTimerHandle> Temp;
			SKillHitTimerHandles.Add(skill->getID(), Temp);
		}
		SKillHitTimerHandles[skill->getID()].Add(TempTimerHandle);
	}
}

void UCSkillInterface::delSkillHitTimer(int32 SKillID)
{
	if (SKillHitTimerHandles.Contains(SKillID))
	{
		TArray<FTimerHandle> timerList = SKillHitTimerHandles[SKillID];
		while (timerList.Num()>0)
		{
			FTimerHandle Temp = timerList.Pop(0);
			if (Temp.IsValid())
			{
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(Temp);
			}	
		}
	}
	
}

int32 UCSkillInterface::receiveSkillHit(CS3Entity * caster, CS3Entity *receiver, int32 skillID, int32 hitTime, int32 Index)
{
	USkill* skill = NULL;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillLoader))
	{
		skill = UUECS3GameInstance::Instance->SkillLoader->getSkillByID(skillID);
	}
	if (!skill)
	{
		return (int32)SKILL_MESSAGE::SKILL_NOT_EXIST;
	}
	USkillHitDefine* skillHitDefine = skill->getHit(hitTime, Index);
	if (skillHitDefine != nullptr)
	{
		skillHitDefine->receive(skill, caster, receiver);
	}
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

int32 UCSkillInterface::getNewHoldEffectIndex()
{
	lastHoldEffectIndex += 1;
	return lastHoldEffectIndex;
}

void UCSkillInterface::addHoldEffectData(UHoldEffectDataType * effectData)
{
	holdEffectData.Add(effectData);
}

void UCSkillInterface::removeHoldEffectData(int32 index)
{
	for (auto effectData : holdEffectData)
	{
		if (effectData->index == index)
		{
			holdEffectData.Remove(effectData);
			break;
		}
	}
}

TArray<UHoldEffectDataType*> UCSkillInterface::GetHoldEffectData()
{
	return holdEffectData;
}

void UCSkillInterface::SetSkillSingTarget(int32 key, USkillTargetObjImpl* value)
{
	SkillSingTarget.Add(key, value);
}

USkillTargetObjImpl* UCSkillInterface::GetSkillSingTarget(int32 key)
{
	if (SkillSingTarget.Contains(key))
	{
		return SkillSingTarget[key];
	}
	return nullptr;
}

void UCSkillInterface::RemoveSkillSingTarget(int32 key)
{
	if (SkillSingTarget.Contains(key))
	{
		SkillSingTarget.Remove(key);
	}
}

void UCSkillInterface::BroadcastCSkillToPosition(int32 SkillID, uint8 isInstantSkill, float PosX, float PosY, float PosZ, TArray<FString> ActionID, TArray<FString> BeginTime, int32 ActionIndex, int32 CasterID)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::BroadcastCSkillToPosition : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(SkillID);
	Args.Add(isInstantSkill);
	Args.Add(PosX);
	Args.Add(PosY);
	Args.Add(PosZ);
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(ActionID));
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(BeginTime));
	Args.Add(ActionIndex);
	Args.Add(CasterID);
	entity->CellCall(TEXT("broadcastCSkillToPosition"), Args);
}

void UCSkillInterface::BroadcastCSkillToTarget(int32 SkillID, uint8 isInstantSkill, int32 TargetID, TArray<FString> ActionID, TArray<FString> BeginTime, int32 ActionIndex, int32 CasterID)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::BroadcastCSkillToPosition : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(SkillID);
	Args.Add(isInstantSkill);
	Args.Add(TargetID);
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(ActionID));
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(BeginTime));
	Args.Add(ActionIndex);
	Args.Add(CasterID);
	entity->CellCall(TEXT("broadcastCSkillToTarget"), Args);
}

void UCSkillInterface::BroadcastCSkillInterrupted(int32 SkillID, int32 Reason, int32 ActionIndex)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::BroadcastCSkillToPosition : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(SkillID);
	Args.Add(Reason);
	Args.Add(ActionIndex);
	entity->CellCall(TEXT("broadcastCSkillInterrupted"), Args);
}

void UCSkillInterface::BroadcastBeHitPlayEffect(int32 CasterID, int32 TargetID, int32 ActionIndex, TArray<FString> ActionID, FString EffectID, FString SoundID, TArray<FString> BeginTime)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::BroadcastBeHitPlayEffect : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(CasterID);
	Args.Add(TargetID);
	Args.Add(ActionIndex);
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(ActionID));
	Args.Add(EffectID);
	Args.Add(SoundID);
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(BeginTime));
	entity->CellCall(TEXT("broadcastBeHitPlayEffect"), Args);
}

void UCSkillInterface::BroadcastHoldEffectPlayEffect(int32 CasterID, int32 EffectIndex, int32 ActionIndex, TArray<FString> ActionID, FString EffectID, FString SoundID, TArray<FString> BeginTime)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::BroadcastHoldEffectPlayEffect : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(CasterID);
	Args.Add(EffectIndex);
	Args.Add(ActionIndex);
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(ActionID));
	Args.Add(EffectID);
	Args.Add(SoundID);
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(BeginTime));
	entity->CellCall(TEXT("broadcastHoldEffectPlayEffect"), Args);
}

void UCSkillInterface::BroadcastHoldEffectEndEffect(int32 EffectIndex, const int32 ActionIndex)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::BroadcastHoldEffectEndEffect : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(EffectIndex);
	Args.Add(ActionIndex);
	entity->CellCall(TEXT("broadcastHoldEffectEndEffect"), Args);
}

void UCSkillInterface::BroadcastPlayBuffEffect(int32 BuffIndex, int32 CasterID, int32 ActionIndex, TArray<FString> ActionID, TArray<FString> BeginTime, FString EffectID, FString SoundID)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::BroadcastPlayBuffEffect : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(BuffIndex);
	Args.Add(CasterID);
	Args.Add(ActionIndex);
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(ActionID));
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(BeginTime));
	Args.Add(EffectID);
	Args.Add(SoundID);
	entity->CellCall(TEXT("broadcastPlayBuffEffect"), Args);

}

void UCSkillInterface::BroadcastAddBuff(int32 BuffIndex, int32 BuffID, FString BuffScript, int32 CasterID, float BuffTotalTime, FString EndTime, int32 Layer)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::BroadcastAddBuff : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(BuffIndex);
	Args.Add(BuffID);
	Args.Add(BuffScript);
	Args.Add(CasterID);
	Args.Add(BuffTotalTime);
	Args.Add(EndTime);
	Args.Add(Layer);
	entity->CellCall(TEXT("broadcastAddBuff"), Args);
}

void UCSkillInterface::BroadcastRemoveBuff(int32 BuffIndex)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::BroadcastRemoveBuff : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(BuffIndex);
	entity->CellCall(TEXT("broadcastRemoveBuff"), Args);
}

void UCSkillInterface::BroadcastOnBuffLayerChange(int32 BuffIndex, int32 layer)
{
	KBEngine::Entity* entity = GetEntity();
	if ( nullptr == entity )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::BroadcastOnBuffLayerChange : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(BuffIndex);
	Args.Add(layer);
	entity->CellCall(TEXT("broadcastOnBuffLayerChange"), Args);
}

void UCSkillInterface::addHitFlyTimer(float delayTime, int32 casterID, TArray<FString> actionID, FString effectID, FString soundID, TArray<FString> actionBeginTime)
{
	if (hitFlyTimer.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(hitFlyTimer);
	}
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, hitFlyTimer, FTimerDelegate::CreateLambda([this, casterID, actionID, effectID, soundID, actionBeginTime]()
	{
		onHitFlyTimer(casterID, actionID, effectID, soundID, actionBeginTime);
	}), delayTime, false);
}

void UCSkillInterface::onHitFlyTimer(int32 casterID, TArray<FString> actionID, FString effectID, FString soundID, TArray<FString> actionBeginTime)
{
	setActionIndex();
	USkillInterface *SkillInterface = ((GameObject*)GetEntity())->Interface_Cache.SkillInterface;
	if (IsValid(SkillInterface))
	{
		SkillInterface->BeHitPlayEffect(casterID, GetEntity()->ID(), getActionIndex(), actionID, effectID, soundID, actionBeginTime);
	}
	BroadcastBeHitPlayEffect(casterID, GetEntity()->ID(), getActionIndex(), actionID, effectID, soundID, actionBeginTime);
}

void UCSkillInterface::delHitFlyTimer()
{
	if (hitFlyTimer.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(hitFlyTimer);
	}
}

void UCSkillInterface::CSkillChangeDirection(FVector direction, int32 changeReason)
{
	KBEngine::Entity* entity = GetEntity();
	if (nullptr == entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillChangeDirection : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(direction);
	Args.Add(changeReason);
	entity->CellCall(TEXT("cSkillChangeDirection"), Args);
}

void UCSkillInterface::CSkillDoHitBack(int32 casterID, float moveSpeed, FVector desPosition, FString actionID, float actionBeginTime)
{
	KBEngine::Entity* entity = GetEntity();
	if (nullptr == entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillDoHitBack : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(casterID);
	Args.Add(moveSpeed);
	Args.Add(desPosition);
	Args.Add(actionID);
	Args.Add(actionBeginTime);
	entity->CellCall(TEXT("cSkillDoHitBack"), Args);
}

void UCSkillInterface::CSkillOnEndHitBack(int32 casterID, FString actionID, FString endActionID)
{
	KBEngine::Entity* entity = GetEntity();
	if (nullptr == entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCSkillInterface::CSkillOnEndHitBack : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(casterID);
	Args.Add(actionID);
	Args.Add(endActionID);
	entity->CellCall(TEXT("cSkillOnEndHitBack"), Args);
}

CONTROL_COMPILE_OPTIMIZE_END