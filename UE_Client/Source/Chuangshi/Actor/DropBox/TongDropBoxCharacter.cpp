// Fill out your copyright notice in the Description page of Project Settings.

#include "TongDropBoxCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/Role/RoleDropBoxInterface.h"
#include "Manager/ParticleManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/VisibleManager.h"
#include "Manager/ShapeManager.h"
#include "Util/CS3Debug.h"
#include "Component/AppearanceComponent.h"
#include "Components/CapsuleComponent.h"
#include "Interface/DropBox/TongDropBoxInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"
#include "CS3Base/UIManager.h"

ATongDropBoxCharacter::ATongDropBoxCharacter()
{
	CharacterClassName = TEXT("TongDropBoxCharacter");
	SetCanGossip(false);
}

void ATongDropBoxCharacter::OnUnBindActorCallBack()
{
	Super::OnUnBindActorCallBack();
	OnClosedWnd();
}

UBaseShape* ATongDropBoxCharacter::CreateSphereShape()
{
	float radius = m_SphereRadius;
	FVector shapeVector = FVector(radius, radius, radius);
	return UUECS3GameInstance::Instance->ShapeManager->CreateShape(this, this, SHAPE_TYPE::SHPERE, shapeVector, &ATongDropBoxCharacter::OnPlayerBeginOverlap, &ATongDropBoxCharacter::OnPlayerEndOverlap);
}

bool ATongDropBoxCharacter::CanGossipWith_Implementation()
{
	return CanGossip;
}

void ATongDropBoxCharacter::SetInteractiveRadius(float InRadius)
{
	pDropBoxShape->UpdateBounds(FVector(InRadius, InRadius, InRadius));
}

void ATongDropBoxCharacter::SetCanGossip(float InCanGossip)
{
	CanGossip = (bool)InCanGossip;
}

void ATongDropBoxCharacter::GossipWith()
{
	///玩家转向DropBox
	FVector StartLoction = GetActorLocation();
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:ASpellBoxCharacter::GossipWith : PlayerActor!"));
		return;
	}

	FVector TargetLoction = PlayerActor->GetActorLocation();
	FRotator PlayerRotation = UGolbalBPFunctionLibrary::GetLookAtRotator(TargetLoction, StartLoction);
	PlayerActor->SetActorRotation(PlayerRotation);
	PlayerActor->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_TALKTODROPBOX;

	if (IsValid(UUECS3GameInstance::Instance->GUIManager) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UTongDropBoxInterface* interface = Cast<UTongDropBoxInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("TongDropBoxInterface"), EntityId));
		if (interface != nullptr)
		{
			if (interface->freeAllocationItems.Num() > 0)
			{
				//打开自由拾取界面
				UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("DropBoxPickUp"));
				UUECS3GameInstance::Instance->GEventManager->OnTongUpdatePickUpWnd.Broadcast(EntityId);
			}
		}	
	}
}

void ATongDropBoxCharacter::OnClosedWnd()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnClosedTongPickWnd.Broadcast(EntityId);
		UUECS3GameInstance::Instance->GEventManager->OnClosedTongDicePickWnd.Broadcast(EntityId);
		UUECS3GameInstance::Instance->GEventManager->OnCloseAuctionPickWndEvent.Broadcast(EntityId);
		UUECS3GameInstance::Instance->GEventManager->OnClosedPickUpWnd.Broadcast(EntityId);
	}
}

void ATongDropBoxCharacter::OnPlayerBeginOverlap_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(this);

	UTongDropBoxInterface* interface = Cast<UTongDropBoxInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("TongDropBoxInterface"), EntityId));
	if (interface != nullptr)
	{
		if (interface->freeAllocationItems.Num() > 0 || interface->notAllocationItems.Num() > 0)
		{
			interface->openTongLeaderPickUpWnd();
			return;
		}

		interface->ReqTongDropBoxData();
	}
}

void ATongDropBoxCharacter::OnPlayerEndOverlap_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(this);
	OnClosedWnd();
}

bool ATongDropBoxCharacter::isVisible(const UINT64 &PlayerDBID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("----- check TongDropBox is visible "));
	KBEngine::Entity* DropBox = GetSelfEntity();

	if (DropBox != nullptr)
	{
		UTongDropBoxInterface* interface = Cast<UTongDropBoxInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("TongDropBoxInterface"), DropBox->ID()));
		if (interface != nullptr)
		{
			if (interface->isVisible())
				return true;
		}
		return false;
	}

	return false;
}

void ATongDropBoxCharacter::FlyTargerOverEvent()
{
	UTongDropBoxInterface* interface = Cast<UTongDropBoxInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("TongDropBoxInterface"), EntityId));
	if (IsValid(interface))
	{
		interface->FlyTargerOverEvent();
	}
	URoleDropBoxInterface* roleDropboxInterface = Cast<URoleDropBoxInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleDropBoxInterface")));
	if (IsValid(roleDropboxInterface))
	{
		roleDropboxInterface->FlyTargerOverEvent();
	}
}
