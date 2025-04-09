// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/NPCBaseObjectInterface.h"
#include "GameData/Item/ItemBase.h"
#include "TeamDropBoxInterface.generated.h"

/*
* 文件名称：TeamDropBoxInterface.h
* 功能说明：
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2020-11-13
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UTeamAllocationItemData : public UCS3Object
{
	GENERATED_BODY()
public:
	///< dbid
	UPROPERTY(BlueprintReadOnly)
		FString dbid;

	///< 拾取的物品
	UPROPERTY(BlueprintReadOnly)
		TArray<UItemBase*> items;
};

/**
 * 帮会宝箱接口类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UTeamDropBoxInterface : public UNPCBaseObjectInterface
{
	GENERATED_BODY()
	typedef UNPCBaseObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UTeamDropBoxInterface();
	~UTeamDropBoxInterface();
	static FString GetName() { return TEXT("TeamDropBoxInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.TeamDropBoxInterface'"); } //获取蓝图对象路径
	virtual void InitBlueCB() override;
	
	//是否显示
	bool isVisible();
	//当前宝箱是否可打开
	bool isCanOpenBox();
	///宝箱物品分配是否是某种分配方式
	bool isAllocationType(TEAM_PICKUP_TYPE type);

	///更新宝箱可见性
	UFUNCTION(BlueprintNativeEvent, Category = "TeamDropBoxInterface")
		void onUpdateDropBoxModelVisible();

	void onOpenDropbox();
	
	///请求获取宝箱数据
	UFUNCTION(BlueprintCallable, Category = "TeamDropBoxInterface")
		void ReqTeamDropBoxData();
	//宝箱物品数据
	void recvDropBoxData(const FVariant& owners, const FVariantArray& freeItems);
	//队长分配的物品数据 还未分配的物品数据
	void recvDropBoxNoAllocationData(const FVariantArray& dbidList, const FVariantArray& items, const FVariantArray& notAllocationItems);
	TArray<UItemBase*> AnalyzeItemData(const FVariantArray& variant);

	///请求分配宝箱物品
	UFUNCTION(BlueprintCallable, Category = "TeamDropBoxInterface")
		void ReqPickUpToMember(const FString& uid, const FString& playerName);
	/// 某人取得了某物品(帮主分配)
	UFUNCTION(BlueprintNativeEvent, Category = "TeamDropBoxInterface")
		void onPickUpByLeader(const FString& uid, const FString& playerDBID);

	///请求自由拾取
	UFUNCTION(BlueprintCallable, Category = "TeamDropBoxInterface")
		void ReqPickUp(const TArray<FString>& uidList);
	/// 某人取得了某物品(自由拾取获得)
	UFUNCTION(BlueprintNativeEvent, Category = "TeamDropBoxInterface")
		void onPickUp(const FString& uid, const FString& playerDBID);
	
	///通知更新自由拾取的物品
	void updateFreeAllocationItem(const FVariant& FVariantItem);

	/**
	*BlueprintCallable,获取所有队长分配物品数据
	*
	*@param outAllocationItems 输出物品ItemBase列表
	*@param outAllocationPlayerName 输出物品对应的分配人员，未分配的传空
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "TeamDropBoxInterface")
		void GetAllleaderAllocationItems(TArray<UItemBase*>& outAllocationItems, TArray<FString>& outAllocationPlayerName);

	///打开自由拾取界面
	void OpenFreePickUpWnd();

	//是否能分配物品
	UFUNCTION(BlueprintCallable, Category = "TeamDropBoxInterface")
		bool isCanPickUpMember();

public:
	///参与宝箱分配的玩家 {DBID:NAME}
	UPROPERTY(BlueprintReadOnly, Category = "TeamDropBoxInterface")
		TMap<FString, FString> ownerInfos;

	//队长分配的物品
	UPROPERTY()
		TMap<FString, UTeamAllocationItemData*> leaderHasAllocationItems;

	///自由拾取的物品{uid:item}
	UPROPERTY(BlueprintReadOnly, Category = "TeamDropBoxInterface")
		TMap<FString, UItemBase*> freeAllocationItems;

	///未进行分配的物品{uid:item} 队长进行分配的物品
	UPROPERTY(BlueprintReadOnly, Category = "TeamDropBoxInterface")
		TMap<FString, UItemBase*> notAllocationItems;

};
