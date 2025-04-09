#include "EffectAddBuff.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"
#include "SKill/SkillBase/Skill.h"

UEffectAddBuff::UEffectAddBuff()
{
}

UEffectAddBuff::~UEffectAddBuff()
{
}

void UEffectAddBuff::init(FHIT_EFFECT dictDat, USkill * skill)
{
	UEffectSkillBase::init(dictDat, skill);
	if (dictDat.Param1 == "" && skill)
	{
		CS3_Warning(TEXT("skillID: %d Buffer config error!!"), skill->getID());
		return;
	}
	_buffID = FSTRING_TO_INT(dictDat.Param1);
}

void UEffectAddBuff::onReceive(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->addBuff(caster, _buffID);
	}
}
