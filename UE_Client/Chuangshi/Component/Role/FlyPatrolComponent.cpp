// Fill out your copyright notice in the Description page of Project Settings.


#include "FlyPatrolComponent.h"

#include "time.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/CapsuleComponent.h"
#include "Engine/EngineTypes.h"

#include "GameData/TeamMemberData.h"
#include "GameData/CharacterData.h"
#include "Interface/Role/RoleSpaceContentInterface.h"
#include "Interface/SkillInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/Role/RoleTeamInterface.h"
#include "Manager/ResourceManager.h"
#include "Manager/StoryManager.h"
#include "CS3Base/UIManager.h"
#include "Component/Role/RideCarrierComponent.h"
#include "../AppearanceComponent.h"
#include "Actor/Pet/FlyCharacter.h"
#include "Manager/VisibleManager.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/Operation/OperationModeMgr.h"
#include "Manager/AtkStateMar.h"
#include "Manager/SkillManager.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/AudioManager.h"
#include "Manager/ParticleManager.h"
#include "Manager/EventManager.h"
#include "Actor/ServerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameFramework/Character.h"
#include "Actor/GameCharacter.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/ConvertUtil.h"
#include "GameData/ShortcutKeyData.h"
#include "CS3Base/GameObject.h"
#include "CS3Base/BaseWindow.h"
#include "Interface/Role/RolePetInterface.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "Kismet/KismetMathLibrary.h"
#include "../../Interface/Role/RoleInterface.h"
#include "Interface/GameObjectInterface.h"
#include "Actor/NPC/ClientGameCharacter.h"

CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("EnterFlyPatrol"), STAT_EnterFlyPatrol, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("PauseFlyPatrol"), STAT_PauseFlyPatrol, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("ReviveFlyPatrol"), STAT_ReviveFlyPatrol, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("StartPreFlyPatrol"), STAT_StartPreFlyPatrol, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("BindFlyAttachActor"), STAT_BindFlyAttachActor, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("OnStopFlyPatrol"), STAT_OnStopFlyPatrol, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("StartFlyPatrol"), STAT_StartFlyPatrol, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("CheckFlyPatrol"), STAT_CheckFlyPatrol, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("CheckFlyPatrolEvent"), STAT_CheckFlyPatrolEvent, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("SwitchFlyOrbitMode"), STAT_SwitchFlyOrbitMode, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("EnterFlyToSubSpace"), STAT_EnterFlyToSubSpace, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("OnStopFlyToSubSpace"), STAT_OnStopFlyToSubSpace, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("OnFlySinglePatrol"), STAT_OnFlySinglePatrol, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("OnFlyMultPatrol"), STAT_OnFlyMultPatrol, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("CheckMultPatrolFlyToSubSpace"), STAT_CheckMultPatrolFlyToSubSpace, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("BindCharacterToFlyAttach"), STAT_BindCharacterToFlyAttach, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("CheckSinglePatrolFlyToSubSpace"), STAT_CheckSinglePatrolFlyToSubSpace, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("PlayFlyPatrolActionOverInSubSpace"), STAT_PlayFlyPatrolActionOverInSubSpace, STATGROUP_UFlyPatrolComponent);
DECLARE_CYCLE_STAT(TEXT("DestroySubSpaceOfFlyAttachActor"), STAT_DestroySubSpaceOfFlyAttachActor, STATGROUP_UFlyPatrolComponent);

UFlyPatrolComponent::UFlyPatrolComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	ResetFlyPatrolData();
	CurFlyPatrolID = TEXT("");
	FlyPatrolState = FLYPATORLSTATE_TYPE::NONE;
	HZMGTeamMembsModle.Empty();
	FlyHZMGSpaceData.Reset();
	ParachuteCharacter = nullptr;
}

void UFlyPatrolComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);
	ClearFlyPatrolHandle();
	DestroyFlyAttachActor();
}

void UFlyPatrolComponent::TickComponent(float DeltaTime, enum ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (PlayerCharacter->ActorIsPlayer())
	{
		CheckSkyCarrierMoveEffect(DeltaTime);
		CheckAutoOpenYCJMDParachute(DeltaTime);
	}
	
}

void UFlyPatrolComponent::EnterFlyPatrol(FString FlyPatrolID, const FString InCarrierId, const FString FlyModleId)
{
	SCOPE_CYCLE_COUNTER(STAT_EnterFlyPatrol);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===FlyPatrolCpt::EnterFlyPatrol[FlyModleId=%s, InCarrierId=%s, FlyModleId=%s]"), *FlyPatrolID, *InCarrierId, *FlyModleId);

	const FFLY_PATROL_DATA* FlyPatrolData = GetFlyPatrolData(FlyPatrolID);

	if (FlyPatrolData == nullptr || FlyPatrolData->FlyPoints.Num() <= 0 || (FlyPatrolData->SpaceName != UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_SCRIPT_ID")))) return;

	//第一次播放起飞不会进入此逻辑（只有后面要接到下一条飞行路线时，才会进入此逻辑）
	if (IsNormalFlyPatrolState() && CurFlyPatrolID.Compare(FlyPatrolID))
	{
		onNotifyRemoveEffectList(CurFlyPatrolID);
		ResetFlyPatrolData();
		CurFlyPatrolID = FlyPatrolID;
		onNotifyAddEffectList(FlyPatrolID, FlyPatrolData->EffectList);
		StartFlyPatrol(CurFlyPatrolID);
	}
	else 
	{
		onNotifyAddEffectList(FlyPatrolID, FlyPatrolData->EffectList);
		ExecuteRideOnCarrierOrFlyActor(FlyPatrolID, InCarrierId, FlyModleId);
	}	
}

void UFlyPatrolComponent::StopFlyPatrol(float DelayTime /*= 0.0f*/)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===FlyPatrolCpt::StopFlyPatrol[DelayTime=%s]"), DelayTime);

	if (IsNormalFlyPatrolState())
	{
		OnStopFlyPatrol(DelayTime);
	}
	else if (IsHZMGFlyState())
	{
		OnStopFlyToHZMGSpace();
	}
}

void UFlyPatrolComponent::StopCycleFlyPatrol(FString FlyPatrolID)
{
	FlyMoveInfo.Reset();
	ReviveFlyPatrol();
	EnterFlyPatrol(FlyPatrolID);
}

void UFlyPatrolComponent::PauseFlyPatrol()
{
	SCOPE_CYCLE_COUNTER(STAT_PauseFlyPatrol);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===FlyPatrolCpt::PauseFlyPatrol"));

	if (!IsNormalFlyPatrolState())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------APlayerCharacter::PauseFlyPatrol CurFlyPatrolID is empty----------%d"));
		return;
	}
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->bIsCanTurn = true;
	}

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController) && PlayerController->GetMoveType() == CS3_MOVE_TYPE::MOVE_TYPE_FLY)
	{
		FlyMoveInfo = PlayerController->GetFlyMoveInfo();
		APlayerCharacter* Player = Cast<APlayerCharacter>(GetOwner());
		if (IsValid(Player))
		{
			Player->StopPlayerMove();
		}
		
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------APlayerCharacter::PauseFlyPatrol CurFlyPatrolID =[%s]----------%d"), *CurFlyPatrolID);
	}
}

void UFlyPatrolComponent::ReviveFlyPatrol()
{
	SCOPE_CYCLE_COUNTER(STAT_ReviveFlyPatrol);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===FlyPatrolCpt::ReviveFlyPatrol"));

	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->bIsCanTurn = false;
	}
	if (!IsNormalFlyPatrolState() || FlyMoveInfo.FlyLocation.IsNearlyZero())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------APlayerCharacter::ReviveFlyPatrol CurFlyPatrolID is empty----------%d"));
		return;
	}

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->FlyToLocation(FlyMoveInfo.FlyLocation, FlyMoveInfo.bIsFlyPatrol, FlyMoveInfo.bIsFixedDirection, FlyMoveInfo.FlyCallback);
		FlyMoveInfo.Reset();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------APlayerCharacter::ReviveFlyPatrol CurFlyPatrolID =[%s]----------%d"), *CurFlyPatrolID);
	}
}

bool UFlyPatrolComponent::IsPausedFlyPatrol()
{
	return ((IsNormalFlyPatrolState() && !FlyMoveInfo.FlyLocation.IsNearlyZero()) || 
		(IsHZMGFlyState() && FlyHZMGSpaceData.EndPoint == FlyHZMGSpaceData.StartPoint&&FlyHZMGSpaceData.StartPoint == 0)) ? true : false;
}


void UFlyPatrolComponent::StartPreFlyPatrol(const FString FlyModleId)
{
	SCOPE_CYCLE_COUNTER(STAT_StartPreFlyPatrol);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===FlyPatrolCpt::StartPreFlyPatrol[FlyModleId=%s]"), *FlyModleId);

	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::StartPreFlyPatrol : PlayerCharacter!"));
		return;
	}
	FlyPatrolState = FLYPATORLSTATE_TYPE::GETON;
	//生成飞行Character
	BindFlyAttachActor(FlyModleId);

	FName ActionId = "Show_FloatGeton";
	FActionOverDelegate Delegate;
	Delegate.AddUObject(this, &UFlyPatrolComponent::PlayFlyPatrolActionOver);
	PlayerCharacter->PlayAction(ActionId, 0.0f, Delegate);
}

void UFlyPatrolComponent::ExecuteRideOnCarrierOrFlyActor(FString FlyPatrolID, const FString InCarrierId, const FString FlyModleId)
{
	APlayerCharacter* playercharacter = Cast<APlayerCharacter>(GetOwner());
	if (IsValid(playercharacter))
	{
		//bIsDisRideOnCarrier这个判断是因为在下载具后，还需要加载单独的人物外观需要时间
		if (playercharacter->IsCarrierState() || playercharacter->IsDisCarrierState())
		{
			FlyPatrolState = FLYPATORLSTATE_TYPE::DisRide;
			TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr(this);
			TWeakObjectPtr<APlayerCharacter> DelayPlayerCharacterPtr(playercharacter);
			playercharacter->OnDisRideOnPetOver = FDisRideOnPetOverDelegate::CreateLambda([DelayThisPtr, FlyPatrolID, InCarrierId, DelayPlayerCharacterPtr, FlyModleId]()
			{
				CS3_Warning(TEXT(" UFlyPatrolComponent::ExecuteRideOnCarrierOrFlyActor OnDisRideOnPetOver"));
				if (DelayThisPtr.IsValid() && DelayPlayerCharacterPtr.IsValid())
				{
					UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
					APlayerCharacter* PlayerCharacterPtr = DelayPlayerCharacterPtr.Get();
					PlayerCharacterPtr->StopPlayerMove();
					ThisPtr->CurFlyPatrolID = FlyPatrolID;
					PlayerCharacterPtr->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
					if (InCarrierId.IsEmpty())
					{
						ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

						if (IsValid(PlayerController) && PlayerCharacterPtr->ActorIsPlayer())
						{
							PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_FLY_ORBIT, true);
						}
						ThisPtr->StartPreFlyPatrol(FlyModleId);
					}
					else
					{
						ThisPtr->FlyPatrolState = FLYPATORLSTATE_TYPE::RIDEONCARRIER;
						PlayerCharacterPtr->RideCarrierComponent->RideOnCarrier(InCarrierId);
					}
				}
			});
		}
		else
		{
			CurFlyPatrolID = FlyPatrolID;
			playercharacter->StopPlayerMove();
			playercharacter->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
		
			if (InCarrierId.IsEmpty())
			{
				ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

				if (IsValid(PlayerController) && playercharacter->ActorIsPlayer())
				{
					PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_FLY_ORBIT, true);
				}
				StartPreFlyPatrol(FlyModleId);
			}
			else
			{
				FlyPatrolState = FLYPATORLSTATE_TYPE::RIDEONCARRIER;
				playercharacter->RideCarrierComponent->RideOnCarrier(InCarrierId);
			}
		}
	}
}

