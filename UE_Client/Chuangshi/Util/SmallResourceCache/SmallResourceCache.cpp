#include "SmallResourceCache.h"
#include "TimerManager.h"
#include "Engine/AssetManager.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/HUD.h"

bool USmallResourceCache::ShouldCreateSubsystem(UObject* Outer) const
{
    Config = GetMutableDefault<USmallResourceCacheConfig>();
    return Config->bEnableCache && !GEngine->IsEditor();
}

void USmallResourceCache::Initialize(FSubsystemCollectionBase& Collection)
{
    Config = GetMutableDefault<USmallResourceCacheConfig>();
    
    for(auto& SmallResourceDataPtr : Config->CacheResourceDatas)
    {
        auto& ResourceDatas = SmallResourceDataPtr.LoadSynchronous()->ResourceData;
        AllCacheResourceData.Reserve(AllCacheResourceData.Num() + ResourceDatas.Num());
        for(auto& ResourceDataInfo: ResourceDatas)
        {
            AllCacheResourceData.Add(FCacheInfo{ResourceDataInfo});
        }
        ResourceDataTotalMemorySize_KB += SmallResourceDataPtr->ResourceDataTotalMemorySize_KB;
    }
    ResourceDataTotalMemorySize_KB *= 2; // 在打包版本中测试发现实际内存占用大概是2倍
    
   WorldDelegateHandle = FWorldDelegates::OnPostWorldInitialization.AddLambda([this](UWorld* World, const UWorld::InitializationValues _)
   {
       if(IsValid(World))
       {
           // 重新注册定时器
           World->GetTimerManager().SetTimer(CheckMemoryTimer, [this]()
           {
               OnCheckMemory();
           }, Config->CheckMemoryInterval, true);

           // 在切换关卡时加载缓存
           OnLoadCache();
       }
   });

    AHUD::OnShowDebugInfo.AddUObject(this, &USmallResourceCache::OnShowDebugInfo);

    static FAutoConsoleVariableRef CV_SingleMaxLoadCache(
    TEXT("CS3_Cache.SingleMaxLoadCache"),
    Config->SingleMaxLoadCache,
    TEXT("每次切换关卡时最多加载多少缓存\n")
    TEXT("SmallResourceCache 是在每次切换关卡时使用同步加载的\n")
    TEXT("因为异步加载很容易被同步加载强制刷新,反而导致更多的卡顿\n")
    TEXT("单位 MB"),
    ECVF_Cheat
    );

    static FAutoConsoleVariableRef CV_EstimatingGameMemoryUsage(
    TEXT("CS3_Cache.EstimatingGameMemoryUsage"),
    Config->EstimatingGameMemoryUsage,
    TEXT("估计正常游戏最大会占用的内存量\n")
    TEXT("用于计算剩余可用于缓存的物理内存\n")
    TEXT("因为异步加载很容易被同步加载强制刷新,反而导致更多的卡顿\n")
    TEXT("单位 MB"),
    ECVF_Cheat
    );

    static FAutoConsoleVariableRef CV_ReservedMemory(
    TEXT("CS3_Cache.ReservedMemory"),
    Config->ReservedMemory,
    TEXT("预留给系统的空闲内存\n")
    TEXT("当系统空余物理内存不足时逐渐释放缓存的资源\n")
    TEXT("然后在内存比较充足时在切换关卡的时候再缓存进来\n")
    TEXT("单位 MB"),
    ECVF_Cheat
    );
    
    static FAutoConsoleVariableRef CV_CheckMemoryInterval(
    TEXT("CS3_Cache.CheckMemoryInterval"),
    Config->CheckMemoryInterval,
    TEXT("检查剩余可用物理内存间隔\n")
    TEXT("检查到内存不足时就开始释放缓存\n"),
    ECVF_Cheat
    );
}

void USmallResourceCache::Deinitialize()
{
    FWorldDelegates::OnPostWorldInitialization.Remove(WorldDelegateHandle);
}

void USmallResourceCache::OnLoadCache()
{
    FStreamableManager& Streamable = UAssetManager::GetStreamableManager();
    const int32 SingleMaxLoadCache_KB = Config->SingleMaxLoadCache * 1024;

    int64 AvailablePhysical_KB = GetAvailablePhysical_KB();
    int32 NowLoadCacheMemory_KB = 0;
    while (AvailablePhysical_KB > 0 && NowCacheIndex + 1 < AllCacheResourceData.Num() && NowLoadCacheMemory_KB < SingleMaxLoadCache_KB)
    {
        ++NowCacheIndex;
        FCacheInfo& CacheInfo = AllCacheResourceData[NowCacheIndex];
        if(Streamable.LoadSynchronous(CacheInfo.ResourceInfo.ResourcePath, true, &CacheInfo.StreamableHandlePtr))
        {
            AvailablePhysical_KB -= CacheInfo.ResourceInfo.GetMemorySize_KB();
            NowLoadCacheMemory_KB += CacheInfo.ResourceInfo.GetMemorySize_KB();
            NowCacheMemory_KB += CacheInfo.ResourceInfo.GetMemorySize_KB();
        }
    }
}

