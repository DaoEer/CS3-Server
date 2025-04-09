// Fill out your copyright notice in the Description page of Project Settings.


#include "Poly.h"
#include "UnrealMathUtility.h"

Poly::Poly()
{
	RectPtr = TSharedPtr<RectArea>(new RectArea());
}

Poly::~Poly()
{
}

void Poly::UpdatePoints(TArray<FVector2D>& Points)
{
	if (Points.Num()==0)return;
	PolyPoints = Points;
	FVector2D MinRectPoint = PolyPoints[0];
	FVector2D MaxRectPoint = PolyPoints[0];
	for (FVector2D Point : PolyPoints)
	{
		if (MinRectPoint.X > Point.X)
		{
			MinRectPoint.X = Point.X;
		}
		if (MinRectPoint.Y > Point.Y)
		{
			MinRectPoint.Y = Point.Y;
		}
		if (MaxRectPoint.X < Point.X)
		{
			MaxRectPoint.X = Point.X;
		}
		if (MaxRectPoint.Y < Point.Y)
		{
			MaxRectPoint.Y = Point.Y;
		}
	}
	if (!RectPtr.IsValid())
	{
		RectPtr = TSharedPtr<RectArea>(new RectArea());
	}
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("Poly UpdatePoints MinRectPoint(%f,%f) MaxRectPoint(%f,%f) "), MinRectPoint.X, MinRectPoint.Y, MaxRectPoint.X, MaxRectPoint.Y);
	RectPtr.Get()->UpdatePoint(MinRectPoint, MaxRectPoint);
}

bool Poly::IsPointIn(FVector & Position)
{
	// 如果不在外接矩形，则必然不在多边形内
	if (RectPtr.IsValid())
	{
		if (!RectPtr->IsPointIn(Position))
		{
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("!RectPtr->IsPointIn------------>>>"));
			return false;
		}
		else if (PolyPoints.Num() == 2)
		{
			return true;
		}
	}
	
	int i, j = PolyPoints.Num();
	bool IsInSide = false;
	float X = Position.X;
	float Y = Position.Y;
	float x1,x2,y1,y2;
	float deltaX12, deltaY12, deltaX, deltaY;
	
	for (i = 0; i <= j - 1; i++)
	{
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("Poly for each------------>>>%i"), i)
		if (i == j - 1)
		{
			x1 = PolyPoints[j - 1].X;
			y1 = PolyPoints[j - 1].Y;
			x2 = PolyPoints[0].X;
			y2 = PolyPoints[0].Y;
		}
		else
		{
			x1 = PolyPoints[i].X;
			y1 = PolyPoints[i].Y;
			x2 = PolyPoints[i + 1].X;
			y2 = PolyPoints[i + 1].Y;
		}

		if ((x1 <= X && X <= x2) || (x2 <= X && X <= x1))
		{
			if (FMath::IsNearlyEqual(X, x2))continue;
			deltaX12 = x1 - x2;
			deltaY12 = y1 - y2;
			deltaX = X - x1;
			deltaY = Y - y1;
			if (deltaX12 > 0 && deltaY * deltaX12 <= deltaX * deltaY12)
			{
				IsInSide = !IsInSide;
			}
			if (deltaX12 < 0 && deltaY * deltaX12 >= deltaX * deltaY12)
			{
				IsInSide = !IsInSide;
			}
		}
	}
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("Poly->IsPointIn------------>>>%i"),IsInSide);
	return IsInSide;
}

bool Poly::IsCloseTo(FVector& Position, float Distance)
{
	int i, j = PolyPoints.Num();
	float x = Position.X;
	float y = Position.Y;
	float x1, x2, y1, y2;
	bool bIsCloseTo = false;
	for (i = 0;i <= j - 1;i++)
	{
		if (i == j - 1)
		{
			x1 = PolyPoints[j - 1].X;
			y1 = PolyPoints[j - 1].Y;
			x2 = PolyPoints[0].X;
			y2 = PolyPoints[0].Y;
		}
		else
		{
			x1 = PolyPoints[i].X;
			y1 = PolyPoints[i].Y;
			x2 = PolyPoints[i + 1].X;
			y2 = PolyPoints[i + 1].Y;
		}
		if ((fabs((x - x1)*(y2 - y1) - (x2 - x1)*(y - y1)) / sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))) <= Distance)
		{
			bIsCloseTo = true;
			break;
		}
	}
	return bIsCloseTo;
}

