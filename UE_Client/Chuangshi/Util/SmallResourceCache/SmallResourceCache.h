/**
* 功能说明：小资源缓存 使用文档: https://www.yuque.com/docs/share/c7b64d80-27bb-40a1-b5c9-f164e088311f?#
* 文件作者：yanjingxin
* 目前维护：yanjingxin
* 创建时间：2020/7/10
*/

#pragma once
#include "CoreMinimal.h"
#include "GameInstanceSubsystem.h"
#include "SmallResourceData.h"
#include "Engine/StreamableManager.h"
#include "UObject/NoExportTypes.h"
#include "SmallResourceCache.generated.h"

class AHUD;
class UCanvas;
class FDebugDisplayInfo;

/**
 * 小资源缓存功能参数配置
 */
UCLASS(Config=SmallResourceCacheConfig)
class CHUANGSHI_API USmallResourceCacheConfig : public UObject
{
	GENERATED_BODY()
public:

	UPROPERTY(Config, EditAnywhere, Meta = (ClampMin="0"), Category = CacheConfig)
	bool bEnableCache = true;
	
	/**
	 * 每次切换关卡时最多加载多少缓存
	 * SmallResourceCache 是在每次切换关卡时使用同步加载的
	 * 因为异步加载很容易被同步加载强制刷新,反而导致更多的卡顿
	 * 单位 MB
	 */
	UPROPERTY(Config, EditAnywhere, Meta = (ClampMin="0"), Category = CacheConfig)
	int32 SingleMaxLoadCache = 512;

	/**
	 * 估计正常游戏最大会占用的内存量
	 * 用于计算剩余可用于缓存的物理内存
	 * 单位 MB
	 */
	UPROPERTY(Config, EditAnywhere, Meta = (ClampMin="0"), Category = CacheConfig)
	int32 EstimatingGameMemoryUsage = 6144;

	/**
	 * 预留给系统的空闲内存
	 * 当系统空余物理内存不足时逐渐释放缓存的资源
	 * 然后在内存比较充足时在切换关卡的时候再缓存进来
	 */
	UPROPERTY(Config, EditAnywhere, Meta = (ClampMin="0"), Category = CacheConfig)
	int32 ReservedMemory = 5120;

	/**
	 * 检查剩余可用物理内存间隔
	 * 检查到内存不足时就开始释放缓存
	 */
	UPROPERTY(Config, EditAnywhere, Meta = (ClampMin="0"), Category = CacheConfig)
	float CheckMemoryInterval = 10.f;
	
	/**
	 * 需要缓存的资源
	 * 按照下标顺序缓存
	 * 内存不足时从后往前释放
	 */
	UPROPERTY(Config, EditAnywhere, Category = CacheConfig)
	TArray<TSoftObjectPtr<USmallResourceData>> CacheResourceDatas;
};

struct FCacheInfo
{
	FResourceDataInfo ResourceInfo;
	TSharedPtr<FStreamableHandle> StreamableHandlePtr;


	FCacheInfo(const FResourceDataInfo& ResourceInfo)
		: ResourceInfo(ResourceInfo)
	{
	}
};

UCLASS()
class USmallResourceCache : public UGameInstanceSubsystem
{
	GENERATED_BODY()
public:
	virtual bool ShouldCreateSubsystem(UObject* Outer) const override;
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;
	
	int64 GetAvailablePhysical_KB() const;

	// 通过控制台指令 ShowDebug SmallResourceCache 显示调试信息
	void OnShowDebugInfo(AHUD* HUD, UCanvas* Canvas, const FDebugDisplayInfo& DisplayInfo, float& YL, float& YPos);
private:
	void OnInit();
	void OnLoadCache();
	void OnCheckMemory();
	void OnReleaseCache(int64 MemorySize_KB);

	mutable USmallResourceCacheConfig* Config = nullptr;
	FTimerHandle CheckMemoryTimer;
	FDelegateHandle WorldDelegateHandle;

	TArray<FCacheInfo> AllCacheResourceData; // USmallResourceCacheConfig::CacheResourceDatas中所有可以缓存的资源信息
	int32 NowCacheIndex = -1;
	int64 NowCacheMemory_KB = 0;
	int32 ResourceDataTotalMemorySize_KB = 0;
};