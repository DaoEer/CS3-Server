// Fill out your copyright notice in the Description page of Project Settings.

#include "MotionBlurMgr.h"
#include "MeshBlur.h"
#include "SkeletalMeshBlur.h"
#include "PoseableBlur.h"
#include "GameFramework/Actor.h"
#include "Util/CS3Debug.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"



// Sets default values
AMotionBlurMgr::AMotionBlurMgr()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
}

// Called when the game starts or when spawned
void AMotionBlurMgr::BeginPlay()
{
	Super::BeginPlay();
	
}

// Called every frame
void AMotionBlurMgr::Tick( float DeltaTime )
{
	Super::Tick( DeltaTime );

	// 创建
	for (int i = 0; i < OriginalData.Num(); i++)
	{
		FBlurData* data = OriginalData[i];
		data->IntervalTimer += DeltaTime;
		// 第一次或者间隔时间到了
		if ((data->CreatedBlurCount == 0 || data->IntervalTimer >= data->IntervalTime) && data->CreatedBlurCount < data->Count)
		{
			for (const MeshMatchData& mesh : data->Meshes)	
			{
				if (mesh.MatchMesh.IsValid())
				{
					if (data->CreatedBlurCount < data->Materials.Num())
						_CreateSingleBlur(mesh, data->Lifetime, data->Materials[data->CreatedBlurCount], data->TickPos);
					else
						_CreateSingleBlur(mesh, data->Lifetime, nullptr, data->TickPos);
				}
			}
			data->CreatedBlurCount += 1;
			data->IntervalTimer = 0.0f;
		}
		if (data->CreatedBlurCount == data->Count)
		{
			delete data;
			OriginalData.RemoveAt(i);
		}
	}
	// 检查残影生命结束就删除
	for (int i = 0; i < BlurArray.Num(); i++)
	{
		AMeshBlur* blur = BlurArray[i];
		if (blur->Lifetimer >= blur->Lifetime)
		{
			if (IsValid(blur))
			{
				blur->Destroy();
			}
			BlurArray.RemoveAt(i);
		}
	}
// 	for (AMotionBlur* blur : BlurArray)
// 	{
// 		if (blur &&(blur->Lifetimer >= blur->Lifetime))
// 		{
// 			blur->Destroy();
// 			//BlurArray.Remove(blur);// 会卡！
// 		}
// 	}
}

void AMotionBlurMgr::Destroyed()
{
	for (int i = 0; i < OriginalData.Num(); i++)
	{
		delete OriginalData[i];
	}
	OriginalData.Empty();
	for (int i = 0; i < BlurArray.Num(); i++)
	{
		BlurArray[i]->Destroy();
	}
	BlurArray.Empty();
}

bool AMotionBlurMgr::ShouldTickIfViewportsOnly() const
{
	return true;
}

void AMotionBlurMgr::CreateBlurMeshes(const TArray<MeshMatchData>& Meshes, float Lifetime, int Count, float IntervalTime, TArray<UMaterialInterface*> Materials, bool TickPos)
{
	//AMotionBlurMgr::Destroyed()中释放
	FBlurData* blur = new FBlurData(Meshes, Lifetime, Count, IntervalTime, Materials, TickPos);
	OriginalData.Add(blur);
}

void AMotionBlurMgr::CreateBlurOneMesh(const MeshMatchData& Mesh, float Lifetime, int Count, float IntervalTime, TArray<UMaterialInterface*> Materials, bool TickPos)
{
	TArray<MeshMatchData> Meshes;
	Meshes.Add(Mesh);
	//AMotionBlurMgr::Destroyed()中释放
	FBlurData* blur = new FBlurData(Meshes, Lifetime, Count, IntervalTime, Materials, TickPos);
	OriginalData.Add(blur);
}

APoseableBlur* AMotionBlurMgr::CreateBlurMeshesDirect(const TArray<MeshMatchData>& Meshes, float Lifetime, UMaterialInterface* Material, bool TickPos)
{
// 	TArray<AMeshBlur*> arrRet;
// 	for (const MeshMatchData& mesh : Meshes)
// 	{
// 		AMeshBlur* blur = _CreateSingleBlur(mesh, Lifetime, Material, TickPos);
// 		if (blur != nullptr)
// 			arrRet.Add(blur);
// 	}
// 	return arrRet;
	UWorld* World = GetWorld();
	if (!World)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMotionBlurMgr::CreateBlurMeshesDirect: World!"));
		return nullptr;
	}
	APoseableBlur* Blur = World->SpawnActor<APoseableBlur>();
	if (!Blur->CreateBlur(Meshes, Lifetime, Material, TickPos))
	{
		Blur->Destroy();
		return nullptr;
	}
	return Blur;
}

AMeshBlur* AMotionBlurMgr::_CreateSingleBlur(const MeshMatchData& Mesh, float Lifetime, UMaterialInterface* Material, bool TickPos)
{
	UWorld* World = GetWorld();
	if (!World)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMotionBlurMgr::_CreateSingleBlur: World!"));
		return nullptr;
	}
	if (!Mesh.MeshComp.IsValid()||!Mesh.MatchMesh.IsValid())
	{
		return nullptr;
	}
	AMeshBlur* Blur = nullptr;
	UMeshComponent* MeshComp = Mesh.MeshComp.Get();	// 要创建的模型组件
	UObject* MatchMesh = Mesh.MatchMesh.Get();
	if (MeshComp->IsA(USkeletalMeshComponent::StaticClass()) && Cast<USkeletalMeshComponent>(MeshComp)->SkeletalMesh)
	{
		Blur = World->SpawnActor<ASkeletalMeshBlur>();
		if (!Blur->CreateBlur(Cast<USkeletalMeshComponent>(MeshComp), MatchMesh, Lifetime, Material, TickPos))
		{
			Blur->Destroy();
			return nullptr;
		}
	}
	else if (MeshComp->IsA(UStaticMeshComponent::StaticClass()) && Cast<UStaticMeshComponent>(MeshComp)->GetStaticMesh())
	{
		Blur = World->SpawnActor<AMeshBlur>();
		if (!Blur->CreateBlur(Cast<UStaticMeshComponent>(MeshComp), MatchMesh, Lifetime, Material, TickPos))
		{
			Blur->Destroy();
			return nullptr;
		}
	}
	if (!Blur)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMotionBlurMgr::_CreateSingleBlur: Blur!"));
		return nullptr;
	}
	BlurArray.Add(Blur);
	return Blur;
}

