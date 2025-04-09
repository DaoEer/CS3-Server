// Fill out your copyright notice in the Description page of Project Settings.

#include "Actor/ServerCharacter.h"
#include "CS3Base/CS3Entity.h"
#include "CS3Base/GameObject.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Components/WidgetComponent.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Interface/SkillInterface.h"
#include "Interface/GameObjectInterface.h"
#include "GameData/FootprintData.h"
#include "Manager/ForceManager.h"
#include "GameData/CollideData.h"
#include "Component/DumbFilterActorComponent.h"
#include "Player/PlayerCharacter.h"
#include "Kismet/KismetMaterialLibrary.h"
#include "Component/AvatarFilterActorComponent.h"
#include "Component/RoleFilterActorComponent.h"
#include "Component/Role/FlyPatrolComponent.h"
#include "Manager/GameStatus.h"
#include "Component/FightComponent.h"
#include "Component/FilterActorComponent.h"
#include "GameCharacter.h"
#include "Component/CollisionComponent.h"
#include "Component/AppearanceComponent.h"
#include "Actor/Pet/RiderCharacter.h"
#include "Manager/ParticleManager.h"
#include "Manager/AudioManager.h"
#include "Manager/CfgManager.h"
#include "Manager/VisibleManager.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/CustomTimerManager.h"
#include "Interface/Monster/MonsterInterface.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/CapsuleComponent.h"
#include "Interface/StateInterface.h"
#include "GameData/GameDeFine.h"
#include "Manager/MotionBlurManager.h"
#include "GameData/ConstData.h"
CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("FloorTrace"), STAT_FloorTrace, STATGROUP_AServerCharacter);

#pragma region	Avatar功能相关

void AServerCharacter::OnGotParentEntity()
{
	if (IsValid(GetFilterComponent()) && GetSelfEntity() != nullptr)
	{
		GetFilterComponent()->OnGotParentEntity(GetSelfEntity()->Parent());
	}
}

void AServerCharacter::OnLoseParentEntity()
{
	if (IsValid(GetFilterComponent()))
	{
		GetFilterComponent()->OnLoseParentEntity();
	}
}

void AServerCharacter::InitFilterActorComponent()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::InitFilterActorComponent Entity %d"), EntityId);

	SetFilterComponent(NewObject<UDumbFilterActorComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr));

	GetFilterComponent()->RegisterComponent();
	GetFilterComponent()->InitFilter(false);
}

void AServerCharacter::OnPlayDeadActionOver(ACharacter *GameCharacter, FACTION_DATA InActionData)
{
	//死亡动作播放完成广播
	if (OnDeadActionPlayOver.IsBound())
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("AServerCharacter::OnPlayDeadActionOver EntityID[%d]"), EntityId);
		OnDeadActionPlayOver.Broadcast();
	}
}

void AServerCharacter::OnFilterSpeedChanged(float speed)
{
	FilterSpeed = speed;
}

void AServerCharacter::SetEnableSyncServerPos(bool IsEnable)
{
	KBEngine::Entity* Entity = this->GetSelfEntity();
	if (Entity == nullptr) return;
	GameObject* SelfEntity = (GameObject*)Entity;
	if (SelfEntity == nullptr) return;
	if (IsEnable)
	{
		SelfEntity->OpenSyncServerPos();
	} 
	else
	{
		SelfEntity->CloseSyncServerPos();
	}
}

void AServerCharacter::SetPosition(const FVector& newVal, int32 parentID /*= 0*/)
{
	if (IsValid(GetFilterComponent()))
	{
		GetFilterComponent()->SetPosition(newVal, parentID);
		UpdateOtherCptPosition();
	}
}

void AServerCharacter::SetDirection(const FVector& newVal, int32 parentID /*= 0*/)
{
	if (IsValid(GetFilterComponent()))
	{
		GetFilterComponent()->SetDirection(newVal, parentID);
	}
}

void AServerCharacter::onUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID /*= 0*/)
{
	if (IsValid(GetFilterComponent()))
	{
		GetFilterComponent()->OnUpdateVolatileData(position, direction, parentID);

		UpdateOtherCptPosition();
	}
}

void AServerCharacter::OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID /*= 0*/)
{
	if (IsValid(GetFilterComponent()) && GetSelfEntity() != nullptr)
	{
		GetFilterComponent()->OnUpdateVolatileDataByParent(position,direction,parentID);
	}
}

#pragma endregion

void AServerCharacter::SetGameCharacterTickInterval(float TickInterval)
{
	Super::SetGameCharacterTickInterval(TickInterval);
	if (MFilterComponent)
	{
		MFilterComponent->SetComponentTickInterval(TickInterval);
	}
}

AServerCharacter::AServerCharacter()
{
	SetSeverCharacterStatus( CS3SeverCharacterStatus::ActorSpawn);
	PrimaryActorTick.bCanEverTick = true;
	CharacterClassName = TEXT("ServerCharacter");
	m_EffectSlotName.Empty();
	m_EffectScale = -1.0f;
	m_RageLinearColor = FLinearColor(0.0f, 0.0f, 0.0f, 0.0f);
	bRageState = false;
	WeaponBindObjData.Empty();
}

void AServerCharacter::BeginPlay()
{
	// 更新碰撞
	CollisionComponent->InitCollision();

	Super::BeginPlay();

	///检查是否动态创建【玩家的】部件组件,因为beginplay的时候才能取到modelNumber进行判断
	if (nullptr != GetSelfEntity())
	{
		FString ModelNumber = (FString)GetSelfEntity()->GetDefinedProperty(TEXT("modelNumber"));
		CheckCreateDynamicPartCpt(ModelNumber);
	}

	OnActorCreateFinish.AddDynamic(this, &AServerCharacter::OnActorCreaterFinish);
	SetMaxWalkSpeed(GetMoveSpeed()*100.0f);
}

void AServerCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (nullptr != GetSelfEntity())
	{
		CS3_Display(CS3DebugType::CL_Actor,TEXT("AServerCharacter::EndPlay EntityID[%d]"), BindEntity->ID());
		//在自己被移除时，检查Entity在不在，如果存在，则将其绑定的Actor设为NULL。
		GetSelfEntity()->Actor(nullptr);
	}

	m_UpForceArr.Empty();
	EntityId = 0;
	Super::EndPlay(EndPlayReason);
}

void AServerCharacter::BeginDestroy()
{
	Super::BeginDestroy();
}

void AServerCharacter::SetInitialized(bool Initialized)
{
	bInitialized = Initialized;
	if (Initialized == true)
	{
		OnInitialized();
	}
}

void AServerCharacter::OnInitialized()
{
	KBEngine::Entity* Entity = GetSelfEntity();
	USkillInterface* SkillInterface = GetEntityInterface_Cache().SkillInterface;
	if (IsValid(SkillInterface) && Entity != nullptr)
	{
		SkillInterface->OnActorCreaterFinish();
	}
	CollisionComponent->SetPlayerCollisionByNormal();
	CollisionComponent->UpdateModelCollision();
}

void AServerCharacter::CreateAppearance()
{
	if (KBEngine::Entity* Entity = this->GetSelfEntity())
	{
		CS3_Log(TEXT("AServerCharacter::CreateAppearance Begin EntityID[%d],"), EntityId);
		Super::CreateAppearance();
		bIsChangeAppearanceling = true;
		FString modelNumber = (FString)Entity->GetDefinedProperty(TEXT("modelNumber"));
		FString newValue = (FString)Entity->GetDefinedProperty(TEXT("extraModelNumber"));
		if (!newValue.IsEmpty())
		{
			modelNumber = newValue;
		}
		GetAppearanceComponent()->CreateAppearance(modelNumber);
	}
	else
	{
		CS3_Log(TEXT("AServerCharacter::CreateAppearance Begin  Entity[%d] Is Null"), EntityId);
	}
}

void AServerCharacter::OnCreateModelOver()
{
	if (GetSelfEntity())
	{
		Super::OnCreateModelOver();
		UpdateOtherCptPosition();//CST-12215
	}
}

void AServerCharacter::OnCreateApperanceOver()
{
	SetSeverCharacterStatus(CS3SeverCharacterStatus::AppearanceCreateFinished);
	
	if (GetSelfEntity())
	{
		CS3_Log(TEXT("AServerCharacter::CreateAppearance End EntityID[%d],"), EntityId);
		Super::OnCreateApperanceOver();
		GameObject* entity = (GameObject*)GetSelfEntity();
		if (entity)
		{
			entity->OnActorCreateApperanceFinished();
		}
		if (bRageState)
		{
			OnShowRageEffect(m_RageLinearColor);
		}

		UpdateCapsuleComponent();
	}
	else
	{
		CS3_Log(TEXT("AServerCharacter::CreateAppearance End  Entity[%d] Is Null"), EntityId);
	}
	
}

void AServerCharacter::OnChangePartOver()
{
	Super::OnChangePartOver();
	if (bRageState)
	{
		OnShowRageEffect(m_RageLinearColor);
	}
}

void AServerCharacter::OnUnBindActorCallBack()
{
	CS3_Log(TEXT("AServerCharacter::OnUnBindToEntity EntityID[%d],"), EntityId);
	//通知去除选中
	APlayerCharacter* PlayerCharacter = (APlayerCharacter*)UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(PlayerCharacter))
	{
		if (PlayerCharacter->CurPlayerTarget == this)
		{
			PlayerCharacter->ClearTargetActor();
		}
	}
	UnBindActorToEntityBP();
}

void AServerCharacter::BindLinkEntity(KBEngine::Entity* Entity)
{
	if (Entity != nullptr)
	{
		SetSeverCharacterStatus(CS3SeverCharacterStatus::BindedEntity);
		CS3_Log(TEXT("AServerCharacter::BindLinkEntityID EntityID[%d],"), Entity->ID());

		EntityId = Entity->ID();
		BindEntity = Entity;
	}
	else
	{
		SetSeverCharacterStatus(CS3SeverCharacterStatus::UnBindedEntity);
		CS3_Log(TEXT("AServerCharacter::UnBindLinkEntityID EntityID[%d],"), EntityId);

		EntityId = 0;
		BindEntity = nullptr;
	}
}

void AServerCharacter::OnBindToEntity()
{
	CS3_Log(TEXT("AServerCharacter::OnBindToEntity EntityID[%d],"), EntityId);
#if WITH_EDITOR
	SetActorLabel(GetFName().ToString() + FString("(") + FString::FromInt(EntityId) + FString(")"));
#endif
	SetSeverCharacterStatus(CS3SeverCharacterStatus::ComponentCreateFinished);
	InitCharacterPosAndDirection();//需先初始化位置和朝向再InitCharacterComponent
	InitCharacterComponent();

	BindActorToEntityBP();
	
}

void AServerCharacter::InitCharacterPosAndDirection()
{
	GameObject* TempGameObject = (GameObject*)GetSelfEntity();
	if (TempGameObject == nullptr) return;
	FVector Pos = TempGameObject->GetServerSetPos();
	if (!IsMoveFlying())
	{
		Pos = FloorTrace(Pos);
	}

	FVector NewPos = GetModelScaleRevisePos(Pos);
	SetActorLocationAndRotation(NewPos, FQuat::MakeFromEuler(TempGameObject->Direction()));
}

