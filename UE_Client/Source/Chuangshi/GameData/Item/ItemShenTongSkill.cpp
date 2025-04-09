#include "ItemShenTongSkill.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/SkillManager.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"

UItemShenTongSkill::UItemShenTongSkill()
{
}

UItemShenTongSkill::~UItemShenTongSkill()
{
}

void UItemShenTongSkill::SetDynamicData(int32 SkillID_, int32 Level_, int32 PreExp, int32 ReduceUseLevel, uint8 isComminution_)
{
	shenTongSkillID = SkillID_;
	shenTongLevel = Level_;
	preExp = PreExp;
	reduceUseSkillLevel = ReduceUseLevel;
	isComminution = (bool)isComminution_;


	SkillID = SkillID_;
	USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillID);
	if (!IsValid(SkillData))
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInfo::InitFormatInfoTips : SkillData!"));
		return;
	}

	///获取技能消耗
	TArray<FSKILL_REQUIRE> RequireDefineList = SkillData->GetCasterRequireList();
	for (FSKILL_REQUIRE RequireData : RequireDefineList)
	{
		switch (RequireData.Type)
		{
		case ENUM_SKILL_REQUIRE_TYPE::RequireMp:
		{
			shenTongRequire = FSTRING_TO_INT(RequireData.Param1);
		}
		}
	}

	///获取技能CD
	TArray<FSKILL_COOL_DOWN> CoolDownList = SkillData->GetCasterCoolDown();
	for (FSKILL_COOL_DOWN CoolDown : CoolDownList)
	{
		shenTongSkillCD = CoolDown.CoolDownTime;
		break;
	}


}