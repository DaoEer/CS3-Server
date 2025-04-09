// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Character.h"
//插件
#include "Entity.h"
//CS3数据
#include "GameData/GameDeFine.h"
//CS3
#include "BaseState.h"
#include "GameData/CS3Object.h"
#include "RoleStateMachine.generated.h"


/*
* 文件名称：RoleStateMachine.h
* 功能说明：人物状态机
* 文件作者：ranxuanwen
* 目前维护：ranyuan
* 创建时间：2016-11-01
*/
class EffectStateBase;
class JumpBaseState;
class ClimbLadderBaseState;

UCLASS(BlueprintType)
class CHUANGSHI_API URoleStateMachine : public UCS3Object
{
	GENERATED_BODY()
public:
	/**
	*初始化状态容器
	*
	*@param RoleEntity ，角色 Entity（Entity*）
	*
	*@return 无
	*/
	void InitStateMap(KBEngine::Entity* RoleEntity);

	/**
	*初始化效果状态容器
	*
	*
	*@return 无
	*/
	void InitEffectStateMap();


	/**
	*初始化跳跃状态容器
	*
	*
	*@return 无
	*/
	void InitJumpStateMap();

	/**
	*初始化攀爬梯子状态容器
	*
	*
	*@return 无
	*/
	void InitClimbLadderStateMap();

	/**
	*更新状态
	*
	*@param NewState ，新状态（ENTITY_STATE）
	*
	*@return 无
	*/
	void UpdateState(ENTITY_STATE NewState);

	/**
	*添加效果状态
	*
	*@param NewState ，新效果状态（EFFECT_STATE）
	*
	*@return 无
	*/
	void OnAddEffectState(EFFECT_STATE EffectState_);

	/**
	*失去效果状态
	*
	*@param NewState ，新效果状态（EFFECT_STATE）
	*
	*@return 无
	*/
	void OnDelEffectState(EFFECT_STATE EffectState_);

	/**
	*更新跳跃表现状态
	*
	*@param JumpShowState ，新状态（JUMP_SHOW_STATE）
	*
	*@return 无
	*/
	void UpdateJumpState(JUMP_SHOW_STATE JumpShowState);

	/**
	*更新跳跃表现状态
	*
	*@param JumpShowState ，新状态（JUMP_SHOW_STATE）
	*
	*@return 无
	*/
	void UpdateClimbLadderState(CLIMB_LADDER_STATE ClimbLadderState);

private:
	/**
	*状态转变
	*
	*@param State ，状态（ENTITY_STATE）
	*
	*@return UBaseState*
	*/
	UBaseState* StateTransition(ENTITY_STATE State);

	/**
	*动作的回调
	*
	*@param RoleChar ，角色（ACharacter *）
	*@param id ，名字（FName）
	*
	*@return 无
	*/
	void OnActionCallBack(ACharacter *RoleChar, FName id);
private:
	UBaseState* CurrentState = nullptr;///<当前状态
	UBaseState* RoleState;//角色状态
	KBEngine::Entity* CurrentEntity;///<当前Entity
	UPROPERTY()
	TMap<ENTITY_STATE, UBaseState*> RoleStateMap;///<角色状态字典

	static TMap<EFFECT_STATE, TSharedPtr<EffectStateBase>> EffectStateMap;///效果状态字典

	JumpBaseState* CurrentJumpUpState = nullptr;
	TMap<JUMP_SHOW_STATE, TSharedPtr<JumpBaseState>> RoleJumpStateMap;///<角色跳跃状态字典

	ClimbLadderBaseState* CurrentClimbLadderState = nullptr;
	TMap<CLIMB_LADDER_STATE, TSharedPtr<ClimbLadderBaseState>> ClimbLadderStateMap;///<角色攀爬梯子状态字典
};
