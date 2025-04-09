// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/StateInterface.h"
#include "GameData/GameDeFine.h"
#include "RoleStateInterface.generated.h"

/*
* 文件名称：RoleStateInterface.h
* 功能说明：角色状态接口类
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2016-11-09
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URoleStateInterface : public UStateInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleStateInterface();
	~URoleStateInterface() {};

	static FString GetName() { return TEXT("StateInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleStateInterface.BP_RoleStateInterface_C'"); } //获取蓝图对象路径


	/**
	* 角色状态改变
	*
	*@param NewState 新的状态值
	*@param OldState 旧的状态值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStateInterface")
		void OnStateChangedBP(const int32& NewState, const int32& OldState);

	//UFUNCTION(BlueprintCallable, Category = "RoleStateInterface")
	void OnRep_state();///<BlueprintCallable,更新当前状态


	//====================================跳跃相关====================

	/**
	* 服务器通知跳跃状态改变
	*
	*@param JumpState 参考枚举JUMP_SHOW_STATE
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStateInterface")
		void OnRepJumpState(int32 JumpState);
	void UpdateJumpState(JUMP_SHOW_STATE JumpState);
	
	/**
	* 客户端请求通知跳跃状态改变
	*
	*@param JumpState 参考枚举JUMP_SHOW_STATE
	*
	*@return 无
	*/
	void RequestChangeJumpState(JUMP_SHOW_STATE JumpState);
	//====================================跳跃相关====================


	//====================================攀爬梯子相关====================
	
	/**
	* 服务器通知攀爬梯子状态改变
	*
	*@param JumpState 参考枚举JUMP_SHOW_STATE
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStateInterface")
		void OnRep_climbLadderState();

	/**
	* 客户端请求通知跳跃状态改变
	*
	*@param ClimbLadderState 参考枚举CLIMB_LADDER_STATE
	*
	*@return 无
	*/
	void RequestChangeClimbLadderState(CLIMB_LADDER_STATE ClimbLadderState);

	/**
	* 服务器通知更新攀爬动作时间轴的值
	*
	*@param JumpState 参考枚举JUMP_SHOW_STATE
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStateInterface")
		void OnRep_ladderPosOffset();

	/**
	* 客户端请求通知更新攀爬动作时间轴的值
	*
	*@param LadderPosOffset 动作轴值
	*
	*@return 无
	*/
	void RequestUpdateClimbLadderActionStepPos(float LadderPosOffset);

	//====================================攀爬梯子相关====================

	virtual void InitBlueCB() override;

protected:
	/**
	*virtual,角色状态改变
	*
	*@param NewState 新的状态值
	*@param OldState 旧的状态值
	*
	*@return 无
	*/
	virtual void OnStateChanged(const int32& NewState, const int32& OldState)override;

};
