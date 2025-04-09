// Fill out your copyright notice in the Description page of Project Settings.

#include "MonsterCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/CapsuleComponent.h"
#include "Interface/StateInterface.h"
#include "Component/FilterActorComponent.h"
#include "Component/PhysicsFilterActorComponent.h"
#include "Component/AvatarFilterActorComponent.h"
#include "Component/DumbFilterActorComponent.h"
#include "Component/LineToPointFilterActorComponent.h"
#include "Component/FightComponent.h"
#include "Component/AppearanceComponent.h"
#include "Util/ConvertUtil.h"
#include "Manager/VisibleManager.h"
#include "Manager/CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ParticleManager.h"
#include "Component/CollisionComponent.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Interface/GameObjectInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/GameDeFine.h"
#include "Component/Monster/MonsterPosSyncComponent.h"
#include "AIController.h"
#include "CS3Base/GameObject.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"
#include "Interface/SkillInterface.h"
#include "Interface/StateInterface.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "Manager/CustomCursorManager.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Manager/EventManager.h"
#include "Manager/CustomTimerManager.h"
#include "Interface/Monster/MonsterAppearInterface.h"
#include "Interface/Monster/MonsterInterface.h"
#include "Interface/Monster/MonsterExtInteractiveInterface.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Interface/Monster/MonsterExtSFMJInterface.h"
#include "Component/Monster/MonsterBlowFilterComponent.h"
#include "Component/Monster/MonsterFollowComponent.h"
#include "Component/Monster/CMonsterPosSyncComponent.h"
#include "Component/Monster/MonsterOptimizeComponent.h"
#include "Interface/Monster/MonsterExtQQRYJInterface.h"
#include "Entity/Monster/CMonster.h"
#include "Manager/GameStatus.h"
#include "CS3Base/CS3EntityInterface.h"
#include "MonsterAI/MonsterAIEnum.h"
#include "MonsterAI/MonsterCommonController.h"
#include "Interface/Monster/MonsterExtAerialLadderInterface.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/CharacterData.h"
#include "GameData/AppearanceStyle/BattlefieldAppearanceStyle.h"
#include "Kismet/KismetMathLibrary.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Interface/Monster/MonsterOptimizeInterface.h"
#include "Interface/Monster/MonsterCopyRoleModelInterface.h"
#include "Component/Monster/MonsterExtJDCYComponent.h"
#include "Manager/ModifyFaceManager.h"


CONTROL_COMPILE_OPTIMIZE_START

void AMonsterCharacter::InitFilterActorComponent()
{
	PhysicsFilter = NewObject<UPhysicsFilterActorComponent>(this, "root1", RF_NoFlags, nullptr, false, nullptr);
	CurveFilter = NewObject<UCurveFilterActorComponent>(this, "CurveFilter", RF_NoFlags, nullptr, false, nullptr);
	DumbFilter = NewObject<UDumbFilterActorComponent>(this, "DumbFilter", RF_NoFlags, nullptr, false, nullptr);
	LineToPointFilter = NewObject<ULineToPointFilterActorComponent>(this, "LineToPointFilter", RF_NoFlags, nullptr, false, nullptr);
	HitBackMoveFilter = NewObject<UHitBackMoveFilterActorComponent>(this, "HitBackFilter", RF_NoFlags, nullptr, false, nullptr);
	ResetFilter();

}

void AMonsterCharacter::ChangeFilter(float moveSpeed, bool isIgnoreServerPos /*= false*/, FVector destPos /*= FVector::ZeroVector*/)
{
	UFilterActorComponent* FilterActorCpt = GetFilterComponent();
	if (FilterActorCpt && PhysicsFilter != FilterActorCpt)
	{
		GetFilterComponent()->SetActiveComponentTick(false);
		SetFilterComponent(PhysicsFilter);
		PhysicsFilter->RegisterComponent();
		PhysicsFilter->InitFilter(true);
		PhysicsFilter->InitData(moveSpeed, destPos);
	}

}

void AMonsterCharacter::ChangeCurveFilter(float Gravity, float UpTime, float XSpeed, FVector DstPos)
{
	if (GetFilterComponent() && CurveFilter != GetFilterComponent())
	{
		GetFilterComponent()->SetActiveComponentTick(false);
		SetFilterComponent(CurveFilter);
		CurveFilter->RegisterComponent();
		CurveFilter->InitFilter(true);
	}
	CurveFilter->InitData(Gravity, UpTime, XSpeed, DstPos);
}

void AMonsterCharacter::ChangeDumbFilter()
{
	if (GetFilterComponent() && DumbFilter != GetFilterComponent())
	{
		GetFilterComponent()->SetActiveComponentTick(false);
		SetFilterComponent(DumbFilter);
		DumbFilter->RegisterComponent();
		DumbFilter->InitFilter(true);
	}
}


void AMonsterCharacter::ChangeLineToPointFilter(float MoveSpeed, FVector DstPos, FRotator Rotator)
{
	if (GetFilterComponent() && LineToPointFilter != GetFilterComponent())
	{
		GetFilterComponent()->SetActiveComponentTick(false);
		SetFilterComponent(LineToPointFilter);
		LineToPointFilter->RegisterComponent();
		LineToPointFilter->InitFilter(true);
		SetActorRotation(Rotator);
		LineToPointFilter->InitData(MoveSpeed, DstPos);
	}
}

void AMonsterCharacter::ChangeHitBackMoveFilter(float MoveSpeed, FVector DestPos /*= FVector::ZeroVector*/)
{
	UFilterActorComponent* FilterCpt = GetFilterComponent();
	if (FilterCpt && HitBackMoveFilter != FilterCpt)
	{
		GetFilterComponent()->SetActiveComponentTick(false);
		SetFilterComponent(HitBackMoveFilter);
		HitBackMoveFilter->RegisterComponent();
		HitBackMoveFilter->InitFilter(true);
		HitBackMoveFilter->InitData(MoveSpeed, DestPos, GetSelfEntity()->Position(), this->FloorTrace(DestPos));
	}
	UGameObjectInterface* interface = GetEntityInterface_Cache().GameObjectInterface;
	if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE))
	{
		MonsterPosSyncComponent->BeHitBack();
	}
	if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY))
	{
		MonsterExtJDCYComponent->BeHitBack();
	}
}

void AMonsterCharacter::ChangeBlowFilter(const FVector & WindDir, const float & WindSpeed)
{
	if (!IsValid(BlowFilterComponent))
	{
		BlowFilterComponent = NewObject<UMonsterBlowFilterComponent>(this, "BlowComponent");
	}
	UFilterActorComponent* FilterCpt = GetFilterComponent();
	if (FilterCpt && BlowFilterComponent != FilterCpt)
	{
		GetFilterComponent()->SetActiveComponentTick(false);
		SetFilterComponent(BlowFilterComponent);
		BlowFilterComponent->RegisterComponent();
		BlowFilterComponent->InitFilter(true);
		BlowFilterComponent->InitData(WindDir, WindSpeed);
	}
}

