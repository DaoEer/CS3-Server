#include "HoldEffectPlayEffect.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Interface/SkillInterface.h"
#include "CS3Base/GameObject.h"

UHoldEffectPlayEffect::UHoldEffectPlayEffect()
{
}

UHoldEffectPlayEffect::~UHoldEffectPlayEffect()
{
}

void UHoldEffectPlayEffect::init(FHOLD_EFFECT dictDat, USkill * skill)
{
	UHoldEffect::init(dictDat, skill);
	if (dictDat.Param1 != "")
	{
		TArray<FString> Param1 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
		for (auto i : Param1)
		{
			TArray<FString> actionInfo = UGolbalBPFunctionLibrary::SplitString(i, false, TEXT(":"));
			if (actionInfo.Num() > 1)
			{
				_actionID.Add(actionInfo[0]);
				_actionBeginTime.Add(actionInfo[1]);

			} else {
				_actionID.Add(actionInfo[0]);
				_actionBeginTime.Add("0.0");
			}
		}
	}
	_effectID = dictDat.Param2;
	_soundID = dictDat.Param3;
}

void UHoldEffectPlayEffect::onBegin(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UHoldEffect::onBegin(effectData, receiver);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->setActionIndex();
		int32 ActionIndex = CSkillInterface->getActionIndex();
		effectData->setTempData("actionIndex", FVariant(ActionIndex));
		USkillInterface *SkillInterface = ((GameObject*)receiver)->Interface_Cache.SkillInterface;
		if (IsValid(SkillInterface))
		{
			SkillInterface->HoldEffectPlayEffect(effectData->casterID, effectData->index, ActionIndex, _actionID, _effectID, _soundID, _actionBeginTime);
		}
		CSkillInterface->BroadcastHoldEffectPlayEffect(effectData->casterID, effectData->index, ActionIndex, _actionID, _effectID, _soundID, _actionBeginTime);
	}
}

void UHoldEffectPlayEffect::onEnd(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	FVariant value = effectData->getTempData("actionIndex", FVariant(0));
	int32 ActionIndex = value.GetValue<int32>();
	USkillInterface *SkillInterface = ((GameObject*)receiver)->Interface_Cache.SkillInterface;
	if (IsValid(SkillInterface))
	{
		SkillInterface->HoldEffectEndEffect( effectData->index, ActionIndex);
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->BroadcastHoldEffectEndEffect(effectData->index, ActionIndex);
	}
	UHoldEffect::onEnd(effectData, receiver);
}
