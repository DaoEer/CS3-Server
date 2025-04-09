// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "GameData/CharacterData.h"
#include "CS3Base/CS3EntityInterface.h"
#include "MonsterAppearInterface.generated.h"

/*
* 文件名称：MonsterAppearInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：all
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterAppearInterface : public UCS3EntityInterface
{
	GENERATED_BODY()    
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
	
public:
	static FString GetName() { return TEXT("MonsterAppearInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterAppearInterface'"); } //获取蓝图对象路径

	/**
	*BlueprintNativeEvent 带位移的出场
	*
	*@param Actions 动作列表（const TArray<FName>&）
	*@param Gravity 重力加速度（const float&）
	*@param UpTime 上升时间（const float&）
	*@param XSpeed 水平速度（const float&）
	*@param TargetPos 目标位置（const FVector&）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void CLIENT_MonsterAppearJump(const TArray<FName>& Actions, const FString& EffectID, 
			const float& Gravity, const float& UpTime, const float& XSpeed, const FVector& TargetPos);

	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void MonsterAppearJump(const TArray<FName>& Actions, const FString& EffectID,
			const float& Gravity, const float& UpTime, const float& XSpeed, const FVector& TargetPos);

	/**
	*BlueprintNativeEvent 不带位移的出场
	*
	*@param Actions 动作列表（const TArray<FName>&）
	*@param LoopTime 第二段跳时间（const float）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void CLIENT_MonsterAppearJumpWithoutMove(const TArray<FName>& Actions, 
			const FString& EffectID, float LoopTime );

	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void MonsterAppearJumpWithoutMove(const TArray<FName>& Actions,
			const FString& EffectID, float LoopTime);

	/**
	*BlueprintNativeEvent 平移到目标点
	*
	*@param DX 目标位置X
	*@param DY 目标位置Y
	*@param DZ 目标位置Z
	*@param Yaw 朝向
	*@param MoveSpeed 移动速度
	*@param ActionID 动作ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void CLIENT_MonsterAppearLineToPoint(float DX, float DY, 
			float DZ, float Yaw, float MoveSpeed, const FString& ActionID);
	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void MonsterAppearLineToPointOver();

	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void MonsterAppearLineToPoint(float DX, float DY,
			float DZ, float Yaw, float MoveSpeed, const FString& ActionID);

	/**
	*BlueprintNativeEvent 怪物模拟跳跃(点对点跳跃)
	*
	*@param InStartPosition 起始位置
	*@param InEndPosition 目标位置
	*@param XMoveSpeed 水平移动速度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void CLIENT_MonsterJumpPointToPoint(const FVector& InStartPosition, const FVector& InEndPosition, float XMoveSpeed);
	/**
	*BlueprintNativeEvent 抛物线移动到目标点
	*
	*@param Actions 动作数组
	*@param RisingDistance 最高点
	*@param InStartPosition 起始位置
	*@param MoveSpeed 速度
	*@param InEndPosition 目标位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void CLIENT_MonsterAppearCurveMove(const TArray<FName>& Actions, 
			float RisingDistance, const FVector& InStartPosition, 
			float MoveSpeed, const FVector& InEndPosition);

	UFUNCTION(BlueprintNativeEvent, Category = "Server | Common")
		void MonsterAppearCurveMove(const TArray<FName>& Actions,
			float RisingDistance, const FVector& InStartPosition,
			float MoveSpeed, const FVector& InEndPosition);
	void RPC_CELL_onMonsterAppearJumpWithoutMoveEnd(ACharacter* Character, FACTION_DATA InActionData);
	void RPC_CELL_onMonsterJumpPointToPointEnd();
	void RPC_CELL_onMonsterAppearLineToPoint();
	virtual void InitBlueCB() override;
private:
	void StopMonsterJumpPointToPoint(FVector Position);

private:
	FTimerHandle CurveMoveHandle;
	FTimerHandle JumpCurveMoveHandle;
	float RisingPercent = 0.0f;
	float JumpPercent = 0.0f;
	float JumpDeltaTime = 0.0f;

	FDelegateHandle MonsterAppearJumpHandle;
	FDelegateHandle MonsterAppearJumpWithoutMoveHandle;
};