void AMonsterCharacter::ResetFilter()
{
	KBEngine::Entity* Entity = this->GetSelfEntity();

	if (Entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMonsterCharacter::ResetFilter : Entity!"));
		return;
	}
	
	UGameObjectInterface* interface = GetEntityInterface_Cache().GameObjectInterface;
	if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE)) //客户端往服务器同步位置的怪物
	{
		if (!IsValid(MonsterPosSyncComponent))
		{
			MonsterPosSyncComponent = NewObject<UMonsterPosSyncComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr);
			MonsterPosSyncComponent->RegisterComponent();
		}
		if (GetFilterComponent() && MonsterPosSyncComponent != GetFilterComponent())
		{
			GetFilterComponent()->SetActiveComponentTick(false);
		}
		SetFilterComponent(MonsterPosSyncComponent);
		MonsterPosSyncComponent->InitFilter(true);
	}
	else if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT) && StaticCast<CMonster*>(Entity)->IsControlClient()) 
	{
		if (!IsValid(CMonsterPosSyncComponent))
		{
			CMonsterPosSyncComponent = NewObject<UCMonsterPosSyncComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr);
			CMonsterPosSyncComponent->RegisterComponent();
		}
		if (GetFilterComponent() && CMonsterPosSyncComponent != GetFilterComponent())
		{
			GetFilterComponent()->SetActiveComponentTick(false);
		}
		SetFilterComponent(CMonsterPosSyncComponent);	
		CMonsterPosSyncComponent->InitFilter(true);
	}
	else if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_FOLLOW_ROLE)
		&& ((int32)Entity->GetDefinedProperty(TEXT("controlEntityID"))) == UGolbalBPFunctionLibrary::GetPlayerID())
	{
		if (!IsValid(FollowFilterComponent))
		{
			FollowFilterComponent = NewObject<UMonsterFollowComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr);
			FollowFilterComponent->RegisterComponent();
		}
		if (GetFilterComponent() && FollowFilterComponent != GetFilterComponent())
		{
			GetFilterComponent()->SetActiveComponentTick(false);
		}
		SetFilterComponent(FollowFilterComponent);
		FollowFilterComponent->InitFilter(true);
	}
	else if (interface && 
		interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_OPTIMIZE)||
		interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_SOLDIER)||
		interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_COMMANDER))
	{
		
		if (!IsValid(MonsterOptimizeComponent))
		{
			MonsterOptimizeComponent = NewObject<UMonsterOptimizeComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr);
			MonsterOptimizeComponent->RegisterComponent();
		}
		if (GetFilterComponent() && MonsterOptimizeComponent != GetFilterComponent())
		{
			GetFilterComponent()->SetActiveComponentTick(false);
		}
		SetFilterComponent( MonsterOptimizeComponent );
		MonsterOptimizeComponent->InitFilter(true);
	}
	else if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY)) //禁地采药怪物
	{
		if (!IsValid(MonsterExtJDCYComponent))
		{
			MonsterExtJDCYComponent = NewObject<UMonsterExtJDCYComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr);
			MonsterExtJDCYComponent->RegisterComponent();
		}
		if (GetFilterComponent() && MonsterExtJDCYComponent != GetFilterComponent())
		{
			GetFilterComponent()->SetActiveComponentTick(false);
		}
		SetFilterComponent(MonsterExtJDCYComponent);
		MonsterExtJDCYComponent->InitFilter(true);
	}
	else
	{
		if (!IsValid(AvatarFilter))
		{
			AvatarFilter = NewObject<UAvatarFilterActorComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr);
			AvatarFilter->RegisterComponent();
		}
		if (GetFilterComponent() && AvatarFilter != GetFilterComponent())
		{
			GetFilterComponent()->SetActiveComponentTick(false);
		}
		SetFilterComponent(AvatarFilter);	
		AvatarFilter->InitFilter(true);
	}
}

void AMonsterCharacter::ResetFilterData()
{
	if (GetFilterComponent() && GetFilterComponent() == AvatarFilter)
	{
		AvatarFilter->ResetComponent();
	}
}

void AMonsterCharacter::CreateAppearance()
{
	if (KBEngine::Entity* Entity = this->GetSelfEntity())
	{
		CS3_Log(TEXT("AServerCharacter::CreateAppearance Begin EntityID[%d],"), EntityId);
		bIsChangeAppearanceling = true;
		FString ModelNumber = (FString)Entity->GetDefinedProperty(TEXT("modelNumber"));
		FString ExtraModelNumber = (FString)Entity->GetDefinedProperty(TEXT("extraModelNumber"));
		if (!ExtraModelNumber.IsEmpty())
		{
			ModelNumber = ExtraModelNumber;
		}

		///创建和PC长像同样的外观，只要继承了UMonsterCopyRoleModelInterface，就copy，服务器必须有ownerID属性
		UGameObjectInterface* GameObjectInterface = GetEntityInterface_Cache().GameObjectInterface;
		UMonsterCopyRoleModelInterface* monsterCopyInterface = Cast<UMonsterCopyRoleModelInterface>(GameObjectInterface);
		if (IsValid(monsterCopyInterface))
		{
			int32 OwnerID = monsterCopyInterface->GetOwnerID();
			AServerCharacter* OwnerCharacter = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(OwnerID));
			if (!IsValid(OwnerCharacter))
			{
				monsterCopyInterface->DelayCreateApperance();
				return;
			}
			GameObject* OwnerEntity = (GameObject*)OwnerCharacter->GetSelfEntity();


			TSharedPtr<FMODEL_DATA> ModelData = OwnerCharacter->GetCurModelData();
			if (ModelData.IsValid())
			{
				//ModelNumber = (FString)RoleEntity->GetDefinedProperty(TEXT("modelNumber"));
				ModelNumber = ModelData->RowName.ToString();
				CheckCreateDynamicPartCpt(ModelNumber);
				FAModelInfo ModelInfo = OwnerEntity->GetModelInfo();
				GetAppearanceComponent()->CreateAppearanceByModelInfo(ModelNumber, ModelInfo);
				return;
			}
		}
		GetAppearanceComponent()->CreateAppearance(ModelNumber);
	}
	else
	{
		CS3_Log(TEXT("AServerCharacter::CreateAppearance Begin  Entity[%d] Is Null"), EntityId);
	}
}

