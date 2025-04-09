#pragma once
#include "CoreMinimal.h"
#include "RelationGroupMember.h"
#include "RelationGroupData.generated.h"

/**
* 文件名称：RelationGroupData.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2016-10-11
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRelationGroupData
{
	GENERATED_USTRUCT_BODY()
		FRelationGroupData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "groupUID")
		int32 groupUID = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "groupName")
		FString groupName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "endTime")
		FString endTime;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "leaterName")
		FString leaterName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "passWord")
		FString passWord;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "frequency")
		int32 frequency = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "canJoin")
		bool canJoin = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "blackList")
		TArray<FString> blackList;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "groupMembers")
		TArray<FRelationGroupMember> groupMembers;
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FRelationGroupSimple
{
	GENERATED_USTRUCT_BODY()
		FRelationGroupSimple() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "groupUID")
		int32 groupUID = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "groupName")
		FString groupName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "groupNum")
		int32 groupNum = 0;

};