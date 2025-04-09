// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Item/ItemBase.h"
#include "GameData/AuctionCfgData.h"
#include "GameData/AuctionDefineData.h"
#include "GameData/GameDeFine.h"
#include "RoleDropBoxInterface.generated.h"

/*
* 文件名称：RoleDropBoxInterface.h
* 功能说明：
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2018-04-20
*/

///掷点
UCLASS(BlueprintType)
class CHUANGSHI_API URollDomData : public UCS3Object
{
	GENERATED_BODY()
public:
	///< 物品uid
	UPROPERTY(BlueprintReadOnly)
		FString uid;

	///< 所有者dbid（掷点数最大且获得了该物品的玩家）默认为0
	UPROPERTY(BlueprintReadOnly)
		FString ownerDBID;

	///< 物品是否已分配（0：否 1：是）
	UPROPERTY(BlueprintReadOnly)
		uint8 isPickUp;

	///< 当前掷点数最大的玩家dbid 默认为0
	UPROPERTY(BlueprintReadOnly)
		FString maxRollDBID;

	///< 最大掷点数 默认为-1未掷点
	UPROPERTY(BlueprintReadOnly)
		int32 maxRoll;

	///< 玩家自己的掷点数 -1:未掷点 0：已放弃掷点
	UPROPERTY(BlueprintReadOnly)
		int32 selfRoll;
};

UCLASS(BlueprintType)
class CHUANGSHI_API UDropBoxData : public UCS3Object
{
	GENERATED_BODY()
public:
	///< 宝箱id
	UPROPERTY(BlueprintReadOnly)
		int32 id;

	///< entityExtFlag
	UPROPERTY(BlueprintReadOnly)
		uint8 entityExtFlag;

	///< 分配方式
	UPROPERTY(BlueprintReadOnly)
		uint8 allocation;

	///< 所有玩家信息{dbid:name}
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, FString> owners;

	///< 物品（包括已分配和未分配的）
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, UItemBase*> items;

	///< 掷点分配数据（所有还未掷点的话，为空，这里只要有玩家掷点了都会往里面存数据）
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, URollDomData*> rollDomItems;

	///< 竞拍分配数据
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, UAuctionData*> auctionItems;

	///< 竞拍顺序列表[uid,uid...]
	UPROPERTY(BlueprintReadOnly)
		TArray<FString> pickupList;

	///< 倒计时(结束时间)
	UPROPERTY(BlueprintReadOnly)
		FString countDown;

	///< 持续时间
	UPROPERTY(BlueprintReadOnly)
		float HoldTime = 120.0;
public:
	UFUNCTION(BlueprintCallable, Category = "UDropBoxData")
	//是否是帮会宝箱
	bool isTongDropBox()
	{
		return ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_TONG_DROPBOX == (ENTITY_TYPE_EXT)entityExtFlag;
	}
	UFUNCTION(BlueprintCallable, Category = "UDropBoxData")
	bool isTeamDropBox()
	{
		return ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_TEAM_DROPBOX == (ENTITY_TYPE_EXT)entityExtFlag;
	}

	UFUNCTION(BlueprintCallable, Category = "UDropBoxData")
	bool isRalldomPickUp()
	{
		if (isTongDropBox())
			return TONG_PICKUP_TYPE::TONG_PICKUP_TYPE_RALLDOM == (TONG_PICKUP_TYPE)allocation;
		if(isTeamDropBox())
			return TEAM_PICKUP_TYPE::TEAM_PICKUP_TYPE_TEAM == (TEAM_PICKUP_TYPE)allocation;
		return false;
	}

	UFUNCTION(BlueprintCallable, Category = "UDropBoxData")
	bool isAuctionPickUp()
	{
		if (isTongDropBox())
			return TONG_PICKUP_TYPE::TONG_PICKUP_TYPE_AUCTION == (TONG_PICKUP_TYPE)allocation;
		if (isTeamDropBox())
			return TEAM_PICKUP_TYPE::TEAM_PICKUP_TYPE_AUCTION == (TEAM_PICKUP_TYPE)allocation;
		return false;
	}

