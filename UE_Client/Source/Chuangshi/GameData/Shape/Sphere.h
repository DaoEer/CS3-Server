
#pragma once

#include "GameData/Shape/BaseShape.h"
#include "Sphere.generated.h"

/**
* 文件名称：Sphere.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-12-22
*/

UCLASS(BlueprintType)
class UShapeSphere : public UBaseShape
{

	GENERATED_BODY()

public:
	UShapeSphere();
	~UShapeSphere();

	virtual bool ActorOnShape();

	virtual void UpdateBounds(FVector Parameter);

public:
	///半径
	float Radius;
};

