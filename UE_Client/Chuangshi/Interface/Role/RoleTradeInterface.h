// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Util/CS3Debug.h"
#include <vector>
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/GameDeFine.h"
#include "RoleTradeInterface.generated.h"

/*
* 文件名称：RoleTradeInterface.h
* 功能说明：角色之间交易接口类
* 文件作者：huangshijie
* 目前维护：chendongyong
* 创建时间：2016-12-07
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URoleTradeInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleTradeInterface();
	~URoleTradeInterface();
	static FString GetName() { return TEXT("RoleTradeInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleTradeInterface.BP_RoleTradeInterface_C'"); } //获取蓝图对象路径
	/**
	*Define method
	*BlueprintImplementableEvent,玩家向你申请交易
	*
	*@param entityID 玩家entityID
	*@param name 玩家名称
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onRoleTrade(int32 id, const FString& name);

	/**
	*Define method
	*BlueprintImplementableEvent,申请交易超时回调
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_tradeOvertime();

	/**
	*Define method
	*BlueprintImplementableEvent,交易状态改变
	*
	*@param state 当前状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onTradeState(int32 TradeState);
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleTradeInterface")
		void OnNotfiyRoleTradeStateBp();//交易状态改变通知蓝图

	/**
	*Define method
	*BlueprintImplementableEvent,对方锁定状态改变
	*
	*@param isLock 当前锁定状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onDstTradeLock(int32 isLock);

	/**
	*Define method
	*BlueprintImplementableEvent,对方确定交易
	*
	*@param state 当前状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onDstTradeSure(int32 state);

	/**
	*Define method
	*BlueprintImplementableEvent,改变交易金币
	*
	*@param money 金币数量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
		void CLIENT_onMoneyChangeBP(int64 money);

	void CLIENT_onMoneyChange(const int64& money);

	/**
	*Define method
	*BlueprintImplementableEvent,对方改变交易金币
	*
	*@param money 金币数量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onDstMoneyChangeBP(int64 money);

	void CLIENT_onDstMoneyChange(const int64& money);

	/**
	*Define method
	*BlueprintImplementableEvent,改变交易物品
	*
	*@param swapOrder 交易格子
	*@param kitOrder 所在背包位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onItemAdd(const int32& swapOrder, const int32& kitOrder, const int32& amount);

	/**
	*Define method
	*BlueprintImplementableEvent,对方改变交易物品
	*
	*@param swapOrder 交易格子
	*@param itemInst 物品数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onDstItemAdd(int32 swapOrder, const FString& itemInst);

	/**
	*Define method
	*BlueprintImplementableEvent,改变交易物品
	*
	*@param swapOrder 交易格子
	*@param kitOrder 所在背包位置
	*@param amount 物品數量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onItemSwap(const int32& swapOrder, const int32& kitOrder, const int32& amount);

	/**
	*Define method
	*BlueprintImplementableEvent,对方改变交易物品
	*
	*@param swapOrder 交易格子
	*@param itemInst 物品数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onDstItemSwap(const int32& swapOrder, const FString& itemInst);

	/**
	*Define method
	*BlueprintImplementableEvent,移除交易物品
	*
	*@param swapOrder 交易格子
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onItemRemove(int32 swapOrder);

	/**
	*Define method
	*BlueprintImplementableEvent,移除交易物品
	*
	*@param swapOrder 交易格子
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void CLIENT_onDstItemRemove(int32 swapOrder);

	/**
	*BlueprintCallable,通知改变任务对话过程中状态
	*
	*@param IsQuestTalking
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTradeInterface")
		void OnChangeTradeState(bool IsTrading);

	/**
	*BlueprintCallable,请求目标玩家交易
	* @param TargetID 目标ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTradeInterface")
		void requestRoleTrade(int32 TargetID);

	/**
	*BlueprintCallable,在申请交易过程中，距离对方过远
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleTradeInterface")
		void OnLeaveTargetByRequest();

	/**
	*BlueprintCallable,客户端请求服务器设置是否拒绝交易
	*
	* @param IsForbidRoleTrade 0：不拒绝；1：拒绝；
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleTradeInterface")
		void setForbidRoleTradeFC(int32 IsForbidRoleTrade);

	virtual void InitBlueCB() override;

	UFUNCTION(BlueprintPure, Category = "RoleTradeInterface")
		TRADE_STATE GetRoleTradeState();

	/*
	*打开邮件、商店、商城界面时，不能发起交易，也不能收到交易邀请
	*/
	UFUNCTION(BlueprintPure, Category = "RoleTradeInterface")
		bool IsCanTrade();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_agreeRoleTrade();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_cancelRoleTrade();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_requestRoleTradeMoneyChange(const int64& MoneyValue);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_requestRoleTradeItemAdd(const FString& STRING_1, const FString& STRING_2, const FString& STRING_3);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_requestRoleTradeItemRemove(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_requestRoleTradeLock();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_cancelRoleTradeLock();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_requestRoleTradeSure();

private:
	// 检测与交易对象的距离
	void detectTradeObject();

public:
	/// 交易对象entityID
	UPROPERTY(BlueprintReadOnly)
		int32 OppositeEntityID;

private:
	TRADE_STATE RoleTradeState;///交易状态

	FTimerHandle TimerHander;
	 
};