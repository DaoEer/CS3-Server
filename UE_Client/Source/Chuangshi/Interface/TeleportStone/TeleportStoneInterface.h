// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Interface/NPCBaseObjectInterface.h"
#include "TeleportStoneInterface.generated.h"

/*
* 文件名称：TeleportStoneInterface.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：qiurunan
* 创建时间：2017-10-10
*/

/**
*NPC接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTeleportStoneInterface : public UNPCBaseObjectInterface
{
	GENERATED_BODY()
	typedef UNPCBaseObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UTeleportStoneInterface();
	~UTeleportStoneInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.TeleportStoneInterface'"); } //获取蓝图对象路径

public:
	//进入传送石触发范围（触发开启）
	UFUNCTION(BlueprintCallable, Category = "cs3|TeleportStone")
	void OnEnterTriggerRange();

	//离开传送石触发范围（触发开启）
	UFUNCTION(BlueprintCallable, Category = "cs3|TeleportStone")
	void OnLeaveTriggerRange();

	/**
	*设置模型编号
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "cs3|NPC")
	virtual void OnRep_modelNumber()override;

	/**
	*设置模型缩放
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "cs3|NPC")
	virtual void OnRep_modelScale()override;

};