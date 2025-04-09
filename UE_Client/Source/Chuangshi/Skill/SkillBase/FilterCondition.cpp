#include "FilterCondition.h"
#include <ctime>
#include "Util/ConvertUtil.h"
#include "GameData/GameDeFine.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Skill.h"

CONTROL_COMPILE_OPTIMIZE_START
UFilterBase::UFilterBase()
{
}

UFilterBase::~UFilterBase()
{
}

void UFilterBase::init(FRECEIVER_FLITER_CONDITION dictDat)
{
}

TArray<CS3Entity*> UFilterBase::filter(CS3Entity * caster, USkillTargetObjImpl * target, TArray<CS3Entity*> receiverList)
{
	return receiverList;
}

UOrderByRandom::UOrderByRandom()
{
	_maxNumber = 0;
}

UOrderByRandom::~UOrderByRandom()
{
}

void UOrderByRandom::init(FRECEIVER_FLITER_CONDITION dictDat)
{
	if (dictDat.Param1 != "")
	{
		_maxNumber = FSTRING_TO_INT(dictDat.Param1);
	}
}

TArray<CS3Entity*> UOrderByRandom::filter(CS3Entity * caster, USkillTargetObjImpl * target, TArray<CS3Entity*> receiverList)
{
	TArray<CS3Entity*> TempList;

	//´òÂÒÁÐ±í
	int32 Num = receiverList.Num();
	
	for (int i = Num; i > 1; i--)
	{
		int cur = Num - i + FMath::RandRange(0, i - 1);
		CS3Entity* temp = receiverList[Num - i];
		receiverList.Insert(receiverList[cur], Num - i);
		receiverList.Insert(temp, cur);
	}
	
	if (_maxNumber >= Num || _maxNumber <= 0)
	{
		TempList = receiverList;
	}
	else
	{
		for (int i = 0; i < _maxNumber; ++i)
		{
			TempList.Add(receiverList[i]);
		}
	}

	return TempList;
}

UOrderByProperty::UOrderByProperty()
{
	_property = "";
	_operation = 0;
	_maxNumber = 0;
}

UOrderByProperty::~UOrderByProperty()
{
}

void UOrderByProperty::init(FRECEIVER_FLITER_CONDITION dictDat)
{
	_property = dictDat.Param1;
	if (dictDat.Param2 != "")
	{
		_operation = FSTRING_TO_INT(dictDat.Param2);
	}
	if (dictDat.Param3 != "")
	{
		_maxNumber = FSTRING_TO_INT(dictDat.Param3);
	}
}

TArray<CS3Entity*> UOrderByProperty::filter(CS3Entity * caster, USkillTargetObjImpl * target, TArray<CS3Entity*> receiverList)
{
	TArray<CS3Entity*> TempList;
	TArray<CS3Entity*> list1 = receiverList.FilterByPredicate([&](CS3Entity* entity)
	{
		if (entity)
		{
			FVariant propvalue = entity->GetDefinedProperty(_property);
			if (propvalue != FVariant(NULL))
			{
				return true;
			}
		}
		return false;
	});

	TArray<CS3Entity*> list2 = receiverList.FilterByPredicate([&](CS3Entity* entity)
	{
		if (entity)
		{
			FVariant propvalue = entity->GetDefinedProperty(_property);
			if (propvalue = FVariant(NULL))
			{
				return true;
			}
		}
		return false;
	});
	list1.Sort([&](CS3Entity& entity1, CS3Entity& entity2)
	{
		FVariant propvalue1 = entity1.GetDefinedProperty(_property);
		FVariant propvalue2 = entity2.GetDefinedProperty(_property);
		bool result = true;
		switch (propvalue1.GetType())
		{
			case EVariantTypes::UInt8:
			{
				result =  propvalue1.GetValue<uint8>() > propvalue2.GetValue<uint8>();
			}
			case EVariantTypes::Int32:
			{
				result =  propvalue1.GetValue<int32>() > propvalue2.GetValue<int32>();
			}
			case EVariantTypes::UInt32:
			{
				result =  propvalue1.GetValue<uint32>() > propvalue2.GetValue<uint32>();
			}
			case EVariantTypes::Int64:
			{
				result = propvalue1.GetValue<int64>() > propvalue2.GetValue<int64>();
			}
			case EVariantTypes::UInt64:
			{
				result = propvalue1.GetValue<uint64>() > propvalue2.GetValue<uint64>();
			}
			case EVariantTypes::Float :
			{
				result = propvalue1.GetValue<float>() > propvalue2.GetValue<float>();
			}
			default:
			{
				result = true;
			}
		}
		if (_operation != 0)
		{
			return result;
		}else{
			return !result;
		}
	});
	list1.Append(list2);

	if (_maxNumber >= receiverList.Num() || _maxNumber <= 0)
	{
		TempList = list1;
	}
	else
	{
		for (int i = 0; i < _maxNumber; ++i)
		{
			TempList.Add(list1[i]);
		}
	}
	return TempList;
}

