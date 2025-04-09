// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Util/CS3Debug.h"
#include "JsonObject.h"
#include <vector>
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/CS3Object.h"
#include "GameData/CrossMapConfigData.h"
#include "RoleTeleportInterface.generated.h"

/*
* 文件名称：RoleTeleportInterface.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：qiurunan
* 创建时间：2017-10-1228
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UTeleportData : public UCS3Object
{
	GENERATED_BODY()
public:
	///< 传送点的唯一索引
	UPROPERTY(BlueprintReadOnly)
		int32 Index; 
	///< 传送点目的地图
	UPROPERTY(BlueprintReadOnly)
		FString ScriptID;
	///< 传送点的等级限制 
	UPROPERTY(BlueprintReadOnly)
		int32 LimitLv;
	///< 传送点的阵营限制
	UPROPERTY(BlueprintReadOnly)
		int32 LimitCamp;
	///< 传送点消耗金钱
	UPROPERTY(BlueprintReadOnly)
		int32 MoneyCost;
	///< 传送点名称
	UPROPERTY(BlueprintReadOnly)
		FString TeleportTitle;
};


UCLASS(BlueprintType)
class CHUANGSHI_API UTeleportTalkData : public UCS3Object
{
	GENERATED_BODY()
public:
	///< 传送组ID
	UPROPERTY(BlueprintReadOnly)
		int32 GroupID;
	///< 传送组名称
	UPROPERTY(BlueprintReadOnly)
		FString GroupName;
	///< 传送组的传送点信息
	UPROPERTY(BlueprintReadOnly)
		TArray<UTeleportData*> TeleportDatas;
};

/**
*
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleTeleportInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleTeleportInterface();
	~URoleTeleportInterface();
	static FString GetName() { return TEXT("RoleTeleportInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleTeleportInterface.BP_RoleTeleportInterface_C'"); } //获取蓝图对象路径
		
public:
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleTeleportInterface")
		bool IsOpen(const FString& point);

	void RPC_TeleportPoint(const FString& point, int32 teleportType);

	//打开地图界面
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|URoleTeleportInterface")
		void OnOpenMapWin();

	UFUNCTION(BlueprintCallable, Category = "cs3|URoleTeleportInterface")
	void TeleportPoint(const FString& point, ENUM_STONE_TELEPORT_TYPE TeleportType = ENUM_STONE_TELEPORT_TYPE::StoneTeleportTypeDefault);

	UFUNCTION(BlueprintCallable, Category = "cs3|URoleTeleportInterface")
	FString GetPointByNPCID(const FString& NPCID);

	///<对话临时变量
	UPROPERTY()
		TArray<UTeleportTalkData*> talkContents;

	UPROPERTY(BlueprintReadOnly)
		FString teleportPointNPCs;

	void CancelTeleport();

public:
	virtual void InitBlueCB() override;

	///取消传送
	void OnCancelTeleport(ENUM_STONE_TELEPORT_TYPE TeleportType);
private:
	FTimerHandle DelayHandle;///定时器
};