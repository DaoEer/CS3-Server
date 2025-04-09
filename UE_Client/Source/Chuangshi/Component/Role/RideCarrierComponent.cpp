// Fill out your copyright notice in the Description page of Project Settings.

#include "RideCarrierComponent.h"
//UE4
#include "TimerManager.h"
#include "Particles/ParticleSystem.h"
//CS3数据
#include "GameData/PetData.h"
#include "GameData/EffectEmitterData.h"
//CS3
#include "Actor/Player/PlayerCharacter.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Actor/Pet/RiderCharacter.h"
#include "Actor/Action/RoleAnimInstance.h"
#include "Actor/Action/RiderAnimInstance.h"
#include "Manager/ParticleManager.h"
#include "Manager/CharacterRideManager.h"
#include "Manager/CustomTimerManager.h"
#include "Util/CS3Debug.h"
#include "JumpComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "FlyPatrolComponent.h"
#include "Manager/CfgManager.h"
#include "Util/ConvertUtil.h"

#include "Util/ConvertUtil.h"
#include "GameData/CharacterData.h"
#include "Actor/Action/BaseAnimInstance.h"
#include "Components/ChildActorComponent.h"
#include "Components/SceneComponent.h"

DECLARE_CYCLE_STAT(TEXT("RideOnPet"), STAT_RideOnPet, STATGROUP_URideCarrierComponent);
DECLARE_CYCLE_STAT(TEXT("DisRideOnPet"), STAT_DisRideOnPet, STATGROUP_URideCarrierComponent);
DECLARE_CYCLE_STAT(TEXT("RideOnCarrier"), STAT_RideOnCarrier, STATGROUP_URideCarrierComponent);
DECLARE_CYCLE_STAT(TEXT("DisRideOnCarrier"), STAT_DisRideOnCarrier, STATGROUP_URideCarrierComponent);
DECLARE_CYCLE_STAT(TEXT("StartRideGetOnAction"), STAT_StartRideGetOnAction, STATGROUP_URideCarrierComponent);
DECLARE_CYCLE_STAT(TEXT("CreateRiderActorComponent"), STAT_CreateRiderActorComponent, STATGROUP_URideCarrierComponent);
DECLARE_CYCLE_STAT(TEXT("DestroyRiderComponent"), STAT_DestroyRiderComponent, STATGROUP_URideCarrierComponent);
DECLARE_CYCLE_STAT(TEXT("PlayRideEffect"), STAT_PlayRideEffect, STATGROUP_URideCarrierComponent);
DECLARE_CYCLE_STAT(TEXT("RideGetOnActionOver"), STAT_RideGetOnActionOver, STATGROUP_URideCarrierComponent);
DECLARE_CYCLE_STAT(TEXT("RideGetOffActionOver"), STAT_RideGetOffActionOver, STATGROUP_URideCarrierComponent);

CONTROL_COMPILE_OPTIMIZE_START
URideCarrierComponent::URideCarrierComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	RiderActorComponent = nullptr;
	bIsDisRideOnCarrier = false;
	CarrierId = "";
}

void URideCarrierComponent::BeginPlay()
{
	Super::BeginPlay();
}

void URideCarrierComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	//更新移动时的速度与方向(绑定播放骑士动作)
	if (CurActionData.ActionType == ACTION_TYPE_ENUM::ACTION_TYPE_MOVE)
	{
		APlayerCharacter* RidePetCharacter = Cast<APlayerCharacter>(GetOwner());
		URiderAnimInstance *RiderAnimInstance = GetRiderAnimInstance();
		if (!IsValid(RidePetCharacter) || !IsValid(RiderAnimInstance))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URideCarrierComponent::TickComponent : RidePetAnimInstance||RiderAnimInstance!"));
			return;
		}

		float MoveSpeed = RidePetCharacter->GetMoveSpeed();
		float MoveDirction = RidePetCharacter->GetMoveDirection();
		RiderAnimInstance->SetMoveSpeedAndMoveDirection(MoveSpeed, MoveDirction);
	}
}

