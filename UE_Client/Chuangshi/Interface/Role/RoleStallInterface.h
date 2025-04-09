// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/StallItemData.h"
#include "GameData/StallRecordData.h"
#include "GameData/StallItemSuccessData.h"
#include "RoleStallInterface.generated.h"

/*
* 文件名称：RoleStallInterface.h
* 功能说明：摆摊出售收购相关函数接口
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

class UItemBase;
class UJsonFieldData;



UCLASS(BlueprintType)
class CHUANGSHI_API URoleStallInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleStallInterface();
	~URoleStallInterface();
	static FString GetName() { return TEXT("RoleStallInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleStallInterface.BP_RoleStallInterface_C'"); } //获取蓝图对象路径

	/**
	* 寻路到摆摊点
	*
	* @return 无
	*/
	void FindStallPoint();
	/// 摆摊路点回调
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
	void CLIENT_OnFindStallPoint(FString& ScriptID, const FString& Number);
	/// 摆摊寻路完成
	void OnNavigateStallFinish();
	/// 摆摊寻路中断
	void OnNavigateStallFail();

	/// 进入摆摊状态（所有角色都会走，该状态）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
		void OnEnterStall();
	/// 离开摆摊状态（所有角色都会走，该状态）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
		void OnLevelStall();

	/**
	* 开始摆摊，自动寻路到摆摊点
	* 
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
	void StartStall();

	/**
	* 取消摆摊(与摆摊结束，行为不同)
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void CancelStall();

	// 显示摆摊界面
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
		void OnShowStall();

	/**
	* 摆开摊位（坐下摆摊）
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void StallItem();

	/**
	* Define method
	* 摆摊成功回调 通知界面创建摆摊开始界面
	*
	* @param tax 摊税
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
	void CLIENT_StallSuccessCB(const int32& tax );

	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void EndStall();

	/**
	* Define method
	* 增加收购物品的回调 通知界面更新数据
	*
	* @param data - 物品的数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
	void CLIENT_AddCollectionItemSuccessCBBP();

	void CLIENT_AddCollectionItemSuccessCB(const FVariant& data);
	/**
	* Define method
	* 更新收购物品的回调 通知界面更新数据
	*
	* @param data - 物品的数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
	void CLIENT_UpdateStallCollectionItemCBBP(const int32& slot);

	void CLIENT_UpdateStallCollectionItemCB(const int32& slot, const FVariant& data);

	/**
	* @param data - 物品的数据
	* 下架收购物品的回调 通知界面更新数据
	*
	* @param playerID 玩家ID
	* @param slot 位置
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
		void CLIENT_RemoveStallCollectionItemCB(const int32& playerID, const int32& slot);

	/**
	* Define method
	* 增加出售物品的回调
	* 
	* @param data - 物品的数据
	* 
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
		void CLIENT_AddStallSellItemSuccessCBBP();

		void CLIENT_AddStallSellItemSuccessCB(const FVariant& data);

	/**
	* Define method
	* 更新出售物品的回调
	*
	* @param data - 物品的数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
		void CLIENT_UpdateStallSellItemCBBP(const int32& slot);

		void CLIENT_UpdateStallSellItemCB(const int32& slot, const FVariant& data);

	/**
	* Define method
	* 下架出售物品的回调
	*
	* @param playerID 玩家ID
	* @param slot 位置
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
		void CLIENT_RemoveStallSellItemCB(const int32& playerID, const int32& slot);

	/**
	* Define method
	* 服务器回调函数 获得对方摆摊物品列表
	* 
	* @param TargetID - 对方ID
	* @param data - 出售物品和收购物品打包数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
	void CLIENT_OnReceiveOtherStallItemsBP(const int32& TargetID, const FString& TempStallName);
	
	void CLIENT_OnReceiveOtherStallItems(const int32& TargetID, const FString& TempStallName, const FVariant& data);

	// 离开目标的摊位
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
		void OnLeaveTargetStall();

	/**
	* Define method
	* 更新摆摊物品的数据
	*
	* @param type - 类型（出售或收购）
	* @param data - 物品的数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
	void CLIENT_UpdateStallItemBP(const int32& type, const int32& slot, const int32& playerID);
	
	void CLIENT_UpdateStallItem(const int32& type , const int32& slot,const int32& playerID, const FVariant& data);

	void CLIENT_UpdateOtherStallItems(const int32& TargetID, const FVariant& data);

	/**
	* Define method
	* 对方购买和出让回调
	*
	* @param type - 类型（出售或收购）
	* @param data - 物品的数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
	void CLIENT_StallItemSuccessToClientBP(const int32& type, const FString& stallName, const FString& ItemName,const int32& Amount,const int32& TotalPrice);

	void CLIENT_StallItemSuccessToClient(const int32& type,const FVariant& data);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
	void StallItemSuccess(const int32& type, const FString& stallName, const FString& Amount, const FString& ItemName, int64 TotalPrice);


	/**
	* Define method
	* 增加摆摊记录
	*
	* @param type - 类型（出售或收购）
	* @param data - 物品的数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
	void CLIENT_AddStallRecordBP(const int32& type,const FStallRecordData& recordData);

	void CLIENT_AddStallRecord(const int32& type, const FVariant& data);

	/**
	* Define method
	* 获得上次未出售完或收购完的物品
	*
	* @param data - 物品的数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleStallInterface")
	void CLIENT_OnRequestStallItemsBP();

	void CLIENT_OnRequestStallItems(const FString& stallName, const FVariant& data);

	/**
	* 设置摊位名称
	*
	* @param name - 摊位名
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void SetStallName(const FString& name);

	/**
	* 通知界面显示出售物品数据 
	*
	* @return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStallInterface")
	void GetStallSellItemsCB();

	/**
	* 打开其他人摊位
	*
	* @param entityID 对方ID
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void OpenRoleStall(const int32& playerID);

	/**
	* 增加收购的物品
	*
	* @param itemID 物品ID
	* @param amount 收购数量
	* @param price 收购单价
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void AddStallCollectionItem(const int32& itemID, const int32& amount, const int64& price);

	/**
	* 更新收购的物品
	*
	* @param slot 位置
	* @param itemID 物品ID
	* @param amount 收购数量
	* @param price 收购单价
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void UpdateStallCollectionItem(const int32& slot,const int32& itemID, const int32& amount, const int64& price);

	/**
	* 下架收购物品
	*
	* @param slot 位置
	* @param itemID 物品ID
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void RemoveStallCollectionItem(const int32& slot, const int32& itemID );

	/**
	* 增加出售的物品
	*
	* @param itemID 物品ID
	* @param amount 收购数量
	* @param price 收购单价
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void AddStallSellItem(const FString& id, const int32& itemID, const int32& amount, const int64& price);

	/**
	* 更新出售的物品
	*
	* @param slot 位置
	* @param itemID 物品ID
	* @param amount 收购数量
	* @param price 收购单价
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void UpdateStallSellItem(const int32& slot, const int32& itemID, const int32& amount, const int64& price);

	/**
	* 下架出售物品
	*
	* @param slot 位置
	* @param itemID 物品ID
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void RemoveStallSellItem(const int32& slot, const int32& itemID);

	/**
	* 购买物品
	*
	* @param entityID 对方ID
	* @param slot 位置
	* @param itemID 物品ID
	* @param amount 收购数量
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void BuyStallItem(const int32& playerID, const int32& slot, const int32& itemID, const int32& amount);

	/**
	* 出让物品给摊位
	*
	* @param entityID 对方ID
	* @param slot 位置
	* @param itemID 物品ID
	* @param amount 收购数量
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void SellStallItem(const int32& playerID, const int32& slot, const int32& itemID, const int32& amount);

	/**
	* 清除所有物品和记录
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		void ClearAllStallItems();

	/**
	* 获得摆摊记录数据
	*
	* @param data 记录数据
	*
	* @return 记录
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		FStallRecordData GetStallItemRecordByData(const FString& data);

	/**
	* 获得摆摊总收益
	*
	* @return 摆摊出售总价格
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		int32 GetTotalSellPrice();

	/**
	* 获得摆摊总支出
	*
	* @return 摆摊收购总价格
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		int32 GetTotalCollectPrice();

	/**
	* 通知背包界面恢复操作
	*
	* @return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleStallInterface")
		void OnBagEnableItem(const FString& id);

	/**
	* 获得对方购买或出让成功的数据
	*
	* @param data 购买或出让成功的数据
	*
	* @return 购买或出让成功数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleStallInterface")
		FStallItemSuccessData GetStallItemSuccessInfoByData(const FString& data);
	/**
	*BlueprintCallable,通知改变任务对话过程中状态
	* @param IsQuestTalking
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleTalkInterface")
		void OnChangeStallState(bool IsStall);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_endStall();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestGetStallItems();

	virtual void InitBlueCB() override;

public:
	///< 摆摊出售物品
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FStallItemData> StallSellItemList;
	///< 摆摊收购物品
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FStallItemData> CollectionItemList;
	///< 摊位名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString StallName;
	///< 出售记录
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FStallRecordData> StallSellItemRecordList;
	///< 收购记录
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FStallRecordData> StallCollectItemRecordList; 

	///< 其他玩家摆摊出售物品
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<UItemBase*> OtherStallSellItemList;
	///< 其他玩家摆摊收购物品
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FStallItemData> OtherCollectionItemList;
private:
	// 解析摆摊物品数据
	void AnalysisStallData(TArray<FStallItemData>& ItemData, UJsonFieldData* data);
	// 解析其他玩家的摆摊数据
	void AnalySisOtherStallItem(TArray<UJsonFieldData*>& data);

private:
	FString StallScriptID;				/// 摆摊点的地图 ScriptID
	FString StallPoint;					///< 摆摊点

	FTimerHandle timer;

};