// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/ShopMallItemData.h"
#include "GameData/BuyShopMallItemData.h"
#include "GameData/GiftGoodsData.h"
#include "RoleShopMallInterface.generated.h"

/*
* 文件名称：RoleShopMallInterface.h
* 功能说明：玩家商城类
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

UENUM(BlueprintType)
enum class SHOPMALLTYPE : uint8
{
	SHOP_TYPE_GIFT	  = 0	UMETA(DisplayName = "SHOP_TYPE_GIFT"),
	SHOP_TYPE_XIANSHI = 1	UMETA(DisplayName = "SHOP_TYPE_XIANSHI"),
	SHOP_TYPE_LINGSHI = 2   UMETA(DisplayName = "SHOP_TYPE_LINGSHI"),
	SHOP_TYPE_XUANSHI = 3	UMETA(DisplayName = "SHOP_TYPE_XUANSHI"),
};
UENUM(BlueprintType)
enum class SHOPMONEYTYPE : uint8
{
	SHOP_MONEY_TYPE_XIANSHI = 0	UMETA(DisplayName = "SHOP_MONEY_TYPE_XIANSHI"),
	SHOP_MONEY_TYPE_LINGSHI = 1 UMETA(DisplayName = "SHOP_MONEY_TYPE_LINGSHI"),
	SHOP_MONEY_TYPE_XUANSHI = 2	UMETA(DisplayName = "SHOP_MONEY_TYPE_XUANSHI"),
};

UCLASS(BlueprintType)
class CHUANGSHI_API URoleShopMallInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleShopMallInterface();
	~URoleShopMallInterface();
	static FString GetName() { return TEXT("RoleShopMallInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleShopMallInterface.BP_RoleShopMallInterface_C'"); } //获取蓝图对象路径

	virtual void OnEnterWorld();            ///< 当Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld();            ///< 当Entity离开世界（被销毁时）时，此方法被调用

	TMap<FString, TMap<FString, int32>>	GiftItemMap;
	TMap<FString, TMap<FString, int32>> XianShiItemMap;
	TMap<FString, TMap<FString, int32>> LingShiItemMap;
	TMap<FString, TMap<FString, int32>> XuanShiItemMap;
	UPROPERTY(BlueprintReadWrite)
	TArray<FShopMallItem> GiftItemList;
	UPROPERTY(BlueprintReadWrite)
	TArray<FShopMallItem> XianShiItemList;
	UPROPERTY(BlueprintReadWrite)
	TArray<FShopMallItem> XuanShiItemList;
	UPROPERTY(BlueprintReadWrite)
	TArray<FShopMallItem> LingShiItemList;
	UPROPERTY(BlueprintReadWrite)
	TArray<FGiftGoodsData> GivingGoodsData;
	UPROPERTY(BlueprintReadWrite)
	TArray<FGiftGoodsData> ReceiveGoodsData;
	UPROPERTY(BlueprintReadWrite)
	TArray<FBuyShopMallItemData> BuyShopMallItemData;
	UPROPERTY(BlueprintReadWrite)
	TArray<FCouponItemData> CouponItemList;

#pragma region 初始化商场中商品
	/**
	* Define method
	* 服务器回调函数
	* BlueprintCallable，获得访问商城中限量物品列表
	*
	* @param id - 打开商城访问的id
	* @param itemList - 商城限量的物品列表
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
	void GetShopMallItemList(const FString& data);
	void GetShopMallItemListCB();

	void AddShopMallItem(SHOPMALLTYPE shopMallType, FShopMallItem mallItem);

	/**
	* 初始化商城物品
	*
	* @param shopMallType - 商城类型
	*
	* @return None
	*/
	bool InitShopMallItem(SHOPMALLTYPE shopMallType);
	/**
	* 初始化商城物品 通知界面
	*
	* @return None
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
	void OnInitShopMallItem();
#pragma endregion
#pragma region 请求购买 和 请求增送 请求处理收到的礼品数据
	/**
	* 请求购买
	*
	* @param couponUID - 优惠劵uid
	*
	* @return None
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
		void RequestBuyShopMallItem(const FString& couponUID);

	/**
	* 请求赠送
	*
	* @param targetDBID - 赠送玩家的DBID
	*
	* @return None
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
		void RequestGiveShopMallItemToRole(int32 targetDBID);

	/**
	*
	* BlueprintCallable，请求处理收到的礼品数据
	*
	* @param goodsDataUIDs uid数组
	* @param dealWay 处理方式  1：接收 0：拒绝
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
		void RequestDealReceiveGoodsData(TArray<FString> goodsDataUIDs, int32 dealWay);

#pragma endregion

	/**
	* 获得商城中商品数量
	*
	* @return 该商场商品的数量
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
		int32 GetItemMapLength(SHOPMALLTYPE shopMallTypeID);
	/**
	* 获得某个商品数据
	*
	* @param slot - 商品id
	*
	* @return 商品数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
		TArray<int32> GetItemMapList(SHOPMALLTYPE shopMallTypeID,const FString& slot);

	TMap<FString, TMap<FString, int32>>* GetShopMallItemMap(SHOPMALLTYPE shopMallTypeID);

	
#pragma region 赠送记录
	/**
	* Define method
	* 服务器回调函数
	* BlueprintCallable，增加一条赠送礼品记录
	*
	* @param goodsData - 数据
	*
	* @return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
	void AddGivingGoodsDataRecord(const FVariant& goodsData);

	/**
	* 
	* 增加一条赠送礼品记录 通知界面
	*
	* @param goodsData - 数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void AddGivingGoodsDataRecordCB(FGiftGoodsData goodsData);

	/**
	* Define method
	* 服务器回调函数
	* BlueprintCallable，增加一条接收礼品记录
	*
	* @param goodsData - 数据
	*
	* @return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
	void AddReceiveGoodsDataRecord(const FVariant& goodsData);

	/**
	* 
	* 增加一条接收礼品记录 通知界面
	*
	* @param goodsData - 数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void AddReceiveGoodsDataRecordCB(FGiftGoodsData goodsData);
	
	/**
	* Define method
	* 服务器回调函数
	* BlueprintCallable，初始化礼品记录
	*
	* @param data - 数据
	*
	* @return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
	
	void InitGoodsDataRecord(const FVariant& data);

	/**
	* 初始化赠送礼品记录
	*
	* @param goodsData - 数据
	*
	* @return None
	*/
	//UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
	void InitGivingGoodsDataRecord(const KBEngine::FVariantArray& goodsData);

	/**
	* 初始化赠送礼品记录  通知界面
	*
	*
	* @return None
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void InitGivingGoodsDataRecordCB();

	/**
	* 初始化接收礼品记录
	*
	* @param goodsData - 数据
	*
	* @return None
	*/
	//UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
	void InitReceiveGoodsDataRecord(const KBEngine::FVariantArray& goodsData);

	/**
	* 初始化接收礼品记录 通知界面
	*
	*
	* @return None
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void InitReceiveGoodsDataRecordCB();

	/**
	* 获得礼品数据
	*
	* @param goodsData - 数据
	*
	* @return None
	*/
	FGiftGoodsData GetGiftDataFromJsonData(const FString& data);

	FGiftGoodsData GetGiftDataFromVariantData(const FVariant& data);
	/**
	* Define method
	* 服务器回调函数
	* BlueprintCallable，处理接收礼品数据的回调函数
	*
	* @param goodsData - 数据
	*
	* @return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
	void DealReceiveGivingGoodsDataCB(const FVariant& data);

	/**
	* Define method
	*
	* BlueprintCallable，处理接收礼品数据的回调函数 通知界面(刷新接收礼品数据)
	*
	* @return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void OnDealReceiveGivingGoodsData(const FString& goodsDataUid);

	/**
	* Define method
	* 服务器回调函数
	* BlueprintCallable，赠送礼品数据的回调函数
	*
	* @param goodsData - 数据
	*
	* @return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
	void ChangeGivingGoodsDataCB(const FVariant& goodsData);

	/**
	* 
	* BlueprintImplementableEvent，赠送礼品数据的回调函数 (刷新赠送的数据)
	*
	* @return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void OnChangeGivingGoodsData(const FString& goodsDataUid);

	/**
	* Define method
	* 服务器回调函数
	* BlueprintCallable，清除赠送记录
	*
	* @param goodsDataUIDs - uid数组
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
		void ClearGivingGoodsDataRecordCB(const TArray<FString>& goodsDataUIDs);

	/**
	*
	* BlueprintImplementableEvent，清除赠送记录 通知界面
	*
	* @return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void OnClearGivingGoodsDataRecord(const FString& goodsDataUid);

	/**
	* Define Method
	* 服务器回调函数
	* BlueprintCallable，清除接收记录
	*
	* @param goodsDataUIDs - uid数组
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
		void ClearReceiveGoodsDataRecordCB(const TArray<FString>& goodsDataUIDs);

	/**
	*
	* BlueprintCallable，清除接收记录 通知界面
	*
	*
	* @return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void OnClearReceiveGoodsDataRecord(const FString& goodsDataUid);

	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
	FGiftGoodsData GetGiftGoodsData(const FString& goodsDataUid, const TArray<FGiftGoodsData>& giftGoodsDataArray);
	/**
	*
	* BlueprintCallable，通过礼品Uid获得礼品数据
	*
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
	FGiftGoodsData GetReceiveGiftGoodsDataByUID(FString goodsDataUid);
	/**
	*
	* BlueprintCallable，通过礼品Uid获得礼品数据
	*
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
	FGiftGoodsData GetGivingGiftGoodsDataByUID(FString goodsDataUid);
#pragma endregion

	/**
	* BlueprintCallable，通过商品ID获得商品数据
	*
	* @param id - 商品ID
	*
	* @return FShopMallItem 商品数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
	FShopMallItem GetShopMallItemByID(FString id);

	/**
	* BlueprintCallable，通过商品ID和商城获得商品数据
	*
	* @param shopMallTypeID 商城类型
	* @param id - 商品ID
	*
	* @return FShopMallItem 商品数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
	FShopMallItem GetShopMallItemByIDAndMallType(SHOPMALLTYPE shopMallTypeID,FString id);

	/**
	* BlueprintCallable，通过商品ID和商品列表获得指定商品
	*
	* @param shopMallTypeID 商城类型
	* @param id - 商品ID
	*
	* @return FShopMallItem 商品数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
	FShopMallItem GetShopMallItemByIDAndItemList(TArray<FShopMallItem> mallItemList, FString id);

#pragma region 优惠劵
	/**
	* 服务器回调函数
	* BlueprintCallable，初始化优惠劵
	*
	* @param data
	*
	* @return None
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
	void InitCouponItem(const FVariant& data);

	/**
	* BlueprintCallable，初始化优惠劵
	*
	* @param data
	*
	* @return None
	*/
	//UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
	//	void OnInitCouponItem(const TArray<FString>& data);

	/**
	* 初始化商城优惠劵 通知界面
	*
	** @return None
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void OnInitCouponItemCB();

	/**
	* BlueprintCallable，初始化优惠劵
	*
	* @param data
	*
	* @return FCouponItemData
	*/
	//UFUNCTION(BlueprintCallable, Category = "RoleShopMallInterface")
	FCouponItemData GetCouponItemByData(const FVariant& data);

	/**
	* Define Method
	* 服务器回调函数
	* BlueprintCallable，增加优惠劵
	*
	* @param data 优惠劵数据
	*
	* @return None
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
	void AddCouponItem(const FVariant& data);

	/**
	* BlueprintCallable，增加优惠劵 通知界面
	*
	* @param data 优惠劵数据
	*
	* @return None
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void AddCouponItemCB(FCouponItemData couponItem);

	/**
	* Define Method
	* 服务器回调函数
	* BlueprintCallable，删除优惠劵
	*
	* @param couponUid 优惠劵uid 唯一标识
	*
	* @return None
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleShopMallInterface")
	void RemoveCouponItem(const FString& couponUid);

	/**
	* BlueprintCallable，删除优惠劵 通知界面
	*
	* @param couponUid 优惠劵uid 唯一标识
	*
	* @return None
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShopMallInterface")
		void RemoveCouponItemCB(const FString& couponUid);

#pragma endregion

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestShopMallItemList();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_withDrawGiveGoodsData(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_clearGivingGoodsDataRecord(const TArray<FString>& ARRAY_STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_clearReceiveGoodsDataRecord(const TArray<FString>& ARRAY_STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_takeBackGivingGoodsData(const FString& STRING_1);

	virtual void InitBlueCB() override;
};