void AMonsterCharacter::OnCreateModelOver()
{
	Super::OnCreateModelOver();

	//CST-11766 解决事务里面的怪物会让玩家弹飞
	ECollisionEnabled::Type CollisionType = GetCapsuleComponent()->GetCollisionEnabled();
	GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	GetCapsuleComponent()->SetCollisionEnabled(CollisionType);

	///创建和PC长像同样的外观
	UGameObjectInterface* GameObjectInterface = GetEntityInterface_Cache().GameObjectInterface;
	UMonsterCopyRoleModelInterface* monsterCopyInterface = Cast<UMonsterCopyRoleModelInterface>(GameObjectInterface);
	if (IsValid(monsterCopyInterface))
	{
		int32 OwnerID = monsterCopyInterface->GetOwnerID();
		AServerCharacter* OwnerCharacter = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(OwnerID));
		if (IsValid(OwnerCharacter))
		{
			///显示捏脸表现
			if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->ModifyFaceManager)
				&& !OwnerCharacter->IsChangeModelState())
			{
				UUECS3GameInstance::Instance->ModifyFaceManager->SetBoneRef(this);
				UUECS3GameInstance::Instance->ModifyFaceManager->SetActorFaceData(this,
					OwnerCharacter->ModifyFaceDatas, OwnerCharacter->FaceStyleDatas);
			}
			UpdateFenShengWeaponState();

			PreviewBodyLightEffectID = UGolbalBPFunctionLibrary::GetFStringPropertyValue(OwnerID, TEXT("bodyLightEffect"));
			if (!PreviewBodyLightEffectID.IsEmpty())
			{
				ChangeBodyLightEffect(PreviewBodyLightEffectID);
			}
			
		}
	}

	if (IsValid(GetBaseAnimInstance()))
	{
		///当前动作发生改变时
		if (!GetBaseAnimInstance()->OnActionChangeFinish.IsBound())
		{
			GetBaseAnimInstance()->OnActionChangeFinish.AddUObject(this, &AMonsterCharacter::OnNotifyActionChangeFinish);
		}

	}
}

AMonsterCharacter::AMonsterCharacter()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = true;
	CharacterClassName = TEXT("MonsterCharacter");
	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;
	MonsterLadderMovementCpt = nullptr;

	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->bConstrainToPlane = true;
	GetCharacterMovement()->bSnapToPlaneAtStart = true;
	InitBaseComponent();
}

void AMonsterCharacter::BeginPlay()
{
	Super::BeginPlay();
	UMonsterInterface* MonsterInterface = Cast<UMonsterInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (IsValid(MonsterInterface) && nullptr != GetSelfEntity())
	{
		EntityTypeExt = MonsterInterface->GetEntityFlagExt();//存储，方便后面不需要取MonsterInterface及还要判断指针对象是否为空

		if (MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE) || 
			MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT) ||
			MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_FOLLOW_ROLE) ||
			MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_OPTIMIZE) ||
			MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_COMMANDER)||
			MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_SOLDIER) ||
			MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY)
			)
		{
			GetCharacterMovement()->UnregisterComponent();
			GetCharacterMovement()->SetAutoActivate(true);
			GetCharacterMovement()->RegisterComponent();
			if (!IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
			{
				return;
			}
			KBEngine::Entity* PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetSelfEntity();

			//设置ControlledBy
			if (PlayerEntity != nullptr)
			{
				MonsterInterface->RPC_CELL_onSetControlledBy();
			}

			if (MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE) ||
				MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_FOLLOW_ROLE) ||
				MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_OPTIMIZE) ||
				MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_COMMANDER)||
				MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_SOLDIER) ||
				MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY)
				) 
			{
				AMonsterCommonController* controller = GetWorld()->SpawnActor<AMonsterCommonController>();
				controller->Possess(this);
			}
		}

		if (MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_ATTACK_LADDER))
		{
			//以下二行解决触发辅助跳：1、设置成默认都碰撞，才能与玩家胶囊体碰撞 2、设置与正常玩家碰撞 
			//ThisPtr->GetCapsuleComponent()->SetCollisionObjectType(ECollisionChannel::ECC_GameTraceChannel7);
			//ThisPtr->GetCapsuleComponent()->SetCollisionResponseToChannel(ECC_GameTraceChannel3, ECR_Block);
			//GetMesh()->SetCollisionResponseToChannel(ECC_GameTraceChannel3, ECR_Block);//若不设置成block，玩家会掉进梯子
			GetCapsuleComponent()->CanCharacterStepUpOn = ECanBeCharacterBase::ECB_Yes;//让玩家可以走在上面
			GetMesh()->bUseAttachParentBound = 0;//设置包围盒不为胶囊体，而为mesh自身，不然玩家旋转角度就看不到梯子了
		}

		//云梯设置
		if (MonsterInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_AERIAL_LADDER))
		{
			TriggerBox = NewObject<UBoxComponent>(this, "LadderTriggerBox");
			TriggerBox->RegisterComponent();
			TriggerBox->AttachToComponent(GetCapsuleComponent(), FAttachmentTransformRules::KeepRelativeTransform, "Root");
			TriggerBox->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
			TriggerBox->SetCollisionObjectType(ECollisionChannel::ECC_GameTraceChannel7);
			TriggerBox->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel3, ECollisionResponse::ECR_Overlap);
			TriggerBox->SetGenerateOverlapEvents(true);
			TriggerBox->OnComponentBeginOverlap.AddDynamic(this, &AMonsterCharacter::OnTriggerBeginOverlap);
			TriggerBox->OnComponentEndOverlap.AddDynamic(this, &AMonsterCharacter::OnTriggerEndOverlap);
			TriggerBox->bVisible = 1;
			TriggerBox->SetBoxExtent(FVector(32.0f, 32.0f, StepHeight), true);

			Bottom = NewObject<USceneComponent>(this, "LadderBottom");
			Bottom->RegisterComponent();
			Bottom->AttachToComponent(GetCapsuleComponent(), FAttachmentTransformRules::KeepRelativeTransform, "Root");

			Top = NewObject<USceneComponent>(this, "LadderTop");
			Top->RegisterComponent();
			Top->AttachToComponent(GetCapsuleComponent(), FAttachmentTransformRules::KeepRelativeTransform, "Root");

			OtherActorTop = NewObject<USceneComponent>(this, "OtherActorLadderTop");
			OtherActorTop->RegisterComponent();
			OtherActorTop->AttachToComponent(GetCapsuleComponent(), FAttachmentTransformRules::KeepRelativeTransform, "Root");
		}
	}
}