void UFlyPatrolComponent::BindFlyAttachActor(const FString FlyModleId)
{
	SCOPE_CYCLE_COUNTER(STAT_BindFlyAttachActor);
	
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::BindFlyAttachActor : PlayerCharacter||Instance||Instance->CfgManager!"));
		return;
	}

	const FCARRIER_DATA *CarrierData = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CARRIER)->GetRow<FCARRIER_DATA>(FSTRING_TO_FNAME(FlyModleId));
	if (CarrierData)
	{
		StartBindFlyCharacter(CarrierData->CarrierModelId);
	}
	else
	{
		LoadFlySword();
	}
}

void UFlyPatrolComponent::StartBindFlyCharacter(FString FlyCarrierModelId)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::StartBindFlyCharacter : PlayerCharacter!"));
		return;
	}

	clock_t AssetTime = clock();

	FlyCharacter = UGolbalBPFunctionLibrary::SpawnActor<AFlyCharacter>();
	FlyCharacter->GetAppearanceComponent()->CreateAppearance(FlyCarrierModelId);
	TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr(this);
	TWeakObjectPtr<APlayerCharacter> DelayPlayerCharacterPtr(PlayerCharacter);
	TWeakObjectPtr<AFlyCharacter> DelayFlyCharacterPtr(FlyCharacter);
	FlyCharacter->FlyCharacterOnCreateModelOver = FFlyCharacterOnCreateModelOverDelegate::CreateLambda([DelayThisPtr, DelayPlayerCharacterPtr, DelayFlyCharacterPtr, AssetTime]()
	{
		clock_t AssetTime1 = clock();
		if (DelayThisPtr.IsValid() && DelayPlayerCharacterPtr.IsValid() && DelayFlyCharacterPtr.IsValid())
		{
			UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
			APlayerCharacter* PlayerCharacterPtr = DelayPlayerCharacterPtr.Get();
			AFlyCharacter* FlyCharacterPtr = DelayFlyCharacterPtr.Get();
			if (AssetTime1 - AssetTime < 700)
			{
				ThisPtr->OnUpdateFlyCharacterVisibility(false);

				FTimerHandle DelayHandle;
				if (IsValid(UUECS3GameInstance::Instance))
				{
					AActor* OwnerActor = ThisPtr->GetOwner();
					if (IsValid(OwnerActor))
					{
						UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(OwnerActor, DelayHandle, FTimerDelegate::CreateLambda([DelayThisPtr]() {
							if (DelayThisPtr.IsValid())
							{
								UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
								ThisPtr->OnUpdateFlyCharacterVisibility();
							}
						}), 0.7f - (AssetTime1 - AssetTime) / 1000, false);
					}
				}
			}
			FTransform RidePetSocketTransformCt = FlyCharacterPtr->GetMesh()->GetSocketTransform(TEXT("Socket_Ride"), RTS_Component);
			FVector RidePetSocketLoctionCt = RidePetSocketTransformCt.GetLocation();//取插槽相对root点位置
			float SocketRideSapceZ = FMath::Abs(RidePetSocketLoctionCt.Z);///算出骑士出来后偏移多少才能贴地
			FVector RidePetSocketRideLocation = FlyCharacterPtr->GetMesh()->GetRelativeTransform().GetLocation();
			FVector ToRideLocation = RidePetSocketRideLocation - FVector(0.0f, 0.0f, SocketRideSapceZ);
			FlyCharacterPtr->AttachToComponent(PlayerCharacterPtr->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, TEXT("Socket_Root"));
			FlyCharacterPtr->SetActorRelativeLocation(ToRideLocation);
			FlyCharacterPtr->SetActorRelativeRotation(FRotator(0.0f, 90.0f, 0.0f));
			PlayerCharacterPtr->AddActorLocalOffset(-ToRideLocation);
		}
	});
}

void UFlyPatrolComponent::LoadFlySword()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::LoadFlySword : PlayerCharacter!"));
		return;
	}

	int32 PlayerCamp = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerCharacter->EntityId, TEXT("camp"));
	const FFLY_PATROL_BIND_DATA *FlyCarrierBindData = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_FLY_CARRIER)->GetRow<FFLY_PATROL_BIND_DATA>(FSTRING_TO_FNAME(INT_TO_FSTRING(PlayerCamp)));
	if (!FlyCarrierBindData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::LoadFlySword : FlyCarrierBindData!"));
		return;
	}
	//判断如果没有骨架，就肯定没有模型了
	if (FlyCarrierBindData->SkeletalMeshPath.ToSoftObjectPath().IsValid())
	{
		TArray<FStringAssetReference> LoadPartArray;
		LoadPartArray.Add(FlyCarrierBindData->SkeletalMeshPath.ToSoftObjectPath());
		LoadPartArray.Add(FlyCarrierBindData->AnimationAssetPath.ToSoftObjectPath());
		TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr(this);

		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, LoadPartArray,
			FStreamableDelegate::CreateLambda([DelayThisPtr, FlyCarrierBindData]()
		{
			if (DelayThisPtr.IsValid())
			{
				UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
				ThisPtr->StartBindSwordFlyCharacter(*FlyCarrierBindData);
			}
		}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER, GetOwner()->GetActorLocation());
	}
}

void UFlyPatrolComponent::StartBindSwordFlyCharacter(FFLY_PATROL_BIND_DATA FlyCarrierBindData)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::StartBindSwordFlyCharacter : PlayerCharacter!"));
		return;
	}
	FlyCharacter = UGolbalBPFunctionLibrary::SpawnActor<AFlyCharacter>();
	FlyCharacter->GetAppearanceComponent()->CreateAppearance(TEXT("SK_GW2421_Carrier"));

	clock_t AssetTime = clock();
	TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr(this);
	TWeakObjectPtr<APlayerCharacter> DelayPlayerCharacterPtr(PlayerCharacter);
	TWeakObjectPtr<AFlyCharacter> DelayFlyCharacterPtr(FlyCharacter);

	FlyCharacter->FlyCharacterOnCreateModelOver = FFlyCharacterOnCreateModelOverDelegate::CreateLambda([
		DelayThisPtr, DelayPlayerCharacterPtr, DelayFlyCharacterPtr, AssetTime, FlyCarrierBindData]()
	{
		clock_t AssetTime1 = clock();
		if (!DelayThisPtr.IsValid() || !DelayPlayerCharacterPtr.IsValid() || !DelayFlyCharacterPtr.IsValid())
		{
			return;
		}

		UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
		APlayerCharacter* PlayerCharacterPtr = DelayPlayerCharacterPtr.Get();
		AFlyCharacter* FlyCharacterPtr = DelayFlyCharacterPtr.Get();
		if (AssetTime1 - AssetTime < 700)
		{
			ThisPtr->OnUpdateFlyCharacterVisibility(false);

			FTimerHandle DelayHandle;
			if (IsValid(UUECS3GameInstance::Instance))
			{
				AActor* OwnerActor = ThisPtr->GetOwner();
				if (IsValid(OwnerActor))
				{
					UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(OwnerActor, DelayHandle, FTimerDelegate::CreateLambda([DelayThisPtr]() {
						if (DelayThisPtr.IsValid())
						{
							UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
							ThisPtr->OnUpdateFlyCharacterVisibility();
						}
					}), 0.7f - (AssetTime1 - AssetTime) / 1000, false);
				}
			}
		}

		//==========将飞剑绑定在FlyCharacter上
 		int32 PlayerCamp = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerCharacterPtr->EntityId, TEXT("camp"));
 		FString ComponentName = TEXT("SKelMeshFlyPatrolCom") + INT_TO_FSTRING(PlayerCamp);
 		USkeletalMeshComponent* AttachMeshPartComponent = NewObject<USkeletalMeshComponent>(ThisPtr, USkeletalMeshComponent::StaticClass(), FSTRING_TO_FNAME(ComponentName));
 		AttachMeshPartComponent->RegisterComponent(); 
		AttachMeshPartComponent->AttachToComponent(FlyCharacterPtr->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, TEXT("Socket_Root1"));
 		ThisPtr->BindMeshComponentDatas.Add(FSTRING_TO_FNAME(ComponentName), AttachMeshPartComponent);
 
 		USkeletalMesh* SkeletalMesh = FlyCarrierBindData.SkeletalMeshPath.Get();
 		AttachMeshPartComponent->SetSkeletalMesh(SkeletalMesh);
 		AttachMeshPartComponent->SetRelativeScale3D(FVector(2.0f, 2.0f, 2.0f));
 
 		UAnimationAsset* ActionAnimation = FlyCarrierBindData.AnimationAssetPath.Get();
 		AttachMeshPartComponent->PlayAnimation(ActionAnimation, true);

		//将FlyCharacter绑定在玩家上
		FTransform RidePetSocketTransformCt = FlyCharacterPtr->GetMesh()->GetSocketTransform(TEXT("Socket_Ride"), RTS_Component);
		FVector RidePetSocketLoctionCt = RidePetSocketTransformCt.GetLocation();//取插槽相对root点位置
		float SocketRideSapceZ = FMath::Abs(RidePetSocketLoctionCt.Z) - 60;///算出骑士出来后偏移多少才能贴地（-60是因为共用了云的空骨骼，Socket_Ride设置的比较高，是适应云的，飞剑的话飞剑与角色之间有空隙，但不能直接修改骨骼，代码调整）
		FVector RidePetSocketRideLocation = FlyCharacterPtr->GetMesh()->GetRelativeTransform().GetLocation();
		FVector ToRideLocation = RidePetSocketRideLocation - FVector(0.0f, 0.0f, SocketRideSapceZ);
		FlyCharacterPtr->AttachToComponent(PlayerCharacterPtr->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, TEXT("Socket_Root"));
		FlyCharacterPtr->SetActorRelativeLocation(ToRideLocation);
		FlyCharacterPtr->SetActorRelativeRotation(FRotator(0.0f, 90.0f, 0.0f));
		PlayerCharacterPtr->AddActorLocalOffset(-ToRideLocation);
	});
}

