// Fill out your copyright notice in the Description page of Project Settings.


#include "ActionManager.h"
//UE4
#include "Animation/AnimMontage.h"
//CS3Êý¾Ý
#include "GameData/CharacterData.h"
#include "GameData/EnumCsvDefine.h"
//CS3
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CfgManager.h"
#include "Chuangshi.h"
CONTROL_COMPILE_OPTIMIZE_START

UActionManager::UActionManager()
{
}

UActionManager::~UActionManager()
{
}

UActionManager* UActionManager::GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<UActionManager>();
}

bool UActionManager::IsBreakAction(FACTION_DATA CurActionData, FACTION_DATA NewActionData)
{
	return IsBreakActionByType(CurActionData.ActionType, NewActionData.ActionType);
}

bool UActionManager::IsBreakActionByType(ACTION_TYPE_ENUM CurActionType, ACTION_TYPE_ENUM NewActionType)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ACTION_BREAK);
	const FACTION_BREAK_DATA* CurActionBreakData = ConfigTable->GetRow<FACTION_BREAK_DATA>(INT_TO_FSTRING((int)CurActionType));
	if (!CurActionBreakData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UActionManager::IsBreakActionByType : CurActionBreakData!"));
		return true;
	}

	int32 DataValue = 0;
	switch (NewActionType)
	{
	case ACTION_TYPE_ENUM::ACTION_TYPE_RANDOM:
		DataValue = CurActionBreakData->RandomState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_STANDBY:
		DataValue = CurActionBreakData->StandByState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_MOVE:
		DataValue = CurActionBreakData->MoveState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_HIT:
		DataValue = CurActionBreakData->HitState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_SHIFT:
		DataValue = CurActionBreakData->ShiftState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_JUMP_START:
		DataValue = CurActionBreakData->JumpStartState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_JUMP_AIR:
		DataValue = CurActionBreakData->JumpAirState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_JUMP_END:
		DataValue = CurActionBreakData->JumpEndState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_JUMP_MOVE_END:
		DataValue = CurActionBreakData->JumpEndMoveState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_DIZZY:
		DataValue = CurActionBreakData->DizzyState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_SLEEP:
		DataValue = CurActionBreakData->SleepState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_HIT_BACK:
		DataValue = CurActionBreakData->HitBackState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_HIT_FLY_FLOOR:
		DataValue = CurActionBreakData->HitFlyFloorState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_HIT_FLY_GET_UP:
		DataValue = CurActionBreakData->HitFlyFloorGetState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_DEATH:
		DataValue = CurActionBreakData->DeathState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_REBORN:
		DataValue = CurActionBreakData->RebornState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_SKILL:
		DataValue = CurActionBreakData->SkillState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_SHOW:
		DataValue = CurActionBreakData->ShowState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_CARRIER:
		DataValue = CurActionBreakData->CarrierState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_FACE:
		DataValue = CurActionBreakData->FaceState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_FILTER:
		DataValue = CurActionBreakData->FilterState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_FRONT_SHOW:
		DataValue = CurActionBreakData->FrontShowState;
		break;
	case ACTION_TYPE_ENUM::ACTION_TYPE_CLIMB_LADDER:
		DataValue = CurActionBreakData->ClimbLadderState;
		break;
	default:
		break;
	}
	return DataValue == 1 ? true : false;
}

FACTION_DATA UActionManager::GetActionDataById(TSoftObjectPtr<UDataTable> configPath, FName ActionId)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const FACTION_DATA* ActionData = CfgManager->GetTableByPath(configPath)->GetRow<FACTION_DATA>(ActionId.ToString());
	FACTION_DATA NewActionData = FACTION_DATA();
	if (ActionData)
	{
		if (ActionData->AnimPath.ToSoftObjectPath().IsValid())
		{
			NewActionData = *ActionData;
			NewActionData.Id = ActionData->RowName;
		}
		else
		{
			char str[100];
			sprintf_s(str, "ActionId=%ls, [AnimPath value = none]", *ActionId.ToString());
			GEngine->AddOnScreenDebugMessage(-1, 3.0f, FColor::Red, str);
		}
	}
	return NewActionData;
}

FACTION_DATA UActionManager::GetActionDataByPose(TSoftObjectPtr<UDataTable> configPath, ACTION_POSE_ENUM ActionPose)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UDataTable* TableData = CfgManager->GetTableByPath(configPath)->GetBaseTable();
	FACTION_DATA NewActionData = FACTION_DATA();
	for (auto it : TableData->GetRowMap())
	{
		FACTION_DATA* ActionData = (FACTION_DATA*)it.Value;
		if (ActionData->ActionPose == ActionPose)
		{
			ActionData->Id = it.Key;
			NewActionData = *ActionData;
			break;
		}
	}
	return NewActionData;
}

ACTION_GROUND_TYPE_ENUM UActionManager::GetActionGround(FACTION_DATA& ActionData)
{
	ACTION_GROUND_TYPE_ENUM GroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_NULL;
	if (!ActionData.Id.IsNone())
	{
		switch (ActionData.AnimType)
		{
		case ANIM_TYPE_ENUM::ANIM_TYPE_QEQUENCE:
		case ANIM_TYPE_ENUM::ANIM_TYPE_COMPOSITE:
		case ANIM_TYPE_ENUM::ANIM_TYPE_BLEND_SPACE:
		case ANIM_TYPE_ENUM::ANIM_TYPE_BLEND_SPACE_1D:
			GroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_BACK;
			break;
		case ANIM_TYPE_ENUM::ANIM_TYPE_OFFSET_BLEND_SAPCE:
		case ANIM_TYPE_ENUM::ANIM_TYPE_OFFSET_BLEND_SAPCE_1D:
		case ANIM_TYPE_ENUM::ANIM_TYPE_DYNAMIC_MONTAGE:
		case ANIM_TYPE_ENUM::ANIM_TYPE_MONTAGE:
			GroundType = ACTION_GROUND_TYPE_ENUM::ACTION_GROUND_TYPE_FRONT;
			break;
		default:
			break;
		}
	}
	return GroundType;
}
CONTROL_COMPILE_OPTIMIZE_END

