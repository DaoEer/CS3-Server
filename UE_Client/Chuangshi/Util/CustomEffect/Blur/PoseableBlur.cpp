// Fill out your copyright notice in the Description page of Project Settings.
#include "PoseableBlur.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Components/PoseableMeshComponent.h"
#include "Util/CS3Debug.h"

// Sets default values
APoseableBlur::APoseableBlur()
{
	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.


// 	StaticMeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("StaticMesh"));
// 	StaticMeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
// 	DefaultSceneRoot = StaticMeshComp;
	DefaultSceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	PoseableBlurMesh = CreateDefaultSubobject<UPoseableMeshComponent>(TEXT("PoseableBlurMesh"));
	PrimaryActorTick.bCanEverTick = true;
	ParentPoseMesh = nullptr;
	FadeOutTime = 0.5f;
	FadeOutTimer = 0.f;
}

// Called when the game starts or when spawned
void APoseableBlur::BeginPlay()
{
	Super::BeginPlay();
}

// Called every frame
void APoseableBlur::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	Lifetimer += DeltaTime;

	for (int i = 0; i < m_MesheComps.Num(); i++)
	{
		if (Lifetimer >= Lifetime)
		{
			Destroy();
		}
		else if (Lifetimer >= Lifetime - FadeOutTime)
		{
			FadeOutTimer += DeltaTime;
			TArray<class UMaterialInterface*> materials = m_MesheComps[i]->GetMaterials();
			for (auto mat : materials)
			{
				UMaterialInstanceDynamic* MatDyn = Cast<UMaterialInstanceDynamic>(mat);
				if (MatDyn)
					MatDyn->SetScalarParameterValue(TEXT("OpacityIntensity"), (1 - FadeOutTimer / FadeOutTime));
			}
		}
	}
}

void APoseableBlur::Destroyed()
{
	for (int i = 0; i < m_MesheComps.Num(); i++)
	{
		if (m_MesheComps[i])
			m_MesheComps[i]->DestroyComponent();
	}
	m_MesheComps.Empty();
}

bool APoseableBlur::ShouldTickIfViewportsOnly() const
{
	return true;
}

bool APoseableBlur::CreateBlur(const TArray<MeshMatchData>& Meshes, float Life, UMaterialInterface* Material, bool TickPos)
{
	//InitialLifeSpan = Life;// +FadeOutTime;
	Lifetime = Life + FadeOutTime;
	for (MeshMatchData data : Meshes)
	{
		if (ParentPoseMesh == nullptr)
			ParentPoseMesh = Cast<USkeletalMeshComponent>(data.MeshComp);
		if (Cast<USkeletalMesh>(data.MatchMesh))
		{
			if (PoseableBlurMesh->SkeletalMesh!=nullptr)
			{

				UPoseableMeshComponent* MeshComp = NewObject<UPoseableMeshComponent>(DefaultSceneRoot/*, TEXT("PoseableMesh")*/);
				CreateSkeletalPoseableMesh(MeshComp, data, Material);
			}
			else
			{
				CreateSkeletalPoseableMesh(PoseableBlurMesh, data, Material);
			}


		}
		else if (Cast<UStaticMesh>(data.MatchMesh))
		{
			SkeletalAttachMesh = true;
			UStaticMeshComponent* MeshComp = NewObject<UStaticMeshComponent>(DefaultSceneRoot/*, TEXT("StaticMesh")*/);
			MeshComp->SetVisibility(false);
			if (IsValid(PoseableBlurMesh))
			{
				MeshComp->AttachToComponent(PoseableBlurMesh, FAttachmentTransformRules::KeepRelativeTransform, data.MeshComp->GetAttachSocketName());
			}
			else
			{
				MeshComp->AttachToComponent(DefaultSceneRoot, FAttachmentTransformRules::KeepRelativeTransform);
				MeshComp->SetWorldTransform(data.MeshComp->GetComponentToWorld());
				MeshComp->SetWorldRotation(data.MeshComp->GetComponentRotation());
			}
			MeshComp->RegisterComponent();
			MeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			MeshComp->SetStaticMesh(Cast<UStaticMesh>(data.MatchMesh));
			MeshComp->bRenderCustomDepth = true;
			m_MesheComps.Add(MeshComp);
			TArray<class UMaterialInterface*> materials = MeshComp->GetMaterials();
			for (int i = 0; i < materials.Num(); i++)
			{
				MeshComp->CreateAndSetMaterialInstanceDynamicFromMaterial(i, Material);
			}
		}
	}
	m_bTickPos = TickPos;
	if (TickPos)
	{
		GetWorld()->GetTimerManager().SetTimer(CopyTimeHandle, this, &APoseableBlur::CopyTimerEvent, 0.05f, true);
	}
	else
	{
		GetWorld()->GetTimerManager().SetTimer(CopyTimeHandle, this, &APoseableBlur::CopyTimerEvent, 0.05f, false);
	}
	GetWorld()->GetTimerManager().SetTimer(DelaySkeletalTimeHandle, this, &APoseableBlur::SetMeshVisable, 0.2f, false);
	return true;
	return true;
}


void APoseableBlur::CopyTimerEvent()
{
	if (IsValid(ParentPoseMesh))
	{
		for (UMeshComponent* mesh : m_MesheComps)
		{
			UPoseableMeshComponent* posemesh = Cast<UPoseableMeshComponent>(mesh);
			if (IsValid(posemesh))
			{
				posemesh->CopyPoseFromSkeletalComponent(ParentPoseMesh);
			}
		}
	}
}

void APoseableBlur::SetMeshVisable()
{
	for (UMeshComponent* mesh : m_MesheComps)
	{
		mesh->SetVisibility(true);
	}
}

void APoseableBlur::CreateSkeletalPoseableMesh(UPoseableMeshComponent* mesh, MeshMatchData data, UMaterialInterface* Material)
{
	if (SkeletalAttachMesh)
	{
		if (IsValid(PoseableBlurMesh))
		{
			mesh->AttachToComponent(PoseableBlurMesh, FAttachmentTransformRules::KeepRelativeTransform, data.MeshComp->GetAttachSocketName());
			mesh->SetRelativeLocation(FVector::ZeroVector);
		}
	}
	else
	{
		mesh->AttachToComponent(DefaultSceneRoot, FAttachmentTransformRules::KeepRelativeTransform);
		mesh->SetWorldTransform(data.MeshComp->GetComponentToWorld());
	}
	mesh->SetVisibility(false);
	mesh->RegisterComponent();
	mesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	mesh->SetSkeletalMesh(Cast<USkeletalMesh>(data.MatchMesh));
	mesh->bRenderCustomDepth = true;
	m_MesheComps.Add(mesh);
	TArray<class UMaterialInterface*> materials = mesh->GetMaterials();
	if (IsValid(Material))
	{
		if (mesh != PoseableBlurMesh)
		{
			materials = mesh->GetMaterials();
			for (int i = 0; i < materials.Num(); i++)
			{
				mesh->SetMaterial(i, Material);
				//mesh->CreateAndSetMaterialInstanceDynamicFromMaterial(i, Material);
			}
		}
	}
	else
	{
		USkeletalMeshComponent* skelete = Cast<USkeletalMeshComponent>(data.MeshComp);
		if (IsValid(skelete))
		{
			materials = skelete->GetMaterials();
			for (int i = 0; i < materials.Num(); i++)
			{
				mesh->SetMaterial(i, Material);
				//mesh->CreateAndSetMaterialInstanceDynamicFromMaterial(i, materials[i]);
			}
		}
	}
}