void AMonsterCharacter::InitBaseComponent()
{
	FightComponent = CreateDefaultSubobject<UMonsterFightComponent>(TEXT("FightComponent"));
	AppearanceComponent = CreateDefaultSubobject<URoleAppearanceComponent>(TEXT("AppearanceComponent"));
}

void AMonsterCharacter::OnEnterFightState()
{
	Super::OnEnterFightState();
	UGameObjectInterface* interface = GetEntityInterface_Cache().GameObjectInterface;
	if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE))
	{
		MonsterPosSyncComponent->ChaseTarget();
	}
	if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY))
	{
		MonsterExtJDCYComponent->ChaseTarget();
	}
	UpdateFenShengWeaponState();
}

void AMonsterCharacter::OnExitFightState()
{
	Super::OnExitFightState();
	UpdateFenShengWeaponState();
}

void AMonsterCharacter::OnEnterWarnState()
{
	Super::OnEnterWarnState();
	UpdateFenShengWeaponState();
}

void AMonsterCharacter::OnExitWarnState()
{
	Super::OnExitWarnState();
	UpdateFenShengWeaponState();
}

void AMonsterCharacter::OnEnterDeadState()
{
	Super::OnEnterDeadState();
	CollisionComponent->UpdateModelCollision();
	DeathDestructiveEffectBP();
}

void AMonsterCharacter::OnExitDeadState()
{
	Super::OnExitDeadState();
	CollisionComponent->UpdateModelCollision();
}

void AMonsterCharacter::OnEnterShowState()
{
	Super::OnEnterShowState();
	CollisionComponent->UpdateModelCollision();
}

void AMonsterCharacter::OnExitShowState()
{
	Super::OnExitShowState();
	CollisionComponent->UpdateModelCollision();
}

void AMonsterCharacter::OnEnterResetState()
{
	Super::OnEnterResetState();
	CollisionComponent->UpdateModelCollision();
	UGameObjectInterface* interface = GetEntityInterface_Cache().GameObjectInterface;
	if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE))
	{
		MonsterPosSyncComponent->GoBack();
	}
}

void AMonsterCharacter::OnExitResetState()
{
	Super::OnExitResetState();
	CollisionComponent->UpdateModelCollision();
}

void AMonsterCharacter::OnEnterFreeState()
{
	Super::OnEnterFreeState();
	UGameObjectInterface* Interface = GetEntityInterface_Cache().GameObjectInterface;
	if (Interface && Interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE))
	{
		MonsterPosSyncComponent->StartWander();
	}
	if (Interface && Interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY))
	{
		MonsterExtJDCYComponent->StartWander();
	}
}

void AMonsterCharacter::PlayAdmissionAction(FName ActionId)
{
	FActionOverDelegate Delegate;
	Delegate.AddUObject(this, &AMonsterCharacter::CallBackPlayAdmissionActionOver);
	PlayAction(ActionId, 0.0f, Delegate);
}

void AMonsterCharacter::CallBackPlayAdmissionActionOver(ACharacter* Character, FACTION_DATA InActionData)
{
	KBEngine::Entity* Monster = GetSelfEntity();
	if (Monster == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMonsterCharacter::CallBackPlayAdmissionActionOver : Monster!"));
		return;
	}
	UMonsterInterface * MonsterInterface = Cast<UMonsterInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (MonsterInterface)
	{
		MonsterInterface->RPC_CELL_startFalling();
	}
}

void AMonsterCharacter::MonsterCharacterJumpStart(const TArray<FName>& Actions, const FString& EffectID)
{
	//抛物线运动过程中无视碰撞
	GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	JumpStartAction = "";
	JumpProcessAction = "";
	JumpEndAction = "";
	if (Actions.IsValidIndex(0))
	{
		JumpStartAction = Actions[0];
	}
	if (Actions.IsValidIndex(1))
	{
		JumpProcessAction = Actions[1];
	}
	if (Actions.IsValidIndex(2))
	{
		JumpEndAction = Actions[2];
	}

	bool IsBoundTest = StartJumpDelegate.IsBound();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("[MonsterJump]JumpStart[EntityId(%d),  IsBound(%d), BaseAnimInstance(%d), JumpStartAction(%s), JumpProcessAction(%s), JumpEndAction(%s)"),
		GetSelfEntity()->ID(), IsBoundTest ? 1 : 0, GetBaseAnimInstance() ? 1 : 0, *JumpStartAction.ToString(), *JumpProcessAction.ToString(),
		*JumpEndAction.ToString());

	if (GetBaseAnimInstance())
	{
		if (StartJumpDelegate.IsBound())
		{
			StartJumpDelegate.Clear();
		}
		IsJumpEnd = false;
		IsForceStopIump = true;
		StartJumpDelegate.AddUObject(this, &AMonsterCharacter::CallBackMonsterJumpStartOver);
		PlayAction(JumpStartAction, 0.0f, StartJumpDelegate);
	}
	MonsterJumpEffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, this, this);
}

void AMonsterCharacter::CallBackMonsterJumpStartOver(ACharacter* Character, FACTION_DATA InActionData)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("[MonsterJump]StartOver[EntityId(%d), IsJumpEnd(%d)"), GetSelfEntity()->ID(), IsJumpEnd ? 1 : 0);
	StartJumpDelegate.Clear();

	if (!IsJumpEnd)
	{
		IsForceStopIump = true;
		FActionOverDelegate Delegate;
		PlayAction(JumpProcessAction, 0.0f, Delegate);
	}
}

void AMonsterCharacter::MonsterCharacterJumpEnd(bool IsCameraShake)
{
	bool IsBoundTest = StartJumpDelegate.IsBound();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("[MonsterJump]JumpEnd[EntityId(%d), IsBound(%d), BaseAnimInstance(%d)"),
		GetSelfEntity()->ID(), IsBoundTest ? 1 : 0, GetBaseAnimInstance() ? 1 : 0);

	IsJumpEnd = true;
	/*StopAction();*/
	if (IsCameraShake)
	{
		//震屏效果
		NotifyCameraShake();
	}
	//抛物线运动结束恢复碰撞
	GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);

	if (IsValid(UUECS3GameInstance::Instance))
	{
		//1秒后结束出场光效
		FTimerHandle DelayHandle;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, this,
			&AMonsterCharacter::StopMonsterJumpEffect, 1.0f, false);
	}

	if (GetBaseAnimInstance())
	{
		if (IsForceStopIump)
		{
			StopFrontAction();
		}
		PlayAction(JumpEndAction, 0.0f);
	}
}

void AMonsterCharacter::OnMonsterAppearJumpEnd(ACharacter* Character, FName ActionId)
{

}