void AServerCharacter::UpdateActorPositionToGround()
{
	//下落中(//(CST-8737)处理模型加载完毕后，在空中则不要设置位置，会导致直接将玩家拉到地面而没有下落过程)
	if (!IsMoveFlying())
	{
		FVector Pos = GetGroundPosition();
		SetActorLocation(Pos);
	}
}

FVector AServerCharacter::GetGroundPositionByEntity()
{
	KBEngine::Entity* SelfEntity = GetSelfEntity();
	if (SelfEntity == nullptr)
	{
		return FVector::ZeroVector;
	}
	FVector Pos = SelfEntity->Position();
	if (IsMoveFlying())
	{
		return Pos;//飞行状态直接返回entity的位置
	}
	return FloorTrace(Pos);
}

FVector AServerCharacter::GetGroundPosition()
{
	KBEngine::Entity* SelfEntity = GetSelfEntity();
	if (SelfEntity == nullptr)
	{
		return GetActorLocation();
	}
	FVector Pos = SelfEntity->Position();
	if (IsMoveFlying())
	{
		return Pos;//飞行状态直接返回entity的位置
	}
	Pos.Z = GetActorLocation().Z;
	return FloorTrace(Pos);
}

void AServerCharacter::InitCharacterComponent()
{
	InitFilterActorComponent();
}


KBEngine::Entity* AServerCharacter::GetSelfEntity() const
{
	if (UUECS3GameInstance::pKBEApp == nullptr) return nullptr;
	return BindEntity;
}

FVector AServerCharacter::FloorTrace(const FVector &Vector, bool bForce/* = false */)
{
	SCOPE_CYCLE_COUNTER(STAT_FloorTrace);
	// 修正高度，一般是胶囊体的一半的高度
	float AdjustedZ = GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight() * GetActorScale3D().Z;
	
	float WorldTimeSeconds = GetWorld()->TimeSeconds;
	//缓存结果保留一段时间才重新查询(短时间内对象不会移动太多,地面高度改变大部分情况都不大,影响效果的话就缩短保留时间)  (由于还是有落差过大导致抖动,将缓存时间设为0.00f)
	if (!bForce && NowGroundLocation.time > 0.f && 
		(WorldTimeSeconds == NowGroundLocation.time || (WorldTimeSeconds - NowGroundLocation.time < 0.00f && (Vector - NowGroundLocation.time).Size2D() <= 50.0f) && (Vector.Z - NowGroundLocation.location_Z) <= 2 * AdjustedZ))
	{
		return FVector(Vector.X, Vector.Y, NowGroundLocation.location_Z + AdjustedZ);
	}

	FVector newPos(Vector);
	FHitResult HitOut(ForceInit);
	static FName TraceTag = FName(TEXT("ComputeFloorDistSweep"));
	FCollisionQueryParams TraceParams = FCollisionQueryParams(TraceTag, true, this);
	TraceParams.bTraceComplex = false;
	//TraceParams.bTraceAsyncScene = false;

	TraceParams.bReturnPhysicalMaterial = false;
	TraceParams.bIgnoreTouches = true;

	if (bDestroy)
	{
		return Vector;
	}

	// 开始进行测试地板
	if (this->GetWorld()->LineTraceSingleByChannel(HitOut, newPos + FVector(0.0f, 0.0f, 200.0f),
		newPos + FVector(0.0f, 0.0f, -10000.0f), ECC_GameTraceChannel10, TraceParams))
	{
		//DrawDebugLine(GetWorld(), newPos + FVector(0.0f, 0.0f, 200.0f), newPos + FVector(0.0f, 0.0f, -10000.0f), FColor::Red, false, 5.0f);

		//CST-7068 怪物移动出平台，用射线碰撞检测不标准。可能会碰撞到客户端的actor
		/*AServerCharacter* Actor = Cast<AServerCharacter>(HitOut.GetActor());
		KBEngine::Entity* SelfEntity = GetSelfEntity();
		if (SelfEntity && Cast<AMonsterCharacter>(SelfEntity->Actor()) && SelfEntity->ParentID() > 0 && (!Actor || (Actor->GetSelfEntity() && Actor->GetSelfEntity()->ID() != SelfEntity->ParentID())))
		{
			KBEngine::FVariantArray Args;
			Args.Add(SelfEntity->ID());
			if (Actor)
			{
				Args.Add(Actor->GetSelfEntity()->ID());
			}
			else
			{
				Args.Add(0);
			}			
			UMonsterInterface* MInterface = Cast<UMonsterInterface>(GetEntityInterface_Cache().GameObjectInterface);
			if (IsValid(MInterface))
			{
				MInterface->RPC_CELL_ChangeMonsterParent(Args);
			}
		}*/
		newPos.Z = HitOut.Location.Z + AdjustedZ;
	}

	NowGroundLocation.time = WorldTimeSeconds;
	NowGroundLocation.location_Z = HitOut.Location.Z;

	//CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::FloorTrace Entity %d--------------collison Pos:%f,%f,%f"),EntityId, newPos.X, newPos.Y, newPos.Z);
	return newPos;
}

void AServerCharacter::SetCharacterMovePosition(const float& MoveDistance, const FVector& TargetLocation, bool bAbsolute/* = true */, bool bSweep/* = false */)
{
	Entity* SelfEntity = GetSelfEntity();
	if (SelfEntity == nullptr) return;
	FVector DstPos;
	if (!bAbsolute && SelfEntity->Parent())// 根据是不是在移动平台上判断，落下的位置
	{
		FVector Pos = SelfEntity->Parent()->PositionWorldToLocal(GetActorLocation());
		Pos += MoveDistance * (TargetLocation - Pos).GetSafeNormal();
		DstPos = SelfEntity->Parent()->PositionLocalToWorld(Pos);
	}
	else
	{
		FVector Pos = GetActorLocation();
		DstPos = MoveDistance * (TargetLocation - Pos).GetSafeNormal() + Pos;
	}

	if (!IsMoveFlying())
	{
		DstPos = FloorTrace(DstPos);
	}
	SetActorLocation(DstPos, bSweep);
}

