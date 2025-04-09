#include "EffectSkillBase.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Skill/SkillBase/Skill.h"

UEffectSkillBase::UEffectSkillBase()
{
	_receiverActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	_casterActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
}

UEffectSkillBase::~UEffectSkillBase()
{
}

void UEffectSkillBase::init(FHIT_EFFECT dictDat, USkill * skill)
{
	_receiverActForbid = dictDat.ReceiverActForbid;
	_casterActForbid = dictDat.CasterActForbid;
}

bool UEffectSkillBase::canEffect(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
	uint32 actionFlagValue1 = uint32(1) << uint32(_receiverActForbid);
	uint32 actForbid1 = UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("actForbid"));
	if (_receiverActForbid != ACTION_FLAG::ACTION_FORBID_NONE && (actForbid1 & actionFlagValue1) != 0)
	{
		return false;
	}

	uint32 actionFlagValue2 = uint32(1) << uint32(_casterActForbid);
	uint32 actForbid2 = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("actForbid"));
	if (_casterActForbid != ACTION_FLAG::ACTION_FORBID_NONE && (actForbid2 & actionFlagValue2) != 0)
	{
		return false;
	}


	return true;
}

void UEffectSkillBase::onReceive(USkill * skill, CS3Entity * caster, CS3Entity * receiver)
{
}
