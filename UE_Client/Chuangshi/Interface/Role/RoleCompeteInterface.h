// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"


#include "RoleCompeteInterface.generated.h"

/*
* 文件名称：RoleCompeteInterface.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2017-09-3
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URoleCompeteInterface :public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleCompeteInterface();
	~URoleCompeteInterface();
	static FString GetName() { return TEXT("RoleCompeteInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleCompeteInterface.BP_RoleCompeteInterface_C'"); } //获取蓝图对象路径


public:

	virtual void InitBlueCB() override;
	/**
	*Define method
	*收到切磋邀请
	*
	*@param inviterID ，邀请者ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleCompeteInterface")
		void CLIENT_RoleCompeteBeInvited(const int32& inviterID);

	/**
	*Define method
	*开始切磋
	*
	*@param 无
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleCompeteInterface")
		void CLIENT_RoleCompeteStart(const int32& targetID);

	/**
	*Define method
	*结束切磋
	*
	*@param 无
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleCompeteInterface")
		void CLIENT_OnRoleCompeteEnd();

	/**
	*Define method
	*显示切磋倒计时界面
	*
	*@param tpye 1：开始前倒计时，2：结束前倒计时，3：脱离范围倒计时
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleCompeteInterface")
		void CLIENT_ShowCompeteCountDown(const int32& type, const int32& time);

	/**
	*Define method
	*关闭切磋倒计时界面
	*
	*@param 无
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleCompeteInterface")
		void CLIENT_CloseCompeteCountDown();
	/**
	*Define method
	*连击回调
	*
	*@param 无
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleCompeteInterface")
		void CLIENT_OnDoubleHit(const int32& DoubleHitTimes);

	UPROPERTY(BlueprintReadWrite)
		int32 CompeteTargetID = 0;

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_requestRoleCompete(const int32& INT32_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_requestAgreeRoleCompete(const int32& INT32_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_requestRefuseRoleCompete(const int32& INT32_1);


};


