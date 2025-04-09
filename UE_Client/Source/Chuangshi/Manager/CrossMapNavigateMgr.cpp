
#include "CrossMapNavigateMgr.h"
#include "Actor/Player/PlayerCharacter.h"
#include "GameData/TeleportPointData.h"
#include "GameData/NPCPointDatas.h"
#include "GameData/CrossMapConfigData.h"
#include "GameDevelop/CS3GameInstance.h"
#include"Chuangshi.h"
#include "GameData/Area.h"
#include "Manager/CfgManager.h"

CONTROL_COMPILE_OPTIMIZE_START

SpacePathVertex::SpacePathVertex(const FString& SpaceName) :
	SpaceName_(SpaceName),
	//Next_(nullptr),
	Prev_(nullptr)
{
	Cost_ = MAX_flt;
	TeleportType_ = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportDefault;
}


SpacePathVertex::~SpacePathVertex()
{
	Neighbours_.Empty();
}

int32 SpacePathVertex::NeighboursCount() const
{
	return Neighbours_.Num();
}

void SpacePathVertex::insertNeighbour(SpacePathVertex* Vertex)
{
	int32 Index;
	bool Result = Neighbours_.Find(Vertex, Index);
	if (!Result)
	{
		Neighbours_.Add(Vertex);
	}
}

void SpacePathVertex::removeNeighbour(SpacePathVertex* Vertex)
{
	int32 Index;
	bool Result = Neighbours_.Find(Vertex, Index);
	if (Result)
	{
		Neighbours_.Remove(Vertex);
	}
}



const FString& SpacePathVertex::GetSpaceName() const
{
	return SpaceName_;
}

//float SpacePathVertex::VerticesCost(const SpacePathVertex* Vertex) const
//{
//	return FVector::Dist(Position_, Vertex->Position());
//}

void SpacePathVertex::ShortestPathInit()
{
	//Next_ = nullptr;
	Prev_ = nullptr;
	Cost_ = MAX_flt;
	TeleportType_ = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportDefault;
}

float SpacePathVertex::GetCost() const
{
	return Cost_;
}

void SpacePathVertex::SetCost(float Cost)
{
	Cost_ = Cost;
}

ENUM_CROSS_MAP_TELEPORT_TYPE SpacePathVertex::GetTeleportType() const
{
	return TeleportType_;
}

void SpacePathVertex::SetTeleportType(ENUM_CROSS_MAP_TELEPORT_TYPE TeleportType)
{
	TeleportType_ = TeleportType;
}

//SpacePathVertex* SpacePathVertex::GetNext()
//{
//	return Next_;
//}
//
//void SpacePathVertex::SetNext(SpacePathVertex* Vertex)
//{
//	Next_ = Vertex;
//}

SpacePathVertex* SpacePathVertex::GetPrev()
{
	return Prev_;
}

void SpacePathVertex::SetPrev(SpacePathVertex* Vertex)
{
	Prev_ = Vertex;
}

SpacePathVertex* SpacePathVertex::GetNeighbourByIndex(int32 Index)
{
	if (Index >= 0 && Index < Neighbours_.Num())
	{
		return Neighbours_[Index];
	}
	else
	{
		return nullptr;
	}
}

UCrossMapNavigateMgr::UCrossMapNavigateMgr()
{

}

UCrossMapNavigateMgr::~UCrossMapNavigateMgr()
{
	Clear();
}

UCrossMapNavigateMgr* UCrossMapNavigateMgr::GetInstance()
{
	cs3_checkNoReentry();
	UCrossMapNavigateMgr* CrossMapNavigateMgr = NewObject<UCrossMapNavigateMgr>();
	CrossMapNavigateMgr->LoadConfig();
	return CrossMapNavigateMgr;
}

int32 UCrossMapNavigateMgr::VerticesCount() const
{
	return Vertices_.Num();
}

