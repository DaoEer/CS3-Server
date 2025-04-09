// Fill out your copyright notice in the Description page of Project Settings.


#include "SkeletalMeshBlur.h"
#include "GameFramework/Actor.h"
#include "Components/PoseableMeshComponent.h"
#include "Util/CS3Debug.h"

// Sets default values
ASkeletalMeshBlur::ASkeletalMeshBlur()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	PoseableMesh = CreateDefaultSubobject<UPoseableMeshComponent>(TEXT("PoseableMesh"));
	PoseableMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	MeshComp = PoseableMesh;
	m_bTickPos = false;
}

void ASkeletalMeshBlur::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
}

void ASkeletalMeshBlur::Destroyed()
{
	if (CopyTimeHandle.IsValid())
	{
		GetWorld()->GetTimerManager().ClearTimer(CopyTimeHandle);
	}
	if (PoseableMesh)
		PoseableMesh->DestroyComponent();
	MeshComp = nullptr;
}

bool ASkeletalMeshBlur::CreateBlur(UMeshComponent* Mesh, UObject* Obj, float Life, UMaterialInterface* Material, bool TickPos)
{
	m_ParentMesh = Cast<USkeletalMeshComponent>(Mesh);
	if (!m_ParentMesh)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ASkeletalMeshBlur::CreateBlur: SkeletalMesh!"));
		return false;
	}
	RootComponent = PoseableMesh;
	PoseableMesh->SetWorldTransform(m_ParentMesh->GetComponentToWorld());
	PoseableMesh->CopyPoseFromSkeletalComponent(m_ParentMesh);

	PoseableMesh->SetSkeletalMesh(Cast<USkeletalMesh>(Obj));
	PoseableMesh->bRenderCustomDepth = true;
	//PoseableMesh->SetSkeletalMesh(MyMesh);
	for (const FName& name : m_ParentMesh->GetAllSocketNames())
	{
		PoseableMesh->SetBoneTransformByName(name, m_ParentMesh->GetSocketTransform(name), EBoneSpaces::WorldSpace);
	}
	TArray<class UMaterialInterface*> materials = PoseableMesh->GetMaterials();
	for (int i = 0; i < materials.Num(); i++)
	{
		PoseableMesh->CreateAndSetMaterialInstanceDynamicFromMaterial(i, Material);
		//PoseableMesh->SetMaterial(i, Material);
	}
	Lifetime = Life + FadeOutTime;
	m_bTickPos = TickPos;
	if (TickPos)
	{
		GetWorld()->GetTimerManager().SetTimer(CopyTimeHandle, this, &ASkeletalMeshBlur::CopyTimerEvent,0.1f, true);
	}
	return true;
}

UPoseableMeshComponent* ASkeletalMeshBlur::GetPoseableMesh()
{
	return PoseableMesh;
}

void ASkeletalMeshBlur::CopyTimerEvent()
{
	if (IsValid(ParentPoseMesh))
	{
		PoseableMesh->CopyPoseFromSkeletalComponent(ParentPoseMesh);
	}else
	{
		if (IsValid(PoseableMesh) && IsValid(m_ParentMesh))
		{
			PoseableMesh->CopyPoseFromSkeletalComponent(m_ParentMesh);
		}
	}

}

