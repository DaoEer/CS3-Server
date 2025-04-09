// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Object.h"
#include "Entity/Alias.h"
#include "GameData/Item/ItemIntensifyData.h"
#include "GameData/Item/ItemCost.h"
#include "GameData/Item/Equip.h"
#include "GameData/ConstData.h"
#include "GameData/RoleInfo.h"
#include "CS3Base/CS3EntityInterface.h"
#include "RoleEquipInterface.generated.h"

/*
* 文件名称：RoleEquipInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

/**
*玩家装备接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleEquipInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleEquipInterface();
	~URoleEquipInterface();
	static FString GetName() { return TEXT("RoleEquipInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleEquipInterface.BP_RoleEquipInterface_C'"); } //获取蓝图对象路径

	/// 穿戴（卸下）装备回调
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void CLIENT_onEquipWieldCb(const FString& ItemUID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void CLIENT_onEquipUnWieldCb(const FString& ItemUID);

	/**
	*BlueprintCallable, 强化多个装备
	*
	*@param EquipUID 强化装备UID
	@param DstLv 强化的目标等级
	@param AttachItemUID 附加材料UID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface | Intensify")
	void IntensifyEquip(const FString& EquipUID, const int32& DstLv, const int32& AttachItemID);
	///<装备强化成功
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleEquipInterface | Intensify")
	void OnIntensifySuccess(const FString& EquipUID);


	/**
	*BlueprintPure, 获取强化消耗
	*
	*@param uids 强化装备UID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintPure, Category = "RoleEquipInterface  | Intensify")
		void GetIntensifyCost(const FString& EquipUID, const int32& IntensifyLv, int32& CostMoney, int32& WhiteBeadCount, int32& FiveBeadCount,int32& SuperBeadCount);

	UFUNCTION(BlueprintPure, Category = "RoleEquipInterface  | Intensify")
		void GetSumIntensifyCost(const FString& EquipUID, const int32& DstLv, int32& CostMoney, int32& WhiteBeadCount, int32& FiveBeadCount, int32& SuperBeadCount);	

	/// 根据物品ID 获取装备强化材料的数量
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		int32 GetTotalAmountByItemID(const int32& ItemID);

	/**
	*BlueprintCallable, 获取玩家背包玄晶的数量
	*
	*@param WhiteBeadCount 玄晶
	*@param FiveBeadCount 五彩玄晶
	*@param SuperBeadCount 超级玄晶
	*
	*@return 无
	*/ 
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface  | Intensify")
		void GetIntensifyCrystal(int32& WhiteBeadCount, int32& FiveBeadCount, int32& SuperBeadCount);
	
	/**
	*BlueprintCallable, 获取玩家背包龙珠的数量
	*
	*@param WhiteDragonCount 龙珠
	*@param FiveDragonCount 五彩龙珠
	*@param SuperDragonCount 超级龙珠
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface  | Intensify")
		void GetIntensifyDragon(int32& WhiteDragonCount, int32& FiveDragonCount, int32& SuperDragonCount);

	/**
	*BlueprintCallable, 获取玩家背包晶石的数量
	*
	*@param WhiteSparCount 晶石
	*@param FiveSparCount 五彩晶石
	*@param SuperSparCount 超级晶石
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface  | Intensify")
		void GetIntensifySpar(int32& WhiteSparCount, int32& FiveSparCount, int32& SuperSparCount);

	/**
	*BlueprintCallable, 获取玩家背包回火符的数量
	*
	*@param HHFuCount 回火符
	*@param ZYFuCount 正阳符
	*@param BDFuCount 北斗符
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface  | Intensify")
		void GetIntensifyFu(int32& HHFuCount, int32& ZYFuCount, int32& BDFuCount);

	/// 获取玩家背包洗练石的数量
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface  | Shuffle")
		void GetShuffleWStone(int32& WStoneCount);

	/// 获取玩家背包血符的数量
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface  | Shuffle")
		void GetShuffleBloodFu(int32& BloodFuCount);

	/// 获取玩家背包重铸宝珠的数量
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface  | Recast")
		void GetRecastCStone(int32& CStoneCount);

	/// 获取玩家背包重铸保护符的数量
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface  | Recast")
		void GetRecastCZFu(int32& CZFuCount);

	/**
	*BlueprintCallable, 装备回火
	*
	*@param EquipUID 强化装备UID
	*@param Indexs 强化附加属性index
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void EquipBackfire(const FString& EquipUID, const TArray<FString>& Indexs);
	///<装备回火成功
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleEquipInterface")
		void OnBackfireSuccess(const FString& EquipUID);

	/**
	*BlueprintPure, 获取回火消耗
	*
	*@param uids 强化装备UID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintPure, Category = "RoleEquipInterface  | BackFire")
		void GetBackFireCost(const FString& EquipUID, const TArray<FString>& SaveUIDs, int32& WhiteSparCount, int32& FiveSparCount, int32& SuperSparCount, int32& MoneyCost);
	
	/**
	*BlueprintCallable, 请求装备备份数据
	*
	*@return bool（false:有数据，界面可以直接读取;true:向服务器请求数据，见回调）
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		bool RequestIntensifySaveSlotInfo();

	void CLIENT_OnRequestIntensifySaveSlotInfo(const int32& SlotNum, const FVariant& EQUIP_INTENSIFY_SAVES_1);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void OnRequestIntensifySaveSlotInfo();
	/// 该物品是否已保存
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		bool HasSaveItemIntensify(const FString& ItemUID);
	/// 获取装备保存数据
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		TArray<FIntensifyData> GetSaveIntensifyInfoByIndex(const int32& Index);
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		TArray<FIntensifyData> GetSaveIntensifyInfoByUID(const FString& ItemUID, int32& Index);
	
	/**
	*BlueprintCallable, 解锁装备备份栏
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void OpenIntensifySaveSlot(const int32& MoneyCost);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void OpenIntensifySaveSlotSuccess();
	
	/**
	*BlueprintCallable, 保存强化装备
	*
	*@param uids 强化装备UID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void IntensifySaveEquip(const FString& Index, const FString& ItemUID);
	void _OnIntensifySaveEquip(const FString& Index, const FString& ItemUID);
	/// 装备强化回调
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void OnIntensifySaveSuccess(const int32& Index, const FString& ItemUID);
	/// 获取强化备份消耗(金钱、北斗符消耗)
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void GetIntensifySaveCost(const FString& ItemUID, int32& MoneyCost, int32& BDFuCost);

	/**
	*BlueprintCallable, 还原装备
	*
	*@param uids 强化装备UID
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void IntensifyRestoreEquip(const FString& ItemUID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void OnIntensifyRestoreSuccess(const FString& ItemUID);
	/// 获取强化还原消耗(金钱、北斗符消耗)
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void GetIntensifyRestoreCost(const FString& ItemUID, int32& MoneyCost, int32& BDFuCost);

	/// 装备洗练
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void ShuffleEquip(const FString& EquipUID, const TArray<int32>& LockProps, const bool& UseYBToStone, const bool& UseYBToFu);
	/* 装备洗练回调
	/*@param EquipUID 装备UID
	/*@param ShuffleProps 装备洗练出的属性（"propertyID#value|propertyID#value"）
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void OnShuffleEquip(const FString& EquipUID, const FString& ShuffleProps);
	// 替换洗练属性
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void ReplaceShufflePro(const FString& EquipUID);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void OnShuffleEquipSuccess(const FString& EquipUID);
	// 获取装备洗练消耗(根据锁定属性数量，计算金钱、洗练石、血符消耗)
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void GetShuffleCost(const FString& EquipUID, const int32 LockNum, int32& MoneyCost, int32& WashStone, int32& BloodFu, int32& YBrepStone, int32& YBrepFu);

	/// 装备重铸
	/* @param EquipUID  装备UID
	/* @param LockProps 锁定属性
	/* @param UseYBToStone 是否用元宝替换重铸宝珠
	/* @param UseYBToFu 是否用元宝替换重铸保护符
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void RecastEquip(const FString& EquipUID, const TArray<int32>& LockProps, const bool& UseYBToStone, const bool& UseYBToFu);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void OnRecastEquipSuccess(const FString& EquipUID);
	// 获取装备重铸消耗(根据保护属性数量，计算金钱、重铸宝珠、重铸符消耗)
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void GetRecastCost(const FString& EquipUID, const int32 LockNum, int32& MoneyCost, int32& RecastStone, int32& RecastFu, int32& YBrepStone, int32& YBrepFu);

	/// 装备传星
	/* @param SrcEquipUID 旧装备UID
	/* @param DstEquipUID 新装备UID
	/* @param UseNewPro 是否使用新装备附加属性
	/* @param BiographyList 需要传星强化属性（UID/Index）
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void BiographyEquip(const FString& SrcEquipUID, const FString& DstEquipUID, const bool& UseNewPro, const TArray<FString>& BiographyList);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void OnBiographyEquipSuccess();
	// 获取装备传星消耗(根据保护属性数量，计算金钱、回火符、正阳符、北斗符消耗)
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void GetBiographyCost(const FString& DstEquipUID, const int32 LockNum, int32& MoneyCost, int32& WhiteSparCount, int32& FiveSparCount, int32& SuperSparCount);

	// 获取装备附加属性的最大值
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void GetEquipPropMax(UEquip* Equip, const int32& PropertyID, int32& Max);
	/// 装备洗练相关属性的显示
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void GetEquipShuffleShow(const FString& EquipUID, TArray<FEquipShuffleData>& ShuffleData);

	// 打开装备改造界面
	UFUNCTION(BlueprintNativeEvent, Category = "RoleEquipInterface")
		void OpenForgeEquip(const int32& NPCID);

	// 是否有足够灵石（仙石），优先扣除灵石
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		bool HasEnoughStone(int32 StoneNum);

#pragma region 装备打造
	/// 查询装备打造卷轴
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void QueryEquipComposeDatas();
	/// 查询回调，如果为空！！则不会返回给客户端（不会调用该方法）
	UFUNCTION(BlueprintNativeEvent, Category = "ComposeEquip")
		void CLIENT_onRequestEquipCompose(const TArray<int32>& EquipBprint);
	///<设置装备打造图纸装备部位对应的装备数据
	void SetEquipBuildPartDatas();
	void AddEquipBuildPartData(int32 EquipID);
	///<获取装备打造图纸某个部位的所有装备ID列表
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		TArray<int32> GetEquipBuildIDList(MODEL_PART_TYPE PartType);
	///<获取装备ID在打造图纸上的部位类型
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		bool GetEquipBuildPartType(int32 EquipID, MODEL_PART_TYPE& PartType);
	/// 学习装备打造卷轴
	UFUNCTION(BlueprintNativeEvent, Category = "ComposeEquip")
		void CLIENT_onStudyEquipCompose(const int32& EquipID);

	/// 打造装备(卷轴ID，也是装备的ID)
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void RequestEquipCompose(const int32& EquipID, bool bUseUnbind);
	UFUNCTION(BlueprintNativeEvent, Category = "ComposeEquip")
		void CLIENT_onSuccessComposeEquip(const int32& EquipID);

	/// 获取装备能打造几把
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		int32 GetComposeEquipNum(const int32& EquipID, const bool& UseUnBind);
	/// 获取装备卷轴信息
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		FEquipComposeCost GetComposeEquipData(const int32& EquipID);

#pragma endregion

	// 请求目标玩家装备信息
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void QueryTargetEquipInfo(const int32& TargetID);
	// 远程请求目标玩家装备信息
	UFUNCTION(BlueprintCallable, Category = "RoleEquipInterface")
		void RemoteQueryTargetEquipInfo(const FString& TargetName);
	void CLIENT_OnQueryTargetEquipInfo(const FVariant& equipFixedDict, const FVariant& roleFixedDict);
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleEquipInteraface")
		void OnQueryTargetEquipInfoCB();

	virtual void InitBlueCB() override;

	virtual void onLeaveWorld() override;

public:
	/// 已开启备份栏数目
	UPROPERTY(BlueprintReadOnly, Category = "RoleEquipInterface")
		int32 IntensifySaveSlotNum;



	/// 备份装备 index : ItemID
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, int32> IntensifySaveItemMap;
	/// 备份装备数据 index : UID
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FString> IntensifyUIDs;

	/// 查看目标装备信息数据
	UPROPERTY(BlueprintReadOnly)
		TArray<UItemBase*> TargetEquipArry;
	/// 查看目标玩家属性数据
	UPROPERTY(BlueprintReadOnly)
		FROLEPROPERTYINFO TargetPropertyInfo;
private:
	bool CanIntensify(const FString& EquipUID, const int32& dstLv, const int32& AttachItemID);///<能否强化
	bool CanBackFire(const FString& EquipUID, const TArray<FString>& SaveUIDs);///是否能回火
	bool CanSaveIntensify(const FString& Index, const FString& EquipUID);///是否能保存备份装备强化
	bool CanRestoreIntensify(const FString& EquipUID);///是否能还原装备强化
	bool CanShuffle(const FString& EquipUID, const TArray<int32>& LockProps, const bool& UseYBToStone, const bool& UseYBToFu, bool& BYbToStone, bool& BYbToFu); ///是否能洗练装备
	bool CanRecast(const FString& EquipUID, const TArray<int32>& LockProps, const bool& UseYBToStone, const bool& UseYBToFu, bool& BYbToStone, bool& BYbToFu); ///是否能重铸装备
	bool CanBiography(const FString& SrcEquipUID, const FString& DstEquipUID, const bool& UseNewPro, const TArray<FString>& BiographyList); ///是否能传星装备

	TMap<FString, TArray<FIntensifyData>> IntensifySaveInfo;		 /// 备份装备数据 UID : FIntensifyData

	TMap<int32,const FEquipComposeCost*> EquipComposeInfo;				/// 装备打造消耗数据
	TMap<MODEL_PART_TYPE, TArray<int32>> EquipPartDatas;				/// 装备打造图纸部位数据{{部位类型,{装备ID1, 装备ID2,....}}}
};