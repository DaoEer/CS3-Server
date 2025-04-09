#include "EffectAction.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Interface/SkillInterface.h"
#include "CS3Base/GameObject.h"

UEffectAction::UEffectAction()
{
}

UEffectAction::~UEffectAction()
{
}

void UEffectAction::init(FHIT_EFFECT dictDat, USkill * skill)
{
	UEffectSkillBase::init(dictDat, skill);
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

			}
			else {
				_actionID.Add(actionInfo[0]);
				_actionBeginTime.Add("0.0");
			}
		}
	}
	_effectID = dictDat.Param2;
	_soundID = dictDat.Param3;

	//标记列表（:冒号|竖号分隔，多个代表“且”，留空代表“没有标记”，具体格式与功能由标记定义）
	if (dictDat.Param4 != "")
	{
		TArray<FString> Param4Split = UGolbalBPFunctionLibrary::SplitString(dictDat.Param4);
		for (auto i : Param4Split)
		{
			TArray<FString> List = UGolbalBPFunctionLibrary::SplitString(i, false, TEXT(":"));
			if (List[0] == "IsLocal")
			{
				_isLocal = true;
			}
			else
			{
				CS3_Warning(TEXT("EffectAction: %s is not a correct tag name!"), *List[0]);
			}

		}
	}
}

void UEffectAction::onReceive(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	int32 casterID = caster != nullptr ? caster->ID() : 0;
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->setActionIndex();
		int32 ActionIndex = CSkillInterface->getActionIndex();
		USkillInterface *SkillInterface =((GameObject*)receiver)->Interface_Cache.SkillInterface;
		if (IsValid(SkillInterface))
		{
			SkillInterface->BeHitPlayEffect(casterID, receiver->ID(), ActionIndex, _actionID, _effectID, _soundID, _actionBeginTime);
		}
		if (!_isLocal)
		{
			CSkillInterface->BroadcastBeHitPlayEffect(casterID, receiver->ID(), ActionIndex, _actionID, _effectID, _soundID, _actionBeginTime);
		}
		
	}
}
