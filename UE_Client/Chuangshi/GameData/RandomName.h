#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "RandomName.generated.h"

/**
* 文件名称：RandomName.h
* 功能说明：随机名字数据
* 文件作者：chenxiaoyu
* 目前维护：chenxiaoyu
* 创建时间：2019-6-18
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRANDOM_SURNAME_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:

	///随机姓氏ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "RANDOM_SURNAME_DATA", DisplayName = "RandomSurnameID")
		int32  URandomSurnameID = 0;
	///随机姓氏内容
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "RANDOM_SURNAME_DATA", DisplayName = "RandomSurname")
		FString  URandomSurname;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRANDOM_NAME_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:

	///随机姓名ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "RANDOM_NAME_DATA", DisplayName = "RandomNameID")
		int32  URandomNameID = 0;
	///随机姓名内容
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "RANDOM_NAME_DATA", DisplayName = "RandomName")
		FString  URandomName;
	///性别（1：男，2：女）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "RANDOM_NAME_DATA", DisplayName = "RandomNameGender")
		int32  URandomNameGender = 1;
};