void UCrossMapNavigateMgr::LoadConfig()
{
	Clear();
	LoadMapConfig();
	const UConfigTable* CrossMapNavigatgeTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CROSS_MAP_NAVIGATE_DATA);
	TArray<FCROSS_MAP_CONFIG_DATA*> CrossMapConfigDatas;
	CrossMapNavigatgeTable->GetAllRows(CrossMapConfigDatas);
	for (auto CrossMapData:CrossMapConfigDatas)
	{
		FCROSS_MAP_START_TO_END_INFO StartToEndInfo;
		StartToEndInfo.StartSpace = CrossMapData->CurrentSpace;
		StartToEndInfo.EndSpace = CrossMapData->DstSpace;
		FCROSS_MAP_TELEPORT_INFO TeleportInfo;
		if (CrossMapConnectInfos.Contains(StartToEndInfo))
		{
			TeleportInfo = CrossMapConnectInfos[StartToEndInfo];
		}
		FVector NPCPosition;
		UGolbalBPFunctionLibrary::GetNPCPositionFromTable(CrossMapData->CurrentSpace, CrossMapData->ScriptID, NPCPosition);
		FVector TeleportPos = UGolbalBPFunctionLibrary::FStringToFVector(CrossMapData->Param1);
		if ((CrossMapData->TeleportType).Equals("SpaceDoor"))
		{
			if (!TeleportPos.IsZero())
			{
				TeleportInfo.SpaceDoorInfo.ScriptID = CrossMapData->ScriptID;
				TeleportInfo.SpaceDoorInfo.Position = NPCPosition;
				TeleportInfo.SpaceDoorInfo.TeleportPos = TeleportPos;
			}
		}
		else if ((CrossMapData->TeleportType).Equals("NPC"))
		{
			if (!TeleportPos.IsZero())
			{
				FCROSSMAP_NPC_PARAM NPCParam;
				NPCParam.ScriptID = CrossMapData->ScriptID;
				NPCParam.TalkKey = CrossMapData->Param2;
				if (CrossMapData->Param3.IsEmpty())
				{
					NPCParam.Camp = 0;
				}
				else
				{
					NPCParam.Camp = FSTRING_TO_INT(CrossMapData->Param3);
				}
				NPCParam.Position = NPCPosition;
				NPCParam.TeleportPos = TeleportPos;
				TeleportInfo.NPCInfos.AddUnique(NPCParam);
			}
		}
		else if ((CrossMapData->TeleportType).Equals("Trap"))
		{
			TeleportInfo.TrapInfo.ScriptID = CrossMapData->ScriptID;
			TeleportInfo.TrapInfo.Position = NPCPosition;
		}
		else if ((CrossMapData->TeleportType).Equals("Carter"))
		{
			if (!TeleportPos.IsZero())
			{
				FCROSSMAP_NPC_PARAM NPCParam;
				NPCParam.ScriptID = CrossMapData->ScriptID;
				NPCParam.TalkKey = CrossMapData->Param2;
				if (CrossMapData->Param3.IsEmpty())
				{
					NPCParam.Camp = 0;
				}
				else
				{
					NPCParam.Camp = FSTRING_TO_INT(CrossMapData->Param3);
				}
				NPCParam.Position = NPCPosition;
				NPCParam.TeleportPos = TeleportPos;
				TeleportInfo.CarterInfos.AddUnique(NPCParam);
			}
		}
		CrossMapConnectInfos.Add(StartToEndInfo, TeleportInfo);
	}
	const UConfigTable* TeleportPointTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TELEPORT_POINT_DATA);
	TArray<FName> TeleportPointIndexs = TeleportPointTable->GetRowNames();
	for (auto It = MapRelatedInfos.CreateConstIterator(); It; ++It)
	{

		FString StartSpace = It->Key;
		FMAP_RELATED_INFO AreaData = It->Value;
		if (AreaData.AreaType == FString(TEXT("SpaceCopyStoryArea")) || AreaData.AreaType == FString(TEXT("SpaceCopyNormalArea")) || AreaData.AreaType == FString(TEXT("PlaneArea")))
		{
			continue;
		}
		ForbidUseTeleportInfos.Add(StartSpace, AreaData.ForbidUseTeleportPoint);
		if (AreaData.ForbidUseTeleportPoint == true)
		{
			continue;
		}
		for (auto TeleportPointIndex : TeleportPointIndexs)
		{
			const FTELEPORT_POINT_DATA* TeleportPoint = TeleportPointTable->GetRow<FTELEPORT_POINT_DATA>(TeleportPointIndex);
			if (StartSpace.Equals(TeleportPoint->ScriptID))
			{
				continue;
			}
			FCROSS_MAP_TELEPORT_INFO TeleportInfo;
			FCROSS_MAP_START_TO_END_INFO StartToEndInfo;
			StartToEndInfo.StartSpace = StartSpace;
			StartToEndInfo.EndSpace = TeleportPoint->ScriptID;
			if (CrossMapConnectInfos.Contains(StartToEndInfo))
			{
				TeleportInfo = CrossMapConnectInfos[StartToEndInfo];
			}

			TeleportPointToCamp.Add(TeleportPointIndex.ToString(), TeleportPoint->LimitCamp);
			TeleportPointToLevel.Add(TeleportPointIndex.ToString(), TeleportPoint->LimitLevel);

			FCROSSMAP_TELEPORT_POINT_PARAM TeleportStoneParam;
			TeleportStoneParam.TeleportIndex = TeleportPointIndex.ToString();
			TeleportStoneParam.TeleportPos = TeleportPoint->Position;
			TeleportStoneParam.LimitCamp = TeleportPoint->LimitCamp;
			TeleportStoneParam.LimitLevel = TeleportPoint->LimitLevel;
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::LoadConfig: StartSpace:%s,EndSpace:%s,teleportIndex:%s"), *StartSpace, *(TeleportPoint->ScriptID), *(TeleportStoneParam.TeleportIndex));
			TeleportInfo.TeleportPointInfos.AddUnique(TeleportStoneParam);
			CrossMapConnectInfos.Add(StartToEndInfo, TeleportInfo);
		}
	}
}

void UCrossMapNavigateMgr::LoadMapConfig()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_AREA_DATA);
	if (ConfigTable)
	{
		TArray<FAREA_DATA*> AreaRows;
		ConfigTable->GetAllRows(AreaRows);
		for (FAREA_DATA* AreaRow : AreaRows)
		{
			if (AreaRow == nullptr)
			{
				CS3_Warning(TEXT("-->Null Pointer error:UCrossMapNavigateMgr::LoadMapConfig : AreaRow!"));
				continue;
			}
			//判断配置有有效性
			UClass* _AreaType = nullptr;
			
			_AreaType = AreaRow->AreaType;

			if (!IsValid(_AreaType))
			{
				CS3_Warning(TEXT("UMapManager::LoadArea --- AreaType Is NULL !"));
				continue;
			}

			FString AreaType = FNAME_TO_FSTRING(_AreaType->GetFName());
			FMAP_RELATED_INFO MapRelatedInfo;
			MapRelatedInfo.AreaType = AreaType;
			MapRelatedInfo.MapScriptID = AreaRow->MapScriptID;
			MapRelatedInfo.ForbidUseTeleportPoint = AreaRow->ForbidUseTeleportPoint;
			MapRelatedInfos.Add(AreaRow->ScriptID, MapRelatedInfo);
		}
	}
}

ENUM_CROSS_MAP_TELEPORT_TYPE UCrossMapNavigateMgr::GetTeleportTypeForPriority(SpacePathVertex* SrcVertex, SpacePathVertex * DstVertex)
{
	FCROSS_MAP_START_TO_END_INFO StartToEndInfo;
	StartToEndInfo.StartSpace = SrcVertex->GetSpaceName();
	StartToEndInfo.EndSpace = DstVertex->GetSpaceName();
	if (PlayerCrossMapConnectInfos.Contains(StartToEndInfo))
	{
		FCROSS_MAP_TELEPORT_INFO TeleportInfo = PlayerCrossMapConnectInfos[StartToEndInfo];
		if (TeleportInfo.TeleportPointInfos.Num() > 0)
		{
			return ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportPoint;
		}
		else if (TeleportInfo.CarterInfos.Num() > 0)
		{
			return ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportCarter;
		}
		else if (TeleportInfo.NPCInfos.Num() > 0 )
		{
			return ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportNPC;
		}
		else if (!(TeleportInfo.TrapInfo.ScriptID.IsEmpty()))
		{
			return ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportTrap;
		}
		else if (!(TeleportInfo.SpaceDoorInfo.ScriptID.IsEmpty()))
		{
			return ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportSpaceDoor;
		}
	}
	return ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportDefault;

}

