// Fill out your copyright notice in the Description page of Project Settings.


#include "SECondition18.h"
#include "GameData/Area/SpaceEventCircleArea.h"
#include "GameData/Area/SpaceEventSquareArea.h"
#include "Manager/MapManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "util/ConvertUtil.h"

/**
@ Param1: 圆形填1，多边形填2
@ Param2: 圆形填中点；多边形填二维坐标列表，用竖号隔开
@ Param3: 圆形填半径；多边形填z值上限
@ Param4: 多边形填z值下限
*/
void USECondition18::InitParams(FString _SpaceScriptID, INT32 _EventType, INT32 _EventID, FString _Param1, FString _Param2, FString _Param3, FString _Param4)
{
	Supper::InitParams(_SpaceScriptID, _EventType, _EventID, _Param1, _Param2, _Param3, _Param4);
	UUECS3GameInstance::Instance->MapManager->AddSpaceEventArea(_SpaceScriptID, EventType, EventID, FSTRING_TO_INT(_Param1), _Param2, _Param3, _Param4);
}

bool USECondition18::CheckCondition(KBEngine::Entity* _entity, TMap<FString, FString> Params)
{
	FString _EventType = *Params.Find(TEXT("eventType"));
	FString _EventID = *Params.Find(TEXT("eventID"));
	if ((FSTRING_TO_INT(_EventType) == EventType) && (FSTRING_TO_INT(_EventID) == EventID))
	{
		return true;
	}

	return false;
}