// Fill out your copyright notice in the Description page of Project Settings.UForceComponent

#pragma once

#include "GameData/FlyPatrolData.h"
#include "PlayerControllerMoveComponent.h"
#include "GameData/CharacterData.h"
#include "GameFramework/Character.h"
#include "Engine/EngineTypes.h"
#include "FlyPatrolComponent.generated.h"

/*
* 文件名称：FlyPatrolComponent.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2018-6-14
*/


// 飞行状态
UENUM(BlueprintType)
enum class FLYPATORLSTATE_TYPE : uint8
{
	NONE = 0,				///<没有飞行
	DisRide = 1,			///<飞行下骑乘中
	GETON = 2,				///<起跳阶段
	RIDEONCARRIER = 3,		///<飞行走载具阶段
	FLYING = 4,				///<飞行中
	HZMGDisRide =5,			///<<幻阵迷宫飞行下骑乘中
	HZMGGETON = 6,			///<幻阵迷宫起跳阶段
	HZMGRIDEONCARRIER = 7,	///<幻阵迷宫飞行走载具阶段
	HZMGFLYING = 8,			///<幻阵迷宫飞行中
};


class AFlyCharacter;
class AServerCharacter;
class AGameCharacter;
class AClientGameCharacter;

DECLARE_STATS_GROUP(TEXT("UFlyPatrolComponent"), STATGROUP_UFlyPatrolComponent, STATCAT_Advanced);

