// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
//插件
#include "KBEngine.h"
//CS3数据
#include "GameData/StateData.h"
#include "GameData/GameDeFine.h"
//CS3
#include "GameData/CS3Object.h"
#include "BaseState.generated.h"

/*
* 文件名称：BaseState.h
* 功能说明：人物状态基类
* 文件作者：ranxuanwen
* 目前维护：wuxiaoou
* 创建时间：2016-11-01
*/

class URoleStateMachine;

UCLASS(BlueprintType)
class CHUANGSHI_API UBaseState : public UCS3Object
{
	GENERATED_BODY()
public:
	virtual void Enter();///< 刚进入时调用
	virtual void Execute();///< 执行时调用
	virtual void Exit();///< 离开时调用
	ENTITY_STATE GetRoleState();///< 获取角色状态

	/**
	*创建状态
	*
	*@param TableData ，表格数据（FSTATE_DATA*）
	*@param StateMachine ，角色状态机（URoleStateMachine*）
	*@param RoleEntity，（Entity*）
	*
	*@return 无
	*/
	void CreateState(const FSTATE_DATA* TableData, URoleStateMachine* StateMachine, KBEngine::Entity* RoleEntity);
protected:
	URoleStateMachine* CurrentStateMachine;///< 当前状态机
	const FSTATE_DATA* StateTableData;///<状态表格数据
	KBEngine::Entity* CurrentEntity;///<当前Entity
};