FVector AServerCharacter::GetModelScaleRevisePos(const FVector &OriginalPosition)
{
	auto SelfEntity = GetSelfEntity();
	if (SelfEntity != nullptr)
	{
		float ModelScale = SelfEntity->GetDefinedProperty(TEXT("modelScale")).GetValue<float>();
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------------------AServerCharacter::GetModelScaleRevisePos:ModelScale:%f"), ModelScale);
		float DisScale = ModelScale - 1.0;
		float DisHeight = DisScale * GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight();
		return OriginalPosition + FVector(0.0, 0.0, DisHeight);
	} 
	else
	{
		return OriginalPosition;
	}
	
}

void AServerCharacter::ShowInvisible()
{
	if (bHidden)
	{
		UGolbalBPFunctionLibrary::SetActorAndCompVisibility(this, UPrimitiveComponent::StaticClass(), true, true);
	}
	bIsShowInvisible = true;
}

void AServerCharacter::HideInvisible()
{
	if (!bHidden)
	{
		UGolbalBPFunctionLibrary::SetActorAndCompVisibility(this, UPrimitiveComponent::StaticClass());
		ClearTargetActor();
	}
	bIsShowInvisible = false;
}

void AServerCharacter::OnEnterDeadState()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::OnEnterDeadState EntityID[%d]"), EntityId);
	bDeadState = true;
	if (IsValid(GetBaseAnimInstance()))
	{
		FActionOverDelegate ActionOverDelegate;
		ActionOverDelegate.AddUObject(this, &AServerCharacter::OnPlayDeadActionOver);
		GetBaseAnimInstance()->PlayDeadAction(ActionOverDelegate);
	}
}

void AServerCharacter::OnExitDeadState()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::OnExitDeadState EntityID[%d]"), EntityId);
	bDeadState = false;
}

void AServerCharacter::OnEnterFreeState()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::OnEnterFreeState EntityID[%d]"), EntityId);
	if (IsValid(GetBaseAnimInstance()))
	{
		APlayerCharacter* Player = Cast<APlayerCharacter>(this);
		if (IsValid(Player) && IsValid(Player->FlyPatrolComponent) && Player->FlyPatrolComponent->IsFlyPatrolState())
		{
			return;
		}
		
		if (IsActiveMoveing())
		{
			GetBaseAnimInstance()->PlayMoveAction();
		}
		else
		{
			GetBaseAnimInstance()->PlayStandbyAction();
		}
	}
}

void AServerCharacter::OnEnterWarnState()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::OnEnterWarnState EntityID[%d]"), EntityId);
	if (IsValid(GetBaseAnimInstance()))
	{
		APlayerCharacter* Player = Cast<APlayerCharacter>(this);
		if (IsValid(Player) && IsValid(Player->FlyPatrolComponent) && Player->FlyPatrolComponent->IsFlyPatrolState())
		{
			return;
		}

		if (IsActiveMoveing())
		{
			GetBaseAnimInstance()->PlayMoveAction();
		}
		else
		{
			GetBaseAnimInstance()->PlayStandbyAction();
		}
	}
}

void AServerCharacter::OnEnterFightState()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::OnEnterFightState EntityID[%d]"), EntityId);
	GetFightComponent()->EnterFightState();
	RemoveOnActorCreaterFinishBind();
}

void AServerCharacter::OnExitFightState()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::OnExitFightState EntityID[%d]"), EntityId);
	GetFightComponent()->OnExitFightState.Broadcast();
}

