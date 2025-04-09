
#pragma once

#include "GameData/Shape/BaseShape.h"
#include "Capsule.generated.h"

/**
* 文件名称：Capsule.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-12-22
*/

UCLASS(BlueprintType)
class UShpaeCapsule : public UBaseShape
{

	GENERATED_BODY()

public:
	UShpaeCapsule();
	~UShpaeCapsule();

	virtual bool ActorOnShape();

	virtual void UpdateBounds(FVector Parameter);

public:
	///胶囊体的半径和半高
	float Radius, HalfHeight;
};

