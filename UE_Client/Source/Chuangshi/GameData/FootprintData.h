#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "FootprintData.generated.h"

/**
* 文件名称：FootprintData.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2017-09-27
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FFOOT_PRINT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	// 当前地图类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TEnumAsByte<EPhysicalSurface> SurfaceType;
	//网格物体名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString  EntityName;
	//左脚材质
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UMaterialInstance*  LeftFootMaterialName;
	//右脚材质
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UMaterialInstance*  RigthFootMaterialName;
	//特效配置表ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ParticleSystemID;
	//脚本声音效ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString FootPrintMusicID;
	//备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Remarks;
};