void AServerCharacter::OnEnterEffectState(EFFECT_STATE EffectState)
{
	switch (EffectState)
	{
	case EFFECT_STATE::EFFECT_STATE_DIZZY:
	{
		if (GetBaseAnimInstance())
		{
			GetBaseAnimInstance()->PlayDizzyAction();
		}
	}
	break;
	case EFFECT_STATE::EFFECT_STATE_UNCONTROLLABLE:
		break;
	case EFFECT_STATE::EFFECT_STATE_INVINCIBLE:
		break;
	case EFFECT_STATE::EFFECT_STATE_HIT_BACK:
	{
		APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(this);
		if (IsValid(PlayerActor))//是玩家就对其做一些操作
		{
			//数值越大优先级越低，当当前的状态比击退低，就将受效果影响状态给予玩家（此状态只为控制玩家旋转用）
			if (PlayerActor->EPlayerInteractiveState >= APLAYER_INTERACTIVE_ENUM::APLAYER_TALKTONPC)
			{
				//设置玩家的旋转不受movement组件影响
				PlayerActor->SetOrientRotationToMovement(false, false);
				OrientRotationCount++;
			}
		}
	}
	break;
	case EFFECT_STATE::EFFECT_STATE_FIX:
		break;
	case EFFECT_STATE::EFFECT_STATE_SLEEP:
	{
		if (GetBaseAnimInstance())
		{
			GetBaseAnimInstance()->PlaySleepAction();
		}
	}
	break;
	case EFFECT_STATE::EFFECT_STATE_PROTECT:
		break;
	case EFFECT_STATE::EFFECT_STATE_STORY:
	{
		APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(this);
		if (IsValid(PlayerActor))//是玩家就对其做一些操作
		{
			PlayerActor->OnEnterEffectStoryState();
		}
	}
		break;
	default:
		break;
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::OnEnterEffectState EntityID[%d] EnterEffectState=%d"), EntityId, EffectState);
}

void AServerCharacter::OnExitEffectState(EFFECT_STATE EffectState)
{
	switch (EffectState)
	{
	case EFFECT_STATE::EFFECT_STATE_DIZZY:
	{
		if (IsValid(GetBaseAnimInstance()))
		{
			GetBaseAnimInstance()->StopActionByType(ACTION_TYPE_ENUM::ACTION_TYPE_DIZZY);
		}
	}
	break;
	case EFFECT_STATE::EFFECT_STATE_UNCONTROLLABLE:
		break;
	case EFFECT_STATE::EFFECT_STATE_INVINCIBLE:
		break;
	case EFFECT_STATE::EFFECT_STATE_HIT_BACK:
	{
		//转换为玩家
		APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(this);
		if (IsValid(PlayerActor))//是玩家就对其做一些操作
		{
			//设置旋转切换
			PlayerActor->SetOrientRotationToMovement(false, false, OrientRotationCount, true);
			OrientRotationCount = 0;
		}
	}
	break;
	case EFFECT_STATE::EFFECT_STATE_FIX:
		break;
	case EFFECT_STATE::EFFECT_STATE_SLEEP:
	{
		if (IsValid(GetBaseAnimInstance()))
		{
			GetBaseAnimInstance()->StopActionByType(ACTION_TYPE_ENUM::ACTION_TYPE_SLEEP);
		}
	}
	break;
	case EFFECT_STATE::EFFECT_STATE_PROTECT:
		break;
	case EFFECT_STATE::EFFECT_STATE_FREEZE:
	{
		if (bDeadState)
		{
			if (IsValid(GetBaseAnimInstance()))
			{
				FActionOverDelegate ActionOverDelegate;
				ActionOverDelegate.AddUObject(this, &AServerCharacter::OnPlayDeadActionOver);
				GetBaseAnimInstance()->PlayDeadAction(ActionOverDelegate);
			}
		}
	}
	break;
	case EFFECT_STATE::EFFECT_STATE_STORY:
	{
		APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(this);
		if (IsValid(PlayerActor))//是玩家就对其做一些操作
		{
			PlayerActor->OnExitEffectStoryState();
		}
	}
	default:
		break;
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::OnExitEffectState EntityID[%d] ExitEffectState=%d"), EntityId, EffectState);

}

void AServerCharacter::PlayDeadMortuaryEffect()
{
	PlayDeadMortuaryEffectBP();
// 	KBEngine::Entity* Entity = GetSelfEntity();
// 	if (Entity == nullptr)
// 	{
// 		CS3_Warning(TEXT("-->Null Pointer error:AMonsterCharacter::PlayDeadEffect : Entity!"));
// 		return;
// 	}
// 	FString ScriptID = Entity->GetDefinedProperty(TEXT("scriptID"));
// 	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
// 	const FMONSTER_DATA* ModelData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MONSTER)->GetRow<FMONSTER_DATA>(ScriptID);
// 	if (ModelData && !ModelData->DeadEffectId.IsEmpty())
// 	{
// 		bIsPlayDeadEffect = true;
// 		UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(this);
// 		
// 		UMotionBlurManager::GetInstance()->CreateBlurMeshes(GetMesh(), FSTRING_TO_FLOAT(ModelData->DeadEffectId));
// 	}
}

FString AServerCharacter::GetUname()
{
	return GetEntityUName();
}

bool AServerCharacter::IsMoveing()
{
	if (bIsClient)
	{
		return ClientFilterSpeed > 0.0f ? true : false;
	}
	else if (ActorIsPlayer())
	{
		FVector CharacterVelocity = GetVelocity();
		CharacterVelocity.Z = 0;
		return CharacterVelocity.Size() > 0.0f ? true : false;
	}
	return GetFilterSpeed() > 0.0f ? true : false;
}

bool AServerCharacter::IsActiveMoveing()
{
	return IsMoveing();
}

bool AServerCharacter::IsMoveFlying()
{
	UCharacterMovementComponent* MovementComponent = GetCharacterMovement();
	if (!IsValid(MovementComponent) || MovementComponent->MovementMode == MOVE_Flying 
		|| MovementComponent->MovementMode == MOVE_Falling || IsLadderMovement() || HasFlag(ENTITY_FLAG::FLAG_CAN_FLY))
	{
		return true;
	}
	return false;
}

float AServerCharacter::GetFilterSpeed()
{
	if (IsValid(UUECS3GameInstance::Instance) && UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() <= EGameStatus::Teleport)
	{
		return 0.0f;
	}
	if (KBEngine::Entity* Entity = GetSelfEntity())
	{
		if (IsMoveType(MOVETYPE::MOVETYPE_CHASE) && !((GameObject*)Entity)->IsSyncServerPos())
		{
			return GetCharacterMovement()->MaxWalkSpeed;
		}
		
		return FilterSpeed;
	}
	return 0.0f;
}

int32 AServerCharacter::GetFinalCamp()
{
	return 0;
}

bool AServerCharacter::HasFlag(ENTITY_FLAG EntityFlag)
{
	KBEngine::Entity* Entity = GetSelfEntity();
	if (Entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AServerCharacter::HasFlag : Entity!"));
		return false;
	}
	UGameObjectInterface* interface_ = GetEntityInterface_Cache().GameObjectInterface;
	if (!IsValid(interface_))
	{
		CS3_Warning(TEXT("-->Null Pointer error:AServerCharacter::HasFlag : interface_!"));
		return false;
	}


	int64 Flags = Entity->GetDefinedProperty(TEXT("flags")).GetValue<int64>();
	int64 Flag = int64(1) << int64(EntityFlag);
	return (Flags & Flag) == Flag;
}

bool AServerCharacter::IsMoveType(MOVETYPE MoveType)
{
	return IsEntityMoveType(MoveType);
}

bool AServerCharacter::IsBoss()
{
	return IsEntityBoss();
}

bool AServerCharacter::IsState(ENTITY_STATE EntityState)
{
	if (GetSelfEntity() != nullptr)
	{
		GameObject* GameEntity = (GameObject*)GetSelfEntity();
		return GameEntity->IsState(EntityState);
	}
	return false;
}

bool AServerCharacter::IsInPending()
{
	if (GetSelfEntity() == nullptr)	return false;
	int32 bIsInPending = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetSelfEntity()->ID(), TEXT("isInPending"));
	return bIsInPending > 0;
}

bool AServerCharacter::IsChangeModelState()
{
	KBEngine::Entity* SelfEntity = GetSelfEntity();
	FString newValue = "";
	if (SelfEntity)
	{
		newValue = (FString)SelfEntity->GetDefinedProperty(TEXT("extraModelNumber"));
	}
	return !newValue.IsEmpty();
}


bool AServerCharacter::ActorIsPlayer()
{
	return EntityId == UGolbalBPFunctionLibrary::GetPlayerID();
}

COMBAT_RELATION AServerCharacter::QueryRelation(AActor* Actor)
{
	///判断自己
	KBEngine::Entity* SelfEntity = this->GetSelfEntity();
	if (SelfEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AServerCharacter::QueryRelation : SelfEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NONE;
	}
	GameObject* _selfEntity = (GameObject*)SelfEntity;

	///判断目标
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
	if (!IsValid(ServerCharacter))
	{
		return COMBAT_RELATION::COMBAT_RELATION_NONE;
	}
	KBEngine::Entity* TargetEntity = ServerCharacter->GetSelfEntity();
	if (TargetEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AServerCharacter::QueryRelation : TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NONE;
	}

	///转到entity判断关系
	return _selfEntity->QueryRelation(TargetEntity);
}

void AServerCharacter::UpdateRelation_Implementation()
{
	CollisionComponent->UpdateModelCollision();

	UStateInterface* StateInterface = GetEntityInterface_Cache().StateInterface;
	if (IsValid(StateInterface) && StateInterface->HasEffectState(EFFECT_STATE::EFFECT_STATE_HIDE))
	{
		UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(this);
	}
}

void AServerCharacter::SetEffectDynamicData(FString SlotName, float EffectScale, FVector pos)
{
	m_EffectSlotName = SlotName;
	m_EffectScale = EffectScale;
	m_EffectLoction = pos * 100.0f;
}

void AServerCharacter::GetEffectDynamicData(FString SlotName, FTransform EffectTrans)
{
	if (!m_EffectSlotName.IsEmpty())
	{
		SlotName = m_EffectSlotName;
		m_EffectSlotName.Empty();
	}

	if (m_EffectScale > 0.0f)
	{
		EffectTrans.SetScale3D(FVector(m_EffectScale, m_EffectScale, m_EffectScale));
		m_EffectScale = -1.0f;
	}

	FVector ChangePos = EffectTrans.GetLocation();
	ChangePos += m_EffectLoction;
	EffectTrans.SetLocation(ChangePos);
}

void AServerCharacter::OnActorCreaterFinish_Implementation()
{
	if (IsState(ENTITY_STATE::EntityStateFight))
	{
		GetFightComponent()->EnterFightState();
	}
	
	/*
	//在外观加载完毕函数有设置缩放UAppearanceComponent::ApplayModelByPartsMap，这里应该是重复设置模型缩放
	//此处注释者：ranyuan
	KBEngine::Entity* Entity = GetSelfEntity();
	UGameObjectInterface* GameObjectInterface = GetEntityInterface_Cache().GameObjectInterface;
	if (IsValid(GameObjectInterface) && Entity != nullptr)
	{
		GameObjectInterface->SetModelScale(Entity->GetDefinedProperty(TEXT("modelScale")).GetValue<float>());
	}
	*/
}

void AServerCharacter::RemoveOnActorCreaterFinishBind()
{
	if (OnActorCreateFinish.IsAlreadyBound(this, &AServerCharacter::OnActorCreaterFinish))
	{
		OnActorCreateFinish.RemoveDynamic(this, &AServerCharacter::OnActorCreaterFinish);
	}
}

bool AServerCharacter::CanGossipWith_Implementation()
{
	return false;
}

FString AServerCharacter::GetEntityUName()
{
	return TEXT("");
}

bool AServerCharacter::IsEntityMoveType(MOVETYPE MoveType)
{
	return false;
}

bool AServerCharacter::IsEntityBoss()
{
	return false;
}

void AServerCharacter::InitBaseComponent()
{

}

UMaterialInstance* AServerCharacter::GetFootPrintData(TEnumAsByte<EPhysicalSurface> SurfaceType , FString EntityName,bool LeftORRight)
{	
	auto FootTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_FOOT_PRINT_DATA);
	TArray<FName> Rows = FootTable->GetRowNames();
	for (FName _Row : Rows)
	{
		const FFOOT_PRINT_DATA* _FootTable = FootTable->GetRow<FFOOT_PRINT_DATA>(_Row);	
		if (_FootTable->SurfaceType == SurfaceType && _FootTable->EntityName == EntityName)
		{
			UUECS3GameInstance::Instance->AudioManager->AsyncPlay3DSound(this, _FootTable->FootPrintMusicID);
			UUECS3GameInstance::Instance->ParticleManager->PlayParticle(_FootTable->ParticleSystemID, 0.0f, this, this);
			if (LeftORRight)
			{
				return _FootTable->LeftFootMaterialName;
			}
			else
			{
				return _FootTable->RigthFootMaterialName;
			}
		}
	}
	return nullptr;
}

