#include "BuffClientStackable.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"

UBuffClientStackable::UBuffClientStackable()
{
	_className = "BuffClientStackable";
}

UBuffClientStackable::~UBuffClientStackable()
{
}

void UBuffClientStackable::init(FString BuffID, const FBUFF_TABLE_DATA * dictDat)
{
	UBuffClientLoop::init(BuffID, dictDat);
	if (dictDat->Param1 != "")
	{
		maxStackLayer = FSTRING_TO_INT(dictDat->Param1);
	}
}

bool UBuffClientStackable::receiveSuccess(CS3Entity * caster, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		TMap<int32, UBuffDataType*> buffDatas = CSkillInterface->getAttrBuffs();
		for (auto i : buffDatas)
		{
			if (i.Value->buffID == getID())
			{
				if (i.Value->layer < maxStackLayer)
				{
					CSkillInterface->stackBuff(i.Value->index);
				}
				CSkillInterface->resetBuffEndTime(i.Value->index);
				return true;
			}
		}
	}
	return UBuffClientLoop::receiveSuccess(caster, receiver);
}

void UBuffClientStackable::addHoldEffect(CS3Entity * receiver, UBuffDataType * buffData, bool isReloadBuff)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	CS3Entity * caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(buffData->casterID);
	int32 index = 0;
	for (auto effect : _holdEffectList)
	{
		if (effect->canEffect(caster, receiver))
		{
			for (int32 i = 0; i < buffData->layer; ++i)
			{
				UHoldEffectDataType *effectData =  effect->getNewEffectData(caster, receiver);
				effectData->index = CSkillInterface->getNewHoldEffectIndex();
				effectData->sourceType = HOLD_EFFECT_SOURCE_TYPE::HOLD_EFFECT_SOURCE_TYPE_BUFF;
				effectData->sourceID = getID();
				effectData->configIndex = index;
				effectData->casterID = caster != nullptr ? caster->ID(): 0;
				effectData->buffIndex = buffData->index;

				CSkillInterface->addHoldEffectData(effectData);
				effect->onBegin(effectData, receiver);
			}
		}
		++index;
	}
}

void UBuffClientStackable::removeHoldEffect(CS3Entity * receiver, UBuffDataType * buffData)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	int32 index = 0;
	for (auto effect : _holdEffectList)
	{
		TArray<UHoldEffectDataType *> tempList;
		for (auto effectData : CSkillInterface->GetHoldEffectData())
		{
			if (effectData->sourceType == HOLD_EFFECT_SOURCE_TYPE::HOLD_EFFECT_SOURCE_TYPE_BUFF &&
				effectData->configIndex == index && effectData->buffIndex == buffData->index)
			{
				tempList.Add(effectData);
			}
		}

		if (tempList.Num() > 0)
		{
			for (int32 i = tempList.Num() - 1; i >= 0; i--)
			{
				effect->onEnd(tempList[i], receiver);
				CSkillInterface->removeHoldEffectData(tempList[i]->index);
			}
		}
		++index;
	}
}

void UBuffClientStackable::doStack(CS3Entity * receiver, UBuffDataType * buffData)
{
	CS3Entity * caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(buffData->casterID);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (nullptr == caster || !IsValid(CSkillInterface))
	{
		return;
	}
	int32 index = 0;
	for (auto effect : _holdEffectList)
	{
		if (effect->canEffect(caster, receiver))
		{
			UHoldEffectDataType *effectData = effect->getNewEffectData(caster, receiver);
			effectData->index = CSkillInterface->getNewHoldEffectIndex();
			effectData->sourceType = HOLD_EFFECT_SOURCE_TYPE::HOLD_EFFECT_SOURCE_TYPE_BUFF;
			effectData->sourceID = getID();
			effectData->configIndex = index;
			effectData->casterID = caster != nullptr ? caster->ID() : 0;
			effectData->buffIndex = buffData->index;

			CSkillInterface->addHoldEffectData(effectData);
			effect->onBegin(effectData, receiver);
		}
		++index;
	}
	buffData->layer += 1;
	CSkillInterface->BroadcastOnBuffLayerChange(buffData->index, buffData->layer);
}