void UCrossMapNavigateMgr::Dijkstra(SpacePathVertex* StartVertex, SpacePathVertex* EndVertex)
{
	ShortestPathInit();
	if (EndVertex->NeighboursCount() <= 0) //没有顶点（地图）和目标点相邻，表示没有路
	{
		return;
	}
	EndVertex->SetCost(0.0f);
	TArray<SpacePathVertex*> TempVertices(Vertices_);
	while (TempVertices.Num() > 0)
	{
		float Cost = TempVertices[0]->GetCost();
		SpacePathVertex* MinVertex = TempVertices[0];
		for (auto It = TempVertices.CreateConstIterator(); It; ++It)
		{
			SpacePathVertex* Vertex = *It;
			if (Vertex->GetCost() < Cost)
			{
				Cost = Vertex->GetCost();
				MinVertex = *It;
			}
		}
		if (FMath::IsNearlyEqual(MinVertex->GetCost(), MAX_flt) || (CROSS_MAP_SPACE_NUM != -1 && MinVertex->GetCost() >= CROSS_MAP_SPACE_NUM - 1)) //①最小消耗为MAX_flt，说明不能到达目标点；②策划规定传送的中间地图最多只有n个
		{
			break;
		}
		if (MinVertex != nullptr && MinVertex->GetSpaceName() == StartVertex->GetSpaceName())
		{
			break;
		}
		TempVertices.Remove(MinVertex);
		for (int32 RelaxIndex = 0; RelaxIndex < MinVertex->NeighboursCount(); ++RelaxIndex)
		{
			if (MinVertex != nullptr && MinVertex->GetNeighbourByIndex(RelaxIndex))
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::Dijkstra MinVertex:%s RelaxVertex:%s"), *(MinVertex->GetSpaceName()), *(MinVertex->GetNeighbourByIndex(RelaxIndex)->GetSpaceName()));
				AdjustVertexPrev(MinVertex, MinVertex->GetNeighbourByIndex(RelaxIndex));
			}
		}
	}
}