void AServerCharacter::OpenUpForce(const float& speed)
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	if (IsValid(ForceMana))
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::CloseUpForce EntityID[%d] speed=%d"), EntityId, speed);
		int32 ForceID = ForceMana->AddForce(this, speed, FVector::UpVector);
		m_UpForceArr.Add(ForceID);
	}
	else
	{
		CS3_Warning(TEXT("AServerCharacter::OpenUpForce-- UForceManager Is Null!"));
	}

}

void AServerCharacter::CloseUpForce()
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	if (IsValid(ForceMana))
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::CloseUpForce EntityID[%d] "), EntityId);
		ForceMana->StopAllForces(this, m_UpForceArr);
	}
	else
	{
		CS3_Warning(TEXT("AServerCharacter::CloseUpForce-- UForceManager Is Null!"));
	}
}

void AServerCharacter::SetCustomDepthStncilValue(CUSTOM_DEPTH_STENCIL StancilValue)
{
	int32 value = (int32)StancilValue;
	for (auto It = MeshPartComponentDatas.CreateConstIterator(); It; ++It)
	{
		It.Value()->SetCustomDepthStencilValue(value);
	}
}

FEntityInterface_Cache& AServerCharacter::GetEntityInterface_Cache()
{
	// 目前所有AServerCharacter绑定的entity都一定是CS3Entity,所以这里直接强转
	static FEntityInterface_Cache empty = FEntityInterface_Cache();
	return GetSelfEntity() ? ((CS3Entity*)GetSelfEntity())->Interface_Cache : empty;
}

