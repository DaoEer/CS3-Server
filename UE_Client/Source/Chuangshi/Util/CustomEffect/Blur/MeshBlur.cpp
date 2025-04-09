// Fill out your copyright notice in the Description page of Project Settings.
#include "MeshBlur.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Util/CS3Debug.h"

// Sets default values
AMeshBlur::AMeshBlur()
{
	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	StaticMeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("StaticMesh"));
	StaticMeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	MeshComp = StaticMeshComp;
	FadeOutTime = 0.5f;
	FadeOutTimer = 0.f;
}

// Called when the game starts or when spawned
void AMeshBlur::BeginPlay()
{
	Super::BeginPlay();
}

// Called every frame
void AMeshBlur::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	Lifetimer += DeltaTime;

	if ( Lifetimer >= Lifetime - FadeOutTime )
	{
		FadeOutTimer += DeltaTime; 
		TArray<class UMaterialInterface*> materials = MeshComp->GetMaterials();
		for (UMaterialInterface* mat : materials)
		{
			UMaterialInstanceDynamic* Mat = Cast<UMaterialInstanceDynamic>(mat);
			if (Mat)
				Mat->SetScalarParameterValue(TEXT("OpacityIntensity"), (1 - FadeOutTimer / FadeOutTime) );
		}
	}
	if (m_TickPos)
	{
		if (IsValid(StaticMeshComp) && IsValid(ParentStaticMesh))
		{
			StaticMeshComp->SetWorldLocation(ParentStaticMesh->GetComponentToWorld().GetLocation()+ DeviationTransform);
			StaticMeshComp->SetWorldRotation(ParentStaticMesh->GetComponentToWorld().GetRotation());
		}
	}
}

void AMeshBlur::Destroyed(){
	if (StaticMeshComp)
		StaticMeshComp->DestroyComponent();
	MeshComp = nullptr;
}

bool AMeshBlur::ShouldTickIfViewportsOnly() const
{
	return true;
}

bool AMeshBlur::CreateBlur(UMeshComponent* Mesh, UObject* Obj, float Life, UMaterialInterface* Material, bool TickPos)
{
	if (!IsValid(Mesh))
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMeshBlur::CreateBlur: StaticMesh!"));
		return false;
	}
	ParentStaticMesh = Cast<UStaticMeshComponent>(Mesh);
	if (!IsValid(ParentStaticMesh))
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMeshBlur::CreateBlur: ParentStaticMesh!"));
		return false;
	}
	RootComponent = StaticMeshComp;
	StaticMeshComp->SetStaticMesh(Cast<UStaticMesh>(Obj));
	StaticMeshComp->SetWorldTransform(ParentStaticMesh->GetComponentToWorld());
	StaticMeshComp->SetWorldRotation(ParentStaticMesh->GetComponentRotation());
	StaticMeshComp->bRenderCustomDepth = true;
	TArray<class UMaterialInterface*> materials = MeshComp->GetMaterials();
	for (int i = 0; i < materials.Num(); i++)
	{
		StaticMeshComp->CreateAndSetMaterialInstanceDynamicFromMaterial(i, Material);
		//MeshComp->SetMaterial(i, Material);
	}
	Lifetime = Life + FadeOutTime;
	m_TickPos = TickPos;
	MeshDeviationTransform += ParentStaticMesh->GetComponentTransform().GetLocation();
	return true;
}

UStaticMeshComponent* AMeshBlur::GetStaticMesh()
{
	return StaticMeshComp;
}