TArray<FCROSS_MAP_TARGET_INFO> UCrossMapNavigateMgr::FindCrossMapPath(const FString& StartSpaceName, const FString& EndSpaceName, const FVector& StartPosition, const FVector& EndPosition /* = FVector::ZeroVector */, const FString& ScriptID /* = "" */, const int& QuestID /* = 0 */)
{
	FString FinalSpaceName = EndSpaceName;
	FVector FinalPosition = EndPosition;
	if (MapRelatedInfos.Contains(EndSpaceName) && MapRelatedInfos[EndSpaceName].AreaType == FString(TEXT("PlaneArea")))
	{
		if (!GetSpacePosInConfig(FinalSpaceName).IsZero())
		{
			FinalPosition = GetSpacePosInConfig(FinalSpaceName);
		}
		FinalSpaceName = MapRelatedInfos[EndSpaceName].MapScriptID;
	}
	else if (MapRelatedInfos.Contains(EndSpaceName) && ( MapRelatedInfos[EndSpaceName].AreaType == FString(TEXT("SpaceCopyStoryArea")) || MapRelatedInfos[EndSpaceName].AreaType == FString(TEXT("SpaceCopyNormalArea"))))
	{
		if (!GetSpacePosInConfig(FinalSpaceName).IsZero())
		{
			FinalPosition = GetSpacePosInConfig(FinalSpaceName);
		}
	}
	if (FinalPosition.IsZero())
	{
		bool IsFind = UGolbalBPFunctionLibrary::GetNPCPositionFromTable(EndSpaceName, ScriptID, FinalPosition);
		if (!IsFind)
		{
			UGolbalBPFunctionLibrary::GetNPCPositionFromTable(FinalSpaceName, ScriptID, FinalPosition);
		}
	}
	TArray<FCROSS_MAP_TARGET_INFO> CrossMapTargetInfos;

	if (StartSpaceName.Equals(FinalSpaceName))
	{
		FCROSS_MAP_TARGET_INFO CrossMapInfo;
		CrossMapInfo.SpaceName = EndSpaceName;
		CrossMapInfo.TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportDefault;
		CrossMapInfo.Position = FinalPosition;
		CrossMapInfo.ScriptID = ScriptID;
		CrossMapTargetInfos.Add(CrossMapInfo);
		return CrossMapTargetInfos;
	}
	this->AutoQuestID = QuestID;
	InitVertexAndEdge();

	SpacePathVertex* StartVertex = GetVertex(StartSpaceName);	
	SpacePathVertex* EndVertex = GetVertex(FinalSpaceName);
	if (StartVertex == nullptr || EndVertex == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCrossMapNavigateMgr::FindCrossMapPath : StartVertex!"));
		return CrossMapTargetInfos;
	}
	SpacePathVertex* FirstVertex = StartVertex;
	Dijkstra(StartVertex, EndVertex);
	FCROSS_MAP_SPACE_TARGET_INFO CurrentSpaceTargetPos,LastSpaceTargetPos;
	FCROSS_MAP_START_TO_END_INFO StartToEndInfo;
	while (StartVertex != EndVertex)
	{
		SpacePathVertex* PrevVertex = StartVertex->GetPrev();
		if (PrevVertex == nullptr)
		{
			CrossMapTargetInfos.Empty();
			return CrossMapTargetInfos;
		}
		if (FirstVertex->GetSpaceName() == StartVertex->GetSpaceName())
		{
			StartToEndInfo.StartSpace = StartVertex->GetSpaceName();
			StartToEndInfo.EndSpace = PrevVertex->GetSpaceName();
			DataTransfer(StartToEndInfo, CurrentSpaceTargetPos);
			if (CurrentSpaceTargetPos.TeleportTypeToTargetInfo.Num() == 0)
			{
				CrossMapTargetInfos.Empty();
				return CrossMapTargetInfos;
			}
			CalculateShortestMultiPosToPos(StartSpaceName, "", StartPosition, CurrentSpaceTargetPos, CrossMapTargetInfos, true);
		}
		else
		{
			StartToEndInfo.StartSpace = StartVertex->GetSpaceName();
			StartToEndInfo.EndSpace = PrevVertex->GetSpaceName();
			DataTransfer(StartToEndInfo, CurrentSpaceTargetPos);
			if (CurrentSpaceTargetPos.TeleportTypeToTargetInfo.Num() == 0 || LastSpaceTargetPos.TeleportTypeToTargetInfo.Num() == 0)
			{
				CrossMapTargetInfos.Empty();
				return CrossMapTargetInfos;
			}
			CalculateShortestMultiPosToMultiPos(LastSpaceTargetPos, CurrentSpaceTargetPos, CrossMapTargetInfos);
		}
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::FindCrossMapPath StartSpace:%s EndSpace:%s"), *(StartToEndInfo.StartSpace), *(StartToEndInfo.EndSpace));
		StartVertex = PrevVertex;
		LastSpaceTargetPos = CurrentSpaceTargetPos;
		ClearCrossMapSpaceTarget(CurrentSpaceTargetPos);
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::FindCrossMapPath FinalSpaceName:%s"), *(FinalSpaceName));
	if (LastSpaceTargetPos.TeleportTypeToTargetInfo.Num() == 0)
	{
		CrossMapTargetInfos.Empty();
		return CrossMapTargetInfos;
	}
	CalculateShortestMultiPosToPos(EndSpaceName, ScriptID, FinalPosition, LastSpaceTargetPos, CrossMapTargetInfos, false);
	if (CrossMapTargetInfos.Num() > 0) //车夫传送只需要走到车夫那里打开对话窗口，传送到另一个地图后不再需要自动寻路
	{
		FCROSS_MAP_TARGET_INFO TempMapTargetInfo = CrossMapTargetInfos[0];
		if (TempMapTargetInfo.TeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportCarter)
		{
			CrossMapTargetInfos.Empty();
			CrossMapTargetInfos.Add(TempMapTargetInfo);
		}
	}
	return CrossMapTargetInfos;
}

void UCrossMapNavigateMgr::Clear()
{
	ClearVertex();
	CrossMapConnectInfos.Empty();
	PlayerCrossMapConnectInfos.Empty();
}

void UCrossMapNavigateMgr::ClearVertex()
{
	for (auto It = Vertices_.CreateConstIterator(); It; ++It)
	{
		SpacePathVertex* Vertex = *It;
		C_SAFE_DELETE(Vertex);
	}
	Vertices_.Empty();
	VerticesMap_.Empty();
}

void UCrossMapNavigateMgr::AddVertex(const FString& SpaceName)
{
	if (VerticesMap_.Contains(SpaceName))
	{
		return;
	}
	SpacePathVertex* Vertex = new SpacePathVertex(SpaceName);//在UCrossMapNavigateMgr::ClearVertex()释放
	Vertices_.Add(Vertex);
	VerticesMap_.Add(SpaceName, Vertex);
}

SpacePathVertex* UCrossMapNavigateMgr::GetVertex(const FString& SpaceName)
{
	SpacePathVertex* Vertex = nullptr;
	if (VerticesMap_.Contains(SpaceName))
	{
		Vertex = VerticesMap_[SpaceName];
	}
	return Vertex;
}

void UCrossMapNavigateMgr::AddEdge(const FString& Start, const FString& End)
{
	check(VerticesMap_[Start]);
	check(VerticesMap_[End]);
	SpacePathVertex* StartVertex = VerticesMap_[Start];
	SpacePathVertex* EndVertex = VerticesMap_[End];
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::AddEdge: Start:%s End:%s"), *Start, *End)
	//StartVertex->insertNeighbour(EndVertex);
	EndVertex->insertNeighbour(StartVertex);
}

void UCrossMapNavigateMgr::ShortestPathInit()
{
	for (auto It = Vertices_.CreateConstIterator(); It; ++It)
	{
		SpacePathVertex* Vertex = *It;
		Vertex->ShortestPathInit();
	}
}

void UCrossMapNavigateMgr::AdjustVertexPrev(SpacePathVertex* Source, SpacePathVertex* Target)
{
	float Cost = Source->GetCost() + 1;
	if (Target->GetCost() > Cost)
	{
		Target->SetCost(Cost);
		//Source->SetNext(Target);
		Target->SetPrev(Source);
		Target->SetTeleportType(GetTeleportTypeForPriority(Target, Source));
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::AdjustVertexPrev: SourceName:%s TargetName:%s"), *(Source->GetSpaceName()), *(Target->GetSpaceName()));
	}
	else if (FMath::IsNearlyEqual(Target->GetCost(), Cost))
	{
		ENUM_CROSS_MAP_TELEPORT_TYPE CurTeleportType = Target->GetTeleportType();
		ENUM_CROSS_MAP_TELEPORT_TYPE TempTeleportType = GetTeleportTypeForPriority(Target, Source);
		//陷阱传送和NPC传送优先级相等
		if ((CurTeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportNPC && TempTeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportTrap) \
			|| (CurTeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportTrap && TempTeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportNPC))
		{
			return;
		}
		else if(TempTeleportType > CurTeleportType)
		{
			Target->SetPrev(Source);
			Target->SetTeleportType(TempTeleportType); 
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::AdjustVertexPrev: SourceName:%s TargetName:%s"), *(Source->GetSpaceName()), *(Target->GetSpaceName()));
		}
	}
}

void UCrossMapNavigateMgr::InitVertexAndEdge()
{
	ClearVertex();
	PlayerCrossMapConnectInfos.Empty();
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(Player))
	{
		KBEngine::Entity* PlayerEntity = Player->GetSelfEntity();
		if (PlayerEntity != nullptr)
		{
			FString TeleportPointNPCs = PlayerEntity->GetDefinedProperty(TEXT("teleportPointNPCs"));
			int32 Camp = PlayerEntity->GetDefinedProperty(TEXT("camp")).GetValue<int32>();
			int32 Level = PlayerEntity->GetDefinedProperty(TEXT("level")).GetValue<int16>();
			TArray<FString> TeleportPointLists = UGolbalBPFunctionLibrary::SplitString(TeleportPointNPCs, true, TEXT("|"));
			for (auto It = CrossMapConnectInfos.CreateConstIterator(); It; ++It)
			{
				FCROSS_MAP_START_TO_END_INFO StartToEndInfo = It->Key;
				FCROSS_MAP_TELEPORT_INFO CrossMapTeleportInfo = It->Value;
				FCROSS_MAP_TELEPORT_INFO TeleportInfo;
				if (PlayerCrossMapConnectInfos.Contains(StartToEndInfo))
				{
					TeleportInfo = PlayerCrossMapConnectInfos[StartToEndInfo];
				}
				AddVertex(StartToEndInfo.StartSpace);
				AddVertex(StartToEndInfo.EndSpace);
				bool HasEdge = false;
				if (CrossMapTeleportInfo.TeleportPointInfos.Num() > 0 && IsCanUseTeleportPoint(StartToEndInfo.StartSpace, AutoQuestID))
				{
					for (auto TeleportPointInfo: CrossMapTeleportInfo.TeleportPointInfos)
					{
						CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::InitVertexAndEdge: TeleportPointNPCs:%s,TeleportIndex:%s,StartSpace:%s,EndSpace:%s"), *TeleportPointNPCs, *(TeleportPointInfo.TeleportIndex), *(StartToEndInfo.StartSpace), *(StartToEndInfo.EndSpace));
						if (TeleportPointLists.Contains(TeleportPointInfo.TeleportIndex))
						{
							if (TeleportPointToCamp.Contains(TeleportPointInfo.TeleportIndex))
							{
								if ((TeleportPointToCamp[TeleportPointInfo.TeleportIndex] != 0 && TeleportPointToCamp[TeleportPointInfo.TeleportIndex] != Camp))
								{
									continue;
								}
							}
							if (TeleportPointToLevel.Contains(TeleportPointInfo.TeleportIndex))
							{
								if (Level < TeleportPointToLevel[TeleportPointInfo.TeleportIndex])
								{
									continue;
								}
							}
							TeleportInfo.TeleportPointInfos.Add(TeleportPointInfo);
							HasEdge = true;
						}
					}
				}
				if (!(CrossMapTeleportInfo.SpaceDoorInfo.ScriptID.IsEmpty()))
				{
					HasEdge = true;
					TeleportInfo.SpaceDoorInfo = CrossMapTeleportInfo.SpaceDoorInfo;
				}
				if(CrossMapTeleportInfo.NPCInfos.Num() > 0)
				{
					for (auto NpcInfo: CrossMapTeleportInfo.NPCInfos)
					{
						if (NpcInfo.Camp == 0 || NpcInfo.Camp == Camp)
						{
							HasEdge = true;
							TeleportInfo.NPCInfos.Add(NpcInfo);
						}
					}
				}
				if (CrossMapTeleportInfo.CarterInfos.Num() > 0)
				{
					for (auto CarterInfo: CrossMapTeleportInfo.CarterInfos)
					{
						if (CarterInfo.Camp == 0 || CarterInfo.Camp == Camp)
						{
							HasEdge = true;
							TeleportInfo.CarterInfos.Add(CarterInfo);
						}
					}
				}
				if (!(CrossMapTeleportInfo.TrapInfo.ScriptID.IsEmpty()))
				{
					HasEdge = true;
					TeleportInfo.TrapInfo = CrossMapTeleportInfo.TrapInfo;
				}
				if (HasEdge)
				{
					AddEdge(StartToEndInfo.StartSpace, StartToEndInfo.EndSpace);
					PlayerCrossMapConnectInfos.Add(StartToEndInfo, TeleportInfo);
				}	
			}
		}
	}
}