UCS3EntityInterface * AServerCharacter::GetInterfaceByName(const FString& name)
{
	return GetSelfEntity() ? ((CS3Entity*)GetSelfEntity())->GetInterfaceByName(name) : nullptr;
}

FString AServerCharacter::GetEntityPropertyValue(const FString& pName)
{
	return GetSelfEntity() ? GetSelfEntity()->GetDefinedProperty(pName): TEXT("");
}

void AServerCharacter::OnShowRageEffect(FLinearColor &LinearColor)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::OnShowRageEffect EntityID[%d] "), EntityId);
	bRageState = true;
	m_RageLinearColor = LinearColor;
	AppearanceComponent->SetMaterialColor(LinearColor);
}

void AServerCharacter::OnEndRageEffect()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::OnEndRageEffect EntityID[%d] "), EntityId);
	bRageState = false;
	m_RageLinearColor = FLinearColor(0.0f, 0.0f, 0.0f, 0.0f);
	AppearanceComponent->SetMaterialColor(m_RageLinearColor);
}

void AServerCharacter::ChangeAnimAction(TSoftClassPtr<UAnimInstance> InAnimationPath, 
	TSoftObjectPtr<UDataTable> InActionConfigPath, 
	FName OutActionId /*= "None"*/, FName InActionId /*= "None"*/)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::ChangeAnimAction EntityID[%d] ActionConfigPath=[%s]"), EntityId, *InActionConfigPath.ToSoftObjectPath().GetAssetPathString());
	bIsChangeAppearanceling = true;
	//先播放出场动作,因为出场动作是在换表之前的动作表中
	if (IsValid(GetBaseAnimInstance()))
	{
		GetBaseAnimInstance()->PlayAction(OutActionId);
	}

	TWeakObjectPtr<AServerCharacter> DelayThisPtr(this);
	AppearanceComponent->ChangeAnimAction(InAnimationPath, InActionConfigPath, 
		FChangeAnimComplete::CreateLambda([DelayThisPtr, InActionId]()
		{
			if (DelayThisPtr.IsValid())
			{
				AServerCharacter* ThisPtr = DelayThisPtr.Get();
				if (!InActionId.IsNone() && ThisPtr->GetBaseAnimInstance())
				{
					//再播放入场动作
					ThisPtr->GetBaseAnimInstance()->PlayAction(InActionId);
				}
				ThisPtr->bIsChangeAppearanceling = false;
				ThisPtr->OnModelChangeAppearanceOverDelegate.Broadcast();
				ThisPtr->OnCreateApperanceOver();
			}
		}));
}

bool AServerCharacter::IsCanPlayAction()
{
	//冻结效果则不播放任何动作
	UStateInterface* StateInterface = GetEntityInterface_Cache().StateInterface;
	if (IsValid(StateInterface) && StateInterface->HasEffectState(EFFECT_STATE::EFFECT_STATE_FREEZE))
	{
		return false;
	}
	return true;
}

void AServerCharacter::BindObjToPartSlot(FPART_SLOT_BIND_OBJ_DATA &InWeaponBindObj)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" AServerCharacter::BindObjToPartSlot EntityID[%d]"), EntityId);
	WeaponBindObjData.Add(InWeaponBindObj);
	OnSkillWeaponBindObj.Broadcast();
}

void AServerCharacter::RemovePartSlotBindObj(int32 InBindId)
{
	for (int32 i = 0; i < WeaponBindObjData.Num(); i++)
	{
		FPART_SLOT_BIND_OBJ_DATA& ObjData = WeaponBindObjData[i];
		if (ObjData.Id != InBindId)
		{
			continue;
		}

		if (ObjData.BindObjType == PART_SLOT_BIND_OBJ_ENUM::PART_SLOT_BIND_OBJ_ACTOR)
		{
			ResetBindObjToPartSlot(ObjData);
			break;
		}
		else if (ObjData.BindObjType == PART_SLOT_BIND_OBJ_ENUM::PART_SLOT_BIND_OBJ_PARTICLE)
		{
			break;
		}
		//删除指定数据
		WeaponBindObjData.RemoveAt(i);
	}
}

void AServerCharacter::RemoveAllPartSlotBindObj()
{
	for (FPART_SLOT_BIND_OBJ_DATA& ObjData : WeaponBindObjData)
	{
		if (ObjData.BindObjType == PART_SLOT_BIND_OBJ_ENUM::PART_SLOT_BIND_OBJ_ACTOR)
		{
			ResetBindObjToPartSlot(ObjData);
		}
		else if (ObjData.BindObjType == PART_SLOT_BIND_OBJ_ENUM::PART_SLOT_BIND_OBJ_PARTICLE)
		{
			
		}
	}
	WeaponBindObjData.Empty();
}

