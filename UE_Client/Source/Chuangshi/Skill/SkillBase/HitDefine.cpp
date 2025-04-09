#include "HitDefine.h"
#include "Skill/SkillBase/HitTypeDefine.h"
#include "Interface/SkillInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include "Skill/EffectLoader.h"
#include "Skill.h"
#include "Buff.h"
#include "CS3Base/GameObject.h"

CONTROL_COMPILE_OPTIMIZE_START
static int32 HIT_TIME_ACCURACY = 1000; //打击时间 hitTime 精确度，保留小数后三位

UHitDefine::UHitDefine()
{
	_hitType = ENUM_HIT_TYPE::HitDodge;
	_hitArea = nullptr;
	_receiverCondition = NewObject<UObjectCondition>();
	_fliterCondition = NewObject<UFilterCondition>();
	_effectList = TArray<UEffectSkillBase*>();
}

UHitDefine::~UHitDefine()
{

}

void UHitDefine::init(FSKILL_HIT dictDat, USkill* skill)
{
	_hitType = dictDat.HitType;
	_hitArea = NewAreaInstance(dictDat.HitArea);
	if (dictDat.ReceiverCondition.Num() > 0)
	{
		_receiverCondition->init(dictDat.ReceiverCondition);
	}
	if (dictDat.FilterCondition.Num() > 0)
	{
		_fliterCondition->init(dictDat.FilterCondition);
	}
	for (auto effectData : dictDat.EffectList)
	{
		UEffectSkillBase* effect = nullptr;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->EffectLoader))
		{
			effect = UUECS3GameInstance::Instance->EffectLoader->createEffect(effectData, skill);
		}
		if (nullptr != effect)
		{
			_effectList.Add(effect);
		}
	}
}

void UHitDefine::receive(USkill* skill, CS3Entity * caster, CS3Entity * receiver)
{

	if (!caster)
	{
		return;
	}

	UHitTypeDefine* g_hitTypeDefine = UHitTypeDefine::GetInstance();
	if (g_hitTypeDefine->isHit(_hitType, caster, receiver) == SKILL_HIT_TYPE::SKILL_HIT_ERROR)
	{
		return;
	}
	else if (g_hitTypeDefine->isHit(_hitType, caster, receiver) == SKILL_HIT_TYPE::SKILL_HIT_FAILED)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->CSkillOnDodgeSkillHit(caster->ID());
		}
		return;
	}
	if (!caster)
	{
		return;
	}

	for (auto effect : _effectList)
	{
		if (effect->canEffect(skill, caster, receiver))
		{
			effect->onReceive(skill, caster, receiver);
		}
	}
}

int32 UHitDefine::validReceiver(CS3Entity * caster, CS3Entity * receiver)
{
	if (!receiver)
	{
		return (int32)SKILL_MESSAGE::SKILL_MISS_TARGET;
	}
	
	return _receiverCondition->valid(caster, receiver, true);
}

TArray<CS3Entity*> UHitDefine::filterReceiver(USkill * skill, CS3Entity * caster, USkillTargetObjImpl * target, TArray<CS3Entity*> receivers)
{
	return _fliterCondition->filter(skill, caster, target, receivers);
}

TArray<CS3Entity*> UHitDefine::getReceivers(USkill * skill, CS3Entity * caster, USkillTargetObjImpl * target)
{
	TArray<CS3Entity*> receivers = _hitArea->getObjectList(caster, target);
	TArray<CS3Entity*> list = receivers.FilterByPredicate([caster, this](CS3Entity* entity)
	{
		if (entity)
		{
			if (validReceiver(caster, entity) == (int32)SKILL_MESSAGE::SKILL_GO_ON)
			{
				return true;
			}
		}
		return false;
	});
	return filterReceiver(skill, caster, target, list);
}

TArray<UEffectSkillBase*> UHitDefine::getEffectList()
{
	return _effectList;
}

USkillHitDefine::USkillHitDefine()
{
	_hitTime = 0;
}

USkillHitDefine::~USkillHitDefine()
{
}

void USkillHitDefine::init(FSKILL_HIT dictDat, USkill * skill)
{
	UHitDefine::init(dictDat, skill);
	if (!skill->isInstantSkill())
	{
		_hitTime = floor(dictDat.HitTime * HIT_TIME_ACCURACY);
	}
}

