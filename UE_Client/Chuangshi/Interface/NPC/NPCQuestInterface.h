// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CS3Base/CS3EntityInterface.h"
#include "NPCQuestInterface.generated.h"

/*
* 文件名称：NPCQuestInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

/**
*NPC任务类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UNPCQuestInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UNPCQuestInterface();
	~UNPCQuestInterface();
	static FString GetName() { return TEXT("NPCQuestInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_NPCQuestInterface.BP_NPCQuestInterface_C'"); } //获取蓝图对象路径

	UFUNCTION(BlueprintCallable, Category = "NPCQuestInterface")
	void RequestQuestStatus();///<查询任务状态

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_questDataApplyByClick(const FString& STRING_1, const FString& STRING_2);

	UFUNCTION(BlueprintNativeEvent, Category = "Game|RPC")
		void CLIENT_SetQuestSign(int32 flag);
	
	UFUNCTION(BlueprintNativeEvent, Category = "Game|RPC")
		void SetQuestSign(int32 flag);

	virtual void InitBlueCB() override;
};