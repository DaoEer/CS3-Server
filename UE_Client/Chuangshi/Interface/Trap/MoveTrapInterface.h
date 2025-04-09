// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "TrapInterface.h"
#include "MoveTrapInterface.generated.h"

/*
* 文件名称：MoveTrapInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMoveTrapInterface : public UTrapInterface
{
	GENERATED_BODY()
	typedef UTrapInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:

	UMoveTrapInterface();
	~UMoveTrapInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MoveTrapInterface'"); } //获取蓝图对象路径
	/**
	*Define method
	*BlueprintNativeEvent，进度条改变
	*@param value 进度条值
	*
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MoveTrap")
		void CLIENT_ChangeProgressBar( float value );

	virtual void InitBlueCB() override;

};