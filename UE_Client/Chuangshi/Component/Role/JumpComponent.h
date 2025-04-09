// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
//UE4
#include "Engine/EngineTypes.h"
//CS3数据
#include "GameData/RoleJumpData.h"
#include "Engine/DataTable.h"
#include "GameData/GameDeFine.h"
//CS3
#include "Components/ActorComponent.h"
#include "JumpComponent.generated.h"

class ACharacter;
class UCharacterMovementComponent;

DECLARE_STATS_GROUP(TEXT("UJumpComponent"), STATGROUP_UJumpComponent, STATCAT_Advanced);

/*
* 文件名称：JumpComponent.h
* 功能说明：负责主角的跳跃功能
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2017-10-09
*/
UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class CHUANGSHI_API UJumpComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	UJumpComponent();

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;
	void InitJumpData();

	///开始主动跳跃表现执行
	void OnStartActiveJump();
	///开始被动跳跃表现执行
	void OnStartPassiveJump(float Height);
	///设置跳跃的最大次数
	void SetJumpMaxCountBySkill();
	///清理跳跃的次数
	void ResetJumpCount();
	///跳跃模型发生改变时
	void MovementModeChanged(EMovementMode PrevMovementMode, uint8 PreviousCustomMode /*= 0*/);
	///更新跳跃状态
	void UpdateJumpState(JUMP_SHOW_STATE InJumpShowState);
	
	/**
	*开始执行边缘辅助起跳
	*@param bUpJump  是否向上跳（true向上，false向下）
	*@param JumpHeight	起跳高度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "JumpComponent")
		void OnStartLedgesJump(bool bUpJump, float JumpHeight);

	void ChangeJumpStateToServer(JUMP_SHOW_STATE JumpState);///设置跳跃状态并通知服务器

	void SetJumpShowType(JUMP_SHOW_TYPE InJumpShowType);///设置跳跃表现类型
	void SetJumpHeight(float JumpHeight);///设置可跳跃高度

	bool IsCanJump();///玩家能否跳跃
	void SetSynchroPlayerJumpState(JUMP_SHOW_STATE InJumpShowState);///设置同步时其他角色的跳跃状态(非本地控制的主角)
	JUMP_SHOW_STATE GetCurJumpShowState();///获取当前跳跃表现状态

protected:
	virtual void BeginPlay() override;

private:
	void CheckJumpFalling();///是否在跳跃后的下落中

	ACharacter* GetOwnerCharacter();

public:
	UPROPERTY(BlueprintReadOnly, Category = CameraRock)
		bool IsJumpState = false;//是否跳跃过程中(包括IsTheFalling、IsTheUping)

	UPROPERTY(BlueprintReadOnly, Category = CameraRock)
		bool IsTheLand = true;//是否在陆地

	UPROPERTY(BlueprintReadOnly, Category = CameraRock)
		bool IsTheFalling = false;//真正的下落

	UPROPERTY(BlueprintReadOnly, Category = CameraRock)
		bool IsTheUping = false;//上升过程中

	int32 PlayerJumpMaxCount;///将引擎的JumpMaxCount设置无限大，使用PlayerJumpMaxCount代替判断

protected:

private:
	FVector OldLoctionForJumpHorizontal;///记录玩家位置-跳跃水平移动时
	JUMP_SHOW_STATE CurJumpShowState;

	float LedgesJumpHeight = 0.0f;///边缘辅助跳跃高度
		
};
