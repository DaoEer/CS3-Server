// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtBatteryInterface.generated.h"

/*
* 文件名称：MonsterExtBatteryInterface.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2019-12-25
*/

UENUM(BlueprintType)
enum class BATTERY_AMMO_TYPE :uint8
{
	// 0：普通炮弹（打中才有效果）
	AMMO_TYPE_COMMON,
	// 1: 铁砂炮（一开炮，就有效果）
	AMMO_TYPE_IRON,
};

UCLASS()
class CHUANGSHI_API UMonsterExtBatteryInterface : public UMonsterInterface
{
	GENERATED_BODY()

public:
	UMonsterExtBatteryInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_MonsterExtBatteryInterface.BP_MonsterExtBatteryInterface_C'"); } //获取蓝图对象路径

	// 初始化 火炮、铁砂炮
	UFUNCTION(BlueprintCallable)
		void Initiative();
	// 初始化 火箭炮
	UFUNCTION(BlueprintCallable)
		void InitiativeRocket();
	UFUNCTION(BlueprintCallable)
		void AddTrap();
	void OnPlayerBeginOverlap();
	void OnPlayerEndOverlap();

	/// 操作者ID
	UFUNCTION(BlueprintCallable)
		void OnRep_operatorID();
	// 操作炮台
	UFUNCTION(BlueprintCallable)
		void OperationBattery(const int32& EntityID_);
	/**
	*BlueprintNativeEvent 客户端本地玩家操作火炮回调(把接口放在一起，方便管理)
	*
	*@param Ammo_ 弹药数量
	*@param EndTime_ 炮弹装载完毕时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_OnSelfOpertionBattery(const int32& Ammo_, const FString& EndTime_);
	// entity操作火炮通知(包括自己)
	UFUNCTION(BlueprintNativeEvent)
		void OnObjectOpertionBattery(const int32& EntityID_);

	// 取消操作
	UFUNCTION(BlueprintCallable)
		void CancelOperationBattery();
	UFUNCTION(BlueprintNativeEvent)
		void OnCancelOperationBattery(const int32& EntityID_);

	// 炮台开火
	UFUNCTION(BlueprintCallable)
		void ProjectBattery(const float& Yaw, const float& Pitch);
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_OnProjectBattery(const float& Yaw, const float& Pitch);
	UFUNCTION(BlueprintCallable)
		void DelayFire();

	// CD时间好了
	UFUNCTION(BlueprintPure)
		bool CDIsReady();

	// 火箭车开火
	UFUNCTION(BlueprintCallable)
		void ProjectRocketBattery(const float& Yaw);
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_OnProjectRocketBattery(const int32& Index, const float& Yaw);
	UFUNCTION(BlueprintNativeEvent)
		void FinishProjectRocketBattery();

	virtual void InitBlueCB() override;

public:
	UPROPERTY(BlueprintReadOnly)
		int32 OpertorID;
	// 弹药光效
	UPROPERTY(BlueprintReadOnly)
		FString BatteryEffect;
	// 弹药类型
	UPROPERTY(BlueprintReadOnly)
		BATTERY_AMMO_TYPE AmmoType;
	// 弹药数量
	UPROPERTY(BlueprintReadOnly)
		int32 Ammo;
	// 装弹时间（CD）
	UPROPERTY(BlueprintReadOnly)
		float LoadCD;
	// 装弹结束时间（CD）
	UPROPERTY(BlueprintReadOnly)
		FDateTime CDTimer;
	// 相机灵敏度
	UPROPERTY(BlueprintReadOnly)
		float InputYawScale;
	// 摄像机位置
	UPROPERTY(BlueprintReadOnly)
		FVector CamerLocation;
	// 摄像机朝向
	UPROPERTY(BlueprintReadOnly)
		FRotator CamerRotation;
	// 火炮转向角度
	UPROPERTY(BlueprintReadOnly)
		int32 TurnAngle;
	UPROPERTY(BlueprintReadOnly)
		FString EndTime;
	// 飞行速度
	UPROPERTY(BlueprintReadOnly)
		float FlySpeed;
	UPROPERTY(BlueprintReadOnly)
		float GravityScale;
	UPROPERTY(BlueprintReadOnly)
		int32 SkillID;

	// 火箭车连续发射 间隔时间
	UPROPERTY(BlueprintReadOnly)
		float GuidInterval;
	// 火箭车连续发射 间隔次数
	UPROPERTY(BlueprintReadOnly)
		int32 GuidTimer;
	// 火箭车连续发射相对位置
	UPROPERTY(BlueprintReadOnly)
		TArray<FVector> FirePos;
	
};
