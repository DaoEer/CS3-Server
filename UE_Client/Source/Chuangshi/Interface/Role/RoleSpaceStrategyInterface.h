// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/SpaceStrategyPointData.h"
#include "RoleSpaceStrategyInterface.generated.h"

/*
* 文件名称：RoleSpaceStrategyInterface.h
* 功能说明：玩家策略点
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-04-19
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URoleSpaceStrategyInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleSpaceStrategyInterface();
	~URoleSpaceStrategyInterface();
	static FString GetName() { return TEXT("RoleSpaceStrategyInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleSpaceStrategyInterface.BP_RoleSpaceStrategyInterface_C'"); } //获取蓝图对象路径

	/**
	* Define method
	* 开始某个策略点
	*
	* @param index 策略点index
	* @param data 策略点数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceStrategyInterface")
		void CLIENT_StartSpaceStrategy(const int32& index, const FString& data);

	/**
	* Define method
	* 更新某个策略点
	*
	* @param index 策略点index
	* @param isSuccess 是否成功
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceStrategyInterface")
		void CLIENT_EndSpaceStrategy(const int32& index, const int32& isSuccess);

	/**
	* Define method
	* 用于重登 接收已完成的策略点
	*
	* @param index 策略点index
	* @param data 策略点数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceStrategyInterface")
		void CLIENT_ReceiveCompleteSpaceStrategy(const int32& index, const FString& data);

	/**
	* Define method
	* 用于重登 接收开始的策略点
	*
	* @param index 策略点index
	* @param data 策略点数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceStrategyInterface")
		void CLIENT_ReceiveOpenSpaceStrategy(const int32& index, const FString& data);

	/**
	* 获得策略点数据
	*
	* @param data 策略点数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleSpaceStrategyInterface")
		FSPACESTRATEGYPOINTDATA GetStrategyPointByJsonData(const FString& data);

	/**
	* 获得策略点
	*
	* @param index 策略点index
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleSpaceStrategyInterface")
		FSPACESTRATEGYPOINTDATA GetStrategyPointByIndex(const int32& index);

	/**
	* Define method
	* 更新某个策略点值
	*
	* @param index 策略点index
	* @param key ("*":策略点值，"?":策略点上限值，"(1)":条件1值，"(2)":条件2值)
	* @param value 当前值
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceStrategyInterface")
		void CLIENT_OnUpdateStrategyValue(const int32& index, const FString& key, const int32& value);

	/**
	* Define method
	* 更新某个策略点值
	*
	* @param index 策略点index
	* @param key ("1":奖励经验值，"2":奖励的潜能值，"3":奖励的帮贡值)
	* @param value 当前值
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceStrategyInterface")
		void CLIENT_OnUpdateRewardValue(const int32& index, const int32& key, const int32& value);

	virtual void onLeaveWorld() override;

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<FSPACESTRATEGYPOINTDATA> StrategyPointList; ///策略点列表

	virtual void InitBlueCB() override;
};
