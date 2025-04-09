#pragma once
#include "Object.h"
#include "Entity/Alias.h"
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Store/StoreGoodsDataTable.h"
#include "GameData/Store/StoreRecordData.h"
#include "GameData/Store/StoreGiftBoxData.h"
#include "GameData/ConstDataBP.h"
#include "KBEngine.h"
#include "GameData/CharacterData.h"
#include "../../Actor/GameCharacter.h"
#include "RoleStoreInterface.generated.h"

class AModifyFaceCharacter;
class AGameCharacter;

/*
* 文件名称：RoleStoreInterface.h
* 功能说明：玩家商城
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2019-04-22
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URoleStoreInterface : public UCS3EntityInterface
{
	GENERATED_BODY()	
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleStoreInterface();
	~URoleStoreInterface();
	static FString GetName() { return TEXT("RoleStoreInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleStoreInterface.BP_RoleStoreInterface_C'"); } //获取蓝图对象路径
			
	virtual void onEnterWorld() override;        ///< 当Entity进入世界时，此方法被调用
	virtual void onLeaveWorld() override;		///< 当Entity离开世界（被销毁时）时，此方法被调用
	void InitBlueCB();

	void Init();

#pragma region	/** 商品数据(客户端没存数据表版本) - 废弃 */
	
	///请求商品数据（专区）<废弃>
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void RPC_openStoreUI(const int32& GoodsType, const int32& ItemType);
	/**
	* Define method
	* <废弃>
	* BlueprintNativeEvent，更新服务器商城数据
	*
	* @return 无
	*/
	void CLIENT_OnUpdateStoreGoods(const FString& FString_1, const FVariant& FSTOREGOODS_DICT_1);

	/**
	* Define method
	* BlueprintImplementableEvent，客户端更新完数据完毕 <废弃>
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLIENT_OnUpdateStoreGoodsOver(const int32& GoodType, const int32& ItemType);

	///根据商品ID列表获得商品<废弃>
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
	void RPC_GetGoodsListByIDList(const TArray<int32>& GoodsIDList);

	/**
	* Define method
	* BlueprintNativeEvent，通过ID列表获得商品列表服务器回调<废弃>
	*
	* @return 无
	*/
	void CLIENT_OnGetGoodsListByIDList(const FVariant& FSTOREGOODS_DICT_1);

	///列表获得商品列表事件回调<废弃>
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStoreInterface")
	void OnGetGoodsListByIDListOver(const TArray<FSTORE_GOODS_DATA_TABLE>& GoodsList);

	///请求推荐商品 <废弃>
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void RPC_UpdateRecommentGoods();
	/**
	* Define method
	*<废弃>
	* BlueprintNativeEvent，通过ID列表获得推荐首页商品列表回调
	*
	* @return 无
	*/
	void CLIENT_OnGetRecommentGoods(const FVariant& FSTOREGOODS_DICT_1);

	///通过ID列表获得推荐首页商品列表事件回调 <废弃>
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStoreInterface")
		void OnGetRecommentGoodsOver();

	///申请获得专区新品数据 <废弃>
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_GetStoreNewGoods(const int32& GoodType);
	/*
	* Define method
	*<废弃>
	* BlueprintNativeEvent，获得商城新品数据回调
	*
	*/
	void CLIENT_OnGetStoreNewGoods(const FString& cfgTime, const FVariant& FSTOREGOODS_DICT_1);

	///列表获得商品列表事件回调 <废弃>
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLIENT_OnUpdateStoreNewGoodsOver(const int32& GoodType);

	/**
	*Define method
	*BlueprintCallable,通知客户端查询数量限制
	*
	*@param goodsIDList 商品ID列表
	*@param amountList 商品可购买数量列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLIENT_OnRequestStoreLimitGoodsList(const TArray<int32>& goodsIDList, const TArray<int32>& amountList);

	/*查询商品限制购买数量*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RequestStoreLimitGoodsList();

	///根据类型获得商品
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GOODS_DATA_TABLE> GetStoreGoodsByType(const int& GoodType, const int32& ItemType);

	///根据类型获得新品商品（专区）
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GOODS_DATA_TABLE> GetStoreNewGoods(const int32& GoodsType);

	///获得推荐页新品商品
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GOODS_DATA_TABLE> GetStoreRecommentNewGoods();
	/**
	*BlueprintCallable，根据类型获得推荐商品
	*
	*@param ItemType 二级标签类型，0:新品，1:神机灵宝，2:幻兽道具，3:奇珍异宝，4:灵丹妙药
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GOODS_DATA_TABLE> GetStoreRecommentGoodsByType(int32 ItemType);
#pragma endregion

#pragma region	/** 商品数据 */
	///根据多级标签获得商品
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GOODS_DATA_TABLE> GetStoreGoodsByLable(const int& GoodType, const int32& ItemType, const int32& ThirdLable);

	///根据多级标签从外观数据表获得商品
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GOODS_DATA_TABLE> GetStoreAppearancesByLable(const int& GoodType, const int32& ItemType, const int32& ThirdLable);

	///根据商品ID获得商品
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		FSTORE_GOODS_DATA_TABLE GetStoreGoodsByID(const int32& GoodsID);

	///根据商品ID判断是否有商品
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		bool IsValidStoreGoods(const int32& GoodsID);

	///消耗仙石获得返利
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		int32 GetRebate(const int32& Price, const int32& GoodsID = 0);

	///搜索商品
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GOODS_DATA_TABLE> GetSearchGoodsList(const FString& SearchString);
#pragma endregion

