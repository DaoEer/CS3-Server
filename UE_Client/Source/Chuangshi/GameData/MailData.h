// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "Item/ItemBase.h"
#include "GameDeFine.h"
#include "MailData.generated.h"

/**
* 文件名称：MailData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-07-24
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMailData
{
	GENERATED_USTRUCT_BODY()
		FMailData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Id")
		FString Id;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Title")
		FString Title;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Content")
		FString Content;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SenderName")
		FString SenderName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ReceiverName")
		FString ReceiverName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Money")
		int64 Money;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SenderType")
		MAIL_SEND_TYPE SenderType = MAIL_SEND_TYPE::MAIL_SENDER_TYPE_PLAYER;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ReceiveTime")
		FString ReceiveTime;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RemainTime")
		int32 RemainTime = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsTaken")
		int32 IsTaken = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemList")
		TArray<UItemBase*> ItemList;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsRead")
		bool IsRead = false;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "LingShi")
		int32 LingShi;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "XianShi")
		int32 XianShi;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "BindMoney")
		int64 BindMoney;
};
