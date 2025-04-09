// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Util/CS3Debug.h"
#include "JsonObject.h"
#include <vector>
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/NPCShopData.h"
#include "GameData/ShopType.h"
#include "Entity/Alias.h"
#include "RoleBuyNPCShopInterface.generated.h"

/*
* 文件名称：RoleBuyNPCShopInterface.h
* 功能说明：NPC商店购买出售相关函数接口
* 文件作者：huangshijie
* 目前维护：chendongyong
* 创建时间：2016-11-16
*/

UENUM(BlueprintType)
enum class NPCSHOP_TYPE :uint8
{
	// 普通类型
	COMMON_TYPE = 0,
	// 轮回秘境灵田种植商店
	LHMJ_FIELD_TYPE = 1,
};

UCLASS(BlueprintType)
class CHUANGSHI_API URoleBuyNPCShopInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleBuyNPCShopInterface();
	~URoleBuyNPCShopInterface();
	static FString GetName() { return TEXT("RoleBuyNPCShopInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleBuyNPCShopInterface.BP_RoleBuyNPCShopInterface_C'"); } //获取蓝图对象路径

	/**
	*Define method
	*BlueprintCallable，获得回购的物品列表
	*
	*@param data 回购物品打包数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void OnInitBuyBackItemList(const TArray<FBuyBackItemData>& buyBackItemDatas);

		void CLIENT_OnInitBuyBackItemList(const FVariant& Var);

	/**
	*Define method
	*BlueprintCallable，获得访问商店的物品列表
	*
	*@param nid 打开商店访问的npcid
	*@param sid 打开的商店id
	*@param itemList 商店物品列表
	*
	*@return 无
	*/
	void InitNPCShopItemList(const int32& nid, const FString& sid, const FVariant& fixedDict );
	/**
	*Define method
	*BlueprintCallable，获得访问商店的物品列表
	*
	*@param nid 打开商店访问的npcid
	*@param sid 打开的商店id
	*@param itemList 商店物品列表
	*@param discount 折扣
	*
	*@return 无
	*/
	void InitNPCShopItemListByDiscount(const int32& nid, const FString& sid, const FVariant& fixedDict, const float& discount);
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleBuyNPCShopInterface")
		void CLIENT_InitNPCShopItemList();

	//随机限量商品出售截止时间
	void onNotifyRandomItemSellEndTime(const FString& sid, const int32& EndTime);
	//获取相应商品随机限量商品出售截止时间
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		int32 getRandomItemShopSellEndTime(const FString& sid);
	//到点移除指定商店中出售的随机限量商品
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void removeRandomItemSell(const FString& sid);
	/**
	*Define method
	*BlueprintCallable，回购列表增加物品
	*
	*@param item 增加的物品
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void OnRequestSellItem(const FBuyBackItemData& buyBackItemData);

		void CLIENT_OnRequestSellItem(const FVariant& Var);
	
	/**
	*Define method
	*BlueprintCallable，回购列表减少物品
	*
	*@param item 减少的物品
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void OnRequestBuyBackItemBP(const FBuyBackItemData& buyBackItemData);

	void OnRequestBuyBackItem(const FVariant& Var);
	
	/**
	*BlueprintCallable，请求购买商店物品
	*
	*@param slot 商品编号
	*@param itemID 物品编号
	*@param amount 物品数量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void requestBuyNPCShopItem(const FString& slot, int itemID, int amount);

	/**
	*Define method
	*BlueprintNativeEvent，成功购物物品
	*
	*@param sid	商店名
	*@param slot 商品编号
	*@param itemID 物品编号
	*@param amount 物品数量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void CLIENT_OnSuccessBuyShopItem(const FString& sid, const FString& slot, int itemID, int amount);


	/**
	*BlueprintCallable，请求出售物品
	*
	*@param itemuid 物品的uid
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void requestSellItem(const FString& itemuid);

	/**
	*BlueprintCallable，请求回购物品
	*
	*@param itemuid 物品的uid
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void requestBuyBackItem(const FString& itemuid);

	/**
	*BlueprintImplementableEvent，刷新回购列表数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleBuyNPCShopInterface")
		void OnUpdateBuyBackItemList();
	
#pragma region	/** 高级回购，目前已删除这个功能，代码暂不删 */
	/**
	*BlueprintCallable，请求回购高级物品
	*
	*@param itemuid 物品的uid
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void requestBuyBackHighItem(const FString& itemuid);
	
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleBuyNPCShopInterface")
		void initHighBuyBackItemCB();///<BlueprintImplementableEvent，初始化高级回购列表回调，数据转到蓝图
	/**
	*Define method
	*BlueprintCallable，高级回购列表增加物品
	*
	*@param uid 物品的uid
	*@param time 回购倒计时
	*@param item 回购物品
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void addHighBuyBackItem(const FString& data);
	/**
	*Define method
	*BlueprintCallable，高级回购列表减少物品
	*
	*@param uid 减少的物品uid
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void subHighBuyBackItem(const FString& uid);
	/**
	*BlueprintImplementableEvent,增加高级回购列表回调，数据转到蓝图
	*
	*@param time 回购限时
	*@param item 物品
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleBuyNPCShopInterface")
		void addHighBuyBackItemCB(const FDateTime& time, const FString& item);

	/**
	*BlueprintImplementableEvent,减少高级回购列表回调，数据转到蓝图
	*
	*@param uid 物品uid
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleBuyNPCShopInterface")
		void subHighBuyBackItemCB(const FString& uid);
	/**
	* 给予高级回购物品所有uid
	*
	*@return TArray<FString> 高级回购物品所有uid
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		TArray<FString> getHighBuyBackUID();

	/**
	* 给予高级回购物品
	*
	*@param uid 物品id
	*
	*@return FString 高级回购物品数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		FString getHighBuyBackItem(const FString& uid);

	/**
	* 给予高级回购物品限时
	*
	*@param uid 物品id
	*
	*@return FDateTime 高级回购物品时间数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		FDateTime getHighBuyBackTime(const FString& uid);

#pragma endregion

#pragma region	/** 获取数据方法 */
	/**
	* 给予商品数量
	*
	*@return int32 商品数量
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		int32 getItemMapLength();

	/**
	* 获得商品Key列表
	*
	*@return TArray<FString> 商品key列表
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		TArray<FString> getItemMapKeys();

	/**
	* 给予商品内容
	*
	*@param slot 商品id
	*
	*@return FNPCShopData 商品数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		FNPCShopData getShopItemBySlot(const FString& slot);

	/**
	* 服务器商品开始时间
	*
	*@param slot 商品id
	*
	*@return float
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		float getShopItemStarTime(const FString& slot);

	/**
	* BlueprintCallable,获取商品价格
	*
	*@param ShopData 商品数据
	*
	*@return int32 TMap<FString, int32> 价格类型:价格值，如 money:10
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		TMap<FString, int32> GetGoodsPrice(FNPCShopData ShopData);

	/**
	* BlueprintCallable,获取商品购买限制
	*
	*@param FString Condition 商品购买限制
	*
	*@return int32 TMap<FString, FString> 价格类型:价格值，如 jadeItemLevel:3
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		TMap<FString, FString> GetGoodsCondition(FString Condition, TArray<FString>& ConditionKeys);

	/**
	* BlueprintCallable,根据商店ID返回商店类型结构体
	*
	*@param shopID 商店ID
	*
	*@return FSHOP_TYPE_DATA 返回配置
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
	FSHOP_TYPE_DATA GetShopTypeConfig(const FString& ShopID, bool& Find);

	/**
	* BlueprintCallable,获取商店标签页的tab名字和序号(跟策划约定 pageindex<0为随机商品的tab)
	*
	*@return 
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void GetShopPageIndexAndTabNames(TArray<int32>& PageIndexs, TArray<FString>& tabNames);
	/**
	* BlueprintCallable,根据标签页获取商品数据
	*
	*@param PageIndex 商店标签页
	*
	*@return FNPCShopData 返回商品数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		TArray<FNPCShopData> GetShopGoodsDataByPageIndex(int32 PageIndex);
	/**
	* BlueprintCallable,根据商品ID获取商品数据
	*
	*@param GoodsID 商品ID
	*
	*@return FNPCShopData 返回商品数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		FNPCShopData GetShopGoodsDataByGoodsID(FString GoodsID);
	/**
	* BlueprintCallable,根据UID获取回购数据
	*
	*@param UID
	*
	*@return FSHOP_TYPE_DATA 返回回购数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		UItemBase* GetBuyBackDataByUID(FString UID);
	/**
	* BlueprintCallable,获得最高可输入该商品的最大堆叠数，最低为1
	*
	*@param UID
	*
	*@return FSHOP_TYPE_DATA 返回数量
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		int32 GetCanBuyMaxCount(int32 Amount, int32 ItemID);
	/**
	* BlueprintCallable,是否置灰不能购买
	*
	*@param Condition 购买条件
	*
	*@return 是否置灰不能购买
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		bool CheckIsUnEnable(FString Condition);

	/**
	* BlueprintCallable,判断条件帮会商店等级
	*
	*@param ReqTongShopLevel 需要帮会商店等级
	*
	*@return 帮会商店等级是否足够
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		bool CheckTradeConditionTongShopLevel(int32 ReqTongShopLevel);

#pragma endregion

	/**
	* 客户端向服务器请求帮会商店数据
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void RequestTongShop();

#pragma region	/** 英雄王座商店 */
	/// 打开英雄王座商店
	void CLIENT_OpenTraviaShop(const int32& NPCID, const FVariant& GUARD_SOUL_DATAS_1, const FVariant& PAGODA_SOUL_DATA_1, const FVariant& DRUP_SOUL_DATAS_1);
	UFUNCTION(BlueprintImplementableEvent)
		void OpenTraviaShop(const int32& NPCID, const TArray<FDRUG_SOUL_SHOP_TYPE_DATA>& DrugShops);

	/// 购买战魂
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void RequestBuyCombatSoulItem(const FString& itemID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void CLIENT_OnRequestBuyCombatSoulItem(const FString& preItemID, const FString& itemID);
	/// 获取下一级战魂提示
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		FString GetNextCombatItemTip(const FString& itemID);
	/// 获取前一等级战魂数据
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		FCOMBAT_SOUL_SHOP_TYPE_DATA GetPreCombatItem(const FString& itemID);
	/// 获取下一等级战魂数据
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		FCOMBAT_SOUL_SHOP_TYPE_DATA GetNextCombatItem(const FString& itemID);

	/// 出售战魂
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void RequestSellCombatSoulItem(const FString& itemID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void CLIENT_OnRequestSellCombatSoulItem(const FString& itemID);
	/// 获取初始（第一级）战魂ID
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		int32 GetInitialCombatItemID(const FString& itemID);

	/// 召唤魂卫(type-0:上路，1:中路，2:下路)
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void RequestBuyGuardSoul(const FString& scriptID, const int32& type);
	/*召唤魂卫回调
	*
	* @param callTimer 召唤次数
	* @param scriptID 召唤魂卫的scriptID
	*
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void CLIENT_OnRequestBuyGuardSoul(const int32& callTimer, const FString& scriptID);

	/// 购买魂塔(srcScriptID-原有魂塔scriptID，dstScriptID-购买后的魂塔scriptID)
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void RequestUpdatePagodaSoul(const FString& srcScriptID, const FString& dstScriptID, const int32& wayType);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void CLIENT_OnRequestUpdatePagodaSoul(const FString& srcScriptID, const FString& dstScriptID,const int32& wayType);


	// 根据scriptID获取魂塔类型（熔岩塔-1，冰封塔-2，馅底塔-3）
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		int32 GetPagodaTypeByScriptID(const FString& SrciptID,const int32& wayType);
	// pagodaScriptID该塔是否存活
	bool IsSurvivalPagoda(const FString& pagodaScriptID, const TArray<FPAGODA_SOUL_SHOP_TYPE_DATA*>& Raws, const TArray<FString>& DeadPagodas, const int32& wayType);

	// 购买 英雄王座 药品
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void RequestBuyDrugItem(const int32& ItemID);
	// 出售 英雄王座 药品
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void RequestSellDrugItem(const int32& ItemID);

	/* 打开英雄王座 中立商店
	*
	* @param NPCID 
	* @param ScriptIDs 可以召唤的魂卫
	* @param Times 可以召唤的魂卫的次数
	* @param Level 可以召唤的魂卫的等级
	*
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void CLIENT_openLMNeuralShop(const int32& NPCID, const TArray<FString>& ScriptIDs, const TArray<int32>& Times, const int32& Level);
	/// 中立商店 购买魂卫(type-0:上路，1:中路，2:下路)
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void RequestBuyNeuralGuard(const FString& ScriptID, const int32& Type);
	UFUNCTION(BlueprintImplementableEvent)
		void CLIENT_OnBuyNeuralGuard(const FString& ScriptID);

	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		TMap<FString, FPAGODA_SOUL_SHOP_TYPE_DATA> GetPagodaSoulShopByWayTyp(const int32& wayType);
#pragma endregion

#pragma region	/** 帮会掠夺战商店分页 */
	///初始化帮会掠夺战商店分页商品数据
	void InitTongPlunderShopData();
	///获取帮会掠夺战商店分页商品数据
	UFUNCTION(BlueprintCallable)
		TArray<FNPCShopData> GetTongPlunderShopData();
	///请求购买帮会掠夺战商店分页商品
	UFUNCTION(BlueprintCallable)
		void RequestBuyTongPlunderShopItem(const FString& slot, int itemID, int amount);
	///锁定帮会商店
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void OnLockTongShop();
	void CLIENT_LockTongShop();
	///解锁帮会商店
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void OnUnLockTongShop();
	void CLIENT_UnLockTongShop();
	///帮会掠夺战商店分页商品售卖开始
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void OnTongPlunderShopSellStartBP();
	void OnTongPlunderShopSellStart(const FVariant& ShopDatas, const FString& EndTime);
	///帮会掠夺战商店分页商品售卖开始结束
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBuyNPCShopInterface")
		void OnTongPlunderShopSellEnd();
	void CLIENT_TongPlunderShopSellEnd();
	// 获得帮会掠夺战商店分页售卖结束时间
	UFUNCTION(BlueprintCallable)
		FString GetTongPlunderShopEndTime();
	// 获得帮会掠夺战商店分页商品出售成功

	void OnTongPlunderShopItemBuySuccess(const FString& Slot, const int& ItemID, const int& Amount);


#pragma endregion


#pragma region	/** 轮回秘境商店 */
	// 初始化商店
	void CLIENT_InitLHMJShopData(const int32& _NPCID, const FString& _ShopID, const FVariant& fixedDict);
	// 蓝图初始化商店
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnInitLHMJShop();
	// 蓝图刷新商店商品列表数据
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnUpdateShopItemList();
	// 蓝图更新刷新次数
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void OnUpdateRefreshNum();

	// 玩家手动刷新
	UFUNCTION(BlueprintCallable)
		void RequestReflashLHMJShop();
	void CLIENT_reflashLHMJShopData(const FVariant& fixedDict);
	// 玩家刷新次数（最多只能刷10次，刷完刷新按钮置灰）
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleLunHuiMiJinInterface")
		void CLIENT_reflashLHMJShopTime(const int32& _reflashNum);
	// 获取玩家手动刷新消耗
	UFUNCTION(BlueprintPure)
		int32 GetCurReflashCost();

	// 获取自动刷新时间（1小时刷一次。倒计时结束，界面调用RequestAutoReflashLHMJShop）
	UFUNCTION(BlueprintCallable)
		int32 GetAutoReflashTime();
	// 自动刷新（系统行为）
	UFUNCTION(BlueprintCallable)
		void RequestAutoReflashLHMJShop();
	void CLIENT_autoReflashLHMJShopData(const FVariant& fixedDict);

	// 购买商品
	UFUNCTION(BlueprintCallable)
		void RequestBuyLHMJShopItem(const FString& slot, const int32& itemID, const int32& amount);
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleLunHuiMiJinInterface")
		void CLIENT_OnSuccessBuyLHMJShopItem(const FString& slot, const int32& amount);
#pragma endregion

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestRepairOneEquip(const FString& STRING_1, const FString& STRING_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestRepairAllEquip(const FString& STRING_1);

	/*筛选小于等于某等级的物品*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void FilterItemsByLevel(const int32& level, const TArray<FNPCShopData> &itemarray, TArray<FNPCShopData>& result);
	/*物品的职业过滤器*/
	UFUNCTION(BlueprintCallable, Category = "RoleBuyNPCShopInterface")
		void FilterItemsByProfession(const int32& profession, const TArray<FNPCShopData> &itemarray, TArray<FNPCShopData>& result);

	virtual void InitBlueCB() override;
	virtual void onLeaveWorld() override;

private:
		void InitShopDatas(const FString& ShopID);
		void InitRandomShopDatas(const FString& ShopID, const TArray<FNPCSHOP_ITEM>& RandItem);
		void StructBackItem(TArray<FBuyBackItemData> Datas);
		UItemBase* GetItemByString(FBuyBackItemData Data);

		void AnalysisCombatSoul();
		void AnalysisGuardSoul(const TArray<FGUARD_SOUL_DATA>& GUARD_SOUL_DATAS_1);
		void AnalysisPagodaSoul(const TArray<FPAGODA_SOUL_DATA>& PAGODA_SOUL_DATA_1);
		void AnalysisNextPagodaSoul(const TArray<FPAGODA_SOUL_SHOP_TYPE_DATA*>& Rows, const FString SrcSriiptID, const FString& ScriptID, const int32& level,const int32& wayType);
		void AnalysisNeuralGuard(const TArray<FString>& ScriptIDs);

		void _InitShopData(const FVariant& fixedDict);

public:
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			int npcID;			///<访问npcid
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			FString shopID;		///<访问商店id
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			NPCSHOP_TYPE ShopType;		///<访问商店类型
		
		//回购数据
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			TArray<UItemBase*> BuyBackDatas;

		//出售比
		float NPCSHOP_SELL_RATIO = 1.0;

		///<战魂商店
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			TMap<int32, FCOMBAT_SOUL_SHOP_TYPE_DATA> CombatSoulShop;	

		///<魂卫商店
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			TMap<FString, FGUARD_SOUL_SHOP_TYPE_DATA> GuardSoulShop;	
		///<魂卫商店等级相关（scriptID：level）
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			TMap<FString, int32> GuardLevelMapping;		
		///<魂卫商店购买次数相关（scriptID：已经购买次数）
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			TMap<FString, int32> GuardBTimeMapping;
			
		///<已经被消灭的魂塔
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			TArray<FString> DeadPagoda;

		///<中立商店 魂卫
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			TMap<FString, FGUARD_SOUL_SHOP_TYPE_DATA> NeuralShop;

		// 轮回秘境商店刷新次数
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
			int32 RefreshNum;
		// 帮会商店掠夺分页是否存在
		UPROPERTY(EditAnywhere, BlueprintReadOnly)
			bool TongPlunderPage = false;

		// 帮会商店是否锁定商品
		UPROPERTY(EditAnywhere, BlueprintReadOnly)
			bool TongShopLock = false;

private:
		TMap<FString, TMap<FString, FNPCShopData>> NPCShopDatas;			// { 商店ID ： { 商品ID（非物品ID） ： 商品数据 } }
		TMap<FString, TMap<FString, FString>> TongShopExtDatas;				// { 商店ID ： { 商品ID（非物品ID） ： 分页 } }
		TMap<FString, TMap<FString, float>> ShopServerTime;					// { 商店ID ： { 商品ID（非物品ID） ： 服务器时间 } }
		//TMap<FString, TMap<FString, float>> *ItemMap;	///<访问商店的物品数据
		TMap<FString, FString> highBuyBackItem;///<高级回购物品数据
		TMap<FString, FDateTime> highBuyBackTime;///<高级回购物品限时
		TMap<int32, TMap<FString, FPAGODA_SOUL_SHOP_TYPE_DATA>> WayPagodaSoulShop;///<每路的魂塔商店

		TMap<FString, TMap<int32, int32>> TongPlunderShopItems; //{商品ID：{ItemID：ItemAmount}}
		TMap<FString, FNPCShopData> TongPlunderShopDatas;//{  商品ID（非物品ID） ： 商品数据 } ，和NPCShopDatas差不多
		FString TongPlunderShopEndTime; //帮会掠夺战商店分页售卖结束时间
		TMap<FString, int32> randomItemSellEndTimes; //随机限量商品出售截止时间
};
