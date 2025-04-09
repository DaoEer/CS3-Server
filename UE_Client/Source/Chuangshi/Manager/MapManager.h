// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/Area.h"
#include "GameData/Area/BaseArea.h"
#include "GameData/Area/BaseQuestArea.h"
#include "GameData/Area/PlaneArea.h"
#include "GameData/Area/ReviveArea.h"
#include "GameData/Area/ProtectedArea.h"
#include "GameData/Area/SubArea.h"
#include "GameData/Area/WholeArea.h"
#include "GameData/Area/SpaceEventBaseArea.h"
#include "GameData/Area/SpaceEventCircleArea.h"
#include "GameData/Area/SpaceEventSquareArea.h"
#include "GameData/Area/SpaceStageBaseArea.h"
#include "GameData/Area/SpaceStageCircleArea.h"
#include "GameData/Area/SpaceStagePolyArea.h"
#include "GameData/Area/ActivityCircleArea.h"
#include "GameData/Area/JSZZCircleArea.h"
#include "MapManager.generated.h"

/*
* 文件名称：MapManager.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2016-12-06
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FAreaReviveData
{
	GENERATED_BODY()

	///复活地图
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString ReviveSpace = TEXT("");
	///复活地图名字
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString ReviveSpaceName = TEXT("");
	///复活位置
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FVector RevivePosition = FVector::ZeroVector;
	///复活朝向
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FRotator ReviveDirection = FRotator::ZeroRotator;
};

/**
* 文件名称：MapManager.h
* 功能说明：地图区域管理器
* 文件作者：chendongyong
* 创建时间：2016/11/26
* 更改记录:
*/
UCLASS(Blueprintable)
class CHUANGSHI_API UMapManager : public UCS3Object
{
	GENERATED_BODY()

public:
	static UMapManager* GetInstance();

	/**
	*加载地图区域
	*
	*@param level 关卡名
	*
	*@return 无
	*/
	void LoadArea(const FName level);

	void ClearAreaInst();/// 清除地图缓冲数据

	void SendEnterSpaceMsg();///进地图读条完毕时，显示进入地图提示。注：进位面时不会调用此方法。

	void AddAreaDetectTimer();///</开始区域检测timer
	void ClearAreaDetectTimer();///<结束区域检测timer
	
	void PauseAreaDetectTimer();///<暂停区域检测，因为在切换关卡的时候会出错，所以在开始切换关卡时，暂停检测；切换好关卡再开始。
	void UnPauseAreaDetectTimer();///</重启区域检测，因为在切换关卡的时候会出错，所以在开始切换关卡时，暂停检测；切换好关卡再开始。

	/**
	*BlueprintCallable，新增触发任务目标区域
	*
	*@param QuestID 任务ID
	*@param TaskID 任务目标ID
	*@param Param1 ScriptID
	*@param Param2 区域中心点坐标的字符串
	*@param Param3 Range/100
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "MapManager")
		void AddAreaQuest(int QuestID, int TaskID, const FString& TaskParam1, const FString& TaskParam2, const FString& TaskParam3);

	/**
	*新增副本阶段任务区域
	*
	*@param SpaceScriptID 副本脚本ID
	*@param EventType 事件类型
	*@param EventID 事件ID
	*@param Param1 事件参数1
	*@param Param2 事件参数2
	*@param Param3 事件参数3
	*
	*@return 无
	*/
	void AddSpaceEventArea(FString SpaceScriptID, INT32 EventType, INT32 EventID, INT8 ShapeType, FString Param1, FString Param2, FString Param3);

	void ClearSpaceEventArea();///<清空副本阶段任务区域

	/**
	*新增触发副本阶段目标完成的区域
	*
	*@param SpaceScriptID 副本脚本ID
	*@param StageIndex 副本阶段ID
	*@param TaskIndex 任务目标ID
	*@param CeilHeight 天空高度
	*@param FloorHeight 地面高度
	*@param AreaParam 区域参数3
	*
	*@return 无
	*/
	void AddSpaceStageArea(FString SpaceScriptID, INT32 StageIndex, INT32 TaskIndex, INT8 ShapeType, float CeilHeight, float FloorHeight, FString AreaParam);

	void ClearSpaceStageArea();///<清空触发副本剧情事件区域

	/**
	*获取玩家当前关卡的地图名
	*
	*@return FString 当前关卡的地图名
	*/
	UFUNCTION(BlueprintCallable, Category = "MapManager")
		FString GetAreaName();

	/**
	*将space 的scriptID转化 为地图名
	*
	*@return FString 关卡的地图名
	*/
	UFUNCTION(BlueprintCallable, Category = "MapManager")
		FString ChangeSpaceScriptIDToAreaName(const FString SpaceScriptID);

