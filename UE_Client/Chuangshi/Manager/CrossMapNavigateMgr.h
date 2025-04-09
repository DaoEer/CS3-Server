#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/CrossMapConfigData.h"
#include "CrossMapNavigateMgr.generated.h"

/*
* 文件名称：CrossMapNavigateMgr.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-11-24
*/

class SpacePathVertex
{
public:
	SpacePathVertex(const FString& SpaceName);
	virtual ~SpacePathVertex();

	int32 NeighboursCount() const;

	void insertNeighbour(SpacePathVertex* Vertex);
	void removeNeighbour(SpacePathVertex* Vertex);

	const FString& GetSpaceName() const;
	//float VerticesCost(const SpacePathVertex* Vertex) const;

	void ShortestPathInit();

	float GetCost() const;
	void SetCost(float Cost);
	ENUM_CROSS_MAP_TELEPORT_TYPE GetTeleportType() const;
	void SetTeleportType(ENUM_CROSS_MAP_TELEPORT_TYPE TeleportType);
	//SpacePathVertex* GetNext();
	//void SetNext(SpacePathVertex* Vertex);
	SpacePathVertex* GetPrev();
	void SetPrev(SpacePathVertex* Vertex);
	SpacePathVertex* GetNeighbourByIndex(int32 Index);

private:
	FString SpaceName_;
	TArray<SpacePathVertex*> Neighbours_;
	float Cost_;
	ENUM_CROSS_MAP_TELEPORT_TYPE TeleportType_;
	//SpacePathVertex* Next_;
	SpacePathVertex* Prev_;

};



UCLASS(BlueprintType)
class CHUANGSHI_API UCrossMapNavigateMgr : public UCS3Object
{
	GENERATED_BODY()
public:
	UCrossMapNavigateMgr();
	virtual ~UCrossMapNavigateMgr();

	static UCrossMapNavigateMgr* GetInstance();
	int32 VerticesCount() const;

	void LoadConfig();
	void Dijkstra(SpacePathVertex* StartVertex, SpacePathVertex* EndVertex);

	TArray<FCROSS_MAP_TARGET_INFO> FindCrossMapPath(const FString& StartSpaceName, const FString& EndSpaceName, const FVector& StartPosition, const FVector& EndPosition = FVector::ZeroVector, const FString& ScriptID = "", const int& AutoQuestID = 0);
	void GetSameSpaceTeleportPointInfo(const FString& SpaceName, FVector StartPos, FVector EndPos, FCROSS_MAP_TARGET_INFO& MapTargetInfo);
	bool IsCanUseTeleportPoint(const FString& StartSpace, const int& QuestID);
	FString GetTeleportPointDstName(const FString& PointID);

private:
	void Clear();
	void ClearVertex();
	void AddVertex(const FString& SpaceName);
	SpacePathVertex* GetVertex(const FString& SpaceName);
	void AddEdge(const FString& Start, const FString& End);

	void ShortestPathInit();
	void AdjustVertexPrev(SpacePathVertex* Source, SpacePathVertex* Target);
	void InitVertexAndEdge();
	void CalculateShortestMultiPosToMultiPos(FCROSS_MAP_SPACE_TARGET_INFO& LastSpaceTargetPos, FCROSS_MAP_SPACE_TARGET_INFO& CurrentSpaceTargetPos, TArray<FCROSS_MAP_TARGET_INFO>& MapPathInfo);
	void CalculateShortestMultiPosToPos(const FString& SpaceName, const FString& ScriptID, FVector Pos, FCROSS_MAP_SPACE_TARGET_INFO& SpaceTargetPos, TArray<FCROSS_MAP_TARGET_INFO>& MapPathInfo, bool IsFirst);
	void DataTransfer(const FCROSS_MAP_START_TO_END_INFO& StartToEndInfo, FCROSS_MAP_SPACE_TARGET_INFO& SpaceTargetPos);
	FVector GetSpacePosInConfig(const FString& SpaceName);
	FString GetStartSpaceInConfig(const FString& SpaceName);
	
	void ClearCrossMapSpaceTarget(FCROSS_MAP_SPACE_TARGET_INFO& SpaceTargetInfo);

	void LoadMapConfig();
	ENUM_CROSS_MAP_TELEPORT_TYPE GetTeleportTypeForPriority(SpacePathVertex* SrcVertex, SpacePathVertex * DstVertex);

private:
	TArray<SpacePathVertex*> Vertices_;
	TMap<FString, SpacePathVertex*> VerticesMap_;
	UPROPERTY()
		TMap<FCROSS_MAP_START_TO_END_INFO, FCROSS_MAP_TELEPORT_INFO> CrossMapConnectInfos;
	UPROPERTY()
		TMap<FString, FMAP_RELATED_INFO> MapRelatedInfos;
	UPROPERTY()
		TMap<FString, int32> TeleportPointToCamp;
	UPROPERTY()
		TMap<FString, int32> TeleportPointToLevel;
	TMap<FCROSS_MAP_START_TO_END_INFO, FCROSS_MAP_TELEPORT_INFO> PlayerCrossMapConnectInfos;
	TMap<FString, bool> ForbidUseTeleportInfos;
	int AutoQuestID;

	int CROSS_MAP_SPACE_NUM = -1;	//跨地图数量限制，-1表示没有限制

};