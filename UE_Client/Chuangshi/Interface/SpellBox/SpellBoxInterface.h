// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Util/CS3Debug.h"
#include "Interface/NPCBaseObjectInterface.h"
#include "SpellBoxInterface.generated.h"

/*
* 文件名称：SpellBoxInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

/**
*NPC接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API USpellBoxInterface : public UNPCBaseObjectInterface
{
	GENERATED_BODY()
	typedef UNPCBaseObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	USpellBoxInterface();
	~USpellBoxInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.SpellBoxInterface'"); } //获取蓝图对象路径
	/**
	*设置最小交互距离
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|SpellBox")
	void OnRep_minGossipDis();

	/**
	*设置最大交互距离
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|SpellBox")
	void OnRep_maxGossipDis();

	/**
	*设置需要监听的事件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|SpellBox")
	void OnRep_listenEvents();

	/**
	*是否监听了某事件
	*
	*@return 无
	*/
	bool HasListenEvent(int32 eventType);

	/**
	*Define method
	*更新箱子状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpellBox")
	void CLIENT_RefreshBoxStatus();

	/**
	*Define method
	*BlueprintCallable，设置箱子状态值
	*
	*param boxStatus， 箱子状态（int32）
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpellBox")
	void CLIENT_SetBoxStatus(int32 boxStatus, const FString& spellBoxEffectID,float effectModelScale, const FString& slotName);

	/**
	*Define method
	*交互中断
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpellBox")
		void CLIENT_SpellBoxInterrupted();

	/**
	*播放动作
	*
	*@param ActionId ，动作ID（FString）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		virtual void OnDelayStopAction(float delayStop)override;

	/**
	*BlueprintCallable，	通知SpeelBox
	*@Param1 Albedo		    颜色Vector
	*@Param2 StarHoldRadius 开始时过渡的半径大小
	*@Param3 EndHoldRadius	结束时过渡的半径大小
	*@Param4 Extinction		雾气的浓度大小
	*@Param5 time			过度时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpellBox")
		void CLIENT_OnHoldRadiusFog(const FString& Albedo, const float& StarHoldRadius, const float& EndHoldRadius,const float& Extinction, const float& time);

	virtual void InitBlueCB() override;
public:
	UPROPERTY(EditAnywhere)
		int32 BoxStatus; ///<箱子状态：0不可见，1不可交互，2可交互

protected:
	//当前粒子的UID
	int32 CurEffectUID;

private:
	FTimerHandle HoldRadiusHandle;///<朝向句柄
	float HoldRadiusTime;

};