// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "BuffData.generated.h"

/**
* 文件名称：BuffData.h
* 功能说明：
* 文件作者：wangzheng
* 目前维护：hejingke
* 创建时间：2017-01-15
*/

/**
* Buff数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBuffData
{
	GENERATED_BODY()

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		int32 BuffIndex = 0;///<Buff索引
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		int32 BuffID = 0;///<BuffID
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		FString BuffScript;///<Buff脚本
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		int32 CasterID = 0;///<施法者
	void createFromStream(const KBEngine::FVariantMap& val)
	{
		BuffIndex = val.Find(TEXT("index"))->GetValue<int32>();
		BuffID = val.Find(TEXT("buffID"))->GetValue<int32>();
		BuffScript = TEXT("");//需要读表
		CasterID = val.Find(TEXT("casterID"))->GetValue<int32>();
	}
};

/**
* Buff界面数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBuffUIData
{
	GENERATED_BODY()

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		int32 BuffIndex = 0;///<Buff索引
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		FString BuffName;///<Buff名称
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		FString Description;///<Buff描述
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		UTexture2D* BuffIcon;///<Buff图标
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		bool IsShowIcon;///<是否显示Buff图标
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		float TotalTime;///<总持续时间
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		float RemainTime;///<剩余时间（-1代表“永久”）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		int32 Layer = 0;///<当前叠加层数
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Buff")
		bool CanInterrupt;///<是否可以主动中断
};
