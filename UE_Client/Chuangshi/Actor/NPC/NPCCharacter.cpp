// Fill out your copyright notice in the Description page of Project Settings.

#include "NPCCharacter.h"
#include "Components/CapsuleComponent.h"
#include "../Player/PlayerCharacter.h"
#include "Manager/ParticleManager.h"
#include "Util/ConvertUtil.h"
#include "Manager/VisibleManager.h"
#include "GameData/GameDefault.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "Manager/CfgManager.h"
#include "Manager/ShapeManager.h"
#include "Util/CS3Debug.h"
#include "Entity/NPC/NPCGinsengFruit.h"
#include "Interface/NPC/NPCInterface.h"
#include "Component/AppearanceComponent.h"

ANPCCharacter::ANPCCharacter()
{
	CharacterClassName = TEXT("NPCCharacter");
	PrimaryActorTick.bCanEverTick = true;
	InitBaseComponent();
}

void ANPCCharacter::BeginPlay()
{
	Super::BeginPlay();
}

void ANPCCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor)) 
	{
		PlayerActor->RemoveFromInteractivityList(this);
	}
}

void ANPCCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();
	pNPCShape = CreateSphereShape();
}

UBaseShape* ANPCCharacter::CreateSphereShape()
{
	float radius = m_SphereRadius;
	FVector shapeVector = FVector(radius, radius, radius);
	return UUECS3GameInstance::Instance->ShapeManager->CreateShape(this, this, SHAPE_TYPE::SHPERE, shapeVector, &ANPCCharacter::OnPlayerBeginOverlap, &ANPCCharacter::OnPlayerEndOverlap);
}


void ANPCCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

void ANPCCharacter::OnPlayerBeginOverlap_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(this);
}

void ANPCCharacter::OnPlayerEndOverlap_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(this);
}

void ANPCCharacter::GossipWith()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor) || !IsValid(PlayerController)) return;
	///NPC转向玩家
	FVector StartLoction = GetActorLocation();
	FVector TargetLoction = PlayerActor->GetActorLocation();
	FRotator NPCRotation = UGolbalBPFunctionLibrary::GetLookAtRotator(StartLoction, TargetLoction);
	if (!this->HasFlag(ENTITY_FLAG::FLAG_CANT_MOVE_AND_ROTATE))
	{
		SetActorRotation(NPCRotation);
	}

	UNPCBaseObjectInterface * NPCInterface = Cast<UNPCBaseObjectInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (NPCInterface)
	{
		NPCInterface->RPC_CELL_gossipWith();
	}
	//KBEngine::FVariantArray Args;

	//if (KBEngine::Entity* NPC = GetSelfEntity())

	//{
	//	NPC->CellCall(TEXT("CELL_gossipWith"), Args);
	//}


	if (UGolbalBPFunctionLibrary::GetActorDistance(PlayerActor, this) < UUECS3GameInstance::Instance->GameDefault->NPCTalkStopMoveDistance * 100.0f)
	{
		PlayerController->StopMove();
		//玩家转向NPC	
		FRotator PlayerRotation = UGolbalBPFunctionLibrary::GetLookAtRotator(TargetLoction, StartLoction);
		PlayerActor->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_TALKTONPC;
		PlayerActor->SetActorRotation(PlayerRotation);

		CS3_Display(CS3DebugType::CL_Undefined, TEXT("ANPCCharacter::GossipWith GetActorDistance() < NPCTalkStopMoveDistance !"));
		return;
	}
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (IsValid(ControllerModeMgr)&& ControllerModeMgr->IsHaveMode(ECONTROL_MODE::YControlMode))
	{
		///<CST-4905 在Y模式下需要取消右键并退出Y模式
		TArray<FString> OtherValue;
		ControllerModeMgr->ExecuteInputInfor(TEXT("FlushPressedKeysAndRecoveryControlMode"), TEXT(""), 0.0f, OtherValue);
	}
	FVector destination = this->GetActorLocation();
	destination.Z = destination.Z - this->GetCapsuleComponent()->GetScaledCapsuleHalfHeight() + this->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight();
	TWeakObjectPtr<ANPCCharacter> DelayThisPtr(this);
	PlayerController->TraceTargetPostion(destination, UUECS3GameInstance::Instance->GameDefault->NPCTalkStopMoveDistance, nullptr, true, FTraceCallback::CreateLambda([DelayThisPtr](bool IsSuccess)
	{
		if (DelayThisPtr.IsValid())
		{
			ANPCCharacter* ThisPtr = DelayThisPtr.Get();
			if (IsSuccess)
			{
				APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
				if (!IsValid(PlayerActor))
				{
					CS3_Warning(TEXT("-->Null Pointer error:ANPCCharacter::GossipWith : PlayerActor!"));
					return;
				}

				FVector StartLoction = ThisPtr->GetActorLocation();
				FVector TargetLoction = PlayerActor->GetActorLocation();
				//玩家转向NPC
				FRotator PlayerRotation = UGolbalBPFunctionLibrary::GetLookAtRotator(TargetLoction, StartLoction);
				PlayerActor->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_TALKTONPC;
				PlayerActor->SetActorRotation(PlayerRotation);
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("ANPCCharacter::GossipWith TraceTargetPostion Success!"));
			}
		}
	}));

}

void ANPCCharacter::SetInitAction()
{
	KBEngine::Entity* SelfEntity = GetSelfEntity();
	InitActionId = !SelfEntity ? "None" : FSTRING_TO_FNAME((FString)SelfEntity->GetDefinedProperty(TEXT("initActionId")));
}

void ANPCCharacter::PlayDeadEffect()
{
	KBEngine::Entity* Entity = GetSelfEntity();
	if (Entity == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:ANPCCharacter::PlayDeadEffect : Entity!"));
		return;
	}
	FString ScriptID = Entity->GetDefinedProperty(TEXT("scriptID"));
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const FNPC_DATA* NpcData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC)->GetRow<FNPC_DATA>(ScriptID);
	if (NpcData && !NpcData->DeadEffectId.IsEmpty())
	{
		bIsPlayDeadEffect = true;
		UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(this);
		UUECS3GameInstance::Instance->ParticleManager->PlayParticle(NpcData->DeadEffectId, 0.0f, this, this);
	}
}

FString ANPCCharacter::GetEntityUName()
{
	return UGolbalBPFunctionLibrary::GetFStringPropertyValue(EntityId, TEXT("uname"));
}

int32 ANPCCharacter::GetFinalCamp()
{
	KBEngine::Entity* Entity = GetSelfEntity();
	if (Entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ANPCCharacter::GetFinalCamp : Entity!"));
		return 0;
	}
	int32 tempCamp = Entity->GetDefinedProperty(TEXT("tempCamp")).GetValue<int32>();
	int32 camp = Entity->GetDefinedProperty(TEXT("camp")).GetValue<int32>();
	if (tempCamp != 0)
	{
		return tempCamp;
	}
	return camp;
}

bool ANPCCharacter::IsEntityBoss()
{
	int32 AttrLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityId, TEXT("attrLevel"));
	return AttrLevel > 1;
}

void ANPCCharacter::RPC_onCollisionBegin()
{
	KBEngine::Entity* entity = GetSelfEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ANPCCharacter::RPC_onCollisionBegin : entity!"));
		return;
	}
	UNPCInterface * NPCInterface = Cast<UNPCInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (NPCInterface)
	{
		NPCInterface->onCollisionBegin();
	}
	//KBEngine::FVariantArray args;
	//entity->CellCall(TEXT("onCollisionBegin"), args);
}