UCLASS(BlueprintType)
class CHUANGSHI_API UFlyPatrolComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	// Sets default values for this actor's properties
	UFlyPatrolComponent();
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void TickComponent(float DeltaTime, enum ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	//执行飞行功能的入口
	UFUNCTION(BlueprintCallable, Category = "Game|FlyPatrol")
		void EnterFlyPatrol(FString FlyPatrolID, const FString InCarrierId = TEXT(""),
			const FString FlyModleId = TEXT("10002"));///<进入飞行传送

	UFUNCTION(BlueprintCallable, Category = "Game|FlyPatrol")
		void StopFlyPatrol(float DelayTime = 0.0f);///<BlueprintCallable 停止飞行传送

	void StopCycleFlyPatrol(FString FlyPatrolID);///<接出循环飞行传送
	void PauseFlyPatrol();///<暂停飞行
	void ReviveFlyPatrol();///<恢复飞行
	bool IsPausedFlyPatrol();  ///<飞行是否暂停
	void StartFlyPatrol(FString FlyPatrolID);///<开始传送飞行

	bool IsFlyPatrolState();	///<是否在飞行中
	void SwitchFlyOrbitMode(bool IsActivate = true);///<切换到飞行模式
	/*----------------幻阵迷宫飞行功能相关---------------------------*/
	/**
	 *BlueprintCallable 幻阵迷宫 飞行表现
	*
	*@param fPatrolID	飞行路径ID(FString)
	*@param sPatrolID	子飞行路径ID(FString)
	*@param pPoint		飞行开始步长(int32)
	*@param speed		飞行目标步长(int32)
	*@param screneID	飞行目标位置(FString)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|Player")
		void EnterFlyToHZMGSpace(const FString fPatrolID, const FString sPatrolID,
			const int32 sPoint, const int32 pPoint, float speed, FVector enterPos);

	void StopFlyToHZMGSpace(const FString FlyID);///<结束幻阵迷宫飞行	
	bool IsHZMGFlyState(); ///<是否处于幻阵迷宫飞行状态

	/*----------------勇闯绝命岛空中飞行及降落表现(新版吃鸡)---------------------------*/
	void StartYCJMDSkyFly(const FString& FlyPathId);///<开始空中飞行效果
	void LeaveSkyCarrierKeyF();///<按F键执行跳伞效果
	void OpenYCJMDParachuteKeyF();///<按F键执行开伞效果
	void CreateParachuteInst();		///<创建降落伞
	void OpenParachuteSlowSpeed();	/// 开伞降速
	void LandYCJMDParachute();///<降落伞着陆动作
	void LandYCJMDSkyDiving();///<玩家跳伞着陆

private:
	/*----------------飞行功能相关---------------------------*/
	void StartPreFlyPatrol(const FString FlyModleId);///<开始起飞前操作
	void ExecuteRideOnCarrierOrFlyActor(FString FlyPatrolID, const FString InCarrierId, const FString FlyModleId);///<执行载具流程还是飞行Actor流程
	void BindFlyAttachActor(const FString FlyModleId);///<绑定飞行载具	
	void StartBindFlyCharacter(FString FlyCarrierModelId);///<将FlyCharacter绑定到玩家上

	void LoadFlySword();///<加载飞剑
	void StartBindSwordFlyCharacter(FFLY_PATROL_BIND_DATA FlyCarrierBindData);///将飞剑FlyCharacter绑定到玩家上

	void PlayFlyPatrolActionOver(ACharacter* Character, FACTION_DATA ActionData);///<播放完geton动作后播站在法宝上的动作

	void OnStopFlyPatrol(float DelayTime = 0.0f);///<BlueprintCallable 停止飞行传送
	void StartFlyPatrolEvent();///<传送飞行时间轴事件处理

	void CheckFlyPatrol(float FlySpeed, const FVector& Point, bool IsSuccess);///<传送飞行过程中检测
	void CheckFlyPatrolEvent(const FFLYEVENT_DATA& FlyEvent, const FVector& Point = FVector(0, 0, 0));///<传送飞行过程中事件触发检测

	void DestroyFlyAttachActor();///<销毁飞行Actor
	void ClearFlyPatrolHandle();
	void ResetFlyPatrolData();

	const FFLY_PATROL_DATA* GetFlyPatrolData(const FString& FlyPatrolID);///<获取飞行数据相关
	void OnUpdateFlyCharacterVisibility(bool bIsVisibility = true);///<更新Character的可见性
	bool IsNormalFlyPatrolState();	///<是否在普通飞行中


	/*----------------幻阵迷宫相关---------------------------*/
	void OnStopFlyToHZMGSpace();///<结束幻阵迷宫飞行
	/**
	*BlueprintCallable 幻阵迷宫 飞行表现
	*
	*@param fPatrolID	飞行路径ID(FString)
	*@param pPoint		飞行开始步长(int32)
	*@param speed		飞行目标步长(int32)
	*@param screneID	飞行目标位置(FString)
	*
	*@return 无
	*/
	void OnFlyToHZMGSpace(const FString fPatrolID, const int32 sPoint, const int32 pPoint, float speed, FVector enterPos);
	void StartFlyToHZMGSpace(FFLYSUBSPACE_DATA flySubSpaceData);///<开始HZMG飞行
	void BindHZMGCharacterToFlyAttach();///<绑定Character到法宝上
	void OnEndFlyToHZMGSpace(const FString FlyID);///<到达目标位置后通知服务器
	void PlayFlyPatrolActionOverInHZMGSpace(ACharacter* Character, FACTION_DATA ActionData);///<播放完geton动作后播站在法宝上的动作
	void DestroyHZMGSpaceOfFlyAttachActor();///< 幻阵迷宫销毁载具和显示队员模型 	
	void OnHZMGFlySinglePatrol(const FString fPatrolID, const int32 sPoint, const int32 pPoint, float speed, FVector enterPos);///<幻阵迷宫第二版 单条飞行路线
	void CheckSinglePatrolFlyToHZMGSpace(const FString fPatrolID, const FVector Point, int32 sPoint, const int32 tPoint, FVector enterPos, bool IsSuccess);
	void GetHZMGNearestFlyPoint(const FString& PatrolID, const int32 sPoint, FVector& Point);///<获取最近的路点

	void OnHZMGFlyMultPatrol(const FString PatrolID, float Speed);///<幻阵迷宫第三版 多条飞行路线
	void CheckMultPatrolFlyToHZMGSpace(const FString PatrolID, const FVector& Point, bool IsSuccess);

	void DisRideOnCarrierToHZMGFly(FFLYSUBSPACE_DATA flySubSpaceData);

	/*----------------飞行通用接口---------------------------*/
	void onNotifyAddEffectList(FString FlyPatrolID, TArray<int32> EffectList);
	void onNotifyRemoveEffectList(FString FlyPatrolID);

	/*----------------勇闯绝命岛空中飞行及降落表现(新版吃鸡)---------------------------*/
	void CheckYCJMDSkyFlyPoint();///<空中飞行检测下一个目标点
	void CheckSkyCarrierMoveEffect(float DeltaTime);///<空中做轻度roll\pitch效果
	void CheckAutoOpenYCJMDParachute(float DeltaTime); ///<距离地面N米自动开伞
	void CheckPlayRollAction();///<检测播放随机翻滚动作
	void OnSkyCairrerRollActionOver(ACharacter* Character, FACTION_DATA ActionData);///<空中翻滚动作播放完毕

	void OnPlayerLandActionOver(ACharacter* Character, FACTION_DATA ActionData);///<跳伞着陆动作播放完毕

private:
	UPROPERTY()
		AActor* HZMGFlyAttachActor;///<幻阵迷宫飞行传送附加Actor

	UPROPERTY()
		AFlyCharacter* FlyCharacter;///<飞行传送附加Actor

	FLYPATORLSTATE_TYPE FlyPatrolState; ///<传送飞行状态	

	FString CurFlyPatrolID = TEXT("");///<当前飞行传送路径ID
	FFLY_MOVE_INFO FlyMoveInfo;///<飞行暂停时飞行数据
	FTimerHandle FlyPatrolHandle;
	FVector StartCycleFlyPoint;///<接入循环飞行点
	FVector EndCycleFlyPoint;///<接出循环飞行点
	int CurFlyCount;///<当前循环飞行次数

	UPROPERTY()
		TMap<FName, UMeshComponent *> BindMeshComponentDatas;///<绑定的mesh组件

	UPROPERTY()
		TArray<AServerCharacter*> HZMGTeamMembsModle;///<幻阵迷宫飞行队员模型
	FFLYSUBSPACE_DATA FlyHZMGSpaceData;///< 幻阵迷宫飞行数据

	//================勇闯绝命岛空中飞行及降落表现(新版吃鸡)============
	FFLY_PATROL_DATA YCJMDSkyFlyData;
	FTimerHandle SkyCarrierAnimHandle;
	AGameCharacter* SkyCarrierActor;
	FRotator SkyCarrrierRotator;///<初始角度为基准，别把载具底部都给翻出来了
	FRotator SkyCarrrierRollRotator;
	float RollDir = 1.0f;///<记录上一次的翻转方向，防止在同一方向连续翻:1 或者 -1
	float LastPlayerPosZ;
	bool bIsPlayRollAction = false;
	bool bIsPlayReadyLandAction = false;
	FVector SprintArmScoOffset;
	FTimerHandle OpenParachuteHandle;


	AClientGameCharacter* ParachuteCharacter;///<降落伞Actor
};

