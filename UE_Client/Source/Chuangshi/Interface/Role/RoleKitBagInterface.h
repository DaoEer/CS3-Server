// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Util/CS3Debug.h"
#include "JsonObject.h"
#include <vector>
//#include "Entity/Role/Role.h"
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Item/ItemBase.h"
#include "GameData/Item/Equip.h"
#include "GameData/GameDeFine.h"
#include "GameData/KitBagGridCost.h"
#include "RoleKitBagInterface.generated.h"

/*
* 文件名称：RoleKitBagInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FKitBagEndSortDelegate);

UENUM(BlueprintType)
enum class FIND_BINDTYPE_ENUM :uint8
{
	///使用非绑定物品
	NONE_BIND = 0 UMETA(DisplayName = "NONE_BIND"),
	///使用绑定物品
	BIND = 5 UMETA(DisplayName = "BINDED"),
	///绑定和不绑定都可以用，优先使用绑定物品
	INGOREBIND = 6  UMETA(DisplayName = "BINDED_OR_NONE_BIND"),
};

UENUM()
enum class KB_LOCK_STATUS :uint8
{
	///背包无密码背包未锁定
	UNLOCK_KB_WITHOUT_PW = 0 UMETA(DisplayName = "UNLOCK_KB_WITHOUT_PW"),
	///背包有密码未锁定
	UNLICK_KB_WITH_PW = 1 UMETA(DisplayName = "UNLICK_KB_WITH_PW"),
	///背包有密码锁定
	LOCK_KB_WITH_PW = 2  UMETA(DisplayName = "LOCK_KB_WITH_PW"),
};

/**
*玩家背包接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleKitBagInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleKitBagInterface();
	~URoleKitBagInterface();
	static FString GetName() { return TEXT("RoleKitBagInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleKitBagInterface.BP_RoleKitBagInterface_C'"); } //获取蓝图对象路径

	virtual void onLeaveWorld() override;

	/*
	*设置背包物品初始化完成
	*/
	void kitbagInit(const FVariantArray& itemList);
	/********************************安全锁***************************************/
	/**
	*判断当前背包是否上锁
	*
	* @param ItemUID 物品UID
	*@return bool，当前背包上锁返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		bool isKBLocked(const FString& ItemUID);

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleKitBagInterface")
		void OnRep_kbLockStatus();///<背包锁状态变化时回调，蓝图实现

	/**
	*Define method
	*BlueprintImplementableEvent，服务器请求打开背包输入解锁密码的界面
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_openInputKBPW();///<服务器请求打开背包输入解锁密码的界面

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleKitBagInterface")
		void OnRep_resetKBPWStatus();///<重置背包锁的状态

	/********************************背包整理****************************************/

	/**
	*判断当前背包是否在整理
	*
	*@return bool，当前背包在整理返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		bool IsSort();

	/**
	*向服务器请求整理背包
	*
	*@param kbType 背包类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Client")
		void requestSortKitBag(int32 kbType);

	/**
	*开始整理背包
	*
	*@param kbType 背包类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Client")
		void startSort(int32 kbType);

	UFUNCTION(BlueprintCallable, Category = "Client")
		void CLIENT_endSort();	///<整理背包结束

	UPROPERTY(BlueprintAssignable, Category = "RoleKitBagInterface")
		FKitBagEndSortDelegate OnKitBagEndSort;///<BlueprintAssignable,整理背包结束事件

	/**
	*依据物品ID和绑定类型获取物品总数
	*
	*@param ItemID 物品ID
	*@param bindType 绑定类型
	*
	*@return int32 物品总数
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		int32 GetAmountByItemID(int32 ItemID, FIND_BINDTYPE_ENUM bindType);

	/**
	*依据背包类型、物品ID和绑定类型获取物品总数
	*
	*@param bagType 背包类型
	*@param ItemID 物品ID
	*@param bindType 绑定类型
	*
	*@return int32 物品总数
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		int32 GetAmountByKBType(EKITBAGTYPE bagType, int32 ItemID, FIND_BINDTYPE_ENUM bindType);

	/**
	*依据物品脚本获取物品列表
	*
	*@param ItemClass 物品脚本
	*
	*@return int32 物品总数
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		TArray<UItemBase*> GetItemListByItemScript(const FString& ItemScript);

	/**
	*判断当前是否能使用物品
	*
	*@param UID 物品UID
	*
	*@return bool，当前能使用物品返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		bool UseItem(const FString& UID);

	/**
	*根据物品order查找物品
	*
	*@param order 物品位置
	*
	*@return UItemBase* 物品
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		UItemBase* FindItemByOrder(int32 order);

	/**
	*根据物品order查找物品
	*
	*@param order 物品位置
	*
	*@return UItemBase* 物品
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		UItemBase* FindItemByUID(const FString& uid);

	/**
	*根据物品id查找物品
	*
	*@param itemid 物品id
	*
	*@return TArray<UItemBase*> 物品
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		TArray<UItemBase*> GetItemsByItemID(int32 itemid);

	/**
	*判断背包里是否有此ItemID的物品
	*
	*@param ItemID 物品id
	*
	*@return 背包里是否有此ItemID的物品
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		bool CheckIsOwnByItemID(int32 ItemID);

	/**
	*依据物品ID和是否绑定获取物品
	*
	*@param ItemID 物品ID
	*@param bIsBinded 是否绑定
	*
	*@return TArray<UItemBase*> 物品
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		TArray<UItemBase*> GetItemsByBindType(int32 itemid, bool bIsBinded);

	/**
	*依据背包类型获取物品
	*
	*@param bagType 背包类型
	*
	*@return TArray<UItemBase*> 物品
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		TArray<UItemBase*> GetItemsByKBType(EKITBAGTYPE bagType);

	/**
	*依据背包类型、物品ID和是否绑定获取物品
	*
	*@param bagType 背包类型
	*@param itemid 物品ID
	*@param bIsBinded 是否绑定
	*
	*@return TArray<UItemBase*> 物品
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		TArray<UItemBase*> GetItemsByKBTypeAndID(EKITBAGTYPE bagType, int32 itemid, bool bIsBinded);

	/**
	*依据物品ID获得背包中第一个同ItemID的物品的绝对ID
	*
	*@param ItemID 物品ID
	*
	*@return int32 物品的绝对ID
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		int32 GetAbsOrderIdByItemID(int32 ItemID);

	/**
	*优先选择空的戒指格子，如果两个格子都有物品，默认选择左手的戒指格子
	*
	*@return int32
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		int32 GetFreeRingOrder();

	/******************************解锁背包格子***************************************/

	/**
	*判断当前背包格子是否上锁
	*
	*@param absorder 背包格子
	*
	*@return bool，当前背包格子上锁返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		bool IsGridLocked(int32 absorder);

	/**
	*计算每个格子解锁的花费
	*
	*@param absorder 背包绝对位置
	*
	*@return int32，当前背包格子解锁花费
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface | UnLock")
		int32 CalcEachUnLockGridCost(int32 absorder);

	/**
	*计算所有格子解锁的花费
	*
	*@param absorder 背包绝对位置
	*@param unlockNum 解锁格子数量
	*
	*@return int32，所有格子解锁花费
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface | UnLock")
		int32 CalcSumUnLockGridCost(int32 absorder, int32& unlockNum);
	
	/// 玩家自己等级改变
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		void OnPlayerLevelChange(const int32& level);

	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void OnEquipHardinessPercentChanged(float HardinessPercentconst, const FString& UId, int32 ItemOrder);///<角色装备耐久度改变

	///< 通知界面更新图标状态
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleKitBagInterface")
		void OnItemCanUseStateChange(const FString& UID);

	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_OnUnLockStoreGridNumChange(const int32& unLockNum);

	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_OnStoreMoneyChange(const FString& money);

	/**
	*Define method
	*添加物品
	*
	*@param jsonstr 物品数据
	*
	*@return 无
	*/
	void addItem(const FVariant& FVariantItem, const uint8& reason );

	//void __addItem(struct FITEM_FOR_CLIENT itemStruct);
	void OnAddItem(UItemBase* ItemInst, const uint8& reason);

	/**
	*Define method
	*删除物品
	*
	*@param itemorder 物品位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_removeItem(int32 itemorder);

	/**
	*BlueprintCallable 向服务器请求删除物品
	*
	*@param UID 物品UID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Client")
		void RequestRemoveItem(FString UID);

	/**
	*BlueprintCallable 向服务器请求删除物品（玩家仓库和帮会仓库调这个方法）
	*
	*@param UID 物品UID
	*@param AbsOrder 格子绝对位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Client")
		void RequestRemoveStoreItem(FString UID, int32 AbsOrder );

	/**
	*Define method
	*BlueprintNativeEvent 设置格子是否置灰
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_OnSetGridEnabledByOrderID(const int32& itemOrder ,const int32& isEnable);

	/**
	*Define method
	*请求删除物品之后，服务器删除物品之前
	*
	*@param UID 物品UID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleKitBagInterface")
		void OnBeforeRemoveItemBP(const FString& UID);

	/**
	*Define method
	*交换物品
	*
	*@param srcorder 物品源位置
	*@param dstorder 物品目标位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_swapItemAC(int32 srcorder, int32 dstorder);
	/**
	*Define method
	*向服务器请求交换物品
	*
	*@param FromAbsOrder 物品移动前绝对位置
	*@param ToAbsOrder 物品移动目标绝对位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Client")
		void RequestSwapItem(int32 FromAbsOrder, int32 ToAbsOrder);
	/**
	*Define method
	*拆分物品
	*
	*@param UID 物品uid
	*@param Amount 拆分数量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Client")
		void splitItem(const FString& UID, const int32& Amount);
	/**
	*Define method
	*整理背包
	*
	*@param kbType 背包类型
	*@param oldorders 删除物品的位置
	*@param neworders 更新物品的位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_requestSortKitBagCB(int32 kbType, const TArray<int32>& oldorders, const TArray<int32>& neworders);

	/**
	*获取物品信息
	*
	*@param jsonstr 物品信息
	*@param itemid 物品id
	*@param itemorder 物品位置
	*@param amount 物品数量
	*@param bindtype 绑定类型
	*@param uid 物品UID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Server")
		void GetItemInfoByString(const FString& jsonstr, int32& itemid, int32& itemorder, int32& amount, int32& bindtype, FString& uid, FString& itemEndTime);

	/**
	*更新背包/装备/仓库等玩家身上的物品格
	*
	*@param uid 物品UID
	*@param absorder 物品位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Server")
		void UpdateGrid(const FString& uid, const int32& absorder);

	/**
	*获取根据动态属性获取物品
	*
	*@param type 物品类型
	*@param propertyname 属性名
	*@param propertyvalue 属性值
	*
	*@return UItemBase* 物品
	*/
	UFUNCTION(BlueprintCallable, Category = "Server")
		UItemBase* GetItemByDynamicProperty(FString& type, FString& propertyname, FString& propertyvalue);

	UFUNCTION(BlueprintCallable, Category = "Server")
		void OnRep_DynamicProperty();///<查询物品动态属性

	/**
	*使用物品设置CD，SkillManager中的UpdateSkillCoolDown调用
	*
	*@param SkillID 物品的技能ID
	*@param RemainningTime CD时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface | CD")
		void OnSetCooldown(int32 SkillID, float RemainningTime, float PersistTime);

	/**
	*通过SkillID获取物品
	*
	*@param SkillID 物品的技能ID
	*
	*@return TArray<UItemBase*> 物品
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface | CD")
		TArray<UItemBase*> GetItemListBySkillID(int32 SkillID);

	/**
	*刷新背包物品使用后CD
	*
	*@param uid 物品UID
	*@param absorder 物品位置
	*@param RemainningTime 物品CD时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface | CD")
		void UpdateGridUsingCD(const FString& uid, const int32& absorder, const float& RemainningTime, const float& PersistTime);

	/**
	*刷新物品使用后CD
	*
	*@param ItemID 物品ItemID
	*@param RemainningTime 物品CD时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleKitBagInterface | CD")
		void OnUpdateItemUsingCD(const int32& ItemID, const float& RemainningTime, const float& PersistTime);

	/**
	*物品删除后
	*
	*@param ItemID 物品ItemID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleKitBagInterface")
		void OnKitBagItemRemoved(const int32& ItemID);

	/**
	*更新快捷栏物品数量
	*
	*@param itemID 物品ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleKitBagInterface | QuickBar")
		void UpdateQBItemAmount(const int32& itemID);

	/// 判断是否是同一个脚本类型物品(用于更新装备强化物品的数量)
	UFUNCTION(BlueprintCallable)
		bool IsSameScriptType(const int32& srcItemID, const int32& dstItemID);

	/**
	*请求打开仓库界面
	*
	*@param npcID		npcID
	*@param unlockNum	解锁格子数量
	*@param money		存款
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleKitBagInterface")
		void CLIENT_requestOpenStoreWindow(const int32& npcID, const int32& unlockNum, const FString& money);

	/**
	*判断金钱是否足够
	*
	*@return bool
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleInterface")
		bool IsStoreMoneyEnough(int64 money);

	/**
	*计算列表中物品总数
	*
	*@param itemList 物品列表
	*
	*@return int32 物品总数
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		int32 GetAmountByItemList(TArray<UItemBase*> itemList);

	/**
	*获取背包物品的技能数据
	*
	*@return TArray<USkillData*> 技能数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		TArray<USkillData*>	GetItemSkillDataList();

	/**
	*通知蓝图整理结束进行处理
	*
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleKitBagInterface")
		void NotifyEndSort();

	/**
	*获取玩家身上同部位装备UIds
	*
	*@return TArray<FString>
	*/
	UFUNCTION(BlueprintPure, Category = "RoleKitBagInterface")
		TArray<FString> GetSamePartEquipUIds(const FString& EquipUId);
	/**
	*获取玩家身上同部位装备
	*
	*@return TArray<FString>
	*/
	UFUNCTION(BlueprintPure, Category = "RoleKitBagInterface")
		void GetSamePartEquipByItem(TArray<FString>& UIDArr, UEquip* Equip_);
	///<是不是相同的部位类型
	UFUNCTION(BlueprintPure, Category = "RoleKitBagInterface")
		bool IsSamePartType(MODEL_PART_TYPE SrcPartType, MODEL_PART_TYPE DstPartType);

	/**
	*增加物品使用限量的数据
	*
	*@param itemID 物品ID
	*@param number 物品剩余可使用数量
	*@param lastUseTime 最后使用改物品时间
	*
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		void CLIENT_AddToItemUseAmountArray(const int32 itemId,const int32 number,const FString createTime);

	/**
	*获得物品使用限量的数据
	*
	*return int32
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		int32 GetItemUseAmountByItemID(const int32 itemID);

	/**
	*获得物品最后使用时间
	*
	*return FString
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		FString GetItemUseCreateTimeByItemID(const int32 itemID);

	/**
	*更新物品可使用数量
	*
	*@param itemID 物品ID
	*@param number 物品剩余可使用数量
	*@param lastUseTime 最后使用改物品时间
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		void CLIENT_UpdateItemUseAmount(const int32 itemId, const int32 number, const FString newRefreshTime);

	/**
	*更新物品可使用数量
	*
	*@param BagType 背包类型
	*@param number 物品剩余可使用数量
	*@return bool 某种类型的背包是否已经满
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		bool IsBagFull(EKITBAGTYPE BagType);

	// 使用指向性物品回调
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		void OnUseItemByPos(FString UID, FVector Pos);

	// 使用指向性物品回调
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		void OnUseItemByPosAndDir(FString UID, FVector Pos, FVector Dir);

	/**
	*显示下个等级的等级礼包
	*@param ReqLevel 需要等级
	*@param GiftItemIDs 礼包物品ID
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleKitBagInterface")
		void CLIENT_ShowNextLevelGift(const int32& ReqLevel, const TArray<int32>& GiftItemIDs, const TArray<int32>& GiftItemAmounts);
	/**
	*显示可以领取的等级礼包
	*@param ItemUID 礼包UID
	*@param GiftItemIDs 礼包物品ID
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleKitBagInterface")
		void CLIENT_ShowLevelGift(const FString& ItemUID, const TArray<int32>& GiftItemIDs, const TArray<int32>& GiftItemAmounts);
	// 领取等级礼包
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		void UseLevelGiftItem(const FString& UID);
	// 等级礼包中的物品排序，品质>装备>药品>道具>礼包 
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		void SortLevelGiftItem(TArray<int32> GiftItemIDs, TArray<int32> GiftItemAmounts, TArray<int32>& NewGiftItemIDs, TArray<int32>& NewGiftItemAmounts);
	/**
	*将物品置灰，不能使用
	*@param ItemID 物品ID
	*
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleKitBagInterface")
		void CLIENT_GreyItem(const int32& ItemID);
	/**
	*将置灰物品还原
	*@param ItemID 物品ID
	*
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleKitBagInterface")
		void CLIENT_ClearGreyItem(const int32& ItemID);
	/**
	*显示获得物品提示
	*@param ItemID 物品UID
	*
	*/
	void CLIENT_ShowItemListIcon(const FVariant& dictStrInt);

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleKitBagInterface")
		void OnShowItemListIcon(const TMap<FString, int32>& mapValue);


	/**
	*BlueprintCallable，超链接获取物品ItemBase，用于Tips显示
	*
	*@param  FString dataString 物品动态属性数据
	*
	*@return ItemBase
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		UItemBase* getItemByHyperLinkString(const FString& dataString);

	// 一键获取所有可熔炼装备UID
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void GetMeltingEquipUID(TArray<FString>& EquipUIDArr);
	// 判断物品是否可熔炼
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		bool CheckMelting(UItemBase* ItemBase);

#pragma region 个人仓库
	/// 仓库添加物品
	void addStoreItem( const FVariant& FVariantItem );

	/// 仓库移除物品
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_removeStoreItem(const int32& itemorder);

	/// 仓库交换物品(只执行仓库之间交换，不支持仓库背包之间交换)
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_swapStoreItemAC(const int32& srcorder, const int32& dstorder);

	/// 背包与仓库交换物品
	///@param srcorder 背包索引
	///@param dstorder 仓库索引
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_swapItemFromBagToStore(const int32& srcorder, const int32& dstorder);

	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		UItemBase* FindStoreItemByUID(const FString& uid);

#pragma endregion

#pragma region 帮会仓库
	/// 帮会仓库添加物品
	void updateTongStoreItem(const FVariant& FVariantItem);

	/// 帮会仓库移除物品
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_removeTongStoreItem(const int32& itemorder);

	/// 帮会仓库交换物品(只执行仓库之间交换，不支持仓库背包之间交换)
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_swapTongStoreItemAC(const int32& srcorder, const int32& dstorder);

	/// 背包与帮会仓库交换物品
	///@param srcorder 背包索引
	///@param dstorder 仓库索引
	UFUNCTION(BlueprintNativeEvent, Category = "Server")
		void CLIENT_swapItemFromBagToTongStore(const int32& srcorder, const int32& dstorder);

	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		UItemBase* FindTongStoreItemByUID(const FString& uid);

	void UseSpaceCopyItemByQuickKey(const int32& index);

#pragma endregion

	virtual void InitBlueCB() override;

public:
	bool _CheckSwapOrder(const int32& FromAbsOrder, const int32&  ToAbsOrder, UItemBase* FromItem, UItemBase* ToItem);
	void _RequestSwapItem(const int32& FromAbsOrder, const int32&  ToAbsOrder);
	
private:
	//获得物品提示
	void ShowAddItemAction(UItemBase* ItemInst, const uint8& reason);

//Exposed调用
public:
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_unLockStoreGrid();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestRemoveStoreItem(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_splitStoreItem(const int32& INT32_1, const int32& INT32_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_swapItem(const FString& STRING_1, const FString& STRING_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_unWieldEquip(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestRemoveItemByUID(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_useItem(const FString& STRING_1, const FString& STRING_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_uesItemByShortcutBar(const int32& ItemID, const int32& TargetID);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_unLockGrid();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestSortKitBag(const int32& INT32_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requsetSetPW(const FString& STRING_1, const FString& STRING_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_unLockKB(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_cancelKBPW(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_resetKBPW();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_cancelResetKBPW();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_LockKB();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestSaveMoney(const int64& MoneyValue);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestTakeMoney(const int64& MoneyValue);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestSaveItem(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestTakeItem(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_swapStoreItem(const FString& STRING_1, const FString& STRING_2);

	/**获取背包解锁格子消耗
	* Return FKITBAG_GRID_COST 格子消耗配置
	* Return GridIndex 第N个格子位
	*/
	UFUNCTION(BlueprintPure, Category = "KitBag")
		FKITBAG_GRID_COST GetKitBagGridCost(int32& GridIndex);
	
	/**获取仓库解锁格子消耗
	* Return FKITBAG_GRID_COST 格子消耗配置
	* Return GridIndex 第N个格子位
	*/
	UFUNCTION(BlueprintPure, Category = "Store")
		FKITBAG_GRID_COST GetStoreGridCost(int32& GridIndex);

