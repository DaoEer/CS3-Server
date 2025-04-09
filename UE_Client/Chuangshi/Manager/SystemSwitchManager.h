#pragma once
#include "GameData/CS3Object.h"
#include "GameData/SystemSwitchData.h"
#include "GameData/UIConfigData.h"
#include "SystemSwitchManager.generated.h"

/*
* 文件名称：SystemSwitchManager.h
* 功能说明：系统开启管理器
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-03-16
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USystemSwitchManager : public UCS3Object
{
	GENERATED_BODY()
	USystemSwitchManager();
	~USystemSwitchManager();

public:
	static USystemSwitchManager* GetInstance();

	///加载配置
	void LoadCfg();
	/**
	*根据系统索引获取配置数据
	*
	*@param	SystemIndex  系统索引
	*@param	IsSuccess  是否成功获取到配置表中的数据
	*
	*@return FSystemSwitchData 配置数据
	*/
	FSystemSwitchData GetSystemSwitchDataBySystemIndex(FName SystemIndex, bool& IsSuccess);
	/**
	*根据系统索引获取配置数据
	*
	*@param	BtnTag  按钮标记
	*@param	IsSuccess  是否成功获取到配置表中的数据
	*
	*@return FSystemSwitchData 配置数据
	*/
	FSystemSwitchData GetSystemSwitchDataByBtnTag(FName BtnTag, bool& IsSuccess);
	/**
	*根据界面类型获取配置数据
	*
	*@param	SystemWindowType 界面类型
	*
	*@return FSystemSwitchData 配置数据
	*/
	FSystemSwitchData GetSystemSwitchDataBySystemWindowType(FString SystemWindowType, bool& IsSuccess);
	/**
	*根据界面类型获取配置数据
	*
	*@param	WindowType  界面类型
	*
	*@return TArray<FSystemSwitchData> 配置数据
	*/
	TArray<FSystemSwitchData> GetSystemSwitchDataByWindowType(FString WindowType);
	/**
	*系统是否已经开放
	*
	*@param	SystemIndex  系统索引
	*
	*@return 系统是否已经开放
	*/
	UFUNCTION(BlueprintCallable, Category = "SystemSwitchManager")
		bool IsOpenBySystemIndex(FName SystemIndex);
	/**
	*系统是否已经开放
	*
	*@param	BtnTag  按钮标记
	*
	*@return 系统是否已经开放
	*/
	UFUNCTION(BlueprintCallable, Category = "SystemSwitchManager")
		bool IsOpenByBtnTag(FName BtnTag);
	/**
	*系统是否已经开放
	*
	*@param	SystemWindowType  界面类型
	*
	*@return 系统是否已经开放
	*/
	UFUNCTION(BlueprintCallable, Category = "SystemSwitchManager")
		bool CheckOpenByWindowType(FString SystemWindowType);
	/**
	*初始化系统开放状态
	*
	*@param	WindowType  界面类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SystemSwitchManager")
		void InitOpenStateByWindowType(FString WindowType);

	/**
	*系统功能按钮tips
	*
	*@param	BtnTag  按钮标记
	*@param	IsOpen  系统是否开启
	*
	*@return 提示字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "SystemSwitchManager")
		FString GetTipsByBtnTag(FName BtnTag, bool& IsOpen);
	/**
	*获取功能按钮配置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SystemSwitchManager")
		FFunctionBtnData GetBtnCfgByBtnTag(FName BtnTag, bool& IsSuccess);

	/**
	*获取功能UClass
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SystemSwitchManager")
		UClass* GetClassByScript(FString Script);

	/**
	*获取某个活动系统的倒计时
	*
	*@param BtnTag 按钮标记
	*
	*@return int32
	*/
	UFUNCTION(BlueprintCallable, Category = "SystemSwitchManager")
		int32 GetRemainTime(FName BtnTag);

	//等级改变
	void OnChangeMyRoleLevel(int32 Level);
	//改变任务状态
	void OnChangeQuestState(int32 QuestID);
	//服务器开启活动系统
	void OnOpenActivitySystem(FName BtnTag, int32 RemainTime);
	//服务器关闭活动系统
	void OnCloseActivitySystem(FName BtnTag);
	//切换地图
	void OnEnterSpaceNotify(FString SpaceScriptID);

	void OnEnterWorld();            ///< 当Entity进入世界时，此方法被调用
	void OnLeaveWorld();            ///< 当Entity离开世界（被销毁时）时，此方法被调用

private:
	///检查是否开启
	void CheckLevelSwitch(int32 Level);
	///检查是否开启
	void CheckQuestSwitch(int32 QuestID);
	///检查是否开启
	void CheckSpaceSwitch(FString SpaceScriptID);
	///放弃任务
	void AbandonQuest(int32 QuestID);

	///系统未开启tips
	FString GetSystemConditionTips(bool& IsOpen, FSystemSwitchData Data);
	///获取tip表配置
	FString GetTipsCfg(FString TipsID);

private:
	static USystemSwitchManager* Instance;
	//配置表数据
	UPROPERTY()
		TMap<FName, FSystemSwitchData> SystemSwitchDatasMap;
};