#pragma region	/** 购买和赠送记录 */
	/*更新购买记录*/
	void CLIENT_OnUpdateBuyRecords(const FVariant& FSTORE_BUY_RECORD_DICT_1);

	/*更新购买记录事件回调*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStoreInterface")
		void OnQueryBuyRecords();
	/*删除购买记录*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DeleteBuyRecord(const FString& UID);
	/*删除购买记录回调*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLINET_OnDeleteBuyRecord(const FString& UID);

	/*清空购买记录*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DeleteBuyRecords();

	/*清空购买记录回调*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLINET_OnDeleteBuyRecords();

	/*申请购买商品*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RequestBuyStoreGoods(int32 GoodsID, int32 Amount);

	/*查询购买记录*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_QueryBuyRecords();

	/**
	*Define method
	*BlueprintCallable,货币不足
	*
	*@param GoodType 商品类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLIENT_StoreNotEnoughMoney(const int32& GoodType);

	/*赠送某人礼物*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RequestPresentGift(const int32 GoodsID, const int32& Amount, const FString& ReceiverName, const FString& ReceiverDBID, const FString& Message);

	void CLIENT_OnRequestPresentGift(const FVariant& FSTORE_GIFT_BOX_DATA_1);

	/*赠送礼物完成回调*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStoreInterface")
	void OnRequestPresentGiftOver(FSTORE_GIFT_BOX SendGift);

	/*更新赠送记录*/
	void CLIENT_OnUpdatePresentRecords(const FVariant& FSTORE_PRESENT_RECORD_DICT_1);
	/*更新赠送记录事件回调*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStoreInterface")
		void OnUpdatePresentRecords();

	/*查询赠送记录*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_QueryPresentRecords();

	/*删除赠送记录*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DeletePresentRecord(const FString& UID);

	/*删除赠送记录回调*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLINET_OnDeletePresentRecord(const FString& UID);

	/*清空赠送记录*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DeletePresentRecords();

	/*清空赠送记录回调*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLINET_OnDeletePresentRecords();

	///获得购买记录
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_BUY_RECORD_DATA> GetBuyRecords();
	///删除购买记录
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void DeleteBuyRecord(const FString& UID);
	///清空购买记录
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void DeleteBuyRecords();

	///获得赠送记录
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_PRESENT_RECORD_DATA> GetPresentRecords();
	///删除购买记录
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void DeletePresentRecord(const FString& UID);
	///清空购买记录
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void DeletePresentRecords();

	///购买完成
	void OnStoreBuyComplete();
#pragma endregion

#pragma region	/** 礼品盒 */
	/*查询礼品盒*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestOpenGiftBox();

	/*接受礼品盒*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_AcceptGift(const FString& UID);

	/*接受全部礼品盒*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_AcceptGifts();

	/*拒绝礼品盒*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RefuseGift(const FString& UID);

	/*拒绝全部礼品盒*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RefuseGifts();

	/*删除收礼记录*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DeleteGiftBoxReceiveRecord(const FString& UID);

	/*删除收礼记录回调*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLINET_OnDeleteGiftBoxReceiveRecord(const FString& UID);

	/*清空收礼记录*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DeleteGiftBoxReceiveRecords();

	/*清空收礼记录回调*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLINET_OnDeleteGiftBoxReceiveRecords();

	/*取回礼品*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_GetBackGift(const FString& UID);

	/*全部取回礼品*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_GetBackGifts();

	/*删除送礼记录*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DeleteGiftBoxSendRecord(const FString& UID);

	/*删除送礼记录回调*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLINET_OnDeleteGiftBoxSendRecord(const FString& UID);

	/*清空送礼记录*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DeleteGiftBoxSendRecords();

	/*删除送礼记录回调*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLINET_OnDeleteGiftBoxSendRecords();

	/*转增*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_TransferPresent(const FString& UID, const FString& ReceiverName, const FString& ReceiverDBID, const FString& Message);

	/**
	*Define method
	*BlueprintCallable,更新礼品盒数据
	*
	*@param SendGiftDict 赠送礼品盒数据
	*@param ReceiveGiftDict 收取礼品盒数据
	*
	*@return 无
	*/
	void CLIENT_OnUpdateGiftBox(const  FVariant& FSTORE_GIFT_BOX_DATA_DICT_1, const FVariant& FSTORE_GIFT_BOX_DATA_DICT_2);
	/*更新礼品盒数据事件回调*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStoreInterface")
		void OnUpdateGiftBox();

	/*接受到礼物更新礼品盒数量事件*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStoreInterface")
		void OnUpdateReceiveGiftBoxAmount(const int32& Amount);

	///赠送礼品盒
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GIFT_BOX> GetSenderGiftBox();

	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void DeleteSenderGiftBox(const FString& UID);

	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void DeleteSenderGiftBoxs();

	///收取礼品盒
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GIFT_BOX> GetReceiverGiftBox();

	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void DeleteReceiverGiftBox(const FString& UID);

	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void DeleteReceiverGiftBoxs();

	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		int32 GetNoStateGiftBoxAmount();

	/**
	*Define method 礼品盒显示红点
	*@param Type 类型 0：赠礼显示红点 1：收礼显示红点
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLINET_GiftBoxShowRedPoint(const int32& Type);

	/*查看礼品盒红点后*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnShowGiftBoxRedPoint(const int32& Type);

#pragma endregion

#pragma region	/** 购物车 */
	/*购物车批量购买商品*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_BuyStoreCartGoods(TArray<int32> GoodsIDList, TArray<int32> AmountList);


	/*购物车批量赠送商品*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_PresentStoreCartGoods(TArray<int32> GoodsIDList, TArray<int32> AmountList, const FString& ReceiverName, const FString& ReceiverDBID, const FString& Message);

	/*将某商品添加到购物车*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_AddStoreCartGoods(int32 GoodsType, int32 GoodsID, int32 Amount);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLIENT_OnAddStoreCartGoods(int32 GoodsType, int32 GoodsID, int32 Amount);

	/*将某商品从购物车删除*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DeleteStoreCartGoods(int32 GoodsType, int32 GoodsID );

	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLIENT_OnDeleteStoreCartGoods(int32 GoodsType, int32 GoodsID);

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStoreInterface")
	void OnDeleteStoreCartGoods(int32 CartType, int32 GoodsID);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DeleteSoldOutStoreCartGoods(const int32& CartType);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
	void OnDeleteSoldOutStoreCartGoods(const int32& CartType, const TArray<int32>& GoodsIDs);

	/*清空某专区的购物车*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_ClearStoreCartGoods(int32 CartType);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleStoreInterface")
		void CLIENT_OnClearStoreCartGoods(int32 CartType);

	/*将客户端的购物车数据更新到服务器*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_SynStoreCartGoods();

	/*打开购物车*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OpenStoreCart();

	/*更新购物车数据到客户端*/
	void CLIENT_UpdateStoreCart(const FVariant& FSTORE_CART_DATA_DICT_1);

	/*更新购物车数据事件回调*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStoreInterface")
		void OnUpdateStoreCart();
	
	/*获得购物车数据
	* @param CartType 购物车标签页类型，0仙石，1玄石
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GOODS_DATA_TABLE> GetStoreCartGoods(int32 CartType);
	/*获得购物车数据*/
	UFUNCTION(BlueprintPure, Category = "RoleStoreInterface")
		int32 GetAllStoreCartGoodsAmount();

	/*修改购物车*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void SetStoreCartGoods(int32 GoodsType, int32 GoodsID, int32 Amount);

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStoreInterface")
		void OnUpdateStoreCartGoodsAmount(int32 GoodsType, int32 GoodsID, int32 Amount);

	/*根据商品类型获得购物车类型
	* @param GoodsType 商品类型
	* return 购物车标签页类型，0仙石，2玄石
	*/
	UFUNCTION(BlueprintPure, Category = "RoleStoreInterface")
		int32 GetCartTypeByGoodsType(int32 GoodsType);
