// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "GameData/GameDeFine.h"
#include "GameData/CsvTableRowBase.h"
#include "LocalTongSettingData.generated.h"

/**
* 文件名称：ULocalTongSettingData.h
* 功能说明：帮会设置数据
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2018-05-25
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTONG_EVENT_SET_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///帮会事件设置类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TONG_EVENT_SET_TYPE TongEventSetType;
	///是勾选
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsChecked;
};

UCLASS()
class CHUANGSHI_API ULocalTongSettingData : public USaveGame
{
	GENERATED_BODY()	
public:
	ULocalTongSettingData();
	UFUNCTION(BlueprintCallable, Category = "LocalTongSettingData")
		const FString& GetFileName();
	///初始化数据
	void InitLocalTongSettingData();
	///获取帮会事件设置默认数据
	UFUNCTION(BlueprintPure, Category = "LocalTongSettingData")
		TArray<FTONG_EVENT_SET_DATA> GetTongEventSetDefaultData();
	/**
	*保存帮会事件设置数据
	*
	*@param EventSetDatas 帮会事件设置数据
	*@param SelectedIndex 时间筛选（0：只显示今日；1：显示一周；2：显示一月；3：显示所有；）
	*@param IsOnlyMe 是否只显示与我相关
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LocalTongSettingData")
		void SaveTongEventSetData(TArray<FTONG_EVENT_SET_DATA> EventSetDatas, int32 SelectedIndex, bool IsOnlyMe);
	/**
	*保存帮会成员面板设置数据
	*
	*@param IsShowOffLine 是否显示离线帮众
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LocalTongSettingData")
		void SaveTongMembersSetData( bool IsShowOffLine);

private:
	UPROPERTY(VisibleAnywhere)
		FString FileName;///文件名字
public:
	///帮会事件设置数据
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "LocalTongSettingData")
		TArray<FTONG_EVENT_SET_DATA> TongEventSetDatas;
	///帮会事件时间筛选索引（0：只显示今日；1：显示一周；2：显示一月；3：显示所有；）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "LocalTongSettingData")
		int32 SelectedOptionIndex = 0;
	///是否只显示与我相关的帮会事件内容
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "LocalTongSettingData")
		bool IsShowOnlyMe;
	///是否显示离线帮众
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly,Category = "LocalTongSettingData")
		bool IsShowOffLineMembers;
};