UOrderByDistanceToCaster::UOrderByDistanceToCaster()
{
	_property = "";
	_operation = 0;
	_maxNumber = 0;
}

UOrderByDistanceToCaster::~UOrderByDistanceToCaster()
{
}

void UOrderByDistanceToCaster::init(FRECEIVER_FLITER_CONDITION dictDat)
{
	_property = dictDat.Param1;
	if (dictDat.Param2 != "")
	{
		_operation = FSTRING_TO_INT(dictDat.Param2);
	}
	if (dictDat.Param3 != "")
	{
		_maxNumber = FSTRING_TO_INT(dictDat.Param3);
	}
}

TArray<CS3Entity*> UOrderByDistanceToCaster::filter(CS3Entity * caster, USkillTargetObjImpl * target, TArray<CS3Entity*> receiverList)
{
	TArray<CS3Entity*> TempList;
	if (_operation)
	{
		if (_property == "3D")
		{
			receiverList.Sort([caster](CS3Entity& entity1, CS3Entity& entity2)
			{
				float distance1 = FVector::Dist(caster->Position(), entity1.Position());
				float distance2 = FVector::Dist(caster->Position(), entity2.Position());
				return distance1 < distance2;
			});
		}
		else if (_property == "2D")
		{
			receiverList.Sort([caster](CS3Entity& entity1, CS3Entity& entity2)
			{
				float distance1 = FVector::Dist2D(caster->Position(), entity1.Position());
				float distance2 = FVector::Dist2D(caster->Position(), entity2.Position());
				return distance1 < distance2;
			});
		}
		else if (_property == "Z")
		{
			receiverList.Sort([caster](CS3Entity& entity1, CS3Entity& entity2)
			{
				double distance1 = abs(caster->Position().Z - entity1.Position().Z);
				double distance2 = abs(caster->Position().Z - entity2.Position().Z);
				return distance1 < distance2; 
			});
		}

	}
	else
	{
		if (_property == "3D")
		{
			receiverList.Sort([caster](CS3Entity& entity1, CS3Entity& entity2)
			{
				float distance1 = FVector::Dist(caster->Position(), entity1.Position());
				float distance2 = FVector::Dist(caster->Position(), entity2.Position());
				return distance1 > distance2;
			});
		}
		else if (_property == "2D")
		{
			receiverList.Sort([caster](CS3Entity& entity1, CS3Entity& entity2)
			{
				float distance1 = FVector::Dist2D(caster->Position(), entity1.Position());
				float distance2 = FVector::Dist2D(caster->Position(), entity2.Position());
				return distance1 > distance2;
			});
		}
		else if (_property == "Z")
		{
			receiverList.Sort([caster](CS3Entity& entity1, CS3Entity& entity2)
			{
				double distance1 = abs(caster->Position().Z - entity1.Position().Z);
				double distance2 = abs(caster->Position().Z - entity2.Position().Z);
				return distance1 > distance2;
			});
		}

	}
	if (_maxNumber >= receiverList.Num() || _maxNumber <= 0)
	{
		TempList = receiverList;
	}
	else
	{
		for (int i = 0; i < _maxNumber; ++i)
		{
			TempList.Add(receiverList[i]);
		}
	}
	return TempList;
}

UOrderByDistanceToTarget::UOrderByDistanceToTarget()
{
	_property = "";
	_operation = 0;
	_maxNumber = 0;
}

UOrderByDistanceToTarget::~UOrderByDistanceToTarget()
{
}

void UOrderByDistanceToTarget::init(FRECEIVER_FLITER_CONDITION dictDat)
{
	_property = dictDat.Param1;
	if (dictDat.Param2 != "")
	{
		_operation = FSTRING_TO_INT(dictDat.Param2);
	}
	if (dictDat.Param3 != "")
	{
		_maxNumber = FSTRING_TO_INT(dictDat.Param3);
	}
}

