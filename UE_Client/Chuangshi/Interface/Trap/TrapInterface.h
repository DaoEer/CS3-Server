// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Interface/NPCBaseObjectInterface.h"
#include "TrapInterface.generated.h"

/*
* 文件名称：TrapInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UTrapInterface : public UNPCBaseObjectInterface
{
	GENERATED_BODY()
	typedef UNPCBaseObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:

	UTrapInterface();
	~UTrapInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.TrapInterface'"); } //获取蓝图对象路径


	/**
	*设置模型编号
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "cs3|Trap")
	virtual void OnRep_modelNumber()override;

	/**
	*设置模型缩放
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "cs3|Trap")
	virtual void OnRep_modelScale()override;

	/**
	*设置触发器半径
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "cs3|Trap")
	void OnRep_triggerRadius();

	/**
	*设置触发器形状
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|Trap")
	void OnRep_triggerShape();


	void OnEnterTrap(int32 entityID);	 ///< 进入陷阱
	void OnLeaveTrap(int32 entityID);    ///< 离开陷阱

	 /**
	* Define method
	* BlueprintCallable,怪物播放暴尸效果
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "TrapInterface")
		void CLIENT_PlayDeadEffect(const FString& EffectID);

	UFUNCTION(BlueprintNativeEvent, Category = "TrapInterface")
		void PlayDeadEffect(const FString& EffectID);
	
	virtual void InitBlueCB() override;
};