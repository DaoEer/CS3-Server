#include "BuffClientHitBack.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/StateInterface.h"
#include "Interface/Monster/CSkillInterface.h"



CONTROL_COMPILE_OPTIMIZE_START
UBuffClientHitBack::UBuffClientHitBack()
{
	_className = "BuffClientHitBack";
}

UBuffClientHitBack::~UBuffClientHitBack()
{
}

void UBuffClientHitBack::init(FString BuffID, const FBUFF_TABLE_DATA * dictDat)
{
	UBuffClientHit::init(BuffID, dictDat);
	if (dictDat->Param1 != "")
	{
		TArray<FString> actionInfos = UGolbalBPFunctionLibrary::SplitString(dictDat->Param1, false, TEXT(":"));
		_actionID = actionInfos[0];
		if (actionInfos.Num() > 1)
		{
			_actionBeginTime = FSTRING_TO_FLOAT(actionInfos[1]);
		}
	}
	if (dictDat->Param2 != "")
	{
		TArray<FString> getUpActionInfos = UGolbalBPFunctionLibrary::SplitString(dictDat->Param2, false, TEXT(":"));
		_endActionID = getUpActionInfos[0];
		_getUpActionID.Add(getUpActionInfos[0]);
		if (getUpActionInfos.Num() >= 2)
		{
			_getUpActionBeginTime.Add(getUpActionInfos[1]);
		} else {
			_getUpActionBeginTime.Add("0.0");
		}
	}
	if (dictDat->Param3 != "")
	{
		TArray<FString> infos = UGolbalBPFunctionLibrary::SplitString(dictDat->Param3, false, TEXT("|"));
		_moveTime = FSTRING_TO_FLOAT(infos[0]);
		if (infos.Num() >= 2)
		{
			_getUpActionDelayTime = FSTRING_TO_FLOAT(infos[1]);
		}
	}

	if (dictDat->Param4 != "")
	{
		TArray<FString> dist = UGolbalBPFunctionLibrary::SplitString(dictDat->Param4, false, TEXT("|"));
		if (dist.Num() >= 2)
		{
			_distMin = FSTRING_TO_FLOAT(dist[0]) *100;
			_distMax = FSTRING_TO_FLOAT(dist[1]) * 100;
		} else {
			if (dictDat->Param4.StartsWith(TEXT("|")))
			{
				_distMin = 0.0;
				_distMax = FSTRING_TO_FLOAT(dist[0]) * 100;
			} else {
				_distMin = FSTRING_TO_FLOAT(dist[0]) * 100;
				_distMax = FSTRING_TO_FLOAT(dist[0]) * 100;
			}
		}
	}
	if (dictDat->Param5 != "")
	{
		TArray<FString> hitType = UGolbalBPFunctionLibrary::SplitString(dictDat->Param5, false, TEXT("|"));
		_directionType = (BUFF_HIT_DIRECTION)FSTRING_TO_INT(hitType[0]);
		if (hitType.Num() >= 2)
		{
			_hitBackType = (BUFF_HIT_TYPE)FSTRING_TO_INT(hitType[1]);
		}
	}
}

bool UBuffClientHitBack::receive(CS3Entity * caster, CS3Entity * receiver)
{
	if (!addBuffCheck(caster, receiver))
	{
		return false;
	}
	if (_replaceCondition->valid(caster, receiver, true) == (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		for (auto effect : _replaceEffectList)
		{
			if (effect->canEffect(nullptr, caster, receiver))
			{
				effect->onReceive(nullptr, caster, receiver);
			}
		}
		return false;
	}
	receiveSuccess(caster, receiver);
	return true;
}

bool UBuffClientHitBack::receiveSuccess(CS3Entity * caster, CS3Entity * receiver)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return false;
	}
	for (auto i : CSkillInterface->getAttrBuffs())
	{
		UBuff * buff = CSkillInterface->getBuff(i.Value->buffID);
		if (i.Value->className == "BuffClientHitBack")
		{
			CSkillInterface->removeBuffByID(i.Value->buffID);
		}
	}
	return UBuffClientHit::receiveSuccess(caster, receiver);
}

bool UBuffClientHitBack::addBuffCheck(CS3Entity * caster, CS3Entity * receiver)
{
	return UBuffClientHit::addBuffCheck(caster, receiver);
}

void UBuffClientHitBack::doBegin(CS3Entity * receiver, UBuffDataType * buffData)
{
	UBuffClientHit::doBegin(receiver, buffData);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillAddEffectState(EFFECT_STATE::EFFECT_STATE_HIT_BACK);
	}
	doHitBack(receiver, buffData);
	
}

void UBuffClientHitBack::doEnd(CS3Entity * receiver, UBuffDataType * buffData, BUFF_END_RESON reason)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkillRemoveEffectState(EFFECT_STATE::EFFECT_STATE_HIT_BACK);
	}
	endHitBack(receiver, buffData);
	UBuffClientHit::doEnd(receiver, buffData, reason);
}

