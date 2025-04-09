// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "Entity/Alias.h"
#include "EntitySpaceEventInterface.generated.h"

/*
* 文件名称：EntitySpaceEventInterface.h
* 功能说明：
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2016-10-15
*/

/**
 * 监听副本事件
 */
USTRUCT()
struct FListenSpaceEvent
{
	GENERATED_USTRUCT_BODY()

public:
	int32 EventType;
	int32 EventID;
	AliasSpaceEventConditions ConsAlias;
};

/**
*副本事件接口
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UEntitySpaceEventInterface: public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	virtual void onLeaveWorld() override;
	static FString GetName() { return TEXT("EntitySpaceEventInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_EntitySpaceEventInterface.BP_EntitySpaceEventInterface_C'"); } //获取蓝图对象路径

	/**
	*Define method
	* BlueprintCallable，添加需要监听的副本事件
	*
	* @param eventType 事件类型，见SpaceEventType.h
	* @param eventID 事件ID
	* @param ConInfoStr 事件条件，格式 "{"ROOT": [{"param1": "", "param3": "2", "id": 1, "param2": "2", "param4": "2"}]}"
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
		void AddListenSpaceEvents(const FString& SpaceScriptID, const int32& EventType, const int32& EventID, const FString& ConInfoStr);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
		void CLIENT_AddListenSpaceEvents(const FString& SpaceScriptID, const int32& EventType, const int32& EventID, const FString& ConInfoStr);

	/**
	*Define method
	*BlueprintCallable，清除监听的副本事件
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
		void ClearListenSpaceEvents();

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
		void CLIENT_ClearListenSpaceEvents();

	/**
	*Define method
	* BlueprintCallable，玩家播放动作
	*
	* @param AtionIDs ，动作列表
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceEvent")
		void SpaceEventPlayAction(const TArray<FString>& AtionIDs);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceEvent")
		void CLIENT_SpaceEventPlayAction(const TArray<FString>& AtionIDs);

	/**
	* 玩家所在世界区域改变
	*
	* @param newArea 新区域
	* @param oldArea 原区域
	*
	* @return 无
	*/
	void onRoleChangeWorldArea(FString newArea, FString OldArea);

	/**
	* 玩家进入某事件区域（圆形、方形、...）
	*
	* @param EventType 事件
	* @param EventID 事件ID
	*
	* @return 无
	*/
	void onRoleEnterEventArea(INT32 EventType, INT32 EventID);

	/**
	* 玩家离开某事件区域（圆形、方形、...）
	*
	* @param EventType 事件
	* @param EventID 事件ID
	*
	* @return 无
	*/
	void onRoleLeaveEventArea(int32 EventType, int32 EventID);


	bool IsInListenSpaceEvent(int32 EventType);

	virtual void InitBlueCB() override;
private:
	/**
	* 触发副本事件
	*
	* @param EventType 事件
	* @param EventID 事件ID
	*
	* @return 无
	*/
	void TriggerSpaceEvent(int32 EventType, const TMap<FString, FString> & Params);


	/**
	* 检测是否符合触发副本事件
	*
	* @param Conditions 条件
	* @param Params 条件参数
	*
	* @return bool 符合触发副本事件返回TRUE，否则返回FALSE
	*/
	bool CheckEventConditions(AliasSpaceEventConditions& Conditions, const TMap<FString, FString> & Params);

	/**
	* 将tMap转换成FString
	*
	* @param tMap 要转换成FString的参数
	*
	* @return FString 将tMap转换成FString值
	*/
	FString MapToString(TMap<FString, FString> tMap);

private:
	void RPC_TriggerSpaceEventByClient(int32, TArray<int32>, FString);

private:
	UPROPERTY()
	TArray<FListenSpaceEvent> ListenSpaceEvents; ///<监听副本事件	
};

