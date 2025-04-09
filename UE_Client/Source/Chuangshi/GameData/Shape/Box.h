
#pragma once

#include "GameData/Shape/BaseShape.h"
#include "Box.generated.h"

/**
* 文件名称：Box.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-12-22
*/

UCLASS(BlueprintType)
class UShapeBox : public UBaseShape
{

	GENERATED_BODY()

public:
	UShapeBox();
	~UShapeBox();

	virtual bool ActorOnShape();

	virtual void UpdateBounds(FVector Parameter);

public:

	///立方体的长宽高
	float X, Y, Z;
};

