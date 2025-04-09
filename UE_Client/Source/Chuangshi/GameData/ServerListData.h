#pragma once

#include "CsvTableRowBase.h"
#include "ServerListData.generated.h"

/**
* 文件名称：ServerListData.h
* 功能说明：服务器列表数据
* 文件作者：张丹
* 目前维护：张丹
* 创建时间：2019-6-20
*/

/**
 *	#服务器状态
 */
UENUM(Blueprintable)
enum class FSERVER_STATE : uint8
{
	MAINTENANCE = 0,	///< 维护
	FULL,				///< 爆满
	BUSY,				///< 繁忙
	GOOD,				///< 良好
	VERY_GOOD,			///< 极佳
};

/**
 * #服务器数据
 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSERVER_DATA
{
	GENERATED_USTRUCT_BODY()

		UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ServerKey;

	/** 服务器类型 1电信，2网通，3双线 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ServerType;

	/** 服务器名字 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName ServerName;

	/** 服务器IP */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> ServerIP;

	/** 服务器状态 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSERVER_STATE ServerState;

	/** 是否推荐 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsRecomment;

	/** 是否是新服务器 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsNewServer;
};

/**
 * #服务器状态数据
 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSERVER_STATE_DATA
{
	GENERATED_USTRUCT_BODY()

	/** 服务器名字 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName ServerName;

	/** 服务器状态 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSERVER_STATE ServerState;

	FORCEINLINE bool operator==(const FSERVER_STATE_DATA& Other) const
	{
		if (this->ServerName == Other.ServerName)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};