void UFlyPatrolComponent::PlayFlyPatrolActionOver(ACharacter* Character, FACTION_DATA ActionData)
{	
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===FlyPatrolCpt::PlayFlyPatrolActionOver[ChacterName=%s]"), *(Character->GetName()));

	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter)|| !PlayerCharacter->ActorIsPlayer())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::PlayFlyPatrolActionOver : PlayerCharacter!"));
		return;
	}	
	SwitchFlyOrbitMode();
}

void UFlyPatrolComponent::OnStopFlyPatrol(float DelayTime /*= 0.0f*/)
{
	SCOPE_CYCLE_COUNTER(STAT_OnStopFlyPatrol);
	APlayerCharacter* playercharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(playercharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::OnStopFlyPatrol : PlayerCharacter!"));
		return;
	}
	if (IsFlyPatrolState())
	{
		if (playercharacter->OnDisRideOnPetOver.IsBound())
		{
			playercharacter->OnDisRideOnPetOver = nullptr;
		}
		playercharacter->StopAction();
		playercharacter->GetCharacterMovement()->MaxFlySpeed = 2000.0f;
		playercharacter->GetCharacterMovement()->SetMovementMode(MOVE_Walking);
		playercharacter->StopPlayerMove();
		if (IsValid(HZMGFlyAttachActor) || IsValid(FlyCharacter))
		{
			FName ActionId = "Show_FloatGetoff";
			playercharacter->PlayAction(ActionId);
			if (DelayTime > 0)
			{
				FTimerHandle DelayHandle;
				if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
				{
					UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, this, &UFlyPatrolComponent::DestroyFlyAttachActor, DelayTime, false);
				}
			}
			else
			{
				DestroyFlyAttachActor();
			}
		}
		else
		{
			playercharacter->RideCarrierComponent->DisRideOnCarrier();
		}

		KBEngine::Entity* Role = playercharacter->GetSelfEntity();
		if (Role == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::OnStopFlyPatrol : Role!"));
		}
		else
		{
			USkillInterface * SkillInterface = ((GameObject*)Role)->Interface_Cache.SkillInterface;
			if (SkillInterface)
			{
				SkillInterface->RPC_onStopFlyPatrol(CurFlyPatrolID);
			}
		}
		FlyPatrolState = FLYPATORLSTATE_TYPE::NONE;
		CurFlyPatrolID = TEXT("");
		FlyMoveInfo.Reset();
		if (playercharacter->GetOldCollision() != ECollisionEnabled::NoCollision)
		{
			playercharacter->GetCapsuleComponent()->SetCollisionEnabled(playercharacter->GetOldCollision());
		}
	}
}

void UFlyPatrolComponent::StartFlyPatrol(FString FlyPatrolID)
{
	SCOPE_CYCLE_COUNTER(STAT_StartFlyPatrol);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===FlyPatrolCpt::StartFlyPatrol[FlyPatrolID=%s]"), *FlyPatrolID);

	APlayerCharacter* playercharacter = Cast<APlayerCharacter>(GetOwner());
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(playercharacter) || !IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::StartFlyPatrol : PlayerCharacter||PlayerController!"));
		return;
	}
	if (playercharacter->GetSelfEntity() && !playercharacter->GetSelfEntity()->IsPlayer())return;

	const FFLY_PATROL_DATA* FlyPatrolData = GetFlyPatrolData(FlyPatrolID);
	if (FlyPatrolData == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::StartFlyPatrol : FlyPatrolData!"));
		return;
	}
	
	TArray<FVector> FlyPoints = FlyPatrolData->FlyPoints;
	FVector FirstPoint = FlyPoints[0];
	float FlySpeed = playercharacter->GetCharacterMovement()->MaxFlySpeed;
	float FirstSpeed = FlyPatrolData->FlySpeeds[0];
	if (FirstSpeed > 0.0f)
	{
		playercharacter->GetCharacterMovement()->MaxFlySpeed = FirstSpeed;
		FlySpeed = FirstSpeed;
	}
	StartFlyPatrolEvent();
	ResetFlyPatrolData();

	if (IsNormalFlyPatrolState())
	{
		FlyPatrolState = FLYPATORLSTATE_TYPE::FLYING;
		TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr(this);
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("===FlyPatrolCpt::[%f,  %f,  %f]"), FirstPoint.X, FirstPoint.Y, FirstPoint.Z);

		//先移动到第一点起飞的点
		PlayerController->FlyToLocation(FirstPoint, true, false, FTraceCallback::CreateLambda([DelayThisPtr, FlySpeed, FirstPoint](bool IsSuccess)
		{
			if (DelayThisPtr.IsValid())
			{
				UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
				ThisPtr->CheckFlyPatrol(FlySpeed, FirstPoint, IsSuccess);
			}
		}));
	}
	else if (IsHZMGFlyState())
	{
		FlyPatrolState = FLYPATORLSTATE_TYPE::HZMGFLYING;
		this->OnFlyToHZMGSpace(FlyHZMGSpaceData.PatrolID, FlyHZMGSpaceData.StartPoint, FlyHZMGSpaceData.EndPoint, FlyHZMGSpaceData.Speed, FlyHZMGSpaceData.EndPos);
	}

	if (playercharacter->GetOldCollision()== ECollisionEnabled::NoCollision)
	{
		playercharacter->SetOldCollision(playercharacter->GetCapsuleComponent()->GetCollisionEnabled());
		playercharacter->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
	else
	{
		playercharacter->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
}

void UFlyPatrolComponent::StartFlyPatrolEvent()
{
	const FFLY_PATROL_DATA* FlyPatrolData = GetFlyPatrolData(CurFlyPatrolID);
	if (FlyPatrolData == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::StartFlyPatrolEvent : FlyPatrolData!"));
		return;
	}
	for (auto data : FlyPatrolData->FlyTimeEventIDs)
	{
		FTimerHandle TimerHandle;
		if (IsValid(UUECS3GameInstance::Instance))
		{
			AActor* OwnerActor = GetOwner();
			if (IsValid(OwnerActor))
			{
				TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr(this);
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(OwnerActor, TimerHandle, FTimerDelegate::CreateLambda([DelayThisPtr, data]() {
					if (DelayThisPtr.IsValid())
					{
						UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
						ThisPtr->CheckFlyPatrolEvent(data.FlyEventData);
					}
				}), data.FlyEventTime, false);
			}
		}
	}
}

void UFlyPatrolComponent::CheckFlyPatrol(float FlySpeed, const FVector& Point, bool IsSuccess)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckFlyPatrol);

	const FFLY_PATROL_DATA* FlyPatrolData = GetFlyPatrolData(CurFlyPatrolID);
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (nullptr != FlyPatrolData && IsSuccess && IsValid(PlayerController))
	{
		UAtkStateMar* AtkStateMar = PlayerController->GetAtkStateMar();

		TArray<FVector> FlyPoints = FlyPatrolData->FlyPoints;
		int32 index = FlyPoints.Find(Point);
		if (index < 0)
		{
			if (!IsValid(AtkStateMar))
			{
				OnStopFlyPatrol();
				CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::CheckFlyPatrol : AtkStateMar!"));
				return;
			}
			AtkStateMar->SwitchFlyOrbitMode(false, TEXT(""));
			return;
		}
		if (FlyPatrolData->FlyEventIDs.Num() > index)
		{
			FFLYEVENT_DATA EventID = FlyPatrolData->FlyEventIDs[index];
			CheckFlyPatrolEvent(EventID, Point);
		}
		if (index == (FlyPoints.Num() - 1) && 0 == CurFlyCount)
		{
			if (IsValid(AtkStateMar))
			{
				AtkStateMar->SwitchFlyOrbitMode(false, TEXT(""));
			}
		}
		else
		{
			APlayerCharacter* playercharacter = Cast<APlayerCharacter>(GetOwner());
			if (!IsValid(playercharacter))
			{
				CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::CheckFlyPatrol : playercharacter!"));
				return;
			}
			playercharacter->GetCharacterMovement()->MaxFlySpeed = FlySpeed;
			float NextSpeed = 0;
			FVector NextPoint = FVector::ZeroVector;
			if (CurFlyCount > 0)
			{
				int StartCycleFlyIndex = FlyPoints.Find(StartCycleFlyPoint);

				int CycleCount = 0;
				FString CycleFlyID;
				TArray<FString>CycleData = UGolbalBPFunctionLibrary::SplitString(FlyPatrolData->FlyEventIDs[StartCycleFlyIndex].Params);
				if (CycleData.Num() > 0)
				{
					CycleCount = FSTRING_TO_INT(CycleData[0]);
				}
				if (CycleData.Num() > 1)
				{
					CycleFlyID = CycleData[1];
				}

				if (CycleCount == CurFlyCount && EndCycleFlyPoint == Point)
				{
					StopCycleFlyPatrol(CycleFlyID);
				}
				else
				{
					if (index == (FlyPoints.Num() - 1))
					{
						NextSpeed = FlyPatrolData->FlySpeeds[StartCycleFlyIndex];
						NextPoint = FlyPoints[StartCycleFlyIndex];
						++CurFlyCount;
					}
					else
					{
						NextSpeed = FlyPatrolData->FlySpeeds[index + 1];
						NextPoint = FlyPoints[index + 1];
					}
				}
			}
			else
			{
				NextSpeed = FlyPatrolData->FlySpeeds[index + 1];
				NextPoint = FlyPoints[index + 1];
			}

			if (NextSpeed > 0.0f)
			{
				playercharacter->GetCharacterMovement()->MaxFlySpeed = NextSpeed;
				FlySpeed = NextSpeed;
			}

			PlayerController->FlyToLocation(NextPoint, true, false, FTraceCallback::CreateLambda([this, FlySpeed, NextPoint](bool IsSuccess)
			{
				this->CheckFlyPatrol(FlySpeed, NextPoint, IsSuccess);
			}));
		}
	}
	else
	{
		StopFlyPatrol();
	}
}