void USkillHitDefine::onHit(USkill * skill, CS3Entity * caster, USkillTargetObjImpl * target, int32 index)
{
	skill->onArrive(caster, target, _hitTime, index);
}

void USkillHitDefine::onHitArrive(USkill * skill, CS3Entity * caster, USkillTargetObjImpl * target, int32 index)
{
	TArray<CS3Entity*> receivers = getReceivers(skill, caster, target);
	for (auto receiver : receivers)
	{
		//if (receiver->ClassName() == "CMonster")
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->receiveSkillHit(caster, receiver, skill->getID(), _hitTime, index);
		}	
	}
}

UBuffHitDefine::UBuffHitDefine()
{
	_hitType = ENUM_HIT_TYPE::HitDodge;
	_hitArea = nullptr;
	_receiverCondition = NewObject<UObjectCondition>();
	_fliterCondition = NewObject<UFilterCondition>();
	_effectList = TArray<UEffectSkillBase*>();
}

UBuffHitDefine::~UBuffHitDefine()
{

}

void UBuffHitDefine::init(FBUFF_HIT dictDat, UBuff * buff)
{
	_hitType = dictDat.HitType;
	_hitArea = NewAreaInstance(dictDat.HitArea);
	if (dictDat.ReceiverCondition.Num() > 0)
	{
		_receiverCondition->init(dictDat.ReceiverCondition);
	}
	if (dictDat.FilterCondition.Num() > 0)
	{
		_fliterCondition->init(dictDat.FilterCondition);
	}
	for (auto effectData : dictDat.EffectList)
	{
		UEffectSkillBase* effect = nullptr;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->EffectLoader))
		{
			effect = UUECS3GameInstance::Instance->EffectLoader->createEffect(effectData, nullptr);
		}
		if (nullptr != effect)
		{
			_effectList.Add(effect);
		}
	}
}

void UBuffHitDefine::receive(UBuff * buff, CS3Entity * caster, CS3Entity * receiver)
{
	if (!caster)
	{
		return;
	}

	UHitTypeDefine* g_hitTypeDefine = UHitTypeDefine::GetInstance();
	if (g_hitTypeDefine->isHit(_hitType, caster, receiver) == SKILL_HIT_TYPE::SKILL_HIT_ERROR)
	{
		return;
	}
	else if (g_hitTypeDefine->isHit(_hitType, caster, receiver) == SKILL_HIT_TYPE::SKILL_HIT_FAILED)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->CSkillOnDodgeSkillHit(caster->ID());
		}
		return;
	}
	if (!caster)
	{
		return;
	}

	for (auto effect : _effectList)
	{
		if (effect->canEffect(nullptr, caster, receiver))
		{
			effect->onReceive(nullptr, caster, receiver);
		}
	}
}

int32 UBuffHitDefine::validReceiver(CS3Entity * caster, CS3Entity * receiver)
{
	if (!receiver)
	{
		return (int32)SKILL_MESSAGE::SKILL_MISS_TARGET;
	}

	return _receiverCondition->valid(caster, receiver, true);
}

TArray<CS3Entity*> UBuffHitDefine::filterReceiver(UBuff * buff, CS3Entity * caster, USkillTargetObjImpl * target, TArray<CS3Entity*> receivers)
{
	return _fliterCondition->filter(nullptr, caster, target, receivers);
}

TArray<CS3Entity*> UBuffHitDefine::getReceivers(UBuff * buff, CS3Entity * caster, USkillTargetObjImpl * target)
{
	TArray<CS3Entity*> receivers = _hitArea->getObjectList(caster, target);
	TArray<CS3Entity*> list = receivers.FilterByPredicate([caster, this](CS3Entity* entity)
	{
		if (entity)
		{
			if (validReceiver(caster, entity) == (int32)SKILL_MESSAGE::SKILL_GO_ON)
			{
				return true;
			}
		}
		return false;
	});
	return filterReceiver(nullptr, caster, target, list);
}

TArray<UEffectSkillBase*> UBuffHitDefine::getEffectList()
{
	return _effectList;
}

void UBuffHitDefine::onHitArrive(UBuff* buff, CS3Entity* caster, USkillTargetObjImpl* target, FString attrName, int32 index)
{
	TArray<CS3Entity*> receivers = getReceivers(nullptr, caster, target);
	for (auto receiver : receivers)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->receiveBuffHit(caster->ID(), buff->getID(), attrName, index);
		}
	}
	target->RemoveFromRoot();
}

