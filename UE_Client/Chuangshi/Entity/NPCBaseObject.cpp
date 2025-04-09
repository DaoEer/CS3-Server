
#include "NPCBaseObject.h"
#include "GameDevelop/CS3GameInstance.h"
#include "../Actor/ServerCharacter.h"
#include "GameData/GameDefault.h"
#include "GameData/GameDefine.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Components/WidgetComponent.h"
#include "Interface/NPCBaseObjectInterface.h"
#include "Interface/Role/RoleTalkInterface.h"
#include "Manager/ResourceManager.h"
#include "Component/CollisionComponent.h"
#include "Manager/LevelManager.h"
#include "Manager/VisibleManager.h"
#include "Manager/CustomTimerManager.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"

DECLARE_CYCLE_STAT(TEXT("CS3_NPCBaseEntity_CreateCharacter"), STAT_CS3_NPCBaseEntity_CreateCharacter, STATGROUP_CS3_NPCBaseEntity);

KBE_BEGIN_ENTITY_METHOD_MAP(NPCBaseObject, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCBaseObject, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

NPCBaseObject::NPCBaseObject()
{

}

NPCBaseObject::~NPCBaseObject()
{
}


void NPCBaseObject::OnSet_flags(const int64 &newValue, const int64 &oldValue)
{
	AServerCharacter* Character = Cast<AServerCharacter>(Actor());
	if (IsValid(Character))
	{
		Character->OnFlagsChanged();
		UNPCBaseObjectInterface * Interface = Cast<UNPCBaseObjectInterface>(Interface_Cache.GameObjectInterface);
		if (IsValid(Interface))
		{
			// 异或一下，有改变的标志位为1
			int64 ChangeResult = newValue ^ oldValue;
			// 与一下，只保留存在的标志位
			int64 OwnerFlag = ChangeResult & newValue;

			// 不可见标志位
			if (Interface->IsInFlags(ENTITY_FLAG::FLAG_UNVISIBLE, ChangeResult))
			{
				UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Actor());
			}
			
			//浮空标志位
			if (Interface->IsInFlags(ENTITY_FLAG::FLAG_CAN_FLY, ChangeResult))
			{
				if (Interface->IsInFlags(ENTITY_FLAG::FLAG_CAN_FLY, OwnerFlag))
				{
					Character->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
				}
				else
				{
					Character->GetCharacterMovement()->SetMovementMode(MOVE_Walking);
				}

				FVector Pos = Character->GetGroundPositionByEntity();
				//CS3_Warning(TEXT("-------------------------NPCBaseObject::OnSet_flags::position %f,%f,%f,pos.Z:%f"), Character->GetActorLocation().X, Character->GetActorLocation().Y, Character->GetActorLocation().Z, Pos.Z);
				Character->SetActorLocation(Pos);
			}

			//不可被选中标志位
			if (Interface->IsInFlags(ENTITY_FLAG::FLAG_CANT_SELECTED, ChangeResult) && Interface->IsInFlags(ENTITY_FLAG::FLAG_CANT_SELECTED, OwnerFlag))
			{
				Character->ClearTargetActor();
			}

			//开启模型碰撞标志位，关闭全部碰撞标志位，开启模型真实碰撞，开启模型摄像机碰撞
			if (Interface->IsInFlags(ENTITY_FLAG::FLAG_OPEN_COLLISION, ChangeResult)
				|| Interface->IsInFlags(ENTITY_FLAG::FLAG_CLOSE_COLLISION, ChangeResult)
				|| Interface->IsInFlags(ENTITY_FLAG::FLAG_MESH_COLLISION, ChangeResult)
				|| Interface->IsInFlags(ENTITY_FLAG::FLAG_OPEN_CAMERA_COLLISION, ChangeResult)
				|| Interface->IsInFlags(ENTITY_FLAG::FLAG_OPEN_GROUND_TRACE_COLLISION_CHANNEL, ChangeResult))
			{
				Character->CollisionComponent->UpdateModelCollision();
			}

			if (Interface->IsInFlags(ENTITY_FLAG::FLAG_CAN_BE_TREAD, ChangeResult))
			{
				Character->GetCapsuleComponent()->CanCharacterStepUpOn = ECanBeCharacterBase::ECB_Yes;
				Character->GetMesh()->CanCharacterStepUpOn = ECanBeCharacterBase::ECB_Yes;
			}
		}
	}
}

void NPCBaseObject::SetSyncPosClient(const int32 &newValue, const int32 &oldValue)
{
	if (newValue == oldValue)return;

	if (newValue != 0)
	{
		CloseSyncServerPos();
	}
	else
	{
		OpenSyncServerPos();
		if (AActor* actor = Actor())
		{
			FVector localPos = actor->GetActorLocation();
			Set_Position(localPos);
		}
	}

	//SyncPosClient是当前客户端玩家是，每0.1秒同步位置到服务器
	if (IsPlayerID(newValue))
	{
		StartSyncPosTimer(0.1f);
	}
	else
	{
		if (HasSyncPosTimer())
		{
			StopSyncPosTimer();
			SyncPosToServer();
		}
	}
}

void NPCBaseObject::StartSyncPosTimer(float interval)
{
	if (HasSyncPosTimer())
	{
		StopSyncPosTimer();
	}
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(
			this, SyncPosTimerHandle_, FTimerDelegate::CreateLambda([this]()
		{
			if (!this) return;
			SyncPosToServer();
		}), interval, true);
	}
}

void NPCBaseObject::StopSyncPosTimer()
{
	if (SyncPosTimerHandle_.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(SyncPosTimerHandle_);
		}
	}
}

