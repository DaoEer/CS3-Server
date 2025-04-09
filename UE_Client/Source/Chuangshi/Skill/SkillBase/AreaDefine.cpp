#include "AreaDefine.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
UArea::UArea()
{
	unitReference = 0;
	direReference = 0;
	maxHeight = 300.0;
	height = 0.0;
	offsetFront = 0.0;
	offsetLeft = 0.0;
	offsetUp = 0.0;
	offsetyaw = 0;
}

UArea::~UArea()
{
}

void UArea::load(FSKILL_HIT_AREA dictDat)
{
	TArray<FString> Param1 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param1);
	if (Param1.Num() > 0 && Param1[0] != "")
	{
		unitReference = FSTRING_TO_INT(Param1[0]);
	}
	if (Param1.Num() >= 2 && Param1[1] != "")
	{
		direReference = FSTRING_TO_INT(Param1[1]);
	}
	TArray<FString> Param3 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param3);
	if (Param3.Num() > 0 && Param3[0] != "")
	{
		offsetFront = FSTRING_TO_FLOAT(Param3[0]) * 100;
	}
	if (Param3.Num() >= 2 && Param3[1] != "")
	{
		offsetLeft = FSTRING_TO_FLOAT(Param3[1]) * 100;
	}
	if (Param3.Num() >= 3 && Param3[2] != "")
	{
		offsetUp = FSTRING_TO_FLOAT(Param3[2]) * 100;
	}
	if (Param3.Num() >= 4 && Param3[3] != "")
	{
		offsetyaw = FSTRING_TO_INT(Param3[3])%360;
		if (offsetyaw < 0)
		{
			offsetyaw += 360;
		}
	}
}

TArray<CS3Entity*> UArea::getObjectList(CS3Entity * caster, USkillTargetObjImpl * target)
{
	return TArray<CS3Entity*>();
}

FVector UArea::GetPosition(CS3Entity * caster, USkillTargetObjImpl * target)
{
	if (caster && caster == target->getObject())
	{
		return caster->Position();
	}

	if (unitReference == (int32)SKILL_HIT_AREA_UNIT::SKILL_HIT_AREA_UNIT_ABSOLUTE)
	{
		return FVector(0.0, 0.0, 0.0);
	}
	else if (unitReference == (int32)SKILL_HIT_AREA_UNIT::SKILL_HIT_AREA_UNIT_CASTER)
	{
		return caster->Position();
	}
	else if (unitReference == (int32)SKILL_HIT_AREA_UNIT::SKILL_HIT_AREA_UNIT_TARGET)
	{
		return target->getObjectPosition();
	}
	else
	{
		return FVector(0.0, 0.0, 0.0);
	}
	
}

FVector UArea::GetDirection(CS3Entity * caster, USkillTargetObjImpl * target)
{
	FVector direction = FVector(0.0, 0.0, 0.0);
	FVector casterPos = caster->Position();
	FVector targetPos = target->getObjectPosition();
	if (direReference == (int32)SKILL_HIT_AREA_DIRE::SKILL_HIT_AREA_DIRE_ABSOLUTE)
	{
		direction =  FVector(0.0, 0.0, 0.0);
	}
	else if (direReference == (int32)SKILL_HIT_AREA_DIRE::SKILL_HIT_AREA_DIRE_TARGET)
	{
		if (target->getType() == SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_POSITION)
		{
			direction = caster->Direction();
		}
		else
		{
			direction = target->getObject()->Direction();
		}
	}
	else if (direReference == (int32)SKILL_HIT_AREA_DIRE::SKILL_HIT_AREA_DIRE_CASTER_TO_TARGET)
	{
		float yaw = UGolbalBPFunctionLibrary::GetLookAtRotator(casterPos, targetPos).Yaw;
		if (yaw < 0)
		{
			yaw += 360.0;
		}
		direction = FVector(0.0, 0.0, yaw);
	}
	else if(direReference == (int32)SKILL_HIT_AREA_DIRE::SKILL_HIT_AREA_DIRE_TARGET_TO_CASTER)
	{
		float yaw = UGolbalBPFunctionLibrary::GetLookAtRotator(targetPos, casterPos).Yaw;
		if (yaw < 0)
		{
			yaw += 360.0;
		}
		direction = FVector(0.0, 0.0, yaw);
	}
	else if (direReference == (int32)SKILL_HIT_AREA_DIRE::SKILL_HIT_AREA_DIRE_CASTER)
	{
		direction = caster->Direction();
	}
	return direction;
}

