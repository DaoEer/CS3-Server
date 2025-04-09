#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "AutoNavigatePathMgr.generated.h"

/*
* 文件名称：AutoNavigatePathMgr.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-09-30
*/

class PathVertex
{
public:
	PathVertex(const FVector& Position);
	virtual ~PathVertex();

	int32 NeighboursCount() const;

	void insertNeighbour(PathVertex* Vertex);
	void removeNeighbour(PathVertex* Vertex);

	const FVector& Position() const;
	float VerticesCost(const PathVertex* Vertex) const;

	void ShortestPathInit();

	float GetCost() const;
	void SetCost(float Cost);
	PathVertex* GetPrev();
	void SetPrev(PathVertex* Vertex);
	PathVertex* GetNeighbourByIndex(int32 Index);

private:
	FVector Position_;
	TArray<PathVertex*> Neighbours_;
	float Cost_;
	PathVertex* Prev_;

};

UCLASS(BlueprintType)
class CHUANGSHI_API UAutoNavigatePathMgr : public UCS3Object
{
	GENERATED_BODY()
public:
	UAutoNavigatePathMgr();
	virtual ~UAutoNavigatePathMgr();

	static UAutoNavigatePathMgr* GetInstance();
	int32 VerticesCount() const;

	void LoadGraph(const FString& SpaceName);
	PathVertex* NearestVertex(const FVector& Position);
	void Dijkstra(PathVertex* Target);
	TArray<FVector> FindAutoPath(const FString& SpaceName, const FVector& StartPosition, const FVector& EndPosition);
	
private:
	void Clear();
	void AddVertex(const int32& ID, const FVector& Position);
	void AddEdge(const int32& Start, const int32& End);

	void ShortestPathInit();
	void AdjustVertexPrev(PathVertex* Source, PathVertex* Target);

private:
	TArray<PathVertex*> Vertices_;
	TMap<int32, PathVertex*> VerticesMap_;
	//static UAutoNavigatePathMgr* Instance;

};