// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "GameFramework/Character.h"
#include "GameData/CharacterData.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "MonsterExtAerialLadderInterface.generated.h"

/*
* 文件名称：MonsterExtAerialLadderInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-02-25
*/
UENUM(BlueprintType)
enum class AERIAL_LADDER_STATE : uint8
{
	AERIAL_LADDER_STATE_FOLLOWER = 0, ///跟随
	AERIAL_LADDER_STATE_BUILD = 1, ///搭建中
	AERIAL_LADDER_STATE_BUILD_SUCCESS = 2, ///搭建成功
};
UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtAerialLadderInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtAerialLadderInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtAerialLadderInterface'"); } //获取蓝图对象路径
	/**
	*BlueprintNativeEvent 接收服务器:云梯移动完毕，准备搭建
	*
	*@param actionID 挂云梯动作ID
	*@param LeaveTopOffset 玩家顶部离开云梯偏移量
	*@param ClimbLadderSpeed 玩家攀爬梯子速度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_AerialLadderMoveFinish(const FString& actionID, float LeaveTopOffset, float ClimbLadderSpeed);

	//接收服务器：从AOI进入执行云梯搭建功能，不播放动作，直接加云梯及设置数据 
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_EnterAerialLadderAOI(float LeaveTopOffset, float ClimbLadderSpeed);

	//通知服务器：云梯搭建完毕
	UFUNCTION(BlueprintCallable)
		void CELL_LadderBuildComplete();

	//接收服务器：云梯准备推倒
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_AerialLadderReadyToFall(const FString& actionID);

	//通知服务器：云梯倒下时上面正在攀爬的entityID
	UFUNCTION(BlueprintCallable)
		void CELL_LadderFallAllEntity(TArray<int32> LadderEntityList);

	//通知服务器：云梯倒下动作播放完毕
	UFUNCTION(BlueprintCallable)
		void CELL_LadderFallActionFinish();

	//通知服务器：有Entity进入梯子(换动作表姿势)
	UFUNCTION(BlueprintCallable)
		void CELL_EntityEnterLadder(int32 EnterEntityId);

	//通知服务器：有Entity退出梯子(恢复动作表姿势)
	UFUNCTION(BlueprintCallable)
		void CELL_EntityExitLadder(int32 EnterEntityId);

	//通知服务器：玩家准备开始爬梯子(蓝图代码中:按F键调用)
	UFUNCTION(BlueprintCallable)
		void CELL_RoleReadyClimbLadder(int32 EnterEntityId);

	virtual void InitBlueCB() override;

private:
	//挂云梯的动作播放完毕
	void CloudLadderActionFinish(ACharacter* Character, FACTION_DATA InActionData);

	//推倒云梯的动作播放完毕
	void FallLadderActionFinish(ACharacter* Character, FACTION_DATA InActionData);
};