USkillHitData::USkillHitData()
{
}

USkillHitData::~USkillHitData()
{
}

void USkillHitData::init(TArray<FSKILL_HIT> hitList, USkill * skill)
{
	for (auto data : hitList)
	{
		USkillHitDefine* hitInstance = NewObject<USkillHitDefine>();
		hitInstance->init(data, skill);
		int32 hitTime = 0;
		if (!skill->isInstantSkill())
		{
			hitTime = floor(data.HitTime * HIT_TIME_ACCURACY);
		}
		if (!_data.Contains(hitTime))
		{
			FSKILL_HIT_DATAS Temp;
			Temp.SkillHitDefines.Add(hitInstance);
			_data.Add(hitTime, Temp);
		}
		else
		{
			_data[hitTime].SkillHitDefines.Add(hitInstance);
		}
	}
}

void USkillHitData::begin(USkill * skill, CS3Entity * caster, USkillTargetObjImpl * target)
{
	if (_data.Num() <= 0)
	{
		skill->onSkillEnd(caster, target, true);
	}
	for (auto i : _data)
	{
		UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
		if (IsValid(CSkillInterface))
		{
			CSkillInterface->addSkillHitTimer(i.Key / (float)HIT_TIME_ACCURACY, skill, caster, target, i.Key);
		}
	}
}

void USkillHitData::onHit(USkill * skill, CS3Entity * caster, USkillTargetObjImpl * target, int32 hitTime)
{
	if (!_data.Contains(hitTime))
	{
		return;
	}
	for (int32 i = 0; i < _data[hitTime].SkillHitDefines.Num();  ++i)
	{
		_data[hitTime].SkillHitDefines[i]->onHit(skill, caster, target, i);
	}
}

void USkillHitData::onHitArrive(USkill * skill, CS3Entity * caster, USkillTargetObjImpl * target, int32 hitTime, int32 index)
{
	if (!_data.Contains(hitTime))
	{
		return;
	}
	if (_data[hitTime].SkillHitDefines.Num() < index)
	{
		return;
	}
	_data[hitTime].SkillHitDefines[index]->onHitArrive(skill, caster, target, index);

	//最后一次打击
	TArray<int32> Temp;
	_data.GenerateKeyArray(Temp);
	Temp.Sort([](const int32 KeyA, const int32 KeyB) 
	{
		return KeyA > KeyB;
	});
	if (hitTime == Temp[0] && index == _data[hitTime].SkillHitDefines.Num()-1)
	{
		skill->onSkillEnd(caster, target, true);
	}
}

USkillHitDefine * USkillHitData::getHit(int32 hitTime, int32 index)
{
	if (_data.Contains(hitTime) && _data[hitTime].SkillHitDefines.Num()> index)
	{
		return _data[hitTime].SkillHitDefines[index];
	}
	return nullptr;
}

float USkillHitData::getTotalTime()
{
	if (_data.Num() > 0)
	{
		TArray<int32> Temp;
		_data.GenerateKeyArray(Temp);
		Temp.Sort([](const int32 KeyA, const int32 KeyB)
		{
			return KeyA > KeyB;
		});
		return Temp[0] / (float)HIT_TIME_ACCURACY;

	}
	return 0.0f;
}

TMap<int32, FSKILL_HIT_DATAS> USkillHitData::getHitData()
{
	return _data;
}

UBuffHitData::UBuffHitData()
{
}

UBuffHitData::~UBuffHitData()
{
}

void UBuffHitData::init(TArray<FBUFF_HIT> hitList, UBuff * buff)
{
	for (auto data : hitList)
	{
		UBuffHitDefine* hitInstance = NewObject<UBuffHitDefine>();
		hitInstance->init(data, buff);
		_data.Add(hitInstance);
	}
}

UBuffHitDefine * UBuffHitData::getHit(int32 index)
{
	if (_data.Num() > index)
	{
		return _data[index];
	}
	return nullptr;
}

void UBuffHitData::onHit(UBuff * buff, CS3Entity * caster, USkillTargetObjImpl * target, FString attrName)
{
	int32 index = 0;
	for (auto hit : _data)
	{
		hit->onHitArrive(buff, caster, target, attrName, index);
		++index;
	}
}

CONTROL_COMPILE_OPTIMIZE_END