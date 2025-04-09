/**
* 功能说明：小资源缓存功能的辅助工具 使用文档: https://www.yuque.com/docs/share/c7b64d80-27bb-40a1-b5c9-f164e088311f?#
* 文件作者：yanjingxin
* 目前维护：yanjingxin
* 创建时间：2020/7/6
*/

#pragma once
#include "AssetActionUtility.h"
#include "SmallResourceCacheTool.generated.h"

/**
 * 用于辅助填充小资源缓存数据表的工具
 */
UCLASS(Blueprintable)
class CHUANGSHIEDITOR_API USmallResourceCacheTool : public UAssetActionUtility
{
    GENERATED_BODY()
public:
    /**
     * 将资源引用从小到大填入指定的表
     * @param TotalMemorySize 总计最大填入多大内存占用的资源,单位为MB
     * @param Target 目标数据表
     * @param bOverlap 是否覆盖目标数据表
     */
    UFUNCTION(BlueprintCallable, DisplayName="自动生成选中的SmallResourceData数据")
    void GeneratingData();
};