void URideCarrierComponent::Destroy()
{
	ClearTimer(RiderGetOnFrameTimerHle);
	ClearTimer(RiderGetOnTimerHle);
	ClearTimer(RiderGetOffTimerHle);
	DestroyRiderComponent();
}

void URideCarrierComponent::RideOnPet(FString RideCarrideId)
{
	SCOPE_CYCLE_COUNTER(STAT_RideOnPet);
	//载具规则是：上优先于下载具
	if (IsRidePetState()) 
	{
		RideGetOffActionOver(false);
	}

	PlayRideEffect("100084");
	CarrierId = RideCarrideId;
	OnCreateRoleAppearance.Broadcast();

	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->JumpComponent))
	{
		PlayerCharacter->JumpComponent->SetJumpMaxCountBySkill();
	}
}

void URideCarrierComponent::DisRideOnPet()
{
	SCOPE_CYCLE_COUNTER(STAT_DisRideOnPet);
	PlayRideEffect("100084");
	DisRideOnCarrier();
}

bool URideCarrierComponent::IsRidePetState()
{
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter) || !PlayerCharacter->GetSelfEntity())
	{
		return false;
	}
	FString RideCarrierId = (FString)PlayerCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("carrierId"));
	return !RideCarrierId.IsEmpty();
}

void URideCarrierComponent::RideOnCarrier(FString InCarrierId)
{
	SCOPE_CYCLE_COUNTER(STAT_RideOnCarrier);
	//载具规则是：上优先于下载具
	if (IsCarrierState())
	{
		RideGetOffActionOver(false);
	}

	CarrierId = InCarrierId;
	OnCreateRoleAppearance.Broadcast();

	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (PlayerCharacter)
	{
		PlayerCharacter->JumpComponent->PlayerJumpMaxCount = 1;
	}
}

void URideCarrierComponent::DisRideOnCarrier()
{
	SCOPE_CYCLE_COUNTER(STAT_DisRideOnCarrier);
	bIsDisRideOnCarrier = true;
	ClearTimer(RiderGetOnTimerHle);
	ClearTimer(RiderGetOnFrameTimerHle);
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URideCarrierComponent::DisRideOnCarrier : PlayerCharacter!"));
		return;
	}
	PlayerCharacter->JumpComponent->SetJumpMaxCountBySkill();

	FName ActionId = "Carrier_GetOff";
	FACTION_DATA ActionData;
	if (IsValid(GetRiderCharacter()) && IsValid(GetRiderCharacter()->GetBaseAnimInstance()))
	{
		ActionData = GetRiderCharacter()->GetBaseAnimInstance()->GetActionDataById(ActionId);
	}

	if (ActionData.Id.IsNone() || !ActionData.CurAnimSquenceBase)
	{
		RideGetOffActionOver(true);
	}
	else
	{
		if (IsValid(PlayerCharacter->GetBaseAnimInstance()))
		{
			PlayerCharacter->PlayAction(ActionId); 
			FName CurActionId = PlayerCharacter->GetBaseAnimInstance()->GetCurPlayActionData().Id;
			//当没播放成功时
			if (CurActionId.IsEqual(ActionId))
			{
				float ActionTime = ActionData.CurAnimSquenceBase->GetPlayLength();
				TWeakObjectPtr<URideCarrierComponent> DelayThisPtr(this);
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, RiderGetOffTimerHle,
					FTimerDelegate::CreateLambda([DelayThisPtr]()
						{
							if (DelayThisPtr.IsValid())
							{
								URideCarrierComponent* ThisPtr = DelayThisPtr.Get();
								ThisPtr->RideGetOffActionOver(true);
							}
						}), ActionTime, false);
			}
			else
			{
				RideGetOffActionOver(true);
			}
		}
	}
}