void UFlyPatrolComponent::CheckFlyPatrolEvent(const FFLYEVENT_DATA& FlyEvent, const FVector& Point /*= FVector(0, 0, 0)*/)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckFlyPatrolEvent);

	APlayerCharacter* playercharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(playercharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::CheckFlyPatrolEvent : playercharacter!"));
		return;
	}
	if (!FlyEvent.Params.IsEmpty())
	{
		switch (FlyEvent.FlyEventType)
		{
		case EFLYEVENT::STORY:
		{
			if (playercharacter->CameraParamsEventID > 0)
			{
				playercharacter->ClearCameraParamsEvent();
			}
			//播放镜头
			UGStoryManager* GStoryManager = UGolbalBPFunctionLibrary::GStoryManager();
			if (GStoryManager)
			{
				GStoryManager->PlaySequence(FlyEvent.Params);
				CS3_Log(TEXT("UFlyPatrolComponent::CheckFlyPatrolEvent : STORY GStoryManager->PlaySequence FlyEvent.Params(%s)!"), *FlyEvent.Params);
			}

			break;
		}
		case  EFLYEVENT::SKILL:
		{
			if (playercharacter->CameraParamsEventID > 0)
			{
				playercharacter->ClearCameraParamsEvent();
			}
			//使用技能
			USkillInterface* SkillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
			int32 SkillID = (int32)FSTRING_TO_INT(FlyEvent.Params);
			USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillID);
			
			if (IsValid(SkillData) && IsValid(SkillInterface))
			{				
				SkillInterface->UseSkill(SkillID, playercharacter->EntityId);
				CS3_Log(TEXT("UFlyPatrolComponent::CheckFlyPatrolEvent : SKILL SkillInterface->UseSkil SkillID(%i) playercharacter->EntityId(%i)!"), SkillID, playercharacter->EntityId);
			}		
			
			break;
		}
		case EFLYEVENT::CAMERALOCK:
		{
			playercharacter->SetCameraParamsEvent(FlyEvent.Params);
			CS3_Log(TEXT("UFlyPatrolComponent::CheckFlyPatrolEvent : CAMERALOCK playercharacter->SetCameraParamsEvent FlyEvent.Params(%s)!"), *FlyEvent.Params);
			break;
		}
		case  EFLYEVENT::STOPFLY:
		{
			if (playercharacter->CameraParamsEventID > 0)
			{
				playercharacter->ClearCameraParamsEvent();
			}
			ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
			UAtkStateMar* AtkStateMar = nullptr;

			if (IsValid(PlayerController))
			{
				AtkStateMar = PlayerController->GetAtkStateMar();
			}

			if (!IsValid(AtkStateMar))
			{
				OnStopFlyPatrol(0.7f);
				CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::CheckFlyPatrolEvent : AtkStateMar!"));
				return;
			}
			AtkStateMar->SwitchFlyOrbitMode(false, TEXT(""), 0.7f);			

			ClearFlyPatrolHandle();
			if (IsValid(UUECS3GameInstance::Instance))
			{
				TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr(this);
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(playercharacter, FlyPatrolHandle, FTimerDelegate::CreateLambda([FlyEvent, DelayThisPtr]() {
					if (DelayThisPtr.IsValid() && !FlyEvent.Params.IsEmpty())
					{
						UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
						APlayerCharacter* playercharacter = Cast<APlayerCharacter>(ThisPtr->GetOwner());
						if (!IsValid(playercharacter))
						{
							CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::CheckFlyPatrolEvent : playercharacter!"));
							return;
						}
						//使用技能
						USkillInterface* SkillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
						int32 SkillID = (int32)FSTRING_TO_INT(FlyEvent.Params);
						USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillID);
						if (IsValid(SkillData))
						{
							SkillInterface->UseSkill(SkillID, playercharacter->EntityId);
							CS3_Log(TEXT("UFlyPatrolComponent::CheckFlyPatrolEvent : STOPFLY SkillInterface->UseSkill  SkillID(%i) playercharacter->EntityId(%i)!"), SkillID, playercharacter->EntityId);

						}
					}

				}), 0.7f, false);
			}
			return;
		}
		case  EFLYEVENT::STARTCYCLEFLY:
		{
			if (CurFlyCount == 0)
			{
				++CurFlyCount;
				StartCycleFlyPoint = Point;
				CS3_Log(TEXT("UFlyPatrolComponent::CheckFlyPatrolEvent : STARTCYCLEFLY!"));
			}
			break;
		}
		case  EFLYEVENT::ENDCYCLEFLY:
		{
			if (EndCycleFlyPoint == FVector::ZeroVector)
			{
				EndCycleFlyPoint = Point;
				CS3_Log(TEXT("UFlyPatrolComponent::CheckFlyPatrolEvent : ENDCYCLEFLY!"));
			}
			break;
		}		
		case EFLYEVENT::SPACEDYNAMIC:
		{
			GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
			if (CS3PlayerEntity == nullptr) return;

			URoleInterface* RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
			RoleInterface->RPC_ChangeFlySpaceEffect(FlyEvent.Params);
			CS3_Log(TEXT("UFlyPatrolComponent::CheckFlyPatrolEvent : SPACEDYNAMIC,RoleInterface->RPC_ChangeFlySpaceEffect FlyEvent.Params(%s)!"), *FlyEvent.Params);
			break;
		}
		}
	}
}

void UFlyPatrolComponent::DestroyFlyAttachActor()
{
	if (IsValid(HZMGFlyAttachActor))
	{
		HZMGFlyAttachActor->Destroy();
		HZMGFlyAttachActor = nullptr;
	}
	if (IsValid(FlyCharacter))
	{
		//=====解除绑定（不然在飞行结束之后会销毁玩家自己）
		for (TPair<FName, UMeshComponent*>& Comp : BindMeshComponentDatas)
		{
			UMeshComponent* AttachMeshPartComponent = Comp.Value;
			FlyCharacter->RemoveOwnedComponent(AttachMeshPartComponent);
			AttachMeshPartComponent->UnregisterComponent();
			AttachMeshPartComponent->DetachFromComponent(FDetachmentTransformRules::KeepRelativeTransform);
			AttachMeshPartComponent = nullptr;
		}
		BindMeshComponentDatas.Empty();
		FlyCharacter->DetachFromActor(FDetachmentTransformRules::KeepRelativeTransform);
		
		FlyCharacter->Destroy();
		FlyCharacter = nullptr;
	}
}

void UFlyPatrolComponent::ClearFlyPatrolHandle()
{
	if (FlyPatrolHandle.IsValid() && IsValid(UUECS3GameInstance::Instance)&&IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(FlyPatrolHandle);
	}
}

void UFlyPatrolComponent::ResetFlyPatrolData()
{
	StartCycleFlyPoint = FVector::ZeroVector;
	EndCycleFlyPoint = FVector::ZeroVector;
	CurFlyCount = 0;
}

void UFlyPatrolComponent::SwitchFlyOrbitMode(bool IsActivate /*= true*/)
{
	SCOPE_CYCLE_COUNTER(STAT_SwitchFlyOrbitMode);
	UAtkStateMar* AtkStateMar = nullptr;
	ACS3PlayerController* PlayerCon = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerCon))
	{
		AtkStateMar = PlayerCon->GetAtkStateMar();
	}
	else
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::SwitchFlyOrbitMode : PlayerCon!"));
	}

	if (IsValid(AtkStateMar))
	{
		if (IsActivate)
		{
			if (IsHZMGFlyState())
			{
				AtkStateMar->SwitchFlyOrbitMode(true, FlyHZMGSpaceData.PatrolID);
			}
			else if (IsNormalFlyPatrolState())
			{
				AtkStateMar->SwitchFlyOrbitMode(true, CurFlyPatrolID);
			}
		}
		else
		{
			if (AtkStateMar->IsHaveState(EATTACT_STATE::BEHAVIOR_FLY_DEKUVERY))
			{
				AtkStateMar->SwitchFlyOrbitMode(false, TEXT(""));
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::SwitchFlyOrbitMode : AtkStateMar!"));
	}
}

const FFLY_PATROL_DATA* UFlyPatrolComponent::GetFlyPatrolData(const FString& FlyPatrolID)
{
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::GetFlyPatrolData : Instance||Instance->CfgManager!"));
		return nullptr;
	}

	const FFLY_PATROL_DATA* FlyPatrolData = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_FLY_PATROL)->GetRow<FFLY_PATROL_DATA>(FlyPatrolID);

	if (FlyPatrolData == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:FFLY_PATROL_DATA* UFlyPatrolComponent::GetFlyPatrolData : FlyPatrolData!"));
	}

	return FlyPatrolData;
}


void UFlyPatrolComponent::EnterFlyToHZMGSpace(const FString fPatrolID, const FString sPatrolID, const int32 sPoint, const int32 pPoint, float speed, FVector enterPos)
{
	SCOPE_CYCLE_COUNTER(STAT_EnterFlyToSubSpace);
	const FFLY_PATROL_DATA* FlyPatrolData = GetFlyPatrolData(fPatrolID);
	if ((FlyPatrolData == nullptr) || FlyPatrolData->FlyPoints.Num() <= 0 || (FlyPatrolData->SpaceName != UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_SCRIPT_ID")))) return;

	FFLYSUBSPACE_DATA flySubSpaceData;
	flySubSpaceData.Init(fPatrolID, sPatrolID, sPoint, pPoint, speed, enterPos);

	if (IsHZMGFlyState())
	{
		onNotifyRemoveEffectList(FlyHZMGSpaceData.PatrolID);
		CurFlyPatrolID = TEXT("");
		FlyHZMGSpaceData = flySubSpaceData;
		onNotifyAddEffectList(FlyHZMGSpaceData.PatrolID, FlyPatrolData->EffectList);
		StartFlyPatrol(fPatrolID);
		return;
	}
	onNotifyAddEffectList(FlyHZMGSpaceData.PatrolID, FlyPatrolData->EffectList);
	DisRideOnCarrierToHZMGFly(flySubSpaceData);
}

void UFlyPatrolComponent::StopFlyToHZMGSpace(const FString FlyID)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UAtkStateMar* AtkStateMar = nullptr;

	if (IsValid(PlayerController))
	{
		AtkStateMar = PlayerController->GetAtkStateMar();
	}

	if (IsValid(AtkStateMar))
	{
		AtkStateMar->SwitchFlyOrbitMode(false, TEXT(""), 0.7f);
	}
}

void UFlyPatrolComponent::OnStopFlyToHZMGSpace()
{
	SCOPE_CYCLE_COUNTER(STAT_OnStopFlyToSubSpace);
	AActor* OwnerActor = GetOwner();
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(OwnerActor);
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::OnStopFlyToSubSpace : PlayerCharacter!"));
		return;
	}

	if (IsHZMGFlyState())
	{
		KBEngine::Entity* Role = PlayerCharacter->GetSelfEntity();
		if (Role == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::OnStopFlyToSubSpace : Role!"));
			return;
		}
		KBEngine::FVariantArray Args;
		if (!(FlyHZMGSpaceData.EndPoint == -1 && FlyHZMGSpaceData.StartPoint == -1 && FlyHZMGSpaceData.EndPos == FVector(-1.0f, -1.0f, -1.0f)))
		{		

			USkillInterface * SkillInterface = ((GameObject*)Role)->Interface_Cache.SkillInterface;
			if (SkillInterface)
			{
				SkillInterface->RPC_onStopFlyPatrol(FlyHZMGSpaceData.PatrolID);
			}
		}
		else
		{
			onNotifyRemoveEffectList(FlyHZMGSpaceData.PatrolID);
			URoleSpaceContentInterface * RoleSpaceContentInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"),Role->ID()));
			if (RoleSpaceContentInterface)
			{
				RoleSpaceContentInterface->RPC_onMagicMazeEndFly();
			}
		}

		CurFlyPatrolID = TEXT("");
		FlyHZMGSpaceData.Reset();
		FlyPatrolState = FLYPATORLSTATE_TYPE::NONE;
		if (PlayerCharacter->OnDisRideOnPetOver.IsBound())
		{
			PlayerCharacter->OnDisRideOnPetOver = nullptr;
		}
		PlayerCharacter->StopPlayerMove();
		PlayerCharacter->StopAction();
		PlayerCharacter->GetCharacterMovement()->MaxFlySpeed = 2000.0f;
		PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Walking);

		FName ActionId = "Show_FloatGetoff";
		PlayerCharacter->PlayAction(ActionId);

		//从绑定点移除
		if (IsValid(HZMGFlyAttachActor))
		{
			HZMGFlyAttachActor->DetachFromActor(FDetachmentTransformRules::KeepRelativeTransform);
		}

		///<销毁队员模型
		if (HZMGTeamMembsModle.Num() > 0)
		{
			for (auto TeamMembModle : HZMGTeamMembsModle)
			{
				TeamMembModle->Destroy();
			}
		}

		HZMGTeamMembsModle.Reset();
		FTimerHandle DelayHandle;
		if (IsValid(UUECS3GameInstance::Instance)&&IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, this, &UFlyPatrolComponent::DestroyHZMGSpaceOfFlyAttachActor, 0.7f, false);
		}

		if (PlayerCharacter->GetOldCollision() != ECollisionEnabled::NoCollision)
		{
			PlayerCharacter->GetCapsuleComponent()->SetCollisionEnabled(PlayerCharacter->GetOldCollision());
		}
	}
}

