

#include "CS3Algorithms.h"


FVector GetSepratePoint(const FVector& StartPoint, const FVector& EndPoint, float NeedDistance)
{
	float PointDist = FVector::Distance(StartPoint, EndPoint);
	if (FMath::IsNearlyZero(PointDist))
	{
		return StartPoint;
	}
	float Scale = NeedDistance / PointDist;
	float PointX, PointY, PointZ;
	PointX = StartPoint.X + (EndPoint.X - StartPoint.X) * Scale;
	PointY = StartPoint.Y + (EndPoint.Y - StartPoint.Y) * Scale;
	PointZ = StartPoint.Z + (EndPoint.Z - StartPoint.Z) * Scale;
	return FVector(PointX, PointY, PointZ);
}


TArray<FVector> AnalysicsPathList(const TArray<FVector>& PathList, float MinDis)
{
	TArray<FVector> Path;
	if (PathList.Num() <= 0)
	{
		return Path;
	}
	int PathListIndex = 1;
	FVector CurrPos, NewPos;
	CurrPos = PathList[0];
	NewPos = PathList[0];
	float RestOfDis = 0.0f;	//小于MinDis的余下部分
	while ( PathListIndex < PathList.Num() )
	{
		float TempRestOfDis = RestOfDis;	//小于MinDis的余下部分的临时值
		float DisBetweenCurrPointAndNextPathPoint;	//当前点和路径中下一个路点之间的距离
		DisBetweenCurrPointAndNextPathPoint = FVector::Distance(PathList[PathListIndex], CurrPos);
		if (DisBetweenCurrPointAndNextPathPoint + RestOfDis > 2 * MinDis)	//当前距离+余下的距离> 2倍的标准距离，表示该2点中间会有多个等距离路径点
		{
			NewPos = GetSepratePoint(CurrPos, PathList[PathListIndex], MinDis - RestOfDis);
			TempRestOfDis = 0.0f;
			CurrPos = NewPos;
			Path.Add(NewPos);
		}
		else if (DisBetweenCurrPointAndNextPathPoint + RestOfDis > MinDis && DisBetweenCurrPointAndNextPathPoint + RestOfDis <= 2 * MinDis)
		{
			NewPos = GetSepratePoint(CurrPos, PathList[PathListIndex], MinDis - RestOfDis);
			TempRestOfDis = DisBetweenCurrPointAndNextPathPoint - MinDis + TempRestOfDis;
			CurrPos = PathList[PathListIndex];
			PathListIndex++;
			Path.Add(NewPos);
		}
		else if (DisBetweenCurrPointAndNextPathPoint + RestOfDis <= MinDis)
		{
			TempRestOfDis += DisBetweenCurrPointAndNextPathPoint;
			CurrPos = PathList[PathListIndex];
			PathListIndex++;
		}
		RestOfDis = TempRestOfDis;
	}
	return Path;
}