// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "KBEngine.h"
#include "Components/ActorComponent.h"
#include "PetPosSyncComponent.generated.h"

/*
* 文件名称：PetPosSyncComponent.h
* 功能说明：幻兽同步移动位置组件（主要向服务器发送同步主角当前移动位置）
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-12-17
*/

UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class CHUANGSHI_API UPetPosSyncComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UPetPosSyncComponent();
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
	KBEngine::Entity* GetMEntity();
	float OldBlendMoveDirection;

};
