#include "ObjectCondition.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "GameData/GameDeFine.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/StateInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "CS3Base/GameObject.h"
#include "Interface/SkillInterface.h"

CONTROL_COMPILE_OPTIMIZE_START
template<typename T>
static bool _Compare(T Value1, T Value2, int32 operation)
{
	if (operation == 0)
	{
		if (Value1 == Value2)
		{
			return true;
		}
		return false;
	}
	else if (operation == 1)
	{
		if (Value1 > Value2)
		{
			return true;
		}
		return false;
	}
	else if (operation == 2)
	{
		if (Value1 < Value2)
		{
			return true;
		}
		return false;
	}
	else if (operation == 3)
	{
		if (Value1 >= Value2)
		{
			return true;
		}
		return false;
	}
	else if (operation == 4)
	{
		if (Value1 <= Value2)
		{
			return true;
		}
		return false;
	}
	else if (operation == 5)
	{
		if (Value1 != Value2)
		{
			return true;
		}
		return false;
	}
	return false;
}

UConditionBase::UConditionBase()
{
}

UConditionBase::~UConditionBase()
{
}

void UConditionBase::init(FSKILL_USE_CONDITION dictDat)
{
}

int32 UConditionBase::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

UConditionTypeRelation::UConditionTypeRelation()
{
}

UConditionTypeRelation::~UConditionTypeRelation()
{
}

void UConditionTypeRelation::init(FSKILL_USE_CONDITION dictDat)
{
	entityTypes = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, true, TEXT("|"));
	TArray<FString> Param21Split = UGolbalBPFunctionLibrary::SplitString(dictDat.Param2, false, TEXT("|"));
	for (auto i : Param21Split)
	{
		relationTypes.Add(FSTRING_TO_INT(i));
	}
}

int32 UConditionTypeRelation::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	if (!target || !caster)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	ENTITY_TYPE EntityFlag = (ENTITY_TYPE)target->GetDefinedProperty(TEXT("entityFlag")).GetValue<uint8>();
	if (!ENTITY_TYPE_DICT.Contains(EntityFlag))
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	FString EntityType = ENTITY_TYPE_DICT[EntityFlag];
	if (entityTypes.Num() > 0 && !entityTypes.Contains(EntityType))
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	int32 Relation = (int32)UGolbalBPFunctionLibrary::QueryRelationByEntityID(caster->ID(), target->ID());
	if (relationTypes.Num() > 0 && !relationTypes.Contains(Relation))
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

UConditionState::UConditionState()
{
}

UConditionState::~UConditionState()
{
}

void UConditionState::init(FSKILL_USE_CONDITION dictDat)
{
	TArray<FString> Param1lSplit = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
	for (auto i : Param1lSplit)
	{
		stateList.Add(FSTRING_TO_INT(i));
	}
	isThisState = FSTRING_TO_INT(dictDat.Param2);
}

int32 UConditionState::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	if (target == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	FVariant propvalue = target->GetDefinedProperty(TEXT("state"));
	if (propvalue == FVariant(NULL))
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	int32 state = target->GetDefinedProperty(TEXT("state")).GetValue<int32>();
	if (bool(isThisState))
	{	
		if (stateList.Contains(state))
		{
			return (int32)SKILL_MESSAGE::SKILL_GO_ON;
		}
	}else{
		if (!stateList.Contains(state))
		{
			return (int32)SKILL_MESSAGE::SKILL_GO_ON;
		}
	}

	return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
}

UConditionBuffCount::UConditionBuffCount()
{
}

UConditionBuffCount::~UConditionBuffCount()
{
}

void UConditionBuffCount::init(FSKILL_USE_CONDITION dictDat)
{
	TArray<FString> Param1lSplit = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
	for (auto i : Param1lSplit)
	{
		_buffIdList.Add(FSTRING_TO_INT(i));
	}
	_operation = FSTRING_TO_INT(dictDat.Param2);
	_scale = FSTRING_TO_FLOAT(dictDat.Param3);
}

int32 UConditionBuffCount::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	if (target == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}

	ENTITY_TYPE EntityFlag = (ENTITY_TYPE)target->GetDefinedProperty(TEXT("entityFlag")).GetValue<uint8>();
	if (EntityFlag == ENTITY_TYPE::ENTITY_FLAG_NPC)
	{
		return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
	}

	TArray<int32> BuffIDList;
	USkillInterface *SkillInterface = ((GameObject*)target)->Interface_Cache.SkillInterface;
	if (IsValid(SkillInterface))
	{
		for (auto i : SkillInterface->getAttrBuffs())
		{
			BuffIDList.Add(i.Value.buffID);
		}
	}
	for (auto id : _buffIdList)
	{
		int32 count = 0;
		for (auto BuffID: BuffIDList)
		{
			if (id == BuffID)
			{
				count += 1;
			}
		}
		if (_Compare((float)count, _scale, _operation))
		{
			return (int32)SKILL_MESSAGE::SKILL_GO_ON;
		}
	}
	return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
}