void UCrossMapNavigateMgr::CalculateShortestMultiPosToMultiPos(FCROSS_MAP_SPACE_TARGET_INFO& LastSpaceTargetPos, FCROSS_MAP_SPACE_TARGET_INFO& CurrentSpaceTargetPos, TArray<FCROSS_MAP_TARGET_INFO>& MapPathInfo)
{
	float MinDistance = MAX_flt;
	FCROSS_MAP_TARGET_INFO MapTargetInfo;
	FCROSS_MAP_SPACE_TARGET_INFO MinLastSpaceTargetPos,MinCurrentSpaceTargetPos;
	for (auto LastTeleportTypeToTarget:LastSpaceTargetPos.TeleportTypeToTargetInfo)
	{
		if (LastTeleportTypeToTarget.TeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportTrap)
		{
			continue;
		}
		for (auto LastScriptIDToTarget:LastTeleportTypeToTarget.ScriptIDToTargetInfo)
		{
			for (auto LastTargetInfo : LastScriptIDToTarget.TargetParam)
			{
				for (auto CurrentTeleportTypeToTarget : CurrentSpaceTargetPos.TeleportTypeToTargetInfo)
				{
					for (auto CurrentScriptIDToTarget : CurrentTeleportTypeToTarget.ScriptIDToTargetInfo)
					{
						float Distance = FVector::Dist(LastTargetInfo.TargetPosition, CurrentScriptIDToTarget.Position);
						if (Distance < MinDistance)
						{
							MinDistance = Distance;

							ClearCrossMapSpaceTarget(MinLastSpaceTargetPos);
							ClearCrossMapSpaceTarget(MinCurrentSpaceTargetPos);

							MinLastSpaceTargetPos.SpaceName = LastSpaceTargetPos.SpaceName;
							FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO MinLastTeleportTypeToTarget;
							MinLastTeleportTypeToTarget.TeleportType = LastTeleportTypeToTarget.TeleportType;
							FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO MinLastScriptIDToTarget;
							MinLastScriptIDToTarget.ScriptID = LastScriptIDToTarget.ScriptID;
							MinLastScriptIDToTarget.Position = LastScriptIDToTarget.Position;
							MinLastScriptIDToTarget.TargetParam.AddUnique(LastTargetInfo);
							MinLastTeleportTypeToTarget.ScriptIDToTargetInfo.AddUnique(MinLastScriptIDToTarget);
							MinLastSpaceTargetPos.TeleportTypeToTargetInfo.AddUnique(MinLastTeleportTypeToTarget);

							MinCurrentSpaceTargetPos.SpaceName = CurrentSpaceTargetPos.SpaceName;
							FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO MinCurrentTeleportTypeToTarget;
							MinCurrentTeleportTypeToTarget.TeleportType = CurrentTeleportTypeToTarget.TeleportType;
							MinCurrentTeleportTypeToTarget.ScriptIDToTargetInfo.AddUnique(CurrentScriptIDToTarget);
							MinCurrentSpaceTargetPos.TeleportTypeToTargetInfo.AddUnique(MinCurrentTeleportTypeToTarget);
						}
					}
				}
			}
			
		}
	}
	if (!MinLastSpaceTargetPos.SpaceName.IsEmpty())
	{
		FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO TeleportTypeToTarget = MinLastSpaceTargetPos.TeleportTypeToTargetInfo[0];
		FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO ScriptIDToTarget = TeleportTypeToTarget.ScriptIDToTargetInfo[0];
		MapTargetInfo.TeleportType = TeleportTypeToTarget.TeleportType;
		MapTargetInfo.SpaceName = MinLastSpaceTargetPos.SpaceName;
		MapTargetInfo.ScriptID = ScriptIDToTarget.ScriptID;
		MapTargetInfo.Position = ScriptIDToTarget.Position;
		MapTargetInfo.Param1 = ScriptIDToTarget.TargetParam[0].Param1;
		MapTargetInfo.Param2 = ScriptIDToTarget.TargetParam[0].Param2;
		MapTargetInfo.Param3 = ScriptIDToTarget.TargetParam[0].Param3;
		MapPathInfo.AddUnique(MapTargetInfo);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::CalculateShortestMultiPosToMultiPos SpaceName:%s TeleportType:%d"), *(MinLastSpaceTargetPos.SpaceName), int(TeleportTypeToTarget.TeleportType));
	}
	else
	{
		FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO TeleportTypeToTarget = LastSpaceTargetPos.TeleportTypeToTargetInfo[0];
		FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO ScriptIDToTarget = TeleportTypeToTarget.ScriptIDToTargetInfo[0];
		MapTargetInfo.TeleportType = TeleportTypeToTarget.TeleportType;
		MapTargetInfo.SpaceName = LastSpaceTargetPos.SpaceName;
		MapTargetInfo.ScriptID = ScriptIDToTarget.ScriptID;
		MapTargetInfo.Position = ScriptIDToTarget.Position;
		MapTargetInfo.Param1 = ScriptIDToTarget.TargetParam[0].Param1;
		MapTargetInfo.Param2 = ScriptIDToTarget.TargetParam[0].Param2;
		MapTargetInfo.Param3 = ScriptIDToTarget.TargetParam[0].Param3;
		MapPathInfo.AddUnique(MapTargetInfo);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::CalculateShortestMultiPosToMultiPos SpaceName:%s TeleportType:%d"), *(LastSpaceTargetPos.SpaceName), int(TeleportTypeToTarget.TeleportType));
	}
	LastSpaceTargetPos = MinLastSpaceTargetPos;
	CurrentSpaceTargetPos = MinCurrentSpaceTargetPos;
}

