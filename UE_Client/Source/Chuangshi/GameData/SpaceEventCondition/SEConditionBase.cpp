// Fill out your copyright notice in the Description page of Project Settings.


#include "SEConditionBase.h"

void USEConditionBase::InitParams(FString _SpaceScriptID, INT32 _EventType, INT32 _EventID, FString _Param1, FString _Param2, FString _Param3, FString _Param4)
{
	EventType = _EventType;
	EventID = _EventID;
}

bool USEConditionBase::CheckCondition(KBEngine::Entity* _entity, TMap<FString, FString> Params)
{
	return false;
}