	///当前自身是否能掷点/竞拍该物品
	UFUNCTION(BlueprintCallable, Category = "UDropBoxData")
	bool isCanSelfPickup(const FString& uid)
	{
		if (isRalldomPickUp())
		{
			if (!rollDomItems.Contains(uid))
				return true;

			if ((rollDomItems[uid]->isPickUp <= 0 && rollDomItems[uid]->selfRoll < 0))
				return true;

			return false;
		}

		if (isAuctionPickUp())
		{
			if (!auctionItems.Contains(uid))
				return true;

			///未竞拍完毕 或者 自己未放弃竞拍
			if (auctionItems[uid]->isPickUp <= 0 && auctionItems[uid]->selfMoney != 0)
				return true;

			return false;
		}
		return false;
	}

	///当前是否能掷点/竞拍该物品
	UFUNCTION(BlueprintCallable, Category = "UDropBoxData")
	bool isCanPickup(const FString& uid)
	{
		if (isRalldomPickUp())
		{
			if (!rollDomItems.Contains(uid))
				return true;

			if (rollDomItems[uid]->isPickUp <= 0)
				return true;

			return false;
		}

		if (isAuctionPickUp())
		{
			if (!auctionItems.Contains(uid))
				return true;

			///未竞拍完毕
			if (auctionItems[uid]->isPickUp <= 0)
				return true;

			return false;
		}
		return false;
	}

	///当前箱子中的物品是否都被分配了
	UFUNCTION(BlueprintCallable, Category = "UDropBoxData")
	bool isAllPickup()
	{
		for (auto It = items.CreateConstIterator(); It; ++It)
		{
			if (isCanPickup(It->Key))
				return false;
		}
		return true;
	}
};

