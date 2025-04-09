// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/NPCBaseObjectInterface.h"
#include "GhostReceiverInterface.generated.h"

/*
* 文件名称：GhostReceiverInterface.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2017-08-10
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UGhostReceiverInterface : public UNPCBaseObjectInterface
{
	GENERATED_BODY()
	typedef UNPCBaseObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.GhostReceiverInterface'"); } //获取蓝图对象路径

};
