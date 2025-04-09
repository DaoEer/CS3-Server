// Fill out your copyright notice in the Description page of Project Settings.

#include "MapManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/EntitySpaceEventInterface.h"
#include "Actor/ServerCharacter.h"
#include "GameData/GameDeFine.h"
#include "PlaneTriggerManager.h"
#include "CustomTimerManager.h"
#include"Chuangshi.h"
#include "Manager/CfgManager.h"
#include "CS3Base/GameObject.h"

UMapManager* UMapManager::GetInstance()
{
	cs3_checkNoReentry();

	return (UMapManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MapManager")));
}

void UMapManager::LoadArea(const FName level)
{
	// 清除缓冲数据
	ClearAreaInst();

	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_AREA_DATA);
	if (ConfigTable)
	{
		TArray<FAREA_DATA*> AreaRows;
		ConfigTable->GetAllRows(AreaRows);
		for (FAREA_DATA* AreaRow : AreaRows)
		{
			//判断配置有有效性
			UClass* _AreaType = nullptr;

			if (nullptr != AreaRow)
			{
				_AreaType = AreaRow->AreaType;
			}

			if (!IsValid(_AreaType))
			{
				CS3_Warning(TEXT("UMapManager::LoadArea --- AreaType Is NULL !"));
				continue;
			}

			FString AreaType = FNAME_TO_FSTRING(_AreaType->GetFName());
			if (AreaRow->MapScriptID.Equals(FNAME_TO_FSTRING(level)))
			{
				//FString AreaType = FNAME_TO_FSTRING(_AreaType->GetFName());
				
				if (AreaType == FString(TEXT("WholeArea")) || AreaType == FString(TEXT("SpaceCopyStoryArea")) || 
					AreaType == FString(TEXT("SpaceCopyNormalArea")))
				{
					UWholeArea* Area = NewObject<UWholeArea>(this, _AreaType);
					Area->InitDatas(AreaRow);
					WholeAreas.Add(level, Area);
					Area->OnEnter(FNAME_TO_FSTRING(level));							// 进入关卡，就开始加载区域相关数据！并触发进入大地图区域
				}

				else if (AreaType == FString(TEXT("SubArea")))
				{
					USubArea* Area = NewObject<USubArea>(this, _AreaType);
					Area->InitDatas(AreaRow);
					SubAreas.Add(Area);
				}
				
				else if (AreaType == FString(TEXT("PlaneArea")))
				{
					UPlaneArea* Area = NewObject<UPlaneArea>(this, _AreaType);
					Area->InitDatas(AreaRow);
					UUECS3GameInstance::Instance->PlaneTriggerManager->InitTriggerData(AreaRow->ScriptID);
					PlaneAreas.Add(Area);
					PlaneWholeAreas.Add(FSTRING_TO_FNAME(AreaRow->ScriptID), Area);
				}
				
				else if (AreaType == FString(TEXT("ReviveArea")))
				{
					UReviveArea* Area = NewObject<UReviveArea>(this, _AreaType);
					Area->InitDatas(AreaRow);
					ReviveAreas.Add(Area);
				}

				else if (AreaType == FString(TEXT("ProtectedArea")))
				{
					UProtectedArea* Area = NewObject<UProtectedArea>(this, _AreaType);
					Area->InitDatas(AreaRow);
					ProtectedAreas.Add(Area);
				}
				
				else
				{
					CS3_Warning(TEXT("Can not Create instance Row(%s) in AreaDataTable "), *FNAME_TO_FSTRING(AreaRow->RowName));
				}

			}
			else if (AreaRow->ScriptID.Equals(FNAME_TO_FSTRING(level)))		/// 进入了位面
			{
				
				// 位面地图
				if (AreaType == FString(TEXT("PlaneArea")))
				{
					UPlaneArea* Area = NewObject<UPlaneArea>(this, _AreaType);
					Area->InitDatas(AreaRow);
					Area->OnEnter(FNAME_TO_FSTRING(level));
					PlaneWholeAreas.Add(FSTRING_TO_FNAME(AreaRow->ScriptID), Area);
				}
				else
				{
					CS3_Warning(TEXT("Can not load Area(%s), it type is %s"), *FNAME_TO_FSTRING(level), *AreaType);
				}
			}
		}
	}
}