void URideCarrierComponent::ClearRideOnCarrier()
{
	bIsDisRideOnCarrier = true;
	ClearTimer(RiderGetOnTimerHle);
	ClearTimer(RiderGetOnFrameTimerHle);
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		return;
	}
	PlayerCharacter->JumpComponent->SetJumpMaxCountBySkill();
	ClearTimer(RiderGetOffTimerHle);
	//ACharacter* riderCharacter = RiderActorComponent->GetChildActor();


	DestroyRiderComponent();
	CarrierId = "";
}

bool URideCarrierComponent::IsCarrierState()
{
	if (IsRidePetState() || !CarrierId.IsEmpty())
	{
		return true;
	}
	return false;
}

bool URideCarrierComponent::IsDisCarrierState()
{
	return bIsDisRideOnCarrier;
}

ARiderCharacter* URideCarrierComponent::GetRiderCharacter()
{
	if (RiderActorComponent)
	{
		return Cast<ARiderCharacter>(RiderActorComponent->GetChildActor());
	}
	return nullptr;
}

void URideCarrierComponent::PlayBindAction(FACTION_DATA ActionData)
{
	URiderAnimInstance *RiderAnimInstance = GetRiderAnimInstance();
	if (!RiderAnimInstance)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URideCarrierComponent::PlayBindAction : RiderAnimInstance!"));
		return;
	}
	RiderAnimInstance->PlayAction(ActionData.Id);
	CurActionData = ActionData;
}

void URideCarrierComponent::StartRideGetOnAction()
{
	SCOPE_CYCLE_COUNTER(STAT_StartRideGetOnAction);
	FName ActionId = "Carrier_GetOn";
	FACTION_DATA ActionData;
	if (IsValid(GetRiderCharacter()->GetBaseAnimInstance()))
	{
		ActionData = GetRiderCharacter()->GetBaseAnimInstance()->GetActionDataById(ActionId);
	}

	if (ActionData.Id.IsNone() || !ActionData.CurAnimSquenceBase)
	{
		RideGetOnActionOver();
	}
	else
	{
		APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
		if (!IsValid(PlayerCharacter))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URideCarrierComponent::StartRideGetOnAction : PlayerCharacter!"));
			return;
		}
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const FCARRIER_DATA *CarrierData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CARRIER)->GetRow<FCARRIER_DATA>(FSTRING_TO_FNAME(CarrierId));
		RiderOffsetX = CarrierData ? CarrierData->RiderOffsetX : RiderOffsetX;

		//设置骑士显示位置（贴地、靠左）,注："Socket_Ride_Proess"插槽暂时不用了，以后若是起跳过程中要咆哮动作会晃动则需要
		FTransform RidePetSocketTransformCt = PlayerCharacter->GetMesh()->GetSocketTransform(TEXT("Socket_Ride"), RTS_Component);
		FVector RidePetSocketLoctionCt = RidePetSocketTransformCt.GetLocation();//取插槽相对root点位置
		SocketRideSapceZ = FMath::Abs(RidePetSocketLoctionCt.Z);///算出骑士出来后偏移多少才能贴地
		FVector RidePetSocketRideLocation = RiderActorComponent->GetRelativeTransform().GetLocation();
		FVector ToRideLocation = RidePetSocketRideLocation - FVector(RiderOffsetX, 0.0f, SocketRideSapceZ);
		RiderActorComponent->SetRelativeLocation(ToRideLocation, true);
		RiderActorComponent->AttachToComponent(PlayerCharacter->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, TEXT("Socket_Ride"));

		//载具播放上马动作
		PlayerCharacter->PlayAction(ActionId);

		//同步计时上马动作播完侦听
		float DelayActionTime = ActionData.CurAnimSquenceBase->GetPlayLength();
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(RiderGetOnTimerHle, this,
			&URideCarrierComponent::RideGetOnActionOver, DelayActionTime, false);

		//以下是上载具位移表现部件
		float InRate = 0.05f;
		//乘以RiderGetOnTimePercent是因为动作到这个百分比的时候就已经坐在马背上了，后面的动作部分缓冲不能算在程序位移中
		float SquenceLength = (DelayActionTime * ActionData.RiderGetOnTimePercent) / InRate;
		TWeakObjectPtr<URideCarrierComponent> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(PlayerCharacter, RiderGetOnFrameTimerHle,
			FTimerDelegate::CreateLambda([DelayThisPtr, SquenceLength]()
		{
			if (DelayThisPtr.IsValid())
			{
				URideCarrierComponent* ThisPtr = DelayThisPtr.Get();
				FVector RiderLocation = ThisPtr->RiderActorComponent->GetRelativeTransform().GetLocation();
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("RiderRider=====(X=%f, y=%f, z=%f)"), RiderLocation.X, RiderLocation.Y, RiderLocation.Z);
				if (RiderLocation.Z >= 0)
				{
					ThisPtr->RiderActorComponent->SetRelativeLocation(FVector(0.0f, 0.0f, 0.0f));
				}
				else
				{
					FVector OffsetVec = FVector(ThisPtr->RiderOffsetX/SquenceLength, 0.0f, ThisPtr->SocketRideSapceZ/SquenceLength);
					ThisPtr->RiderActorComponent->SetRelativeLocation(RiderLocation + OffsetVec);
				}
			}
		}), InRate, true);
	}
}

