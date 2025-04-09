// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "ChatType.h"
#include "ChatPageType.h"
#include "ChatData.generated.h"

/**
* 文件名称：ChatData.h
* 功能说明：
* 文件作者：huangshijie
* 目前维护：hejingke
* 创建时间：2016-09-06
*/

///聊天数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatData
{
	GENERATED_USTRUCT_BODY()
		FChatData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerDBID")
		int32 playerDBID = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "name")
		FString name;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "type")
		ChatType type = ChatType::Nearby;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "entityType")
		int32 entityType = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "message")
		FString message;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "time")
		FDateTime time = FDateTime::Now();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "richText")
		TArray<FString> richText;
};

///某个分页的聊天数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTabChatData
{
	GENERATED_USTRUCT_BODY()
		FTabChatData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ChatPageType PageType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FChatData> ChatDatas;
};

///搜索聊天数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTabFindChatData
{
	GENERATED_USTRUCT_BODY()
		FTabFindChatData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ChatPageType PageType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FText Text;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsVisible;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ChatDataCount;
};

///私聊和讨论组数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatWhisperAndGroupData
{
	GENERATED_USTRUCT_BODY()
		FChatWhisperAndGroupData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ChatType ChannelType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name;
};

///某个分页的聊天数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatHyperlinkData
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ResultStr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> RichTextStrs;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> InputBoxTextStrs;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> RichTextIndex;
};