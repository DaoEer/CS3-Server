// Fill out your copyright notice in the Description page of Project Settings.


#include "SceneCharacter.h"
#include "Manager/ParticleManager.h"
#include "Component/AppearanceComponent.h"
#include "Util/ConvertUtil.h"
#include "Actor/Particle/EffectEmitter.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"

//CONTROL_COMPILE_OPTIMIZE_START

ASceneCharacter::ASceneCharacter()
{
	PrimaryActorTick.bCanEverTick = true;
	CharacterClassName = TEXT("SceneCharacter");
	InitBaseComponent();
}

void ASceneCharacter::BeginPlay()
{
	Super::BeginPlay();	
}

void ASceneCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);
	if (SceneCreateApperanceOver.IsBound())
	{
		SceneCreateApperanceOver.Clear();
	}	 
}

void ASceneCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

void ASceneCharacter::CreateActorData(FCREATE_ENTITY_EFFECT_DATA EntityEffectData)
{
	ModelNumber = EntityEffectData.ModelNumber;
	ModelScale = EntityEffectData.ModelScale;
	ActionNames = EntityEffectData.ActionNames;
	ActionIntervals = EntityEffectData.ActionIntervals;
	CollisionType = EntityEffectData.CollisionType;
	bAffectNavigation = EntityEffectData.bAffectNavigation;
	bCameraCollision = EntityEffectData.bCameraCollision;
	bVisibilityCollision = EntityEffectData.bVisibilityCollision;
	EffectIDs = EntityEffectData.EffectIDs;
	EffectIntervals = EntityEffectData.EffectIntervals;
	bIsRandomAction = EntityEffectData.bIsRandomAction;
	bIsRandomEffect = EntityEffectData.bIsRandomEffect;
	DeathActionID = TEXT("");
	DeathEffectID = TEXT("");
	GetAppearanceComponent()->CreateAppearance(ModelNumber);
}

void ASceneCharacter::SetActionData(TArray<FString> actionName, TArray<float> actionInterval, bool bIsRandom)
{
	///<停止播放
	if (ActionNames.Num() > 0)
	{
		ActionNames.Reset();
		ActionIntervals.Reset();
		StopAction();
	}

	bIsRandomAction = bIsRandom;
	ActionNames = actionName;
	ActionIntervals = actionInterval;
	FACTION_DATA ActionData = FACTION_DATA();
	CheckPlayAction(this, ActionData);
}

void ASceneCharacter::SetEffectData(TArray<FString> effectID, TArray<float> effectInterval, bool bIsRandom /*= false*/)
{
	if (EffectIDs.Num() > 0)
	{
		if (CurEffectUID > 0)
		{
			UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(CurEffectUID);
		}
		EffectIDs.Reset();
		EffectIntervals.Reset();
	}
	bIsRandomEffect = bIsRandom;
	EffectIDs = effectID;
	EffectIntervals = effectInterval;
	CheckPlayEffect();
}

void ASceneCharacter::SetDestroyAction(FString actionName)
{
	DeathActionID = actionName;
}

void ASceneCharacter::SetDestroyEffect(FString effectID)
{
	DeathEffectID = effectID;
}

void ASceneCharacter::ClearActionData()
{
	ActionNames.Empty();
	ActionIntervals.Empty();
	StopAction();
}

void ASceneCharacter::ClearEffectData()
{
	EffectIDs.Empty();
	EffectIntervals.Empty();
	UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(CurEffectUID);

}

void ASceneCharacter::OnBeginDestroyActor_Implementation()
{
	///<播放动作
	if (!DeathActionID.IsEmpty())
	{
		FActionOverDelegate Delegate;
		Delegate.AddUObject(this, &ASceneCharacter::OnPlayDestroyActionOver);
		PlayAction(FSTRING_TO_FNAME(DeathActionID), 0.0f, Delegate);
	}

	///<播放光效
	if (!DeathEffectID.IsEmpty())
	{
		TWeakObjectPtr<ASceneCharacter> DelayThisPtr(this);
		CurEffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(DeathEffectID, 0.0f, this, this, FEffectCreate::CreateLambda([DelayThisPtr](int32 UID)
		{
			if (DelayThisPtr.IsValid())
			{
				AEffectEmitter* Effect = Cast<AEffectEmitter>(UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID));
				ASceneCharacter* ThisPtr = DelayThisPtr.Get();
				if (Effect)
				{
					Effect->OnEffectStop.AddDynamic(ThisPtr, &ASceneCharacter::OnPlayDestroyEffectOver);
				}
				else
				{
					UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(ThisPtr->CurEffectUID);
					ThisPtr->OnPlayDestroyEffectOver();
				}
			}
		}));
	}
	///<无动作或光效直接销毁
	if (DeathEffectID.IsEmpty() && DeathActionID.IsEmpty())
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(CurEffectUID);
		Destroy();
	}
}