void URideCarrierComponent::CreateRiderActorComponent()
{
	SCOPE_CYCLE_COUNTER(STAT_CreateRiderActorComponent);
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URideCarrierComponent::CreateRiderActorComponent : PlayerCharacter!"));
		return;
	}

	if (!IsValid(RiderActorComponent))
	{
		RiderActorComponent = NewObject<UChildActorComponent>(this, UChildActorComponent::StaticClass(), TEXT("RiderActorComponent"));
		RiderActorComponent->RegisterComponent();
		RiderActorComponent->SetChildActorClass(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Rider")));
		RiderActorComponent->AttachToComponent(PlayerCharacter->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, TEXT("Socket_Ride"));
		GetRiderCharacter()->ProfessionID = PlayerCharacter->ProfessionID;
	}
}

void URideCarrierComponent::DestroyRiderComponent()
{
	SCOPE_CYCLE_COUNTER(STAT_DestroyRiderComponent);
	if (IsValid(RiderActorComponent))
	{
		//CST-4775
		//因直接删除组件会崩溃,DestroyComponent()删除顺序有问题,导致子组件注销布料模拟的时候取不到父组件的数据导致崩溃,所以先删除子组件
		if (ARiderCharacter* RiderCharacter = Cast<ARiderCharacter>(RiderActorComponent->GetChildActor()))
		{
			TArray<USceneComponent*> AllChildren = RiderCharacter->GetMesh()->GetAttachChildren();
			for (USceneComponent* Children : AllChildren)
			{
				Children->DestroyComponent();
			}
		}
		RiderActorComponent->DestroyComponent();
		RiderActorComponent = nullptr;
	}
}

