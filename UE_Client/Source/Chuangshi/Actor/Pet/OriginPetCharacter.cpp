// Fill out your copyright notice in the Description page of Project Settings.


#include "OriginPetCharacter.h"
#include "GameData\PetEpitome.h"
#include "GameData\PetData.h"
#include "NavigationSystem\Public\NavigationSystem.h"
#include "CoreMinimal.h"
#include "AIController.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Component/AppearanceComponent.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"
#include "TransActorCapture.h"
#include "Manager/CfgManager.h"

void AOriginPetCharacter::BeginPlay()
{
	AAIController* AIController = GetWorld()->SpawnActor<AAIController>();
	AIController->Possess(this);
	GetCharacterMovement()->SetAutoActivate(true);
	IsMoveDisAppear = false;
	Super::BeginPlay();
}

void AOriginPetCharacter::InitOriginPet(const ORIGIN_PET_CLIENT_SIMPLE_DATA& Data)
{
	index = FMath::CeilToInt(Data.index / 2);
	UID = FString::Printf(TEXT("%llu"), Data.uid);
	ScriptID = Data.scriptID;
	SetMaxWalkSpeed(600.0f);
	const UConfigTable* ConfigTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET);
	if (ConfigTable)
	{
		const FPET_DATA* petData = ConfigTable->GetRow<FPET_DATA>(Data.scriptID);
		if (petData != nullptr)
		{
			if (Data.bEvolution)
			{
				ModelNumber = petData->ModelNumber;
				ModelScale = petData->ModelScale;
			}
			else
			{
				ModelNumber = petData->OriginModelNumber;
				ModelScale = petData->OriginModelScale;
			}
		}
		CreateAppearance();
	}
	
}

void AOriginPetCharacter::CreateAppearance()
{
	GetAppearanceComponent()->CreateAppearance(ModelNumber);
}

void AOriginPetCharacter::OnCreateModelOver()
{
	SetActorScale3D(FVector(ModelScale, ModelScale, ModelScale));
	UpdateCapsuleComponent();
	if (UGolbalBPFunctionLibrary::CustomTimerManager())
	{
		if (!UGolbalBPFunctionLibrary::CustomTimerManager()->IsTimerActive(MoveTimer))
		{
			TWeakObjectPtr<AOriginPetCharacter> DelayThisPtr(this);
			UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(this, MoveTimer, FTimerDelegate::CreateLambda([DelayThisPtr]()
			{
				if (DelayThisPtr.IsValid())
				{
					DelayThisPtr.Get()->RandomMove();
				}
			}), 5.0f, true);
		}
	}
	
}

float AOriginPetCharacter::GetMoveSpeed()
{
	return 600.f;
}

bool AOriginPetCharacter::IsActiveMoveing()
{
	if (IsMoveDisAppear)
	{
		return true;
	}
	return Super::IsActiveMoveing();
}

void AOriginPetCharacter::MoveLeaveBeforeDestroy()
{
	UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(MoveTimer);
	if (ORIGIN_PET_RUN_POS.Num() <= index)
	{
		Destroy();
		return;
	}
	IsMoveDisAppear = true;
	TargetPos = ORIGIN_PET_RUN_POS[index];
	changeDelta = 2.0f;
	AAIController* control = Cast<AAIController>(GetController());
	if (IsValid(control))
	{
		control->StopMovement();				// 因为有随机移动，不去掉就一直往随机点移动
	}
	TWeakObjectPtr<AOriginPetCharacter> DelayThisPtr(this);
	UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(this, MoveTimer, FTimerDelegate::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			DelayThisPtr.Get()->MoveChangeImp();
		}
	}), 0.02f, true);

}

void AOriginPetCharacter::MoveChangeImp()
{
	if (FVector::Dist2D(GetActorLocation(),TargetPos) <= 10.f)
	{
		TargetPos = ORIGIN_PET_RUN_LAST_POS;
	}
	
	FRotator Rotation = FRotationMatrix::MakeFromX(TargetPos - GetActorLocation()).Rotator();
	FVector  Location = GetActorLocation() + Rotation.Quaternion().GetAxisX() * GetMoveSpeed() * 0.02f;
	Location.Z = GetActorLocation().Z;
	SetActorLocationAndRotation(Location, Rotation);

	changeDelta -= 0.02;
	if (changeDelta < 0.0f)
	{
		Destroy();
		return;
	}
	ATransActorCapture::SetTransActor(this, changeDelta);
}

void AOriginPetCharacter::RandomMove()
{
	FNavLocation DstPos;
	UNavigationSystemV1* NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());
	if (NavSys->GetRandomReachablePointInRadius(GetActorLocation(), 5000, DstPos))
	{
		UAIBlueprintHelperLibrary::SimpleMoveToLocation(GetController(), DstPos.Location);
	}
	
}
