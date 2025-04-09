#pragma once

#include "GameData/CsvTableRowBase.h"
#include "GameData/GameDeFine.h"
#include "SpaceEntityRelationTableData.generated.h"

/**
* 文件名称：SpaceEntityRelationTableData.h
* 功能说明：地图entity关系判断实例配置表
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-06-26
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSpaceEntityRelationTableData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString RelationMode;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ENTITY_TYPE_EXT EntityFlagExt;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString RelationScript;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool RelationModeResult = (!(this->RelationMode.IsEmpty())) && (this->RelationMode == "RelationDefault");
		bool EntityFlagExtResult = (this->EntityFlagExt >= (ENTITY_TYPE_EXT)0) && (this->EntityFlagExt <= (ENTITY_TYPE_EXT)25);
		bool RelationScriptResult = !(this->RelationScript.IsEmpty());
		bool result = RelationModeResult && EntityFlagExtResult && RelationScriptResult;

		if (result)
		{
			ResultInfo.Result = Ok;
			return;
		}
		else
		{
			ResultInfo.Result = Error;
		}
		if (!RelationModeResult)
		{
			ResultInfo.CheckLog += FString::Printf(TEXT("RelationMode: \"%s\" is config error!  "), *this->RelationMode);
		}
		if (!EntityFlagExtResult)
		{
			ResultInfo.CheckLog += FString::Printf(TEXT("EntityFlagExt: is config error!  "));
		}
		if (!RelationScriptResult)
		{
			ResultInfo.CheckLog += FString::Printf(TEXT("RelationScript: \"%s\" is config error! "), *this->RelationScript);
		}
		if (!result)
		{
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};