void ASceneCharacter::SetModelScale(const float &newValue)
{
	///<设置Scale不修改位置是生成的位置是已改变模型大小的后的位置。
	SetActorScale3D(FVector(newValue, newValue, newValue));
}

void ASceneCharacter::SetCollisionType(const FString &newValue)
{
	if (newValue == "COLLISION_DEFAULT")
	{
		SetMeshCollisionType(ECollisionEnabled::QueryAndPhysics);
		GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
	else if (newValue == "COLLISION_ENEMY")
	{
		SetMeshCollisionType(ECollisionEnabled::NoCollision);
		GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
		GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_Pawn, ECollisionResponse::ECR_Block);
		GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel3, ECollisionResponse::ECR_Block);
		GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel4, ECollisionResponse::ECR_Block);
		GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel5, ECollisionResponse::ECR_Block);
		GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel6, ECollisionResponse::ECR_Block);

	}
	else if (newValue == "COLLISION_NONE")
	{		
		SetMeshCollisionType(ECollisionEnabled::NoCollision);
		GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}

	GetMesh()->SetCanEverAffectNavigation(bAffectNavigation);

}

void ASceneCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();
	SetModelScale(ModelScale);
	SetInitAction();
	SetCollisionType(CollisionType);
	FACTION_DATA ActionData = FACTION_DATA();
	CheckPlayAction(this, ActionData);
	CheckPlayEffect();
	SceneCreateApperanceOver.Broadcast(this);
}

void ASceneCharacter::OnChangePartOver()
{

}
void ASceneCharacter::OnPlayDestroyActionOver(ACharacter *RoleChar, FACTION_DATA InActionData)
{
	if (IsValid(RoleChar) && IsValid(Cast<ASceneCharacter>(RoleChar)) && Cast<ASceneCharacter>(RoleChar) == this)
	{
		DeathActionID = TEXT("");
		if (DeathEffectID.IsEmpty())
		{
			Destroy();
		}
	}
}

void ASceneCharacter::OnPlayDestroyEffectOver()
{
	DeathEffectID = TEXT("");
	if (DeathActionID.IsEmpty())
	{
		Destroy();
	}
}

void ASceneCharacter::PlayMultiAction()
{
	int ActionNameIndex = 0;
	if (ActionNames.Num() > 0)
	{
		if (bIsRandomAction)
		{
			///<按随机播放动作
			ActionNameIndex = GetRandomIndex(ActionNames.Num());
		}

		///<播放动作
		FActionOverDelegate Delegate;
		Delegate.AddUObject(this, &ASceneCharacter::CheckPlayAction);
		PlayAction(FSTRING_TO_FNAME(ActionNames[ActionNameIndex]), 0.0f, Delegate);
		if (!bIsRandomAction)
		{
			ActionNames.RemoveAt(0);
		}			
	}
	else
	{
		if (DelayHandle.IsValid())
		{
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayHandle);
			}
		}
	}
}

void ASceneCharacter::CheckPlayAction(ACharacter *RoleChar, FACTION_DATA InActionData)
{
	if (ActionNames.Num() > 0 && IsValid(RoleChar) && IsValid(Cast<ASceneCharacter>(RoleChar)) && Cast<ASceneCharacter>(RoleChar) == this)
	{
		if (ActionIntervals.Num() > 0 && ActionIntervals[0] > 0)
		{
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, this, 
					&ASceneCharacter::PlayMultiAction, ActionIntervals[0], false);
			}

		}
		else
		{
			PlayMultiAction();
			if (!bIsRandomAction)
			{
				if (ActionIntervals.Num() > 0)
				{
					ActionIntervals.RemoveAt(0);
				}
			}
		}
	}
}