void UMapManager::ClearAreaInst()
{
	PlaneWholeAreas.Empty();
	WholeAreas.Empty();
	PlaneAreas.Empty();
	SubAreas.Empty();
	ReviveAreas.Empty();
	ProtectedAreas.Empty();
}

void UMapManager::SendEnterSpaceMsg()
{
	//进地图提示
	FString AreaName = GetAreaName();
	if (AreaName != "")
	{
		UGolbalBPFunctionLibrary::StatusMessage(105, AreaName);     //聊天框提示
		const int32 SpaceType = FSTRING_TO_INT(UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_TYPE"))));
		if (SpaceType == int(ENUM_SPACE_TYPE::SPACE_TYPE_STORY_COPY)) //剧情副本
		{
			UGolbalBPFunctionLibrary::StatusMessage(106, AreaName);	//半身像界面提示
		}
		else //其他地图
		{
			UGolbalBPFunctionLibrary::StatusMessage(107, AreaName);	//屏幕中央提示
		}
	}
}

void UMapManager::AddAreaDetectTimer()
{
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DetectTimerHander, this, &UMapManager::DetectArea, 0.1, true);
}

void UMapManager::ClearAreaDetectTimer()
{
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DetectTimerHander);
}

void UMapManager::PauseAreaDetectTimer()
{
	if (DetectTimerHander.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->PauseTimer(DetectTimerHander);
	}
}

void UMapManager::UnPauseAreaDetectTimer()
{
	if (DetectTimerHander.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->UnPauseTimer(DetectTimerHander);
	}
}

void UMapManager::AddAreaQuest(int QuestID, int TaskID, const FString& TaskParam1, const FString& TaskParam2, const FString& TaskParam3)
{
	// 如果该level存在，需要判断是否已经加载过
	for (auto QA : QuestAreas)
	{
		if (QA->QuestID == QuestID && QA->TaskID == TaskID)return;
	}

	UBaseQuestArea* Quest = NewObject<UBaseQuestArea>();
	Quest->InitDatas(QuestID, TaskID, TaskParam1, TaskParam2, TaskParam3);
	QuestAreas.Add(Quest);

}

void UMapManager::AddSpaceEventArea(FString SpaceScriptID, INT32 EventType, INT32 EventID, INT8 ShapeType, FString Param1, FString Param2, FString Param3)
{		
		if (ShapeType == 1)	//圆形
		{
			USpaceEventBaseArea* Area = NewObject<USpaceEventCircleArea>();
			Area->InitParams(SpaceScriptID, EventType, EventID, Param1, Param2, Param3);
			Area->AreaIndex = SpaceEventAreas.Num();
			SpaceEventAreas.Add(Area);
		}
		else if(ShapeType == 2)	//多边形
		{
			USpaceEventBaseArea* Area = NewObject<USpaceEventSquareArea>();
			Area->InitParams(SpaceScriptID, EventType, EventID, Param1, Param2, Param3);
			Area->AreaIndex = SpaceEventAreas.Num();
			SpaceEventAreas.Add(Area);
		}
}

void UMapManager::ClearSpaceEventArea()
{
	SpaceEventAreas.Empty();
	LastSEAreaIndexs.Empty();
}

