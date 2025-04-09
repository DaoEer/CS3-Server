// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/RoleReviveCostData.h"
#include "GameData/GameDeFine.h"
#include "RoleReviveInterface.generated.h"

/*
* 文件名称：RoleReviveInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：all
* 创建时间：2017-07-29
*/

/**
 * 玩家复活接口类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleReviveInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	static FString GetName() { return TEXT("RoleReviveInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleReviveInterface.BP_RoleReviveInterface_C'"); } //获取蓝图对象路径

	/**
	*BlueprintCallable，复活
	*
	*@param reviveType 复活类型
	*
	*@return None
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleReviveInterface")
		void Revive(REVIVE_TYPE reviveType);

	/**
	*BlueprintCallable，区域复活点复活（优先）
	*
	*@param reviveSpace 复活地图
	*@param revivePosition 复位置
	*@param reviveDirection 复活方向
	*
	*@return None
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleReviveInterface")
		void ReviveOnArea(FString reviveSpace, FString revivePosition, FString reviveDirection);

	/**
	*BlueprintCallable，获得复活需要的消耗
	*
	*@param reviveType 复活类型
	*@param number  复活次数
	*
	*@return 消耗数量
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleReviveInterface")
		int32 GetReviveCostByOriginType(REVIVE_TYPE reviveType,int32 number);

	virtual void InitBlueCB() override;

	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface")
	void CLIENT_SetRevivePosStatus(int32 statusID, const FString& spaceScriptID);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface")
	void CLIENT_OnHideRevive();

	UFUNCTION(BlueprintCallable, Category = "RoleReviveInterface")
		void SetRevivePos();

	UFUNCTION(BlueprintNativeEvent, Category = "RoleRelationInterface")
		void NotifyReviveSpaceScriptID(const FString& spaceScriptID);

	/**
	*BlueprintCallable，请求复活对应的SpaceScriptID
	*@param reviveType 复活类型
	*@return None
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleReviveInterface")
		void RPC_requestReviveSpaceScriptID(REVIVE_TYPE reviveType);

private:
	void LoadReviveCostConfig();
private:
	TMap<REVIVE_TYPE, TArray<FROLE_REVIVE_COST_DATA*>> reviveCostDatas;//复活消耗数据
};
