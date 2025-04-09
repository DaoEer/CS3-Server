// Fill out your copyright notice in the Description page of Project Settings.

#include "AnimNotify_Transparency.h"
// UE4
#include "Components/SkeletalMeshComponent.h"
// ²å¼þ
#include "TransActorCapture.h"
// CS3ÀàÐÍ
#include "Util/ConvertUtil.h"
#include "GameDevelop/CS3GameInstance.h"

FString UAnimNotify_Transparency::GetNotifyName_Implementation() const
{
	if (TransType == Transparency_Type::ADDTRANS)
	{
		return FString(TEXT("AddTrans : ")) + FLOAT_TO_FSTRING(Alpha);
	}
	else
	{
		return FString(TEXT("RomoveTrans"));
	}
}

void UAnimNotify_Transparency::Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	AActor* Owner = MeshComp->GetOwner();
	if (!IsValid(Owner) || !UUECS3GameInstance::Instance)
	{
		return;
	}

	if (TransType == Transparency_Type::ADDTRANS)
	{
		ATransActorCapture::SetTransActor(Owner, 1.f - Alpha);
	}
	else 
	{
		ATransActorCapture::RemoveTransActor(Owner);
	}
}

void UAnimNotify_Transparency::StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{
	AActor* Owner = MeshComp->GetOwner();
	if (!IsValid(Owner) || !UUECS3GameInstance::Instance)
	{
		return;
	}

	if (TransType == Transparency_Type::ADDTRANS)
	{
		ATransActorCapture::RemoveTransActor(Owner);
	}
}
