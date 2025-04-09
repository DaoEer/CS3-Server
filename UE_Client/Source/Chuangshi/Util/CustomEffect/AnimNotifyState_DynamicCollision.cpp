// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotifyState_DynamicCollision.h"
#include "Components/BoxComponent.h"
#include "Interface/SkillInterface.h"
#include "Util/CS3Debug.h"
#include "Kismet/GameplayStatics.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/ServerCharacter.h"
#include "Particles/ParticleSystemComponent.h"

CONTROL_COMPILE_OPTIMIZE_START

UAnimNotifyState_DynamicCollision::UAnimNotifyState_DynamicCollision()
	: Supper()
{
	PSTemplate = nullptr;
	LocationOffset.Set(0.0f, 0.0f, 0.0f);
	RotationOffset = FRotator(0.0f, 0.0f, 0.0f);
	PSC = nullptr;
}

void UAnimNotifyState_DynamicCollision::NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration)
{
	Supper::NotifyBegin(MeshComp, Animation, TotalDuration);
	CurTime = 0.0f;

	if (PSTemplate)
	{
		if (Attached)
		{
			PSC = UGameplayStatics::SpawnEmitterAttached(PSTemplate, MeshComp, SocketName, LocationOffset, RotationOffset);
		}
		else
		{
			const FTransform MeshTransform = MeshComp->GetSocketTransform(SocketName);
			FTransform SpawnTransform;
			SpawnTransform.SetLocation(MeshTransform.TransformPosition(LocationOffset));
			SpawnTransform.SetRotation(MeshTransform.GetRotation() * FQuat(RotationOffset));
			PSC = UGameplayStatics::SpawnEmitterAtLocation(MeshComp->GetWorld(), PSTemplate, SpawnTransform);
		}
	}
	if (!IsValid(BoxCollision))
	{
		BoxCollision = NewObject<UBoxComponent>(MeshComp);
		BoxCollision->AttachToComponent(MeshComp, FAttachmentTransformRules::KeepRelativeTransform, SocketName);
		BoxCollision->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
		BoxCollision->SetCollisionObjectType(ECollisionChannel::ECC_Pawn);
		BoxCollision->SetCollisionResponseToChannel(ECollisionChannel::ECC_EngineTraceChannel3, ECollisionResponse::ECR_Overlap);
		BoxCollision->SetCollisionResponseToChannel(ECollisionChannel::ECC_EngineTraceChannel4, ECollisionResponse::ECR_Overlap);
		BoxCollision->SetGenerateOverlapEvents(true);
		BoxCollision->OnComponentBeginOverlap.AddDynamic(this, &UAnimNotifyState_DynamicCollision::OnEmitterCollisionBegin);
		BoxCollision->OnComponentEndOverlap.AddDynamic(this, &UAnimNotifyState_DynamicCollision::OnEmitterCollisionEnd);
		BoxCollision->bVisible = 1;
		BoxCollision->RegisterComponentWithWorld(MeshComp->GetWorld());

		
	}
	BoxCollision->SetRelativeLocation(BoxLocationOffset);
	BoxCollision->SetRelativeRotation(BoxRotationOffset);
	BoxCollision->SetBoxExtent(FVector(0.0, BoxWide, BoxHigh), true);
}

void UAnimNotifyState_DynamicCollision::NotifyTick(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation, float FrameDeltaTime)
{
	Supper::NotifyTick(MeshComp, Animation, FrameDeltaTime);
	if (!IsValid(BoxCollision))return;

	CurTime += FrameDeltaTime;

	_CalculateBox();
}

void UAnimNotifyState_DynamicCollision::NotifyEnd(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{
	if (IsValid(PSC))
	{
		if (bDestroyAtEnd)
		{
			PSC->DestroyComponent();
		}
		else
		{
			PSC->DeactivateSystem();
		}
	}
	
	Supper::NotifyEnd(MeshComp, Animation);
}

void UAnimNotifyState_DynamicCollision::StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{
	Supper::StopNotifyEffect(MeshComp, Animation);

	NotifyEnd(MeshComp, Animation);
}

void UAnimNotifyState_DynamicCollision::OnEmitterCollisionBegin(UPrimitiveComponent * OverlappedComp, AActor * Other, UPrimitiveComponent * OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult & SweepResult)
{
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Other);
	if (IsValid(ServerCharacter))
	{
		KBEngine::Entity* _entity = ServerCharacter->GetSelfEntity();
		if (_entity && _entity->IsPlayer())
		{
			USkillInterface* _SkillInterface = ServerCharacter->GetEntityInterface_Cache().SkillInterface;
			if (IsValid(_SkillInterface))
			{
				_SkillInterface->UseSkill(EnterSkillID, ServerCharacter->EntityId);
			}
		}
	}
}

void UAnimNotifyState_DynamicCollision::OnEmitterCollisionEnd(UPrimitiveComponent * OverlappedComp, AActor * Other, UPrimitiveComponent * OtherComp, int32 OtherBodyIndex)
{
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Other);
	if (IsValid(ServerCharacter))
	{
		KBEngine::Entity* _entity = ServerCharacter->GetSelfEntity();
		if (_entity && _entity->IsPlayer())
		{
			USkillInterface* _SkillInterface = ServerCharacter->GetEntityInterface_Cache().SkillInterface;
			if (IsValid(_SkillInterface))
			{
				_SkillInterface->UseSkill(LeaveSkillID, ServerCharacter->EntityId);
			}
		}
	}
}

void UAnimNotifyState_DynamicCollision::_CalculateBox()
{
	if (CurTime == 0.0)  return;
	if (CurTime <= GrowTime)
	{
		FVector BoxExtent(CurTime * PerGrow, BoxWide, BoxHigh);
		BoxCollision->SetBoxExtent(BoxExtent, true);
		FTransform transForm = BoxCollision->GetRelativeTransform();
		BoxCollision->SetRelativeLocation(BoxLocationOffset + transForm.TransformVector(FVector(CurTime * PerGrow, 0.0, 0.0)));
	}
	else if (CurTime <= GrowTime + HoldTime)
	{
		return;
	}
	else
	{
		float DecayTime = CurTime - GrowTime - HoldTime;
		float ExtentValue = GrowTime * PerGrow - DecayTime * PerDecay;
		FVector BoxExtent(ExtentValue, BoxWide, BoxHigh);

		BoxCollision->SetBoxExtent(BoxExtent, true);
		FTransform transForm = BoxCollision->GetRelativeTransform();
		BoxCollision->SetRelativeLocation(BoxLocationOffset + transForm.TransformVector(FVector(GrowTime * PerGrow + DecayTime * PerDecay, 0.0, 0.0)));
	}
}

#if WITH_EDITOR
void UAnimNotifyState_DynamicCollision::PreEditChange(UProperty* PropertyAboutToChange)
{
	if (PropertyAboutToChange && IsValid(BoxCollision))
	{
		BoxCollision->SetRelativeRotation(BoxRotationOffset);
		_CalculateBox();
	}
}

#endif


CONTROL_COMPILE_OPTIMIZE_END