void UMapManager::AddSpaceStageArea(FString SpaceScriptID, INT32 StageIndex, INT32 TaskIndex, INT8 ShapeType, float CeilHeight, float FloorHeight, FString AreaParam)
{

	if (ShapeType == 1)	//圆形
	{
		USpaceStageBaseArea* Area = NewObject<USpaceStageCircleArea>();
		Area->InitParams(SpaceScriptID, StageIndex, TaskIndex, CeilHeight, FloorHeight, AreaParam);
		Area->AreaIndex = SpaceStageAreas.Num();
		SpaceStageAreas.Add(Area);
	}
	else if (ShapeType == 2)	//多边形
	{
		USpaceStageBaseArea* Area = NewObject<USpaceStagePolyArea>();
		Area->InitParams(SpaceScriptID, StageIndex, TaskIndex, CeilHeight, FloorHeight, AreaParam);
		Area->AreaIndex = SpaceStageAreas.Num();
		SpaceStageAreas.Add(Area);
	}
}

void UMapManager::ClearSpaceStageArea()
{
	SpaceStageAreas.Empty();
	LastSSAreaIndexs.Empty();
}

FString UMapManager::GetAreaName()
{
	// 先到大地图找，找不到再从位面中找
	const FString Level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (WholeAreas.Contains(FSTRING_TO_FNAME(Level)))
	{
		return WholeAreas[FSTRING_TO_FNAME(Level)]->AreaName;
	}
	if (PlaneWholeAreas.Contains(FSTRING_TO_FNAME(Level)))
	{
		return PlaneWholeAreas[FSTRING_TO_FNAME(Level)]->AreaName;
	}
	return FString(TEXT(""));
}

FString UMapManager::ChangeSpaceScriptIDToAreaName(const FString SpaceScriptID)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_AREA_DATA);
	if (ConfigTable)
	{
		TArray<FAREA_DATA*> AreaRows;
		ConfigTable->GetAllRows(AreaRows);
		for (FAREA_DATA* AreaRow : AreaRows)
		{
			if (AreaRow->ScriptID == SpaceScriptID)
			{
				return AreaRow->AreaName;
			}
		}
	}
	FString AreaName_;
	return AreaName_;
}

FAreaReviveData UMapManager::GetAreaReviveData()
{
	FAreaReviveData AreaReviveData;
	for (auto Revive : ReviveAreas)
	{
		if (Revive->IsPlayerIn())
		{
			AreaReviveData.ReviveSpace = Revive->ReviveSpace;
			AreaReviveData.RevivePosition = Revive->RevivePosition;
			AreaReviveData.ReviveDirection = Revive->ReviveDirection;
			AreaReviveData.ReviveSpaceName = Revive->AreaName;
			break;
		}
	}
	return AreaReviveData;
}

bool UMapManager::IsPlayerUnderArea()
{
	const FString level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	for (auto Revive : ReviveAreas)
	{
		if (Revive->IsPlayerUnder())
		{
			return true;
		}
	}
	//默认死亡深度
	if (WholeAreas.Contains(FSTRING_TO_FNAME(level)))
	{
		UWholeArea* CWholeArea = WholeAreas[FSTRING_TO_FNAME(level)];
		return CWholeArea->IsPlayerUnder();
	}
	else if (PlaneWholeAreas.Contains(FSTRING_TO_FNAME(level)))
	{
		UPlaneArea* CPlaneArea = PlaneWholeAreas[FSTRING_TO_FNAME(level)];
		return CPlaneArea->IsPlayerUnder();
	}
	return false;
}

bool UMapManager::IsPlayerFlyCeiling()
{
	const FString level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));

	//默认飞行深度
	if (WholeAreas.Contains(FSTRING_TO_FNAME(level)))
	{
		UWholeArea* CWholeArea = WholeAreas[FSTRING_TO_FNAME(level)];
		return CWholeArea->IsPlayerFlyCeiling();
	}
	else if (PlaneWholeAreas.Contains(FSTRING_TO_FNAME(level)))
	{
		UPlaneArea* CPlaneArea = PlaneWholeAreas[FSTRING_TO_FNAME(level)];
		return CPlaneArea->IsPlayerFlyCeiling();
	}
	return false;
}

bool UMapManager::IsPlayerInPlane()
{
	const FString Level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (PlaneWholeAreas.Contains(FSTRING_TO_FNAME(Level)))
	{
		return PlaneWholeAreas[FSTRING_TO_FNAME(Level)]->ScriptID == Level;
	}
	return false;
}