bool NPCBaseObject::HasSyncPosTimer()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		return UUECS3GameInstance::Instance->CustomTimerManager->GetTimerRemaining(SyncPosTimerHandle_) > 0;
	}

	return false;
}

void NPCBaseObject::SyncPosToServer()
{
	FVector localPos = Actor()->GetActorLocation();
	FVector serverPos = KBEngine::KBEMath::Unreal2KBEnginePosition(localPos);
	KBEngine::FVariantArray args;
	args.Add(serverPos);
	CellCall(TEXT("syncPosToServer"), args);
}

void NPCBaseObject::OnEnterScenes()
{
	Supper::OnEnterScenes();
	if (IsReadyCreateActor())
	{
		CreateCharacter();
	}
	else
	{
		int32 EntityId = ID();
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(
				this, DetectParentTimerHandle, FTimerDelegate::CreateLambda([this, EntityId]()
			{
				if (!this) return;
				if (EntityId <= 0 || UGolbalBPFunctionLibrary::FindEntity(EntityId) == nullptr || UGolbalBPFunctionLibrary::FindEntity(EntityId) != this)
				{
					CS3_Warning(TEXT("-->Null Pointer error:NPCBaseObject::OnEnterScenes : UGolbalBPFunctionLibrary::FindEntity(ID()!"));
					return;
				}
				if (IsReadyCreateActor())
				{
					CreateCharacter();
				}
			}), 0.2, true);
		}
		
	}
}

void NPCBaseObject::OnEnterWorld()
{
	Supper::OnEnterWorld();
}

void NPCBaseObject::OnLeaveWorld()
{
	Supper::OnLeaveWorld();
	if (HasSyncPosTimer())
	{
		StopSyncPosTimer();
	}
	if (DetectParentTimerHandle.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DetectParentTimerHandle);
		}
	}
	///更新周围SpellBox交互状态 JIRA CST-3631
	URoleTalkInterface * talkInterface = Cast<URoleTalkInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTalkInterface")));
	if (talkInterface)
	{
		talkInterface->RefreshAroundBoxStatus(int32(SPELL_BOX_LISTEN_EVENT::EVENT_HAS_ENTITY));
	}
	if (IsValid(UUECS3GameInstance::Instance->LevelManager))
	{
		UUECS3GameInstance::Instance->LevelManager->RequestLeaveScenes(this);
	}
}


bool NPCBaseObject::IsReadyCreateActor()
{
	if (ParentID())
	{
		if (Parent() && IsValid(Parent()->Actor()))
		{
			return true;
		}
		return false;
	}
	return true;
}

void NPCBaseObject::DoCreateCharacter()
{
	SCOPE_CYCLE_COUNTER(STAT_CS3_NPCBaseEntity_CreateCharacter);
	UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;

	if (GameInstance)
	{
		UClass* ActorClass = GetEntityModelClassAsset();
		if (!ActorClass)
		{
			CS3_Warning(TEXT("-->Null Pointer error:NPCBaseObject::CreateCharacter : ActorClass!"));
			return;
		}
		int32 EntityId = ID();
		GameInstance->ResourceManager->RequestAsyncLoad(this, FStringAssetReference(ActorClass),
			FStreamableDelegate::CreateLambda([this, ActorClass, EntityId]()
		{
			if (!this) return;
			if (EntityId <= 0 || UGolbalBPFunctionLibrary::FindEntity(EntityId) == nullptr || UGolbalBPFunctionLibrary::FindEntity(EntityId) != this)
			{
				CS3_Warning(TEXT("-->Null Pointer error:NPCBaseObject::CreateCharacter : UGolbalBPFunctionLibrary::FindEntity(ID()!"));
				return;
			}

			if (ActorClass)
			{
				//const FVector &Location = Position();
				//const FRotator &Ratation = FRotator(FQuat::MakeFromEuler(Direction()));
				//AServerCharacter* RetActor = UGolbalBPFunctionLibrary::SpawnActor<AServerCharacter>(ActorClass, Location, Ratation);
				FTransform SpawnTransform = FTransform();
				SpawnTransform.SetLocation(Position());
				SpawnTransform.SetRotation(FQuat::MakeFromEuler(Direction()));
				AServerCharacter* RetActor = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::BeginDeferredActorSpawnFromClass(ActorClass, SpawnTransform));
				if (RetActor)
				{
					this->BindActorToEntity(RetActor);
				}
			}
		}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_OTHER_ENTITY, Position() );
	}
	if (DetectParentTimerHandle.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DetectParentTimerHandle);
		}
	}
}

void NPCBaseObject::OnBindActorToEntity()
{
	Supper::OnBindActorToEntity();

	//更新任务相关Entity可见性
	UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Actor());
	//更新周围SpellBox交互状态 JIRA CST-3631
	URoleTalkInterface * talkInterface = Cast<URoleTalkInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTalkInterface")));
	if (talkInterface)
	{
		talkInterface->RefreshAroundBoxStatus(int32(SPELL_BOX_LISTEN_EVENT::EVENT_HAS_ENTITY));
	}

	UNPCBaseObjectInterface * Interface = Cast<UNPCBaseObjectInterface>(Interface_Cache.GameObjectInterface);
	if (IsValid(Interface))
	{
		UGolbalBPFunctionLibrary::SetActorAndCompVisibility(Actor(), UPrimitiveComponent::StaticClass());
		AServerCharacter* MyCharacter = Cast<AServerCharacter>(Actor());
		Interface->PlayBeforeSpawnEffect(MyCharacter);
	}
}