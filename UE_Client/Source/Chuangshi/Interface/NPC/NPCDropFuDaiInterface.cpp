
#include "NPCDropFuDaiInterface.h"
#include "Components/TextRenderComponent.h"
#include "Actor/NPC/NPCCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/AvatarFilterActorComponent.h"
#include "Manager/ParticleManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(UNPCDropFuDaiInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UNPCDropFuDaiInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()


UNPCDropFuDaiInterface::UNPCDropFuDaiInterface()
{
}


UNPCDropFuDaiInterface::~UNPCDropFuDaiInterface()
{
}

void UNPCDropFuDaiInterface::RPC_onFuDaiCollisionBegin(const int32& PlayID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNPCDropFuDaiInterface::RPC_onFuDaiCollisionBegin : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(PlayID);

	entity->CellCall(TEXT("onFuDaiCollisionBegin"), args);
}

void UNPCDropFuDaiInterface::RPC_onFuDaiCollisionPlayer(const int32& PlayID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNPCDropFuDaiInterface::RPC_onFuDaiCollisionPlayer : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(PlayID);

	entity->CellCall(TEXT("onFuDaiCollisionPlayer"), args);
}
void UNPCDropFuDaiInterface::RPC_onFuDaiCollisionMonster(const int32& MonsterID)
{
}

void UNPCDropFuDaiInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_fuDaiStartMove");
	ArrBlueFunc.Add("CLIENT_OnPlayFloorEffect");
	ArrBlueFunc.Add("CLIENT_OnFuDaiBlink");
	ArrBlueFunc.Add("NotifyIntegralAmount");
	Supper::InitBlueCB();
}

void UNPCDropFuDaiInterface::CLIENT_fuDaiStartMove_Implementation(const float& Resistance, const FString& EffectID)
{
	ANPCCharacter* NPCCharacter = Cast<ANPCCharacter>(GetActor());
	if (NPCCharacter)
	{
		PickEffectID = EffectID;
		NPCCharacter->SetEnableSyncServerPos(false);//关闭服务器同步位置
		UFilterActorComponent* FilterComponent = Cast<UFilterActorComponent>(NPCCharacter->GetFilterComponent());
		if (FilterComponent)
		{
			FilterComponent->SetActiveComponentTick(false);	
		}
		NPCCharacter->GetCapsuleComponent()->SetSimulatePhysics(true);
		NPCCharacter->GetCapsuleComponent()->SetLinearDamping(Resistance);

		// 播放落地的预警光效
		TWeakObjectPtr<ANPCCharacter> ActorPtr(NPCCharacter);
		UUECS3GameInstance::Instance->ParticleManager->PlayParticle("101718", 0.f, NPCCharacter, NPCCharacter, FEffectCreate::CreateLambda([ActorPtr](int32 UID)
		{
			AActor* Emitter = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);

			if (IsValid(Emitter) && ActorPtr.IsValid())
			{
				ANPCCharacter* ThisActor = ActorPtr.Get();
				FVector Location = ThisActor->FloorTrace(ThisActor->GetActorLocation());
				Location.Z -= ThisActor->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
				Emitter->SetActorLocation(Location);
			}
		}));
	}
}

void UNPCDropFuDaiInterface::CLIENT_OnPlayFloorEffect_Implementation(const FString& EffectID)
{
	ANPCCharacter* NPCCharacter = Cast<ANPCCharacter>(GetActor());
	if (NPCCharacter)
	{
		TWeakObjectPtr<ANPCCharacter> ActorPtr(NPCCharacter);
		UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.f, NPCCharacter, NPCCharacter, FEffectCreate::CreateLambda([ActorPtr](int32 UID)
		{
			AActor* Emitter = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);

			if (IsValid(Emitter) && ActorPtr.IsValid())
			{
				ANPCCharacter* ThisActor = ActorPtr.Get();
				FVector Location = ThisActor->FloorTrace(ThisActor->GetActorLocation());
				Location.Z -= ThisActor->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
				Emitter->SetActorLocation(Location);
			}
		}));
	}
}

void UNPCDropFuDaiInterface::NotifyIntegralAmount_Implementation(const int32& moneyAmount)
{
	ANPCCharacter* NPCCharacter = Cast<ANPCCharacter>(GetActor());
	if (NPCCharacter)
	{
		if (!IsValid(TextRenderComponent))
		{
			APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			if (PlayerCharacter && PlayerCharacter->CameraComponent)
			{
				FRotator TextRenderRotation = FRotator(0, PlayerCharacter->CameraComponent->GetComponentRotation().Yaw + 180.f, 0);
				FVector TextLoaction = PlayerCharacter->CameraComponent->GetRightVector() * 100 + NPCCharacter->GetActorLocation() + FVector::UpVector * -50.f;
				TextRenderComponent = NewObject<UTextRenderComponent>(NPCCharacter, TEXT("TextRenderComponent"));
				TextRenderComponent->RegisterComponent();
				TextRenderComponent->SetAbsolute(true, true, true);
				TextRenderComponent->AttachToComponent(NPCCharacter->GetRootComponent(),FAttachmentTransformRules::KeepRelativeTransform);
				TextRenderComponent->SetWorldLocation(TextLoaction);
				TextRenderComponent->SetWorldRotation(TextRenderRotation.Quaternion());
				TextRenderComponent->SetWorldScale3D(FVector::OneVector);
				// 设置数字
				TextRenderComponent->SetText(FSTRING_TO_FTEXT("X " + INT_TO_FSTRING(moneyAmount)));
				TextRenderComponent->SetWorldSize(90);
				TextRenderComponent->SetTextRenderColor(FColor::Red);
				SetJinBiPosition();
			}
		}
	}
}

void UNPCDropFuDaiInterface::SetJinBiPosition()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
	{
		TWeakObjectPtr<UNPCDropFuDaiInterface> DelayAIComponentPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, SetPosTimer,
			FTimerDelegate::CreateLambda([DelayAIComponentPtr]()
		{
			if (DelayAIComponentPtr.IsValid())
			{
				ANPCCharacter* NPCCharacter = Cast<ANPCCharacter>(DelayAIComponentPtr.Get()->GetActor());
				if (NPCCharacter)
				{
					if (IsValid(DelayAIComponentPtr.Get()->TextRenderComponent))
					{
						APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
						if (PlayerCharacter && PlayerCharacter->CameraComponent)
						{
							FRotator TextRenderRotation = FRotator(0, PlayerCharacter->CameraComponent->GetComponentRotation().Yaw + 180.f, 0);
							FVector TextLoaction = PlayerCharacter->CameraComponent->GetRightVector() * 100 + NPCCharacter->GetActorLocation() + FVector::UpVector * -50.f;
							DelayAIComponentPtr.Get()->TextRenderComponent->SetWorldLocation(TextLoaction);
							DelayAIComponentPtr.Get()->TextRenderComponent->SetWorldRotation(TextRenderRotation.Quaternion());
							DelayAIComponentPtr.Get()->TextRenderComponent->SetWorldScale3D(FVector::OneVector);
						}
					}
				}
			}
		}
		), 0.2, true);
	}
}

CONTROL_COMPILE_OPTIMIZE_END
