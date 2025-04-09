// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Item/ToolCost.h"
#include "RoleWorkShopInterface.generated.h"

/*
* 文件名称：RoleWorkShopInterface.h
* 功能说明：轮回秘境打造接口
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2020-03-06
*/
UENUM(BlueprintType)
enum class COMPOSE_TYPE :uint8
{
	// 无
	COMPOSE_TYPE_NONE = 0,
	// 工具打造
	COMPOSE_TYPE_TOOL = 1,
	// 绿装打造
	COMPOSE_TYPE_GEQUIP = 2,
	// 乾坤鼎打造
	COMPOSE_TYPE_TRIPOD = 3,
};




UCLASS()
class CHUANGSHI_API URoleWorkShopInterface : public UCS3EntityInterface
{
	GENERATED_BODY()


public:
	static FString GetName() { return TEXT("RoleWorkShopInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleWorkShopInterface.BP_RoleWorkShopInterface_C'"); } //获取蓝图对象路径

	virtual void OnEnterScenes() override;///<开始场景

	/**
	*BlueprintNativeEvent,工具打造相关数据，并打开界面
	*
	*@param ComposeType  1为工具打造，2为绿装打造，3为乾坤鼎打造
	*@param EndTime 当前打造结束时间。使用FromServerTimeToClientTime转化
	*@param ItemID 当前打造的物品ID（无打造物品为0）
	*@param UnlockNum 储物柜解锁格子数，储物柜的物品在rolekitbaginterface中
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_onRequestComposeData(const int32& ComposeType, const int32& EndTime, const int32& ItemID, const int32& UnlockNum, const int32& NPCID);
	// 绿装打造数据 SuccessRate:绿装打造成功率（90.9，为 90.9%）
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_onRequestGEComposeData(const int32& ComposeType, const int32& EndTime, const int32& ItemID, const int32& UnlockNum, const float& SuccessRate, const int32& NPCID);

	// 打造回调 ComposeType： 1为工具打造，2为绿装打造，3为乾坤鼎打造
	UFUNCTION(BlueprintNativeEvent, Category = "ComposeEquip")
		void CLIENT_beginComposeTool(const int32& ComposeType, const int32& ItemID, const int32& EndTime);
	// 绿装打造回调 SuccessRate:绿装打造成功率（90.9，为 90.9%）
	UFUNCTION(BlueprintNativeEvent, Category = "ComposeEquip")
		void CLIENT_beginGEComposeTool(const int32& ComposeType, const int32& ItemID, const int32& EndTime, const float& SuccessRate);
	// 工具打造完成回调ComposeType  1为工具打造，2为绿装打造，3为乾坤鼎打造
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_OnFinishCompose(const int32& ComposeType, const int32& ItemID, const int32& Result);

	// 占领轮回秘境spaceType改变
	void OnOccypySpaceTypeChange(const enum LHMJ_SPACE_TYPE & _spaceType);

	// 获取当前建筑消耗倍率
	UFUNCTION(BlueprintCallable)
		float GetBuildConsumeRate(const enum LHMJ_BUILD_TYPE & _buildType);
	// 获取当建筑成功率和消耗倍率
	UFUNCTION(BlueprintCallable)
		void GetBuildSuccessRate(LHMJ_BUILD_TYPE BuildType, int32 ComposeType, int32& SuccessRate, int32& ConsumeRate);

	/// 获取工具能打造几个
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		int32 GetComposeToolNum(const int32& ItemID);
	/// 获取绿装能打造几个 
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		int32 GetComposeGEquipNum(const int32& ItemID);
	/// 获取乾坤鼎能打造几个
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		int32 GetComposeTripodNum(const int32& ItemID);
	/// 排序物品ID（用于界面 显示材料排序方式,先排品质，再排物品ID）
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void SortItemIDs(TArray<int32> InputItemIDArr, TArray<int32>& ItemIDArr);

	// 打造工具(卷轴ID，也是装备的ID) composeType:1为工具打造，3为乾坤鼎打造
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void ComposeTool(const int32& ComposeType, const int32& EquipID, bool bUseUnbind);
	// 打造绿装 BPrintUID:使用图纸的UID
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void ComposeGreedEquip(const int32& EquipID, bool bUseUnbind, const FString& BPrintUID);

	// 图纸熔炼 BPrintUID:图纸的UID(一键获得所有熔炼装备UID，见RoleKitBagInteface::GetMeltingEquipUID)
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void MeltingGreedEquip(const FString& BPrintUID, const TArray<FString> EquipUIDArr);
	// 打造回调 AddRate：熔炼增加的成功率（数值在0~100之间！ 数值是10.0，就是10.0%）
	UFUNCTION(BlueprintNativeEvent, Category = "ComposeEquip")
		void CLIENT_onMeltingtEquip(const FString& BPrintUID, const float& AddRate);

	// 向服务器请求祈福时间表
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void RequestPrayTimes();
	// 获取祈福更新 倒计时单位：秒（倒计时结束，界面需要调用RequestPrayTimes）
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		int32 GetReflashTime();
	// 请求回调 ProyNum：已经祈福的次数，剩余的祈福次数=10-ProyNum
	UFUNCTION(BlueprintNativeEvent, Category = "ComposeEquip")
		void CLIENT_OnRequestPrayTimes(const TArray<int32>& ProyTimeArr, const int32& ProyNum);
	// 开始祈福
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void BeginPrayComposeTimes();
	// 祈福回调 剩余祈福次数，需要减1
	UFUNCTION(BlueprintNativeEvent, Category = "ComposeEquip")
		void CLIENT_OnPrayTime(const int32& ProyTime);

	// 打开装备淬炼界面
	UFUNCTION(BlueprintNativeEvent, Category = "ComposeEquip")
		void CLIENT_OpenQuenchingEquip(const int32& NPCID);
	// 装备淬炼
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void QuenchingEquip(const FString& EquipUID);
	// 淬炼回调 NewProperty:淬炼后装备的属性
	UFUNCTION(BlueprintNativeEvent, Category = "ComposeEquip")
		void CLIENT_OnQuenchingEquip(const FString& EquipUID);

	// 从储物柜取物品（储物柜物品见RoleKitbagInteface::CLIENT_addStoreItem\CLIENT_removeStoreItem）
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		void RequestTakeToolItem(const int32& Order);

	virtual void InitBlueCB() override;

public:
	// 根据打造类型获取物品类型列表
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		TArray<FString> GetCategoryNameList(COMPOSE_TYPE ComposeType);

	// 获取某类型下的工具打造数据
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		TArray<int32> GetToolIDList(FString LabelName);
	// 获取某类型下的绿装打造数据
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		TArray<int32> GetEquipIDList(FString LabelName);
	// 获取某类型下的乾坤鼎数据
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		TArray<int32> GetTripodIDList(FString LabelName);

	// 是否在打造中
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		bool CheckComposeState(COMPOSE_TYPE ComposeType, float& RemainTime);

	// 获取打造所需时间
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		float GetComposeTotalTime(COMPOSE_TYPE ComposeType, int32 ComposeItemID);

	// 获取熔炼增加的成功率
	UFUNCTION(BlueprintCallable, Category = "ComposeEquip")
		float GetMeltingEquipSuccessRate(FString BlueprintUID, TArray<FString> EquipUIDs);

private:
	void _InitToolConfig();
	void _InitTripodConfig();

public:
	//当前正在打造的工具类型（只记录工具打造\绿装，不记录乾坤鼎）
	UPROPERTY(BlueprintReadOnly)
		COMPOSE_TYPE ToolComposeType;
	//打造的工具结束时间
	UPROPERTY(BlueprintReadOnly)
		FDateTime ToolComposeEndTime;

	// 工具打造消耗
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FToolComposeCost> ToolComposeCost;
	// 绿装打造消耗
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FGreenEquipComposeCost> GEquipComposeCost;
	// 熔炼配置
	UPROPERTY(BlueprintReadOnly)
		TArray<FMeltingEquipCost> MeltingEquipCfg;

	//乾坤鼎打造结束时间
	UPROPERTY(BlueprintReadOnly)
		FDateTime TripodComposeEndTime;
	// 乾坤鼎打造消耗
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, FTripodComposeCost> TripodComposeCost;

private:
	int32 _ProyNum;			// 祈福次数
	LHMJ_SPACE_TYPE spaceType;

};
