// Fill out your copyright notice in the Description page of Project Settings.

#pragma once


#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/QTEDate.h"
#include "Operation/QTEBaseOperation.h"
#include "QTEManager.generated.h"


/*
* 文件名称：QTEManager.h
* 功能说明：QTE管理类
* 文件作者：huting
* 目前维护：huting
* 创建时间：2018-7-17
*/
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnKeyInputEvent, FKey, Key);

DECLARE_STATS_GROUP(TEXT("UQTEManager"), STATGROUP_QTEManager, STATCAT_Advanced);
UCLASS(BlueprintType)
class CHUANGSHI_API UQTEManager : public UCS3Object
{
	GENERATED_BODY()

private:
	UQTEManager();
	~UQTEManager();

public:
	static UQTEManager* GetInstance();

	void OnStartQTEEvent(FString TableRowName);///<开始QTE事件
	void OnStartQTESetTimer();
	void OnCheckQTEEvent();///<检测QTE事件
	void OnDeathQTEEvent();///<停止QTE事件
	void OnStopQTEEvent();
	void OnStartQTEEventType(FQTE_EVENT_DATA QTEEventData);
	void ImplementQTETypeEvent(QTE_COMPLETE_TYPE QTECompleteType);
	void OtherShowQTE();

	/**
	*null，显示boss进度条
	*
	*@param IsShow 是否显示
	*@param Percent 受伤害百分数
	*@param HurtPercent 预计扣血白分数
	*@param IsQTE 是否有QTE
	*
	*@return 无
	*/
	void ShowHPProgressBar(uint8 bIsShow, int32 Percent, int32 HurtPercent);

	UFUNCTION()
		void OnCheckKey(FKey Key);//开始执行输入QTE事件

	UFUNCTION()
		void OnContinueCheckKey(FKey Key);

	UFUNCTION()
		void OnContinueCheckRandomKey(FKey Key);///<CST-12007

	UFUNCTION()
		void OnContinuityKeyboard(FKey Key);

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|QTEManager")
		void OnBPStartQTEEvent(); ///蓝图开始事件

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|QTEManager")
		void OnBPStopQTEEvent(); ///蓝图结束事件

	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|QTEManager")
		void ShowWobbleMouseBar(bool isvisbale);

	/**
	*显示boss进度条
	*
	*@param IsShow 是否显示
	*@param Percent 受伤害百分数
	*@param HurtPercent 预计扣血白分数
	*@param IsQTE 是否有QTE
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|QTEManager")
		void OnBPShowHPProgressBar(uint8 bIsShow, int32 Percent, int32 HurtPercent);

	/**
	*提示玩家是否开始摇晃鼠标ui显示
	*
	*@param bIsSucceed 是否显示
	*@param Delay 延迟多少秒进行显示
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|QTEManager")
		void OnBPNotifyClinetQTEResult(uint8 bIsSucceed,float DelayTime);

	/**
	*BlueprintImplementableEvent，其他玩家显示QTE提示
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|QTEManager")
		void OnBPOtherShowQTE();

	UFUNCTION(BlueprintCallable, Category = "cs3|QTEManager")
		float GetQTEValue() { return QTEValue; }

		FOnKeyInputEvent OnKeyInputEvent;

private:
	void OnCellCall(bool bIsSuccess);///<通知服务器是否成功
	void OnCreatOperation(int32 QteType);///<创建QTE操作
	void OnResetQTEDate();///<清除QTE数据
	void OnClearTimer();
	void ResetContinueRandomKey(FQTE_TYPE_DATA  QTEType);///<重置连续随机键数据
	void SetContinueRandomKeyActionEnable(bool Enable);///<连续按键是否激活玩家Action行为 
private:
	FTimerHandle CheckQTEEventHandle;///<检测QTE事件定时器
	FTimerHandle StopQTEEventHandle;///<停止QTE事件定时器
	FTimerHandle DelayQTEEventHandle;///<延迟QTE事件定时器
	UQTEBaseOperation* Operation;//<QTE操作
	float QTEValue;
	bool Mouseistrue;
	TArray<FString> QTETypeArray;
	TArray<FString> QTETimeArray;
	TArray<FString> QTEKeypressArray;
	int32 QTEIndex = 0;
	TArray<FQTE_TYPE_DATA> QTETypeDataArray;
	TArray<FQTE_EVENT_DATA> QTEEventDataArray;
	TArray<FString> ContinueKeyList;
	FString ContinueName;
	FKey KeyValue;
	int8 ContinueInedx;
};