TArray<CS3Entity*> UArea::filterHeight(FVector position, TArray<CS3Entity*> receivers)
{
	TArray<CS3Entity*> entityInArea;
	if (position == FVector(0.0, 0.0, 0.0))
	{
		return receivers;
	}

	float Height;
	if (height != 0.0)
	{
		Height = height;
	}
	else
	{
		Height = maxHeight;
	}
	for (auto receiver : receivers)
	{
		if (abs(position.Z - receiver->Position().Z) <= Height)
		{
			entityInArea.Add(receiver);
		}
	}
	return entityInArea;
}

FVector UArea::calculateOffset(FVector position, FVector direction)
{
	double yaw = direction.Z * PI / 180;
	if (offsetFront)
	{
		position.Y += offsetFront * FMath::Sin(yaw);
		position.X += offsetFront * FMath::Cos(yaw);
	}
	if (offsetLeft)
	{
		position.Y += offsetLeft * FMath::Sin(yaw - PI / 2);
		position.X += offsetLeft * FMath::Cos(yaw - PI / 2);
	}
	if (offsetUp)
	{
		position.Z += offsetUp;
	}
	
	return position;
}

float UArea::calculateYaw(float yaw)
{
	return yaw - (offsetyaw * PI / 180);
}

TArray<CS3Entity*> UArea::filterCircular(TArray<CS3Entity*> receivers, FVector centerPos, float radius)
{
	TArray<CS3Entity*> TempList;
	for (auto receiver : receivers)
	{
		if (FVector::Dist2D(centerPos, receiver->Position()) < radius)
		{
			TempList.Add(receiver);
		}
	}
	return TempList;
}

UNoRange::UNoRange()
{
}

UNoRange::~UNoRange()
{
}

void UNoRange::load(FSKILL_HIT_AREA dictDat)
{
	UArea::load(dictDat);
}

TArray<CS3Entity*> UNoRange::getObjectList(CS3Entity * caster, USkillTargetObjImpl * target)
{
	return TArray<CS3Entity*>();
}


USingle::USingle()
{
	unitReference = (int32)SKILL_HIT_AREA_UNIT::SKILL_HIT_AREA_UNIT_CASTER;
}

USingle::~USingle()
{
}

void USingle::load(FSKILL_HIT_AREA dictDat)
{
	UArea::load(dictDat);
	if (dictDat.Param1 != "")
	{
		unitReference = FSTRING_TO_INT(dictDat.Param1);
	}
}

TArray<CS3Entity*> USingle::getObjectList(CS3Entity * caster, USkillTargetObjImpl * target)
{
	TArray<CS3Entity*> TempList;
	if (unitReference == (int32)SKILL_HIT_AREA_UNIT::SKILL_HIT_AREA_UNIT_TARGET)
	{
		if (!target)
		{
			return TempList;
		}

		if (!IsValid(target))
		{
			return TempList;
		}

		if (target->getType() == SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_ENTITY)
		{
			TempList.Add(target->getObject());
		}
	}
	else if(unitReference== (int32)SKILL_HIT_AREA_UNIT::SKILL_HIT_AREA_UNIT_CASTER)
	{
		TempList.Add(caster);
	}
	return TempList;
}

USphere::USphere()
{
	radius = 0.0;
}

USphere::~USphere()
{
}

void USphere::load(FSKILL_HIT_AREA dictDat)
{
	UArea::load(dictDat);
	if (dictDat.Param2 != "")
	{
		radius = FSTRING_TO_FLOAT(dictDat.Param2)*100;
	}
}

TArray<CS3Entity*> USphere::getObjectList(CS3Entity * caster, USkillTargetObjImpl * target)
{
	TArray<CS3Entity*> circularList;
	FVector centerPos = GetPosition(caster, target);
	FVector direction = GetDirection(caster, target);
	centerPos = calculateOffset(centerPos, direction);
	TArray<CS3Entity*> TempList = UGolbalBPFunctionLibrary::GetCS3EntitysInRange("", radius, centerPos);
	circularList = TempList.FilterByPredicate([&](CS3Entity* entity)
	{
		if (entity)
		{
			if (FVector::Dist(centerPos, entity->Position()) < radius)
			{
				return true;
			}
		}
		return false;
	});
	return circularList;
}

