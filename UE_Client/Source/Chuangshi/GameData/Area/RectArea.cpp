// Fill out your copyright notice in the Description page of Project Settings.


#include "RectArea.h"

RectArea::RectArea()
{
}

RectArea::~RectArea()
{
}

void RectArea::UpdatePoint(FVector2D& MinPoint, FVector2D& MaxPoint)
{
	MinPos = MinPoint;
	MaxPos = MaxPoint;
}

bool RectArea::IsPointIn(FVector & Position)
{
	if (MinPos.X <= Position.X && MinPos.Y <= Position.Y &&
		MaxPos.X >= Position.X && MaxPos.Y >= Position.Y)
	{
		return true;
	}
	return false;
}