bool UFlyPatrolComponent::IsHZMGFlyState()
{
	return (FlyPatrolState== FLYPATORLSTATE_TYPE::HZMGDisRide|| FlyPatrolState == FLYPATORLSTATE_TYPE::HZMGGETON|| FlyPatrolState == FLYPATORLSTATE_TYPE::HZMGRIDEONCARRIER||FlyPatrolState == FLYPATORLSTATE_TYPE::HZMGFLYING) ? true : false;
}

bool UFlyPatrolComponent::IsFlyPatrolState()
{
	return FlyPatrolState != FLYPATORLSTATE_TYPE::NONE;
}

void UFlyPatrolComponent::OnFlyToHZMGSpace(const FString fPatrolID, const int32 sPoint, const int32 pPoint, float speed, FVector enterPos)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::OnFlyToSubSpace : PlayerCharacter!"));
		return;
	}
	const FFLY_PATROL_DATA* FlyPatrolData = GetFlyPatrolData(fPatrolID);
	
	if (FlyPatrolData != nullptr)
	{
		if (FlyPatrolData->SpaceName != UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_SCRIPT_ID"))) return;

		if (sPoint == -1 && pPoint == -1 && enterPos == FVector(-1.0f, -1.0f, -1.0f))
		{
			OnHZMGFlyMultPatrol(fPatrolID, speed);
		}
		else
		{
			OnHZMGFlySinglePatrol(fPatrolID, sPoint, pPoint, speed, enterPos);
		}		
	}
}

void UFlyPatrolComponent::OnHZMGFlySinglePatrol(const FString fPatrolID, const int32 sPoint, const int32 pPoint, float speed, FVector enterPos)
{
	SCOPE_CYCLE_COUNTER(STAT_OnFlySinglePatrol);
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::OnFlySinglePatrol : PlayerCharacter!"));
		return;
	}
	FVector FirstPoint = FVector::ZeroVector;
	GetHZMGNearestFlyPoint(fPatrolID, sPoint, FirstPoint);
	if (FirstPoint == FVector::ZeroVector)
	{
		StopFlyToHZMGSpace(fPatrolID);
		CS3_Warning(TEXT("APlayerCharacter::OnFlyToSubSpace --- Can't Find StartPoint!"));
		return;
	}
	if (speed > 0.0f)
	{
		PlayerCharacter->GetCharacterMovement()->MaxFlySpeed = speed;
	}
	StartFlyPatrolEvent();
	ResetFlyPatrolData();
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->FlyToLocation(FirstPoint, true, false, FTraceCallback::CreateLambda([this, fPatrolID, FirstPoint, sPoint, pPoint, enterPos](bool IsSuccess)
		{
			this->CheckSinglePatrolFlyToHZMGSpace(fPatrolID, FirstPoint, sPoint, pPoint, enterPos, IsSuccess);
		}));
	}
}

void UFlyPatrolComponent::OnHZMGFlyMultPatrol(const FString PatrolID, float Speed)
{
	SCOPE_CYCLE_COUNTER(STAT_OnFlyMultPatrol);
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::OnFlyMultPatrol : PlayerController!"));
		return;
	}
	
	StartFlyPatrolEvent();
	ResetFlyPatrolData();
	const FFLY_PATROL_DATA* FlyPatrolData = GetFlyPatrolData(PatrolID);

	UAtkStateMar* AtkStateMar = PlayerController->GetAtkStateMar();
	AActor* OwnerActor = GetOwner();
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(OwnerActor);
	if (!IsValid(PlayerCharacter) || FlyPatrolData == nullptr)
	{
		if (!IsValid(AtkStateMar))
		{
			OnStopFlyPatrol();
			CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::OnFlyMultPatrol : FlyPatrolData||PlayerCharacter||AtkStateMar !"));
			return;
		}
		AtkStateMar->SwitchFlyOrbitMode(false, TEXT(""));
		return;
	}

	TArray<FVector> FlyPoints = FlyPatrolData->FlyPoints;
	FVector FirstPoint;
	if (FlyPoints.Num() > 0)
	{
		FirstPoint = FlyPoints[0];
	}
	else
	{
		if (!IsValid(AtkStateMar))
		{
			OnStopFlyPatrol();
			CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::OnFlyMultPatrol : AtkStateMar!"));
			return;
		}
		AtkStateMar->SwitchFlyOrbitMode(false, TEXT(""));
		return;
	}

	if (Speed > 0.0f)
	{
		PlayerCharacter->GetCharacterMovement()->MaxFlySpeed = Speed;
	}

	PlayerController->FlyToLocation(FirstPoint, true, false, FTraceCallback::CreateLambda([this, PatrolID, FirstPoint, Speed](bool IsSuccess)
	{
		this->CheckMultPatrolFlyToHZMGSpace(PatrolID, FirstPoint, IsSuccess);
	}));
}

void UFlyPatrolComponent::CheckMultPatrolFlyToHZMGSpace(const FString PatrolID,const FVector& Point, bool IsSuccess)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckMultPatrolFlyToSubSpace);
	APlayerCharacter* playercharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(playercharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::CheckMultPatrolFlyToSubSpace : playercharacter!"));
		return;
	}
	const FFLY_PATROL_DATA* FlyPatrolData = GetFlyPatrolData(PatrolID);
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (nullptr != FlyPatrolData && IsSuccess && IsValid(PlayerController))
	{
		UAtkStateMar* AtkStateMar = PlayerController->GetAtkStateMar();

		TArray<FVector> FlyPoints = FlyPatrolData->FlyPoints;
		int32 index = FlyPoints.Find(Point);
		if (index < 0)
		{
			if (!IsValid(AtkStateMar))
			{
				StopFlyPatrol();
				CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::CheckMultPatrolFlyToSubSpace : AtkStateMar!"));
				return;
			}
			AtkStateMar->SwitchFlyOrbitMode(false, TEXT(""));
			return;
		}

		if (index == (FlyPoints.Num() - 1))
		{
			if (IsValid(AtkStateMar))
			{
				AtkStateMar->SwitchFlyOrbitMode(false, TEXT(""));
			}
		}
		else
		{
			FVector	NextPoint = FlyPoints[index + 1];
			PlayerController->FlyToLocation(NextPoint, true, false, FTraceCallback::CreateLambda([this, PatrolID, NextPoint](bool IsSuccess)
			{
				this->CheckMultPatrolFlyToHZMGSpace(PatrolID,NextPoint, IsSuccess);
			}));
		}
	}
	else
	{
		UAtkStateMar* AtkStateMar = PlayerController->GetAtkStateMar();
		if (!IsValid(AtkStateMar))
		{
			StopFlyPatrol();
			CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::CheckMultPatrolFlyToSubSpace : AtkStateMar!"));
			return;
		}
		AtkStateMar->SwitchFlyOrbitMode(false, TEXT(""));		
	}
}

void UFlyPatrolComponent::DisRideOnCarrierToHZMGFly(FFLYSUBSPACE_DATA flySubSpaceData)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::EnterFlyToSubSpace : PlayerCharacter!"));
		return;
	}
	//bIsDisRideOnCarrier这个判断是因为在下载具后，还需要加载单独的人物外观需要时间
	if (PlayerCharacter->IsCarrierState() || PlayerCharacter->IsDisCarrierState())
	{
		URolePetInterface * Interface = Cast<URolePetInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePetInterface"), 0));

		if (IsValid(Interface))
		{
			Interface->RequestTransformPetFC();
		}
		FlyPatrolState = FLYPATORLSTATE_TYPE::HZMGDisRide;
		TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr(this);
		PlayerCharacter->OnDisRideOnPetOver = FDisRideOnPetOverDelegate::CreateLambda([DelayThisPtr, flySubSpaceData]()
		{
			CS3_Warning(TEXT("APlayerCharacter::OnBroadCreateModelOver"));
			if (DelayThisPtr.IsValid())
			{
				UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
				ThisPtr->StartFlyToHZMGSpace(flySubSpaceData);
			}
		});
	}
	else
	{
		StartFlyToHZMGSpace(flySubSpaceData);
	}
}

void UFlyPatrolComponent::onNotifyAddEffectList(FString FlyPatrolID, TArray<int32> EffectList)
{
	USkillInterface * SkillInterface = Cast<USkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("SkillInterface"), 0));
	if (IsValid(SkillInterface) && EffectList.Num() > 0)
	{
		SkillInterface->RPC_AddFlyPatrolEffectList(FlyPatrolID, EffectList);
	}
}