/**
 * 玩家掉落接口类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleDropBoxInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleDropBoxInterface();
	~URoleDropBoxInterface();
	static FString GetName() { return TEXT("RoleDropBoxInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleDropBoxInterface.BP_RoleDropBoxInterface_C'"); } //获取蓝图对象路径


	/**
	*BlueprintCallable,发送掉落物品列表数据到客户端
	*
	*@param dropBoxEntityID: DropBox Entity的ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void ReqSendItemInfoListToClient(int32 dropBoxEntityID);

	/**
	*BlueprintCallable,拾取物品请求
	*
	*@param dropBoxEntityID: DropBox Entity的ID
	*@param ItemUIdList 物品uid List
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void ReqPickUp(int32 dropBoxEntityID, const TArray<FString>& ItemUIdList);

	/**
	*BlueprintCallable,客户端请求服务器掷筛子
	*
	*@param dropBoxEntityID: DropBox Entity的ID
	*@param ItemUId 物品uid
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void RollRandomFC(int32 dropBoxEntityID, const FString ItemUId);

	/**
	*BlueprintCallable,客户端请求放弃参与掷骰子
	*
	*@param dropBoxEntityID: DropBox Entity的ID
	*@param ItemUId 物品uid
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void AbandonRollFC(int32 dropBoxEntityID, const FString ItemUId);

	/**
	*BlueprintCallable,队长分配模式下，客户端请求将物品分配给某个队友
	*
	*@param dropBoxEntityID: DropBox Entity的ID
	*@param ItemUId 物品uid
	*@param DstEntityID 将得到物品的玩家的entityId
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void PickUpToMemberFC(int32 dropBoxEntityID, const FString ItemUId, const int32 DstEntityID);

	/**
	* Define method
	* BlueprintNativeEvent，点击掉落宝箱服务器回调给客户端拾取物品信息列表
	*
	* @param dropBoxEntityID: DropBox Entity的ID
	* @param JsonStr JSON打包的物品信息数据
	*
	* @return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
	void FPickup_GetItemInfoList(const int32 dropBoxEntityID, const FVariant& JsonStr);

	///<点击宝箱Actor打开宝箱回调通知蓝图显示拾取界面
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleDropBox")
		void BP_OnGetItemInfoList(int32 dropBoxEntityID);

	/**
	* Define method
	* BlueprintNativeEvent，拾取结果服务器回调
	*
	* @param dropBoxEntityID: DropBox Entity的ID
	* @param IsSuccess 是否拾取成功（0:失败，1:成功；）
	* @param UId 拾取物品的UID
	* @param LeftAmount 拾取过后宝箱剩余某个物品数量（比如：宝箱里面有某个物品A数量5个，背包能放下3个，拾取过后剩余LeftAmount就是2）
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
		void PickUp(int32 dropBoxEntityID, int32 IsSuccess, const FString& UId, int32 LeftAmount);

	/**
	* Define method
	* BlueprintNativeEvent，服务器通知所有具有奖励权的玩家客户端弹出掷骰子界面（队伍拾取才有）
	*
	* @param dropBoxEntityID: DropBox Entity的ID
	* @param UId 拾取物品的UID
	* @param ItemID 拾取物品的ID
	* @param RollRemainTime 筛子剩余时间
	*
	* @return 无
	*/
	void FRollRandom(int32 dropBoxEntityID, const FString& UId, const FVariant& FVariantItem, int32 RollRemainTime);
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleDropBox")
		void OnFRollRandom(int32 dropBoxEntityID, const FString& UId, int32 itemID, int32 RollRemainTime);
	/**
	* Define method
	* BlueprintNativeEvent，掷骰子结束服务器通知返回掷骰子结果
	*
	* @param dropBoxEntityID: DropBox Entity的ID
	* @param UId 拾取物品的UID
	* @param ItemID 拾取物品的ID
	* @param Result 结果（0:没有获得物品，1:获得物品）
	* @param LeftAmount 拾取过后宝箱剩余某个物品数量（比如：宝箱里面有某个物品A数量5个，背包能放下3个，拾取过后剩余LeftAmount就是2）
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
		void receiverRollResult(int32 dropBoxEntityID, const FString& UId, int32 ItemID, int32 Result, int32 LeftAmount);

	/**
	* Define method
	* BlueprintNativeEvent，点击掉落宝箱服务器回调给客户端拾取物品信息列表（队长分配模式下用的）
	*
	* @param dropBoxEntityID: DropBox Entity的ID
	* @param UId 拾取物品的UID
	* @param JsonStr 拥有该物品奖励权的玩家ID列表
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
		void pickUpToMember(int32 dropBoxEntityID, const FString& UId, const FString& JsonStr);

	///< 将拾取物品JSON打包的数据解析成物品信息数据ItemBase，服务器打包结构{"ROOT":[{"id":"10", "uid":12,"amount":"1", "bindType":"1", "icon":"T_Icon_0001_D", "name": "AA", "quality":"1"},{},....]}
	///UFUNCTION(BlueprintPure, Category = "RoleDropBox")
	TArray<UItemBase*> AnalyzePickUpItemJsonStr(const FVariant& variant);

	///< 判断UID在不在拾取物品列表里面
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		bool HasUIdInPKItemList(const FString& UId);

	///<更新拾取物品信息列表（UId：拾取物品的UID，LeftAmount：拾取过后宝箱剩余某个物品数量）
	void UpdatePKItemList(const FString& UId, int32 LeftAmount);

	///< 清空拾取物品Item列表及打开的宝箱的EntityID（关闭拾取界面的时候会关闭宝箱并重置数据）
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void ClearPickUpData();

	///< 宝箱Entity销毁调用，在Entity的OnLeaveWord的时候调(服务器Entity销毁，客户端Entity首先走了OnLeaveWorld（方法里面做了UnBindActorToEntity把Actor的EntityID置0，所以不能在Actor销毁事件后面传ID过来）然后是Entity析构函数)；
	void OnDropBoxDestroyed(int32 dropBoxEntityID);

	///< 宝箱销毁回调（通知蓝图关闭拾取界面）
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleDropBox")
	void BP_OnDropBoxDestroyed(int32 dropBoxEntityID);

	///全部拾取CST-5235
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void GetAllPickUp();

	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		UItemBase* FindBoxItemByUID(const FString& uid);

	/**
	*BlueprintNativeEvent 宝箱出现时飞行接口
	*
	*@param dropBoxEntityID 宝箱ID
	*@param InStartPosition 起始位置
	*@param InEndPosition 目标位置
	*@param XMoveSpeed 水平移动速度
	*@param Scale 模型最终大小
	*@param Gravity 重力加速度，影响抛物线的弧度，加速度越大，弧度越高
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
		void CLIENT_dropBoxMoveToPoint(const int32& dropBoxEntityID, const FVector& InStartPosition, const FVector& InEndPosition, float XMoveSpeed, float Scale, float Gravity, const FString& DragActionID, const FString& levitateActionID);
	
	virtual void onEnterWorld();
	virtual void onLeaveWorld();

	virtual void InitBlueCB() override;


	//---------------------------------------帮会宝箱(掷点/竞拍) -------------------------------------------------------------------------------------
	///获取到宝箱基础数据(宝箱ID、分配方式、宝箱类型、拥有分配权限的玩家信息、宝箱中的物品)
	void recvDropBoxData(const int32& dropBoxID, const uint8& entityExtFlag, const uint8& allocation, const FVariant& owners, const FVariantArray& items);
	///初始化宝箱掷点数据(各个物品掷点情况、倒计时)
	void recvDropBoxRalldomData(const int32& dropBoxID, const FVariantArray& items, const FString& countDown);
	///初始化宝箱竞拍数据(各个物品竞拍情况、倒计时)
	void recvDropBoxAuctionData(const int32& dropBoxID, const FVariantArray& items, const FVariantArray& pickupList, const FString& countDown);
	TArray<UItemBase*> AnalyzeItemData(const FVariantArray& variant);
	/**
	*BlueprintNativeEvent 获取掷点分配宝箱物品数
	*
	*@param InDropBoxID 宝箱ID
	*@param OutEndTime 输出掷点结束时间
	*@param OutNoRollItems 宝箱内玩家未掷点的物品
	*@param OutHasPickItems 宝箱内已经分配的物品
	*@param OutHasRollNoPickItems 宝箱内玩家已掷点未分配的物品
	*
	*@return 是否找到物品数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		bool GetRollRandomDropBox(int32 InDropBoxID, float& OutHoldTime, FString& OutEndTime, TArray<UItemBase*>& OutNoRollItems, TArray<UItemBase*>& OutHasPickItems, TArray<UItemBase*>& OutHasRollNoPickItems);
	///获取宝箱物品掷点数据
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		URollDomData* GetRollDomData(int32 InDropBoxID, const FString& InUId);

	///请求掷点分配宝箱物品
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void ReqRollRandomDropBox(const int32& dropBoxID, const FString& uid);
	///放弃掷点
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void ReqAbandomRollRandomDropBox(const int32& dropBoxID, const FString& uid);
	///掷点 (放弃掷点也走这接口，只不过roll = 0)
	UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
		void onRollRandomDropBox(const int32& dropBoxID, const FString& uid, const FString& dbid, const int32& roll);
	///玩家掷点出当前最大点数(当有人掷出了最大点数就会通知)
	UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
		void onRollRandomMaxDropBox(const int32& dropBoxID, const FString& uid, const FString& dbid, const int32& roll);


	///请求竞拍宝箱物品(出价)
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void ReqAuctionDropBox(const int32& dropBoxID, const FString& uid, const int32& money);
	///出价结果
	UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
		void onAuctionDropBox(const int32& dropBoxID, const FString& uid, const int32& money, const FString& dbid, const int32&curAuctionRoleAmount, const int32& round,  const FString& countDown);
	///放弃竞拍宝箱物品(放弃出价)
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void ReqAbandomAuctionDropBox(const int32& dropBoxID, const FString& uid);
	///放弃竞价结果
	UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
		void onAbandomAuctionDropBox(const int32& dropBoxID, const FString& uid, const FString& dbid, const int32&curAuctionRoleAmount);
	///放弃竞拍所有宝箱物品(放弃出价)
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void ReqAbandomAuctionAllDropBox();
	//物品竞拍结束(更新竞拍列表和倒计时)
	void onDropBoxAuctionItemEnd(const int32& dropBoxID, const FString& uid, const FVariantArray& pickupList, const FString& countDown);
	//请求竞拍历史数据
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		void ReqAuctionHistoryData();
	//收到竞拍历史数据
	void recvAuctionHistoryData(const FVariantArray& datas);
	//更新历史数据
	void updateAuctionHistoryData(const FVariant& data);
	//物品竞拍结束(更新竞拍列表和倒计时)
	void onStartAuction(const int32& dropBoxID, const FVariantArray& pickupList, const FString& countDown);


	///竞拍/掷点 分配到物品
	UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
		void onPickupItemToRole(const int32& dropBoxID, const FString& uid, const FString& dbid, const int32& targetID);
	///移除箱子（竞拍/掷点结束）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleDropBox")
		void onPickUpDropBoxEnd(int32 dropBoxID);
	
	/* 竞价物品UID列表是否还有物品可竞拍（没有被分配&&自己没有放弃）
	*@param DropBoxType 宝箱类型：0帮会宝箱，1队伍宝箱
	*/
	UFUNCTION(BlueprintPure, Category = "RoleDropBox")
		bool HasCanAuctionItem(int32 DropBoxType);
	///竞价物品UID列表
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		TArray<FString> GetAuctionItems(int32 dropBoxID);
	///获取竞价物品ItemBase
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		UItemBase* FindAuctionItemByUID(int32 dropBoxID, FString UID);
	///根据UID获取竞价物品数据
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		UAuctionData* GetAuctionData(int32 dropBoxID, FString UID);
	///根据DBID获取玩家名字
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		FString GetAuctionPlayerName(int32 dropBoxID, FString DBID);
	///获取最低出价
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		int32 GetMinBidPrice(int32 dropBoxID, FString UID);
	///获取掉落每轮竞拍的相关参数配置
	UFUNCTION(BlueprintCallable, Category = "RoleDropBox")
		FAUCTIONCFG_DATA GetAuctionCfg(int32 Round);

	void FlyTargerOverEvent();//飞行光效到达目标点通知

