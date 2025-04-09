#pragma once

#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "LeadTroopsHeadIcon.generated.h"

/**
* 文件名称：LeadTroopsHeadIcon.h
* 功能说明：领兵模式头顶数据相关
* 文件作者：zhuangzhenguo
* 目前维护：zhuangzhenguo
* 创建时间：2020-05-08
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FLEADTROOPSHEAD_ICON_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:

	///ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LEADTROOPSHEAD_ICON_DATA", DisplayName = "ScriptID")
		FString  ScriptId;
	///友好关系
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LEADTROOPSHEAD_ICON_DATA", DisplayName = "RelationNormal")
		TSoftObjectPtr<UTexture2D> RelationNormal;
	///敌对关系
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LEADTROOPSHEAD_ICON_DATA", DisplayName = "RelationEnemy")
		TSoftObjectPtr<UTexture2D> RelationEnemy;

};