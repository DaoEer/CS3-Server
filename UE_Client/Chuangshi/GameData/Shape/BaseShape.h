
#pragma once

#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "BaseShape.generated.h"

/**
* 文件名称：BaseShape.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-12-22
*/

DECLARE_DELEGATE(FSingleShapeDelegate);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FBaseShapeDelegate);

// 服务器和客户端单位比例换算
#define SCALE 100.f

UCLASS(BlueprintType)
class UBaseShape : public UCS3Object
{
	GENERATED_BODY()
public:
	UBaseShape();
	~UBaseShape();

	///玩家是否在形状内
	virtual bool ActorOnShape() { return false; }

	///更新边界
	UFUNCTION(BlueprintCallable)
	virtual void UpdateBounds(FVector Parameter) {}

	///开启tick
	UFUNCTION(BlueprintCallable)
	void EnableTick();

	///关闭tick
	UFUNCTION(BlueprintCallable)
	void DisableTick();

	///销毁Shpae
	UFUNCTION(BlueprintCallable)
	void DestoryShape();

	///重置重叠属性
	UFUNCTION(BlueprintCallable)
	void Reset();

	virtual void BeginDestroy() override;

private:
	///循环检测重叠事件
	void Tick();

public:
	///重叠开始和结束
	FBaseShapeDelegate BeginOverlap;
	FBaseShapeDelegate EndOverlap;

	FSingleShapeDelegate BeginOverlapSingle;
	FSingleShapeDelegate EndOverlapSingle;

	///用来进行距离检测的目标
	UPROPERTY()
	AActor* Owner;

private:
	///tick的句柄
	FTimerHandle TickHandle;
	///重叠状态
	bool bOverlap = false;
};