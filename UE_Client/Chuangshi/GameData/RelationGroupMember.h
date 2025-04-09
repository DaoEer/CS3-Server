#pragma once
#include "CoreMinimal.h"
#include "RelationGroupMember.generated.h"

/**
* 文件名称：RelationGroupMember.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2016-10-11
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRelationGroupMember
{
	GENERATED_USTRUCT_BODY()
		FRelationGroupMember() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerName")
		FString playerName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "profession")
		int32 profession = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "level")
		int32 level = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "camp")
		int32 camp = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "isOnline")
		bool isOnline = false;

	FORCEINLINE bool operator==(const FRelationGroupMember& member) const
	{
		if (this->playerName == member.playerName)
		{
			return true;
		}
		return false;
	}
};