void UCrossMapNavigateMgr::CalculateShortestMultiPosToPos(const FString& SpaceName, const FString& ScriptID, FVector Pos, FCROSS_MAP_SPACE_TARGET_INFO& SpaceTargetPos, TArray<FCROSS_MAP_TARGET_INFO>& MapPathInfo, bool IsFirst)
{
	float MinDistance = MAX_flt;
	FCROSS_MAP_TARGET_INFO MapTargetInfo;
	FCROSS_MAP_SPACE_TARGET_INFO MinSpaceTargetPos;
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCrossMapNavigateMgr::CalculateShortestMultiPosToPos : Player!"));
		return;
	}
	if (IsFirst)
	{
		for (auto TeleportTypeToTarget: SpaceTargetPos.TeleportTypeToTargetInfo)
		{
			for (auto ScriptIDToTarget:TeleportTypeToTarget.ScriptIDToTargetInfo)
			{
				float Distance = FVector::Dist(Pos, ScriptIDToTarget.Position);
				TArray<FVector> StartAutoPathList;
				Player->GetBestNavigatePathList(Pos, ScriptIDToTarget.Position, SpaceName, StartAutoPathList);
				if (Distance < MinDistance && StartAutoPathList.Num() > 1)
				{
					MinDistance = Distance;

					ClearCrossMapSpaceTarget(MinSpaceTargetPos);

					MinSpaceTargetPos.SpaceName = SpaceTargetPos.SpaceName;
					FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO MinTeleportTypeToTarget;
					MinTeleportTypeToTarget.TeleportType = TeleportTypeToTarget.TeleportType;
					MinTeleportTypeToTarget.ScriptIDToTargetInfo.AddUnique(ScriptIDToTarget);
					MinSpaceTargetPos.TeleportTypeToTargetInfo.AddUnique(MinTeleportTypeToTarget);
					CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::CalculateShortestMultiPosToPos SpaceName:%s TeleportType:%d"), *(SpaceTargetPos.SpaceName), int(TeleportTypeToTarget.TeleportType));
				}
			}
		}
		if (!MinSpaceTargetPos.SpaceName.IsEmpty())
		{
			SpaceTargetPos = MinSpaceTargetPos;
		}
	}
	else
	{
		for (auto TeleportTypeToTarget : SpaceTargetPos.TeleportTypeToTargetInfo)
		{
			if (TeleportTypeToTarget.TeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportTrap)
			{
				continue;
			}
			for (auto ScriptIDToTarget : TeleportTypeToTarget.ScriptIDToTargetInfo)
			{
				for (auto TargetInfo: ScriptIDToTarget.TargetParam)
				{
					float Distance = FVector::Dist(Pos, TargetInfo.TargetPosition);
					if (Distance < MinDistance)
					{
						MinDistance = Distance;

						ClearCrossMapSpaceTarget(MinSpaceTargetPos);

						MinSpaceTargetPos.SpaceName = SpaceTargetPos.SpaceName;
						FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO MinTeleportTypeToTarget;
						MinTeleportTypeToTarget.TeleportType = TeleportTypeToTarget.TeleportType;
						FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO MinScriptIDToTarget;
						MinScriptIDToTarget.ScriptID = ScriptIDToTarget.ScriptID;
						MinScriptIDToTarget.Position = ScriptIDToTarget.Position;
						MinScriptIDToTarget.TargetParam.AddUnique(TargetInfo);
						MinTeleportTypeToTarget.ScriptIDToTargetInfo.AddUnique(MinScriptIDToTarget);
						MinSpaceTargetPos.TeleportTypeToTargetInfo.AddUnique(MinTeleportTypeToTarget);
					}
				}
			}
		}
		if (!MinSpaceTargetPos.SpaceName.IsEmpty())
		{
			FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO TeleportTypeToTarget = MinSpaceTargetPos.TeleportTypeToTargetInfo[0];
			FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO ScriptIDToTarget = TeleportTypeToTarget.ScriptIDToTargetInfo[0];
			MapTargetInfo.TeleportType = TeleportTypeToTarget.TeleportType;
			MapTargetInfo.SpaceName = MinSpaceTargetPos.SpaceName;
			MapTargetInfo.ScriptID = ScriptIDToTarget.ScriptID;
			MapTargetInfo.Position = ScriptIDToTarget.Position;
			MapTargetInfo.Param1 = ScriptIDToTarget.TargetParam[0].Param1;
			MapTargetInfo.Param2 = ScriptIDToTarget.TargetParam[0].Param2;
			MapTargetInfo.Param3 = ScriptIDToTarget.TargetParam[0].Param3;
			MapPathInfo.AddUnique(MapTargetInfo);
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::CalculateShortestMultiPosToPos 1 SpaceName:%s TeleportType:%d"), *(MinSpaceTargetPos.SpaceName), int(TeleportTypeToTarget.TeleportType));
		}
		else
		{
			if (SpaceTargetPos.TeleportTypeToTargetInfo.Num() > 0)
			{
				FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO TeleportTypeToTarget = SpaceTargetPos.TeleportTypeToTargetInfo[0];
				FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO ScriptIDToTarget = TeleportTypeToTarget.ScriptIDToTargetInfo[0];
				MapTargetInfo.TeleportType = TeleportTypeToTarget.TeleportType;
				MapTargetInfo.SpaceName = SpaceTargetPos.SpaceName;
				MapTargetInfo.ScriptID = ScriptIDToTarget.ScriptID;
				MapTargetInfo.Position = ScriptIDToTarget.Position;
				MapTargetInfo.Param1 = ScriptIDToTarget.TargetParam[0].Param1;
				MapTargetInfo.Param2 = ScriptIDToTarget.TargetParam[0].Param2;
				MapTargetInfo.Param3 = ScriptIDToTarget.TargetParam[0].Param3;
				MapPathInfo.AddUnique(MapTargetInfo);
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::CalculateShortestMultiPosToPos 2 SpaceName:%s TeleportType:%d"), *(SpaceTargetPos.SpaceName), int(TeleportTypeToTarget.TeleportType));
			}
			else
			{
				MapPathInfo.Empty();
				return;
			}
		}
		FCROSS_MAP_TARGET_INFO EndMapTargetInfo;
		EndMapTargetInfo.TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportDefault;
		EndMapTargetInfo.SpaceName = SpaceName;
		EndMapTargetInfo.ScriptID = ScriptID;
		EndMapTargetInfo.Position = Pos;
		MapPathInfo.AddUnique(EndMapTargetInfo);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCrossMapNavigateMgr::CalculateShortestMultiPosToPos 3 SpaceName:%s TeleportType:%d"), *SpaceName, int(EndMapTargetInfo.TeleportType));

	}
}

