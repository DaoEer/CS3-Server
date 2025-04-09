
#pragma once

#include "GameData/Shape/BaseShape.h"
#include "Cylinder.generated.h"

/**
* 文件名称：Cylinder.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-12-22
*/

UCLASS(BlueprintType)
class UShapeCylinder : public UBaseShape
{

	GENERATED_BODY()

public:
	UShapeCylinder();
	~UShapeCylinder();

	virtual bool ActorOnShape();

	virtual void UpdateBounds(FVector Parameter);

public:
	///圆柱体的半径和高
	float Radius, Height;
};

