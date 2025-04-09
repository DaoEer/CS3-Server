
#include "RequireDefine.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "GameData/GameDeFine.h"
#include "Skill.h"

URequire::URequire()
{

}

URequire::~URequire()
{

}

void URequire::load(FSKILL_REQUIRE Args)
{

}

int32 URequire::validObject(CS3Entity* caster, USkill* SkillInstance)
{
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

void URequire::pay(CS3Entity* caster, USkill* SkillInstance)
{

}

int32 URequire::getPay(CS3Entity* caster, USkill* skillInstance)
{
	return 0;
}

URequireMp::URequireMp()
{
}

URequireMp::~URequireMp()
{
}

void URequireMp::load(FSKILL_REQUIRE Args)
{
	if (Args.Param1 != "")
	{
		_value = FSTRING_TO_INT(Args.Param1);
	}
	if (Args.Param2 != "")
	{
		_percent = FSTRING_TO_FLOAT(Args.Param2);
	}
}

int32 URequireMp::validObject(CS3Entity * caster, USkill * SkillInstance)
{
	int32 MP = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("MP"));
	if (MP >= getPay(caster, SkillInstance))
	{
		return (int32)SKILL_MESSAGE::SKILL_GO_ON;
	}
	return (int32)SKILL_MESSAGE::SKILL_OUTOF_MP;
}

void URequireMp::pay(CS3Entity * caster, USkill * SkillInstance)
{
	int value = getPay(caster, SkillInstance);
	if (value == 0)
	{
		return;
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillSetMP(value);
	}
}

int32 URequireMp::getPay(CS3Entity * caster, USkill * skillInstance)
{
	int32 MP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("MP_Max"));
	int32 RequireValue = _value + int(MP_Max * _percent);
	return RequireValue > 0 ? RequireValue : 0 ;
}

URequireHp::URequireHp()
{
}

URequireHp::~URequireHp()
{
}

void URequireHp::load(FSKILL_REQUIRE Args)
{
	if (Args.Param1 != "")
	{
		_value = FSTRING_TO_INT(Args.Param1);
	}
	if (Args.Param2 != "")
	{
		_percent = FSTRING_TO_FLOAT(Args.Param2);
	}
}

int32 URequireHp::validObject(CS3Entity * caster, USkill * SkillInstance)
{
	int32 HP = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("HP"));
	if (HP >= getPay(caster, SkillInstance))
	{
		return (int32)SKILL_MESSAGE::SKILL_GO_ON;
	}
	return (int32)SKILL_MESSAGE::SKILL_OUTOF_HP;
}

void URequireHp::pay(CS3Entity * caster, USkill * SkillInstance)
{
	int value = getPay(caster, SkillInstance);
	if (value == 0)
	{
		return;
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillSetHP(value);
	}
}

int32 URequireHp::getPay(CS3Entity * caster, USkill * skillInstance)
{
	int32 HP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("HP_Max"));
	int32 RequireValue = _value + int(HP_Max * _percent);
	return RequireValue > 0 ? RequireValue : 0;
}

URequireGangQi::URequireGangQi()
{
}

URequireGangQi::~URequireGangQi()
{
}

inline void URequireGangQi::load(FSKILL_REQUIRE Args)
{
	if (Args.Param1 != "")
	{
		_value = FSTRING_TO_INT(Args.Param1);
	}
	if (Args.Param2 != "")
	{
		_percent = FSTRING_TO_FLOAT(Args.Param2);
	}
}

inline int32 URequireGangQi::validObject(CS3Entity * caster, USkill * SkillInstance)
{
	int32 gangQiValue = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("gangQiValue"));
	if (gangQiValue >= getPay(caster, SkillInstance))
	{
		return (int32)SKILL_MESSAGE::SKILL_GO_ON;
	}
	return (int32)SKILL_MESSAGE::SKILL_OUTOF_HP;
}

void URequireGangQi::pay(CS3Entity * caster, USkill * SkillInstance)
{
	int value = getPay(caster, SkillInstance);
	if (value == 0)
	{
		return;
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillRecvGangQi(value);
	}
}

int32 URequireGangQi::getPay(CS3Entity * caster, USkill * skillInstance)
{
	int32 gangQiValue_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("gangQiValue_Max"));
	int32 RequireValue = _value + int(gangQiValue_Max * _percent);
	return RequireValue > 0 ? RequireValue : 0;
}

URequireCostItem::URequireCostItem()
{

}

URequireCostItem::~URequireCostItem()
{
}

void URequireCostItem::load(FSKILL_REQUIRE Args)
{
	if (Args.Param1 != "")
	{
		_itemID = FSTRING_TO_INT(Args.Param1);
	}
	if (Args.Param2 != "")
	{
		_amount = FSTRING_TO_INT(Args.Param2);
	}
}

int32 URequireCostItem::validObject(CS3Entity * caster, USkill * SkillInstance)
{
	URoleKitBagInterface* RoleKitBagInterface = Cast<URoleKitBagInterface>
		(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));

	TArray<UItemBase*> Items = RoleKitBagInterface->GetItemsByItemID(_itemID);
	if (Items.Num() <= 0)
	{
		return (int32)SKILL_MESSAGE::SKILL_OUTOF_ITEM;
	}
	int32 totalAmount = 0;
	for (auto Item : Items)
	{
		totalAmount += Item->Amount;
	}
	if (totalAmount > _amount)
	{
		return (int32)SKILL_MESSAGE::SKILL_OUTOF_ITEM;
	}
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

void URequireCostItem::pay(CS3Entity * caster, USkill * SkillInstance)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillRequireItem(_itemID, _amount);
	}
}

int32 URequireCostItem::getPay(CS3Entity * caster, USkill * skillInstance)
{
	return 0;
}

URequireDefine::URequireDefine()
{

}

URequireDefine::~URequireDefine()
{

}

void URequireDefine::load(TArray<FSKILL_REQUIRE> Args)
{
	for (auto i : Args)
	{
		if (i.Type == ENUM_SKILL_REQUIRE_TYPE::RequireMp)
		{
			URequireMp * Instance = NewObject <URequireMp>();
			Instance->load(i);
			_requires.Add((URequire* )Instance);
		}
		else if (i.Type == ENUM_SKILL_REQUIRE_TYPE::RequireHp)
		{
			URequireHp * Instance = NewObject <URequireHp>();
			Instance->load(i);
			_requires.Add((URequire*)Instance);
		}
		else if (i.Type == ENUM_SKILL_REQUIRE_TYPE::RequireGangQi)
		{
			URequireGangQi * Instance = NewObject <URequireGangQi>();
			Instance->load(i);
			_requires.Add((URequire*)Instance);
		}
		else if (i.Type == ENUM_SKILL_REQUIRE_TYPE::RequireCostItem)
		{
			URequireCostItem * Instance = NewObject <URequireCostItem>();
			Instance->load(i);
			_requires.Add((URequire*)Instance);
		}
		else
		{
			URequire * Instance = NewObject <URequire>();
			Instance->load(i);
			_requires.Add(Instance);
		}
	}
}

int32 URequireDefine::validObject(CS3Entity* caster, USkill* SkillInstance)
{
	for (auto requires : _requires)
	{
		int32 state = requires->validObject(caster, SkillInstance);
		if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON )
		{
			return state;
		}
	}
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

void URequireDefine::pay(CS3Entity* caster, USkill* SkillInstance)
{
	for (auto requires : _requires)
	{
		requires->pay(caster, SkillInstance);
	}
}

