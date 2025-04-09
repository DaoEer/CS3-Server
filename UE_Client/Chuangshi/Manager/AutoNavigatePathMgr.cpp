
#include "AutoNavigatePathMgr.h"
#include "GameData/NavigatePath.h"
#include"Chuangshi.h"
#include "CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"

PathVertex::PathVertex(const FVector& Position):
	Position_(Position),
	Prev_(nullptr)
{
	Cost_ = MAX_flt;
}


PathVertex::~PathVertex()
{
	Neighbours_.Empty();
}

int32 PathVertex::NeighboursCount() const
{
	return Neighbours_.Num();
}

void PathVertex::insertNeighbour(PathVertex* Vertex)
{
	int32 Index;
	bool Result = Neighbours_.Find(Vertex, Index);
	if (!Result)
	{
		Neighbours_.Add(Vertex);
	}
}

void PathVertex::removeNeighbour(PathVertex* Vertex)
{
	int32 Index;
	bool Result = Neighbours_.Find(Vertex, Index);
	if (Result)
	{
		Neighbours_.Remove(Vertex);
	}
}



const FVector& PathVertex::Position() const
{
	return Position_;
}

float PathVertex::VerticesCost(const PathVertex* Vertex) const
{
	if (Vertex != nullptr)
	{
		return FVector::Dist(Position_, Vertex->Position());
	}
	return MAX_flt;
}

void PathVertex::ShortestPathInit()
{
	Prev_ = nullptr;
	Cost_ = MAX_flt;
}

float PathVertex::GetCost() const
{
	return Cost_;
}

void PathVertex::SetCost(float Cost)
{
	Cost_ = Cost;
}

PathVertex* PathVertex::GetPrev()
{
	return Prev_;
}

void PathVertex::SetPrev(PathVertex* Vertex)
{
	Prev_ = Vertex;
}

PathVertex* PathVertex::GetNeighbourByIndex(int32 Index)
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

UAutoNavigatePathMgr::UAutoNavigatePathMgr()
{

}

UAutoNavigatePathMgr::~UAutoNavigatePathMgr()
{
	Clear();
}


void UAutoNavigatePathMgr::Clear()
{
	for (auto It = Vertices_.CreateConstIterator(); It; ++It)
	{
		PathVertex* Vertex = *It;
		C_SAFE_DELETE(Vertex);
	}
	Vertices_.Empty();
	VerticesMap_.Empty();
}

void UAutoNavigatePathMgr::AddVertex(const int32& ID, const FVector& Position)
{
	PathVertex* Vertex = new PathVertex(Position);//UAutoNavigatePathMgr::Clear()ÊÍ·Å
	Vertices_.Add(Vertex);
	VerticesMap_.Add(ID, Vertex);
}

void UAutoNavigatePathMgr::AddEdge(const int32& Start, const int32& End)
{
	check(VerticesMap_[Start]);
	check(VerticesMap_[End]);
	PathVertex* StartVertex = VerticesMap_[Start];
	PathVertex* EndVertex = VerticesMap_[End];
	StartVertex->insertNeighbour(EndVertex);
	EndVertex->insertNeighbour(StartVertex);
}

void UAutoNavigatePathMgr::ShortestPathInit()
{
	for (auto It = Vertices_.CreateConstIterator(); It; ++It)
	{
		PathVertex* Vertex = *It;
		Vertex->ShortestPathInit();
	}
}

void UAutoNavigatePathMgr::AdjustVertexPrev(PathVertex* Source, PathVertex* Target)
{
	float Cost = Source->GetCost() + Source->VerticesCost(Target);
	if (Target && Target->GetCost() > Cost)
	{
		Target->SetCost(Cost);
		Target->SetPrev(Source);
	}
}

UAutoNavigatePathMgr* UAutoNavigatePathMgr::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UAutoNavigatePathMgr>();
}

int32 UAutoNavigatePathMgr::VerticesCount() const
{
	return Vertices_.Num();
}

void UAutoNavigatePathMgr::LoadGraph(const FString& SpaceName)
{
	Clear();
	const UConfigTable* AutoNavigatePathTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_AUTO_NAVIGATE_PATH_DATA);
	const FNAVIGATE_PATH_INFO* NavigatePathData = AutoNavigatePathTable->GetRow<FNAVIGATE_PATH_INFO>(SpaceName);
	if (NavigatePathData != nullptr)
	{
		auto Points = NavigatePathData->Points;
		for (auto It = Points.CreateConstIterator(); It; ++It)
		{
			AddVertex(It->ID, It->Position);
		}
		auto Edges = NavigatePathData->Edges;
		for (auto It = Edges.CreateConstIterator(); It; ++It)
		{
			AddEdge(It->Start, It->End);
		}
	}
}

PathVertex* UAutoNavigatePathMgr::NearestVertex(const FVector& Position)
{
	PathVertex* Vertex = nullptr;
	float Cost = MAX_flt;
	for (auto It = Vertices_.CreateConstIterator(); It; ++It)
	{
		PathVertex* TempVertex = *It;
		float VertexDis = FVector::Dist(Position, TempVertex->Position());
		if (VertexDis < Cost)
		{
			Vertex = TempVertex;
			Cost = VertexDis;
		}
	}
	return Vertex;
}

void UAutoNavigatePathMgr::Dijkstra(PathVertex* Target)
{
	ShortestPathInit();
	Target->SetCost(0.0f);
	TArray<PathVertex*> TempVertices(Vertices_);
	while (TempVertices.Num() > 0)
	{
		float Cost = TempVertices[0]->GetCost();
		PathVertex* MinVertex = TempVertices[0];
		for (auto It = TempVertices.CreateConstIterator(); It; ++It)
		{
			PathVertex* Vertex = *It;
			if (Vertex->GetCost() < Cost)
			{
				Cost = Vertex->GetCost();
				MinVertex = *It;
			}
		}
		TempVertices.Remove(MinVertex);
		for (int32 RelaxIndex = 0; RelaxIndex < MinVertex->NeighboursCount(); ++RelaxIndex)
		{
			AdjustVertexPrev(MinVertex, MinVertex->GetNeighbourByIndex(RelaxIndex));
		}
	}

}

TArray<FVector> UAutoNavigatePathMgr::FindAutoPath(const FString& SpaceName, const FVector& StartPosition, const FVector& EndPosition)
{
	TArray<FVector> PathPoints;
	if (Vertices_.Num() == 0)
	{
		LoadGraph(SpaceName);
	}
	PathVertex* StartVertex = NearestVertex(StartPosition);
	PathVertex* EndVertex = NearestVertex(EndPosition);
	if (StartVertex == nullptr || EndVertex == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UAutoNavigatePathMgr::FindAutoPath : StartVertex||EndVertex!"));
		return PathPoints;
	}
	else if (StartVertex == EndVertex)
	{
		PathPoints.Add(StartVertex->Position());
		return PathPoints;
	}
	Dijkstra(EndVertex);
	while (StartVertex != EndVertex)
	{
		PathPoints.Add(StartVertex->Position());
		StartVertex = StartVertex->GetPrev();
		if (StartVertex == nullptr)
		{
			PathPoints.Empty();
			return PathPoints;
		}
	}
	PathPoints.Add(EndVertex->Position());
	return PathPoints;
}