int ASceneCharacter::GetRandomIndex(int MaxRandomIndex)
{
	if (MaxRandomIndex > 0)
	{
		return FMath::RandHelper(MaxRandomIndex);
	}
	return 0;
}

void ASceneCharacter::CheckPlayEffect()
{
	if (EffectIDs.Num() > 0)
	{		
		if (EffectIntervals.Num() > 0 && EffectIntervals[0] > 0)
		{
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayEffectHandle, this, 
					&ASceneCharacter::PlayMultiEffect, EffectIntervals[0], false);
			}
		}
		else
		{
			PlayMultiEffect();
			if (!bIsRandomAction)
			{
				if (EffectIntervals.Num() > 0)
				{
					EffectIntervals.RemoveAt(0);
				}
			}
		}
	}
}

void ASceneCharacter::PlayMultiEffect()
{
	int EffectIndex = 0;
	if (EffectIDs.Num() > 0)
	{
		if (bIsRandomEffect)
		{
			///<按随机播放动作
			EffectIndex = GetRandomIndex(EffectIDs.Num());
		}
		///<播放粒子
		TWeakObjectPtr<ASceneCharacter> DelayThisPtr(this);
		CurEffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectIDs[EffectIndex], 0.0f, this, this, FEffectCreate::CreateLambda([DelayThisPtr, DelayCurEffectUID = CurEffectUID](int32 UID)
		{
			if (DelayThisPtr.IsValid())
			{
				ASceneCharacter* ThisPtr = DelayThisPtr.Get();
				AEffectEmitter* Effect = Cast<AEffectEmitter>(UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID));
				if (Effect) 
				{
					Effect->OnEffectStop.AddDynamic(ThisPtr, &ASceneCharacter::CheckPlayEffect);
				}
			}
			else
			{
				UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(DelayCurEffectUID);
			}
		}));
		if (!bIsRandomEffect)
		{
			EffectIDs.RemoveAt(0);
		}
	}
	else
	{
		if (DelayEffectHandle.IsValid())
		{
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayEffectHandle);
			}
		}
	}
}

void ASceneCharacter::SetMeshCollisionType(ECollisionEnabled::Type CollisionTYpe)
{
	if (IsValid(GetMesh()) && IsValid(GetMesh()->SkeletalMesh))
	{
		SetCollisionCollisionTypeAndResponseToChannel(GetMesh(), CollisionTYpe);
	}
	if (IsValid(STMesh_DefaultStatic) && IsValid(STMesh_DefaultStatic->GetStaticMesh()))
	{
		SetCollisionCollisionTypeAndResponseToChannel(STMesh_DefaultStatic, CollisionTYpe);
	}
}

void ASceneCharacter::SetCollisionCollisionTypeAndResponseToChannel(UMeshComponent* SKComp, ECollisionEnabled::Type CollisionTYpe)
{
	if (IsValid(SKComp))
	{
		SKComp->SetCollisionEnabled(CollisionTYpe);
		SKComp->SetCollisionResponseToChannel(ECollisionChannel::ECC_Camera, bCameraCollision == true ? ECollisionResponse::ECR_Block : ECollisionResponse::ECR_Ignore);
		SKComp->SetCollisionResponseToChannel(ECollisionChannel::ECC_Visibility, bVisibilityCollision == true ? ECollisionResponse::ECR_Block : ECollisionResponse::ECR_Ignore);
		if (CollisionTYpe == ECollisionEnabled::NoCollision)
			return;
		SKComp->SetCollisionResponseToChannel(ECollisionChannel::ECC_Pawn, ECollisionResponse::ECR_Block);
		SKComp->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel3, ECollisionResponse::ECR_Block);
		SKComp->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel4, ECollisionResponse::ECR_Block);
		SKComp->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel5, ECollisionResponse::ECR_Block);
		SKComp->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel6, ECollisionResponse::ECR_Block);
	}
}

//CONTROL_COMPILE_OPTIMIZE_END
