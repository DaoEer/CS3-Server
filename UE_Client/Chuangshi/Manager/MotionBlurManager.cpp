// Fill out your copyright notice in the Description page of Project Settings.


#include "MotionBlurManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/CustomEffect/Blur/MotionBlurMgr.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/MeshComponent.h"
#include "Materials/MaterialInterface.h"
#include "Components/SceneComponent.h"
#include "Engine/World.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

UMotionBlurManager* UMotionBlurManager::Instance = nullptr;

UMotionBlurManager::UMotionBlurManager()
{
}

UMotionBlurManager::~UMotionBlurManager()
{
// 	if (CurDecalData)
// 	{
// 		delete CurDecalData;
// 		CurDecalData = nullptr;
// 	}
}

UMotionBlurManager* UMotionBlurManager::GetInstance()
{
	//-----------------------------------------------------------------
	// UMotionBlurManager 设定为独立单键，UMotionBlurManager内的东西和通过每个world自身来创建	
	// 编辑器不启动游戏也需要能获取此单键,所以不希望和UUECS3GameInstance绑定，
	// zhengxuemei,2020年3月19日09:51:39，如需修改请慎重。
	if (!IsValid(Instance))
	{
		Instance = NewObject<UMotionBlurManager>();
		Instance->AddToRoot();
	}
	return Instance;
	//-----------------------------------------------------------------
}

void UMotionBlurManager::ClearInstance()
{
	Instance = nullptr;
}

void UMotionBlurManager::BeginDestroy()
{
	Super::BeginDestroy();
}

// void UMotionBlurManager::CreateBlurMeshes(const TArray<MeshMatchData>& Meshes, float Lifetime, int Count, float IntervalTime, TArray<UMaterialInterface*> Materials)
// {
// 	if (Instance && IsValid(Instance))
// 	{
// 		if (RealMgr && IsValid(RealMgr))
// 			RealMgr->CreateBlurMeshes(Meshes, Lifetime, Count, IntervalTime, Materials);
// 	}
// }

void UMotionBlurManager::CreateBlurMeshes(UMeshComponent* ParentMeshComp, float Lifetime, USkeletalMesh* DefaultMesh, bool TickPos)
{
	TArray<UMaterialInterface*> arrMat;
	arrMat.Empty();
	CreateBlurMeshes(ParentMeshComp, Lifetime, 1, 1, arrMat, DefaultMesh, TickPos);
}

void UMotionBlurManager::CreateBlurMeshes(UMeshComponent* ParentMeshComp, float Lifetime, int Count, float IntervalTime, 
	TArray<UMaterialInterface*> Materials, USkeletalMesh* DefaultMesh, bool TickPos)
{
	if (IsValid(Instance))
	{
		AMotionBlurMgr* RealMgr = FindOrSpawnMotionBlurMgr(ParentMeshComp->GetWorld());
		if (IsValid(RealMgr))
		{
			TArray<MeshMatchData> meshes = GetAttachedOriginMesh(ParentMeshComp, DefaultMesh);
			RealMgr->CreateBlurMeshes(meshes, Lifetime, Count, IntervalTime, Materials, TickPos);
		}	
	}
}

APoseableBlur* UMotionBlurManager::CreateBlurMeshesDirect(UMeshComponent* ParentMeshComp, float Lifetime, UMaterialInterface* Material, USkeletalMesh* DefaultMesh, bool TickPos)
{
	if (IsValid(Instance))
	{
		AMotionBlurMgr* RealMgr = FindOrSpawnMotionBlurMgr(ParentMeshComp->GetWorld());
		if (IsValid(RealMgr))
		{
			TArray<MeshMatchData> meshes = GetAttachedOriginMesh(ParentMeshComp, DefaultMesh);
			return RealMgr->CreateBlurMeshesDirect(meshes, Lifetime, Material, TickPos);
		}
	}
	return nullptr;
}

