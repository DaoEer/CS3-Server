// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "RoleSpaceStageInterface.generated.h"

/*
* 文件名称：RoleSpaceStageInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：yikun
* 创建时间：2017-07-29
*/

/**
 * 副本阶段目标完成接口类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleSpaceStageInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleSpaceStageInterface();
	~URoleSpaceStageInterface();
	static FString GetName() { return TEXT("RoleSpaceStageInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleSpaceStageInterface.BP_RoleSpaceStageInterface_C'"); } //获取蓝图对象路径

	/**
	*Define method
	*BlueprintNativeEvent,添加副本阶段区域
	*
	*@param SpaceScriptID，副本脚本ID(const FString&)
	*@param StageIndex，阶段索引(const int32&)
	*@param AreaInfoStr，区域信息(const FString&)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceStage")
		void CLIENT_AddSpaceStageTaskArea(const FString& SpaceScriptID, const int32& StageIndex, const FString& AreaInfoStr);

	/**
	*Define method
	*BlueprintNativeEvent,添加副本阶段区域
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceStage")
		void CLIENT_ClearSpaceStageTaskArea();///<BlueprintNativeEvent，清除副本阶段区域

	/**
	*Define method
	*BlueprintNativeEvent,显示下个阶段目标
	*
	*@param stageIndex，阶段索引
	*@param spaceStageTasks，阶段目标
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceStage")
		void CLIENT_showSpaceStageNextTask( const int32& stageIndex, const FString& tasksJson );

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|SpaceStage")
		void ShowSpaceStageNextTask(const int32& stageIndex, const int32& taskIndex, const FString& implType, const FString& taskTitle, const FString& val, const FString& reqVal, const FString& param1, const FString& param2, const FString& param3, const FString& navigateData, bool isShowByProgressbar, bool isEnd);

	/**
	*Define method
	*BlueprintNativeEvent,显示阶段
	*
	*@param stageFileName，阶段名字
	*@param completeStages，已完成阶段
	*@param spaceStageJson，阶段数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceStage")
		void CLIENT_showSpaceStageWin(const FString& stageFileName,const TArray<FString>& completeStages,const FString& spaceStageJson);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|SpaceStage")
		void ShowSpaceStageWin(const FString& stageFileName, const TArray<FString>& completeStages, const int32& stageIndex,const FString& title,const FString& comment,const int32& taskIndex,const FString& implType,const FString& taskTitle,const FString& val,const FString& reqVal,const FString& param1,const FString& param2,const FString& param3,const FString& navigateData,bool isShowByProgressbar,bool isEnd);


	/**
	*Define method
	*BlueprintNativeEvent,更新阶段目标值
	*
	*@param stageIndex，阶段索引
	*@param taskData，阶段目标值 taskIndex:value
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceStage")
		void CLIENT_updateSpaceStageWin(const int32& stageIndex, const FString& taskData);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|SpaceStage")
		void UpdateSpaceStageWin(const int32& stageIndex, const int32& taskIndex, const FString& val);


	/**
	*Define method
	*BlueprintNativeEvent,更新已完成的阶段
	*
	*@param completeStages，已完成的阶段
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceStage")
		void CLIENT_updateCompleteSpaceStage(const TArray<FString>& completeStages);

	/**
	*Define method
	*BlueprintNativeEvent,隐藏阶段
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceStage")
		void CLIENT_hideSpaceStageWin();

	/**
	*Define method
	*BlueprintNativeEvent,显示副本统计
	*
	*@param statisticsFileName，统计名称
	*@param JsonSec，统计Json数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceStage")
		void CLIENT_showSpaceStatistics(const FString& statisticsFileName, const FString& statisticsJson);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|SpaceStage")
		void ShowSpaceStatistics(const FString& statisticsFileName, const int32& questID, const FString& title, const FString& comment, const int32& entryIndex, const FString& statisticsTitle, const FString& value, const FString& postfix, const FString& param1, const FString& param2, const FString& param3, const FString& param4, const FString& progress, bool isEnd);

	/**
	*Define method
	*BlueprintNativeEvent,更新副本统计数据
	*
	*@param statisticsJson，Json数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceStage")
		void CLIENT_updateSpaceStatistics(const FString& statisticsJson);
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|SpaceStage")
		void UpdateSpaceStatistics(const int32& entryIndex, const FString& value);

	/**
	*Define method
	*BlueprintNativeEvent,隐藏副本统计
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|SpaceStage")
		void CLIENT_hideSpaceStatistics();

	/**
	*进入副本阶段目标完成的区域
	*
	*@param StageIndex 副本类型
	*@param TaskIndex 任务目标Index
	*
	*@return 无
	*/
	void CELL_OnEnterSpaceStageArea(INT32 StageIndex, INT32 TaskIndex);
	
	virtual void InitBlueCB() override;
};
