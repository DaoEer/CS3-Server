// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "../ChatData.h"
#include "LocalRelationData.generated.h"


/**
* 文件名称：ULocalRelationData.h
* 功能说明：关系界面下线保存的数据
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2018-07-25
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRelationChatData
{
	GENERATED_USTRUCT_BODY()
		FRelationChatData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "name")
		FString name;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "time")
		FDateTime time = FDateTime::Now();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "message")
		FString message;
};
UCLASS()
class CHUANGSHI_API ULocalRelationData : public USaveGame
{
	GENERATED_BODY()
	
public:
	ULocalRelationData();
	UFUNCTION(BlueprintCallable, Category = "LocalRelationData")
		const FString& GetFileName();

	///初始化关系数据
	UFUNCTION(BlueprintCallable, Category = "LocalRelationData")
		void InitLocalRelationData();

	///通过RelationUId获取和某个玩家的关系聊天数据
	UFUNCTION(BlueprintPure, Category = "LocalRelationData")
		TArray<FRelationChatData> GetRelationChatDatas(const FString& RelationUId);

	/**
	*保存关系聊天数据
	*
	*@param RelationUId 玩家关系UID
	*@param RelationChatData 关系聊天数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LocalRelationData")
		void SaveRelationChatData(const FString& RelationUId, FRelationChatData RelationChatData);

	///保存关系设置是否只显示在线玩家
	UFUNCTION(BlueprintCallable, Category = "LocalRelationData")
		void SaveRelationSetShowOnline(bool IsShowOnline);

	///根据时间限制删除聊天记录(比如days为7，则删除7天之前的聊天记录)，根据定义的最大保存数量，超过则删除
	void RemoveRelationChatData(const FString& RelationUId);

	
private:
	UPROPERTY(VisibleAnywhere)
		FString FileName;///文件名字
public:
	///是否只显示在线玩家
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "LocalRelationData")
		bool IsShowOnlyOnline;
	///关系聊天数据
	TMap<FString, TArray<FRelationChatData>>RelationChatDatas;
};