void URideCarrierComponent::PlayRideEffect(FString EffectId)
{
	SCOPE_CYCLE_COUNTER(STAT_PlayRideEffect);
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URideCarrierComponent::PlayRideEffect : PlayerCharacter!"));
		return;
	}

	TWeakObjectPtr<URideCarrierComponent> DelayThisPtr(this);
	UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectId, 0.0f,
		PlayerCharacter, PlayerCharacter, FEffectCreate::CreateLambda([this, EffectId, DelayThisPtr](int32 UID)
	{
		if (!DelayThisPtr.IsValid())
		{
			return;
		}
		URideCarrierComponent* ThisPtr = DelayThisPtr.Get();
		APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(ThisPtr->GetOwner());
		if (PlayerCharacter && PlayerCharacter->IsControlled())
		{
			const FEFFECT_EMITTER_DATA *EffectEmitterData = UUECS3GameInstance::Instance->ParticleManager->GetEffectData(EffectId);
			UCharacterRideManager *CharacteRiderManager = UUECS3GameInstance::Instance->CharacterRideManager;
			CharacteRiderManager->CacheRideAsset(EffectEmitterData->ParticleData.ParticleSystemAsset.ToString(), EffectEmitterData->ParticleData.ParticleSystemAsset.Get());
			if (EffectEmitterData->SkeletalMesh.AnimAssetList.Num())
			{
				CharacteRiderManager->CacheRideAsset(EffectEmitterData->SkeletalMesh.AnimAssetList[0].ToString(), EffectEmitterData->SkeletalMesh.AnimAssetList[0].Get());
			}
			CharacteRiderManager->CacheRideAsset(EffectEmitterData->SkeletalMesh.SkeletalMeshAsset.ToString(), EffectEmitterData->SkeletalMesh.SkeletalMeshAsset.Get());
			CharacteRiderManager->CacheRideAsset(EffectEmitterData->StaticMesh.StaticMeshAsset.ToString(), EffectEmitterData->StaticMesh.StaticMeshAsset.Get());
		}
	}));
}

void URideCarrierComponent::RideGetOnActionOver()
{
	SCOPE_CYCLE_COUNTER(STAT_RideGetOnActionOver);
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URideCarrierComponent::RideGetOnActionOver : PlayerCharacter!"));
		return;
	}
	ClearTimer(RiderGetOnFrameTimerHle);
	RiderActorComponent->AttachToComponent(PlayerCharacter->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, TEXT("Socket_Ride"));
	RiderActorComponent->SetRelativeLocation(FVector(0.0f, 0.0f, 0.0f));
	//RiderActorComponent->SetAbsolute(false, false, false);
	//骑上马后武器是隐藏的，但是一走动又显示出来
	GetRiderCharacter()->CheckPartHideByAction(GetRiderCharacter()->GetBaseAnimInstance()->GetCurPlayActionData());

	//检测人物的状态[如:飞行中]
	if (IsValid(PlayerCharacter->FlyPatrolComponent) && PlayerCharacter->FlyPatrolComponent->IsFlyPatrolState())
	{
		PlayerCharacter->FlyPatrolComponent->SwitchFlyOrbitMode();
	}
}

void URideCarrierComponent::RideGetOffActionOver(bool IsCreateAppearance)
{
	SCOPE_CYCLE_COUNTER(STAT_RideGetOffActionOver);
	ClearTimer(RiderGetOffTimerHle);
	DestroyRiderComponent();
	CarrierId = "";
	///已在载具的时候下，则不要重复创建单独模型
	if (IsCreateAppearance)
	{
		OnCreateRoleAppearance.Broadcast();
	}
}

void URideCarrierComponent::ClearTimer(FTimerHandle& InHandle)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(InHandle);
	}
}

URoleAnimInstance* URideCarrierComponent::GetRoleAnimInstance()
{
	APlayerCharacter* RidePetCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!RidePetCharacter)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URideCarrierComponent::GetRoleAnimInstance : RidePetCharacter!"));
		return nullptr;
	}
	return Cast<URoleAnimInstance>(RidePetCharacter->GetBaseAnimInstance());
}

URiderAnimInstance* URideCarrierComponent::GetRiderAnimInstance()
{
	APlayerCharacter* RidePetCharacter = Cast<APlayerCharacter>(GetOwner());
	if (!IsValid(RidePetCharacter) || !RidePetCharacter->GetRiderCharacter())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URideCarrierComponent::GetRiderAnimInstance : RidePetCharacter||GetRiderCharacter()!"));
		return nullptr;
	}
	return Cast<URiderAnimInstance>(RidePetCharacter->GetRiderCharacter()->GetBaseAnimInstance());
}

CONTROL_COMPILE_OPTIMIZE_END