#pragma endregion

#pragma region	/** 外观 */
	/**
	*BlueprintCallable，获取商品外观数据
	*
	*@param GoodsID	商品ID
	*@param AppearType	外观类型，-1为坐骑，非-1为模型部件类型MODEL_PART_TYPE
	*@param AppearID	外观ID，AppearType为-1时表示坐骑ID，非-1时表示模型部件ID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void GetAppearanceData(int32 GoodsID, int32& AppearType, FString& AppearID);
	/**
	*BlueprintCallable，获取商品外观数据
	*
	*@param ItemID	物品ID
	*@param AppearType	外观类型，-1为坐骑，非-1为模型部件类型MODEL_PART_TYPE
	*@param AppearID	外观ID，AppearType为-1时表示坐骑ID，非-1时表示模型部件ID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void GetAppearanceDataByItemID(int32 ItemID, int32& AppearType, FString& AppearID);
	/**
	*BlueprintCallable，切换天气
	*
	*@param IsNightWeather ture为黑夜，false为返回默认天气（黄昏）
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void ChangeWeather(bool IsNightWeather);
	///增加拥有外观
	void AddHasStoreAppearance(const int32& ItemID);

	/**
	*BlueprintCallable，换上商城外观
	*@param AppearanceType 外观类型
	*@param AppearanceID 外观模型ID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_PutOnStoreAppearance(int32 AppearanceType, FString AppearanceID, int32 ItemID);

	/**
	*BlueprintCallable，脱掉商城外观
	*@param AppearanceType 外观类型
	*@param AppearanceID 外观模型ID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_TakeOffStoreAppearance(int32 AppearanceType, FString AppearanceID, int32 ItemID);

	///穿上商城外观
	void AddStoreAppearance(const int32& ItemID);

	///脱掉商城外观
	void RemoveStoreAppearance(const int32& ItemID);

	/**
	*BlueprintCallable，将客户端的商城外观背饰的参数更新到服务器
	*@param ItemID 背饰物品ID
	*@param Location 相对位置
	*@param Rotation 相对旋转
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
	void RPC_SetStoreBackAdornParam(int32 ItemID, FVector Location, FRotator Rotation);

	/*将服务器的商城外观背饰的参数更新到客户端*/
	void UpdateStoreBackAdornParam(int32 ItemID, FString ParamStr);

	/*通过物品ID获得背饰参数*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		FSTORE_BACK_ADORN_PARAM GetStoreBackAdornParam(const int32& ItemID);

	/*判断商城外观物品是否过期*/
	bool IsItemAppearacesExpired(const int32& ItemID);

	/*根据商品ID获得商城外观状态*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		STORE_APPEARANCE_STATE StoreAppearanceState(const int32& GoodsID);

	/*新增试穿外观*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void AddStoreTryAppearances(const int32& PartType, const int32& GoodsID);

	/*移除试穿外观*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void RemoveStoreTryAppearances(const int32& PartType);

	/*清空试穿外观*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		void ClearStoreTryAppearances();

	/*获得试穿外观*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TMap<int32, int32> GetStoreTryAppearances();

	/*外观是否已试穿*/
	bool IsStoreTryAppearance(int32 ItemID);

	/*获取已试穿的外观部件*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TMap<MODEL_PART_TYPE, FString> GetStoreTryAppearancePart();

	/*获得已穿外观*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<int32> GetStoreWearAppearances();

	/*根据部件类型获得已拥有外观的数量*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		int32 GetStoreHasAppearancesAmount(int32 AppearanceType);

	/*筛选出已拥有的外观商品*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		TArray<FSTORE_GOODS_DATA_TABLE> FilterHasAppearances(TArray<FSTORE_GOODS_DATA_TABLE> GoodsDatas);

	/*根据载具ID获取载具数据*/
	UFUNCTION(BlueprintCallable, Category = "RoleStoreInterface")
		FCARRIER_DATA GetCarrierConfigData(FString CarrierID);

	/*更新云裳阁外观后,同步更新云裳阁角色（主要针对这二条协议回复：
	   RPC_PutOnStoreAppearance
	   RPC_TakeOffStoreAppearance）*/
	void OnUpdateStoreAppearance(const int32&  AppearanceType);

	/*获取云裳阁里面的Character(真实类：BP_ClothesCharacter继承自ModifyFaceCharacter)*/
	UFUNCTION(BlueprintPure, Category = "RoleStoreInterface")
		AModifyFaceCharacter* GetStoreCharacter();

	/*偏移值Float转换为FVector*/
	UFUNCTION(BlueprintPure, Category = "RoleStoreInterface")
		float SetVectorForFloat(FVector CurVector, AGameCharacter* TargetCharacter,FString PartID);

	/*偏移值Float转换为FVector*/
	UFUNCTION(BlueprintPure, Category = "RoleStoreInterface")
		FVector SetFloatForVector(float CurDeviation, AGameCharacter* TargetCharacter, FString PartID);