	/**
	*获取区域复活数据
	*
	*@return FAreaReviveData 区域复活数据
	*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
		FAreaReviveData GetAreaReviveData();

	/**
		*是否超过区域死亡深度
		*
		*@return bool 超过区域死亡深度返回TRUE，否则返回FALSE。
		*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
		bool IsPlayerUnderArea();

	/**
	*玩家是否在飞行高度以上
	*
	*@return bool 
	*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
		bool IsPlayerFlyCeiling();

	/**
	*玩家是否在位面中
	*
	*@return bool 玩家在位面中返回TRUE，否则返回FALSE。
	*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
		bool IsPlayerInPlane();

	/**
	* @fn	FString GetRelatedMapScriptID();
	*
	* @brief	获取当前区域（位面、子区域）对应的大地图的scriptID.
	*
	* @date	2017/4/21
	*
	* @return	当前区域（位面、子区域）对应的大地图的scriptID.
	*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
		FString GetRelatedMapScriptID(const FString& level);

	/**
	*IsPlaneSpace
	* @brief 是否是位面Space
	* @param const FString & Level	地图SpaceID
	* @return bool	是位面返回true，否则返回false
	*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
		bool IsPlaneSpace(const FString& Level);

	/**
	*IsCopySpace
	* @brief 是否是副本Space，包括SpaceCopyStoryArea和SpaceCopyNormalArea
	* @param const FString & Level	地图SpaceID
	* @return bool	是位面返回true，否则返回false
	*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
		bool IsCopySpace(const FString& Level);

	/**
	*获取玩家当前位面的区域
	*
	*@return TArray<FVector2D> 玩家当前位面的区域
	*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
		TArray<FVector2D> GetPlanePolygon();

	/**
	*设置玩家当前位面的区域
	*/
	void SetPlanePolygon(const FString& spaceScriptID, const TArray<FVector>& wallPosList);

	/**
	*是否靠近位面边界
	*
	*@return bool 靠近位面边界返回TRUE，否则返回FALSE。
	*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
		bool IsPlayerCloseToPlaneArea(float Distance);

	/**
	*获得当前子区域的ScriptID
	*
	*@return FString 返回当前大地图的ScriptID,返回当前子区域的ScriptID. 
	*
	*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
	void GetCurrentSubAreaScriptID(FString& MapScriptID,FString& SubAreaScriptID, FString& SubAreaName);

	/**
	*当前是否在子区域
	*/
	UFUNCTION(BlueprintPure, Category = "MapManager")
	bool IsPlayerInSubArea();

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|SpaceEvent")
		void BP_UpdateSubArea(const FString& NewArea, const FString& OldArea);
	/**
	*新增大地图活动圆形区域
	*
	*@param SpaceScriptID 地图名

	*
	*@return 无
	*/
	void AddActivityCircleArea(FString SpaceScriptID, FVector position, float Range, int32 Index);
	void ClearActivityCircleArea();///<清空活动圆形区域区域

	void AddJSZZCircleArea(FString SpaceScriptID, FVector position, float Range);
	void ClearJSZZCircleArea(); ///<清除金树种子区域检测

private:
	virtual void BeginDestroy() override;
	void DetectArea();					///<检测区域包括（位面区域、触发任务目标区域、副本剧情区域、子区域、副本阶段任务区域）
	void DetectPlaneArea();				///<检测位面区域
	void DetectQuestArea();				///<检测触发任务目标区域
	void DetectSpaceEventArea();		///<检测副本剧情区域
	void DetectSubArea();				///<检测子区域
	void DetectSpaceStageArea();		///<副本阶段任务区域
	void DetectActivityCircleArea();	///<检测大地图活动圆形区域
	void DetectProtectedArea();			///<检测保护区域
	void DetectJSZZArea();				///<检测金树种子区域

private:
	UPROPERTY()
	TArray<UPlaneArea*> PlaneAreas;///< 位面区域
	UPROPERTY()
	TMap<FName, UPlaneArea*> PlaneWholeAreas;	///< 位面地图区域( 添加这个，是为了效率查找位面区域！而无需遍历所有位面)
	UPROPERTY()
	TArray<USubArea*> SubAreas;	///<子区域	
	UPROPERTY()
	TMap<FName, UWholeArea*> WholeAreas;///< 关卡区域	
	UPROPERTY()
	TArray<UBaseQuestArea*> QuestAreas;///< 触发任务目标区域	
	UPROPERTY()
	TArray<UReviveArea*> ReviveAreas;///< 复活区域	
	UPROPERTY()
	TArray<UProtectedArea*> ProtectedAreas; ///< 保护区域
	UPROPERTY()
	TArray<USpaceEventBaseArea*> SpaceEventAreas;///<副本剧情区域	
	UPROPERTY()
	TArray<INT32> LastSEAreaIndexs;///<上一次检测时处于的副本剧情区域AreaIndex，列表中有多个表示同时处于多个区域
	UPROPERTY()
	TArray<USpaceStageBaseArea*> SpaceStageAreas;	///<副本阶段任务区域
	UPROPERTY()
	TArray<INT32> LastSSAreaIndexs;	///< 上一次检测时处于的副本阶段任务区域AreaIndex，列表中有多个表示同时处于多个区域
	UPROPERTY()
	FTimerHandle DetectTimerHander;	///< timer	
	UPROPERTY()
	USubArea* LastSubArea;///<上一次检测时处于的普通子区域
	UPROPERTY()
	TArray<UActivityCircleArea*> ActivityCircleAreas;	///<检测大地图活动圆形区域
	UPROPERTY()
	TArray<int32> LastACAreaIndexs;///< 上一次检测时处于的副本阶段任务区域AreaIndex，列表中有多个表示同时处于多个区域
	UPROPERTY()
	UJSZZCircleArea* JSZZCircleArea;
	UPROPERTY()
	bool isAreaInJSZZArea = false;///<是否已经进入过了金树种子区域
	
	//static UMapManager* Instance;
};
