// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Interface/NPCBaseObjectInterface.h"
#include "VehiclePetInterface.generated.h"

/*
* 文件名称：VehiclePetInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/


UCLASS(BlueprintType)
class CHUANGSHI_API UVehiclePetInterface : public UNPCBaseObjectInterface
{
	GENERATED_BODY()
	typedef UNPCBaseObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	virtual void onLeaveWorld() override;
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.VehiclePetInterface'"); } //获取蓝图对象路径


	/**
	*设置模型编号
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "cs3|VehiclePet")
	virtual void OnRep_modelNumber()override;

	/**
	*设置模型缩放
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "cs3|VehiclePet")
	virtual void OnRep_modelScale()override;

	UFUNCTION(BlueprintCallable, Category = "cs3|VehiclePet")
		void OnRep_baseOwnerID();

	void RPC_onSetPetControlledBy();


};