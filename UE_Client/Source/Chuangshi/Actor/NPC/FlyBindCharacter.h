// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/NPC/ClientGameCharacter.h"
#include "GameData/FlyBindMeshData.h"
#include "FlyBindCharacter.generated.h"


/**
 * 
 */
UCLASS(BlueprintType)
class CHUANGSHI_API AFlyBindCharacter : public AClientGameCharacter
{
	GENERATED_BODY()
public:
	AFlyBindCharacter();
	void initFlyBindActor(const FFLY_BIND_MESH_DATA* Config,int32 PlayerId);

	UFUNCTION(BlueprintImplementableEvent, Category = "Effect")
		void OnInitFromConfig();

	UFUNCTION(BlueprintImplementableEvent, Category = "Effect")
		void UseSkill(int32 CasterID = 0, int32 TargetID = 0);

	///路径资源
	UPROPERTY(BlueprintReadOnly)
		TSubclassOf<ABaseSplineAsset> SplineAsset;
	///循环次数
	UPROPERTY(BlueprintReadOnly)
		int32 LoopNumber;

	///移动速度
	UPROPERTY(BlueprintReadWrite)
		float FlySpeed;

	///是否开始世界位置
	UPROPERTY(BlueprintReadOnly)
		bool bIsAbsoluteLocation;

	///是否开始世界旋转
	UPROPERTY(BlueprintReadOnly)
		bool bIsAbsoluteRotation;

	///是否开始世界大小
	UPROPERTY(BlueprintReadOnly)
		bool bIsAbsoluteScale;

	UPROPERTY(BlueprintReadOnly)
		TArray<FString> AnimID;

	///技能特效id列表
	UPROPERTY(BlueprintReadOnly)
		TArray<FString> EffectID;

	///法宝动画延迟时间，根据动画流程顺序配置。
	UPROPERTY(BlueprintReadOnly)
		TArray<float> PlayTime;

	///技能类型
	UPROPERTY(BlueprintReadOnly)
		FLYBINDSKILL_STATE SkillType;
	///插槽
	UPROPERTY(BlueprintReadOnly)
		FName FlyModeBindSocket;
	///玩家ID
	UPROPERTY(BlueprintReadOnly)
		int32 PlayerID;

	///绑定的位置和朝向
	UPROPERTY(BlueprintReadOnly)
		FTransform FlyTransform;
	///绑定的位置和朝向
	UPROPERTY(BlueprintReadOnly)
		FTransform FlySplineTransform;
	
};
