// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

// UE4
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
// 数据类型
#include "GameData/ModelPartData.h"
#include "CollisionComponent.generated.h"

/*
* 文件名称：CollisionComponent.h
* 功能说明：碰撞组件
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-02-07
*/

struct FACTION_DATA;
//enum class WATER_TYPE_ENUM;

UCLASS(BlueprintType)
class CHUANGSHI_API UCollisionComponent : public UActorComponent
{
	GENERATED_BODY()
public:	

	void UpdateModelCollision();///<更新模型碰撞

	bool UpdateModelCollisionByFlag();

	bool UpdateModelCollisionByState();

	bool UpdateModelCollisionByChannel();

	void SetPlayerCollisionByNormal();///<设置客户端玩家自己正常碰撞

	void SetPlayerCollisionByCast();///<设置客户端玩家施法时的碰撞

	///<考虑到需要组件也需要设置碰撞通道，所以这里给了一个默认值，详情见函数内部实现
	void SetPlayerCollisionResponseToChannel(ECollisionChannel Channel, UPrimitiveComponent* Comp = nullptr);

	// 初始化所有Mesh和胶囊体的碰撞
	void InitCollision();

	// 关闭模型所有碰撞，一般在Actor被销毁时调用
	void DisableAllCollision();

	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

	// 设置水面碰撞
	UFUNCTION(BlueprintCallable, Category = "CollisionComponent")
	static void SetWaterCollision(UPrimitiveComponent* Component, WATER_TYPE_ENUM WaterType);

private:
	
	// 当前身体正在使用的碰撞通道 24 到 31 (ECC_GameTraceChannel11 - ECC_GameTraceChannel18)，每一帧刷新为-1
	int32 CurrentTrace = -1;

	// 当前碰撞标志位的缓存
	int64 FlagCache = 0;

	FDelegateHandle BlockMeshHandle;
};