TArray<CS3Entity*> UOrderByDistanceToTarget::filter(CS3Entity * caster, USkillTargetObjImpl * target, TArray<CS3Entity*> receiverList)
{
	TArray<CS3Entity*> TempList;
	FVector TargetPosition = target->getObjectPosition();
	if (_operation)
	{
		if (_property == "3D")
		{
			receiverList.Sort([TargetPosition](CS3Entity& entity1, CS3Entity& entity2)
			{
				float distance1 = FVector::Dist(TargetPosition, entity1.Position());
				float distance2 = FVector::Dist(TargetPosition, entity2.Position());
				return distance1 < distance2;
			});
		}
		else if (_property == "2D")
		{
			receiverList.Sort([TargetPosition](CS3Entity& entity1, CS3Entity& entity2)
			{
				float distance1 = FVector::Dist2D(TargetPosition, entity1.Position());
				float distance2 = FVector::Dist2D(TargetPosition, entity2.Position());
				return distance1 < distance2;
			});
		}
		else if (_property == "Z")
		{
			receiverList.Sort([TargetPosition](CS3Entity& entity1, CS3Entity& entity2)
			{
				double distance1 = abs(TargetPosition.Z - entity1.Position().Z);
				double distance2 = abs(TargetPosition.Z - entity2.Position().Z);
				return distance1 < distance2;
			});
		}

	}
	else
	{
		if (_property == "3D")
		{
			receiverList.Sort([TargetPosition](CS3Entity& entity1, CS3Entity& entity2)
			{
				float distance1 = FVector::Dist(TargetPosition, entity1.Position());
				float distance2 = FVector::Dist(TargetPosition, entity2.Position());
				return distance1 > distance2;
			});
		}
		else if (_property == "2D")
		{
			receiverList.Sort([TargetPosition](CS3Entity& entity1, CS3Entity& entity2)
			{
				float distance1 = FVector::Dist2D(TargetPosition, entity1.Position());
				float distance2 = FVector::Dist2D(TargetPosition, entity2.Position());
				return distance1 > distance2;
			});
		}
		else if (_property == "Z")
		{
			receiverList.Sort([TargetPosition](CS3Entity& entity1, CS3Entity& entity2)
			{
				double distance1 = abs(TargetPosition.Z - entity1.Position().Z);
				double distance2 = abs(TargetPosition.Z - entity2.Position().Z);
				return distance1 > distance2;
			});
		}

	}
	if (_maxNumber >= receiverList.Num() || _maxNumber <= 0)
	{
		TempList = receiverList;
	}
	else
	{
		for (int i = 0; i < _maxNumber; ++i)
		{
			TempList.Add(receiverList[i]);
		}
	}
	return TempList;
}

UFilterCondition::UFilterCondition()
{
}

UFilterCondition::~UFilterCondition()
{
}

void UFilterCondition::init(TArray<FRECEIVER_FLITER_CONDITION> conditionList)
{
	if (conditionList.Num() <= 0)
	{
		return;
	}
	for (auto condition : conditionList)
	{
		add(condition);
	}
}

TArray<CS3Entity*> UFilterCondition::filter(USkill * Skill, CS3Entity * caster, USkillTargetObjImpl * target, TArray<CS3Entity*> receiverList)
{
	for (auto i : _conditions)
	{
		receiverList = i->filter(caster, target, receiverList);
	}
	return receiverList;
}

void UFilterCondition::add(FRECEIVER_FLITER_CONDITION Condition)
{
	UFilterBase* Instance = nullptr;
	if (Condition.FliterConditionType == ENUM_FLITER_CONDITION_TYPE::OrderByRandom)
	{
		UOrderByRandom * Temp = NewObject<UOrderByRandom>();
		Temp->init(Condition);
		Instance = (UFilterBase*)Temp;
	}
	else if(Condition.FliterConditionType == ENUM_FLITER_CONDITION_TYPE::OrderByProperty)
	{
		UOrderByProperty * Temp = NewObject<UOrderByProperty>();
		Temp->init(Condition);
		Instance = (UFilterBase*)Temp;
	}
	else if (Condition.FliterConditionType == ENUM_FLITER_CONDITION_TYPE::OrderByDistanceToCaster)
	{
		UOrderByDistanceToCaster * Temp = NewObject<UOrderByDistanceToCaster>();
		Temp->init(Condition);
		Instance = (UFilterBase*)Temp;
	}
	else if (Condition.FliterConditionType == ENUM_FLITER_CONDITION_TYPE::OrderByDistanceToTarget)
	{
		UOrderByDistanceToTarget * Temp = NewObject<UOrderByDistanceToTarget>();
		Temp->init(Condition);
		Instance = (UFilterBase*)Temp;
	}
	else
	{
		Instance = NewObject<UFilterBase>();
		Instance->init(Condition);
	}
	_conditions.Add(Instance);
}

CONTROL_COMPILE_OPTIMIZE_END