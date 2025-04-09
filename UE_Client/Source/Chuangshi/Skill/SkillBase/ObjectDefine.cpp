#include "ObjectDefine.h"
#include "Util/ConvertUtil.h"
#include "GameData/GameDeFine.h"



UTargetBase::UTargetBase()
{
}

UTargetBase::~UTargetBase()
{
	type = ENUM_CAST_TARGET_TYPE::TargetNothing;
}

void UTargetBase::init(const FSKILL_TABLE_DATA* dictDat)
{
	CastRangeMax = dictDat->CastRangeMax * 100;
}

ENUM_CAST_TARGET_TYPE UTargetBase::GetType()
{
	return type;
}

int32 UTargetBase::CastValid(CS3Entity * caster, USkillTargetObjImpl * target)
{
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

UTargetNothing::UTargetNothing()
{
	type = ENUM_CAST_TARGET_TYPE::TargetNothing;
}

UTargetNothing::~UTargetNothing()
{
}

void UTargetNothing::init(const FSKILL_TABLE_DATA* dictDat)
{
	CastRangeMax = dictDat->CastRangeMax * 100;
}

ENUM_CAST_TARGET_TYPE UTargetNothing::GetType()
{
	return type;
}

int32 UTargetNothing::CastValid(CS3Entity* caster, USkillTargetObjImpl* target)
{
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

UTargetPosition::UTargetPosition()
{
	type = ENUM_CAST_TARGET_TYPE::TargetPosition;
}

UTargetPosition::~UTargetPosition()
{
}

void UTargetPosition::init(const FSKILL_TABLE_DATA* dictDat)
{
	CastRangeMax = dictDat->CastRangeMax * 100;
}

ENUM_CAST_TARGET_TYPE UTargetPosition::GetType()
{
	return type;
}

int32 UTargetPosition::CastValid(CS3Entity* caster, USkillTargetObjImpl* target)
{
	if (!target && nullptr == target->getObject())
	{
		return (int32)SKILL_MESSAGE::SKILL_MISS_POSITION;
	}
	if (target->getType() != SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_POSITION)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_POSITION_ONLY;
	}		
	float distance =FVector::Dist2D(target->getObjectPosition(), caster->Position());
	if (CastRangeMax > 0.0 && distance > abs(CastRangeMax) + 150.0)
	{
		return (int32)SKILL_MESSAGE::SKILL_TOO_FAR;
	}
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

UTargetLock::UTargetLock()
{
	type = ENUM_CAST_TARGET_TYPE::TargetLock;
}

UTargetLock::~UTargetLock()
{
}

void UTargetLock::init(const FSKILL_TABLE_DATA* dictDat)
{
	CastRangeMax = dictDat->CastRangeMax *100;
}

ENUM_CAST_TARGET_TYPE UTargetLock::GetType()
{
	return type;
}

int32 UTargetLock::CastValid(CS3Entity* caster, USkillTargetObjImpl* target)
{
	CS3Entity* tObject = target->getObject();
	if (!caster && !tObject)
	{
		return (int32)SKILL_MESSAGE::SKILL_MISS_TARGET;
	}

	if (target->getType() != SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_ENTITY)
	{
		return (int32)SKILL_MESSAGE::SKILL_CAST_ENTITY_ONLY;
	}

	float distanceBB = FVector::Dist2D(tObject->Position(), caster->Position());
	if (CastRangeMax > 0.0 && distanceBB > abs(CastRangeMax) + 150.0)
	{
		return (int32)SKILL_MESSAGE::SKILL_TOO_FAR;
	}
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}


UTargetBase * ObjectDefineNewInstance(ENUM_CAST_TARGET_TYPE type)
{
	if (type == ENUM_CAST_TARGET_TYPE::TargetLock)
	{
		UTargetLock* Temp = NewObject <UTargetLock>();
		return (UTargetBase*)Temp;
	}
	else if (type == ENUM_CAST_TARGET_TYPE::TargetPosition)
	{
		UTargetPosition* Temp = NewObject <UTargetPosition>();
		return (UTargetBase*)Temp;
	}
	else
	{
		return NewObject <UTargetBase>();
	}
}