TArray<MeshMatchData> UMotionBlurManager::GetAttachedOriginMesh(UMeshComponent* ParentMeshComp, USkeletalMesh* DefaultMesh)
{
	TArray<USceneComponent*> MeshAttached;
	ParentMeshComp->GetChildrenComponents(false, MeshAttached);
	TArray<MeshMatchData> ret;
	
	if (DefaultMesh)// 模型组件使用默认模型
	{
		ret.Add(MeshMatchData(ParentMeshComp, DefaultMesh));
	}
	else // 使用原始模型
	{
		// 先将自己加入列表
		// 因为ParentMeshComp可能不是USkeletalMeshComponent，有可能是DebugSkelMeshComponent（动画窗口中的）
		// 所以就直接转吧
	/*	UClass* MeshCptClass = ParentMeshComp->GetClass();
		if (MeshCptClass == UStaticMeshComponent::StaticClass())
		{
			ret.Add(MeshMatchData(ParentMeshComp, Cast<UStaticMeshComponent>(ParentMeshComp)->GetStaticMesh()));
		}
		else if (MeshCptClass == USkeletalMeshComponent::StaticClass() 
			//|| MeshCptClass == UDebugSkelMeshComponent::StaticClass()
			)
		{
			ret.Add(MeshMatchData(ParentMeshComp, Cast<USkeletalMeshComponent>(ParentMeshComp)->SkeletalMesh));
		}*/
		UStaticMeshComponent* StaticMeshComp = Cast<UStaticMeshComponent>(ParentMeshComp);
		if (IsValid(StaticMeshComp))
		{
			ret.Add(MeshMatchData(StaticMeshComp, StaticMeshComp->GetStaticMesh()));
		}
		USkeletalMeshComponent* USkeletalMeshComp = Cast<USkeletalMeshComponent>(ParentMeshComp);
		if (IsValid(USkeletalMeshComp))
		{
			ret.Add(MeshMatchData(USkeletalMeshComp, USkeletalMeshComp->SkeletalMesh));
		}

		for (USceneComponent* comp : MeshAttached)
		{

			StaticMeshComp = Cast<UStaticMeshComponent>(comp);
			if (IsValid(StaticMeshComp)&& StaticMeshComp->IsVisible())
			{
				ret.Add(MeshMatchData(StaticMeshComp, StaticMeshComp->GetStaticMesh()));
				continue;
			}

			USkeletalMeshComp = Cast<USkeletalMeshComponent>(comp);
			if (IsValid(USkeletalMeshComp) && USkeletalMeshComp->IsVisible())
			{
				ret.Add(MeshMatchData(USkeletalMeshComp, USkeletalMeshComp->SkeletalMesh));
				continue;
			}
		}
	}	
	return ret;
}

void UMotionBlurManager::DestroyRealMgrInWorld(UWorld* World)
{
	AMotionBlurMgr* Mgr = GetMotionBlurMgr(World);
	if (IsValid(Mgr))
	{
		Mgr->Destroyed();
	}
}

AMotionBlurMgr* UMotionBlurManager::FindOrSpawnMotionBlurMgr(UWorld* World)
{
	AMotionBlurMgr* Mgr = GetMotionBlurMgr(World);
	//world没有生成过就生成一个
	if (!IsValid(Mgr))
	{
		Mgr = World->SpawnActor<AMotionBlurMgr>();
	}
	return Mgr;
}

AMotionBlurMgr* UMotionBlurManager::GetMotionBlurMgr(UWorld* World)
{
	AMotionBlurMgr* Mgr = nullptr;
	if (ULevel* TestLevel = World->PersistentLevel)
	{
		for (AActor* Actor : TestLevel->Actors)
		{
			if (!IsValid(Actor))
				continue;

			UClass* MeshCptClass = Actor->GetClass();
			if (MeshCptClass == AMotionBlurMgr::StaticClass())
			{
				Mgr = Cast<AMotionBlurMgr>(Actor);
				if (IsValid(Mgr))
				{
					return Mgr;
				}
			}
		}
	}
	return nullptr;
}

// 
// AMotionBlurMgr* UMotionBlurManager::CheckMotionBlurMgr()
// {
// 	if (Instance && IsValid(Instance))
// 	{
// 		if (RealMgr)
// 		{
// 			if (Instance->GetWorld() != RealMgr->GetWorld())
// 			{
// 				RealMgr->Destroyed();
// 				RealMgr = Instance->GetWorld()->SpawnActor<AMotionBlurMgr>();
// 				RealMgr->AddToRoot();
// 			}
// 		}
// 		else
// 		{
// 			RealMgr = Instance->GetWorld()->SpawnActor<AMotionBlurMgr>();
// 			RealMgr->AddToRoot();
// 		}
// 	}
// 	return RealMgr;
// }

CONTROL_COMPILE_OPTIMIZE_END