void UCrossMapNavigateMgr::DataTransfer(const FCROSS_MAP_START_TO_END_INFO& StartToEndInfo, FCROSS_MAP_SPACE_TARGET_INFO& SpaceTargetPos)
{
	if (!PlayerCrossMapConnectInfos.Contains(StartToEndInfo))
	{
		return;
	}
	FCROSS_MAP_TELEPORT_INFO TeleportInfo = PlayerCrossMapConnectInfos[StartToEndInfo];
	SpaceTargetPos.SpaceName = StartToEndInfo.StartSpace;
	//优先级：传送点传送＞车夫传送＞NPC/陷阱传送
	if (TeleportInfo.TeleportPointInfos.Num() > 0)
	{
		APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		if (IsValid(Player))
		{
			FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO TeleportTypeToTarget;
			TeleportTypeToTarget.TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportPoint;
			FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO ScriptIDToTargetParam;
			ScriptIDToTargetParam.ScriptID = "";
			ScriptIDToTargetParam.Position = Player->GetActorLocation();
			for (auto TeleportPointInfo : TeleportInfo.TeleportPointInfos)
			{
				FCROSS_MAP_TARGET_PARAM_INFO TargetParamInfo;
				TargetParamInfo.TargetPosition = TeleportPointInfo.TeleportPos;
				TargetParamInfo.Param1 = TeleportPointInfo.TeleportIndex;
				ScriptIDToTargetParam.TargetParam.AddUnique(TargetParamInfo);
			}
			TeleportTypeToTarget.ScriptIDToTargetInfo.AddUnique(ScriptIDToTargetParam);
			SpaceTargetPos.TeleportTypeToTargetInfo.AddUnique(TeleportTypeToTarget);
			return;
		}
	}
	if (TeleportInfo.CarterInfos.Num() > 0)
	{
		FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO TeleportTypeToTarget;
		TeleportTypeToTarget.TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportCarter;
		for (auto CarterInfo : TeleportInfo.CarterInfos)
		{
			FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO ScriptIDToTargetParam;
			ScriptIDToTargetParam.ScriptID = CarterInfo.ScriptID;
			ScriptIDToTargetParam.Position = CarterInfo.Position;
			FCROSS_MAP_TARGET_PARAM_INFO TargetParamInfo;
			if (TeleportTypeToTarget.ScriptIDToTargetInfo.Contains(ScriptIDToTargetParam))
			{
				int32 Index = TeleportTypeToTarget.ScriptIDToTargetInfo.IndexOfByKey(ScriptIDToTargetParam);
				ScriptIDToTargetParam = TeleportTypeToTarget.ScriptIDToTargetInfo[Index];
			}
			TargetParamInfo.TargetPosition = CarterInfo.TeleportPos;
			TargetParamInfo.Param1 = CarterInfo.TalkKey;
			ScriptIDToTargetParam.TargetParam.AddUnique(TargetParamInfo);
			TeleportTypeToTarget.ScriptIDToTargetInfo.AddUnique(ScriptIDToTargetParam);
		}
		SpaceTargetPos.TeleportTypeToTargetInfo.AddUnique(TeleportTypeToTarget);
		return;
	}
	if (TeleportInfo.NPCInfos.Num() > 0)
	{
		FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO TeleportTypeToTarget;
		TeleportTypeToTarget.TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportNPC;
		for (auto NPCInfo : TeleportInfo.NPCInfos)
		{
			FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO ScriptIDToTargetParam;
			ScriptIDToTargetParam.ScriptID = NPCInfo.ScriptID;
			ScriptIDToTargetParam.Position = NPCInfo.Position;
			FCROSS_MAP_TARGET_PARAM_INFO TargetParamInfo;
			if (TeleportTypeToTarget.ScriptIDToTargetInfo.Contains(ScriptIDToTargetParam))
			{
				int32 Index = TeleportTypeToTarget.ScriptIDToTargetInfo.IndexOfByKey(ScriptIDToTargetParam);
				ScriptIDToTargetParam = TeleportTypeToTarget.ScriptIDToTargetInfo[Index];
			}
			TargetParamInfo.TargetPosition = NPCInfo.TeleportPos;
			TargetParamInfo.Param1 = NPCInfo.TalkKey;
			ScriptIDToTargetParam.TargetParam.AddUnique(TargetParamInfo);
			TeleportTypeToTarget.ScriptIDToTargetInfo.AddUnique(ScriptIDToTargetParam);
		}
		SpaceTargetPos.TeleportTypeToTargetInfo.AddUnique(TeleportTypeToTarget);
	}
	if (!TeleportInfo.TrapInfo.ScriptID.IsEmpty())
	{
		FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO TeleportTypeToTarget;
		TeleportTypeToTarget.TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportTrap;
		FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO ScriptIDToTargetParam;
		ScriptIDToTargetParam.ScriptID = TeleportInfo.TrapInfo.ScriptID;
		ScriptIDToTargetParam.Position = TeleportInfo.TrapInfo.Position;
		FCROSS_MAP_TARGET_PARAM_INFO TargetParamInfo;
		TargetParamInfo.TargetPosition = FVector::ZeroVector;
		ScriptIDToTargetParam.TargetParam.AddUnique(TargetParamInfo);
		TeleportTypeToTarget.ScriptIDToTargetInfo.AddUnique(ScriptIDToTargetParam);
		SpaceTargetPos.TeleportTypeToTargetInfo.AddUnique(TeleportTypeToTarget);
	}
	if (!TeleportInfo.SpaceDoorInfo.ScriptID.IsEmpty())
	{
		FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO TeleportTypeToTarget;
		TeleportTypeToTarget.TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportSpaceDoor;
		FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO ScriptIDToTargetParam;
		ScriptIDToTargetParam.ScriptID = TeleportInfo.SpaceDoorInfo.ScriptID;
		ScriptIDToTargetParam.Position = TeleportInfo.SpaceDoorInfo.Position;
		FCROSS_MAP_TARGET_PARAM_INFO TargetParamInfo;
		TargetParamInfo.TargetPosition = TeleportInfo.SpaceDoorInfo.TeleportPos;
		ScriptIDToTargetParam.TargetParam.AddUnique(TargetParamInfo);
		TeleportTypeToTarget.ScriptIDToTargetInfo.AddUnique(ScriptIDToTargetParam);
		SpaceTargetPos.TeleportTypeToTargetInfo.AddUnique(TeleportTypeToTarget);
	}
}

