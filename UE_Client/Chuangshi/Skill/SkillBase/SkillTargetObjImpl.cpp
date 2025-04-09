#include "SkillTargetObjImpl.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3GameInstance.h"

USkillTargetObjImpl::USkillTargetObjImpl()
{
}

USkillTargetObjImpl::~USkillTargetObjImpl()
{
}

SKILL_TARGET_TYPE USkillTargetObjImpl::getType()
{
	return SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_NONE;
}

CS3Entity * USkillTargetObjImpl::getObject()
{
	return nullptr;
}

FVector USkillTargetObjImpl::getObjectPosition()
{
	return FVector::ZeroVector;
}

void USkillTargetObjImpl::onSkillBegin(CS3Entity * caster)
{
}


USkillTargetObjNone::USkillTargetObjNone()
{
	_type = SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_NONE;
}

USkillTargetObjNone::~USkillTargetObjNone()
{
}

SKILL_TARGET_TYPE USkillTargetObjNone::getType()
{
	return _type;
}

CS3Entity * USkillTargetObjNone::getObject()
{
	return nullptr;
}

FVector USkillTargetObjNone::getObjectPosition()
{
	return FVector::ZeroVector;
}

USkillTargetObjEntity::USkillTargetObjEntity()
{
	_type = SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_ENTITY;
	_entityID = 0;
}

USkillTargetObjEntity::~USkillTargetObjEntity()
{
}

void USkillTargetObjEntity::init(CS3Entity * entity)
{
	_entityID = entity->ID();
}

SKILL_TARGET_TYPE USkillTargetObjEntity::getType()
{
	return _type;
}

CS3Entity * USkillTargetObjEntity::getObject()
{
	return (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(_entityID);
}

FVector USkillTargetObjEntity::getObjectPosition()
{
	CS3Entity * entity = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(_entityID);
	if (!entity)
	{
		return FVector::ZeroVector;
	}
	return entity->Position();
}

void USkillTargetObjEntity::onSkillBegin(CS3Entity * caster)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->setReceiverID(_entityID);
	}
}

USkillTargetObjPosition::USkillTargetObjPosition()
{
	_type = SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_POSITION;
	_entityPosition = FVector::ZeroVector;
}

USkillTargetObjPosition::~USkillTargetObjPosition()
{
}

void USkillTargetObjPosition::init(FVector position)
{
	_entityPosition = position;
}

SKILL_TARGET_TYPE USkillTargetObjPosition::getType()
{
	return _type;
}

FVector USkillTargetObjPosition::getObjectPosition()
{
	return _entityPosition;
}
