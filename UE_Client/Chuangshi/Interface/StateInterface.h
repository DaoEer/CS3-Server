// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CS3Base/CS3EntityInterface.h"

#include "GameData/GameDeFine.h"
#include "GameData/EffectEmitterData.h"

#include "StateInterface.generated.h"
/*
 * 文件名称：StateInterface.h  
 * 功能说明： 
 * 文件作者：wangzheng
 * 目前维护：ranyuan
 * 创建时间：2016/10/29
 */ 

class URoleStateMachine;

UCLASS(BlueprintType)
class CHUANGSHI_API UStateInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	static FString GetName() { return TEXT("StateInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_StateInterface.BP_StateInterface_C'"); } //获取蓝图对象路径


	virtual void onEnterWorld() override;///< 当Entity进入世界时，此方法被调用

	void InitStateMachine();///<初始化状态机

	/**
	*virtual,状态改变
	*
	*@param NewState 新的状态值
	*@param OldState 旧的状态值
	*
	*@return 无
	*/
	virtual void OnStateChanged(const int32& NewState, const int32& OldState);

	UFUNCTION(BlueprintCallable, Category = "StateInterface")
	void OnRep_state();///<BlueprintCallable,更新当前状态

	/**
	*virtual,效果状态改变
	*
	*@param NewState 新的效果状态值
	*@param OldState 旧的效果状态值
	*
	*@return 无
	*/
	virtual void OnEffectStateChanged(const int32& NewEffectState, const int32& OldEffectState);

	// 更新优先级 效果状态
	void UpdatePriorityEffectState(const int32& NewEffectState, const int32& OldEffectState);
	// 更新无优先级 效果状态
	void UpdateUnPriorityEffectState(const int32& NewEffectState, const int32& OldEffectState);

	UFUNCTION(BlueprintNativeEvent, Category = "StateInterface")
	void OnRep_effectState();///<BlueprintCallable,更新当前效果状态

	/**
	*BlueprintCallable,是否拥有某行为标记
	*
	*@param actionFlag 行为标记,见 GameDefine.ACTION_FLAG
	*
	*@return bool 拥有某行为标记返回TRUE，否则返回FALSE。
	*/
	UFUNCTION(BlueprintCallable, Category = "StateInterface")
	bool IsActionForbid(const ACTION_FLAG& actionFlag);

	/**
	*BlueprintCallable,是否拥有某效果状态
	*
	*@param EffectState 效果状态
	*
	*@return bool 拥有某效果状态返回TRUE，否则返回FALSE。
	*/
	UFUNCTION(BlueprintPure, Category = "StateInterface")
	bool HasEffectState(const EFFECT_STATE EffectState);

	/**
	*BlueprintCallable,是否拥有禁止玩家朝向改变（移动时候的朝向不影响）的效果状态
	*
	*@return bool 拥有禁止玩家朝向改变（移动时候的朝向不影响）开关的效果状态返回TRUE，否则返回FALSE。
	*/
	UFUNCTION(BlueprintCallable, Category = "StateInterface")
	bool IsHasEffectStates();

	void GetCurEffectState(EFFECT_STATE& EffectState);

	virtual void InitBlueCB() override;
private:
	void GetEffectStateSortList(TArray<EFFECT_STATE> &StateDatas);

	void UpdataEffectByEffectState();

public:
	int32 CurrentState = -1;///<当前状态
	int32 CurrentEffectState = 0;///<当前效果状态

protected:
	UPROPERTY()
		URoleStateMachine* RoleStateMachine;///<玩家状态机

private:
	TArray<int32> EffectStates;
	UPROPERTY()
	TMap<EFFECT_STATE, FStateParticles> CurEffectMap;
};