UConditionBuffLayer::UConditionBuffLayer()
{
}

UConditionBuffLayer::~UConditionBuffLayer()
{
}

void UConditionBuffLayer::init(FSKILL_USE_CONDITION dictDat)
{
	_buffID = FSTRING_TO_INT(dictDat.Param1);
	_operation = FSTRING_TO_INT(dictDat.Param2);
	_scale = FSTRING_TO_FLOAT(dictDat.Param3);
}

int32 UConditionBuffLayer::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	if (target == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}

	ENTITY_TYPE EntityFlag = (ENTITY_TYPE)target->GetDefinedProperty(TEXT("entityFlag")).GetValue<uint8>();
	if (EntityFlag == ENTITY_TYPE::ENTITY_FLAG_NPC)
	{
		return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
	}

	int32 layer = 0;
	USkillInterface *SkillInterface = ((GameObject*)target)->Interface_Cache.SkillInterface;
	if (IsValid(SkillInterface))
	{
		for (auto i : SkillInterface->getAttrBuffs())
		{
			if (i.Value.buffID == _buffID)
			{
				layer = i.Value.layer;
				if (_Compare((float)layer, _scale, _operation))
				{
					return (int32)SKILL_MESSAGE::SKILL_GO_ON;
				}
			}
		}
	}
	return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;

}

UConditionEnemy::UConditionEnemy()
{
}

UConditionEnemy::~UConditionEnemy()
{
}

void UConditionEnemy::init(FSKILL_USE_CONDITION dictDat)
{
	TArray<FString> Param1lSplit = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
	for (auto i : Param1lSplit)
	{
		_assemble.Add(FSTRING_TO_INT(i));
	}
	_operation = FSTRING_TO_INT(dictDat.Param2);
}

int32 UConditionEnemy::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	if (target == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	if (!caster->Actor() || !target->Actor())
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	COMBAT_RELATION Relation = Cast<AServerCharacter>(caster->Actor())->QueryRelation(Cast<AServerCharacter>(target->Actor()));
	if (_operation)
	{
		if (_assemble.Contains(int32(Relation)))
		{
			return (int32)SKILL_MESSAGE::SKILL_GO_ON;
		}
	} else {
		if (!_assemble.Contains(int32(Relation)))
		{
			return (int32)SKILL_MESSAGE::SKILL_GO_ON;
		}
	}
	return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
}

UConditionScriptID::UConditionScriptID()
{
}

UConditionScriptID::~UConditionScriptID()
{
}

void UConditionScriptID::init(FSKILL_USE_CONDITION dictDat)
{
	TArray<FString> Param1lSplit = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
	for (auto i : Param1lSplit)
	{
		ScriptIDList.Add(FSTRING_TO_INT(i));
	}
	_isThisType = FSTRING_TO_INT(dictDat.Param2);
	if (dictDat.Param3 != "")
	{
		needRole = FSTRING_TO_INT(dictDat.Param2);
	}
}

int32 UConditionScriptID::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	if (target == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	UGameObjectInterface * Interface = ((GameObject*)target)->Interface_Cache.GameObjectInterface;
	if (IsValid(Interface))
	{
		if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
		{
			if (needRole)
			{
				return (int32)SKILL_MESSAGE::SKILL_GO_ON;
			}
		}
	}
	FVariant value = target->GetDefinedProperty(TEXT("scriptID"));
	if (value == FVariant(NULL))
	{
		return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
	}
	FString ScriptID = target->GetDefinedProperty(TEXT("scriptID"));
	if (_isThisType && ScriptIDList.Contains(FSTRING_TO_INT(ScriptID)))
	{
		return (int32)SKILL_MESSAGE::SKILL_GO_ON;
	}
	else if (!_isThisType && !ScriptIDList.Contains(FSTRING_TO_INT(ScriptID)))
	{
		return (int32)SKILL_MESSAGE::SKILL_GO_ON;
	}
	return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
}

UConditionEffectState::UConditionEffectState()
{
}

UConditionEffectState::~UConditionEffectState()
{
}