FVector UCrossMapNavigateMgr::GetSpacePosInConfig(const FString& SpaceName)
{
	const UConfigTable* CrossMapNavigatgeTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CROSS_MAP_NAVIGATE_DATA);
	TArray<FCROSS_MAP_CONFIG_DATA*> CrossMapConfigDatas;
	CrossMapNavigatgeTable->GetAllRows(CrossMapConfigDatas);
	for (auto CrossMapData : CrossMapConfigDatas)
	{
		if (CrossMapData->DstSpace == SpaceName)
		{
			FVector NPCPosition;
			UGolbalBPFunctionLibrary::GetNPCPositionFromTable(CrossMapData->CurrentSpace, CrossMapData->ScriptID, NPCPosition);
			return NPCPosition;
		}
	}
	return FVector::ZeroVector;
}

FString UCrossMapNavigateMgr::GetStartSpaceInConfig(const FString& SpaceName)
{
	const UConfigTable* CrossMapNavigatgeTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CROSS_MAP_NAVIGATE_DATA);
	TArray<FCROSS_MAP_CONFIG_DATA*> CrossMapConfigDatas;
	CrossMapNavigatgeTable->GetAllRows(CrossMapConfigDatas);
	for (auto CrossMapData : CrossMapConfigDatas)
	{
		if (CrossMapData->DstSpace == SpaceName)
		{
			return CrossMapData->CurrentSpace;
		}
	}
	return TEXT("");

}


void UCrossMapNavigateMgr::GetSameSpaceTeleportPointInfo(const FString& SpaceName, FVector StartPos, FVector EndPos, FCROSS_MAP_TARGET_INFO& MapTargetInfo)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(Player))
	{
		KBEngine::Entity* PlayerEntity = Player->GetSelfEntity();
		if (PlayerEntity != nullptr)
		{
			FString TeleportPointNPCs = PlayerEntity->GetDefinedProperty(TEXT("teleportPointNPCs"));
			int32 Camp = PlayerEntity->GetDefinedProperty(TEXT("camp")).GetValue<int32>();
			int32 Level = PlayerEntity->GetDefinedProperty(TEXT("level")).GetValue<int16>();
			TArray<FString> TeleportPointLists = UGolbalBPFunctionLibrary::SplitString(TeleportPointNPCs, true, TEXT("|"));
			float MinEndDistance = MAX_flt;

			const UConfigTable* TeleportPointTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TELEPORT_POINT_DATA);
			TArray<FName> TeleportPointIndexs = TeleportPointTable->GetRowNames();

			for (auto TeleportPointIndex : TeleportPointIndexs)
			{
				const FTELEPORT_POINT_DATA* TeleportPoint = TeleportPointTable->GetRow<FTELEPORT_POINT_DATA>(TeleportPointIndex);
				if (SpaceName.Equals(TeleportPoint->ScriptID) && TeleportPointLists.Contains(TeleportPointIndex.ToString()) && Level >= TeleportPoint->LimitLevel && \
					(TeleportPoint->LimitCamp == 0 || TeleportPoint->LimitCamp == Camp))
				{
					float EndDistance = FVector::Distance(EndPos, TeleportPoint->Position);
					TArray<FVector> EndAutoPathList;
					Player->GetBestNavigatePathList(TeleportPoint->Position, EndPos, SpaceName, EndAutoPathList);
					if (EndDistance < MinEndDistance && EndAutoPathList.Num() > 1)
					{
						MapTargetInfo.SpaceName = SpaceName;
						MapTargetInfo.TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportPoint;
						MapTargetInfo.Param1 = TeleportPointIndex.ToString();
						MinEndDistance = EndDistance;
					}
				}
			}

		}
	}
}

FString UCrossMapNavigateMgr::GetTeleportPointDstName(const FString& PointID)
{
	FString DstName = "";
	const UConfigTable* TeleportPointTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TELEPORT_POINT_DATA);
	TArray<FName> TeleportPointIndexs = TeleportPointTable->GetRowNames();

	if (TeleportPointIndexs.Contains(FName(*PointID)))
	{
		const FTELEPORT_POINT_DATA* TeleportPoint = TeleportPointTable->GetRow<FTELEPORT_POINT_DATA>(FName(*PointID));
		return TeleportPoint->DstName;
	}
	return DstName;
}

//是否能够使用传送点传送
bool UCrossMapNavigateMgr::IsCanUseTeleportPoint(const FString& StartSpace, const int& QuestID)
{
	if (ForbidUseTeleportInfos.Contains(StartSpace) && ForbidUseTeleportInfos[StartSpace])
	{
		return false;
	}
	if (QuestID != 0)
	{
		return true;
	}
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(Player))
	{
		TArray<UItemBase*> ItemList = Player->GetItemTeleportStone();
		if (ItemList.Num() > 0)
		{
			return true;
		}
	}
	return false;
}

void UCrossMapNavigateMgr::ClearCrossMapSpaceTarget(FCROSS_MAP_SPACE_TARGET_INFO& SpaceTargetInfo)
{
	SpaceTargetInfo.SpaceName = TEXT("");
	SpaceTargetInfo.TeleportTypeToTargetInfo.Empty();
}

CONTROL_COMPILE_OPTIMIZE_END
