#pragma once
#include "CoreMinimal.h"
#include "RelationData.generated.h"

/**
* 文件名称：RelationData.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2016-09-27
*/

///@struct FRelationData
USTRUCT(BlueprintType)
struct CHUANGSHI_API FRelationData
{
	GENERATED_USTRUCT_BODY()
		FRelationData() {};
public:
	/// UID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "relationUID")
		FString relationUID;

	/// 玩家名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playName")
		FString playName;

	/// 玩家备注名
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "aliasName")
		FString aliasName;

	/// 玩家DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerDBID")
		FString playerDBID;
	/// 玩家id(用于判断是否在线）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerID")
		int32 playerID = 0;

	/// 关系数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "relationShip")
		int32 relationShip = 0;

	/// 玩家职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "profession")
		int32 profession = 0;

	/// 玩家等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "level")
		int32 level = 0;

	/// 玩家阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Camp")
		int32 Camp = 0;

	/// 帮会名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "tongName")
		FString tongName;

	/// 玩家所在地
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "localSpace")
		FString localSpace;

};
///@struct FRelationCatalogData
USTRUCT(BlueprintType)
struct CHUANGSHI_API FRelationCatalogData
{
	GENERATED_USTRUCT_BODY()
		FRelationCatalogData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "relationIndex")
		int32 relationIndex = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "relationName")
		FString relationName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "relationUID")
		TArray<FString> relationUIDs;

	FORCEINLINE bool operator==(const FRelationCatalogData& A) const
	{
		if (A.relationIndex == this->relationIndex)
		{
			return true;
		}
		return false;
	};
};