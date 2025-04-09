// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Interface/NPCBaseObjectInterface.h"
#include "MultiAreaSpellBoxInterface.generated.h"

/*
* 文件名称：MultiAreaSpellBoxInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-10-18
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMultiAreaSpellBoxInterface : public UNPCBaseObjectInterface
{
	GENERATED_BODY()
	typedef UNPCBaseObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	UMultiAreaSpellBoxInterface();
	~UMultiAreaSpellBoxInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MultiAreaSpellBoxInterface'"); } //获取蓝图对象路径

	/**
	*Define method 服务器通知跳转到指定检测区域
	*@param 区域索引
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MultiAreaSpellBoxInterface")
		void CLIENT_OnSwitchArea(int32 areaIndex);

	virtual void InitBlueCB() override;
};