void UFlyPatrolComponent::onNotifyRemoveEffectList(FString FlyPatrolID)
{
	USkillInterface * SkillInterface = Cast<USkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("SkillInterface"), 0));
	if (IsValid(SkillInterface))
	{
		SkillInterface->RPC_RemoveFlyPatrolEffectList(FlyPatrolID);
	}
}

void UFlyPatrolComponent::StartFlyToHZMGSpace(FFLYSUBSPACE_DATA flySubSpaceData)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::StartFlyToSubSpace : PlayerCharacter!"));
		return;
	}

	FlyPatrolState = FLYPATORLSTATE_TYPE::HZMGGETON;
	FlyHZMGSpaceData = flySubSpaceData;
	CurFlyPatrolID = TEXT("");
	FTimerHandle DelayHandle;
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, this, &UFlyPatrolComponent::BindHZMGCharacterToFlyAttach, 0.5f, false);
	}
	PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
	FName ActionId = "Show_FloatGeton";
	FActionOverDelegate Delegate;
	Delegate.AddUObject(this, &UFlyPatrolComponent::PlayFlyPatrolActionOverInHZMGSpace);
	PlayerCharacter->PlayAction(ActionId, 0.0f, Delegate);
}

void UFlyPatrolComponent::BindHZMGCharacterToFlyAttach()
{
	SCOPE_CYCLE_COUNTER(STAT_BindCharacterToFlyAttach);
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::BindCharacterToFlyAttach : PlayerCharacter!"));
		return;
	}
	UClass* BP_FlyAttachActorClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_HZMGFlyActor"));
	FVector Location = PlayerCharacter->GetActorTransform().GetLocation();
	FRotator Ratation = FRotator(PlayerCharacter->GetActorTransform().GetRotation());
	FActorSpawnParameters SpawnParameters;
	SpawnParameters.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	HZMGFlyAttachActor = (GetWorld())->SpawnActor(BP_FlyAttachActorClass, &Location, &Ratation, SpawnParameters);
	HZMGFlyAttachActor->SetActorLocationAndRotation(PlayerCharacter->GetActorLocation() + FVector(0.0f, 0.0f, -25.0f), PlayerCharacter->GetActorRotation() + FRotator(0.0f, -90.0f, 0.0f));

	///<生成队员的模型
	HZMGTeamMembsModle.Reset();
	URoleTeamInterface * RoleTeamInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.RoleTeamInterface : nullptr;
	if (IsValid(RoleTeamInterface))
	{
		TArray<FTeamMemberData> Members = RoleTeamInterface->Members;
		if (Members.Num() > 0)
		{
			HZMGFlyAttachActor->SetActorScale3D(FVector(2.0f, 2.0f, 2.0f));
			for (int i = 0; i < Members.Num(); i++)
			{
				///<等于玩家自己
				if (Members[i].EntityID == PlayerCharacter->EntityId || Members[i].EntityID == 0 || Members[i].OnLineState == 0)
				{
					continue;
				}
				KBEngine::Entity* entity = UGolbalBPFunctionLibrary::FindEntity(Members[i].EntityID);	
				
				if (entity!=nullptr)
				{
					CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------APlayerCharacter::BindCharacterToFlyAttach TeamMember-----------%d"), entity->ID());
					APlayerCharacter* player = Cast<APlayerCharacter>(entity->Actor());
					UClass* ActorClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Character"));
					if (!ActorClass)
					{
						CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::BindCharacterToFlyAttach : ActorClass!"));
						return;
					}
					TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr(this);
					TWeakObjectPtr<APlayerCharacter> DelayPlayerPtr(player);
					UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(PlayerCharacter, FStringAssetReference(ActorClass),
						FStreamableDelegate::CreateLambda([DelayThisPtr, DelayPlayerPtr, ActorClass]()
					{
						if (!DelayThisPtr.IsValid() || !DelayPlayerPtr.IsValid() || !ActorClass || !DelayPlayerPtr.Get()->GetSelfEntity())
						{
							CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------APlayerCharacter::BindCharacterToFlyAttach Role RequestAsyncLoad-----callback-----------"));
							return;
						}
						UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
						APlayerCharacter* PlayerPtr = DelayPlayerPtr.Get();
						URoleTeamInterface * RoleTeamInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.RoleTeamInterface : nullptr;
						if (!IsValid(RoleTeamInterface))
						{
							CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::BindCharacterToFlyAttach : RoleTeamInterface!"));
							return;
						}

						if (ActorClass)
						{
							int index = RoleTeamInterface->GetMemberIndexOnFaBaoByEntityID(PlayerPtr->GetSelfEntity()->ID());
							APlayerCharacter* OtherRole = UGolbalBPFunctionLibrary::SpawnActor<APlayerCharacter>(ActorClass);
							ThisPtr->HZMGTeamMembsModle.Add(OtherRole);
							OtherRole->AppearanceComponent->CopyCharacterFromClientAppearance(PlayerPtr);
							OtherRole->AttachToComponent(ThisPtr->HZMGFlyAttachActor->GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform, TEXT("Socket_Root"));
							OtherRole->SetActorRelativeRotation(FRotator(0, 90.0f, 0));
							if (index == 0)
							{
								OtherRole->SetActorRelativeLocation(FVector(0, 100.0f, 65.0f));
							}
							else if (index == 1)
							{
								OtherRole->SetActorRelativeLocation(FVector(0, 40.0f, 65.0f));
							}
							else  if (index == 2)
							{
								OtherRole->SetActorRelativeLocation(FVector(0, -50.0f, 65.0f));
							}
							else
							{
								OtherRole->SetActorRelativeLocation(FVector(0, -80.0f*(index - 2) - 50.0f, 65.0f));
							}
							OtherRole->SetActorRelativeScale3D(FVector(0.5f, 0.5f, 0.5f));
							TWeakObjectPtr<APlayerCharacter> DelayOtherRolePtr(OtherRole);
							OtherRole->OnBroadCreateModelOver.BindLambda([DelayPlayerPtr, DelayOtherRolePtr]()
							{
								if (DelayPlayerPtr.IsValid() && DelayOtherRolePtr.IsValid())
								{
									APlayerCharacter* PlayerPtr = DelayPlayerPtr.Get();
									APlayerCharacter* OtherRolePtr = DelayOtherRolePtr.Get();
									if (PlayerPtr->GetSelfEntity() != nullptr)
									{
										OtherRolePtr->OnChangeHeadInfosByOtherOwner(PlayerPtr);
									}
									FName ActionId = "Show_FloatRun";
									OtherRolePtr->PlayAction(ActionId, 0.0f);
									UGolbalBPFunctionLibrary::SetActorAndCompVisibility(OtherRolePtr, UPrimitiveComponent::StaticClass(), true, true);
									OtherRolePtr->OnBroadCreateModelOver.Unbind();
								}
							});
							UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(PlayerPtr);
						}
					}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER, GetOwner()->GetActorLocation());
				}
			}
		}
	}
}

void UFlyPatrolComponent::GetHZMGNearestFlyPoint(const FString& PatrolID, const int32 sPoint, FVector& Point)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::GetNearestFlyPoint : PlayerCharacter!"));
		return;
	}
	const FFLY_PATROL_DATA* FlyPatrolData = GetFlyPatrolData(PatrolID);

	if (FlyPatrolData != nullptr&&sPoint > -1)
	{
		FVector Location = PlayerCharacter->GetActorTransform().GetLocation();
		int32 shortIndex = 0;
		float shortDist = FVector::Dist(FlyPatrolData->FlyPoints[0], Location);
		for (auto IT = FlyPatrolData->FlyEventIDs.CreateConstIterator(); IT; IT++)
		{
			int32 Index = IT.GetIndex();
			if ((FlyPatrolData->FlyEventIDs[Index].FlyIndex) == sPoint)
			{
				Point = FlyPatrolData->FlyPoints[Index];
				return;
			}
		}
	}
}

void UFlyPatrolComponent::CheckSinglePatrolFlyToHZMGSpace(const FString fPatrolID, const FVector Point, int32 sPoint, const int32 tPoint, FVector enterPos, bool IsSuccess)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckSinglePatrolFlyToSubSpace);
	const FFLY_PATROL_DATA* FlyPatrolData = GetFlyPatrolData(fPatrolID);

	if (nullptr != FlyPatrolData && IsSuccess)
	{
		///<CST-4479 在初始位置点（下标为0）
		if (sPoint == tPoint&&tPoint == 0)
		{
			AActor* OwnerActor = GetOwner();
			APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(OwnerActor);
			if (!IsValid(PlayerCharacter))
			{
				CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::CheckSinglePatrolFlyToSubSpace : PlayerCharacter!"));
				return;
			}
			PlayerCharacter->StopPlayerMove();
			KBEngine::Entity* SelfEntity = PlayerCharacter->GetSelfEntity();
			if (SelfEntity != nullptr)
			{
				URoleSpaceContentInterface* interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"), PlayerCharacter->GetSelfEntity()->ID()));
				interface->RPC_onMagicMazeNodeFly();
			}
			return;
		}

		TArray<FVector> FlyPoints = FlyPatrolData->FlyPoints;
		int32 index = FlyPoints.Find(Point);
		if (index < 0)
		{
			CS3_Warning(TEXT("APlayerCharacter::CheckFlyToSubSpace --- Can't Find Point!"));
			return;
		}
		if (FlyPatrolData->FlyEventIDs.Num() > index)
		{
			FFLYEVENT_DATA EventID = FlyPatrolData->FlyEventIDs[index];
			// 移动到目标点
			if (EventID.FlyIndex == tPoint)
			{
				ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
				if (IsValid(PlayerController))
				{
					PlayerController->FlyToLocation(enterPos, true, false, FTraceCallback::CreateLambda([this, fPatrolID](bool IsSuccess)
					{
						this->OnEndFlyToHZMGSpace(fPatrolID);
					}));
				}
				return;
			}
		}

		if (tPoint > sPoint)
		{
			index += 1;
		}
		else
		{
			index -= 1;
		}
		if (FlyPatrolData->FlyPoints.Num() - 1 >= index)
		{
			FVector movePoint = FlyPatrolData->FlyPoints[index];

			ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
			if (IsValid(PlayerController))
			{
				PlayerController->FlyToLocation(movePoint, true, false, FTraceCallback::CreateLambda([this, fPatrolID, movePoint, sPoint, tPoint, enterPos](bool IsSuccess)
				{
					this->CheckSinglePatrolFlyToHZMGSpace(fPatrolID, movePoint, sPoint, tPoint, enterPos, IsSuccess);
				}));
			}
		}
	}
}

