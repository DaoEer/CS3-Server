// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3GameViewportClient.h"
#include "SignificanceManager.h"
#include "Kismet/GameplayStatics.h"
#include "SceneView.h"
#include "Engine/LocalPlayer.h"
#include "Actor/GameCharacter.h"
#include "Util/CS3Debug.h"

CSV_DEFINE_STAT_GLOBAL(FPS);
CSV_DEFINE_CATEGORY(T,true);

CONTROL_COMPILE_OPTIMIZE_START
void UCS3GameViewportClient::Tick(float DeltaTime)
{
 	UGameViewportClient::Tick(DeltaTime);
    const float NowFps = 1.f / (FApp::GetCurrentTime() - FApp::GetLastTime());
	CSV_CUSTOM_STAT_DEFINED(FPS, NowFps, ECsvCustomStatOp::Set);
 	// 更新Significance系统
 	{
 		// 确保具有有效的世界场景和Significance Manager实例。
 		if (World)
 		{
 			if (USignificanceManager* SignificanceManager = FSignificanceManagerModule::Get(World))
 			{
 				// 仅使用玩家0的全局变换，每帧更新一次。
 				if (APlayerCameraManager* PlayerCameraManager = UGameplayStatics::GetPlayerCameraManager(World, 0))
 				{
					// 检查ManagedObjectInfo得有效性
					{
						TArray<USignificanceManager::FManagedObjectInfo*> OutManagedObjects;
						SignificanceManager->GetManagedObjects(OutManagedObjects);
						for (auto ManagedObjectInfo : OutManagedObjects)
						{
							UObject* Object = ManagedObjectInfo->GetObject();
							if (!IsValid(Object) || !Object->IsValidLowLevel() || !IsValid(Object->GetWorld()) || !Object->GetWorld()->IsValidLowLevel()) // 将无效的FManagedObjectInfo删除,防止在后面得更新中报错
							{
								SignificanceManager->UnregisterObject(Object);
							}
						}
					}

 					// 更新view信息
 					{
 						ProjMatrix = PlayerCameraManager->ViewTarget.POV.CalculateProjectionMatrix();
 					}
 
 					// 更新重要度
 					{
 						// Significance Manager使用ArrayView。构造单元素数组来容纳Transform。
 						TArray<FTransform> TransformArray;
 						TransformArray.Add(FTransform(PlayerCameraManager->GetCameraRotation(), PlayerCameraManager->GetCameraLocation()));
 						// 使用通过ArrayView传入的单元素数组来更新Significance Manager。
 						SignificanceManager->Update(TArrayView<FTransform>(TransformArray));
 					}
 
 					// 重要度整体后处理
 					{
 						// 限制最大SignificanceType::Complete重要度的Actor数量
 						{
 							static const FName PlayerName = TEXT("PlayerCharacter");
 							static const FName MonsterName = TEXT("MonsterCharacter");
 
 							auto Fun = [SignificanceManager](const FName& TagName, int Limit)
 							{
 								int CompleteCount = 0;
 								const TArray<USignificanceManager::FManagedObjectInfo*>& OutManagedObjects = SignificanceManager->GetManagedObjects(TagName);
 
 								// OutManagedObjects是已经排序过的,所以将保留前Limit个SignificanceType::Complete, 后面的降为SignificanceType::Near
 								for (auto ManagedObjectInfo : OutManagedObjects)
 								{
 									AGameCharacter* GameCharacter = Cast<AGameCharacter>(ManagedObjectInfo->GetObject());
 									if (GameCharacter->Significance == SignificanceType::Complete)
 									{
 										if (++CompleteCount > Limit)
 										{
 											GameCharacter->Significance = SignificanceType::Near;
 										}
 									}
 									else
 									{
 										// 后面肯定没有SignificanceType::Complete了
 										return;
 									}
 								}
 							};
 
 							Fun(PlayerName, 10);
 							Fun(MonsterName, 15);
 						}
 
 						// 触发AGameCharacter::OnSignificanceChange()事件
 						{
 							TArray<USignificanceManager::FManagedObjectInfo*> AllObjects;
 							SignificanceManager->GetManagedObjects(AllObjects);
 							for (auto ManagedObjectInfo : AllObjects)
 							{
 								AGameCharacter* GameCharacter = Cast<AGameCharacter>(ManagedObjectInfo->GetObject());
 								if (GameCharacter->Significance != GameCharacter->OldSignificance)
 								{
 									GameCharacter->OnSignificanceChange();
 								}
 							}
 						}
 					}
 				}
 			}
 		}
 	}
}

void UCS3GameViewportClient::Init(FWorldContext& WorldContext, UGameInstance* OwningGameInstance, bool bCreateNewAudioDevice)
{
	Super::Init(WorldContext, OwningGameInstance, bCreateNewAudioDevice);
	FWorldDelegates::OnPreWorldInitialization.AddLambda([this](UWorld* NewWorld, const UWorld::InitializationValues InitializationValues)
	{
        CSV_EVENT_GLOBAL(TEXT("EnterWorld %s"), *NewWorld->GetName());

		static FTimerHandle Handle;
		if(Handle.IsValid())
		{
			NewWorld->GetTimerManager().ClearTimer(Handle);
		}
        NewWorld->GetTimerManager().SetTimer(Handle, []()
        {
        	CSV_EVENT(T, TEXT("  %s"), *FDateTime::Now().ToString(TEXT("%H:%M:%S"))); 
        }, 5.f, true);
    });
}

CONTROL_COMPILE_OPTIMIZE_END
