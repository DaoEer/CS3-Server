// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
//UE4
#include "Engine/EngineTypes.h"
//CS3数据
#include "GameData/CharacterData.h"
//CS3
#include "Components/ActorComponent.h"
#include "RideCarrierComponent.generated.h"

/*
* 文件名称：RideCarrierComponent.h
* 功能说明：负责主角的骑乘功能
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2018-11-15
*/

class ARiderCharacter;
class URoleAnimInstance;
class URiderAnimInstance;
class UJumpComponent;

DECLARE_STATS_GROUP(TEXT("URideCarrierComponent"), STATGROUP_URideCarrierComponent, STATCAT_Advanced);

DECLARE_MULTICAST_DELEGATE(FCreateRoleAppearanceDelegate);///当前动作准备改变时
UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class CHUANGSHI_API URideCarrierComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	URideCarrierComponent();
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;
	void Destroy();

	/*----------------骑乘功能相关---------------------------*/
	void RideOnPet(FString RideCarrideId);///服务器通知上骑宠 
	void DisRideOnPet();///下骑宠
	void PlayBindAction(FACTION_DATA ActionData);
	bool IsRidePetState();///<是否骑乘状态[不包含载具状态，骑乘只是载具里面的一种途径]

	/*----------------载具功能相关---------------------------*/
	void RideOnCarrier(FString InCarrierId);///上载具
	void DisRideOnCarrier();///下载具
	void ClearRideOnCarrier();/// 只消除载具，不变回原始模型
	bool IsCarrierState();///<是否在载具状态[包含骑乘、御剑都属载具状态]
	bool IsDisCarrierState();///<是否在下载具状态

	void CreateRiderActorComponent();
	void DestroyRiderComponent();
	void StartRideGetOnAction();
	ARiderCharacter* GetRiderCharacter();///获取玩家坐骑Actor


protected:
	virtual void BeginPlay() override;

private:
	/*----------------骑乘功能相关---------------------------*/
	void PlayRideEffect(FString EffectId);

	/*----------------上载具(法宝)相关---------------------------*/
	void RideGetOnActionOver();
	void RideGetOffActionOver(bool IsCreateAppearance);

	void ClearTimer(FTimerHandle& InHandle);

	URoleAnimInstance* GetRoleAnimInstance();
	URiderAnimInstance* GetRiderAnimInstance();

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UChildActorComponent* RiderActorComponent;
	bool bIsDisRideOnCarrier = false;///<下载具过程状态记录
	FString CarrierId;///载具（法宝）ID
	FCreateRoleAppearanceDelegate OnCreateRoleAppearance;
	
protected:
	 
private:
	/*----------------骑乘功能相关---------------------------*/
	FTimerHandle RiderGetOnFrameTimerHle;///上载具每帧更新骑士位置
	FTimerHandle RiderGetOnTimerHle;///上载具定时器
	FTimerHandle RiderGetOffTimerHle;///下载具定时器
	float SocketRideSapceZ = 0.0f;
	float RiderOffsetX = -100.0f;

	FACTION_DATA CurActionData;//绑定时当前动作播放
};
