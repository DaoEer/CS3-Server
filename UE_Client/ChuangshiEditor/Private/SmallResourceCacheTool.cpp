#include "SmallResourceCacheTool.h"
#include "AssetRegistryModule.h"
#include "ScopedSlowTask.h"
#include "Util/SmallResourceCache/SmallResourceData.h"

#define LOCTEXT_NAMESPACE "SmallResourceCacheTool"

void USmallResourceCacheTool::GeneratingData()
{
    FAssetRegistryModule& AssetRegistryModule = FModuleManager::LoadModuleChecked<FAssetRegistryModule>(TEXT("AssetRegistry"));
    IAssetRegistry& AssetRegistry = AssetRegistryModule.Get();

    TArray<UObject*> SelectedAssets = GetSelectedAssets();
    FScopedSlowTask SelectedObjectProgress(SelectedAssets.Num(), LOCTEXT("SelectedObjectProgress", "给选中的 SmallResourceData 自动生成数据"));
    SelectedObjectProgress.MakeDialog();
    for(auto SelectedObject : SelectedAssets)
    {
        SelectedObjectProgress.EnterProgressFrame(1.f, FText::FromString(TEXT("自动生成数据: ") + SelectedObject->GetName()));
        if(USmallResourceData* SmallResourceData = Cast<USmallResourceData>(SelectedObject))
        {
            FARFilter Filter;
            
            //先将目标目录扫描一遍
            TArray<FString> FilePaths;
            for(const auto& FilePath : SmallResourceData->ContentPaths)
            {
                FilePaths.Add(FilePath.Path);
                Filter.PackagePaths.Add(FName(*FilePath.Path));
            }
            AssetRegistry.ScanFilesSynchronous(FilePaths, true);

            //筛选出指定类型的资源
            Filter.bRecursiveClasses = true;
            Filter.bRecursivePaths = true;
            for(const auto Class : SmallResourceData->ResourceClass)
            {
                Filter.ClassNames.Add(Class->GetFName());
            }
            TArray<FAssetData> AssetList;
            AssetRegistry.GetAssets(Filter, AssetList);

            //加载资源
            FScopedSlowTask LoadProgress(AssetList.Num(), LOCTEXT("LoadProgress", "加载扫描到的资源"));
            LoadProgress.MakeDialog();
            TArray<UObject*> ObjectList;
            for(const auto& AssetData : AssetList)
            {
                LoadProgress.EnterProgressFrame(1.f, FText::FromString(TEXT("加载资源: ") + AssetData.GetFullName()));
                if(UObject* Object = AssetData.GetAsset())
                {
                    ObjectList.Add(Object);
                }
            }
            LoadProgress.Destroy();
            
            //按照内存占用从小到大排序
            FScopedSlowTask SortProgress(0, LOCTEXT("ObjectList.Sort", "对所有资源按照内存占用大小排序"));
            SortProgress.MakeDialog();
            ObjectList.Sort([&SortProgress](UObject& A, UObject& B)
            {
                SortProgress.EnterProgressFrame();
                return A.GetResourceSizeBytes(EResourceSizeMode::Exclusive) < B.GetResourceSizeBytes(EResourceSizeMode::Exclusive);
            });
            SortProgress.Destroy();

            //从小到大填入数据引用
            FScopedSlowTask FillProgress(1.f, LOCTEXT("FillProgress", "从小到大填充ResourceData"));
            FillProgress.MakeDialog();
            SmallResourceData->ResourceData.Empty();
            SIZE_T NowTotalMemorySize = 0; //单位是字节
            SIZE_T TotalSize = SmallResourceData->TotalMemorySize * 1024 * 1024;
            for(auto Object : ObjectList)
            {
                if(NowTotalMemorySize / 1024 / 1024 >= SmallResourceData->TotalMemorySize) break;

                SIZE_T Size = Object->GetResourceSizeBytes(EResourceSizeMode::Exclusive);
                FillProgress.EnterProgressFrame((double)Size / (double)TotalSize, FText::FromString(TEXT("填充资源引用: ") + Object->GetPathName()));
                SmallResourceData->ResourceData.Add(FResourceDataInfo{
                    FSoftObjectPath{Object},
                    static_cast<int32>(Size < 1024 ? 1 : Size / 1024)
                });
                SmallResourceData->ResourceDataTotalMemorySize_KB += static_cast<int32>(Size < 1024 ? 1 : Size / 1024); 
                NowTotalMemorySize += Size;
            }
            SmallResourceData->Modify();
        }
    }
}

#undef LOCTEXT_NAMESPACE