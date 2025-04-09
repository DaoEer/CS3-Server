// Fill out your copyright notice in the Description page of Project Settings.


#include "EquipBuildClientCharacter.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Components/CapsuleComponent.h"
#include "UnrealMathUtility.h"
#include "LandscapeProxy.h"
#include "Engine/StaticMeshActor.h"
#include "Component/CollisionComponent.h"
#include "Materials/Material.h"

void AEquipBuildClientCharacter::BeginPlay()
{
	Super::BeginPlay();
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = false;
	PrimaryActorTick.SetTickFunctionEnable(false);
	GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, -1.0f * GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight()));
	lastMouseScreenPos = FVector2D::ZeroVector;
	GetCollisionComponent()->DisableAllCollision();
}

void AEquipBuildClientCharacter::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	UpdateActorLocationAndRotation();
	UpdateModelMaterialColor();
}

void AEquipBuildClientCharacter::OnCreateApperanceOver()
{
	SetActorTickEnabled(true);
	InitModelMaterial();
}

void AEquipBuildClientCharacter::InitModelMaterial()
{

	UMaterialInstance* MaterialBlue = LoadObject<UMaterialInstance>(NULL, TEXT("/Game/Materials/M_TransBlue_Inst.M_TransBlue_Inst"), NULL, LOAD_None, NULL);
	if (IsValid(MaterialBlue))
		TransBlue_Inst = UMaterialInstanceDynamic::Create(MaterialBlue, this);
	UMaterialInstance* MaterialRed = LoadObject<UMaterialInstance>(NULL, TEXT("/Game/Materials/M_TransRed_Inst.M_TransRed_Inst"), NULL, LOAD_None, NULL);
	if (IsValid(MaterialRed))
		TransRed_Inst = UMaterialInstanceDynamic::Create(MaterialRed, this);

// 
// 	TArray<class UMaterialInterface*> MaterialsList;
// 	MaterialsList = GetMesh()->GetMaterials();
// 	for (int i = 0; i < MaterialsList.Num(); i++)
// 	{
// 		if (IsValid(MaterialsList[i]))
// 		{
// 			UMaterialInstanceDynamic* MaterialInstanceDynamic = GetMesh()->UPrimitiveComponent::CreateDynamicMaterialInstance(i, MaterialsList[i]);
// 			MaterialInstanceDynamic->SetScalarParameterValue(TEXT("UseEmissiveColor"), 1);
// 		}
// 	}
// 
// 	TArray<class UMaterialInterface*> ST_MaterialsList;
// 	ST_MaterialsList = STMesh_DefaultStatic->GetMaterials();
// 	for (int i = 0; i < ST_MaterialsList.Num(); i++)
// 	{
// 		if (IsValid(ST_MaterialsList[i]))
// 		{
// 			UMaterialInstanceDynamic* StaticMeshMaterialInstanceDynamic = STMesh_DefaultStatic->UPrimitiveComponent::CreateDynamicMaterialInstance(i, ST_MaterialsList[i]);
// 			StaticMeshMaterialInstanceDynamic->SetScalarParameterValue(TEXT("UseEmissiveColor"), 1);
// 		}
// 	}
}

void AEquipBuildClientCharacter::UpdateModelMaterialColor()
{
	if (bCanBuild)
	{
		ChangeModelMaterial(2);
	} 
	else
	{
		ChangeModelMaterial(1);
	}
}

