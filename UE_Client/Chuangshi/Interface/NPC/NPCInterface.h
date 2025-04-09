// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Interface/NPCBaseObjectInterface.h"
#include "NPCInterface.generated.h"

/*
* 文件名称：NPCInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

/**
*NPC接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UNPCInterface : public UNPCBaseObjectInterface
{
	GENERATED_BODY()
	typedef UNPCBaseObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UNPCInterface();
	~UNPCInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.NPCInterface'"); } //获取蓝图对象路径
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

	/**
	*NPC头像冒泡对话
	*
	* voice : 语音ID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|NPC")
		void CLIENT_BubbleDialogue(const FString& voice);


	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_talkWith(const FString& STRING_1, const FString& STRING_2);
	
	void onCollisionBegin();

	virtual void InitBlueCB() override;
};