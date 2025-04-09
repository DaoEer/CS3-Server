// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotify_CustomMotionBlur.h"
#include "Components/SkeletalMeshComponent.h"
#include "Manager/MotionBlurManager.h"


UAnimNotify_CustomMotionBlur::UAnimNotify_CustomMotionBlur()
	:Super(),
	DefaultMesh(nullptr)
{
#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(255, 128, 25, 0);
#endif // WITH_EDITORONLY_DATA
}


void UAnimNotify_CustomMotionBlur::PostLoad()
{
	Super::PostLoad();
}
// 
// #if WITH_EDITOR
// void UAnimNotify_CustomMotionBlur::PostEditChangeProperty(struct FPropertyChangedEvent& PropertyChangedEvent)
// {
// 	Super::PostEditChangeProperty(PropertyChangedEvent);
// 
// 	if (PropertyChangedEvent.MemberProperty && PropertyChangedEvent.MemberProperty->GetFName() == GET_MEMBER_NAME_CHECKED(UAnimNotify_PlayParticleEffect, RotationOffset))
// 	{
// 		RotationOffsetQuat = FQuat(RotationOffset);
// 	}
// }
// #endif

FString UAnimNotify_CustomMotionBlur::GetNotifyName_Implementation() const
{
	return Super::GetNotifyName_Implementation();
}

void UAnimNotify_CustomMotionBlur::Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
// 	if (Materials.Num() < BlurCount)
// 	{
// 		UE_LOG(LogScript, Warning, TEXT("UAnimNotify_CustomMotionBlur::Notify: Materials.Num < BlurCount!"));
// 		return;
// 	}

	UMotionBlurManager* MotionBlurManager = UMotionBlurManager::GetInstance();
	if (IsValid(MotionBlurManager))
	{
		//MotionBlurManager->CreateBlurMeshes(MeshComp, Lifetime, BlurCount, IntervalTime, Materials, DefaultMesh);
		MotionBlurManager->CreateBlurMeshesDirect(MeshComp, Lifetime, Materials[0], DefaultMesh, TickPos);
	}
// 	UWorld* World = MeshComp->GetWorld();
// 	TArray<MeshMatchData> meshes = _GetMeshAttachedChildren(MeshComp);
// 	if (World)
// 	{
// 		AMotionBlurMgr* MotionBlurMgr = _FindMotionBlurMgr(World);
// 		if (!MotionBlurMgr)
// 			MotionBlurMgr = World->SpawnActor<AMotionBlurMgr>();
// 		if (MotionBlurMgr)
//` 			//MotionBlurMgr->CreateBlurOneMesh(MeshComp, Lifetime, BlurCount, IntervalTime, Materials);
// 			MotionBlurMgr->CreateBlurMeshes(meshes, Lifetime, BlurCount, IntervalTime, Materials);
// 
// 		UMotionBlurManager* manager = UMotionBlurManager::GetInstance();
// 		if (manager)
// 		{
// 			//manager->CreateBlurMeshes(MeshComp, Lifetime);
// 		}
// 	}
}

void UAnimNotify_CustomMotionBlur::StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{
	UWorld* World = MeshComp->GetWorld();
	UMotionBlurManager* manager = UMotionBlurManager::GetInstance();
	if (manager)
	{
		manager->DestroyRealMgrInWorld(World);
	}
}
