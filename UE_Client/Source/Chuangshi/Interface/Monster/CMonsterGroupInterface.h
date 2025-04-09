// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3Base/CS3EntityInterface.h"
#include "CMonsterGroupInterface.generated.h"

/**
* 文件名称：CMonsterGroupInterface.h
* 功能说明：客户端集群怪物接口
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-12-16
 */
UCLASS()
class CHUANGSHI_API UCMonsterGroupInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	

public:
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.CMonsterGroupInterface'"); } //获取蓝图对象路径
	//void ReceiveCMDFollow(FVector TargetPos)
};