public:	
	UPROPERTY(EditAnywhere)
		FString DynamicProperty;///<为了更新物品属性定义的临时变量，临时数据。type_ + "|#|" + uid + "|#|" + propertyname[0].upper() + propertyname[1:]  + "|#|" + str(propertyvalue)

	UPROPERTY(BlueprintReadOnly)
		int32 commonCapacity;///<普通背包默认开启的格子
	
	UPROPERTY(BlueprintReadOnly)
		int32 questCapacity; ///<任务背包容量

	UPROPERTY(BlueprintReadOnly)
		int32 crystalCapacity;///<晶石背包容量

	UPROPERTY(BlueprintReadOnly)
		int32 canUnLockCapacity;///<普通背包可以开启默认锁定的格子

	UPROPERTY(BlueprintReadOnly)
		int32 storeCapacity;///<仓库容量
	UPROPERTY(BlueprintReadOnly)
		int32 canUnLockStoreCapacity;///<仓库可以开启100个默认锁定的格子
	UPROPERTY(BlueprintReadOnly)
		int32 unLockStoreGridNum;	///<已经解锁的仓库格子数量
	UPROPERTY(BlueprintReadOnly)
		int64 StoreMoney;

	UPROPERTY(BlueprintReadOnly)
		int32 toolCapacity;///<轮回秘境 工具打造储物柜
	UPROPERTY(BlueprintReadOnly)
		int32 canUnLockToolCapacity;///<储物柜可以开启70个默认锁定的格子
	UPROPERTY(BlueprintReadOnly)
		int32 unLockToolGridNum;	///<已经解锁的 工具储物柜 格子数量
	UPROPERTY(BlueprintReadOnly)
		int32 tripodeCapacity;///<轮回秘境 乾坤鼎打造储物柜
	UPROPERTY(BlueprintReadOnly)
		int32 unLockTripodGridNum;	///<已经解锁的 乾坤鼎储物柜 格子数量

	UPROPERTY(BlueprintReadOnly)
		int32 kbLockStatus;///<背包锁状态
	
	UPROPERTY(BlueprintReadOnly)
		int32 resetKBPWStatus;///<背包密码重置状态，0表示未重置，1表示重置中

	UPROPERTY(BlueprintReadOnly)
		bool bIsSort;	///<整理状态
	UPROPERTY(BlueprintReadOnly)
		bool initKitBag;  ///背包初始化状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleKitBagInterface")
		TArray<UItemBase*> FKB_ItemList; ///<物品列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleKitBagInterface")
		TArray<UItemBase*> StoreItemList; ///<仓库列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleKitBagInterface")
		TArray<UItemBase*> TongStoreItemList; ///<帮会仓库列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleKitBagInterface")
		TArray<UItemBase*> ToolStoreItemList; ///<工具打造储物柜
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleKitBagInterface")
		TArray<UItemBase*> TripodStoreItemList; ///<乾坤鼎打造储物柜
	
	UPROPERTY(BlueprintReadOnly)
		int32 unLockGridNum;///<已经解锁的普通背包格子数量（最大100）

	UPROPERTY(BlueprintReadOnly)
		TArray<FItemUseAmountInfo> ItemUseAmountArray;///<物品剩余使用次数

};