#pragma endregion

private:
	///更新客户端数据
	void OnUpdateStoreGoods(const TArray<FSTORE_GOODS_DATA_TABLE> goodsList, const FString cfgTime);
	TArray<FSTORE_GOODS_DATA_TABLE> SortStoreGoods(TArray<FSTORE_GOODS_DATA_TABLE> GoodsList);
	TArray<FSTORE_GOODS_DATA_TABLE> SortStoreAppearanceGoods(TArray<FSTORE_GOODS_DATA_TABLE> GoodsList);
	void OnRequestPresentGift(FSTORE_GIFT_BOX SenderGift);
	void OnRequestOpenGiftBox(TArray <FSTORE_GIFT_BOX> SenderGiftList, TArray <FSTORE_GIFT_BOX> ReceiverGiftList);
	void OnUpdateRecommentGoods(const TArray<FSTORE_GOODS_DATA_TABLE> goodsList);
	void OnUpdateStoreNewGoods(const TArray<FSTORE_GOODS_DATA_TABLE> goodsList);

	FSTORE_GOODS_DATA_TABLE AnalysisStoreGoods(FSTOREGOODS Value);
	FSTORE_GIFT_BOX AnalysisGiftBox(FSTORE_GIFT_BOX_DATA data);
	FSTORE_PRESENT_RECORD_DATA AnalysisPresentRecord(FSTORE_PRESENT_RECORD data);
	FSTORE_BUY_RECORD_DATA AnalysisBuyRecord(FSTORE_BUY_RECORD data);
	/*设置购买记录*/
	void SetBuyRecords(TArray <FSTORE_BUY_RECORD_DATA> Records);
	/*设置赠送记录*/
	void SetPresentRecords(TArray <FSTORE_PRESENT_RECORD_DATA> Records);

	///读推荐商品表
	void InitRemommentConfigData();

	///初始商城商品表数据
	void InitStoreConfigData();
	///读客户端商品表（只有商品名和商品ID，目前只用于搜索）
	void InitStoreSearchConfigData();

	void ClearAllData();

	///增加拥有外观回调
	void OnAddHasStoreAppearance(const int32& ItemID);
	///穿上商城外观回调
	void OnAddStoreAppearance(const int32& ItemID);
	///脱掉商城外观回调
	void OnRemoveStoreAppearance(const int32& ItemID);
	///新增试穿外观
	void OnAddStoreTryAppearances(const int32& PartType, const int32& GoodsID);
	///移除试穿外观
	void OnRemoveStoreTryAppearances(const int32& PartType, const int32& GoodsID);
	///清除所有试穿外观
	void OnClearStoreTryAppearances();