void USmallResourceCache::OnCheckMemory()
{
    int64 AvailablePhysical = GetAvailablePhysical_KB();
    //达不到预留内存时开始释放缓存
    if(AvailablePhysical < 0) OnReleaseCache(AvailablePhysical * -1);
}

void USmallResourceCache::OnReleaseCache(int64 MemorySize_KB)
{
    bool bIsGc = false;
    while(MemorySize_KB > 0 && NowCacheIndex >= 0)
    {
        FCacheInfo& CacheInfo = AllCacheResourceData[NowCacheIndex];
        if(CacheInfo.StreamableHandlePtr.IsValid())
        {
            CacheInfo.StreamableHandlePtr->ReleaseHandle();
            MemorySize_KB -= CacheInfo.ResourceInfo.GetMemorySize_KB();
            NowCacheMemory_KB -= CacheInfo.ResourceInfo.GetMemorySize_KB();
            bIsGc = true;
        }
        --NowCacheIndex;
    }

    if(bIsGc) GEngine->ForceGarbageCollection();
}

int64 USmallResourceCache::GetAvailablePhysical_KB() const
{
    FPlatformMemoryStats MemoryStats = FPlatformMemory::GetStats();

    uint64 EstimatingGameMemoryUsage = static_cast<uint64>(Config->EstimatingGameMemoryUsage) * 1024 * 1024;
    uint64 AvailablePhysical;
    if(MemoryStats.UsedPhysical >= EstimatingGameMemoryUsage)
        AvailablePhysical = MemoryStats.AvailablePhysical;
    else
        AvailablePhysical = MemoryStats.AvailablePhysical - (EstimatingGameMemoryUsage - MemoryStats.UsedPhysical);

    int64 ReservedMemory_KB = static_cast<int64>(Config->ReservedMemory) * 1024;
    return static_cast<int64>(AvailablePhysical / 1024) - ReservedMemory_KB;
}

void USmallResourceCache::OnShowDebugInfo(AHUD* HUD, UCanvas* Canvas, const FDebugDisplayInfo& DisplayInfo, float& YL, float& YPos)
{
    static const FName NAME_SmallResourceCache("SmallResourceCache");
    if (Canvas && HUD->ShouldDisplayDebug(NAME_SmallResourceCache))
    {
        FDisplayDebugManager& DisplayDebugManager = Canvas->DisplayDebugManager;
        DisplayDebugManager.SetFont(GEngine->GetSmallFont());
        DisplayDebugManager.SetDrawColor(FColor::Yellow);
        DisplayDebugManager.DrawString(FString::Printf(TEXT("SmallResourceCache 小资源缓存状态")));

        DisplayDebugManager.SetDrawColor(FColor::Cyan);
        DisplayDebugManager.DrawString(FString::Printf(TEXT("AllCacheResourceDataNum = %d"), AllCacheResourceData.Num()));
        DisplayDebugManager.DrawString(FString::Printf(TEXT("NowCacheIndex = %d"), NowCacheIndex));
        DisplayDebugManager.DrawString(FString::Printf(TEXT("当前空闲可缓存内存 %lld MB"), GetAvailablePhysical_KB() / 1024));
        DisplayDebugManager.DrawString(FString::Printf(TEXT("当前缓存内存占用 %lld MB (这个不是很准,只能看个大概)"), NowCacheMemory_KB / 1024));
        
        DisplayDebugManager.SetDrawColor(FColor::Yellow);
        DisplayDebugManager.DrawString(FString::Printf(TEXT("SmallResourceCache 小资源缓存配置")));
        DisplayDebugManager.DrawString(FString::Printf(TEXT("可以通过控制台命令 CS3_Cache.xxx 修改以下配置")));

        DisplayDebugManager.SetDrawColor(FColor::Cyan);
        DisplayDebugManager.DrawString(FString::Printf(TEXT("SingleMaxLoadCache = %d MB //每次切换关卡时最多加载多少缓存"), Config->SingleMaxLoadCache));
        DisplayDebugManager.DrawString(FString::Printf(TEXT("EstimatingGameMemoryUsage = %d MB //预计正常游戏最大会占用的内存量"), Config->EstimatingGameMemoryUsage));
        DisplayDebugManager.DrawString(FString::Printf(TEXT("ReservedMemory = %d MB //预留给系统的空闲内存"), Config->ReservedMemory));
        DisplayDebugManager.DrawString(FString::Printf(TEXT("CheckMemoryInterval = %f秒 //检查剩余可用物理内存间隔"), Config->CheckMemoryInterval));
        DisplayDebugManager.DrawString(FString::Printf(TEXT("所有可缓存资源总大小: %d KB"), ResourceDataTotalMemorySize_KB));
    }
}