void AMonsterCharacter::OnMoveOver(const uint32 movingID, const bool isSuccess)
{
	Monster *m = static_cast<Monster*>(GetSelfEntity());
	if( m != nullptr )
		m->OnMoveOver(movingID, isSuccess);
}

void AMonsterCharacter::MonsterCharacterJumpWithoutMoveStart(const TArray<FName>& Actions, const FString& EffectID, float Time)
{
	JumpStartAction = Actions[0];
	JumpProcessAction = Actions[1];
	JumpEndAction = Actions[2];
	LoopTime = Time;
	if (GetBaseAnimInstance())
	{
		FActionOverDelegate Delegate;
		Delegate.AddUObject(this, &AMonsterCharacter::CallBackMonsterJumpWithoutStartOver);
		PlayAction(JumpStartAction, 0.0f, Delegate);
	}
	MonsterJumpEffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, this, this);
}

void AMonsterCharacter::CallBackMonsterJumpWithoutStartOver(ACharacter* Character, FACTION_DATA InActionData)
{
	FActionOverDelegate Delegate;
	PlayAction(JumpProcessAction, 0.0f, Delegate);

	if (IsValid(UUECS3GameInstance::Instance))
	{
		FTimerHandle DelayHandle;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, this,
			&AMonsterCharacter::MonsterCharacterJumpWithoutMoveEnd, LoopTime, false);
	}
}

void AMonsterCharacter::MonsterCharacterJumpWithoutMoveEnd()
{
	//StopAction();
	if (IsValid(UUECS3GameInstance::Instance))
	{
		//1秒后结束出场光效
		FTimerHandle DelayHandle;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, this,
			&AMonsterCharacter::StopMonsterJumpEffect, 1.0f, false);
	}

	FActionOverDelegate Delegate;
	Delegate.AddUObject(this, &AMonsterCharacter::CallBackMonsterJumpWithoutEndOver);
	PlayAction(JumpEndAction, 0.0f, Delegate);
}

void AMonsterCharacter::CallBackMonsterJumpWithoutEndOver(ACharacter* Character, FACTION_DATA InActionData)
{
	UMonsterAppearInterface * MonsterAppearInterface = Cast<UMonsterAppearInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("MonsterAppearInterface"), EntityId));
	if (MonsterAppearInterface)
	{
		MonsterAppearInterface->RPC_CELL_onMonsterAppearJumpWithoutMoveEnd(Character, InActionData);
	}

}

void AMonsterCharacter::SetInitAction()
{
	KBEngine::Entity* SelfEntity = GetSelfEntity();
	InitActionId = !SelfEntity ? "None" : FSTRING_TO_FNAME((FString)SelfEntity->GetDefinedProperty(TEXT("initActionId")));
}

void AMonsterCharacter::PlayDeadEffect()
{
	KBEngine::Entity* Entity = GetSelfEntity();
	if (Entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMonsterCharacter::PlayDeadEffect : Entity!"));
		return;
	}
	FString ScriptID = Entity->GetDefinedProperty(TEXT("scriptID"));
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const FMONSTER_DATA* MonsterData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MONSTER)->GetRow<FMONSTER_DATA>(ScriptID);
	if (MonsterData && !MonsterData->DeadEffectId.IsEmpty())
	{
	bIsPlayDeadEffect = true;
	UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(this);
	UUECS3GameInstance::Instance->ParticleManager->PlayParticle(MonsterData->DeadEffectId, 0.0f, this, this);
	}
}

FString AMonsterCharacter::GetEntityUName()
{
	return UGolbalBPFunctionLibrary::GetFStringPropertyValue(EntityId, TEXT("uname"));
}

float AMonsterCharacter::GetMoveSpeed()
{
	if (bIsClient)
	{
		return ClientMoveSpeed;
	}
	return UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, TEXT("moveSpeed"));
}

bool AMonsterCharacter::IsEntityMoveType(MOVETYPE MoveType)
{
	int32 MovingType = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityId, TEXT("moveScriptID"));
	return MovingType == int32(MoveType);
}

bool AMonsterCharacter::IsEntityBoss()
{
	int32 AttrLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityId, TEXT("attrLevel"));
	return AttrLevel > 1;
}


void AMonsterCharacter::InitCharacterComponent()
{
	Super::InitCharacterComponent();
	GameObject* InGameObject = (GameObject*)GetSelfEntity();
	UGameObjectInterface* interface = GetEntityInterface_Cache().GameObjectInterface;
	if (InGameObject && interface && (interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE)
		|| interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY)
		|| (interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_FOLLOW_ROLE) && (GetSelfEntity() && ((int32)GetSelfEntity()->GetDefinedProperty(TEXT("controlEntityID"))) == UGolbalBPFunctionLibrary::GetPlayerID()))))
	{
		FVector Pos = GetActorLocation();
		SpawnPosition = Pos;
		KBEngine::Entity* PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetSelfEntity();
		//往服务器同步位置
		if (GetSelfEntity() != nullptr && PlayerEntity != nullptr)
		{
			InitPosSyncComponent();
		}
	}
}

void AMonsterCharacter::InitPosSyncComponent()
{
	UGameObjectInterface* interface = GetEntityInterface_Cache().GameObjectInterface;
	if (interface)
	{
		if (interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE))
		{
			MonsterPosSyncComponent = NewObject<UMonsterPosSyncComponent>(this, "TransFormControl", RF_NoFlags, nullptr, false, nullptr);
			MonsterPosSyncComponent->RegisterComponent();
			MonsterPosSyncComponent->SetActiveComponentTick(true);
		}
		else if (interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_FOLLOW_ROLE)
			&& (GetSelfEntity() && ((int32)GetSelfEntity()->GetDefinedProperty(TEXT("controlEntityID"))) == UGolbalBPFunctionLibrary::GetPlayerID()))
		{
			FollowFilterComponent = NewObject<UMonsterFollowComponent>(this, "TransFormControl", RF_NoFlags, nullptr, false, nullptr);
			FollowFilterComponent->RegisterComponent();
			FollowFilterComponent->SetActiveComponentTick(true);
		}
		else if (interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY))
		{
			MonsterExtJDCYComponent = NewObject<UMonsterExtJDCYComponent>(this, "TransFormControl", RF_NoFlags, nullptr, false, nullptr);
			MonsterExtJDCYComponent->RegisterComponent();
			MonsterExtJDCYComponent->SetActiveComponentTick(true);
		}
	}
}