void UBuffClientHitBack::doHitBack(CS3Entity * receiver, UBuffDataType * buffData)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	CS3Entity * caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(buffData->casterID);
	AServerCharacter* receiverCharacter = Cast<AServerCharacter>(receiver->Actor());
	if (nullptr != caster && IsValid(receiverCharacter) && !receiverCharacter->HasFlag(ENTITY_FLAG::FLAG_CANT_MOVE_AND_ROTATE))
	{
		///目标朝向扩展
		FVector recvDir = FVector(receiver->Direction());
		if (_directionType == BUFF_HIT_DIRECTION::BUFF_HIT_TYPE_CASTER_DIRECTION)
		{
			recvDir.Z = caster->Direction().Z;
		}
		else if (_directionType == BUFF_HIT_DIRECTION::BUFF_HIT_TYPE_CASTER_RDIRECTION)
		{
			recvDir.Z = caster->Direction().Z + 180.0f;
		}
		else if (_directionType == BUFF_HIT_DIRECTION::BUFF_HIT_TYPE_CATORE_DIRECTION)
		{
			if (receiver->Position().X == caster->Position().X && receiver->Position().Y == caster->Position().Y)
			{
				recvDir.Z = caster->Direction().Z;
			} else {
				FVector dir = receiver->Position() - caster->Position();
				float z = FMath::Atan2(dir.Y, dir.X);
				recvDir.Z = z * 180.0f / PI;
			}
		}
		else if (_directionType == BUFF_HIT_DIRECTION::BUFF_HIT_TYPE_CATORE_RDIRECTION)
		{
			if (receiver->Position().X == caster->Position().X && receiver->Position().Y == caster->Position().Y)
			{
				recvDir.Z = receiver->Direction().Z;
			} else {
				FVector dir = caster->Position() - receiver->Position();
				float z = FMath::Atan2(dir.Y, dir.X);
				recvDir.Z = z * 180.0f / PI;
			}
		}
		else if (_directionType == BUFF_HIT_DIRECTION::BUFF_HIT_TYPE_RECEIVER_DIRECTION)
		{
			recvDir.Z = receiver->Direction().Z;
		}
		else if (_directionType == BUFF_HIT_DIRECTION::BUFF_HIT_TYPE_RECEIVER_RDIRECTION)
		{
			recvDir.Z += 180.0f;
		}

		CSkillInterface->CSkillChangeDirection(recvDir, 1);
	}
	int32 casterID = 0;
	float yaw = caster->Direction().Z;
	if (nullptr != caster)
	{
		casterID = caster->ID();
		///击退朝向扩展
		if (_hitBackType == BUFF_HIT_TYPE::BUFF_HIT_TYPE_CASTER_FORWARD)
		{
			yaw = caster->Direction().Z;
		}
		else if (_hitBackType == BUFF_HIT_TYPE::BUFF_HIT_TYPE_CASTER_REAR)
		{
			yaw = caster->Direction().Z + 180.0f;
		}
		else if (_hitBackType == BUFF_HIT_TYPE::BUFF_HIT_TYPE_CATORE_FORWARD)
		{
			if (receiver->Position().X == caster->Position().X && receiver->Position().Y == caster->Position().Y)
			{
				yaw = caster->Direction().Z;
			} else {
				FVector dir = receiver->Position() - caster->Position();
				float z = FMath::Atan2(dir.Y, dir.X);
				yaw = z * 180 / PI;
			}
		}
		else if (_hitBackType == BUFF_HIT_TYPE::BUFF_HIT_TYPE_CATORE_REAR)
		{
			if (receiver->Position().X == caster->Position().X && receiver->Position().Y == caster->Position().Y)
			{
				yaw = receiver->Direction().Z;
			} else {
				FVector dir = caster->Position() - receiver->Position();
				float z = FMath::Atan2(dir.Y, dir.X);
				yaw = z * 180 / PI;
			}
		}
		else if (_hitBackType == BUFF_HIT_TYPE::BUFF_HIT_TYPE_RECEIVER_FORWARD)
		{
			yaw = receiver->Direction().Z;
		}
		else if (_hitBackType == BUFF_HIT_TYPE::BUFF_HIT_TYPE_RECEIVER_REAR)
		{
			yaw = receiver->Direction().Z + 180.0f;
		}
	}
	else
	{
		yaw = receiver->Direction().Z + 180.0f;
	}
	yaw = yaw * PI / 180.0f;
	FVector pos = FVector(receiver->Position());
	FVector dest = FVector(0.0f,0.0f,0.0f);
	float moveSpeed = 0.0f;
	if (_moveTime > 0.0)
	{
		float backDistance = FMath::RandRange(0.0f, 1.0f)*(_distMax - _distMin) + _distMin;
		moveSpeed = backDistance / _moveTime;
		dest = FVector(backDistance  * FMath::Cos(yaw), backDistance  * FMath::Sin(yaw), 0.0f);
		pos = FVector(receiver->Position() + dest);
	}

	CSkillInterface->CSkillDoHitBack(casterID, moveSpeed, pos, _actionID, _actionBeginTime);
	CSkillInterface->addHitFlyTimer(_getUpActionDelayTime, casterID, _getUpActionID, "", "", _getUpActionBeginTime);
}

void UBuffClientHitBack::endHitBack(CS3Entity * receiver, UBuffDataType * buffData)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	/*
	UGameObjectInterface * Interface = Cast<UGameObjectInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("GameObjectInterface"), receiver->ID()));
	if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{

	} else {
		CSkillInterface->CSkillStopMove(MOVETYPE::MOVETYPE_HIT_BACK);
	}
	*/
	CSkillInterface->CSkillOnEndHitBack(buffData->casterID, _actionID, _endActionID);
	CSkillInterface->delHitFlyTimer();
}

CONTROL_COMPILE_OPTIMIZE_END