public:
	UPROPERTY(BlueprintReadWrite, Category = "RoleStoreInterface")
		TArray<FSTORE_GOODS_DATA_TABLE> HomeRecommentGoods;   ///<首页推荐商品
	UPROPERTY(BlueprintReadWrite, Category = "RoleStoreInterface")
		int32 BuyLimitAmount = 99; ///<每次购买不限量商品的最大数量

private:
	TMap<int32, FString> NewGoodsConfigTime;         ///<新品商品配置时间
	TMap<int32, TMap<int32, FSTORE_GOODS_DATA_TABLE>> StoreCart;  ///<购物车 {购物车类型:{商品ID:商品}}

	TMap<int32, TMap<int32, FString>> ConfigTime;       ///<配置时间
	TMap<int32, TMap<int32, TArray<FSTORE_GOODS_DATA_TABLE>>> StoreGoodsListDatas; ///< 商城商品数据{商品类型：{物品类型：商品列表}}
	UPROPERTY()
		TMap<int32, FSTORE_GOODS_DATA_TABLE> StoreGoodsDatas;   ///< 商城商品数据 {商品ID：商品}
	UPROPERTY()
		TMap <FString, FSTORE_BUY_RECORD_DATA> BuyRecords;  ///<购买记录 {uid：购买记录}
	UPROPERTY()
		TMap <FString, FSTORE_PRESENT_RECORD_DATA> PresendRecords;  ///<赠送记录 {uid：赠送记录}
	UPROPERTY()
		TMap <FString, FSTORE_GIFT_BOX> SenderGiftBox;    ///<赠送礼品盒  {uid：礼品}
	UPROPERTY()
		TMap <FString, FSTORE_GIFT_BOX> ReceiverGiftBox;  ///<收取礼品盒  {uid：礼品}

	TMap<int32, FSTORE_GOODS_DATA_TABLE> AppearanceConfigDatas;///<商品外观表数据{商品ID:商品数据}
	TArray<int32> HomeRecommentGoodsIDs;///<首页推荐商品
	TArray<int32> RecommentGoodsIDs;///< 推荐页推荐商品
	TMap<int32, TArray<FSTORE_GOODS_DATA_TABLE>> RecommentGoods;   ///< 推荐页推荐商品，key为二级标签类型
	TArray<FSTORE_GOODS_DATA_TABLE> RecommentNewGoods;  ///< 推荐页新品
	TArray<FSTORE_SEARCH_DATA> StoreSearchConfigDatas;///<商品搜索表数据
	TMap<int32, FSTORE_GOODS_DATA_TABLE> StoreAppearancesDatas;   ///< 商城外观数据 {商品ID：商品}
	TArray<int32> HasStoreAppearances; ///<玩家已拥有的商城外观物品ID列表(使用后商城外观物品会从普通背包移除)
	TArray<int32> StoreAppearances; ///<玩家已穿上的商城外观物品ID列表
	TMap<int32, FSTORE_BACK_ADORN_PARAM> StoreBackAdornParam; ///<商城外观背饰的参数
	TMap<int32, int32> StoreTryAppearances; ///<玩家试穿的商城外观 {部件类型：商品ID}
};
