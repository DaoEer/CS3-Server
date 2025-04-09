// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/TradeOrderData.h"
#include "GameData/TradeSuccessData.h"
#include "Entity/Alias.h"
#include "RoleLingShiTradeInterface.generated.h"

/*
* 文件名称：RoleLingShiTradeInterface.h
* 功能说明：灵石寄售
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

UENUM(BlueprintType)
enum class TRADETYPE : uint8
{
	LINGSHI_TRADE_SELL = 0	UMETA(DisplayName = "LINGSHI_TRADE_SELL"),
	LINGSHI_TRADE_COLLECT = 1   UMETA(DisplayName = "LINGSHI_TRADE_COLLECT"),
};

UCLASS(BlueprintType)
class CHUANGSHI_API URoleLingShiTradeInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleLingShiTradeInterface();
	~URoleLingShiTradeInterface();
	static FString GetName() { return TEXT("RoleLingShiTradeInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleLingShiTradeInterface.BP_RoleLingShiTradeInterface_C'"); } //获取蓝图对象路径

	/**
	*Define method
	*获得所有订单
	*
	*@param data 订单数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleLingShiTradeInterface")
	void GetAllOrderCB(const FVariant& data);

	/**
	*Define method
	*添加订单的回调
	*
	*@param data 订单数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleLingShiTradeInterface")
	void AddOrderCB(const FVariant& variant);

	/**
	*
	*添加订单的回调（自己） 通知界面
	*
	*@param OrderData  订单数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleLingShiTradeInterface")
		void OnAddMyOrder(FTradeOrderData OrderData);

	/**
	*
	*添加订单的回调（所有） 通知界面
	*
	*@param OrderData  订单数据
	*@param type 类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleLingShiTradeInterface")
		void OnAddOrderOfAll(int32 type, FTradeOrderData OrderData);

	/**
	*Define method
	*更新订单(自己的)
	*
	*@param data 订单数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleLingShiTradeInterface")
	void UpdataMyOrderToClient(const FVariant& variant);

	/**
	*
	*更新订单(自己的) 通知界面
	*
	*@param data 订单数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleLingShiTradeInterface")
		void OnUpdataMyOrderToClient(FTradeOrderData OrderData);

	/**
	*Define method
	*更新订单(所有的)
	*
	*@param data 订单数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleLingShiTradeInterface")
	void UpdataOrder(const FVariant& variant);

	/**
	*
	*通知界面更新出售订单
	*
	*@param OrderData 订单数据
	*@param type 类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleLingShiTradeInterface")
		void OnUpdataOrderOfAllOrades(int32 type,  FTradeOrderData OrderData);

	/**
	*
	*通知界面更新交易成功订单(收购)
	*
	*@param OrderData 订单数据
	*@param type 类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleLingShiTradeInterface")
		void OnUpdataSuccessOrder(int32 type, FTradeSuccessData OrderData);

	/**
	*Define method
	*下架订单
	*
	*@param data 订单数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleLingShiTradeInterface")
	void RemoveLingShiTradeOrderCB(const FString& uid);

	/**
	*
	*下架订单（自己） 通知界面
	*
	*@param uid 订单uid
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleLingShiTradeInterface")
		void OnRemoveMyLingShiTradeOrder(FTradeOrderData OrderData);

	/**
	*
	*下架订单（所有） 通知界面
	*
	*@param OrderData 订单
	*@param type 类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleLingShiTradeInterface")
		void OnRemoveAllLingShiTradeOrder(int32 type, FTradeOrderData OrderData);

	/**
	*Define method
	*刷新自己订单
	*
	*@param data 订单数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleLingShiTradeInterface")
	void RefreshMyOrderCB(const FVariant& variant);

	/**
	*Define method
	*刷新所有出售订单
	*
	*@param data 订单数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleLingShiTradeInterface")
	void RefreshAllSellOrderCB(const FVariant& variant);

	/**
	*Define method
	*刷新所有收购订单
	*
	*@param data 订单数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleLingShiTradeInterface")
	void RefreshAllCollectOrder(const FVariant& variant);

	/**
	*获得订单
	*
	*@param uid 订单唯一值
	*@param orderArray 订单数组
	*
	*@return 订单
	*/
	//UFUNCTION(BlueprintCallable, Category = "RoleLingShiTradeInterface")
	FTradeOrderData GetOrder(FString uid, TArray<FTradeOrderData> orderArray);

	/**
	*初始化我的订单
	*
	*@param orderData 订单数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "RoleLingShiTradeInterface")
	void InitLingShiTradeData(const TArray<FORDER_DATA>& orderData );

	/**
	*初始化所有出售订单
	*
	*@param orderData 订单数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "RoleLingShiTradeInterface")
	void InitAllLingShiTradeSellOrder(const TArray<FORDER_DATA>& orderData);
	/**
	*初始化所有收购订单
	*
	*@param orderData 订单数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintCallable, Category = "RoleLingShiTradeInterface")
	void InitAllLingShiTradeCollectOrder(const TArray<FORDER_DATA>& orderData);

	/**
	*从Json数据中获得订单
	*
	*@param data 订单数据
	*
	*@return 订单
	*/
	//UFUNCTION(BlueprintCallable, Category = "RoleLingShiTradeInterface")
	FTradeOrderData GetOrderFromJsonData(const FORDER_DATA& data);

	/**
	*
	*通知界面  初始化所有出售订单
	*
	*@param allSellOrder 所有出售订单
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleLingShiTradeInterface")
		void OnInitAllLingShiTradeSellOrder();

	/**
	*
	*通知界面  初始化所有收购订单
	*
	*@param allCollectOrder 所有收购订单
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleLingShiTradeInterface")
		void OnInitAllLingShiTradeCollectOrder();

	/**
	*
	*通知界面  初始化所有收购订单
	*
	*@param myAllOrder 自己所有订单
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleLingShiTradeInterface")
		void OnInitMyLingShiTradeOrder();

	/**
	*
	*处理寄售订单(购买或出让)
	*
	*@param type		类型
	*@param amount		数量
	*@param totalPrice 总价钱
	*@param uid		 订单数据唯一标识
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleLingShiTradeInterface")
		void DealLinShiTradeOrder(int type, int32 amount, int32 totalPrice, FString uid);

	/**
	*
	*增加订单(出售或收购)
	*
	*@param type		类型
	*@param price		单价
	*@param amount		数量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleLingShiTradeInterface")
		void AddOrder(int type, int32 price, int32 amount);


#pragma region	/** 排序显示相关 */
	/**
	*根据价格排序
	*
	*@param TradeType	类型，0：出售，1：收购
	*@param IsDescendingOrder	是否降序，true：降序，false：升序
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleLingShiTradeInterface")
		void SortOrdersByPrice(int TradeType, bool IsDescendingOrder);
	/**
	*根据数量排序
	*
	*@param TradeType	类型，0：出售，1：收购
	*@param IsDescendingOrder	是否降序，true：降序，false：升序
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleLingShiTradeInterface")
		void SortOrdersByAmount(int TradeType, bool IsDescendingOrder);
	/**
	*根据剩余时间排序
	*
	*@param TradeType	类型，0：出售，1：收购
	*@param IsDescendingOrder	是否降序，true：降序，false：升序
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleLingShiTradeInterface")
		void SortOrdersByRemainTime(int TradeType, bool IsDescendingOrder);
#pragma endregion

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_removeLingShiTradeOrder(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_refreshMyOrder();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestGetOrder();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_refreshAllSellOrder();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_refreshAllCollectOrder();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_takeOutMoney();

	virtual void InitBlueCB() override;
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<FTradeOrderData> LingShiTradeOrder;///< 玩家订单
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<FTradeOrderData> AllLingShiTradeSellOrder; ///< 所有的出售订单
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<FTradeOrderData> AllLingShiTradeCollectOrder;///< 所有的收购订单
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<FTradeSuccessData> LingShiTradeSellSuccessData;///< 所有的出售成功订单
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<FTradeSuccessData> LingShiTradeCollectSuccessData;///< 所有的收购成功订单
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 TradeTax; ///< 寄售的手续费
};
