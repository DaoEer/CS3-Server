/**
* 功能说明：小资源缓存 使用文档: https://www.yuque.com/docs/share/c7b64d80-27bb-40a1-b5c9-f164e088311f?#
* 文件作者：yanjingxin
* 目前维护：yanjingxin
* 创建时间：2020/7/10
*/

#pragma once
#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "Engine/EngineTypes.h"
#include "SmallResourceData.generated.h"

USTRUCT(BlueprintType)
struct FResourceDataInfo
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere)
    FSoftObjectPath ResourcePath;

    UPROPERTY(EditAnywhere)
    int32 MemorySize_KB;

    int32 GetMemorySize_KB() const
    {
        return MemorySize_KB * 2; // 在打包版本中测试发现实际内存占用大概是2倍
    }

    FResourceDataInfo(const FSoftObjectPath& ResourcePath, int32 MemorySize_KB)
     : ResourcePath(ResourcePath),
       MemorySize_KB(MemorySize_KB)
    {
    }
 
    FResourceDataInfo()
    {
    }
};

/**
 * SmallResourceCache 小资源缓存功能用到的数据
 */
UCLASS()
class CHUANGSHI_API USmallResourceData : public UDataAsset
{
	GENERATED_BODY()
public:
    /**
     * 对SmallResourceData资源使用右键脚本操作自动生成 ResourceData 时会按照这些路径搜索资源
     */
    UPROPERTY(EditAnywhere, Category = AutoDataGeneration, meta = (ContentDir))
    TArray<FDirectoryPath> ContentPaths;

    /**
     * 搜索的资源类型
     */
    UPROPERTY(EditAnywhere, Category = AutoDataGeneration)
    TArray<UClass*> ResourceClass;

    /**
     * 最大填入 ResourceData 中的总内存占用量
     */
    UPROPERTY(EditAnywhere, Category = AutoDataGeneration)
    int32 TotalMemorySize = 1024;
    
    UPROPERTY(EditAnywhere, Category = Data)
    TArray<FResourceDataInfo> ResourceData;

    UPROPERTY(EditAnywhere, Category = Data)
    int32 ResourceDataTotalMemorySize_KB = 0;
};