URectangle::URectangle()
{
}

URectangle::~URectangle()
{
}

void URectangle::load(FSKILL_HIT_AREA dictDat)
{
	UArea::load(dictDat);
	TArray<FString> Param2 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param2);
	if (Param2.Num() >= 2 && Param2[0] != "" && Param2[1] != "")
	{
		length = FSTRING_TO_FLOAT(Param2[0]) * 100;
		width = FSTRING_TO_FLOAT(Param2[1]) * 100;
	}

	if (Param2.Num() >= 3 && Param2[2] != "")
	{
		height = FSTRING_TO_FLOAT(Param2[2]) * 100;
	}
}

TArray<CS3Entity*> URectangle::getObjectList(CS3Entity * caster, USkillTargetObjImpl * target)
{
	TArray<CS3Entity*> circularList;
	FVector centerPos = GetPosition(caster, target);
	FVector direction = GetDirection(caster, target);
	centerPos = calculateOffset(centerPos, direction);
	float yaw = calculateYaw(direction.Z *PI / 180);
	TArray<CS3Entity*> TempList = UGolbalBPFunctionLibrary::GetCS3EntitysInRange("", FMath::Sqrt(length*length + width * width), centerPos);
	circularList = TempList.FilterByPredicate([&, centerPos, yaw](CS3Entity* entity)
	{
		if (entity)
		{
			if (inArea(entity->Position(), centerPos, yaw))
			{
				return true;
			}
		}
		return false;
	});
	return filterHeight(centerPos, circularList);
}

bool URectangle::inArea(FVector dstPos, FVector srcPos, float yaw)
{
	dstPos.Y = srcPos.Y;
	return UGolbalBPFunctionLibrary::IsInRectangle(dstPos, srcPos, yaw, width, length);
}

UCircular::UCircular()
{
}

UCircular::~UCircular()
{
}

void UCircular::load(FSKILL_HIT_AREA dictDat)
{
	UArea::load(dictDat);
	TArray<FString> Param2 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param2);
	if (Param2.Num() >= 1 && Param2[0] != "")
	{
		radius = FSTRING_TO_FLOAT(Param2[0]) * 100;
	}

	if (Param2.Num() >= 2 && Param2[1] != "")
	{
		height = FSTRING_TO_FLOAT(Param2[1]) * 100;
	}
}

TArray<CS3Entity*> UCircular::getObjectList(CS3Entity * caster, USkillTargetObjImpl * target)
{
	FVector centerPos = GetPosition(caster, target);
	FVector direction = GetDirection(caster, target);
	centerPos = calculateOffset(centerPos, direction);
	TArray<CS3Entity*> circularList = UGolbalBPFunctionLibrary::GetCS3EntitysInRange("", radius, centerPos);
	return filterHeight(centerPos, circularList);
}

USector::USector()
{
}

USector::~USector()
{
}

void USector::load(FSKILL_HIT_AREA dictDat)
{
	UArea::load(dictDat);
	TArray<FString> Param2 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param2);
	if (Param2.Num() >= 2 && Param2[0] != "" && Param2[1] != "")
	{
		radius = FSTRING_TO_FLOAT(Param2[0]) * 100;
		angle = FSTRING_TO_FLOAT(Param2[1]) * 100;
	}

	if (Param2.Num() >= 3 && Param2[2] != "")
	{
		height = FSTRING_TO_FLOAT(Param2[2]) * 100;
	}
}

TArray<CS3Entity*> USector::getObjectList(CS3Entity * caster, USkillTargetObjImpl * target)
{
	TArray<CS3Entity*> circularList;
	FVector centerPos = GetPosition(caster, target);
	FVector direction = GetDirection(caster, target);
	centerPos = calculateOffset(centerPos, direction);
	float yaw = calculateYaw(direction.Z *PI / 180);
	TArray<CS3Entity*> TempList = UGolbalBPFunctionLibrary::GetCS3EntitysInRange("", radius, centerPos);
	circularList = TempList.FilterByPredicate([&, centerPos, yaw](CS3Entity* entity)
	{
		if (entity)
		{
			if (inArea(entity->Position(), centerPos, yaw))
			{
				return true;
			}
		}
		return false;
	});
	return filterHeight(centerPos, circularList);
}

