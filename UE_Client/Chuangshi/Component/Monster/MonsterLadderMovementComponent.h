// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "GameData/CharacterData.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "MonsterLadderMovementComponent.generated.h"


/*
* 文件名称：MonsterLadderMovementComponent.h
* 功能说明：负责怪物的攀爬梯子功能
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2020-03-20
*/
class AMonsterCharacter;
UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class CHUANGSHI_API UMonsterLadderMovementComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UMonsterLadderMovementComponent();

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;
	void InitData(AMonsterCharacter *LadderCharacter);

	void StartClimbLadder(FVector LadderStartLocation, FVector LadderEndLocation, FRotator LadderRotation);//怪物开始爬梯子
	void StartFallToLadder();//怪物开始从梯子掉落
	void LadderResetPitch();//恢复怪物pitch角度

protected:
	virtual void BeginPlay() override;

private:
	void ExitTop();//怪物<从顶部>离开梯子
	void ExitFallLand();//怪物<从空中掉落着陆>离开梯子
	void ClimbUpToLader(float DeltaSeconds);//怪物向上攀爬tick模拟表现
	void FallDownToLader(float DeltaSeconds);//怪物向下掉落tick模拟表现
	void ActionExitTopOver(ACharacter * Character, FACTION_DATA Action);

public:
	UPROPERTY(BlueprintReadOnly, Category = "LadderCustomMovementComponent")
		AMonsterCharacter* CurMonsterCharacter;///当前怪物

	UPROPERTY(BlueprintReadOnly, Category = "LadderCustomMovementComponent")
		UCharacterMovementComponent* CurCharacterMovement;///当前怪物移动组件 

	UPROPERTY(BlueprintReadOnly, Category = "LadderCustomMovementComponent")
		AMonsterCharacter* CurLadderCharacter;///当前梯子

private:
	bool IsAIEnterLadder = false;//怪物是否进入云梯
	FVector AIMonsterStartLoaction;//怪物的初始位置
	FVector AIMonsterEndLoaction;//怪物的结束位置
	FRotator AIMonsterRotation;

	bool IsLadderDownFalling = false;//是否怪物正在从梯子上掉落
	FVector AIMonsterFallDownEndLoaction;//怪物的掉落的结束位置（地板）
	float AddSpeed = 0.0f;//怪物下落的加速度
		
};
