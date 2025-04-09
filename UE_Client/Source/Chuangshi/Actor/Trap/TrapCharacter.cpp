// Fill out your copyright notice in the Description page of Project Settings.

#include "TrapCharacter.h"
#include "Interface/Trap/TrapInterface.h"
#include "Component/AvatarFilterActorComponent.h"
#include "Component/DumbFilterActorComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Manager/GameStatus.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/ShapeManager.h"
#include "CS3Base/GameObject.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include "Component/FightComponent.h"
#include "Component/AppearanceComponent.h"

void ATrapCharacter::InitFilterActorComponent()
{
	KBEngine::Entity* Entity = GetSelfEntity();
	if (Entity == nullptr) { 
		CS3_Warning(TEXT("-->Null Pointer error:ATrapCharacter::InitFilterActorComponent : Entity!"));
		return; 
	}
	GameObject *Trap_cast = (GameObject *)Entity;
	bool IsStartActiveFilter;
	if (Trap_cast != nullptr && Trap_cast->ClassName() == "Trap")
	{
		SetFilterComponent(NewObject<UDumbFilterActorComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr));
		IsStartActiveFilter = false;
	}
	else
	{
		SetFilterComponent(NewObject<UAvatarFilterActorComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr));
		IsStartActiveFilter = true;
	}
	GetFilterComponent()->RegisterComponent();
	GetFilterComponent()->InitFilter(IsStartActiveFilter);
}

ATrapCharacter::ATrapCharacter()
{
	CharacterClassName = TEXT("TrapCharacter");
	PrimaryActorTick.bCanEverTick = true;
	InitBaseComponent();
}

void ATrapCharacter::InitBaseComponent()
{
	FightComponent = CreateDefaultSubobject<UFightComponent>(TEXT("FightComponent"));
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}



int32 ATrapCharacter::GetTriggerShape()
{
	return UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityId, TEXT("triggerShape"));
}

FVector ATrapCharacter::GetTriggerLocation()
{
	FString triggerPosition = UGolbalBPFunctionLibrary::GetEntityPropertyValue(EntityId, TEXT("triggerPosition"));

	TArray<FString> LocationString = UGolbalBPFunctionLibrary::SplitString(triggerPosition, false, TEXT(" "));

	FVector LocationValue = FVector::ZeroVector;

	if(LocationString.Num() == 3)
	{
		LocationValue.X = FSTRING_TO_FLOAT(LocationString[0]);
		LocationValue.Y = FSTRING_TO_FLOAT(LocationString[1]);
		LocationValue.Z = FSTRING_TO_FLOAT(LocationString[2]);
	}

	return LocationValue;
}

void ATrapCharacter::OnEnterTrap(int32 eID)
{
	if (GetSelfEntity() == nullptr)
	{
		CS3_Warning(TEXT("ATrapCharacter::OnEnterTrap no this entity %d"),EntityId);
		return;
	}
	UTrapInterface * Interface = Cast<UTrapInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (IsValid(Interface))
	{		
		Interface->OnEnterTrap(eID);
	}
}

void ATrapCharacter::OnLeaveTrap(int32 eID)
{
	if (GetSelfEntity() == nullptr)
	{
		CS3_Warning(TEXT("ATrapCharacter::OnLeaveTrap no this entity %d"), EntityId);
		return;
	}
	UTrapInterface * Interface = Cast<UTrapInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (IsValid(Interface))
	{
		Interface->OnLeaveTrap(eID);
	}
}


void ATrapCharacter::OnInitialized()
{
	Super::OnInitialized();

}

void ATrapCharacter::SetInitAction()
{
	KBEngine::Entity* SelfEntity = GetSelfEntity();
	InitActionId = !SelfEntity ? "None" : FSTRING_TO_FNAME((FString)SelfEntity->GetDefinedProperty(TEXT("initActionId")));
}

FString ATrapCharacter::GetEntityUName()
{
	return UGolbalBPFunctionLibrary::GetFStringPropertyValue(EntityId, TEXT("uname"));
}

float ATrapCharacter::GetMoveSpeed()
{
	if (bIsClient)
	{
		return ClientMoveSpeed;
	}
	return UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, TEXT("moveSpeed"));
}

bool ATrapCharacter::IsEntityMoveType(MOVETYPE MoveType)
{
	int32 MovingType = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityId, TEXT("movingType"));
	return MovingType == int32(MoveType);
}


float ATrapCharacter::GetFilterSpeed()
{
	KBEngine::Entity* Entity = GetSelfEntity();
	GameObject *Trap_cast = (GameObject *)Entity;
	if (Trap_cast && Trap_cast->GetActorName() == "Trap") { return 0.0f; }
	if (UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() <= EGameStatus::Teleport)
	{
		return 0.0f;
	}
	if (Entity)
	{
		if (IsMoveType(MOVETYPE::MOVETYPE_CHASE) && !((GameObject*)Entity)->IsSyncServerPos())
		{
			return GetCharacterMovement()->MaxWalkSpeed;
		}
		
		return FilterSpeed;
		
	}
	return 0.0f;
}

void ATrapCharacter::CLIENT_DelayToAddTrap_Implementation(float value)
{
	FTimerHandle  m_timerHandle;
	if (FMath::IsNearlyZero(value))
	{
		AddTrapShape();
		return;
	}
	
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(m_timerHandle, this, 
			&ATrapCharacter::AddTrapShape, value, false);
	}
}


void ATrapCharacter::AddTrapShape()
{
	int32 triggerShape = GetTriggerShape();
	switch (triggerShape)
	{
		case 0:
			pTrapShape = CreateBoxShape();
			break;
		case 1:
			pTrapShape = CreateSphereShape();
			break;
		case 2:
			pTrapShape = CreateCylinderShape();
			break;
	default:
		return;
	}
}

UBaseShape* ATrapCharacter::CreateBoxShape()
{
	float depth = UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, TEXT("triggerDepth"));
	float width = UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, TEXT("triggerWidth"));
	float height = UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, TEXT("triggerHeight"));
	FVector	shapeVector = FVector(depth, width, height);
	return UUECS3GameInstance::Instance->ShapeManager->CreateShape(this, this, SHAPE_TYPE::BOX, shapeVector, &ATrapCharacter::OnBeginOverlap, &ATrapCharacter::OnEndOverlap);
}

UBaseShape* ATrapCharacter::CreateSphereShape()
{
	float radius = UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, TEXT("triggerRadius"));
	FVector shapeVector = FVector(radius, radius, radius);
	return  UUECS3GameInstance::Instance->ShapeManager->CreateShape(this, this, SHAPE_TYPE::SHPERE, shapeVector, &ATrapCharacter::OnBeginOverlap, &ATrapCharacter::OnEndOverlap);
}

UBaseShape* ATrapCharacter::CreateCylinderShape()
{
	float radius = UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, TEXT("triggerRadius"));
	float height = UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, TEXT("triggerHeight"));
	FVector shapeVector = FVector(radius, radius, height);
	return UUECS3GameInstance::Instance->ShapeManager->CreateShape(this, this, SHAPE_TYPE::CYLINDER, shapeVector, &ATrapCharacter::OnBeginOverlap, &ATrapCharacter::OnEndOverlap);
}

void ATrapCharacter::OnBeginOverlap()
{
	int32 PlayerID = UGolbalBPFunctionLibrary::GetPlayerID();
	OnEnterTrap(PlayerID);
}

void ATrapCharacter::OnEndOverlap()
{
	int32 PlayerID = UGolbalBPFunctionLibrary::GetPlayerID();
	OnLeaveTrap(PlayerID);
}