bool USector::inArea(FVector dstPos, FVector srcPos, float yaw)
{
	dstPos.Y = srcPos.Y;
	return UGolbalBPFunctionLibrary::IsInSector(dstPos, srcPos, yaw, radius, angle);
}

UAnnulus::UAnnulus()
{
}

UAnnulus::~UAnnulus()
{
}

void UAnnulus::load(FSKILL_HIT_AREA dictDat)
{
	UArea::load(dictDat);
	TArray<FString> Param2 = UGolbalBPFunctionLibrary::SplitString(dictDat.Param2);
	if (Param2.Num() >= 1 && Param2[0] != "" )
	{
		innerDiameter = FSTRING_TO_FLOAT(Param2[0]) * 100;
		outerDiameter = innerDiameter;
	}
	if (Param2.Num() >= 2 &&  Param2[1] != "")
	{
		outerDiameter = FSTRING_TO_FLOAT(Param2[1]) * 100 + innerDiameter;
	}

	if (Param2.Num() >= 3 && Param2[2] != "")
	{
		height = FSTRING_TO_FLOAT(Param2[2]) * 100;
	}
}

TArray<CS3Entity*> UAnnulus::getObjectList(CS3Entity * caster, USkillTargetObjImpl * target)
{
	TArray<CS3Entity*> circularList;
	FVector centerPos = GetPosition(caster, target);
	FVector direction = GetDirection(caster, target);
	centerPos = calculateOffset(centerPos, direction);
	TArray<CS3Entity*> TempList = UGolbalBPFunctionLibrary::GetCS3EntitysInRange("", outerDiameter, centerPos);
	circularList = TempList.FilterByPredicate([&](CS3Entity* entity)
	{
		if (entity)
		{
			if (FVector::Dist2D(centerPos, entity->Position()) >= innerDiameter)
			{
				return true;
			}
		}
		return false;
	});
	return filterHeight(centerPos, circularList);
}

UArea* NewAreaInstance(FSKILL_HIT_AREA dictData)
{
	if (dictData.HitAreaType == ENUM_SKILIL_HIT_AREA_TYPE::NoRange)
	{
		UNoRange * Instance = NewObject<UNoRange>();
		Instance->load(dictData);
		return (UArea*)Instance;
	}
	else if (dictData.HitAreaType == ENUM_SKILIL_HIT_AREA_TYPE::Single)
	{
		USingle * Instance = NewObject<USingle>();
		Instance->load(dictData);
		return (UArea*)Instance;
	}
	else if(dictData.HitAreaType == ENUM_SKILIL_HIT_AREA_TYPE::Sphere)
	{
		USphere * Instance = NewObject<USphere>();
		Instance->load(dictData);
		return (UArea*)Instance;
	}
	else if (dictData.HitAreaType == ENUM_SKILIL_HIT_AREA_TYPE::Rectangle)
	{
		URectangle * Instance = NewObject<URectangle>();
		Instance->load(dictData);
		return (UArea*)Instance;
	}
	else if (dictData.HitAreaType == ENUM_SKILIL_HIT_AREA_TYPE::Circular)
	{
		UCircular * Instance = NewObject<UCircular>();
		Instance->load(dictData);
		return (UArea*)Instance;
	}
	else if (dictData.HitAreaType == ENUM_SKILIL_HIT_AREA_TYPE::Sector)
	{
		USector * Instance = NewObject<USector>();
		Instance->load(dictData);
		return (UArea*)Instance;
	}
	else if (dictData.HitAreaType == ENUM_SKILIL_HIT_AREA_TYPE::Annulus)
	{
		UAnnulus * Instance = NewObject<UAnnulus>();
		Instance->load(dictData);
		return (UArea*)Instance;
	}
	else
	{
		return nullptr;
	}
}

CONTROL_COMPILE_OPTIMIZE_END