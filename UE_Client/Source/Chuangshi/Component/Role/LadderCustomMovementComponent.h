// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameData/CharacterData.h"
#include "GameData/GameDeFine.h"
#include "LadderCustomMovementComponent.generated.h"

/*
* 文件名称：LadderCustomMovementComponent.h
* 功能说明：负责主角的攀爬梯子功能
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2020-02-22
*/
class APlayerCharacter;
class AMonsterCharacter;
UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class CHUANGSHI_API ULadderCustomMovementComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	// Sets default values for this component's properties
	ULadderCustomMovementComponent();

protected:
	// Called when the game starts
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	void InitLadderData();
	void ClearLadderData();//退出副本时清理爬梯数据

	void BeginOverlappedCustomMoveZone(AMonsterCharacter *LadderCharacter);//进入梯子区域
	void EndOverlappedCustomMoveZone(AMonsterCharacter *LadderCharacter);//离开梯子区域
	void AddMovementLadderUp(float InputScale);//接收外部WS按键输入

	bool IsLadderMovement();//是否梯子模式(进梯子过程、爬梯子、出梯子过程)
	void StartFallToLadder();//玩家从梯子掉落
	void StartEnterLadderBottom();//F键交互完成，从底部进入梯子
	void LadderFallLand();//从梯子掉落着陆

	void NotifyClimbLadderStateToServer(CLIMB_LADDER_STATE InClimbLadderState, float InLadderStepPos = 0.0f);//将本地玩家攀爬状态通知给服务器
	void SetSynchroPlayerClimbLadderState(CLIMB_LADDER_STATE InClimbLadderState, float InLadderStepPos = 0.0f);//同步其他客户端表现
protected:

private:
	void UpdateCustomMovement(float DeltaTime);//自定义移动的tick更新
	void UpdateLadderMovement(float DeltaTime);
	void UpdateRootMotion(float DeltaTime);
	float GetClimbLadderActionFramePos();//获取梯子攀爬动作的步长位置点
	void ResetCharacterPitch();//恢复玩家的pitch角度

	void CheckEnterLadder(float InputScale);//检测玩家进入梯子
	bool CheckEnterBottom(FVector CharacterFootLocation, FVector CharacterInputDirection, float CharacterInputScale);
	bool CheckEnterTop(FVector CharacterFootLocation, FVector CharacterInputDirection, float CharacterInputScale);
	bool CheckEnterMiddle(FVector CharacterFootLocation, FVector CharacterInputDirection, float CharacterInputScale);
	void EnterBottom();
	void EnterTop();
	void EnterMiddle();
	void ActionEnterBottomBlendOutOver(ACharacter * Character, FACTION_DATA Action);

	void CheckExitLadder(float InputScale);//检测玩家退出梯子
	bool CheckExitBottom(float InputScale, FVector CharacterFootLocation);
	bool CheckExitTop(float InputScale, FVector CharacterFootLocation);
	bool CheckExitMiddle(float InputScale, FVector CharacterFootLocation);
	void ExitBottom();
	void ExitTop();
	void ExitMiddle();
	void ActionExitBottomOver(ACharacter * Character, FACTION_DATA Action);
	void ActionExitTopOver(ACharacter * Character, FACTION_DATA Action);

	APlayerCharacter* GetPlayerCharacter();

public:
	UPROPERTY(BlueprintReadWrite, Category = "LadderCustomMovementComponent")
		float ClimbLadderSpeed = 200;///<攀爬梯子上移动速度(米/秒)

	UPROPERTY(BlueprintReadWrite, Category = "LadderCustomMovementComponent")
		bool IsRootMotionHaveUpAction;///<是否需要攀爬根运动动作过渡

	UPROPERTY(BlueprintReadWrite, Category = "LadderCustomMovementComponent")
		CUSTOM_MOVEMENT_MODE_ENUM TempCustomMovementMode;///<玩家爬梯中自定义移动模式

	UPROPERTY(BlueprintReadWrite, Category = "LadderCustomMovementComponent")
		float ClimbLadderActionFramePos;///<中间攀爬动作步长位置

	CLIMB_LADDER_STATE CurClimbLadderState;///<非本地玩家的攀爬状态（同步用）

protected:

	UPROPERTY(BlueprintReadOnly, Category = "LadderCustomMovementComponent")
		AMonsterCharacter* CurLadderCharacter;///当前梯子

private: 
	bool IsOverLadderZone = false;//是否进入梯子碰撞区域(不代表可以上梯子，还有距离方向的判断)
	bool IsCustomLadderModel = false;//是否梯子模式(进梯子过程、爬梯子、出梯子过程)  [注:非本地玩家(同步时)会有此状态]
	bool IsEnterLaddering = false;//是否进入梯子过程中
	bool IsExitLaddering = false;//是否出梯子过程中

	float LadderStetPosOnStoping = 0.0f;

	FDelegateHandle EnterLadderHandle;
};