void AServerCharacter::ResetBindObjToPartSlot(FPART_SLOT_BIND_OBJ_DATA &InWeaponBindObj)
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		return;
	}
	KBEngine::Entity* ByBindEntity = UUECS3GameInstance::pKBEApp->FindEntity(InWeaponBindObj.ByBindEntityID);
	AServerCharacter* ByBindActor = Cast<AServerCharacter>(ByBindEntity->Actor());
	//解绑设置朝向
	ByBindActor->DetachFromActor(FDetachmentTransformRules::KeepWorldTransform);
	ByBindActor->SetActorRotation(FRotator(0.f, ByBindActor->GetActorRotation().Yaw, 0.f));
	//更新碰撞
	ByBindActor->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);

	if (ByBindEntity->ClassName() == "Role")
	{
		ByBindActor->GetCharacterMovement()->SetMovementMode(EMovementMode::MOVE_Walking);
		//开启重力
		if (ByBindEntity->ID() == UGolbalBPFunctionLibrary::GetPlayerID())
		{
			ByBindActor->SetBaseGravityScale(5.0f);
		}
		else
		{
			ByBindActor->SetBaseGravityScale(1.0f);
		}
		//开启服务器位置同步
		URoleFilterActorComponent* FilterComp = Cast<URoleFilterActorComponent>(ByBindActor->GetFilterComponent());
		if (FilterComp)
		{
			//FilterComp->IsIgnoreServerPos = false;
		}

	}
	else
	{
		//开启服务器位置同步 
		UAvatarFilterActorComponent* FilterComp = Cast<UAvatarFilterActorComponent>(ByBindActor->GetFilterComponent());
		if (FilterComp)
		{
			//FilterComp->IsIgnoreServerPosValue = false;
		}
	}
}

void AServerCharacter::SetHeadInfo3DUIVisible()
{
	AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	float tempDistance;
	//头顶UI显示规则方法调用频繁写lambda比写函数好
	auto IsInYCJMD = []() {
		const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
		return SpaceScriptID.Equals("fu_ben_L_YCJMD_zhenyingPVP"); };
	auto Fun = [](AServerCharacter* InServerCharacter, float InDistance) {
		if (InDistance > YCJMD_HeadUIShowDist_Far)
		{
			InServerCharacter->HeadInfo3DUI->SetVisibility(false);
		}
		else
		{
			InServerCharacter->HeadInfo3DUI->SetVisibility(true);
			if (InDistance <= YCJMD_HeadUIShowDist_Near)
			{
				InServerCharacter->OnUpdateHeadInfo3DUIBP(false);
			} 
			else
			{
				InServerCharacter->OnUpdateHeadInfo3DUIBP(true);
			}
		} };
	if (IsValid(PlayerCharacter))
	{
		if (ActorIsPlayer()) 
		{
			///如果是本地客户端玩家，则所有的Entity都需要更新头顶信息UI
			TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
			for (auto& Elem : EntitiesMap)
			{

				KBEngine::Entity* Entity = Elem.Value;
				if (Entity != nullptr)
				{
					if (!Entity->Actor())
					{
						continue;
					}
					AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Entity->Actor());
					if (IsValid(ServerCharacter) && ServerCharacter->OpenScene3DUI && IsValid( ServerCharacter->HeadInfo3DUI))
					{
						tempDistance = UGolbalBPFunctionLibrary::GetActorDistance(PlayerCharacter, ServerCharacter);
						if (IsInYCJMD() && ServerCharacter->CharacterClassName.IsEqual(TEXT("PlayerCharacter")))//CST-13806 大荒战场
						{
							Fun(ServerCharacter, tempDistance);
						} 
						else
						{
							if (tempDistance <= ServerCharacter->HeadInfo3DUIShowDist)
							{
								ServerCharacter->HeadInfo3DUI->SetVisibility(true);
							}
							else
							{
								ServerCharacter->HeadInfo3DUI->SetVisibility(false);
							}
						}
					}
				}
			}
		}
		else
		{
			///如果不是本地客户端玩家，则只需要更新该Entity头顶信息UI
			if (OpenScene3DUI && HeadInfo3DUI)
			{
				tempDistance = UGolbalBPFunctionLibrary::GetActorDistance(PlayerCharacter, this);
				if (IsInYCJMD() && this->CharacterClassName.IsEqual(TEXT("PlayerCharacter")))//CST-13806 大荒战场
				{
					Fun(this, tempDistance);
				}
				else
				{
					if (tempDistance <= HeadInfo3DUIShowDist)
					{
						HeadInfo3DUI->SetVisibility(true);
					}
					else
					{
						HeadInfo3DUI->SetVisibility(false);
					}
				}
			}
		}
	}
}

FName AServerCharacter::GetWeaponSockName(bool IsLeft)
{
	bool IsFightShow = IsState(ENTITY_STATE::EntityStateFight) || IsState(ENTITY_STATE::EntityStateWarn);
	ROLE_PROFESSION_ENUM RoleProfession = (ROLE_PROFESSION_ENUM)ProfessionID;
	if (!IsFightShow && RoleProfession == ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_SHE_SHOU)
	{
		return IsLeft ? TEXT("Socket_Weapon_Whip_Spine_L") : TEXT("Socket_Weapon_Whip_Spine_R");
	}
	return IsLeft ? TEXT("Socket_Weapon_L") : TEXT("Socket_Weapon_R");
}

void AServerCharacter::UpdateOtherCptPosition()
{
	SetHeadInfo3DUIVisible();
}

CONTROL_COMPILE_OPTIMIZE_END
