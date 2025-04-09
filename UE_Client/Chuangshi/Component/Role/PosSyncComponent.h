// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "KBEngine.h"
#include "Components/ActorComponent.h"
#include "PosSyncComponent.generated.h"

/*
* 文件名称：PosSyncComponent.h
* 功能说明：角色同步移动位置组件（主要向服务器发送同步主角当前移动位置）
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2016-12-06
*/

UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class CHUANGSHI_API UPosSyncComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	UPosSyncComponent();
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	void setTickDoing(bool bDoing);

	FORCEINLINE void Init(int32 EntityID)
	{
		MEntityID = EntityID;
	}

private:
	KBEngine::Entity* GetMEntity();
	int32 MEntityID = 0;
	float OldBlendMoveDirection;
	
};
