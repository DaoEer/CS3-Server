// Fill out your copyright notice in the Description page of Project Settings.


#include "SpellBoxCharacter.h"
#include "Entity/SpellBox/SpellBoxHit.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/ShapeManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/SpellBox/SpellBoxInterface.h"
#include "Interface/SpellBox/SpellBoxAdvancedInterface.h"
#include "Component/AppearanceComponent.h"
#include "Component/AvatarFilterActorComponent.h"
#include "GameDevelop/CS3PlayerController.h"

ASpellBoxCharacter::ASpellBoxCharacter()
{
	PrimaryActorTick.bCanEverTick = true;
	CharacterClassName = TEXT("SpellBoxCharacter");
	InitBaseComponent();
}

void ASpellBoxCharacter::BeginPlay()
{
	Super::BeginPlay();
}

void ASpellBoxCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		PlayerActor->RemoveFromInteractivityList(this);
	}
	
	Super::EndPlay(EndPlayReason);
}

void ASpellBoxCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();
	pSpellBoxShape = CreateSphereShape();
}

void ASpellBoxCharacter::InitFilterActorComponent()
{
	SetFilterComponent(NewObject<UAvatarFilterActorComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr));
	GetFilterComponent()->RegisterComponent();
	GetFilterComponent()->InitFilter(true);
}

UBaseShape* ASpellBoxCharacter::CreateSphereShape()
{
	float radius = m_SphereRadius;
	FVector shapeVector = FVector(radius, radius, radius);
	return UUECS3GameInstance::Instance->ShapeManager->CreateShape(this, this, SHAPE_TYPE::SHPERE, shapeVector, &ASpellBoxCharacter::OnPlayerBeginOverlap, &ASpellBoxCharacter::OnPlayerEndOverlap);
}

void ASpellBoxCharacter::SetInitAction()
{
	KBEngine::Entity* SelfEntity = GetSelfEntity();
	InitActionId = !SelfEntity ? "None" : FSTRING_TO_FNAME((FString)SelfEntity->GetDefinedProperty(TEXT("initActionId")));
}

void ASpellBoxCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

void ASpellBoxCharacter::GossipWith()
{
	///玩家转向SpellBox
	FVector StartLoction = GetActorLocation();
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:ASpellBoxCharacter::GossipWith : PlayerActor!"));
		return;
	}
	if (GetSelfEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ASpellBoxCharacter::GossipWith : SpellBox Entity!"));
		return;
	}
	if (!(GetSelfEntity()->ClassName() == "SpellBoxHit") && !(GetSelfEntity()->ClassName() == "SpellBoxDoor"))
	{
		FVector TargetLoction = PlayerActor->GetActorLocation();
		FRotator PlayerRotation = UGolbalBPFunctionLibrary::GetLookAtRotator(TargetLoction, StartLoction);
		PlayerActor->SetActorRotation(PlayerRotation);
	}
	PlayerActor->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_TALKTOSPELLBOX;
	
	USpellBoxInterface * SpellBoxInterface = Cast<USpellBoxInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (SpellBoxInterface)
	{
		SpellBoxInterface->RPC_CELL_gossipWith();
	}
	//KBEngine::FVariantArray Args;
	//if (KBEngine::Entity* SpellBox = GetSelfEntity())
	//{
	//	SpellBox->CellCall(TEXT("CELL_gossipWith"), Args);
	//}
}

void ASpellBoxCharacter::OnSetBoxStatus_Implementation(int32 BoxStatus)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:ASpellBoxCharacter::GossipWith : PlayerActor!"));
		return;
	}
	///<交互完成后状态的刷新，设置玩家的交互状态
	if (IsValid(PlayerActor->CurInteractiveTarget) && IsValid(this) && PlayerActor->CurInteractiveTarget == this)
	{
		PlayerActor->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_SUCCESS;
	}	
}

void ASpellBoxCharacter::RPC_reqStartInteractive()
{
	USpellBoxAdvancedInterface * SpellBoxAdvancedInterface = Cast<USpellBoxAdvancedInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (SpellBoxAdvancedInterface)
	{
		SpellBoxAdvancedInterface->CELL_reqStartInteractive();
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:ASpellBoxCharacter::RPC_reqStartInteractive : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;

	//entity->CellCall(TEXT("CELL_reqStartInteractive"), args);
}

void ASpellBoxCharacter::RPC_reqInterruptInteractive()
{
	USpellBoxAdvancedInterface * SpellBoxAdvancedInterface = Cast<USpellBoxAdvancedInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (SpellBoxAdvancedInterface)
	{
		SpellBoxAdvancedInterface->CELL_reqInterruptInteractive();
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:ASpellBoxCharacter::RPC_reqInterruptInteractive : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;
	
	//entity->CellCall(TEXT("CELL_reqInterruptInteractive"), args);
}

void ASpellBoxCharacter::SpellBoxInteractiveInterrupted()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	///<交互完成后状态的刷新，设置玩家的交互状态
	if (IsValid(PlayerActor->CurInteractiveTarget) && IsValid(this) && PlayerActor->CurInteractiveTarget == this)
	{
		PlayerActor->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_NODE;
	}
}

void ASpellBoxCharacter::OnPlayerBeginOverlap_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(this);
}

void ASpellBoxCharacter::OnPlayerEndOverlap_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(this);
}

FString ASpellBoxCharacter::GetEntityUName()
{
	return UGolbalBPFunctionLibrary::GetFStringPropertyValue(EntityId, TEXT("uname"));
}