private:
	//---------------------------------------宝箱竞拍 -------------------------------------------------------------------------------------
	///初始化宝箱竞拍数据(各个物品竞拍情况、倒计时)
	void OnRecvDropBoxAuctionData(const int32& dropBoxID);
	///出价结果
	void OnAuctionBidPrice(const int32& dropBoxID, const FString& uid, const int32& money, const FString& dbid, const FString& countDown, const FAUCTIONMESSAGE& MessageData);
	///放弃竞价结果
	void OnAbandomAuctionItem(const int32& dropBoxID, const FString& uid, const FString& dbid, const FAUCTIONMESSAGE& MessageData);
	///物品竞拍结束(更新竞拍列表和倒计时)
	void OnAuctionItemEnd(const int32& dropBoxID, const FString& uid);
	///打开竞拍界面
	void OnShowAuctionWindow(const int32& dropBoxID);
	//---------------------------------------宝箱竞拍end ----------------------------------------------------------------------------------

public:
		//宝箱物品的动态属性数据
		UPROPERTY(EditAnywhere, Category = "RoleDropBox")
			FString DropBoxDyProperty;
		///<当前打开的宝箱的拾取物品列表
		UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleDropBox")
			TArray<UItemBase*> FPK_ItemList;

		///<当前打开的宝箱的EntityID（只有点击宝箱请求宝箱数据回调给客户端的时候才设置，宝箱生成的时候请求回调不需设置）
		UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleDropBox")
			int32 DropBoxID;

		///<正在进行掷骰子的物品({uid:物品})（注意：掷骰子的物品对应的宝箱ID不一定是DropBoxID（当前打开的宝箱的EntityID））
		UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleDropBox")
			TMap<FString, UItemBase*> FPK_RollItemUidDict;
		
		///宝箱数据(帮会宝箱/队伍宝箱)
		UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleDropBox")
			TMap<int32, UDropBoxData*> dropBoxs;

		///宝箱ID列表(理论上只有队伍才有可能同时出现多个宝箱，帮会如果出现那可能有问题了)
		///如果既存在队伍宝箱，又存在帮会宝箱，竞拍界面怎么显示？
		///如果两个帮会宝箱竞拍中只有部分人员重合，竞拍界面怎么显示？
		UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleDropBox")
			TArray<int32> dropBoxIDList;

		///竞拍历史数据
		UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleDropBox")
			TArray<UAuctionHistroy*> auctionHistory;

	private:
		bool isBagFull;											// 普通背包和晶核背包是否已满
		FDelegateHandle MoveHandle;
};
