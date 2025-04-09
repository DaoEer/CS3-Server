// Fill out your copyright notice in the Description page of Project Settings.


#include "SECondition3.h"


void USECondition3::InitParams(FString _SpaceScriptID, INT32 _EventType, INT32 _EventID, FString _Param1, FString _Param2, FString _Param3, FString _Param4)
{
	Supper::InitParams(_SpaceScriptID, _EventType, _EventID, _Param1, _Param2, _Param3, _Param4);
	NewArea = _Param1;
}

bool USECondition3::CheckCondition(KBEngine::Entity* _entity, TMap<FString, FString> Params)
{
	FString newArea = *Params.Find(TEXT("newArea"));
	return newArea == NewArea;
}