bool AMonsterCharacter::IsMoveing()
{
	UCS3EntityInterface* TempInterface = GetEntityInterface_Cache().GameObjectInterface;
	if (IsValid(TempInterface))
	{
		UGameObjectInterface* interface = Cast<UGameObjectInterface>(TempInterface);
		if (IsValid(interface) && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE))
		{
			if (MonsterPosSyncComponent->GetCurMonsterMoveType() == MONSTER_MOVE_TYPE::None)
			{
				return false;
			}
			return true;
		}
		else if (IsValid(interface) && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_FOLLOW_ROLE)
			&& (GetSelfEntity() && ((int32)GetSelfEntity()->GetDefinedProperty(TEXT("controlEntityID"))) == UGolbalBPFunctionLibrary::GetPlayerID()))
		{
			if (FollowFilterComponent->GetCurMonsterMoveType() == MONSTER_FOLLOW_MOVE_TYPE::None || FollowFilterComponent->GetCurMonsterMoveType() == MONSTER_FOLLOW_MOVE_TYPE::StopMove)
			{
				return false;
			}
			return true;
		}
		else if (IsValid(interface) && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
		{
			if (((int32)GetSelfEntity()->GetDefinedProperty(TEXT("controlEntityID"))) == UGolbalBPFunctionLibrary::GetPlayerID())
			{
				return !GetCharacterMovement()->Velocity.IsZero();
			}
		}
		else if (IsValid(interface) && (interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_OPTIMIZE)|| 
			interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_COMMANDER)||
			interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_SOLDIER)))
		{
			if(GetFilterComponent() && GetFilterComponent()==MonsterOptimizeComponent)
			{
				UMonsterOptimizeInterface* intf = Cast<UMonsterOptimizeInterface>(interface);
				return !GetCharacterMovement()->Velocity.IsZero() || intf->clientMovingPathPoints.Num() != 0;
			}
			
		}
		if (IsValid(interface) && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY))
		{
			if (MonsterExtJDCYComponent->GetCurMonsterMoveType() == MONSTER_MOVE_TYPE::None)
			{
				return false;
			}
			return true;
		}
	}
	return Super::IsMoveing();
}

void AMonsterCharacter::CELL_MonsterFloorFalling()
{
	KBEngine::Entity* entity = GetSelfEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMonsterCharacter::CELL_MonsterFalling : entity!"));
		return;
	}
	//KBEngine::FVariantArray args;
	//entity->CellCall(TEXT("CELL_startFalling"), args);
	UMonsterInterface * MonsterInterface = Cast<UMonsterInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (MonsterInterface)
	{
		MonsterInterface->RPC_CELL_startFalling();
	}
}

void AMonsterCharacter::EndHitBack()
{
	UGameObjectInterface* interface = GetEntityInterface_Cache().GameObjectInterface;
	if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE))
	{
		MonsterPosSyncComponent->SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
	}
	if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY))
	{
		MonsterExtJDCYComponent->SetMonsterMoveType(MONSTER_MOVE_TYPE::None);
	}
}

void AMonsterCharacter::ChasePlayer(float distance)
{
	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::InWorld))
	{
		if (bIsChasePlayer && distance == ChaseDistance)
		{
			if (!GetVelocity().Equals(FVector::ZeroVector, 0.0001))
			{
				return;
			}
		}
		else
		{
			GetCapsuleComponent()->SetCollisionObjectType(ECollisionChannel::ECC_Vehicle);
			GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_Pawn, ECollisionResponse::ECR_Block);
			UAIBlueprintHelperLibrary::SimpleMoveToActor(GetController(), UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			ChaseDistance = distance;
			bIsChasePlayer = true;
		}
	}
}

void AMonsterCharacter::OnChasePlayer()
{
	if (bIsChasePlayer && (UGolbalBPFunctionLibrary::GetActorDistance(this, UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()) <= ChaseDistance * 100))
	{
		GetMovementComponent()->StopMovementImmediately();
		GetCapsuleComponent()->SetCollisionObjectType(ECollisionChannel::ECC_Pawn);
		GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_Pawn, ECollisionResponse::ECR_Ignore);
		ChaseDistance = 0.0;
		bIsChasePlayer = false;
		USkillInterface *SkillInterface = GetEntityInterface_Cache().SkillInterface;
		if (IsValid(SkillInterface))
		{
			SkillInterface->RPC_OnChasePlayerFinish();
		}
	}

}

void AMonsterCharacter::OnLeftMouseClicked()
{
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr))
	{
		TArray<FString> OtherValue;
		OtherValue.Add(INT_TO_FSTRING(bIsShowInvisible ? 1 : 0));
		OtherValue.Add(INT_TO_FSTRING(EntityId));
		OtherValue.Add(INT_TO_FSTRING(EntityId));
		OtherValue.Add(INT_TO_FSTRING(int(CHARACTER_TYPE::MONSTER_CHARACTER)));

		ControllerModeMgr->ExecuteInputInfor(TEXT("ShowSelectTarget"), TEXT(""), 0.0f, OtherValue);
	}
}

