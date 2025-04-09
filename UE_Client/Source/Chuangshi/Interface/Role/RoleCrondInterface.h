// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Entity/Alias.h"
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/CrondDatas.h"
#include "RoleCrondInterface.generated.h"

/*
* 文件名称：RoleCrondInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：qiurunan
* 创建时间：2017-07-29
*/



UCLASS(BlueprintType)
class CHUANGSHI_API URoleCrondInterface:public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleCrondInterface();
	~URoleCrondInterface();
	static FString GetName() { return TEXT("RoleCrondInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleCrondInterface.BP_RoleCrondInterface_C'"); } //获取蓝图对象路径

	virtual void InitBlueCB() override;

public:
	//设置当天活动提醒设置数据
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		void SetCrondRemindSettingData(const FString& scriptID, CROND_REMIND_TYPE remindType);

	//获取当天活动提醒设置数据
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		TArray<FCrondRemindSettingData> GetCrondRemindSettingDatas();

	//根据活动脚本ID获取提醒设置数据
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		 bool GetCrondRemindSettingData(const FString& scriptID, FCrondRemindSettingData& OutRemindSettingData);

	//----------------------------------------------------------------------------------------------------------------
	//获取活动提醒设置数据
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestCrondRemindData();

	/**
	*Define method
	*获取活动提醒数据
	*
	*@param crondInfos ，数据（const FString&）
	*
	*@return 无
	*/
	void receiveCrondRemindData(const FVariant& datas);
	UFUNCTION(BlueprintImplementableEvent, Category = "CrondMgr")
		void BP_ReceiveCrondRemind();

	//收到活动提醒
	UFUNCTION(BlueprintNativeEvent, Category = "CrondMgr")
		void receiveCrondRemind(const FString& scriptID, const CROND_REMIND_TYPE& remindType);

	//请求当天活动日程数据
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RequestTodayActivitiesData();

	/**
	*Define method
	*活动日程数据
	*
	*@param activityCronds ，活动日程数据
	*
	*@return 无
	*/
	void recviveTodayActivitiesData(const FVariant& activityCronds);

	UFUNCTION(BlueprintImplementableEvent, Category = "CrondMgr")
		void BP_RefreshCrondDatasForWDay();

	/**
	*Define method
	*更新活动日程数据(更新当天)
	*
	*@param activityCronds 活动日程数据
	*
	*@return 无
	*/
	void recviveUpdateTodayActivitiesData(const FVariant& activityCronds);

	UFUNCTION(BlueprintImplementableEvent, Category = "CrondMgr")
		void BP_OnUpdateCrondData(const FString& scriptID, const FCrondData& CrondData);

	//请求未来6天的活动日程数据
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RequestWeekActivitiesData();

	/**
	*Define method
	*活动日程数据(未来6天)
	*
	*@param activityCronds ，活动日程数据
	*
	*@return 无
	*/
	void receiveWeekActivitiesData(const FVariantArray& activityCronds, const uint8& clearDataFalg);

	FCrondData getParseCrondData(const FString& date, const int32& wday, const FACTIVITY_DATA_DICT& data);

	/**
	*BlueprintCallable,请根据活动类型活动某个类型的所有当天的活动数据
	*
	*@param InRewardStr 奖励字符串列表
	*@param ItemNumList 物品数量列表
	*
	*@return 物品ID列表
	*/
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		TArray<int32> GetCrondRewardList(const FString& InRewardStr, TArray<int32>& ItemNumList);

	//根据活动类型活动某个类型的所有当天的活动数据及该活动参与的次数
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		TArray<FCrondData> GetCrondDatasByActiveType(TArray<int32>& OutActivityJoinTimes,ACTIVE_TYPE ActiveType);

	//获取相应奖励类型的活动数据
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		TArray<FNewCrondConfigData> GetActivitiesByRewardType(ACTIVE_REWARD_TYPE type);

	//获取相应日程类型的活动数据
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		TArray<FNewCrondConfigData> GetActivitiesByCrondType(CROND_TYPE CrondType = CROND_TYPE::CROND_TYPE_COMMON);

	//活动排序
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		TArray<FCrondData> SortCrondDatas(TArray<FCrondData> cronds);

	//前往活动地点
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		void NavigateToPoint(const FString& scriptID);
	//结束导航
	void OnNavigateCrondFinish();
	//导航失败
	void OnNavigateCrondFail();

	/**
	*Define method
	*获取活动参与次数
	*
	*@param datas ，数据（const FString&）
	*
	*@return 无
	*/
	void recvActivityTimesData(const FString& datas);

	/**
	*Define method
	*更新活动参与次数
	*
	*@param 
	*
	*@return 无
	*/
	void updateActivityTimesData(const int32& type, const int32& times);
	///<通知蓝图更新活动次数
	UFUNCTION(BlueprintImplementableEvent, Category = "CrondMgr")
		void BP_UpdateActivityTimesData(const FString& scriptID, const int32 JoinTimes, const int32 TotalTimes);

	//获取活动参与次数
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
	int32 GetActivityTimes(const FString& scriptID);

	//获取周特色玩法说明字段
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
	FString GetInfoByWeekDay(int32 weekDay, FString& OutSpecialPlaySummary);

	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		TArray<FDayCrondData> GetWeekCrondDatas();

	///获取活动状态
	UFUNCTION(BlueprintCallable, Category = "CrondMgr")
		ACTIVE_STATUS GetCrondStatusByScriptID(FString& scriptID);

private:
	const FNewCrondConfigData* GetNewCrondConfigData(const FString scriptID);
	void LoadCrondRewardDatas();
	void InitLoadCrondConfigDatas();
	void InitLoadWeekCrondConfigDatas();
	//活动提醒设置默认值
	void SetCrondRemindDefault(FString scriptID);

public:
	// 剩下六天的活动数据(按照顺序：第二天……第七天)
	UPROPERTY(BlueprintReadWrite, Category = "URoleCrondInterface")
		TArray<FDayCrondData> nextSixDayDatas;

	// 当天活动数据
	UPROPERTY(BlueprintReadWrite, Category = "URoleCrondInterface")
		FDayCrondData todayDatas;
		
private:
	TArray<FNewCrondConfigData*> CrondConfigDatas;
	TMap<int32, FWeekCrondConfigData*> WeekCrondConfigDatas; //周历配置数据, Key为0-6周一到周日, Value为周历配置数据
	//奖励类型(从配置中直接读取,包括所有的活动)
	TMap<ACTIVE_REWARD_TYPE, TArray<FNewCrondConfigData>> CrondRewardDatas;
	//活动提醒数据
	TMap<FString, FCrondRemindSettingData> CrondRemindSettingDatas;
	TMap<FString, int32> ActivityJoinTimes;//活动参与次数,Key为scriptID,Value为参与次数
};