FString UMapManager::GetRelatedMapScriptID(const FString& level)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_AREA_DATA);
	if (ConfigTable)
	{
		TArray<FAREA_DATA*> AreaRows;
		ConfigTable->GetAllRows(AreaRows);
		for (FAREA_DATA* AreaRow : AreaRows)
		{
			if (AreaRow->ScriptID.Equals(level))
			{
				return AreaRow->MapScriptID;
			}
		}
	}
	return FString(TEXT(""));
}

bool UMapManager::IsPlaneSpace(const FString& Level)
{
	if (PlaneWholeAreas.Contains(FSTRING_TO_FNAME(Level)))
	{
		return true;
	}
	return false;
}


bool UMapManager::IsCopySpace(const FString& Level)
{
	FName LevelName = FSTRING_TO_FNAME(Level);
	if (WholeAreas.Contains(LevelName))
	{
		SPACE_AREA_TYPE Type = WholeAreas[LevelName]->GetType();
		if (Type == SPACE_AREA_TYPE::SPACE_AREA_TYPE_SC_NORMAL || Type == SPACE_AREA_TYPE::SPACE_AREA_TYPE_SC_STORY)
		{
			return true;
		}
	}
	return false;
}

TArray<FVector2D> UMapManager::GetPlanePolygon()
{
	const FString Level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (PlaneWholeAreas.Contains(FSTRING_TO_FNAME(Level)))
	{
		return PlaneWholeAreas[FSTRING_TO_FNAME(Level)]->GetPolygon();
	}
	return TArray<FVector2D>();
}

void UMapManager::SetPlanePolygon(const FString& spaceScriptID, const TArray<FVector>& wallPosList)
{
	if (PlaneWholeAreas.Contains(FSTRING_TO_FNAME(spaceScriptID)))
	{
		PlaneWholeAreas[FSTRING_TO_FNAME(spaceScriptID)]->SetPolygon(wallPosList);
	}
}

bool UMapManager::IsPlayerCloseToPlaneArea(float Distance)
{
	const FString Level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (PlaneWholeAreas.Contains(FSTRING_TO_FNAME(Level)))
	{
		return PlaneWholeAreas[FSTRING_TO_FNAME(Level)]->IsPlayerCloseTo(Distance);
	}
	return false;
}

void UMapManager::GetCurrentSubAreaScriptID(FString& MapScriptID,FString& SubAreaScriptID, FString& SubAreaName)
{
	const FString level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	FString subScriptID = "";
	if (IsValid(LastSubArea))
	{
		subScriptID = LastSubArea->ScriptID;
		SubAreaName = LastSubArea->AreaName;
	}
	MapScriptID = level;
	SubAreaScriptID = subScriptID;
}

bool UMapManager::IsPlayerInSubArea()
{
	if (IsValid(LastSubArea))
	{
		return true;
	}
	return false;
}

void UMapManager::BeginDestroy()
{
	Super::BeginDestroy();
}

void UMapManager::DetectArea()
{
	DetectPlaneArea();
	DetectQuestArea();
	DetectSubArea();
	DetectSpaceEventArea();
	DetectSpaceStageArea();
	DetectActivityCircleArea();
	DetectProtectedArea();
	DetectJSZZArea();
}

void UMapManager::DetectPlaneArea()
{
	if (!UUECS3GameInstance::pKBEApp || !UUECS3GameInstance::pKBEApp->pBaseApp())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMapManager::DetectPlaneArea : app|| app->pBaseApp()!"));
		return;
	}
	for (auto Plane:PlaneAreas)
	{		
		if (Plane->IsPlayerIn())
		{
			UPlaneTriggerManager* PTMgr = UUECS3GameInstance::Instance->PlaneTriggerManager;
			if (PTMgr->CanEnterPlane(Plane->ScriptID))
			{
				Plane->trriger(Plane->ScriptID);
			}			
		}
	}

}