void UFlyPatrolComponent::OnEndFlyToHZMGSpace(const FString FlyID)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::OnEndFlyToSubSpace : PlayerCharacter!"));
		return;
	}
	PlayerCharacter->StopPlayerMove();
	KBEngine::FVariantArray args;
	KBEngine::Entity* SelfEntity = PlayerCharacter->GetSelfEntity();
	
	if (SelfEntity != nullptr)
	{
		URoleSpaceContentInterface* SCInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"), SelfEntity->ID()));
		if (IsValid(SCInterface))
		{
			SCInterface->RPC_onMagicMazeEndFly();
		}
	}
}

void UFlyPatrolComponent::PlayFlyPatrolActionOverInHZMGSpace(ACharacter* Character, FACTION_DATA ActionData)
{
	SCOPE_CYCLE_COUNTER(STAT_PlayFlyPatrolActionOverInSubSpace);
	if (!FlyHZMGSpaceData.PatrolID.Equals(TEXT("")))
	{
		///<生成队员的模型
		URoleTeamInterface * RoleTeamInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.RoleTeamInterface : nullptr;
		if (IsValid(RoleTeamInterface))
		{
			AActor* OwnerActor = GetOwner();
			APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(OwnerActor);
			if (!IsValid(PlayerCharacter))
			{
				CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::PlayFlyPatrolActionOverInSubSpace : PlayerCharacter!"));
				return;
			}
			TArray<FTeamMemberData> Members = RoleTeamInterface->Members;
			if (Members.Num() > 0)
			{
				for (int i = 0; i < Members.Num(); i++)
				{
					KBEngine::Entity* entity = UGolbalBPFunctionLibrary::FindEntity(Members[i].EntityID);
					///<等于玩家自己
					if (Members[i].EntityID == PlayerCharacter->EntityId)
					{						
						if (IsValid(PlayerCharacter->ChildActor) && IsValid(HZMGFlyAttachActor))
						{
							int index = RoleTeamInterface->GetMemberIndexOnFaBaoByEntityID(PlayerCharacter->EntityId);
							HZMGFlyAttachActor->AttachToComponent(PlayerCharacter->ChildActor, FAttachmentTransformRules::KeepRelativeTransform);
							HZMGFlyAttachActor->SetActorRotation(PlayerCharacter->ChildActor->K2_GetComponentRotation() + FRotator(0.0f, 0.0f, 0.0f));
							HZMGFlyAttachActor->SetActorRelativeLocation(FVector(0, -160.0f + (140 * index), 20.0f));
						}
						///<目前没有资源临时处理方案
						PlayerCharacter->SetActorLocation(PlayerCharacter->GetActorLocation() + FVector(0.0f, 0.0f, 79.0f));

						break;
					}
				}
			}
			else
			{			
				if (IsValid(PlayerCharacter->ChildActor) && IsValid(HZMGFlyAttachActor))
				{
					HZMGFlyAttachActor->AttachToComponent(PlayerCharacter->ChildActor, FAttachmentTransformRules::KeepRelativeTransform);
					HZMGFlyAttachActor->SetActorRotation(PlayerCharacter->ChildActor->K2_GetComponentRotation() + FRotator(0.0f, -8.0f, 0.0f));
					HZMGFlyAttachActor->SetActorRelativeLocation(FVector(0, 20, 20));
				}
				///<目前没有资源临时处理方案
				PlayerCharacter->SetActorLocation(PlayerCharacter->GetActorLocation() + FVector(0.0f, 0.0f, 79.0f));
			}
		}
	}
	SwitchFlyOrbitMode();
}

void UFlyPatrolComponent::DestroyHZMGSpaceOfFlyAttachActor()
{
	SCOPE_CYCLE_COUNTER(STAT_DestroySubSpaceOfFlyAttachActor);
	DestroyFlyAttachActor();
	///<显示队员的模型
	URoleTeamInterface * RoleTeamInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.RoleTeamInterface : nullptr;
	if (IsValid(RoleTeamInterface))
	{
		AActor* OwnerActor = GetOwner();
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(OwnerActor);
		if (!IsValid(PlayerCharacter))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UFlyPatrolComponent::DestroySubSpaceOfFlyAttachActor : PlayerCharacter!"));
			return;
		}
		TArray<FTeamMemberData> Members = RoleTeamInterface->Members;
		if (Members.Num() > 0)
		{
			for (int i = 0; i < Members.Num(); i++)
			{
				KBEngine::Entity* entity = UGolbalBPFunctionLibrary::FindEntity(Members[i].EntityID);
				///<等于玩家自己
				if (Members[i].EntityID == PlayerCharacter->EntityId)
				{
					continue;
				}
				if (entity)
				{
					APlayerCharacter* player = Cast<APlayerCharacter>(entity->Actor());
					if (IsValid(player))
					{
						UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(player);									
					}					
				}
			}
		}
	}
}

void UFlyPatrolComponent::OnUpdateFlyCharacterVisibility(bool bIsVisibility /*= true*/)
{
	if (IsValid(FlyCharacter))
	{
		UGolbalBPFunctionLibrary::SetActorAndCompVisibility(FlyCharacter, UPrimitiveComponent::StaticClass(), bIsVisibility, bIsVisibility);
	}
}

bool UFlyPatrolComponent::IsNormalFlyPatrolState()
{
	return (FlyPatrolState == FLYPATORLSTATE_TYPE::DisRide || FlyPatrolState == FLYPATORLSTATE_TYPE::GETON || FlyPatrolState == FLYPATORLSTATE_TYPE::RIDEONCARRIER || FlyPatrolState == FLYPATORLSTATE_TYPE::FLYING) ? true : false;
}

void UFlyPatrolComponent::StartYCJMDSkyFly(const FString& FlyPathId)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		return;
	}
	const FFLY_PATROL_DATA* data = GetFlyPatrolData(FlyPathId);
	if (data == nullptr)return;

	YCJMDSkyFlyData = *(data);
	if (YCJMDSkyFlyData.FlyPoints.Num() > 0)
	{
		PlayerCharacter->SetActorLocation(YCJMDSkyFlyData.FlyPoints[0]);
		FRotator FindRotator = UKismetMathLibrary::FindLookAtRotation(PlayerCharacter->GetActorLocation(), YCJMDSkyFlyData.FlyPoints[1]);
		PlayerCharacter->SetActorRotation(FindRotator);
		SkyCarrrierRotator = PlayerCharacter->GetActorRotation();//做翻滚效果
		SkyCarrrierRollRotator = SkyCarrrierRotator;//赋值是为了CheckSkyCarrierMoveEffect时Equals能通过
		CheckYCJMDSkyFlyPoint();

		UGolbalBPFunctionLibrary::AudioManager()->PlayVoice(Parachute_WindVoiceID);
		UGolbalBPFunctionLibrary::AudioManager()->SetSingleVoiceVol(2.f);
		UGolbalBPFunctionLibrary::AudioManager()->StopSceneMusic(true);				// 降低背景音乐
		UGolbalBPFunctionLibrary::AudioManager()->StopEnvironmentSound();
		UGolbalBPFunctionLibrary::ParticleManager()->PlayParticle(Parachute_RCarrierParticleID, 0.0f, PlayerCharacter, PlayerCharacter);
		UGolbalBPFunctionLibrary::ParticleManager()->PlayParticle(Parachute_LCarrierParticleID, 0.0f, PlayerCharacter, PlayerCharacter);

		URoleSpaceContentInterface* SCInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URoleSpaceContentInterface::GetName()));
		if (IsValid(SCInterface))
		{
			SCInterface->OnYCJMSkyFly();
		}

		TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr = this;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, SkyCarrierAnimHandle,
			FTimerDelegate::CreateLambda([DelayThisPtr]()
				{
					if (!DelayThisPtr.IsValid())
					{
						return;
					}
					UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
					ThisPtr->CheckPlayRollAction();
				}), 10.0f, true);
	}
}

void UFlyPatrolComponent::CheckYCJMDSkyFlyPoint()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		return;
	}

	if (YCJMDSkyFlyData.FlyPoints.Num() > 1)
	{
		auto index = YCJMDSkyFlyData.FlySpeeds.Num() - YCJMDSkyFlyData.FlyPoints.Num();
		if (index >= 0)
		{
			PlayerCharacter->GetCharacterMovement()->MaxFlySpeed = YCJMDSkyFlyData.FlySpeeds[index];
		}
		YCJMDSkyFlyData.FlyPoints.RemoveAt(0);
		FVector NextPoint = YCJMDSkyFlyData.FlyPoints[0];
		// 增加 偏移的随机值
		SprintArmScoOffset.X = FMath::Clamp(NextPoint.X - PlayerCharacter->GetActorLocation().X, -300.f, 0.f);
		SprintArmScoOffset.Y = FMath::Clamp(NextPoint.Y - PlayerCharacter->GetActorLocation().Y, -100.f, 300.f);
		SprintArmScoOffset.Z = FMath::Clamp(NextPoint.Z - PlayerCharacter->GetActorLocation().Z, -300.f, 0.f);
		SkyCarrrierRollRotator = UKismetMathLibrary::FindLookAtRotation(PlayerCharacter->GetActorLocation(), NextPoint);
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		PlayerController->FlyToLocation(NextPoint, true, true, FTraceCallback::CreateLambda([this, NextPoint](bool IsSuccess)
			{
				this->CheckYCJMDSkyFlyPoint();
			}));
	}
	else
	{
		LeaveSkyCarrierKeyF();
	}
}

void UFlyPatrolComponent::CheckSkyCarrierMoveEffect(float DeltaTime)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter) || !PlayerCharacter->IsParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_CARRIER) || bIsPlayRollAction)
	{
		return;
	}

	FRotator PlayerRotation = PlayerCharacter->GetActorRotation();
	float RinterrpSpeed = UKismetMathLibrary::RandomFloatInRange(2.0f, 4.0f);

	if (PlayerRotation.Equals(SkyCarrrierRollRotator, 5.0f))
	{
		float RollAngle = SkyCarrrierRotator.Roll + UKismetMathLibrary::RandomFloatInRange(25, 50.0f);//翻滚的随机范围
		RollDir *= -1.0f;
		SkyCarrrierRollRotator = SkyCarrrierRotator;
		SkyCarrrierRollRotator.Roll = RollAngle * RollDir;
	}
	PlayerCharacter->SetActorRotation(FMath::RInterpTo(PlayerRotation, SkyCarrrierRollRotator, DeltaTime, RinterrpSpeed));

	if (PlayerCharacter->SpringArmCompent->SocketOffset.Equals(SprintArmScoOffset))
	{
		SprintArmScoOffset = FVector(-300.f, 0.f, 0.f);
	}
	PlayerCharacter->SpringArmCompent->SocketOffset = FMath::VInterpTo(PlayerCharacter->SpringArmCompent->SocketOffset, SprintArmScoOffset, DeltaTime, RinterrpSpeed);
}

