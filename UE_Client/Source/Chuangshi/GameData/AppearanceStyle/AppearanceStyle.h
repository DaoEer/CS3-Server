/**
* 功能说明：基础的模型外观样式数据结构
* 文件作者：yanjingxin
* 目前维护：yanjingxin
* 创建时间：2020/4/26
*/

#pragma once

#include "CoreMinimal.h"
#include "Actor/GameCharacter.h"
#include "GameData/CharacterData.h"
#include "Materials/MaterialInterface.h"
#include "AppearanceStyle.generated.h"

DECLARE_STATS_GROUP(TEXT("CS3_AppearanceStyle"), STATGROUP_AppearanceStyle, STATCAT_Advanced);

class AGameCharacter;

USTRUCT(BlueprintType)
struct FMeshMaterial
{
    GENERATED_BODY()

    /**
     * \brief 材质球的下标从0开始算
     */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="FMeshMaterial")
    int32 ElementIndex = 0;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="FMeshMaterial")
    TSoftObjectPtr<UMaterialInterface> Material;
};

USTRUCT(BlueprintType)
struct FMeshMaterialParameter
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="FMeshMaterialParameter")
    FName ParameterName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="FMeshMaterialParameter")
    int32 ParameterValue;
};

/**
 * \brief 模型外貌样式信息
 */
USTRUCT(BlueprintType)
struct FAppearanceStyle
{
    GENERATED_BODY()

    /**
     * \brief 样式对应的模型部位
     */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AppearanceStyle")
    MODEL_PART_TYPE ModelPartType;
    
    /**
     * \brief 模型材质球对应的材质
     */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AppearanceStyle")
    TArray<FMeshMaterial> MeshMaterial;
    
    /**
     * \brief 模型上的材质参数
     */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AppearanceStyle")
    TArray<FMeshMaterialParameter> MeshMaterialParameter;
};

class AppearanceStyleUtilities
{
 public:
    /**
     * \brief 应用AppearanceStyle外貌样式
     * \param GameCharacter 目标
     * \param AppearanceStyle 外貌样式
     */
    static void ApplyAppearanceStyle(AGameCharacter& GameCharacter, const FAppearanceStyle& AppearanceStyle);
};