void AMonsterCharacter::OnActorBeginCursorOver()
{
	if (!UGolbalBPFunctionLibrary::GetSkillAssistUI())
	{
		if (!bIsShowInvisible)
		{
			if (HasFlag(ENTITY_FLAG::FLAG_CANT_SELECTED) || UGolbalBPFunctionLibrary::VisibleManager()->GetModelVisibleStyle(this) == VISIBLE_STYLE::VISIBLE_STYLE_FALSE)
			{
				return;
			}
			// 隐身
			UStateInterface * StateInterface = GetEntityInterface_Cache().StateInterface;
			if (IsValid(StateInterface) && StateInterface->HasEffectState(EFFECT_STATE::EFFECT_STATE_HIDE))
			{
				return;
			}
			//关系
			AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
			if (IsValid(PlayerActor) && QueryRelation(PlayerActor) == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
			{
				UGolbalBPFunctionLibrary::CustomCursorManager()->SetCursor("AttackCursor");
				bIsCursorOver = true;
			}
		}

	}
}

void AMonsterCharacter::OnActorEndCursorOver()
{
	UGolbalBPFunctionLibrary::CustomCursorManager()->DefaultCursor();
	bIsCursorOver = false;
}

void AMonsterCharacter::SetHitMaterial()
{
	GetMesh()->SetScalarParameterValueOnMaterials("EdgeGlowIntensity", 1.2);
	GetMesh()->SetScalarParameterValueOnMaterials("EdgeGlowWidth", -0.3);
	GetMesh()->SetVectorParameterValueOnMaterials("EdgeGlowColor", FVector(1.0, 0.62, 0.05));
}

void AMonsterCharacter::CreateHitMaterial()
{
	TArray<class UMaterialInterface*> MaterialsList;
	MaterialsList = GetMesh()->GetMaterials();
	for (int i = 0; i < MaterialsList.Num(); i++)
	{
		UMaterialInstanceDynamic* material = Cast<UMaterialInstanceDynamic>(MaterialsList[i]);
		if (!IsValid(material))
		{
			GetMesh()->UPrimitiveComponent::CreateDynamicMaterialInstance(i, GetMesh()->GetMaterials()[i]);
		}

	}
	//SetHitMaterial();暂时先屏蔽（CST-8032）
}

int32 AMonsterCharacter::GetFinalCamp()
{
	KBEngine::Entity* Entity = GetSelfEntity();
	if (Entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMonsterCharacter::GetFinalCamp : Entity!"));
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

void AMonsterCharacter::BaseChange()
{
	Super::BaseChange();
	BP_OnBaseChange();
}

void AMonsterCharacter::UpdateRelation_Implementation()
{
	BattlefieldStyleUtilities::ApplyAppearanceStyle(this);
	Super::UpdateRelation_Implementation();
}

void AMonsterCharacter::StopMonsterJumpEffect()
{
	UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(MonsterJumpEffectUID);
	/*if (IsValid(MonsterJumpEffect))
	{
		MonsterJumpEffect->Stop();
	}*/
}

void AMonsterCharacter::OnNotifyActionChangeFinish(FACTION_DATA ActionData)
{
	//UpdateFenShengWeaponState();

	if (!PreviewBodyLightEffectID.IsEmpty())
	{
		ChangeBodyLightEffect(PreviewBodyLightEffectID);
	}
}

void AMonsterCharacter::UpdateFenShengWeaponState()
{
	UMonsterCopyRoleModelInterface* copyRoleModelInterface = Cast<UMonsterCopyRoleModelInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (IsValid(copyRoleModelInterface))
	{
		//取玩家的状态更新分身的武器状态
		GameObject* SelfEntity = (GameObject *)(UGolbalBPFunctionLibrary::FindEntity(copyRoleModelInterface->GetOwnerID()));
		if (SelfEntity)
		{
			int32 Profession = (int32)SelfEntity->GetDefinedProperty(TEXT("profession"));
			bool bIsFightShow = SelfEntity->IsState(ENTITY_STATE::EntityStateFight) || SelfEntity->IsState(ENTITY_STATE::EntityStateWarn);
			GetAppearanceComponent()->UpdateWeaponLocation(bIsFightShow, Profession);
		}
	}
}

void AMonsterCharacter::CreatePartMapByServer(TMap<MODEL_PART_TYPE, FString>& InPartDataMap)
{
	GameObject* SelfEntity = (GameObject*)GetSelfEntity();
	if (SelfEntity == nullptr)
	{
		return;
	}
	FString newValue = (FString)SelfEntity->GetDefinedProperty(TEXT("extraModelNumber"));
	if (!newValue.IsEmpty())
	{
		return;
	}

	if (SelfEntity->ClassName() == "MonsterExtXinMo" || SelfEntity->ClassName() == "MonsterExtModel" || SelfEntity->ClassName() == "MonsterExtClickAndModel")
	{
		InPartDataMap = GetAppearanceComponent()-> GetPartDataMapByModelInfo(SelfEntity->GetModelInfo());
	}
}

void AMonsterCharacter::RPC_onClickCallBack()
{
	KBEngine::Entity* entity = GetSelfEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMonsterCharacter::RPC_onClickCallBack : entity!"));
		return;
	}
	UMonsterInterface * MonsterInterface = Cast<UMonsterInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (MonsterInterface)
	{
		MonsterInterface->RPC_onClickCallBack();
	}
	//KBEngine::FVariantArray args;
	//entity->CellCall(TEXT("onClickCallBack"), args);
}

void AMonsterCharacter::OnMonsterAppearLineToPoint()
{
	UMonsterAppearInterface * MonsterAppearInterface = Cast<UMonsterAppearInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("MonsterAppearInterface"), EntityId));
	if (MonsterAppearInterface)
	{
		MonsterAppearInterface->RPC_CELL_onMonsterAppearLineToPoint();
	}
}

void AMonsterCharacter::GossipWith()
{
	UGameObjectInterface* interface = GetEntityInterface_Cache().GameObjectInterface;
	if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_INTERACTIVE))
	{
		KBEngine::Entity* entity = GetSelfEntity();
		if (entity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:AMonsterCharacter::GossipWith : entity!"));
			return;
		}
		UMonsterExtInteractiveInterface * MonsterExtInteractiveInterface = Cast<UMonsterExtInteractiveInterface>(GetEntityInterface_Cache().GameObjectInterface);
		if (MonsterExtInteractiveInterface)
		{
			MonsterExtInteractiveInterface->RPC_InteractiveWith();
		}
	}
	else if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_SFMJ))
	{
		KBEngine::Entity* entity = GetSelfEntity();
		if (entity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:AMonsterCharacter::GossipWith : entity!"));
			return;
		}
		UMonsterExtSFMJInterface * MonsterExtSFMJInterface = Cast<UMonsterExtSFMJInterface>(GetEntityInterface_Cache().GameObjectInterface);
		if (MonsterExtSFMJInterface)
		{
			MonsterExtSFMJInterface->RPC_InteractionResults();
		}
	}
	else if (interface && interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_QQRYJ))
	{
		KBEngine::Entity* entity = GetSelfEntity();
		if (entity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:AMonsterCharacter::GossipWith : entity!"));
			return;
		}
		UMonsterExtQQRYJInterface * MonsterExtQQRYJInterface = Cast<UMonsterExtQQRYJInterface>(GetEntityInterface_Cache().GameObjectInterface);
		if (MonsterExtQQRYJInterface)
		{
			MonsterExtQQRYJInterface->RPC_alternatelyResults();
			APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			if (IsValid(PlayerActor))
			{
				///<交互完成后状态的刷新，设置玩家的交互状态
				if (IsValid(PlayerActor->CurInteractiveTarget) && IsValid(this) && PlayerActor->CurInteractiveTarget == this)
				{
					PlayerActor->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_NODE;
				}
			}
		}
	}
}

void AMonsterCharacter::EndBlow()
{
	// 将风吹的位置 同步到filter
	ResetFilter();
	//GetFilterComponent()->SetPosition(GetActorLocation(), 0);
	if (IsValid(BlowFilterComponent))
	{
		BlowFilterComponent->EndBlow();
	}
}

FVector AMonsterCharacter::GetLadderBottomLocation()
{
	return Bottom->GetComponentLocation();
}

FVector AMonsterCharacter::GetLadderTopLocation()
{
	return Top->GetComponentLocation();
}

