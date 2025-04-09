#include "HitTypeDefine.h"
#include<ctime>
#include "Util/GolbalBPFunctionLibrary.h"

CONTROL_COMPILE_OPTIMIZE_START
UHitBase::UHitBase()
{
}

UHitBase::~UHitBase()
{
}

SKILL_HIT_TYPE UHitBase::isHit(CS3Entity * caster, CS3Entity * receiver)
{
	return SKILL_HIT_TYPE::SKILL_HIT_SUCCEED;
}

UHitDirect::UHitDirect()
{
}

UHitDirect::~UHitDirect()
{
}

SKILL_HIT_TYPE UHitDirect::isHit(CS3Entity * caster, CS3Entity * receiver)
{
	
	return SKILL_HIT_TYPE::SKILL_HIT_SUCCEED;
}

UHitDodge::UHitDodge()
{
}

UHitDodge::~UHitDodge()
{
}

SKILL_HIT_TYPE UHitDodge::isHit(CS3Entity * caster, CS3Entity * receiver)
{
	int32 hitrate = !caster ? 0:UGolbalBPFunctionLibrary::GetIntPropertyValue(caster->ID(), TEXT("hitrate"));
	int32 dodgerate = !receiver ? 0 : UGolbalBPFunctionLibrary::GetIntPropertyValue(receiver->ID(), TEXT("dodgerate"));
	/*
	if (hitrate == 0 || dodgerate == 0)
	{
		return SKILL_HIT_TYPE::SKILL_HIT_ERROR;
	}
	*/
	int32 hitValue = hitrate - dodgerate;
	
	if (hitValue < FMath::RandRange(0, 10000 - 1))
	{
		return SKILL_HIT_TYPE::SKILL_HIT_FAILED;
	}
	return SKILL_HIT_TYPE::SKILL_HIT_SUCCEED;
}


UHitTypeDefine::UHitTypeDefine()
{
}

UHitTypeDefine::~UHitTypeDefine()
{
}

UHitTypeDefine * UHitTypeDefine::GetInstance()
{
	if (Instance == nullptr)
	{
		Instance = NewObject<UHitTypeDefine>();
	}
	return Instance;
}

SKILL_HIT_TYPE UHitTypeDefine::isHit(ENUM_HIT_TYPE type, CS3Entity * caster, CS3Entity * receiver)
{
	SKILL_HIT_TYPE Result= SKILL_HIT_TYPE::SKILL_HIT_SUCCEED;
	if (type == ENUM_HIT_TYPE::HitDirect)
	{
		UHitDirect* hitDirect = NewObject <UHitDirect>();
		Result = hitDirect->isHit(caster, receiver);
		delete hitDirect;
		hitDirect = nullptr;
	}
	else if (type == ENUM_HIT_TYPE::HitDodge)
	{
		UHitDodge* hitDodge = NewObject <UHitDodge>();
		Result = hitDodge->isHit(caster, receiver);
		delete hitDodge;
		hitDodge = nullptr;
	}
	return Result;
}
CONTROL_COMPILE_OPTIMIZE_END