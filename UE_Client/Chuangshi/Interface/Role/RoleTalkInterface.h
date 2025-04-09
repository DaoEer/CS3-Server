// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Util/CS3Debug.h"
#include "JsonObject.h"
#include <vector>
#include "CS3Base/CS3EntityInterface.h"
#include "RoleTalkInterface.generated.h"

/*
* 文件名称：RoleTalkInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URoleTalkInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleTalkInterface();
	~URoleTalkInterface();

	static FString GetName() { return TEXT("RoleTalkInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleTalkInterface.BP_RoleTalkInterface_C'"); } //获取蓝图对象路径


public:
	/**
	*Define method
	*刷新周围SpellBox的交互状态
	*
	*param eventType: 引起刷新的事件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|URoleTalkInterface")
		void RefreshAroundBoxStatus(int32 eventType);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|URoleTalkInterface")
		void onPlayGossipVoice(const FString& VoiceID);

	/**
	*BlueprintCallable,通知改变任务对话过程中状态
	* @param IsQuestTalking
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleTalkInterface")
		void OnChangeTalkState(bool IsTalking);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|URoleTalkInterface")
		void openStoreWindown(const int32& npcID);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_talkWithMonster(const FString& STRING_1, const FString& STRING_2);

	virtual void InitBlueCB() override;

	void CELL_RequestRefreshAreaStatus(int32 entityID);
};