FVector AMonsterCharacter::GetOtherActorLadderTopLocation()
{
	return OtherActorTop->GetComponentLocation();
}

FVector AMonsterCharacter::GetEnterLadderTopLocation()
{
	FVector WorldLocation = Top->GetComponentLocation();
	WorldLocation.Z += StepHeight * CharacterLadderNum;
	return WorldLocation;
}

FRotator AMonsterCharacter::GetLadderBottomRotation()
{
	FRotator TempRotation = Bottom->GetComponentRotation();
	TempRotation.Yaw -= 180.0f;//因为玩家与梯子是对着的（方向相反）
	TempRotation.Pitch -= LadderPitchValue;
	return TempRotation;
}

FRotator AMonsterCharacter::GetLadderTopRotation()
{
	FRotator TempRotation = Top->GetComponentRotation();
	TempRotation.Yaw -= 180.0f;//因为玩家与梯子是对着的（方向相反）
	TempRotation.Pitch -= LadderPitchValue;
	return TempRotation;
}

TArray<int32> AMonsterCharacter::GetLadderAllEntityList()
{
	TArray<int32> EntityIdList;
	for (AServerCharacter *Character : LadderCharacterList)
	{
		if (IsValid(Character) && Character->GetSelfEntity())
		{
			EntityIdList.Add(Character->GetSelfEntity()->ID());
		}
	}
	return EntityIdList;
}

void AMonsterCharacter::InitLadderData(AMonsterCharacter *LadderCharacter)
{
	if (!IsValid(MonsterLadderMovementCpt))
	{
		MonsterLadderMovementCpt = NewObject<UMonsterLadderMovementComponent>(this,
			UMonsterLadderMovementComponent::StaticClass(), TEXT("MonsterLadderMovementComponent"));
		MonsterLadderMovementCpt->RegisterComponent();
		MonsterLadderMovementCpt->InitData(LadderCharacter);
	}
}

void AMonsterCharacter::ClearLadderData()
{
	if (IsValid(MonsterLadderMovementCpt))
	{
		MonsterLadderMovementCpt->UnregisterComponent();
		MonsterLadderMovementCpt->DestroyComponent();
		MonsterLadderMovementCpt = nullptr;
	}
}

void AMonsterCharacter::OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComp, AActor* Other, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& OverlapInfo)
{
	if (!IsEnableCollisionTriggerBox)
	{
		return;
	}
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(Other);
	if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->LadderCustomMovmentCpt))
	{
		if (PlayerCharacter->ActorIsPlayer())//只有本地玩家才需要进入攀爬的逻辑
		{
			PlayerCharacter->LadderCustomMovmentCpt->BeginOverlappedCustomMoveZone(this);
		}
		LadderCharacterList.Add(PlayerCharacter);
	}
	else
	{
		AMonsterCharacter *MonsterCharacter = Cast<AMonsterCharacter>(Other);
		//云梯单机测试需要修改的位置(删除MonsterCharacter->EntityTypeExt==判断)
		if (IsValid(MonsterCharacter) && (MonsterCharacter->EntityTypeExt == ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_CLIENT_BASE|| MonsterCharacter->EntityTypeExt == ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT||
			MonsterCharacter->EntityTypeExt == ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_JDCY))
		{
			if (IsValid(MonsterCharacter->GetController()))
			{
				MonsterCharacter->GetController()->StopMovement();
			}
			LadderCharacterList.Add(MonsterCharacter);
			MonsterCharacter->InitLadderData(this);
			MonsterCharacter->MonsterLadderMovementCpt->StartClimbLadder(GetLadderBottomLocation(), GetOtherActorLadderTopLocation(),
				GetLadderBottomRotation());
		}
	}
}

void AMonsterCharacter::OnTriggerEndOverlap(UPrimitiveComponent* OverlappedComp, AActor* Other, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{
	if (!IsEnableCollisionTriggerBox)
	{
		return;
	}

	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(Other);
	if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->LadderCustomMovmentCpt) && PlayerCharacter->GetSelfEntity())
	{
		if (PlayerCharacter->ActorIsPlayer())//只有本地玩家才需要退出攀爬的逻辑
		{
			PlayerCharacter->LadderCustomMovmentCpt->EndOverlappedCustomMoveZone(this);
		}
		LadderCharacterList.Remove(PlayerCharacter);
		//删除梯子交互键提示F
		PlayerCharacter->RemoveFromInteractivityList(this);
	}
	else
	{
		AMonsterCharacter *MonsterCharacter = Cast<AMonsterCharacter>(Other);
		if (MonsterCharacter && MonsterCharacter->GetSelfEntity())
		{
			LadderCharacterList.Remove(MonsterCharacter);
		}
	}
}

void AMonsterCharacter::NofityAllCharacterFallOutToLadder()
{
	for (AServerCharacter* CharacterObject : LadderCharacterList)
	{
		APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(CharacterObject);
		//只有本地玩家才需要进入攀爬的逻辑
		if (IsValid(PlayerCharacter) && PlayerCharacter->ActorIsPlayer())
		{
			PlayerCharacter->LadderCustomMovmentCpt->StartFallToLadder();
		}
		else
		{
			AMonsterCharacter *AIMonsterCharacter = Cast<AMonsterCharacter>(CharacterObject);
			if (IsValid(AIMonsterCharacter) && IsValid(AIMonsterCharacter->MonsterLadderMovementCpt))
			{
				AIMonsterCharacter->MonsterLadderMovementCpt->StartFallToLadder();
			}
		}
	}
	//清空梯子上的对象
	LadderCharacterList.Empty();
}

void AMonsterCharacter::EntityEnterLadder(int32 EnterEntityID)
{
	UMonsterExtAerialLadderInterface* MonsterExtAerialLadderInterface = 
		Cast<UMonsterExtAerialLadderInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (IsValid(MonsterExtAerialLadderInterface) && nullptr != GetSelfEntity())
	{
		if (MonsterExtAerialLadderInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_AERIAL_LADDER))
		{
			MonsterExtAerialLadderInterface->CELL_EntityEnterLadder(EnterEntityID);
		}
	}
}

void AMonsterCharacter::EntityExitLadder(int32 EnterEntityID)
{
	UMonsterExtAerialLadderInterface* MonsterExtAerialLadderInterface =
		Cast<UMonsterExtAerialLadderInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (IsValid(MonsterExtAerialLadderInterface) && nullptr != GetSelfEntity())
	{
		if (MonsterExtAerialLadderInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_AERIAL_LADDER))
		{
			MonsterExtAerialLadderInterface->CELL_EntityExitLadder(EnterEntityID);
		}
	}
}

CONTROL_COMPILE_OPTIMIZE_END


