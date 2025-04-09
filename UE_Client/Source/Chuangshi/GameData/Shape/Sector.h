
#pragma once

#include "GameData/Shape/BaseShape.h"
#include "Sector.generated.h"

/**
* 文件名称：Sector.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-12-22
*/

UCLASS(BlueprintType)
class UShapeSector : public UBaseShape
{

	GENERATED_BODY()

public:
	UShapeSector();
	~UShapeSector();

	virtual bool ActorOnShape();

	virtual void UpdateBounds(FVector Parameter);

public:
	///半径，角度和高度
	float Radius, Angle, Height;
};