void UConditionEffectState::init(FSKILL_USE_CONDITION dictDat)
{
	TArray<FString> Param1lSplit = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1, false, TEXT("|"));
	for (auto i : Param1lSplit)
	{
		effectStateList.Add(FSTRING_TO_INT(i));
	}
	isThisState = FSTRING_TO_INT(dictDat.Param2);
}

int32 UConditionEffectState::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	if (target == nullptr)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	UStateInterface* StateInterface = ((GameObject*)target)->Interface_Cache.StateInterface;
	if (!IsValid(StateInterface))
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}
	for (auto i : effectStateList)
	{
		if (isThisState && StateInterface->HasEffectState((EFFECT_STATE)i))
		{
			return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
		}
		else if (!isThisState && !StateInterface->HasEffectState((EFFECT_STATE)i))
		{
			return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
		}
	}
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

UObjectCondition::UObjectCondition()
{
}

UObjectCondition::~UObjectCondition()
{
}

void UObjectCondition::init(TArray<FSKILL_USE_CONDITION> Conditions)
{
	if (Conditions.Num() <= 0)
	{
		return;
	}
	for (auto Condition : Conditions)
	{
		add(Condition);
	}
}

int32 UObjectCondition::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	for (auto i : _conditions)
	{
		int32 state = i->valid(caster, target, isCastValidCheck);
		if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
		{
			return state;
		}
	}
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

bool UObjectCondition::isHasConditions()
{
	if (_conditions.Num()>0)
	{
		return true;
	}
	return false;
}

void UObjectCondition::add(FSKILL_USE_CONDITION Condition)
{
	UConditionBase * Instance = nullptr;
	if (Condition.ConditionType == ENUM_USE_CONDITION_TYPE::ConditionTypeRelation)
	{
		UConditionTypeRelation * Temp = NewObject<UConditionTypeRelation>();
		Temp->init(Condition);
		Instance = (UConditionBase*)Temp;
	}
	else if (Condition.ConditionType == ENUM_USE_CONDITION_TYPE::ConditionState)
	{
		UConditionState * Temp = NewObject<UConditionState>();
		Temp->init(Condition);
		Instance = (UConditionBase*)Temp;
	}
	else if (Condition.ConditionType == ENUM_USE_CONDITION_TYPE::ConditionBuffCount)
	{
		UConditionBuffCount * Temp = NewObject<UConditionBuffCount>();
		Temp->init(Condition);
		Instance = (UConditionBase*)Temp;
	}
	else if (Condition.ConditionType == ENUM_USE_CONDITION_TYPE::ConditionBuffLayer)
	{
		UConditionBuffLayer * Temp = NewObject<UConditionBuffLayer>();
		Temp->init(Condition);
		Instance = (UConditionBase*)Temp;
	}
	else if (Condition.ConditionType == ENUM_USE_CONDITION_TYPE::ConditionEnemy)
	{
		UConditionEnemy * Temp = NewObject<UConditionEnemy>();
		Temp->init(Condition);
		Instance = (UConditionBase*)Temp;
	}
	else if (Condition.ConditionType == ENUM_USE_CONDITION_TYPE::ConditionScriptID)
	{
		UConditionScriptID * Temp = NewObject<UConditionScriptID>();
		Temp->init(Condition);
		Instance = (UConditionBase*)Temp;
	}
	else if (Condition.ConditionType == ENUM_USE_CONDITION_TYPE::ConditionEffectState)
	{
		UConditionEffectState * Temp = NewObject<UConditionEffectState>();
		Temp->init(Condition);
		Instance = (UConditionBase*)Temp;
	}
	else
	{
		Instance = NewObject<UConditionBase>();
		Instance->init(Condition);
	}
	_conditions.Add(Instance);
}

UBuffReplaceCondition::UBuffReplaceCondition()
{
}

UBuffReplaceCondition::~UBuffReplaceCondition()
{
}

int32 UBuffReplaceCondition::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	if (_conditions.Num() == 0)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_FAILED;
	}
	return UObjectCondition::valid(caster, target, isCastValidCheck);
}

UBuffExtraCondition::UBuffExtraCondition()
{
}

UBuffExtraCondition::~UBuffExtraCondition()
{
}

int32 UBuffExtraCondition::valid(CS3Entity * caster, CS3Entity * target, bool isCastValidCheck)
{
	if (_conditions.Num() == 0)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_FAILED;
	}
	return UObjectCondition::valid(caster, target, isCastValidCheck);
}

CONTROL_COMPILE_OPTIMIZE_END