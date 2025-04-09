// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/AuctionDefineData.h"
#include "PublicDelegateObject.generated.h"

/**
 * 公共委托声明对象
 */

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnOpenTestWindow, int32, isOpen);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAddHasStoreAppearance, int32, ItemID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAddStoreAppearance, int32, ItemID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRemoveStoreAppearance, int32, ItemID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAddStoreTryAppearance, int32, PartType, int32, GoodsID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnRemoveStoreTryAppearance, int32, PartType, int32, GoodsID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnClearStoreTryAppearance);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnShowStartBillingWnd, int32, Level, int32, CountDownTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnHideStartBillingWnd);
//----竞价分配
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnOpenAuctionPickWnd, int32, DropBoxType, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnCloseAuctionPickWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAddDropBoxAuction, int32, DropBoxType, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_FiveParams(FOnAuctionBid, int32, DropBoxID, FString, UID, int32, Money, FString, PlayerDBID, FString, CountDownTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnAuctionAbandon, int32, DropBoxID, FString, UID, FString, PlayerDBID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAuctionItemEnd, int32, DropBoxID, FString, UID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnAddAuctionMessage, int32, DropBoxID, FString, UID, FAUCTIONMESSAGE, AuctionMessage);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnRecvAuctionHistoryData);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAddAuctionHistory, UAuctionHistroy*, AuctionHistroy);
//----竞价分配end
//----拾取
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnTongUpdatePickUpWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnTeamUpdatePickUpWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPickUpSuccessed, int32, DropBoxID, const FString&, ItemUid);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnClosedPickUpWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnUpdateTeamDicePickWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnClosedTeamDicePickWnd);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnTeamRollPickupResult, int32, DropBoxID, const FString&, ItemUid, int32, Result);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnUpdateTeamPickWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnClosedTeamPickWnd, int32, DropBoxID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPickUpByCaptainSuccessed, const FString&, uid, const FString&, playerName);
//----拾取end
//----多人载具
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSetDismountVehicleVisibility, bool, IsVisibility);
//----多人载具end
UCLASS()
class CHUANGSHI_API UPublicDelegateObject : public UCS3Object
{
	GENERATED_BODY()
public:
#pragma region	/** gm打开某个界面的通知事件 */
	//打开淬炼界面
	UPROPERTY(BlueprintAssignable, Category = "GM|TestWindow")
		FOnOpenTestWindow OnOpenTestWindowByGM;
#pragma endregion

#pragma region	/** 拾取界面的通知事件 */
	//帮会更新自由拾取界面
	UPROPERTY(BlueprintAssignable, Category = "Allocation|Tong|PickupWnd")
		FOnTongUpdatePickUpWnd OnTongUpdatePickUpWnd;
	//队伍更新自由拾取界面
	UPROPERTY(BlueprintAssignable, Category = "Allocation|Team|PickupWnd")
		FOnTeamUpdatePickUpWnd OnTeamUpdatePickUpWnd;
	//自由拾取成功
	UPROPERTY(BlueprintAssignable, Category = "Allocation|Team|PickupWnd")
		FOnPickUpSuccessed OnPickUpSuccessed;
	//关闭拾取界面
	UPROPERTY(BlueprintAssignable, Category = "Allocation|PickupWnd")
		FOnClosedPickUpWnd OnClosedPickUpWnd;
	//更新队伍掷点拾取界面
	UPROPERTY(BlueprintAssignable, Category = "Allocation|Team|DicePickupWnd")
		FOnUpdateTeamDicePickWnd OnUpdateTeamDicePickWnd;
	//关闭队伍掷点拾取界面
	UPROPERTY(BlueprintAssignable, Category = "Allocation|Team|DicePickupWnd")
		FOnClosedTeamDicePickWnd OnClosedTeamDicePickWnd;
	//队伍掷点物品最终分配通知
	UPROPERTY(BlueprintAssignable, Category = "Allocation|Team|DicePickupWnd")
		FOnTeamRollPickupResult OnTeamRollPickupResult;
	//更新队长分配界面数据
	UPROPERTY(BlueprintAssignable, Category = "Allocation|Team|TeamPickWnd")
		FOnUpdateTeamPickWnd OnUpdateTeamPickWnd;
	//关闭队长分配界面
	UPROPERTY(BlueprintAssignable, Category = "Allocation|Team|TeamPickWnd")
		FOnClosedTeamPickWnd OnClosedTeamPickWnd;
	//队长分配成功
	UPROPERTY(BlueprintAssignable, Category = "Tong|Allocation")
		FOnPickUpByCaptainSuccessed OnPickUpByCaptainSuccessed;
#pragma endregion

#pragma region	/** 商城 */
	//增加拥有外观
	UPROPERTY(BlueprintAssignable, Category = "AppearMall")
		FOnAddHasStoreAppearance OnAddHasStoreAppearance;
	//穿戴商城外观
	UPROPERTY(BlueprintAssignable, Category = "AppearMall")
		FOnAddStoreAppearance OnAddStoreAppearance;
	//脱掉商城外观
	UPROPERTY(BlueprintAssignable, Category = "AppearMall")
		FOnRemoveStoreAppearance OnRemoveStoreAppearance;
	//试穿商城外观
	UPROPERTY(BlueprintAssignable, Category = "AppearMall")
		FOnAddStoreTryAppearance OnAddStoreTryAppearance;
	//取消试穿商城外观
	UPROPERTY(BlueprintAssignable, Category = "AppearMall")
		FOnRemoveStoreTryAppearance OnRemoveStoreTryAppearance;
	//取消所有试穿商城外观
	UPROPERTY(BlueprintAssignable, Category = "AppearMall")
		FOnClearStoreTryAppearance OnClearStoreTryAppearance;
#pragma endregion

#pragma region	/** 游戏付费 */
	//显示付费时长到期界面
	UPROPERTY(BlueprintAssignable, Category = "TopUp")
		FOnShowStartBillingWnd OnShowStartBillingWnd;
	//隐藏付费时长到期界面
	UPROPERTY(BlueprintAssignable, Category = "TopUp")
		FOnHideStartBillingWnd OnHideStartBillingWnd;
#pragma endregion

#pragma region	/** 竞价分配 */
	//显示竞价界面
	UPROPERTY(BlueprintAssignable, Category = "Auction")
		FOnOpenAuctionPickWnd OnOpenAuctionPickWndEvent;
	//关闭竞价界面
	UPROPERTY(BlueprintAssignable, Category = "Auction")
		FOnCloseAuctionPickWnd OnCloseAuctionPickWndEvent;
	//追加竞拍宝箱
	UPROPERTY(BlueprintAssignable, Category = "Auction")
		FOnAddDropBoxAuction OnAddDropBoxAuctionEvent;
	//出价
	UPROPERTY(BlueprintAssignable, Category = "Auction")
		FOnAuctionBid OnAuctionBidEvent;
	//放弃竞价
	UPROPERTY(BlueprintAssignable, Category = "Auction")
		FOnAuctionAbandon OnAuctionAbandonEvent;
	//物品竞拍结束
	UPROPERTY(BlueprintAssignable, Category = "Auction")
		FOnAuctionItemEnd OnAuctionItemEndEvent;
	//收到竞拍历史列表（请求的返回数据）
	UPROPERTY(BlueprintAssignable, Category = "Auction")
		FOnRecvAuctionHistoryData OnRecvAuctionHistoryDataEvent;
	//增加一条历史列表
	UPROPERTY(BlueprintAssignable, Category = "Auction")
		FOnAddAuctionHistory OnAddAuctionHistoryEvent;
	//增加一条竞拍消息
	UPROPERTY(BlueprintAssignable, Category = "Auction")
		FOnAddAuctionMessage OnAddAuctionMessageEvent;
#pragma endregion

#pragma region	/** 多人载具 */
	//显示隐藏多人载具下载具按钮
	UPROPERTY(BlueprintAssignable, Category = "MoveVehicle")
		FOnSetDismountVehicleVisibility OnSetDismountVehicleVisibility;
#pragma endregion
};