void AEquipBuildClientCharacter::UpdateActorLocationAndRotation()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController)) return;
	FVector2D ScreenPosition;
	if (!PlayerController->GetMousePosition(ScreenPosition.X, ScreenPosition.Y))
	{
		return;
	}
	if (FVector2D::Distance(ScreenPosition, lastMouseScreenPos) >= 1.0f)
	{
		lastMouseScreenPos = ScreenPosition;
		bCanBuild = false;//重置
		FVector MousePos;
		FHitResult TraceHitResult;
		FCollisionQueryParams TraceParams = FCollisionQueryParams(FName(TEXT("ComputeFloorDistSweep")), true, this);
		TraceParams.bTraceComplex = true;
		TraceParams.AddIgnoredActor(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		PlayerController->GetHitResultAtScreenPosition(ScreenPosition, PlayerController->CurrentClickTraceChannel, TraceParams, TraceHitResult);
		if (TraceHitResult.bBlockingHit)
		{
			MousePos = TraceHitResult.ImpactPoint + FVector(0.0f, 0.0f, GetCapsuleComponent()->GetScaledCapsuleHalfHeight());
			AActor* HitActor = TraceHitResult.GetActor();
			if (IsValid(HitActor) && (HitActor->GetClass()->IsChildOf(ALandscapeProxy::StaticClass()) || HitActor->GetClass()->IsChildOf(AStaticMeshActor::StaticClass())))
			{
				bCanBuild = true;
				//检测材质
				if (IsValid(TraceHitResult.GetComponent()))
				{
					if (IsValid(TraceHitResult.GetComponent()->GetMaterial(0)))
					{
						UMaterial* Material = TraceHitResult.GetComponent()->GetMaterial(0)->GetBaseMaterial();
						if (IsValid(Material))
						{
							FString PathName = Material->GetPathName();
							FString FullName = Material->GetFullName();
							FString Name = Material->GetName();
							if (Material->BlendMode == BLEND_Translucent)//水面不能建造
							{
								bCanBuild = false;
							}
						}
					}
				}
				//检测地面是不是平的
				if (bCanBuild)
				{
					FHitResult HitOut(ForceInit);
					FCollisionQueryParams Params = FCollisionQueryParams(FName(TEXT("ComputeFloorDistSweep")), true, this);
					Params.bTraceComplex = false;
					Params.bReturnPhysicalMaterial = false;
					Params.bIgnoreTouches = true;
					FVector Dest;
					FVector Box;
					//Box = GetBoxExtent();
					float Radius = GetCapsuleComponent()->GetScaledCapsuleRadius();
					float HalfHeight = GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
					Box = FVector(Radius, Radius, HalfHeight);
					if (this->GetWorld()->SweepSingleByChannel(HitOut, MousePos + FVector(0.0f, 0.0f, 100.0f), TraceHitResult.ImpactPoint - FVector(0.0f, 0.0f, 100.0f), FQuat::Identity, ECC_Visibility, FCollisionShape::MakeBox(Box), Params))
					{
						//UKismetSystemLibrary::DrawDebugLine(GetWorld(), MousePos + FVector(0.0f, 0.0f, 100.0f), TraceHitResult.ImpactPoint - FVector(0.0f, 0.0f, 100.0f), FColor::Red, 3.0f, 5.0f);
						Dest = HitOut.Location;
						//UKismetSystemLibrary::DrawDebugSphere(GetWorld(), TraceHitResult.ImpactPoint, 18.f, 12, FLinearColor::Green, 3.0);
						//UKismetSystemLibrary::DrawDebugSphere(GetWorld(), MousePos, 15.f, 12, FLinearColor::Red, 3.0);
						//UKismetSystemLibrary::DrawDebugSphere(GetWorld(), HitOut.ImpactPoint, 12.f, 12, FLinearColor::Yellow, 3.0);
						//UKismetSystemLibrary::DrawDebugSphere(GetWorld(), HitOut.Location, 10.f, 12, FLinearColor::Blue, 3.0);
					}
					bCanBuild = (FMath::IsNearlyEqual(MousePos.Z, Dest.Z, 10.0f));
				}
			}
		}
		FVector Direction = FVector::ZeroVector;
		Direction.Z = PlayerController->GetControlRotation().Euler().Z;
		SetActorLocationAndRotation(MousePos, FQuat::MakeFromEuler(Direction));
	}
}

void AEquipBuildClientCharacter::ChangeModelMaterial(int32 ColorIndex)
{
	if (ColorIndex == curState)
	{
		return;
	}
	else
	{
		curState = ColorIndex;
	}
	for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		if (IsValid(Component.Value()))
		{
			USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
			
			if (IsValid(MeshComponent) && IsValid(MeshComponent->SkeletalMesh))
			{
				for (int32 i =0;i<MeshComponent->GetMaterials().Num();i++)
				{
					if (ColorIndex == 2)
					{
						MeshComponent->SetMaterial(i, TransBlue_Inst);
					}
					if (ColorIndex == 1)
					{
						MeshComponent->SetMaterial(i, TransRed_Inst);
					}
				}
				return;
			}

			UStaticMeshComponent* StaticMeshComponent = Cast<UStaticMeshComponent>(Component.Value());
			if (IsValid(StaticMeshComponent) && IsValid(StaticMeshComponent->GetStaticMesh()))
			{
				for (int32 i = 0; i < StaticMeshComponent->GetMaterials().Num(); i++)
				{
					if (ColorIndex == 2)
					{
						StaticMeshComponent->SetMaterial(i, TransBlue_Inst);
					}
					if (ColorIndex == 1)
					{
						StaticMeshComponent->SetMaterial(i, TransRed_Inst);
					}
				}
			}
		}
	}
}

FVector AEquipBuildClientCharacter::GetBoxExtent()
{
	FVector BoxExtent = FVector::ZeroVector;
	if (IsValid(STMesh_DefaultStatic) && IsValid(STMesh_DefaultStatic->GetStaticMesh()))
	{
		BoxExtent = STMesh_DefaultStatic->GetStaticMesh()->GetBounds().BoxExtent;
	}
	else if (IsValid(GetMesh()) && IsValid(GetMesh()->SkeletalMesh))
	{
		BoxExtent = GetMesh()->SkeletalMesh->GetBounds().BoxExtent;
	}
	return BoxExtent;
}

bool AEquipBuildClientCharacter::CanBuild()
{
	return bCanBuild;
}
