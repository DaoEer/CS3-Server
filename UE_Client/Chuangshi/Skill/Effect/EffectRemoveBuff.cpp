#include "EffectRemoveBuff.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Skill/SkillBase/Skill.h"

UEffectRemoveBuff::UEffectRemoveBuff()
{
}

UEffectRemoveBuff::~UEffectRemoveBuff()
{
}

void UEffectRemoveBuff::init(FHIT_EFFECT dictDat, USkill * skill)
{
	UEffectSkillBase::init(dictDat, skill);
	if (dictDat.Param1 == "" && skill)
	{
		CS3_Warning(TEXT("Skill EffectRemoveBuff config is none! SkillID=%d!!"), skill->getID());
		return;
	}
	TArray<FString> buffList = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
	for (auto i : buffList)
	{
		_buffIdList.Add(FSTRING_TO_INT(i));
	}
}

void UEffectRemoveBuff::onReceive(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	for (auto i : _buffIdList)
	{
		CSkillInterface->removeBuffByID(i);
	}
}
