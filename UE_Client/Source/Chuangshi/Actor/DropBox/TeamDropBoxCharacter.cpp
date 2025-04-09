// Fill out your copyright notice in the Description page of Project Settings.

#include "TeamDropBoxCharacter.h"
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
#include "Interface/DropBox/TeamDropBoxInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"
#include "CS3Base/UIManager.h"

ATeamDropBoxCharacter::ATeamDropBoxCharacter()
{
	CharacterClassName = TEXT("TeamDropBoxCharacter");
}

void ATeamDropBoxCharacter::OnUnBindActorCallBack()
{
	Super::OnUnBindActorCallBack();
	OnClosedWnd();
}

bool ATeamDropBoxCharacter::CanGossipWith_Implementation()
{
	return true;
}

void ATeamDropBoxCharacter::GossipWith()
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
	ReqTeamDropBoxData();
}

void ATeamDropBoxCharacter::ReqTeamDropBoxData()
{
	UTeamDropBoxInterface* interface = Cast<UTeamDropBoxInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("TeamDropBoxInterface"), EntityId));
	if (interface != nullptr)
	{
		if (interface->freeAllocationItems.Num()>0 || interface->notAllocationItems.Num()>0)
		{
			if(interface->freeAllocationItems.Num() > 0)
				interface->OpenFreePickUpWnd();

			if (interface->notAllocationItems.Num() > 0)
			{
				UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TeamPick"));
				UUECS3GameInstance::Instance->GEventManager->OnUpdateTeamPickWnd.Broadcast(EntityId);
			}

			return;
		}
		interface->ReqTeamDropBoxData();
	}
}

void ATeamDropBoxCharacter::OnClosedWnd()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnClosedPickUpWnd.Broadcast(EntityId);
		UUECS3GameInstance::Instance->GEventManager->OnClosedTeamPickWnd.Broadcast(EntityId);
	}
}

TArray<UItemBase*> ATeamDropBoxCharacter::GetBoxItemList()
{
	TArray<UItemBase*> outItemBaseList;
	UTeamDropBoxInterface* interface = Cast<UTeamDropBoxInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("TeamDropBoxInterface"), EntityId));
	if (interface != nullptr && interface->freeAllocationItems.Num() > 0)
	{
		for (auto itemDict : interface->freeAllocationItems)
		{
			outItemBaseList.Add(itemDict.Value);
		}
	}
	return outItemBaseList;
}

void ATeamDropBoxCharacter::OnPlayerBeginOverlap_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(this);
}

void ATeamDropBoxCharacter::OnPlayerEndOverlap_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(this);
	OnClosedWnd();
}

bool ATeamDropBoxCharacter::isVisible(const UINT64 &PlayerDBID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("----- check TongDropBox is visible "));
	KBEngine::Entity* DropBox = GetSelfEntity();

	if (DropBox != nullptr)
	{
		UTeamDropBoxInterface* interface = Cast<UTeamDropBoxInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("TeamDropBoxInterface"), DropBox->ID()));
		if (interface != nullptr)
		{
			if (interface->isVisible())
				return true;
		}
	}

	return false;
}