void UMapManager::DetectQuestArea()
{
	if (!UUECS3GameInstance::pKBEApp || !UUECS3GameInstance::pKBEApp->pBaseApp())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMapManager::DetectQuestArea : app|| app->pBaseApp()!"));
		return;
	}
	//获取当前Level
	const FString level = UUECS3GameInstance::pKBEApp->pBaseApp()->GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	TArray<UBaseQuestArea*> RemoveQuests;
	for (auto Quest : QuestAreas)
	{
		if (Quest->IsPlayerIn())
		{
			if (Quest->CheckCondition())
			{
				Quest->OnEnter(level);
				RemoveQuests.Add(Quest);
			}
		}
	}
	for (auto RemoveQuest:RemoveQuests)
	{
		QuestAreas.Remove(RemoveQuest);
	}

}

void UMapManager::DetectSpaceEventArea()
{
	if (!UUECS3GameInstance::pKBEApp || !UUECS3GameInstance::pKBEApp->pBaseApp())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMapManager::DetectSpaceEventArea : app|| app->pBaseApp()!"));
		return;
	}
	//获取当前Level
	const FString level = UUECS3GameInstance::pKBEApp->pBaseApp()->GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	
	for (auto Area : SpaceEventAreas)
	{
		if (Area->IsPlayerIn()) 
		{
			if (LastSEAreaIndexs.Find(Area->AreaIndex) < 0)
			{
				LastSEAreaIndexs.Add(Area->AreaIndex);
				Area->OnEnter(level);
			}
		}
		else 
		{
			if (LastSEAreaIndexs.Find(Area->AreaIndex)>= 0)
			{
				LastSEAreaIndexs.Remove(Area->AreaIndex);
				Area->OnLeave(level);
			}
		}
	}
}

void UMapManager::DetectSubArea()
{
	if (!UUECS3GameInstance::pKBEApp || !UUECS3GameInstance::pKBEApp->pBaseApp())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMapManager::DetectSubArea : app|| app->pBaseApp()!"));
		return;
	}
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!PlayerActor)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMapManager::DetectSubArea : PlayerActor!"));
		return;
	}
	UEntitySpaceEventInterface* Interface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.EntitySpaceEventInterface : nullptr;
	
	//获取当前Level
	const FString level = UUECS3GameInstance::pKBEApp->pBaseApp()->GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));

	USubArea *CurrentSubArea = nullptr;
	for (auto Area : SubAreas) 
	{
		if (Area->IsPlayerIn())
		{
			CurrentSubArea = Area;
			break;
		}
	}

	if (!IsValid(LastSubArea) && IsValid(CurrentSubArea))	///进区域
	{
		CurrentSubArea->OnEnter(level);
		if (IsValid(Interface))
		{
			Interface->onRoleChangeWorldArea(CurrentSubArea->ScriptID, "");
		}
		LastSubArea = CurrentSubArea;
		BP_UpdateSubArea(CurrentSubArea->ScriptID, "");
		return;
	}
	else if (IsValid(LastSubArea) && !IsValid(CurrentSubArea))	///出区域
	{
		LastSubArea->OnLeave(level);
		if (IsValid(Interface))
		{
			Interface->onRoleChangeWorldArea("", LastSubArea->ScriptID);
		}
		FString LastSubAreaScriptID = LastSubArea->ScriptID;
		LastSubArea = CurrentSubArea;		
		BP_UpdateSubArea("", LastSubAreaScriptID);
		return;
	}
	else if (IsValid(LastSubArea) && IsValid(CurrentSubArea))
	{
		if (CurrentSubArea->ScriptID != LastSubArea->ScriptID) 	///改变区域
		{
			LastSubArea->OnLeave(level);
			CurrentSubArea->OnEnter(level);
			if (IsValid(Interface))
			{
				Interface->onRoleChangeWorldArea(CurrentSubArea->ScriptID, LastSubArea->ScriptID);
			}
			LastSubArea = CurrentSubArea;
			BP_UpdateSubArea(CurrentSubArea->ScriptID, LastSubArea->ScriptID);
			return;
		}
	}

	LastSubArea = CurrentSubArea;
}

