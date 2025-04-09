#include "HoldEffectAddAttr.h"
#include "Util/CS3Debug.h"
#include "Skill/SkillBase/Skill.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"



UHoldEffectAddAttr::UHoldEffectAddAttr()
{
}

UHoldEffectAddAttr::~UHoldEffectAddAttr()
{

}

void UHoldEffectAddAttr::init(FHOLD_EFFECT dictDat, USkill* skill)
{
	UHoldEffect::init(dictDat, skill);
	if (dictDat.Param1 == "")
	{
		CS3_Warning(TEXT("Skill HoldEffectAddAttr config is none! SkillID=%d!"), skill->getID());
	}else {
		TArray<FString> Param1 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
		for (auto i : Param1)
		{
			_propertiesList.Add(FSTRING_TO_INT(i));
		}
	}
	if (dictDat.Param2 != "")
	{
		_attrPercent = (int32)(FSTRING_TO_FLOAT(dictDat.Param2) * 10000);
	}
	
	if (dictDat.Param3 != "")
	{
		_attrValue = FSTRING_TO_INT(dictDat.Param3);
	}
}

void UHoldEffectAddAttr::onBegin(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UHoldEffect::onBegin(effectData, receiver);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface) && _propertiesList.Num() > 0)
	{
		CSkillInterface->CSkillEffectAddAttr(_propertiesList, _attrPercent, _attrValue);
	}

}

void UHoldEffectAddAttr::onEnd(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface) && _propertiesList.Num() > 0)
	{
		CSkillInterface->CSkillEffectAddAttr(_propertiesList, -_attrPercent, -_attrValue);
	}

	UHoldEffect::onEnd(effectData, receiver);
}