void UFlyPatrolComponent::CheckAutoOpenYCJMDParachute(float DeltaTime)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter) || !PlayerCharacter->IsJumpParachuteState())
	{
		return;
	}
	if (PlayerCharacter->IsParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_FALL))					// 还没开伞
	{
		FVector PlayerLocation = PlayerCharacter->GetActorLocation();
		// 地图的水平面高度是-300米，在距离水平面340米的时候开伞
		if (PlayerLocation.Z + 30000.f <= 34000.f)
		{
			OpenYCJMDParachuteKeyF();
		}
	}
	if (PlayerCharacter->IsParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_OPEN) && !bIsPlayReadyLandAction)				// 已经开伞
	{
		if (IsValid(GetWorld()))
		{
			FHitResult HitOut(ForceInit);
			static FName TraceTag = FName(TEXT("YCJMDSkyToFloorDist"));
			FCollisionQueryParams TraceParams = FCollisionQueryParams(TraceTag, false, PlayerCharacter);
			FVector AcharacterLoction = PlayerCharacter->GetActorLocation();
			if (GetWorld()->LineTraceSingleByChannel(HitOut, AcharacterLoction,
				AcharacterLoction + FVector(0.0f, 0.0f, -1000.0f), ECC_GameTraceChannel10, TraceParams))
			{
				if (HitOut.Distance >= 500)
				{
					PlayerCharacter->PlayAction(Parachute_ReadyLandActionID);
				}
				bIsPlayReadyLandAction = true;
				
			}
		}
	}
	if (PlayerCharacter->IsSkyParachuteState())
	{
		float Speed = (LastPlayerPosZ - PlayerCharacter->GetActorLocation().Z) / DeltaTime * 0.036;
		LastPlayerPosZ = PlayerCharacter->GetActorLocation().Z;

		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnUpdateYCJMDSpeed.Broadcast(Speed);
		}
	}
}

void UFlyPatrolComponent::CheckPlayRollAction()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter) || !PlayerCharacter->IsParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_CARRIER))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(SkyCarrierAnimHandle);
		return;
	}
	bIsPlayRollAction = true;
	FActionOverDelegate SkyCarrierActionOverDelegate;
	SkyCarrierActionOverDelegate.AddUObject(this, &UFlyPatrolComponent::OnSkyCairrerRollActionOver);
	FName ActionName = UKismetMathLibrary::RandomIntegerInRange(1, 10) > 5 ? "Show_01" : "Show_02";
	PlayerCharacter->PlayAction(ActionName, 0.0f, SkyCarrierActionOverDelegate);
}

void UFlyPatrolComponent::OnSkyCairrerRollActionOver(ACharacter* Character, FACTION_DATA ActionData)
{
	bIsPlayRollAction = false;
}

void UFlyPatrolComponent::LeaveSkyCarrierKeyF()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	ACS3PlayerController* PlayerControl = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerCharacter) || !IsValid(PlayerControl))
	{
		return;
	}
	PlayerCharacter->SetBrakingDecelerationFalling(0.0f);
	URoleSpaceContentInterface* SCInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URoleSpaceContentInterface::GetName()));
	if (IsValid(SCInterface))
	{
		SCInterface->ChangeParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_FALL);
		SCInterface->OnShowYCJMDUI();
	}

	PlayerCharacter->StopPlayerMove();
	PlayerCharacter->RideCarrierComponent->ClearRideOnCarrier();
	uint8 gender = (uint8)PlayerCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("gender")).GetValue<int32>();
	if (Parachute_SexActionTable.Contains(gender))
	{
		PlayerCharacter->GetAppearanceComponent()->CreateAppearance(Parachute_SexActionTable[gender]);
	}
	PlayerCharacter->BindMesh(Parachute_BagID);//绑定降落伞背包
	
	

	PlayerCharacter->SetActorRotation(FRotator(0.0f, PlayerControl->GetControlRotation().Yaw, 0.0f));//还原角色角度
	PlayerControl->RotationInput.Pitch = -30.f;
	UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerCharacter->SpringArmCompent, 900.0f);
	UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerCharacter->SpringArmCompent, FVector(-300.0f, 0.0f, 0.0f));

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::YcjmdParachute, CC_MODE_REASON::CCM_YJP_CONTROLLER_MODE);
	OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_YCJMD_PARACHUTE);

	/*//载具大鸟模型换成跳伞的玩家
	UGameObjectInterface* GameObjectInterface = Cast<UGameObjectInterface>(
		UGolbalBPFunctionLibrary::GetInterfaceByName(UGameObjectInterface::GetName()));
	if (IsValid(GameObjectInterface))
	{
		//FString ActionId = "";
		//GameObjectInterface->CLIENT_ChangeShowAnimAndActionPosture(ModelId, ActionId, ActionId);

		
	}*/

	UGolbalBPFunctionLibrary::AudioManager()->SetSingleVoiceVol(4.0f);
	UGolbalBPFunctionLibrary::ParticleManager()->PlayParticle(Parachute_YunParticleID, 0.0f, PlayerCharacter, PlayerCharacter);
	UGolbalBPFunctionLibrary::ParticleManager()->StopEffectByID(Parachute_RCarrierParticleID);
	UGolbalBPFunctionLibrary::ParticleManager()->StopEffectByID(Parachute_LCarrierParticleID);
}

void UFlyPatrolComponent::OpenYCJMDParachuteKeyF()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter) || IsValid(ParachuteCharacter))
	{
		return;
	}
	URoleSpaceContentInterface* SCInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URoleSpaceContentInterface::GetName()));
	if (IsValid(SCInterface))
	{
		SCInterface->ChangeParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_OPEN);
		SCInterface->OnOpenParachute();
	}
	CreateParachuteInst();
	
	UGolbalBPFunctionLibrary::AudioManager()->SetSingleVoiceVol(2.f);
	FCClientVoiceComplete ClientVoiceCreate;
	UGolbalBPFunctionLibrary::AudioManager()->ClientVoicePlay(Parachute_OpenVoiceID, ClientVoiceCreate);
	UGolbalBPFunctionLibrary::ParticleManager()->StopEffectByID(Parachute_YunParticleID);

	TWeakObjectPtr<UFlyPatrolComponent> DelayThisPtr = this;
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, OpenParachuteHandle,
		FTimerDelegate::CreateLambda([DelayThisPtr]()
	{
		if (!DelayThisPtr.IsValid())
		{
			return;
		}
		UFlyPatrolComponent* ThisPtr = DelayThisPtr.Get();
		ThisPtr->OpenParachuteSlowSpeed();
	}), 0.05f, true);
}

void UFlyPatrolComponent::CreateParachuteInst()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter) || IsValid(ParachuteCharacter))
	{
		return;
	}
	PlayerCharacter->PlayAction(Parachute_OpenActionID);
	//创建绑定降落伞对象
	UClass* ParachuteClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Parachute"));
	ParachuteCharacter = UGolbalBPFunctionLibrary::SpawnActor<AClientGameCharacter>(ParachuteClass);
	if (IsValid(ParachuteCharacter))
	{
		//ParachuteCharacter->GetAppearanceComponent()->CreateAppearance("SK_ZW0446_Parachute");
		ParachuteCharacter->AttachToComponent(PlayerCharacter->GetMesh(), FAttachmentTransformRules::SnapToTargetNotIncludingScale, TEXT("Socket_Parachute"));
		ParachuteCharacter->SetActorRelativeLocation(FVector(0.0, 30.0, -220.0f));	
	}
}


void UFlyPatrolComponent::OpenParachuteSlowSpeed()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		return;
	}
	if (PlayerCharacter->GetCharacterMovement()->Velocity.Z >= -800.f)
	{
		UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();				// 需要做 打开降落伞，速度减慢的过程。所以把这个模式放这里
		OperationModeMgr->ChangeMode(EATTACT_STATE::BEHAVIOR_YCJMD_PARACHUTE_OPEN);
		

		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(OpenParachuteHandle);
		return;
	}
	PlayerCharacter->GetCharacterMovement()->Velocity.Z += 40.f;
}

void UFlyPatrolComponent::LandYCJMDParachute()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());				// 本地玩家和其他玩家都会走这里
	if (!IsValid(PlayerCharacter) || !IsValid(ParachuteCharacter))
	{
		return;
	}
	
	PlayerCharacter->UnBindMesh(Parachute_BagID);//取消绑定降落伞背包
	ParachuteCharacter->DetachFromActor(FDetachmentTransformRules::KeepWorldTransform);
	ParachuteCharacter->OnDoingCustomEvent(0);
	ParachuteCharacter = nullptr;
	
}

void UFlyPatrolComponent::LandYCJMDSkyDiving()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		return;
	}
	UGolbalBPFunctionLibrary::AudioManager()->StopVoice();
	UGolbalBPFunctionLibrary::AudioManager()->LoopPlaySceneMusicByPlayerState(true, true, false);
	UGolbalBPFunctionLibrary::AudioManager()->PlayEnvironmentSound();
	FRotator CurActorRotation = PlayerCharacter->GetActorRotation();
	PlayerCharacter->SetActorRotation(FRotator(0.0f, CurActorRotation.Yaw, 0.0f));//还原角色角度

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	ControllerModeMgr->RecoveryMode();
	OperationModeMgr->RecoveryMode();
	
	


	//玩家播放跳伞着陆动作
	bIsPlayReadyLandAction = true;
	FActionOverDelegate PlayerActionOverDelegate;
	PlayerActionOverDelegate.AddUObject(this, &UFlyPatrolComponent::OnPlayerLandActionOver);
	PlayerCharacter->PlayAction(Parachute_LandActionID, 0.0f, PlayerActionOverDelegate);
	FVector PlayerVector = UKismetMathLibrary::Normal(PlayerCharacter->GetActorForwardVector());			// 添加一个向前的惯性
	PlayerCharacter->GetCharacterMovement()->Velocity.X = PlayerVector.X * 1500.f;
	PlayerCharacter->GetCharacterMovement()->Velocity.Y = PlayerVector.Y * 1500.f;

	URoleSpaceContentInterface* SCInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(URoleSpaceContentInterface::GetName()));
	if (IsValid(SCInterface))
	{

	  SCInterface->ChangeParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_NORMAL);
	  SCInterface->OnHideYCJMDUI();
	  SCInterface->SetIsEnabledQuickBar(false);
	}
}

void UFlyPatrolComponent::OnPlayerLandActionOver(ACharacter* Character, FACTION_DATA ActionData)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerCharacter))
	{
		PlayerCharacter->CreateAppearance();
		
	}
}

CONTROL_COMPILE_OPTIMIZE_END