void UMapManager::DetectSpaceStageArea()
{
	if (!UUECS3GameInstance::pKBEApp || !UUECS3GameInstance::pKBEApp->pBaseApp())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMapManager::DetectSpaceStageArea : app|| app->pBaseApp()!"));
		return;
	}
	//获取当前Level
	const FString level = UUECS3GameInstance::pKBEApp->pBaseApp()->GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));

	for (auto Area : SpaceStageAreas)
	{
		if (Area->IsPlayerIn())
		{
			if (LastSSAreaIndexs.Find(Area->AreaIndex) < 0)
			{
				LastSSAreaIndexs.Add(Area->AreaIndex);
				Area->OnEnter(level);
			}
		}
		else
		{
			if (LastSSAreaIndexs.Find(Area->AreaIndex) >= 0)
			{
				LastSSAreaIndexs.Remove(Area->AreaIndex);
			}
		}
	}
}
void UMapManager::DetectActivityCircleArea()
{
	if (!UUECS3GameInstance::pKBEApp || !UUECS3GameInstance::pKBEApp->pBaseApp())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMapManager::DetectActivityCircleArea : app|| app->pBaseApp()!"));
		return;
	}
	//获取当前Level
	const FString SpaceScriptID = UUECS3GameInstance::pKBEApp->pBaseApp()->GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));

	for (auto Area : ActivityCircleAreas)
	{
		if (Area->IsPlayerIn())
		{
			if (LastACAreaIndexs.Find(Area->AreaIndex) < 0)
			{
				LastACAreaIndexs.Add(Area->AreaIndex);
				Area->OnEnter(SpaceScriptID);
			}
		}
		else
		{
			if (LastACAreaIndexs.Find(Area->AreaIndex) >= 0)
			{
				LastACAreaIndexs.Remove(Area->AreaIndex);
				Area->OnLeave(SpaceScriptID);
			}
		}
	}
}

void UMapManager::DetectProtectedArea()
{
	if (!UUECS3GameInstance::pKBEApp || !UUECS3GameInstance::pKBEApp->pBaseApp())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMapManager::DetectSpaceEventArea : app|| app->pBaseApp()!"));
		return;
	}
	for (auto Area : ProtectedAreas)
	{
		if (Area->IsPlayerUnder())
		{
			Area->Triger();
			return;
		}
	}
}

void UMapManager::AddActivityCircleArea(FString SpaceScriptID, FVector position, float Range, int32 Index)
{
	UActivityCircleArea* Area = NewObject<UActivityCircleArea>();
	Area->InitParams(SpaceScriptID, position, Range, Index);
	ActivityCircleAreas.Add(Area);
}

void UMapManager::ClearActivityCircleArea()
{
	ActivityCircleAreas.Empty();
	LastACAreaIndexs.Empty();
}

void UMapManager::AddJSZZCircleArea(FString SpaceScriptID, FVector position, float Range)
{
	JSZZCircleArea = NewObject<UJSZZCircleArea>();
	JSZZCircleArea->InitParams(SpaceScriptID, position, Range);
}
void UMapManager::ClearJSZZCircleArea()
{
	JSZZCircleArea = nullptr;
}
void UMapManager::DetectJSZZArea()
{
	if (IsValid(JSZZCircleArea))
	{
		//获取当前Level
		const FString SpaceScriptID = UUECS3GameInstance::pKBEApp->pBaseApp()->GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
		if (JSZZCircleArea->IsPlayerIn())
		{
			if (!isAreaInJSZZArea) 
			{
				isAreaInJSZZArea = true;
				JSZZCircleArea->OnEnter(SpaceScriptID);
			}
		}
		else
		{
			if (isAreaInJSZZArea)
			{
				isAreaInJSZZArea = false;
				JSZZCircleArea->OnLeave(SpaceScriptID);
			}
		}
	}
}