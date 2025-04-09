// Fill out your copyright notice in the Description page of Project Settings.

#include "PlayerCharacter.h"
#include "Components/CapsuleComponent.h"
#include "CS3Base/GameObject.h"
#include "GameData/GameDeFine.h"
#include "GameData/NPCPointDatas.h"
#include "GameData/Item/ItemUseAssist.h"
#include "Interface/SkillInterface.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/EventManager.h"
#include "GameData/StateData.h"
#include "Kismet/KismetMathLibrary.h"
#include "GameData/CameraParamsEventData.h"
#include "Interface/Role/RolePetInterface.h"
#include "Component/AppearanceComponent.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/GameDefault.h"
#include "Util/CS3Algorithms.h"
#include "GameData/ConstData.h"
#include "Runtime/NavigationSystem/Public/NavigationSystem.h"
#include "Runtime/NavigationSystem/Public/NavigationPath.h"
#include "Navigation/PathFollowingComponent.h"
#include "GameData/CharacterData.h"
#include "Interface/Role/RoleStateInterface.h"
#include "Component/PhysicsFilterActorComponent.h"
#include "Interface/Role/RoleInterface.h"
#include "Component/ActorTraceMoveComponent.h"
#include "Component/DumbFilterActorComponent.h"
#include "Component/RoleFilterActorComponent.h"
#include "Actor/SpellBox/SpellBoxCharacter.h"
#include "Actor/ServerCharacter.h"
#include "GameData/PetData.h"
#include "Interface/Role/RolePerformanceInterface.h"
#include "Interface/Role/RoleTeamInterface.h"
#include "MagicCharacter.h"
#include "GameData/FaBaoData.h"
#include "Actor/Scene/MovingPlatformCharacter.h"
#include "GameData/FlyBindMeshData.h"
#include "../NPC/FlyBindCharacter.h"
#include "Interface/Role/RoleSpaceInterface.h"
#include "../NPC/NPCCharacter.h"
#include "Entity/Role/CS3Role.h"
#include "Component/SpringArmComponentEX.h"
#include "Camera/CameraComponent.h"
#include "Engine/StaticMeshActor.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Interface/Role/RoleTeleportInterface.h"
#include "Manager/GameStatus.h"
#include "Manager/StoryManager.h"
#include "Manager/ParticleManager.h"
#include "Component/Role/JumpComponent.h"
#include "Component/Role/RideCarrierComponent.h"
#include "Component/Role/FlyPatrolComponent.h"
#include "Component/Role/PosSyncComponent.h"
#include "Manager/LevelManager.h"
#include "Manager/MessageManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "Manager/MapManager.h"
#include "Util/ConvertUtil.h"
#include "Manager/VisibleManager.h"
#include "Manager/AutoNavigatePathMgr.h"
#include "Manager/ForceManager.h"
#include "Manager/CrossMapNavigateMgr.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "Manager/Operation/OperationModeMgr.h"
#include "Manager/AtkStateMar.h"
#include "Manager/SkillManager.h"
#include "Manager/CustomTimerManager.h"
#include "Interface/Role/RoleStallInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CustomEffect/CameraControl.h"
#include "Interface/NPC/NPCInterface.h"
#include "../Monster/MonsterCharacter.h"
#include "Interface/Monster/MonsterExtBatteryInterface.h"
#include "GameFramework/WorldSettings.h"
#include "Manager/AudioManager.h"
#include "Particles/ParticleSystemComponent.h"
#include "Component/FightComponent.h"
#include "GameData/RoleJumpData.h"
#include "Interface/Role/RoleSpaceContentInterface.h"
#include "Components/MeshComponent.h"

CONTROL_COMPILE_OPTIMIZE_START

uint8 APlayerCharacter::ModelColorScheme = 0;

APlayerCharacter::APlayerCharacter()
{
	CharacterClassName = TEXT("PlayerCharacter");
	PrimaryActorTick.bCanEverTick = true;
	IsCalNarDirection = false;
	bIsRoleInteractive = false;
	CapsuleVec = FVector::ZeroVector;

	LadderCustomMovmentCpt = nullptr;

	bModeOrientRotation = true;
	OrientRotationNum = 0;

	EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_NODE;
	OtherPlayerMoveType = CS3_MOVE_TYPE::MOVE_TYPE_NONE;
	CreateRoleMesh();
	InitBaseComponent();

	GetCharacterMovement()->SetAutoActivate(true);
}

void APlayerCharacter::PostInitProperties()
{
	Super::PostInitProperties();
	DefaultMaxStepHeight = this->GetCharacterMovement()->MaxStepHeight;
	DefaultWalkableFloorAngle = this->GetCharacterMovement()->GetWalkableFloorAngle();
}

void APlayerCharacter::BeginPlay()
{
	Super::BeginPlay();

	SetCharacterMovementDefaultWalkProperty();

	//本地或非本地角色组件初始化
	{
		if (ActorIsPlayer())
		{
			InitLocalPlayerComponent();
			///<开始检测交互目标
			StartCheckingInteractiveTarget();
			//开始网络检查
			reqNetwordTime();
			WorldPostActorTickHandle = FWorldDelegates::OnWorldPostActorTick.AddUFunction(this, TEXT("OnWorldPostActorTick"));

			//玩家跳跃jump()时忽略掉脚下物体的Z轴速度[CST-8284]
			GetCharacterMovement()->bImpartBaseVelocityZ = false;
		}
		else
		{
			InitNotLocalPlayerComponent();
		}

		GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel1, ECollisionResponse::ECR_Block); // 需要碰到Water CST-10063
	}
}

void APlayerCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(RandomActionTimerHander);
	}
	ClearWorldPostActorTickHandle();
	StopCheckingInteractiveTarget();
	UnBindWeatherSoundComp();
	WindIDArr.Empty();
	if (IsValid(CameraControl))
	{
		CameraControl->Destroy();
	}
	RideCarrierComponent->OnCreateRoleAppearance.Clear();
	RideCarrierComponent->Destroy();
	DeactivatePlayerControllerMoveComopnent();
	if (ActorIsPlayer())
	{
		clearNetwordTime();
	}

	Super::EndPlay(EndPlayReason);
}


FNAVIGATE_NPC_INFO APlayerCharacter::GetNavigateNPCInfo()
{
	return NavigateNPCInfo;
}

void APlayerCharacter::ClearNavigateNPCInfo()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" APlayerCharacter::ClearNavigateNPCInfo EntityID[%d]"), EntityId);
	NavigateNPCInfo.ResetData();
}


void APlayerCharacter::OnDodgeRotation()
{
	IsDodgeState = true;
}

void APlayerCharacter::InitBaseComponent()
{
	//这里面只初始化本地玩家和非本地玩家都通用的组件  相关http://172.16.2.227/browse/CST-6274

	UCapsuleComponent* CharacterCapsuleComponent = GetCapsuleComponent();

	ChildActor = CreateDefaultSubobject<UChildActorComponent>(TEXT("ChildActor"));
	ChildActor->AttachToComponent(CharacterCapsuleComponent, FAttachmentTransformRules::KeepRelativeTransform);
	ChildActor->SetRelativeLocationAndRotation(FVector(-50.0f, 0.0f, -150.0f), FRotator(0.0f, -90.0f, 0.0f));

	FightComponent = CreateDefaultSubobject<UFightComponent>(TEXT("FightComponent"));
	AppearanceComponent = CreateDefaultSubobject<URoleAppearanceComponent>(TEXT("RoleAppearanceComponent"));
	
	ActorTraceMoveComponent = CreateDefaultSubobject<UActorTraceMoveComponent>(TEXT("ActorTraceMoveComponent"));
	FlyPatrolComponent = CreateDefaultSubobject<UFlyPatrolComponent>(TEXT("FlyPatrolComponent"));
	
	JumpComponent = CreateDefaultSubobject<UJumpComponent>(TEXT("JumpComponent"));
	JumpComponent->InitJumpData();

	LadderCustomMovmentCpt = CreateDefaultSubobject<ULadderCustomMovementComponent>(TEXT("LadderCustomMovementComponent"));
	LadderCustomMovmentCpt->InitLadderData();

	RideCarrierComponent = CreateDefaultSubobject<URideCarrierComponent>(TEXT("RideCarrierComponent"));
	if (!RideCarrierComponent->OnCreateRoleAppearance.IsBound())
	{
		RideCarrierComponent->OnCreateRoleAppearance.AddUObject(this, &APlayerCharacter::NotifyCreateRoleAppearance);
	}
}

void APlayerCharacter::InitLocalPlayerComponent()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" APlayerCharacter::InitLocalPlayerComponent"));
	UCapsuleComponent* CharacterCapsuleComponent = GetCapsuleComponent();

	//镜头摇臂组件
	//镜头组件
	{
		SpringArmCompent = NewObject<USpringArmComponentEX>(this, TEXT("SpringArmCompent"));
		SpringArmCompent->RegisterComponent();
		SpringArmCompent->AttachToComponent(CharacterCapsuleComponent, FAttachmentTransformRules::KeepRelativeTransform);
		UGolbalBPFunctionLibrary::SetCameraTargetArmLength(SpringArmCompent, 1500.0f);
		UGolbalBPFunctionLibrary::SetCameraSocketOffset(SpringArmCompent, FVector(-300.0f, 0.0f, 0.0f));
		SpringArmCompent->bUsePawnControlRotation = true;
		SpringArmCompent->SetRelativeLocation(FVector(0.0f, 0.0f, 65.0f));
		
		CameraComponent = NewObject<UCS3CameraComponent>(this, TEXT("FirstPersonCamera"));
		CameraComponent->RegisterComponent();
		CameraComponent->AttachToComponent(SpringArmCompent, FAttachmentTransformRules::KeepRelativeTransform);
		CameraComponent->SetRelativeLocationAndRotation(FVector(60.0f, 0.0f, 0.0f), FRotator(0.0f, 0.0f, 0.0f));
		UGolbalBPFunctionLibrary::SetCameraFOV(CameraComponent, 90.0f);
		CameraComponent->PostProcessSettings = PostProcessSettings;
		
		CameraControl = UGolbalBPFunctionLibrary::SpawnActor<ACameraControl>(ACameraControl::StaticClass());
		if (IsValid(CameraControl))
		{
			CameraControl->Init(CameraComponent, CameraComponent);
		}
	}
	///<初始化光照跟随效果
	InitLightComponent();
	///<初始化天气效果
	InitWeatherComponent();
}

void APlayerCharacter::InitNotLocalPlayerComponent()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" APlayerCharacter::InitNotLocalPlayerComponent"));
}

void APlayerCharacter::OnMouseLeftButtonClick()
{
	FVector MousePos = UGolbalBPFunctionLibrary::GetMouseWorldPos();
	if (HasSkillAssistUi && !MousePos.IsZero())
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::OnMouseLeftButtonClick EntityID[%d] MousePos x=%f y=%f z=%f"), EntityId, MousePos.X, MousePos.Y, MousePos.Z);
		LeftMouseClickCallback.ExecuteIfBound(MousePos);
		SkillAssisCallBack(MousePos);
	}
}

void APlayerCharacter::OnSimulateMouseLeftButtonClick(FVector Pos)
{
	if (HasSkillAssistUi && !Pos.IsZero())
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::OnSimulateMouseLeftButtonClick EntityID[%d] MousePos x=%f y=%f z=%f"), EntityId, Pos.X, Pos.Y, Pos.Z);
		LeftMouseClickCallback.ExecuteIfBound(Pos);
		SkillAssisCallBack(Pos);
	}
}

void APlayerCharacter::OnMouseScrollRoll(float Scale)
{
	if (Scale != 0.0f)
	{
		MouseScrollCallback.ExecuteIfBound(Scale);
	}
}

void APlayerCharacter::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);

	if (SequenceId.Compare(TEXT("")))
	{
		StartPlayStory_P();		
	}

	if (FMath::IsNearlyZero(UKismetMathLibrary::VSize(GetVelocity())) && IsCalNarDirection)
	{
		IsCalNarDirection = false;
	}

	if (bUpdatePos)
	{
		OnPlayerPositionSet(GetSelfEntity()->Position());
		bUpdatePos = false;
	}

	if (bIsYCJMDCopy && ActorIsPlayer())//设置瞄准偏移的方向值yaw/pitch
	{
		UpdateAimOffsetYawAndPitch(DeltaSeconds);
	}
}

void APlayerCharacter::BreakFalling()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT(" APlayerCharacter::BreakFalling EntityID[%d]"), EntityId);
	IsNotifyServerLandFalling = false;
}

void APlayerCharacter::SetInitAction()
{
	KBEngine::Entity* SelfEntity = GetSelfEntity();
	InitActionId = !SelfEntity ? "None" : FSTRING_TO_FNAME((FString)SelfEntity->GetDefinedProperty(TEXT("initActionId")));
}

bool APlayerCharacter::IsCanPlayAction()
{
	//冻结效果则不播放任何动作
	UStateInterface* StateInterface = GetEntityInterface_Cache().StateInterface;
	if (IsValid(StateInterface) && StateInterface->HasEffectState(EFFECT_STATE::EFFECT_STATE_FREEZE))
	{
		return false;
	}
	return true;
}

void APlayerCharacter::BindLinkEntity(KBEngine::Entity* Entity)
{
	Super::BindLinkEntity(Entity);
	this->SetRemoteRoleForBackwardsCompat(ROLE_None);
}

void APlayerCharacter::OnInitialized()
{
	Super::OnInitialized();
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	UUECS3GameInstance::Instance->AutoNavigatePathMgr->LoadGraph(SpaceScriptID);
	if (ActorIsPlayer())
	{
		UUECS3GameInstance::Instance->CS3PC->Possess(this);
	}
}

void APlayerCharacter::OnEnterDeadState()
{
	Super::OnEnterDeadState();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (EntityId != UGolbalBPFunctionLibrary::GetPlayerID()) return;

	//弹出复活界面
	if (IsValid(UUECS3GameInstance::Instance))
	{
		FTimerHandle DelayResurrectionPanelHandle;
		TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayResurrectionPanelHandle,
			FTimerDelegate::CreateLambda([DelayThisPtr]() {
			if (DelayThisPtr.IsValid())
			{
				if (DelayThisPtr.IsValid())
					if (DelayThisPtr->IsState(ENTITY_STATE::EntityStateDead))
					{
						APlayerCharacter* ThisPtr = DelayThisPtr.Get();
						ThisPtr->OnOpenResurrectionPanelBP();
					}
			}
		}), RESURRECTION_PANEL_OPEN_TIME, false);
	}
	// 取消火炮操作
	if (OperatorBatteryID)
	{
		UMonsterExtBatteryInterface* MBInterface = Cast<UMonsterExtBatteryInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(UMonsterExtBatteryInterface::GetName(), OperatorBatteryID));
		if (IsValid(MBInterface))
		{
			MBInterface->CancelOperationBattery();
		}
	}
	// 取消跳伞
	if (IsJumpParachuteState())
	{
		FlyPatrolComponent->LandYCJMDParachute();
		FlyPatrolComponent->LandYCJMDSkyDiving();
	}
}

void APlayerCharacter::OnEnterFreeState()
{
	Super::OnEnterFreeState();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	//CST-5825 在寻路状态并且是本地玩家且不再骑乘状态下
	if (IsValid(OperationModeMgr) && OperationModeMgr->IsHaveMode(EATTACT_STATE::NAVIGATE_MOVE) && ActorIsPlayer() && !IsCarrierState())
	{
		URolePetInterface * RolePetInterface = Cast<URolePetInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePetInterface"), EntityId));
		if (RolePetInterface)
		{
			RolePetInterface->RequestTransformPetFC();
		}
	}
}

void APlayerCharacter::OnEnterWarnState()
{
	Super::OnEnterWarnState();
}

void APlayerCharacter::EnterVehicleMode(RIDE_POSTURE_ENUM RidePosture, int32 Profession, int32 Gender)
{
	URoleAppearanceComponent* RoleAppearanceComponent = Cast<URoleAppearanceComponent>(GetAppearanceComponent());
	if (IsValid(RoleAppearanceComponent))
	{
		FRIDER_MODEL_ANIM_DATA* RiderModelAnimData = RoleAppearanceComponent->GetRideModelAnimDataFromCfg(RidePosture, (ROLE_PROFESSION_ENUM)Profession, (ROLE_GENDER_ENUM)Gender);
		if (RiderModelAnimData != nullptr)
		{
			ChangeAnimAction(RiderModelAnimData->AnimationPath, RiderModelAnimData->ActionConfigPath);
		}
	}
}

int32 APlayerCharacter::HasVehicle()
{
	KBEngine::Entity* ServerEntity = GetSelfEntity();
	if (ServerEntity != nullptr)
	{
		int32 vehicleId = ServerEntity->GetDefinedProperty(TEXT("vehicleId")).GetValue<int32>();
		return vehicleId;
	}
	return 0;
}

void APlayerCharacter::OnCreateRiderModelOver()
{
	if (IsCarrierState())
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT(" APlayerCharacter::OnCreateRiderModelOver EntityID[%d]"), EntityId);
		OnCreateApperanceOver();
		///载具模式创建完毕，开始上载具动作
		RideCarrierComponent->StartRideGetOnAction();

		OnBroadCreateRidderModelOver.ExecuteIfBound();
	}
}

void APlayerCharacter::OnCreateModelOver()
{
	if (!IsRidePetState() || !IsCarrierState())
	{
		OnCreateApperanceOver();
	}

	if (RideCarrierComponent->bIsDisRideOnCarrier)
	{
		RideCarrierComponent->bIsDisRideOnCarrier = false;
		OnDisRideOnPetOver.ExecuteIfBound();
	}

	//如果玩家有载具，在进入AOI的时候需要去服务器请求数据
	int32 tempVehicleID = HasVehicle();
	if (tempVehicleID)
	{
		URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
		if (Interface)
		{
			return Interface->CELL_reqVehicleData(EntityId, tempVehicleID);
		}
	}

	if (APlayerCharacter::ModelColorScheme == 2)
	{
		ChangeModelColor();
	}

	OnBroadCreateModelOver.ExecuteIfBound();
}

void APlayerCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();
	OnModelChangeAppearanceOverDelegate.Broadcast();

	if (IsValid(GetBaseAnimInstance()))
	{
		///同步载具上那个RideCharacter角色的动作
		if (IsRidePetState() || IsCarrierState())
		{
			if (!GetBaseAnimInstance()->OnPlayNewAction.IsBound())
			{
				GetBaseAnimInstance()->OnPlayNewAction.AddUObject(this, &APlayerCharacter::OnNotifyActionChange);
			}
		}
		else
		{
			GetBaseAnimInstance()->OnPlayNewAction.Clear();
		}

		///当前动作发生改变时
		if (!GetBaseAnimInstance()->OnActionChangeFinish.IsBound())
		{
			GetBaseAnimInstance()->OnActionChangeFinish.AddUObject(this, &APlayerCharacter::OnNotifyActionChangeFinish);
			//加载完成后检测动作CST-4103 
			CheckPartHideByAction(GetBaseAnimInstance()->GetCurPlayActionData());
		}

		///设置状态机的根运动模式，保证本机玩家有动画位移，服务器其他玩家没有
		if (!ActorIsPlayer())
		{
			GetBaseAnimInstance()->SetRootMotionMode(ERootMotionMode::IgnoreRootMotion);
		}
	}

	if (IsState(ENTITY_STATE::EntityStateDead))
	{
		OnEnterDeadState();
	}
	else if (IsState(ENTITY_STATE::EntityStateStall))
	{
		OnEnterStallState();
	}
	
	UpdateWeaponState();

	JumpComponent->SetJumpMaxCountBySkill();
}

void APlayerCharacter::ReSetOpenScen3DUI()
{
	/**先屏蔽，暂时不需要，后续可能又需要，暂不删除
	if (!ActorIsPlayer())
	{
		const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
		if (SpaceScriptID.Equals("fu_ben_L_YCJMD_zhenyingPVP"))//CST-12598 大荒战场不显示敌对玩家头顶信息
		{
			if (IsEnemyPlayer(this))
			{
				OpenScene3DUI = false;
				return;
			}
		}
	}
	*/
	OpenScene3DUI = true;
}

void APlayerCharacter::OnSignificanceChange()
{
	if(!ActorIsPlayer()) // 本地玩家不做游戏逻辑LOD优化
	{
		Super::OnSignificanceChange();
	}
}

void APlayerCharacter::CheckChangeState(ENTITY_STATE NewState, ENTITY_STATE OldState)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(this);
	bool bFlyState = Player && Player->FlyPatrolComponent->IsFlyPatrolState();
	//飞行状态下不拔刀和收刀

	//拔刀条件：自由--战斗、自由--警戒
	if ((NewState == ENTITY_STATE::EntityStateWarn || NewState == ENTITY_STATE::EntityStateFight) &&
		OldState == ENTITY_STATE::EntityStateFree && !bFlyState)
	{
		if (IsValid(GetBaseAnimInstance()))
		{
			//注意：拔刀先换武器，再播拔刀过程
			UpdateWeaponState();
			GetBaseAnimInstance()->PlayBaDaoAction();
		}
	}//收刀条件：战斗--自由、警戒--自由
	else if ((OldState == ENTITY_STATE::EntityStateWarn || OldState == ENTITY_STATE::EntityStateFight) &&
		NewState == ENTITY_STATE::EntityStateFree && !bFlyState)
	{
		if (IsValid(GetBaseAnimInstance()))
		{
			//注意：收刀先播收刀过程，再换武器
			FActionOverDelegate ActionOverDelegate;
			ActionOverDelegate.AddUObject(this, &APlayerCharacter::OnPlayShouBaoDaoActionOver);
			GetBaseAnimInstance()->PlayShouDaoAction(ActionOverDelegate);
		}
	}
	else if (NewState == ENTITY_STATE::EntityStateFree && OldState == ENTITY_STATE::EntityStateDead)
	{
		if (IsValid(GetBaseAnimInstance()))
		{
			GetBaseAnimInstance()->PlayRebornAction();
		}
	}
}

void APlayerCharacter::AddSkillAssistUiToScene(bool IsAddSkillAssistUi, int32 SkillId /*= 0*/, UFightAssist* FightAssist /*= nullptr*/)
{
	HasSkillAssistUi = IsAddSkillAssistUi;
	if (HasSkillAssistUi && FightAssist && SkillId != 0)
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::AddSkillAssistUiToScene EntityID[%d] IsAddSkillAssistUi=%d SkillId=%d"), EntityId, IsAddSkillAssistUi, SkillId);
		TWeakObjectPtr<UFightAssist> DelayFightAssistPtr(FightAssist);
		TWeakObjectPtr<APlayerCharacter> DelayPlayerCharacter(this);
		LeftMouseClickCallback = LeftMouseClickCallbackDelegate::CreateLambda([SkillId, DelayFightAssistPtr, DelayPlayerCharacter](FVector TargetPostion)
		{
			if (!DelayFightAssistPtr.IsValid())return;
			if (!DelayPlayerCharacter.IsValid())return;
			UFightAssist* FightAssist = DelayFightAssistPtr.Get();
			APlayerCharacter* AtkActor = DelayPlayerCharacter.Get();

			USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillId);
			float CastRange = SkillData->GetRangeMax();
			if (IsValid(AtkActor) && AtkActor->GetSkillAssistUi())
			{
				if (FVector::Dist(AtkActor->GetActorLocation(), TargetPostion) <= CastRange*100.0f)
				{
					FightAssist->UsePostionSkill(AtkActor, SkillId, TargetPostion);
				}
				else
				{
					//获取玩家控制器
					auto PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
					UAtkStateMar* AtkStateMar = nullptr;
					if (IsValid(PlayerController))
					{
						AtkStateMar = PlayerController->GetAtkStateMar();
					}

					if (IsValid(AtkStateMar) && (AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT) ||
						AtkStateMar->IsActivateState(EATTACT_STATE::HALF_HOMING_SPELL_ATT)))
					{
						if (AtkActor->GetSelfEntity() != nullptr&&AtkActor->GetSelfEntity()->IsPlayer() && IsValid(AtkActor->CurPlayerTarget))
						{
							//目标距离过远，请靠近后使用
							UUECS3GameInstance::Instance->MessageManager->ShowMessage(12);
							FightAssist->ClearFightAssistUi(true);
							AtkActor->AddSkillAssistUiToScene(false);
							return;
						}
						//指定位置无效，请重新选择。
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(24);
						FightAssist->CopyFightAssistUi();
					}
					else
					{
						//指定位置无效，请重新选择。
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(24);
						FightAssist->CopyFightAssistUi();

					}
				}
			}
		});
	}
	else
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::AddSkillAssistUiToScene EntityID[%d] IsAddSkillAssistUi=%d "), EntityId, IsAddSkillAssistUi);
		LeftMouseClickCallback = LeftMouseClickCallbackDelegate();
	}
}


void APlayerCharacter::AddItemAssistUiToScene(bool IsAddSkillAssistUi, FString UID /*= TEXT("")*/, int32 SkillId /*= 0*/, UFightAssist* FightAssist /*= nullptr*/)
{
	HasSkillAssistUi = IsAddSkillAssistUi;
	if (HasSkillAssistUi && FightAssist && SkillId != 0)
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::AddItemAssistUiToScene EntityID[%d] IsAddSkillAssistUi=%d SkillId=%d"), EntityId, IsAddSkillAssistUi, SkillId);
		TWeakObjectPtr<UFightAssist> DelayFightAssistPtr(FightAssist);
		TWeakObjectPtr<APlayerCharacter> DelayPlayerCharacter(this);
		LeftMouseClickCallback = LeftMouseClickCallbackDelegate::CreateLambda([UID, SkillId, DelayFightAssistPtr, DelayPlayerCharacter](FVector TargetPostion)
		{
			if (!DelayFightAssistPtr.IsValid())return;
			if (!DelayPlayerCharacter.IsValid())return;
			UFightAssist* FightAssist = DelayFightAssistPtr.Get();
			APlayerCharacter* AtkActor = DelayPlayerCharacter.Get();

			USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillId);
			float CastRange = SkillData->GetRangeMax();
			if (IsValid(AtkActor) && AtkActor->GetSkillAssistUi())
			{
				if (FVector::Dist(AtkActor->GetActorLocation(), TargetPostion) <= CastRange*100.0f)
				{
					FightAssist->UsePostionItem(AtkActor, UID, SkillId, TargetPostion);
				}
				else
				{
					//获取玩家控制器
					auto PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
					UAtkStateMar* AtkStateMar = nullptr;
					if (IsValid(PlayerController))
					{
						AtkStateMar = PlayerController->GetAtkStateMar();
					}

					if (IsValid(AtkStateMar) && AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT) &&
						AtkStateMar->IsActivateState(EATTACT_STATE::HALF_HOMING_SPELL_ATT))
					{
						if (AtkActor->GetSelfEntity() != nullptr&&AtkActor->GetSelfEntity()->IsPlayer() && IsValid(AtkActor->CurPlayerTarget))
						{
							//目标距离过远，请靠近后使用
							UUECS3GameInstance::Instance->MessageManager->ShowMessage(12);

							FightAssist->ClearFightAssistUi(true);
							AtkActor->AddSkillAssistUiToScene(false);
							return;
						}
						//指定位置无效，请重新选择。
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(24);
						FightAssist->CopyFightAssistUi();
					}
					else
					{
						//指定位置无效，请重新选择。
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(24);
						FightAssist->CopyFightAssistUi();
					}
				}

			}
		});
	}
	else
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::AddItemAssistUiToScene EntityID[%d] IsAddSkillAssistUi=%d "), EntityId, IsAddSkillAssistUi);
		LeftMouseClickCallback = LeftMouseClickCallbackDelegate();
	}
}

void APlayerCharacter::AddItemAssistUiToSceneExt(bool IsAddSkillAssistUi, FString UID, int32 SkillId, UFightAssist * FightAssist)
{
	HasSkillAssistUi = IsAddSkillAssistUi;
	IsSkillAssistUseTurn = false;
	if (!UID.IsEmpty())
	{
		URoleKitBagInterface* kitbag = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName("RoleKitBagInterface", EntityId));
		UItemUseAssist* item = Cast<UItemUseAssist>(kitbag->FindItemByUID(UID));
		if (!IsValid(item))
		{
			FightAssist->ClearModelAssistUi();
			return;
		}
		IsSkillAssistUseTurn = item->IsUseDirection();
	}
	if (HasSkillAssistUi && FightAssist && SkillId != 0)
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::AddItemAssistUiToScene EntityID[%d] IsAddSkillAssistUi=%d SkillId=%d"), EntityId, IsAddSkillAssistUi, SkillId);
		
		if (IsSkillAssistUseTurn)
		{
			TWeakObjectPtr<UFightAssist> DelayFightAssistPtr(FightAssist);
			MouseScrollCallback = MouseScrollCallbackDelegate::CreateLambda([DelayFightAssistPtr](float Scale)
			{
				if (!DelayFightAssistPtr.IsValid())return;
				UFightAssist* FightAssist = DelayFightAssistPtr.Get();
				FightAssist->TurnAssistModelDir(Scale);
			});
		}
		TWeakObjectPtr<UFightAssist> DelayFightAssistPtr(FightAssist);
		TWeakObjectPtr<APlayerCharacter> DelayPlayerCharacter(this);
		LeftMouseClickCallback = LeftMouseClickCallbackDelegate::CreateLambda([UID, SkillId, DelayFightAssistPtr, DelayPlayerCharacter](FVector TargetPostion)
		{
			if (!DelayFightAssistPtr.IsValid())return;
			if (!DelayPlayerCharacter.IsValid())return;
			UFightAssist* FightAssist = DelayFightAssistPtr.Get();
			APlayerCharacter* AtkActor = DelayPlayerCharacter.Get();

			USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillId);
			float CastRange = SkillData->GetRangeMax();
			URoleKitBagInterface* kitbag = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName("RoleKitBagInterface", AtkActor->EntityId));
			if (IsValid(AtkActor) && AtkActor->GetSkillAssistUi() && IsValid(kitbag))
			{
				UItemUseAssist* item = Cast<UItemUseAssist>(kitbag->FindItemByUID(UID));
				if (!IsValid(item))
				{
					FightAssist->ClearModelAssistUi();
					return;
				}
				if (AtkActor->IsSkillAssistUseTurn || FVector::Dist(AtkActor->GetActorLocation(), TargetPostion) <= CastRange * 100.0f)
				{
					if (item->CheckModelAssistValid(TargetPostion))
					{
						FightAssist->UsePostionItemExt(AtkActor, UID, SkillId, TargetPostion);
						AtkActor->AddSkillAssistUiToScene(false);
					}
					else
					{
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(24);
					}
					
				}
				else
				{
					//获取玩家控制器
					auto PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
					UAtkStateMar* AtkStateMar = nullptr;
					if (IsValid(PlayerController))
					{
						AtkStateMar = PlayerController->GetAtkStateMar();
					}

					if (IsValid(AtkStateMar) && AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT) &&
						AtkStateMar->IsActivateState(EATTACT_STATE::HALF_HOMING_SPELL_ATT))
					{
						if (AtkActor->GetSelfEntity() != nullptr&&AtkActor->GetSelfEntity()->IsPlayer() && IsValid(AtkActor->CurPlayerTarget))
						{
							//目标距离过远，请靠近后使用
							UUECS3GameInstance::Instance->MessageManager->ShowMessage(12);

							FightAssist->ClearModelAssistUi();
							AtkActor->AddSkillAssistUiToScene(false);
							return;
						}
						//指定位置无效，请重新选择。
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(24);
						FightAssist->CopyFightAssistUi();
					}
					else
					{
						//指定位置无效，请重新选择。
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(24);
						FightAssist->CopyFightAssistUi();
					}
				}

			}
		});
	}
	else
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::AddItemAssistUiToScene EntityID[%d] IsAddSkillAssistUi=%d "), EntityId, IsAddSkillAssistUi);
		LeftMouseClickCallback = LeftMouseClickCallbackDelegate();
		MouseScrollCallback = MouseScrollCallbackDelegate();
	}
}

void APlayerCharacter::GossipWithNearby(AActor* TargetActor, float NearbyDistance)
{
	if (IsState(ENTITY_STATE::EntityStateDead))
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::GossipWithNearby EntityID[%d] Is EntityStateDead  "), EntityId);
		SetInteractiveTarget(NULL);
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1314);
		return;
	}
	APlayerCharacter* AtkActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(AtkActor)|| !IsValid(TargetActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::GossipWithNearby : AtkActor!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::GossipWithNearby EntityID[%d] TargetActor=%s NearbyDistance=%d "), EntityId, *(TargetActor->GetName()), NearbyDistance);
	if (HasVehicle())
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(5933); //骑乘状态无法交互
		return;
	}

	if (UGolbalBPFunctionLibrary::GetActorDistance(AtkActor, TargetActor) < NearbyDistance * 100.0f)
	{
		EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_TRACETOTARGET;
		Cast<AServerCharacter>(TargetActor)->GossipWith();
		return;
	}
	ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(AtkActor->GetController());
	TWeakObjectPtr<AActor> DelayTargetActorPtr(TargetActor);
	TWeakObjectPtr<APlayerCharacter> DelayPlayerCharacterPtr(this);
	if (IsValid(PlayerController))
	{
		EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_TRACETOTARGET;
		//SpellBox专用，需要获取胶囊体底部坐标获取导航数据
		if (Cast<ASpellBoxCharacter>(TargetActor))
		{
			ASpellBoxCharacter* spellBox = Cast<ASpellBoxCharacter>(TargetActor);
			FVector destination = spellBox->GetActorLocation();
			destination.Z -= spellBox->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
			PlayerController->TraceTargetPostion(destination, NearbyDistance, FTraceCallback::CreateLambda(
				[DelayTargetActorPtr, DelayPlayerCharacterPtr, PlayerController](bool IsSuccess)
			{
				if (DelayTargetActorPtr.IsValid()&& DelayPlayerCharacterPtr.IsValid()  && IsValid(PlayerController))
				{
					if (IsSuccess)
					{
						//CST-10393 陈家伟在开箱子技能中加入了需要停下来后，才能成功放技能开箱子，所以这里就需要检测玩家的移动状态是否停止
						if (PlayerController->GetMoveType() == CS3_MOVE_TYPE::MOVE_TYPE_NONE)
						{
							AActor* TargetActorPtr = DelayTargetActorPtr.Get();
							Cast<AServerCharacter>(TargetActorPtr)->GossipWith();
						}
						else
						{
							DelayPlayerCharacterPtr->DelayGossipWithNearBy(DelayTargetActorPtr.Get());
						}
					}
					else
					{
						DelayPlayerCharacterPtr.Get()->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_NODE;
					}					
				}				
			}));
		}
		else  if (Cast<ANPCCharacter>(TargetActor))
		{
			ANPCCharacter* NPCCharacter = Cast<ANPCCharacter>(TargetActor);
			FVector destination = NPCCharacter->GetActorLocation();
			destination.Z = destination.Z - NPCCharacter->GetCapsuleComponent()->GetScaledCapsuleHalfHeight() + NPCCharacter->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight();

			if (IsValid(NPCCharacter))
			{
				PlayerController->TraceTargetPostion(destination, NearbyDistance, nullptr, false, FTraceCallback::CreateLambda([DelayTargetActorPtr, DelayPlayerCharacterPtr](bool IsSuccess)
				{
					if (DelayTargetActorPtr.IsValid() && DelayPlayerCharacterPtr.IsValid())
					{
						if (IsSuccess)
						{
							AActor* TargetActorPtr = DelayTargetActorPtr.Get();
							Cast<AServerCharacter>(TargetActorPtr)->GossipWith();
						}
						else
						{ 
							DelayPlayerCharacterPtr.Get()->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_NODE;
						}
					} 
				}));
			}		
		} 
		else
		{
			AServerCharacter* ServerCharacter = Cast<AServerCharacter>(TargetActor);
			FVector destination = ServerCharacter->GetActorLocation();
			destination.Z = destination.Z - ServerCharacter->GetCapsuleComponent()->GetScaledCapsuleHalfHeight() + ServerCharacter->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight();
			PlayerController->TraceTargetPostion(destination, NearbyDistance, FTraceCallback::CreateLambda([DelayTargetActorPtr, DelayPlayerCharacterPtr](bool IsSuccess)
			{
				if (DelayTargetActorPtr.IsValid() && DelayPlayerCharacterPtr.IsValid())
				{
					if (IsSuccess)
					{
						AActor* TargetActorPtr = DelayTargetActorPtr.Get();
						Cast<AServerCharacter>(TargetActorPtr)->GossipWith();
					}
					else
					{
						DelayPlayerCharacterPtr.Get()->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_NODE;
					}
				}
			}));
		}
	}
}

bool APlayerCharacter::IsEnemyPlayer(AActor* TargetActor)
{
	if (IsValid(TargetActor))
	{
		if (TargetActor->GetClass()->IsChildOf(APlayerCharacter::StaticClass()))
		{
			APlayerCharacter* TargetCharacter = Cast<APlayerCharacter>(TargetActor);
			if (IsValid(TargetCharacter))
			{
				APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
				if (IsValid(PlayerCharacter))
				{
					//目标对自己的关系，调的是目标的方法
					return TargetCharacter->QueryRelation(PlayerCharacter) == COMBAT_RELATION::COMBAT_RELATION_ENEMY;
				}
			}
		}
	}
	return false;
}

void APlayerCharacter::DelayGossipWithNearBy(AActor* TargetActor)
{
	TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
	TWeakObjectPtr<AActor> TargetActorPtr(TargetActor);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayGossipWithHandle,
		FTimerDelegate::CreateLambda([DelayThisPtr, TargetActorPtr]()
			{
				APlayerCharacter* AtkActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
				ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(AtkActor->GetController());
				if (TargetActorPtr.IsValid() && IsValid(PlayerController) && PlayerController->GetMoveType() == CS3_MOVE_TYPE::MOVE_TYPE_NONE)
				{
					AServerCharacter* TargetServer = Cast<AServerCharacter>(TargetActorPtr);
					if (IsValid(TargetServer))
					{
						Cast<AServerCharacter>(TargetActorPtr)->GossipWith();
					}
					CS3_Warning(TEXT("APlayerCharacter::DelayGossipWithNearBy"));
					UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayThisPtr->DelayGossipWithHandle);
				}
			}), 0.01f, true);
}

void APlayerCharacter::StartPlayStory(const FString& SequenceID, int32 LoopNum /*= 1*/)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::StartPlayStory EntityID[%d] SequenceID=%s LoopNum=%d "), EntityId,*SequenceID,LoopNum);
	SequenceId = SequenceID;
	SequenceLoopNum = LoopNum;
}

void APlayerCharacter::StartPlayStory_P()
{
	ULevelManager* LevelManager = UGolbalBPFunctionLibrary::LevelManager();
	UGStoryManager* GStoryManager = UGolbalBPFunctionLibrary::GStoryManager();
	if (LevelManager && GStoryManager&&UUECS3GameInstance::Instance&&UUECS3GameInstance::Instance->GameStatus)
	{
		if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
		{
			return;
		}
		else if (UUECS3GameInstance::Instance&&UUECS3GameInstance::Instance->GameStatus->GetIsInWorldLoadingOver())
		{
			GStoryManager->PlaySequence(SequenceId, SequenceLoopNum);
			SequenceId = TEXT("");
			SequenceLoopNum = 1;
		}
	}
}

void APlayerCharacter::SwitchFly(bool bIsSwitch/* = true*/, bool bIsFly /*= true*/)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::SwitchFly EntityID[%d] bIsSwitch=%d LoopNum=%d "), EntityId, bIsSwitch, bIsFly);

	UCharacterMovementComponent* MovementComponent = this->GetCharacterMovement();
	if (bIsSwitch) 
	{
		if (MovementComponent->IsFlying())
		{
			MovementComponent->SetMovementMode(MOVE_Walking);
		}
		else
		{
			MovementComponent->SetMovementMode(MOVE_Flying);
		}
	}
	else 
	{
		if (bIsFly)
		{
			MovementComponent->SetMovementMode(MOVE_Flying);
		}
		else
		{
			MovementComponent->SetMovementMode(MOVE_Walking);
		}
	}
}

void APlayerCharacter::StartFlyPatrol(FString FlyPatrolID)
{
	if (IsValid(FlyPatrolComponent))
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::StartFlyPatrol EntityID[%d] FlyPatrolID=%s"), EntityId, *FlyPatrolID);
		FlyPatrolComponent->StartFlyPatrol(FlyPatrolID);
	}
}
bool APlayerCharacter::IsHZMGFlyState()
{
	if (IsValid(FlyPatrolComponent))
	{
		return FlyPatrolComponent->IsHZMGFlyState();
	}
	return false;
}

void APlayerCharacter::EnterFlyPatrol(FString FlyPatrolID, const FString InCarrierId, const FString FlyModleId )
{	
	if (!IsValid(FlyPatrolComponent))
	{	
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::EnterFlyPatrol : FlyPatrolComponent!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::EnterFlyPatrol EntityID[%d] FlyPatrolID=%s InCarrierId=%s FlyModleId=%s"), EntityId, *FlyPatrolID, *InCarrierId,*FlyModleId);
	if (ActorIsPlayer())
	{
		URoleSpaceInterface * Interface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface"), EntityId));
		if (IsValid(Interface))
		{
			(Interface->OnEnterAreaNotifyEvent).AddDynamic(this, &APlayerCharacter::SwitchOffFlyOrbitMode);
		}
	}
	
	FlyPatrolComponent->EnterFlyPatrol(FlyPatrolID, InCarrierId, FlyModleId);
}

void APlayerCharacter::StopFlyPatrol(float DelayTime/*= 0.0f*/)
{
	if (!IsValid(FlyPatrolComponent))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::StopFlyPatrol : FlyPatrolComponent!"));
		return;
	}
	if (ActorIsPlayer())
	{
		URoleSpaceInterface * Interface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface"), EntityId));
		if (IsValid(Interface))
		{
			(Interface->OnEnterAreaNotifyEvent).Remove(this, TEXT("SwitchOffFlyOrbitMode"));

		}
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::StopFlyPatrol EntityID[%d] DelayTime=%f "), EntityId, DelayTime);

	FlyPatrolComponent->StopFlyPatrol(DelayTime);
}

void APlayerCharacter::StopCycleFlyPatrol(FString FlyPatrolID)
{
	if (!IsValid(FlyPatrolComponent))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::StopCycleFlyPatrol : FlyPatrolComponent!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::StopFlyPatrol EntityID[%d] FlyPatrolID=%s "), EntityId, *FlyPatrolID);
	FlyPatrolComponent->StopCycleFlyPatrol(FlyPatrolID);
}

void APlayerCharacter::PauseFlyPatrol()
{
	if (GetSelfEntity() && !GetSelfEntity()->IsPlayer())return;
	if (!IsValid(FlyPatrolComponent))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::PauseFlyPatrol : FlyPatrolComponent!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::PauseFlyPatrol EntityID[%d]"), EntityId);
	FlyPatrolComponent->PauseFlyPatrol();
}

void APlayerCharacter::ReviveFlyPatrol()
{
	if (GetSelfEntity() && !GetSelfEntity()->IsPlayer())return;
	if (!IsValid(FlyPatrolComponent))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::ReviveFlyPatrol : FlyPatrolComponent!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::ReviveFlyPatrol EntityID[%d]"), EntityId);
	FlyPatrolComponent->ReviveFlyPatrol();
}

bool APlayerCharacter::IsPausedFlyPatrol()
{
	if (IsValid(FlyPatrolComponent))
	{
		return FlyPatrolComponent->IsPausedFlyPatrol();
	}
	return false;
}

bool APlayerCharacter::IsFlyPatrolState()
{
	if (IsValid(FlyPatrolComponent))
	{
		 return FlyPatrolComponent->IsFlyPatrolState();
	}
	return false;
}

void APlayerCharacter::EnterFlyToHZMGSpace(const FString fPatrolID, const FString sPatrolID, const int32 sPoint, const int32 pPoint, float speed, FVector enterPos)
{
	KBEngine::Entity* Player = GetSelfEntity();
	if (Player == nullptr || !Player->IsPlayer())
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::EnterFlyToSubSpace : Player !"));
		return;
	}
	if (!IsValid(FlyPatrolComponent))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::EnterFlyToSubSpace : FlyPatrolComponent!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::EnterFlyPatrol EntityID[%d] FlyPatrolID=%s sPatrolID=%s sPoint=%d pPoint=%d enterPos.x=%f enterPos.y=%f enterPos.z=%f"), EntityId, *fPatrolID, *sPatrolID, sPoint, pPoint, enterPos.X, enterPos.Y, enterPos.Z);
	URoleSpaceInterface * Interface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface"), 0));
	if (IsValid(Interface))
	{
		(Interface->OnEnterAreaNotifyEvent).AddDynamic(this, &APlayerCharacter::SwitchOffFlyOrbitMode);
	}
	FlyPatrolComponent->EnterFlyToHZMGSpace(fPatrolID, sPatrolID, sPoint, pPoint, speed, enterPos);
}


void APlayerCharacter::StopFlyToHZMGSpace(const FString FlyID)
{
	KBEngine::Entity* Player = GetSelfEntity();
	if (Player==nullptr ||!Player->IsPlayer()) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::StopFlyToSubSpace : Player!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::EnterFlyPatrol EntityID[%d] FlyPatrolID=%s "), EntityId, *FlyID);
	if (IsValid(FlyPatrolComponent))
	{
		FlyPatrolComponent->StopFlyToHZMGSpace(FlyID);
	}	
}

void APlayerCharacter::ShowAllNavigateGuide(const TArray<FVector>& PathList, int32 QuestID /* = 0 */)
{
	ClearAllNavigateGuide(false);
	NavigateGuidePathList = AnalysicsPathList(PathList, AUTO_NAVIGATE_GUIDE_DISTANCE);
	if (NavigateGuidePathList.Num() <= 1)
	{
		return;
	}
	for (int PathIndex = 0; PathIndex < NavigateGuidePathList.Num();++PathIndex)
	{
		NavigateGuideEffctTypeList.Add(false);
		FVector newPos(NavigateGuidePathList[PathIndex]);
		FHitResult HitOut(ForceInit);
		FCollisionQueryParams TraceParams = FCollisionQueryParams(FName(TEXT("ComputeFloorDistSweep")), true, this);
		if (this->GetWorld()->LineTraceSingleByChannel(HitOut, newPos + FVector(0.0f, 0.0f, 200.0f),
			newPos + FVector(0.0f, 0.0f, -1000.0f), ECC_Visibility, TraceParams))
		{
			newPos.Z = HitOut.Location.Z;
			if (IsValid(HitOut.Component.Get()) && IsValid(HitOut.Component.Get()->GetMaterial(0))
				&& IsValid(HitOut.Component.Get()->GetMaterial(0)->GetBaseMaterial()))
			{
				EBlendMode HitBlendMode = HitOut.Component.Get()->GetMaterial(0)->GetBaseMaterial()->BlendMode;
				if (HitBlendMode == BLEND_Additive || HitBlendMode == BLEND_Translucent)
				{
					NavigateGuideEffctTypeList[PathIndex] = true;
				}
			}
		}
		NavigateGuidePathList[PathIndex] = newPos;
	}
	/*
	int StartPointIndex = 0;
	int EndPointIndex = FMath::Min(NavigateGuidePathList.Num(), StartPointIndex + AUTO_NAVIGATE_GUIDE_SHOW_EFFECT_NUM);
	TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
	for (int PathIndex = StartPointIndex; PathIndex < EndPointIndex; ++PathIndex)
	{
		FString EffectID = AUTO_NAVIGATE_GUIDE_EFFECTID_LIST[0];
		if (NavigateGuideEffctTypeList[PathIndex] == true)
		{
			EffectID = AUTO_NAVIGATE_GUIDE_EFFECTID_LIST[1];
		}
		int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, GetWorld()->GetWorldSettings(), GetWorld()->GetWorldSettings(), FEffectCreate::CreateLambda([DelayThisPtr, PathIndex](AEffectEmitter* Effect)
		{
			if (DelayThisPtr.IsValid())
			{
				APlayerCharacter* ThisPtr = DelayThisPtr.Get();
				if (ThisPtr->NavigateGuidePathList.Num() > 0)
				{
					Effect->SetActorLocation(ThisPtr->NavigateGuidePathList[PathIndex]);
				}
			}
		}));
		NavigateGuideEffectList.Add(EffectUID);
	}
	CheckPlayArriveGuidePoint(StartPointIndex, EndPointIndex);*/

	NavigateParticleUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(AUTO_NAVIGATE_GUIDE_EFFECTID, 0.0f, GetWorld()->GetWorldSettings(), GetWorld()->GetWorldSettings());
}

void APlayerCharacter::ClearAllNavigateGuide(bool IsArrived)
{
	//for (auto GuideEffect : NavigateGuideEffectList)
	//{
	//	UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(GuideEffect);
	//	/*if (IsValid(GuideEffect))
	//	{
	//		GuideEffect->Stop();
	//	}*/	
	//}
	//NavigateGuideEffectList.Empty();
	NavigateGuidePathList.Empty();
	NavigateGuideEffctTypeList.Empty();
	/*if (AutoNavigateHandle.IsValid() && UUECS3GameInstance::Instance)
	{
		ClearTimer(AutoNavigateHandle);
	}*/

	if (NavigateParticleUID == -1)
	{
		return;
	}

	if (IsArrived)		//到达终点后10秒后才停止光效
	{
		FTimerHandle DelayStop;
		int32 UID = NavigateParticleUID;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayStop, FTimerDelegate::CreateLambda([UID]()
		{
			UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(UID);			
		}), 10, false);
	}
	else
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(NavigateParticleUID);		
	}
	NavigateParticleUID = -1;
}

void APlayerCharacter::ClearCrossMapInfos()
{
	URolePerformanceInterface * RolePerformanceInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), 0));
	if (IsValid(RolePerformanceInterface))
	{
		TArray<FCROSS_MAP_TARGET_INFO> CrossMapInfos;
		CrossMapInfos.Empty();
		FCROSS_MAP_TARGET_INFO MapTargetInfo;
		RolePerformanceInterface->SetCrossMapTargetInfo(CrossMapInfos);
		RolePerformanceInterface->SetCurrentMapTargetInfo(MapTargetInfo, false, "", 0);
	}
}

/*
void APlayerCharacter::CheckPlayArriveGuidePoint(const int32& LastStartPointIndex, const int32& LastEndPointIndex)
{
	if (!IsValid(this))
	{
		return;
	}
	TArray<int> PassedPointsIndex;
	KBEngine::Entity* Player = GetSelfEntity();
	if (Player == nullptr)
	{
		CS3_Warning(TEXT("APlayerCharacter::CheckPlayArriveGuidePoint no this entity%d"), EntityId);
		return;
	}
	FVector PlayerPos = Player->Position();
	for (int PathIndex = 0; PathIndex < NavigateGuidePathList.Num(); ++PathIndex)
	{
		float PointDis = FVector::Distance(PlayerPos, NavigateGuidePathList[PathIndex]);
		if (PointDis <= AUTO_NAVIGATE_GUIDE_POINT_CHECK_DISTANCE)
		{
			PassedPointsIndex.Add(PathIndex);
		}
	}
	PassedPointsIndex.Sort();
	int StartPointIndex = LastStartPointIndex;
	if (PassedPointsIndex.Num() > 0 && PassedPointsIndex.Last() >= LastStartPointIndex)
	{
		StartPointIndex = PassedPointsIndex.Last() + 1;
	}
	int NavigateGuidePathStart = FMath::Max(LastEndPointIndex, StartPointIndex);
	int NavigateGuidePathEnd = FMath::Max(LastEndPointIndex, StartPointIndex + AUTO_NAVIGATE_GUIDE_SHOW_EFFECT_NUM);
	NavigateGuidePathEnd = FMath::Min(NavigateGuidePathEnd, NavigateGuidePathList.Num());
	if (StartPointIndex >= LastStartPointIndex + AUTO_NAVIGATE_GUIDE_SHOW_EFFECT_NUM)
	{
		for (auto GuideEffect : NavigateGuideEffectList)
		{
			UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(GuideEffect);
			//if (IsValid(GuideEffect))
			//{
			//	GuideEffect->Stop();
			//}
		}
		NavigateGuideEffectList.Empty();
	}
	else if (StartPointIndex > LastStartPointIndex && StartPointIndex < LastStartPointIndex + AUTO_NAVIGATE_GUIDE_SHOW_EFFECT_NUM)
	{
		int IntervalIndex = StartPointIndex - LastStartPointIndex;
		int EffectEndIndex = IntervalIndex;
		if (NavigateGuideEffectList.Num() > AUTO_NAVIGATE_GUIDE_SHOW_EFFECT_NUM)
		{
			EffectEndIndex = IntervalIndex + NavigateGuideEffectList.Num() - AUTO_NAVIGATE_GUIDE_SHOW_EFFECT_NUM;
		}
		EffectEndIndex = FMath::Min(EffectEndIndex, NavigateGuideEffectList.Num());
		for (int EffectIndex = 0; EffectIndex < EffectEndIndex; ++EffectIndex)
		{
			if (NavigateGuideEffectList.Num() > EffectIndex)
			{
				UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(NavigateGuideEffectList[EffectIndex]);
			}
		}
		NavigateGuideEffectList.RemoveAt(0, EffectEndIndex);
	}

	if (StartPointIndex == NavigateGuidePathList.Num())
	{
		for (auto GuideEffect : NavigateGuideEffectList)
		{
			UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(GuideEffect);
			//if (IsValid(GuideEffect))
			//{
			//	GuideEffect->Stop();
			//}
		}
		NavigateGuideEffectList.Empty();
		return;
	}
	if (NavigateGuidePathList.Num() > AUTO_NAVIGATE_GUIDE_SHOW_EFFECT_NUM && NavigateGuidePathList.Num() > NavigateGuideEffectList.Num())
	{
		TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
		for (int PathIndex = NavigateGuidePathStart; PathIndex < NavigateGuidePathEnd; ++PathIndex)
		{
			FString EffectID = AUTO_NAVIGATE_GUIDE_EFFECTID_LIST[0];
			if (NavigateGuideEffctTypeList[PathIndex] == true)
			{
				EffectID = AUTO_NAVIGATE_GUIDE_EFFECTID_LIST[1];
			}
			int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, GetWorld()->GetWorldSettings(), GetWorld()->GetWorldSettings(), FEffectCreate::CreateLambda([DelayThisPtr, PathIndex](AEffectEmitter* Effect)
			{
				APlayerCharacter* ThisPtr = DelayThisPtr.Get();
				if (ThisPtr->NavigateGuidePathList.Num() > 0)
				{
					Effect->SetActorLocation(ThisPtr->NavigateGuidePathList[PathIndex]);
				}
			}));
			NavigateGuideEffectList.Add(EffectUID);
		}
	}

	TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
	SetTimer(this, AutoNavigateHandle, FTimerDelegate::CreateLambda([DelayThisPtr, StartPointIndex, NavigateGuidePathEnd]() {
		if (DelayThisPtr.IsValid())
		{
			APlayerCharacter* ThisPtr = DelayThisPtr.Get();
			ThisPtr->CheckPlayArriveGuidePoint(StartPointIndex, NavigateGuidePathEnd);
		}
	}), 0.5f, false);

}*/

void APlayerCharacter::GetAutoNavigatePathList(const FVector& StartPos, const FVector& EndPos, FString SpaceName, TArray<FVector>& FinalAutoPathList)
{
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	FinalAutoPathList = UUECS3GameInstance::Instance->AutoNavigatePathMgr->FindAutoPath(SpaceScriptID, StartPos, EndPos);
	if (FinalAutoPathList.Num() == 0 || FinalAutoPathList.Num() == 1)
	{
		GetNormalNavigatePathList(StartPos, EndPos, SpaceName, FinalAutoPathList);
		return;
	}
	else
	{
		FVector Pos0 = FinalAutoPathList[0];
		FVector Pos1 = FinalAutoPathList[1];
		float dotResult = FVector::DotProduct(Pos0 - StartPos, Pos1 - Pos0);
		if (dotResult < 0)	//夹角为钝角
		{
			FinalAutoPathList.Remove(Pos0);
			if (FinalAutoPathList.Num() == 0 || FinalAutoPathList.Num() == 1)
			{
				GetNormalNavigatePathList(StartPos, EndPos, SpaceName, FinalAutoPathList);
				return;
			}
		}
	}

	if (FinalAutoPathList.Num() > 1)
	{
		FVector Pos0 = FinalAutoPathList[0];
		if (FVector::Dist(Pos0, StartPos) > AUTO_NAVIGATE_DIRECT_ARRIVE_DISTANCE)
		{
			TArray<FVector> StartPathList;
			GetNormalNavigatePathList(StartPos, Pos0, SpaceName, StartPathList);
			if (StartPathList.Num() > 0)
			{
				StartPathList.Pop();
				StartPathList.Append(FinalAutoPathList);
				FinalAutoPathList = StartPathList;
			}
			else
			{
				FinalAutoPathList.Empty();
				return;
			}
		}
	}

	if (FVector::Dist(FinalAutoPathList.Last(), EndPos) > AUTO_NAVIGATE_DIRECT_ARRIVE_DISTANCE)
	{
		TArray<FVector> EndPathList;
		GetNormalNavigatePathList(FinalAutoPathList.Last(), EndPos, SpaceName, EndPathList);
		if (EndPathList.Num() > 0)
		{
			FinalAutoPathList.Pop();
			FinalAutoPathList.Append(EndPathList);
		}
		else
		{
			FinalAutoPathList.Empty();
			return;
		}
	}

	if (FVector::Dist(FinalAutoPathList[0], StartPos) > AUTO_NAVIGATE_PATH_START_OR_END_DISTANCE)
	{
		FinalAutoPathList.Insert(StartPos, 0);
	}

	if (FVector::Dist(FinalAutoPathList.Last(), EndPos) > AUTO_NAVIGATE_PATH_START_OR_END_DISTANCE)
	{
		FinalAutoPathList.Add(EndPos);
	}

	GetAdjustedAutoNavigatePathList(FinalAutoPathList);

}

void APlayerCharacter::GetAdjustedAutoNavigatePathList(TArray<FVector>& FinalAutoPathList)
{
	for (int32 Index = 0; Index < FinalAutoPathList.Num(); ++Index)
	{
		FNavLocation ProjectLoc;
		UNavigationSystemV1 *const NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());
		FVector Point = FinalAutoPathList[Index];
		const FVector& EndPos = Point;
		bool bProjectedLocationValid = NavSys->ProjectPointToNavigation(EndPos, ProjectLoc);
		if (bProjectedLocationValid)
		{
			Point = ProjectLoc.Location;
		}
		FinalAutoPathList[Index] = Point;
	}
	if (FinalAutoPathList.Num() > 1 && FVector::Dist(FinalAutoPathList[0], FinalAutoPathList[1]) < AUTO_NAVIGATE_MIN_DISTANCE)
	{
		FinalAutoPathList.RemoveAt(0, 1);
	}
	if (FinalAutoPathList.Num() > 1 && FVector::Dist(FinalAutoPathList[FinalAutoPathList.Num() - 2], FinalAutoPathList.Last()) < AUTO_NAVIGATE_MIN_DISTANCE)
	{
		FinalAutoPathList.Pop();
	}
}


void APlayerCharacter::GetBestNavigatePathList(const FVector& StartPos, const FVector& EndPos, FString SpaceName, TArray<FVector>& FinalAutoPathList)
{
	GetAutoNavigatePathList(StartPos, EndPos, SpaceName, FinalAutoPathList);
	if (FinalAutoPathList.Num() < 1)
	{
		GetNormalNavigatePathList(StartPos, EndPos, SpaceName, FinalAutoPathList);
	}
}

void APlayerCharacter::GetNormalNavigatePathList(const FVector& StartPos, const FVector& EndPos, FString SpaceName, TArray<FVector>& FinalAutoPathList)
{
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (SpaceScriptID.Equals(SpaceName))
	{
		UNavigationSystemV1 *const NavSys =  FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());;
		/*const ANavigationData* NavigationData = NULL;
		const FNavAgentProperties& NavAgentProperties = GetCharacterMovement()->GetNavAgentPropertiesRef();
		NavigationData = NavSys->GetNavDataForProps(NavAgentProperties);
		APlayerController* PlayerController = GetWorld()->GetFirstPlayerController();
		FPathFindingQuery Query(GetCharacterMovement(), *NavigationData, StartPos, EndPos, UNavigationQueryFilter::GetQueryFilter(*NavigationData, GetCharacterMovement(), UNavigationQueryFilter::StaticClass()));
		Query.SetNavAgentProperties(NavAgentProperties);
		Query.SetAllowPartialPaths(false);
		const FPathFindingResult Result = NavSys->FindPathSync(Query, EPathFindingMode::Hierarchical);
		UNavigationPath* ResultPath = NewObject<UNavigationPath>(NavSys);
		if (Result.IsSuccessful())
		{
		ResultPath->SetPath(Result.Path);
		}
		AutoNavPathPoints = ResultPath->PathPoints;*/
		UNavigationPath *const NavPath = NavSys->FindPathToLocationSynchronously(GetWorld(), StartPos, EndPos, GetWorld()->GetFirstPlayerController());
		if (NavPath != NULL && !NavPath->IsPartial() && NavPath->PathPoints.Num() > 0)
		{
			FinalAutoPathList = NavPath->PathPoints;
		}
	}
}

const TArray<FVector>& APlayerCharacter::GetAutoNavPathPoints()
{
	return AutoNavPathPoints;
}

const TArray<FVector>& APlayerCharacter::GetNavigateGuidePathList()
{
	return NavigateGuidePathList;
}

TArray<UItemBase*> APlayerCharacter::GetItemTeleportStone()
{
	TArray<UItemBase*> ItemList;
	URoleKitBagInterface* KitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (IsValid(KitbatInst))
	{
		ItemList = KitbatInst->GetItemListByItemScript(TEXT("ItemTeleportStone"));
	}
	return ItemList;
}

bool APlayerCharacter::CheckItemTeleportStone()
{
	//判断背包是否存在神行石和是否不在CD中
	TArray<UItemBase*> ItemList = GetItemTeleportStone();
	if (ItemList.Num() == 0)
	{
		return false;
	}
	for (auto ItemInst : ItemList)
	{
		if (ItemInst->IsCoolDowning())
		{
			return false;
		}
	}
	return true;
}

void APlayerCharacter::StartAutoNavigate(const FVector& DstPosition, float NearbyRange /* = 2.0f */, FString DstSpaceName/* ="" */, int AutoQuestID /* = 0 */, bool IsSearch /* = false */,int32 GossipWithType /*=0*/)
{
	if (IsState(ENTITY_STATE::EntityStateDead))
	{
		return;
	}
	ACS3PlayerController* CS3PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(CS3PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::StartAutoNavigate : CS3PlayerController!"));
		return;
	}
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	FString FinalSpaceName = DstSpaceName;
	if (DstSpaceName.Equals(""))
	{
		FinalSpaceName = SpaceScriptID;
	}
	if (SpaceScriptID.Equals(FinalSpaceName))
	{
		if (NavigateNPCInfo.TeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportPoint)
		{
			//只有第一次是跨地图并且传送点传送才会走这里
			if (IsState(ENTITY_STATE::EntityStateFight))
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(4298);//当前为战斗状态，无法使用传送点进行寻路!
				ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, true);
				return;
			}
			if (AutoQuestID != 0)
			{
				//任务传送
				NavigateNPCInfo.NPCScriptID = "";
				NavigateNPCInfo.PointTeleportType = ENUM_POINT_TELEPORT_TYPE::TELEPORT_BY_NONE;
				ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, true);

			}
			else
			{
				//非任务传送，走神行石规则
				TArray<UItemBase*> ItemList = GetItemTeleportStone();
				if (ItemList.Num() != 0)
				{
					NavigateNPCInfo.NPCScriptID = "";
					NavigateNPCInfo.PointTeleportType = ENUM_POINT_TELEPORT_TYPE::TELEPORT_BY_TELEPORTSTONE;
					ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, true);
				}
				else
				{
					CS3_Warning(TEXT("No NavigateData in DstPosition:%s DstSpaceName:%s"), *DstPosition.ToString(), *DstSpaceName);
					UUECS3GameInstance::Instance->MessageManager->ShowMessage(2400);//寻路失败，目标点无法到达。
					ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, true);
				}
			}
			return;
		}

		FVector PlayerLocation = GetActorLocation();
		if (IsSearch)
		{
			GetNormalNavigatePathList(PlayerLocation, DstPosition, FinalSpaceName, AutoNavPathPoints);
		}
		else
		{
			GetBestNavigatePathList(PlayerLocation, DstPosition, FinalSpaceName, AutoNavPathPoints);
		}
		if (AutoNavPathPoints.Num() <= 1)
		{
			UCrossMapNavigateMgr* CrossMapNavigateMgr = UUECS3GameInstance::Instance->CrossMapNavigateMgr;
			if (IsValid(CrossMapNavigateMgr))
			{
				FCROSS_MAP_TARGET_INFO MapTargetInfo;
				CrossMapNavigateMgr->GetSameSpaceTeleportPointInfo(FinalSpaceName, PlayerLocation, DstPosition, MapTargetInfo);
				if (!MapTargetInfo.Param1.IsEmpty())
				{
					if (AutoQuestID != 0)
					{
						//任务寻路
						NavigateNPCInfo.NPCScriptID = "";
						NavigateNPCInfo.TeleportType = MapTargetInfo.TeleportType;
						NavigateNPCInfo.Param1 = MapTargetInfo.Param1;
						NavigateNPCInfo.PointTeleportType = ENUM_POINT_TELEPORT_TYPE::TELEPORT_BY_NONE;
						FString DstName = CrossMapNavigateMgr->GetTeleportPointDstName(NavigateNPCInfo.Param1);
						TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(2411, DstName, FBtnClick::CreateLambda([DelayThisPtr](RT_BTN_TYPE RtType)
						{
							ACS3PlayerController* CS3PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
							if (DelayThisPtr.IsValid() && IsValid(CS3PlayerController))
							{
								APlayerCharacter* ThisPtr = DelayThisPtr.Get();
								if (RtType == RT_BTN_TYPE::RT_OK)
								{
									ThisPtr->ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, true);
								}
								else
								{
									ThisPtr->ClearNavigateNPCInfo();
									ThisPtr->ClearCrossMapInfos();
									ThisPtr->ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, true);
								}
							}
						}));
					}
					else
					{
						//非任务寻路
						TArray<UItemBase*> ItemList = GetItemTeleportStone();
						if (ItemList.Num() != 0)
						{
							NavigateNPCInfo.NPCScriptID = "";
							NavigateNPCInfo.TeleportType = MapTargetInfo.TeleportType;
							NavigateNPCInfo.Param1 = MapTargetInfo.Param1;
							NavigateNPCInfo.PointTeleportType = ENUM_POINT_TELEPORT_TYPE::TELEPORT_BY_TELEPORTSTONE;
							ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, true);
						}
						else
						{
							///<同一地图玩家在目的地附近CST-5292   
							if (FVector::Distance(PlayerLocation, DstPosition) <= NearbyRange * 100.0f)
							{
								NavigateNPCInfo.DstPosition = DstPosition;
								NavigateNPCInfo.SpaceName = DstSpaceName;
								NavigateNPCInfo.IsSearch = IsSearch;
								NavigateNPCInfo.NearbyRange = NearbyRange;
								NavigateNPCInfo.AutoQuestID = AutoQuestID;
								NavigateNPCInfo.GossipWithType = GossipWithType;
								ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, true);					
							}
							else
							{
								CS3_Warning(TEXT("No NavigateData in DstPosition:%s DstSpaceName:%s"), *DstPosition.ToString(), *DstSpaceName);
								UUECS3GameInstance::Instance->MessageManager->ShowMessage(2400);//寻路失败，目标点无法到达。
								ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, false);						
							}
						}
					}	
				}
				else
				{
					///<同一地图玩家在目的地附近CST-5292   
					if (FVector::Distance(PlayerLocation, DstPosition) <= NearbyRange * 100.0f)
					{
						NavigateNPCInfo.DstPosition = DstPosition;
						NavigateNPCInfo.SpaceName = DstSpaceName;
						NavigateNPCInfo.IsSearch = IsSearch;
						NavigateNPCInfo.NearbyRange = NearbyRange;
						NavigateNPCInfo.AutoQuestID = AutoQuestID;
						NavigateNPCInfo.GossipWithType = GossipWithType;
						ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, true);						
					}
					else
					{
						CS3_Warning(TEXT("No NavigateData in DstPosition:%s DstSpaceName:%s"), *DstPosition.ToString(), *DstSpaceName);
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(2400);//寻路失败，目标点无法到达。
						ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, false);
					}
				}
				return;
			}
			else
			{
				CS3_Warning(TEXT("No NavigateData in DstPosition:%s DstSpaceName:%s"), *DstPosition.ToString(), *DstSpaceName);
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(2400);//寻路失败，目标点无法到达。
				ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, false);
				return;
			}
		}	
		SubroutineAutoNavigate(DstPosition, NearbyRange, FinalSpaceName, AutoQuestID);
		NavigateNPCInfo.DstPosition = DstPosition;
		NavigateNPCInfo.SpaceName = DstSpaceName;
		NavigateNPCInfo.IsSearch = IsSearch;
		NavigateNPCInfo.NearbyRange = NearbyRange;
		NavigateNPCInfo.AutoQuestID = AutoQuestID;
		NavigateNPCInfo.GossipWithType = GossipWithType;
	}
}

void APlayerCharacter::SubroutineAutoNavigate(const FVector& DstPosition, float NearbyRange /* = 0.0f */, FString FinalSpaceName/* ="" */, int AutoQuestID /* = 0 */, bool IsSearch /* = false */)
{
	FVector FirstPoint;
	FVector PlayerLocation = GetActorLocation();
	int32 PointIndex = 0;
	if (AutoNavPathPoints.Num() > 1 && FVector::Dist2D(PlayerLocation, AutoNavPathPoints[0]) < AUTO_NAVIGATE_MIN_DISTANCE)
	{
		FirstPoint = AutoNavPathPoints[1];
		PointIndex = 1;
	}
	else
	{
		FirstPoint = AutoNavPathPoints[0];
	}
	ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
	if (IsValid(PlayerController))
	{
		URolePerformanceInterface * RolePerformanceInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), 0));
		if (!(FVector::Dist(PlayerLocation, DstPosition) <= NearbyRange * 100.0f && IsValid(RolePerformanceInterface) && RolePerformanceInterface->GetNavigateActionType() == ENUM_NAVIGATE_ACTION_TYPE::NavigateActionStall))
		{
			if (!IsCarrierState())
			{
				if (IsState(ENTITY_STATE::EntityStateFree))
				{
					URolePetInterface * RolePetInterface = Cast<URolePetInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePetInterface"), EntityId));
					if (RolePetInterface)
					{
						RolePetInterface->RequestTransformPetFC();
					}
					//KBEngine::FVariantArray args;
					//if (this->GetSelfEntity() != nullptr)
					//{
					//	this->GetSelfEntity()->CellCall(TEXT("transformPet"), args);
					//}
				}
			}
		}		
	
		TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
		PlayerController->AutoNavigateToLocation(FirstPoint, FinalSpaceName, NearbyRange, FTraceCallback::CreateLambda([DelayThisPtr, FinalSpaceName, FirstPoint, NearbyRange](bool IsSuccess)
		{
			if (DelayThisPtr.IsValid())
			{
				APlayerCharacter* ThisPtr = DelayThisPtr.Get();
				ThisPtr->CheckAutoNavigate(FinalSpaceName, FirstPoint, NearbyRange, IsSuccess);
			}
		}));
	}
	else
	{
		//当取消自动移动时只有第一个参数和最后一个参数是有效参数。
		ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, false);
		//StopAutoNavigate(false);
	}	

	KBEngine::Entity* ServerEntity = GetSelfEntity();
	if (ServerEntity != nullptr)
	{
		int32 OnWaterArea = ServerEntity->GetDefinedProperty(TEXT("onWaterArea")).GetValue<int32>();
		if (OnWaterArea != 0 && !AutoNavigateWaterJumpHandle.IsValid())
		{
			if (IsValid(UUECS3GameInstance::Instance))
			{
				TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, AutoNavigateWaterJumpHandle, 
					FTimerDelegate::CreateLambda([DelayThisPtr]() {
					if (DelayThisPtr.IsValid())
					{
						APlayerCharacter* ThisPtr = DelayThisPtr.Get();
						ThisPtr->OnWaterJumpBegin();
					}
				}), AUTO_NAVIGATE_WATER_JUMP_CHECK_TIME, true);
			}
		}
	}

	ShowAllNavigateGuide(AutoNavPathPoints, AutoQuestID);
}

void APlayerCharacter::CheckAutoNavigate(FString DstSpaceName, const FVector& DstPosition, float NearbyRange, bool IsSuccess)
{
	ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::CheckAutoNavigate : PlayerController!"));
		return;
	}
	if (IsSuccess)
	{
		const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
		if (!DstSpaceName.Equals(SpaceScriptID))
		{
			return;
		}
		int PointIndex = AutoNavPathPoints.Find(DstPosition);
		if (PointIndex == AutoNavPathPoints.Num() - 1 || (AutoNavPathPoints.Num() > 0 && FVector::Dist(AutoNavPathPoints.Last(), GetActorLocation()) <= NearbyRange * 100.0f))
		{
			//当取消自动移动时只有第一个参数和最后一个参数是有效参数。
			ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, true);
			//StopAutoNavigate(true);
		}
		else
		{
			FVector NextPoint = AutoNavPathPoints[PointIndex + 1];
			
			if (IsValid(PlayerController))
			{
				TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
				PlayerController->AutoNavigateToLocation(NextPoint, DstSpaceName, NearbyRange, FTraceCallback::CreateLambda([DelayThisPtr, DstSpaceName, NextPoint, NearbyRange](bool IsSuccess)
				{
					if (DelayThisPtr.IsValid())
					{
						APlayerCharacter* ThisPtr = DelayThisPtr.Get();
						ThisPtr->CheckAutoNavigate(DstSpaceName, NextPoint, NearbyRange, IsSuccess);
					}
				}));
			}
			else
			{
				//当取消自动移动时只有第一个参数和最后一个参数是有效参数。
				ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, false);
				//StopAutoNavigate(false);
			}
		}
	}
	else
	{
		//当取消自动移动时只有第一个参数和最后一个参数是有效参数。
		ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, false);
		//StopAutoNavigate(false);
	}
}

bool APlayerCharacter::canTargetActorNavigate(AServerCharacter* ServerCharacter)
{
	//如果目标无效或者是玩家类型
	if (!IsValid(ServerCharacter) || (ServerCharacter->GetClass()->IsChildOf(APlayerCharacter::StaticClass())))
	{
		return false;
	}
	//如果是Monster
	if (ServerCharacter->GetClass()->IsChildOf(AMonsterCharacter::StaticClass()))
	{
		if (!ServerCharacter->IsState(ENTITY_STATE::EntityStateDead))
		{
			return true;
		}
		return false;
	}
	//如果是SpellBox
	if (ServerCharacter->GetClass()->IsChildOf(ASpellBoxCharacter::StaticClass()))
	{
		if (ServerCharacter->GetSelfEntity() == nullptr) 
			{
			CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::CheckAutoNavigate : GetSelfEntity()!"));
				return false;
			}

		VISIBLE_STYLE rule = UGolbalBPFunctionLibrary::VisibleManager()->GetModelVisibleStyle(ServerCharacter->GetSelfEntity()->Actor());
		switch (rule)
		{
		case VISIBLE_STYLE::VISIBLE_STYLE_FALSE:
		{
			return false;
		}
		case VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT:
		{
			return true;
		}
		case VISIBLE_STYLE::VISIBLE_STYLE_TRUE:
		{
			return true;
		}
		default:	return false;
		}
	}
	//其余类型默认可以被寻路
	return true;

}

void APlayerCharacter::StopAutoNavigate(bool IsArrived)
{
	AutoNavPathPoints.Empty();
	if (AutoNavigateWaterJumpHandle.IsValid() && UUECS3GameInstance::Instance)
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(AutoNavigateWaterJumpHandle);
		}
	}
	if (IsArrived)
	{
		if (!NavigateNPCInfo.NPCScriptID.IsEmpty())
		{
			AServerCharacter* TargetCharacter = nullptr;
			TArray<FString> NPCIDArray = UGolbalBPFunctionLibrary::SplitString(NavigateNPCInfo.NPCScriptID, true, TEXT("|"));
			TArray<AActor*> ActorsInRange = UGolbalBPFunctionLibrary::GetActorsInRange(AServerCharacter::StaticClass(), QUEST_NAVIGATE_FIND_RANGE);
			bool IsFind = false;
			float MinDist = MAX_flt;
			for (auto TargetActor : ActorsInRange)
			{
				AServerCharacter* ServerCharacter = Cast<AServerCharacter>(TargetActor);
				if (canTargetActorNavigate(ServerCharacter))
				{
					KBEngine::Entity* ServerEntity = ServerCharacter->GetSelfEntity();
					if (ServerEntity != nullptr)
					{
						FString ScriptID = ServerEntity->GetDefinedProperty(TEXT("scriptID"));
						if (NPCIDArray.Contains(ScriptID))
						{
							float ActorDist = UGolbalBPFunctionLibrary::GetActorDistance(ServerCharacter, this);
							if (ActorDist < MinDist)
							{
								MinDist = ActorDist;
								TargetCharacter = ServerCharacter;
								IsFind = true;
							}
						}
					}
				}
			}
			ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
			if (IsValid(PlayerController))
			{
				if (IsFind && IsValid(TargetCharacter))
				{
					if (UGolbalBPFunctionLibrary::GetActorDistance(this, TargetCharacter) < NavigateNPCInfo.NearbyRange * 100.0f)
					{
						OnNavigateEndProcess(TargetCharacter);
					}
					else
					{
						TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
						TWeakObjectPtr<AServerCharacter> DelayTargetCharacterPtr(TargetCharacter);
						PlayerController->TraceTargetActor(TargetCharacter, NavigateNPCInfo.NearbyRange, nullptr, false, FTraceCallback::CreateLambda([DelayThisPtr, DelayTargetCharacterPtr](bool IsSuccess)
						{
							if (IsSuccess && DelayThisPtr.IsValid() && DelayTargetCharacterPtr.IsValid())
							{
								APlayerCharacter* ThisPtr = DelayThisPtr.Get();
								AServerCharacter* TargetCharacterPtr = DelayTargetCharacterPtr.Get();
								ThisPtr->OnNavigateEndProcess(TargetCharacterPtr);
							}
						}));
					}
				}
				//PlayerController->OnTestSpaceAllQuestNavigate(NavigateNPCInfo.SpaceName, NavigateNPCInfo.NPCScriptID);
			}

		}
		else
		{
			OnNavigateEndProcess(nullptr);
		}
	}
	else
	{
		StopPlayerMove();
		ClearNavigateNPCInfo();
		ClearCrossMapInfos();
		URolePerformanceInterface * RolePerformanceInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), 0));
		if (IsValid(RolePerformanceInterface))
		{
			RolePerformanceInterface->OnNavigateStop();
			RolePerformanceInterface->SetNavigateActionType(ENUM_NAVIGATE_ACTION_TYPE::NavigateActionDefault);
		}
	}
	ClearAllNavigateGuide(IsArrived);
}

void APlayerCharacter::AutomaticMount()
{
}


bool APlayerCharacter::GetNPCPositionByQuest(FString DstSpaceName, FString NPCScriptID, bool IsCompletedQuest, FString QuestTaskClass, FVector& NPCPosition)
{
	if (!NPCScriptID.IsEmpty())
	{
		TArray<FString> NPCIDArray = UGolbalBPFunctionLibrary::SplitString(NPCScriptID, true, TEXT("|"));
		TArray<AActor*> ActorsInRange = UGolbalBPFunctionLibrary::GetActorsInRange(AServerCharacter::StaticClass(), QUEST_NAVIGATE_FIND_RANGE);
		bool IsFind = false;
		float MinDist = MAX_flt;
		for (auto TargetActor : ActorsInRange)
		{
			AServerCharacter* ServerCharacter = Cast<AServerCharacter>(TargetActor);
			if (canTargetActorNavigate(ServerCharacter))
			{
				KBEngine::Entity* ServerEntity = ServerCharacter->GetSelfEntity();
				if (ServerEntity != nullptr)
				{
					FString ScriptID = ServerEntity->GetDefinedProperty(TEXT("scriptID"));
					if (NPCIDArray.Contains(ScriptID))
					{
						float ActorDist = UGolbalBPFunctionLibrary::GetActorDistance(ServerCharacter, this);
						if (ActorDist < MinDist)
						{
							MinDist = ActorDist;
							NPCPosition = ServerEntity->Position();
							NPCPosition.Z -= ServerCharacter->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();	//将寻路目标的位置改到脚底所在位置。
							IsFind = true;
						}
					}
				}
			}
		}

		if (IsFind)
		{
			return true;
		}
		else
		{
			UGolbalBPFunctionLibrary::GetNPCPositionFromTable(DstSpaceName, NPCScriptID, NPCPosition);
			if (NPCPosition.IsZero())
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(2402, NPCScriptID);//刷新点表格中没有对应的NPCID
			}
			return false;
		}

	}
	return false;
}

void APlayerCharacter::StartQuestNavigate(bool IsCompletedQuest, FString QuestTaskClass /* = "" */, FString NPCScriptID /* = "" */, FString DstSpaceName /* = "" */, FVector FinalPosition /* = FVector::ZeroVector */, float NearbyRange /* = 2.0f */, int AutoQuestID /* = 0 */, bool IsCrossMap /* = false */, int32 GossipWithType/* = 0*/)
{
	if (IsState(ENTITY_STATE::EntityStateDead))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(4297);//当前为死亡状态，无法进行寻路！
		return;
	}
	FVector NPCPosition = FVector::ZeroVector;
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	FString FinalSpaceName = DstSpaceName;
	if (DstSpaceName.Equals(""))
	{
		FinalSpaceName = SpaceScriptID;
	}
	UMapManager* MapManager = UUECS3GameInstance::Instance->MapManager;
	bool IsInPlane = MapManager->IsPlaneSpace(FinalSpaceName);
	bool IsInCopy = MapManager->IsCopySpace(FinalSpaceName);
	if ((IsInPlane || IsInCopy) && IsCrossMap && SpaceScriptID.Equals(FinalSpaceName))
	{
		return;
	}
	if (IsInPlane && !SpaceScriptID.Equals(FinalSpaceName))
	{
		FinalSpaceName = MapManager->GetRelatedMapScriptID(FinalSpaceName);
	}
	bool IsSearch = false;
	if (SpaceScriptID.Equals(FinalSpaceName))
	{
		if (NPCScriptID == "")
		{
			NPCPosition = FinalPosition;
		}
		else
		{
			if (!IsInPlane)
			{
				IsSearch = GetNPCPositionByQuest(FinalSpaceName, NPCScriptID, IsCompletedQuest, QuestTaskClass, NPCPosition);
			}
			else
			{
				IsSearch = GetNPCPositionByQuest(DstSpaceName, NPCScriptID, IsCompletedQuest, QuestTaskClass, NPCPosition);
			}
		}
		if (!NPCPosition.IsZero())
		{
			NavigateNPCInfo.NPCScriptID = NPCScriptID;
			ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
			if (IsValid(PlayerController)&& IsValid(PlayerController->GetAtkStateMar()))
			{
				if (NavigateNPCInfo.TeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportPoint)
				{
					if (IsState(ENTITY_STATE::EntityStateFight))
					{
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(4298);//当前为战斗状态，无法使用传送点进行寻路!
						return;
					}
					//如果是传送点传送，则玩家需要确认是否传送
					//TArray<UItemBase*> ItemList = GetItemTeleportStone();
					if (AutoQuestID != 0) //
					{
						UCrossMapNavigateMgr* CrossMapNavigateMgr = UUECS3GameInstance::Instance->CrossMapNavigateMgr;
						if (!IsValid(CrossMapNavigateMgr))
						{
							CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::StartQuestNavigate : CrossMapNavigateMgr!"));
							return;
						}
						FString DstName = CrossMapNavigateMgr->GetTeleportPointDstName(NavigateNPCInfo.Param1);
						TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(2411, DstName, FBtnClick::CreateLambda([DelayThisPtr, NPCPosition, NearbyRange, FinalSpaceName, AutoQuestID, IsSearch, GossipWithType](RT_BTN_TYPE RtType)
						{
							if (DelayThisPtr.IsValid())
							{
								APlayerCharacter* ThisPtr = DelayThisPtr.Get();
								if (RtType == RT_BTN_TYPE::RT_OK)
								{
									ThisPtr->ActivateNavigateMoveModeOperation(true, NPCPosition, NearbyRange, FinalSpaceName, AutoQuestID, IsSearch, false, GossipWithType);
									//StartAutoNavigate(NPCPosition, NearbyRange, FinalSpaceName, AutoQuestID, IsSearch);
								}
								else
								{
									ThisPtr->ClearNavigateNPCInfo();
									ThisPtr->ClearCrossMapInfos();
								}
							}
						}));
					}
					else
					{
						ActivateNavigateMoveModeOperation(true, NPCPosition, NearbyRange, FinalSpaceName, AutoQuestID, IsSearch, false, GossipWithType);
					}
				}
				else
				{
					ActivateNavigateMoveModeOperation(true, NPCPosition, NearbyRange, FinalSpaceName, AutoQuestID, IsSearch, false,GossipWithType);
					//StartAutoNavigate(NPCPosition, NearbyRange, FinalSpaceName, AutoQuestID, IsSearch);
				}

			}
		}
	}
}

void APlayerCharacter::StartCrossMapNavigate(FString DstSpaceName, bool IsCompletedQuest, FString QuestTaskClass /*= ""*/, FString NPCScriptID /*= ""*/, FVector FinalPosition /*= FVector::ZeroVector*/, float NearbyRange /*= 2.0f*/, int AutoQuestID /*= 0*/, ENUM_NAVIGATE_ACTION_TYPE NavigateActionType /*= ENUM_NAVIGATE_ACTION_TYPE::NavigateActionDefault*/,int32 GossipWithType/*=0*/)
{
	ACS3PlayerController* CS3PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(CS3PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::StartCrossMapNavigate : CS3PlayerController!"));
		return;
	}
	URolePerformanceInterface * RolePerformanceInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), 0));
	if (IsValid(RolePerformanceInterface))
	{
		RolePerformanceInterface->SetNavigateActionType(NavigateActionType);
	}
	EMovementMode CurrMovementMode = GetCharacterMovement()->MovementMode;
	if (CurrMovementMode != EMovementMode::MOVE_None && CurrMovementMode != EMovementMode::MOVE_Walking && CurrMovementMode != EMovementMode::MOVE_NavWalking)
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(2412);//寻路失败，目标点无法到达。
		ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, false);
		if (IsValid(RolePerformanceInterface))
		{
			RolePerformanceInterface->OnNavigateStop();
		}
		return;
	}
	StopPlayerMove();
	float NewNearbyRange = NearbyRange;
	if (!NPCScriptID.IsEmpty())
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const FNPC_DATA* NpcData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC)->GetRow<FNPC_DATA>(NPCScriptID);
		if (NpcData)
		{
			NewNearbyRange = UUECS3GameInstance::Instance->GameDefault->NPCTalkStartDistance;
		}
	}
	const FString StartSpaceName = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	FString FinalSpaceName = DstSpaceName;
	if (DstSpaceName.Equals(""))
	{
		FinalSpaceName = StartSpaceName;
	}
	if (StartSpaceName.Equals(FinalSpaceName))
	{
		NavigateNPCInfo.TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportDefault;
		StartQuestNavigate(IsCompletedQuest, QuestTaskClass, NPCScriptID, FinalSpaceName, FinalPosition, NewNearbyRange, AutoQuestID, false, GossipWithType);
	}
	else
	{
		UMapManager* MapManager = UUECS3GameInstance::Instance->MapManager;
		bool IsInPlane = MapManager->IsPlaneSpace(StartSpaceName);
		bool IsInCopy = MapManager->IsCopySpace(StartSpaceName);
		if (IsInPlane || IsInCopy)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(2401);//寻路失败，请完成当前剧情内容。
			return;
		}
		UCrossMapNavigateMgr* CrossMapNavigateMgr = UUECS3GameInstance::Instance->CrossMapNavigateMgr;
		if (IsValid(CrossMapNavigateMgr))
		{
			FVector PlayerLocation = GetActorLocation();
			TArray<FCROSS_MAP_TARGET_INFO> CrossMapPaths = CrossMapNavigateMgr->FindCrossMapPath(StartSpaceName, FinalSpaceName, PlayerLocation, FinalPosition, NPCScriptID, AutoQuestID);
			if (CrossMapPaths.Num() == 0)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(2400);//寻路失败，目标点无法到达。
				ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, false);
				return;
			}
			if (IsValid(RolePerformanceInterface) && CrossMapPaths.Num() > 0)
			{
				RolePerformanceInterface->StartPerformCrossMapNavigate(CrossMapPaths, FinalSpaceName, IsCompletedQuest, QuestTaskClass, NPCScriptID, FinalPosition, NewNearbyRange, AutoQuestID);
			}
		}
	}
}

void APlayerCharacter::OnStartCrossMapNavigate(FCROSS_MAP_QUEST_TARGET_INFO& MapQuestTargetInfo)
{
	bool IsCompletedQuest = MapQuestTargetInfo.IsCompletedQuest;
	FString QuestTaskClass = MapQuestTargetInfo.QuestTaskClass;
	int AutoQuestID = MapQuestTargetInfo.AutoQuestID;
	FString NPCScriptID = MapQuestTargetInfo.TargetInfo.ScriptID;
	FString DstSpaceName = MapQuestTargetInfo.TargetInfo.SpaceName;
	FVector FinalPosition = MapQuestTargetInfo.TargetInfo.Position;

	NavigateNPCInfo.TeleportType = MapQuestTargetInfo.TargetInfo.TeleportType;
	NavigateNPCInfo.Param1 = MapQuestTargetInfo.TargetInfo.Param1;
	NavigateNPCInfo.Param2 = MapQuestTargetInfo.TargetInfo.Param2;
	NavigateNPCInfo.Param3 = MapQuestTargetInfo.TargetInfo.Param3;
	if (IsCarrierState())
	{
		StartQuestNavigate(IsCompletedQuest, QuestTaskClass, NPCScriptID, DstSpaceName, FinalPosition, 4.0f, AutoQuestID, true, MapQuestTargetInfo.GossipWithType);
	}
	else
	{
		StartQuestNavigate(IsCompletedQuest, QuestTaskClass, NPCScriptID, DstSpaceName, FinalPosition, 2.0f, AutoQuestID, true, MapQuestTargetInfo.GossipWithType);
	}

}

void APlayerCharacter::OnWaterJumpBegin()
{
	float Probability = FMath::RandRange(0.0f, 1.0f);
	if (Probability <= AUTO_NAVIGATE_WATER_JUMP_PROBABILITY)
	{
		ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
		if (IsValid(PlayerController))
		{
			PlayerController->StartJumpInAutoNavigate();
		}
	}
}

void APlayerCharacter::MoveItem(int32 SrcOrder, int32 DstOrder)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::MoveItem EntityID[%d] SrcOrder=%d DstOrder=%d"), EntityId, SrcOrder, DstOrder);
	EKITBAGTYPE KitBagType = UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(SrcOrder);;
	switch (KitBagType)
	{
	case EKITBAGTYPE::EQUIP:
	{
		URoleKitBagInterface * RoleKitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), EntityId));
		if (RoleKitBagInterface)
		{
			RoleKitBagInterface->RPC_unWieldEquip(FString::FromInt(SrcOrder));
		}

		//KBEngine::Entity* Player = GetSelfEntity();
		//if (Player == nullptr) 
		//{
		//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::MoveItem : Player!"));
		//	return;
		//}
		//KBEngine::FVariantArray Args;
		//Args.Add(SrcOrder);
		//Player->CellCall(TEXT("CELL_unWieldEquip"), Args);
		break;
	}
	case EKITBAGTYPE::COMMON:
	case EKITBAGTYPE::QUEST:
	{
		UItemBase* item = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0))->FindItemByOrder(DstOrder);
		if (item && IsValid(item))
		{
			if (item->IsEquip())
			{
				KBEngine::Entity* Player = GetSelfEntity();
				if (Player == nullptr)
				{
					CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::MoveItem : Player!"));
					return;
				}
				URoleKitBagInterface * RoleKitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), EntityId));
				if (RoleKitBagInterface)
				{
					RoleKitBagInterface->RPC_swapItem(FString::FromInt(SrcOrder), FString::FromInt(DstOrder));
				}
			}
		}
		break;
	}
	case EKITBAGTYPE::CRYSTAL:break;
	case EKITBAGTYPE::STORE:break;
	}
}

void APlayerCharacter::OnRoleOnWaterAreaChange(const int32 onWaterArea)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::OnRoleOnWaterAreaChange EntityID[%d] onWaterArea=%d "), EntityId, onWaterArea);
	if (onWaterArea)
	{
		ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
		if (IsValid(PlayerController))
		{
			CS3_MOVE_TYPE MoveType = PlayerController->GetMoveType();
			if (MoveType == CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE && !AutoNavigateWaterJumpHandle.IsValid())
			{
				if (IsValid(UUECS3GameInstance::Instance))
				{
					TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
					UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, AutoNavigateWaterJumpHandle, 
						FTimerDelegate::CreateLambda([DelayThisPtr]() {
						if (DelayThisPtr.IsValid())
						{
							APlayerCharacter* ThisPtr = DelayThisPtr.Get();
							ThisPtr->OnWaterJumpBegin();
						}
					}), AUTO_NAVIGATE_WATER_JUMP_CHECK_TIME, true);
				}
			}
		}
	}
	else
	{
		if (AutoNavigateWaterJumpHandle.IsValid())
		{
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(AutoNavigateWaterJumpHandle);
			}
		}
	}
}

bool APlayerCharacter::HasRoleFlag(ROLE_FLAG RoleFlag)
{
	KBEngine::Entity* Player = GetSelfEntity();
	if (Player == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::HasRoleFlag : Player!"));
		return false;
	}
	UGameObjectInterface* interface_ = Cast<UGameObjectInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (!IsValid(interface_) || !interface_->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		return false;
	}

	int64 Flags = Player->GetDefinedProperty(TEXT("flags")).GetValue<int64>();
	int64 Flag = int64(1) << int64(RoleFlag);
	return (Flags & Flag) == Flag;
}

void APlayerCharacter::OnTriggerPlane(const FString SpaceScriptID, bool IsLeave /*= false*/)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::OnTriggerPlane EntityID[%d] SpaceScriptID=%s IsLeave=%d"), EntityId,*SpaceScriptID, IsLeave);
	KBEngine::Entity* Player = GetSelfEntity();
	if (Player == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::OnTriggerPlane : Player!"));
		return;
	}
	TriggerPlaneEffect(IsLeave);
	GotoSpacePlane_(SpaceScriptID);
}

void APlayerCharacter::GotoSpacePlane_(const FString SpaceScriptID)
{
	KBEngine::Entity* Player = GetSelfEntity();
	if (Player == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::GotoSpacePlane_ : Player!"));
		return;
	}
	FVector Location = GetActorLocation();
	FVector Direction = FVector::ZeroVector;
	Direction.Z = GetActorRotation().Euler().Z;
	KBEngine::FVariantArray Args;
	Args.Add(SpaceScriptID);
	Args.Add(Location);
	Args.Add(Direction);
	Player->CellCall(TEXT("requestGotoSpacePlane"), Args);
}

void APlayerCharacter::EnableInputToControll(bool IsCanInput)
{
	UWorld* GameWorld = UUECS3GameInstance::Instance->GetWorld();
	APlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	ACS3PlayerController* GamePC = Cast<ACS3PlayerController>(PlayerController);
	GamePC->EnableInputToControll(IsCanInput);
}

void APlayerCharacter::ChangeModelColor()
{
	KBEngine::Entity* Player = GetSelfEntity();
	if (Player == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::HasRoleFlag : Player!"));
		return;
	}
	if (IsCarrierState())return;							// 在坐骑状态下，不变颜色
	int32 tempCamp = Player->GetDefinedProperty(TEXT("tempCamp")).GetValue<int32>();
	if (tempCamp == 0)return;

	const FVector Color = tempCamp == 2 ? CONST_COLOR_RED : CONST_COLOR_BLUE;
	UMeshComponent* MeshCom = GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_COATS);
	if (IsValid(MeshCom))
	{
		MeshCom->SetVectorParameterValueOnMaterials(TEXT("Param_BlocColor"), Color);
	}
}

void APlayerCharacter::OnStartOutsideCopyGame(float InDelayTime, FString InCarrierId, float InInputYawScale)
{
	ACS3PlayerController* GamePC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(GamePC))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::OnStartOutsideCopyGame : GamePC!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::OnStartOutsideCopyGame EntityID[%d] InDelayTime=%f InCarrierId=%s InInputYawScale=%f"), EntityId, InDelayTime, *InCarrierId, InInputYawScale);
	OutsideCopyCamScaleHeadle = GamePC->SetCameraRotateScale(InInputYawScale / GamePC->InputYawScale);
	
	RideCarrierComponent->RideOnCarrier(InCarrierId);

	if (!bIsDelayAutoMovement)
	{
		bIsDelayAutoMovement = true;
	}
	else
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(AutoMovementTimerHander);
		}
	}

	if (IsValid(UUECS3GameInstance::Instance))
	{
		TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, AutoMovementTimerHander, 
			FTimerDelegate::CreateLambda([DelayThisPtr]()
		{
			ACS3PlayerController* GamePC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
			if (UUECS3GameInstance::Instance&&UGolbalBPFunctionLibrary::GetCS3PlayerCharacter() && IsValid(GamePC) && DelayThisPtr.IsValid())
			{
				APlayerCharacter* ThisPtr = DelayThisPtr.Get();
				ThisPtr->bIsDelayAutoMovement = false;
				GamePC->GetAtkStateMar()->SwitchJingSuMode(true);
			}
		}), InDelayTime, false);
	}
}

void APlayerCharacter::OnOverOutsideCopyGame()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::OnOverOutsideCopyGame EntityID[%d]"), EntityId);	
	///<在延时时间内下Buff
	if (bIsDelayAutoMovement && AutoMovementTimerHander.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(AutoMovementTimerHander);
		}
	}
	UWorld* GameWorld = UUECS3GameInstance::Instance->GetWorld();
	ACS3PlayerController* GamePC = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(GamePC) && IsValid(GamePC->GetAtkStateMar()))
	{
		GamePC->RemoveCameraRotateScale(OutsideCopyCamScaleHeadle);
		GamePC->GetAtkStateMar()->SwitchJingSuMode(false);
	}
	OutsideCopyCamScaleHeadle = -1;
	if (GetSelfEntity() && GetSelfEntity()->IsPlayer())
	{
		GetCharacterMovement()->RotationRate = FRotator(0.0f, 5000.0f, 0.0f);
	}

	RideCarrierComponent->DisRideOnCarrier();
}

void APlayerCharacter::OnStartPlayerAutoMoveCopyGame(float InInputYawScale)
{
	ACS3PlayerController* GamePC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(GamePC))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::OnStartPlayerAutoMoveCopyGame : GamePC!"));
		return;
	}
	OutsideCopyCamScaleHeadle = GamePC->SetCameraRotateScale(InInputYawScale / GamePC->InputYawScale);


	if (UUECS3GameInstance::Instance&&UGolbalBPFunctionLibrary::GetCS3PlayerCharacter() && IsValid(GamePC) && IsValid(this))
	{
		GamePC->GetAtkStateMar()->SwitchLeiZhenMode(true);
	}
}

void APlayerCharacter::OnOverPlayerAutoMoveCopyGame()
{
	APlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	ACS3PlayerController* GamePC = Cast<ACS3PlayerController>(PlayerController);
	GamePC->RemoveCameraRotateScale(OutsideCopyCamScaleHeadle);
	OutsideCopyCamScaleHeadle = -1;
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchLeiZhenMode(false);
	if (GetSelfEntity() && GetSelfEntity()->IsPlayer())
	{
		GetCharacterMovement()->RotationRate = FRotator(0.0f, 5000.0f, 0.0f);
	}
}

void APlayerCharacter::OnPlayerCameraRotation(float RotationTime/* = 0.0f*/)
{
	ACS3PlayerController* GamePC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(GamePC) || !IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::OnPlayerCameraRotation : GamePC||PlayerActor!"));
		return;
	}

	float playerRoll;
	float pitch;
	float yaw;
	float playerPitch;
	float playerYaw;
	UKismetMathLibrary::BreakRotator(PlayerActor->GetControlRotation(), playerRoll, pitch, yaw);
	UKismetMathLibrary::BreakRotator(PlayerActor->GetActorRotation(), playerRoll, playerPitch, playerYaw);
	FRotator sControlRotator = PlayerActor->GetControlRotation();
	FRotator eControlRotator = UKismetMathLibrary::MakeRotator(playerRoll, pitch, playerYaw);
	if (RotationTime > 0)
	{
		static	float DurationTime = 0.0f;
		static	FTimerHandle CameraTimerHander;
		float DeltaTime = FApp::GetDeltaTime();
		if (DurationTime > 0.0f)
		{
			DurationTime = 0.0f;
		}

		if (CameraTimerHander.IsValid())
		{
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CameraTimerHander);
			}
		}

		TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, CameraTimerHander, 
				FTimerDelegate::CreateLambda([DelayThisPtr, DeltaTime, playerRoll, pitch, yaw, 
					playerYaw, sControlRotator, eControlRotator, RotationTime]()
			{
				ACS3PlayerController* GamePC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
				if (!DelayThisPtr.IsValid() || !IsValid(GamePC))
				{
					return;
				}
				APlayerCharacter* ThisPtr = DelayThisPtr.Get();

				DurationTime += DeltaTime;
				float DurationPct = (RotationTime - DurationTime) / RotationTime;

				float resultYaw = 0;
				if (FMath::Abs(playerYaw - yaw) <= 180)
				{
					resultYaw = FMath::Lerp(playerYaw, yaw, DurationPct);
				}
				else
				{
					float tempPlayerYaw = playerYaw;
					float tempYaw = yaw;
					if (yaw < -180.0f)
					{
						tempYaw = yaw + 360.0f;
					}
					else if (yaw > 180.0f)
					{
						tempYaw = yaw - 360.0f;
					}
					if (playerYaw < -180.0f)
					{
						tempPlayerYaw = playerYaw + 360.0f;

					}
					else if (playerYaw > 180)
					{
						tempPlayerYaw = playerYaw - 360.0f;
					}

					if (FMath::Abs(tempPlayerYaw - tempYaw) <= 180)
					{
						resultYaw = FMath::Lerp(tempPlayerYaw, tempYaw, DurationPct);
					}
					else
					{
						if (tempYaw < 0)
						{
							float count = FMath::Abs(tempYaw + 180.0f) + FMath::Abs(180 - tempPlayerYaw);
							float bDurationPct = (tempYaw + 180.0f) / count;
							float eDurationPct = (180 - tempPlayerYaw) / count;
							if (1 - DurationPct < bDurationPct)
							{
								resultYaw = FMath::Lerp(tempYaw, -180.0f, (1 - DurationPct) / (bDurationPct));
							}
							else
							{
								resultYaw = FMath::Lerp(180.0f, tempPlayerYaw, (1 - DurationPct - bDurationPct) / (eDurationPct));
							}
						}
						else
						{
							float count = FMath::Abs(tempYaw + 180.0f) + FMath::Abs(180 - tempPlayerYaw);
							float bDurationPct = (180.0f - tempYaw) / count;
							float eDurationPct = (180.0f + tempPlayerYaw) / count;
							if (1 - DurationPct < bDurationPct)
							{
								resultYaw = FMath::Lerp(tempYaw, 180.0f, (1 - DurationPct) / eDurationPct);
							}
							else
							{
								resultYaw = FMath::Lerp(-180.0f, tempPlayerYaw, (1 - DurationPct - bDurationPct) / bDurationPct);
							}
						}
					}
				}

				FRotator Rotator = UKismetMathLibrary::MakeRotator(playerRoll, pitch, resultYaw);
				if (DurationPct <= 0.0f)
				{
					DurationTime = 0.0f;
					GamePC->SetControlRotation(eControlRotator);
					if (IsValid(UUECS3GameInstance::Instance))
					{
						UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CameraTimerHander);
					}
				}
				else
				{
					if (GamePC)
					{
						GamePC->SetControlRotation(Rotator);
					}
				}
			}), DeltaTime, true);
		}
	}
	else
	{
		PlayerActor->GetController()->SetControlRotation(eControlRotator);
	}
}

void APlayerCharacter::CreateAppearance()
{
	if (KBEngine::Entity* Entity = this->GetSelfEntity())
	{
		bIsChangeAppearanceling = true; 

		FCREATE_APPEARANCE_DATA CreateAppData;
		CreateAppData.RoleModelId = (FString)Entity->GetDefinedProperty(TEXT("modelNumber"));
		CreateAppData.RoleProfession = (int32)Entity->GetDefinedProperty(TEXT("profession"));
		CreateAppData.RoleGender = (int32)Entity->GetDefinedProperty(TEXT("gender"));
		CreateAppData.RoleCamp = (int32)Entity->GetDefinedProperty(TEXT("camp"));
		FString ExtraModelNumber = (FString)Entity->GetDefinedProperty(TEXT("extraModelNumber"));
		FString RideCarrierId = (FString)Entity->GetDefinedProperty(TEXT("CarrierId"));
		FString CarrierId = RideCarrierId.IsEmpty() ? RideCarrierComponent->CarrierId : RideCarrierId;
		this->ProfessionID = CreateAppData.RoleProfession;
		if (!ExtraModelNumber.IsEmpty())
		{
			CreateAppData.RoleModelId = ExtraModelNumber;
		}

		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		if (!CarrierId.IsEmpty())
		{
			RideCarrierComponent->CreateRiderActorComponent();
			const FCARRIER_DATA *CarrierData = CfgManager->GetTableByType(
				CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CARRIER)->GetRow<FCARRIER_DATA>(FSTRING_TO_FNAME(CarrierId));
			CreateAppData.RidePetModelId = CarrierData->CarrierModelId;
			CreateAppData.RidePosture = CarrierData->RidePosture;
			GetAppearanceComponent()->CreateRideAppearance(CreateAppData);
		}
		else
		{
			GetAppearanceComponent()->CreateRideAppearance(CreateAppData);
		}
	}
}

void APlayerCharacter::UpdateActorPositionToGround()
{
	if (!IsMoveFlying() && !HasVehicle())
	{
		FVector Pos = GetGroundPosition();
		SetActorLocation(Pos);
	}
}

void APlayerCharacter::OnNavigateEndProcess(AServerCharacter* TargetCharacter)
{
	ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
	KBEngine::Entity* PlayerEntity = GetSelfEntity();
	if (PlayerEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::OnNavigateEndProcess : PlayerEntity!"));
		return;
	}
	if (IsValid(PlayerController))
	{
		if (NavigateNPCInfo.TeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportDefault || NavigateNPCInfo.TeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportCarter)
		{
			if (IsValid(TargetCharacter))
			{
				if (!NavigateNPCInfo.NPCScriptID.IsEmpty())
				{
					UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
					const FNPC_DATA* NpcData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC)->GetRow<FNPC_DATA>(NavigateNPCInfo.NPCScriptID);
					if (!NpcData)
					{
						StopPlayerMove();
					}
				}
				else
				{
					StopPlayerMove();
				}
				///<处理寻路后交互的问题 GossipWithType =0 以目标对象类型为依据可以交互的entity类型有spellBox、npc、MultiAreaSpellBox 该字段默认配置为0，配置0时该字段不发生任何作用，默认以类型配置触发条件触发，若配置1则强制触发，若配置为2则强制不触发
				if (!NavigateNPCInfo.GossipWithType)
				{
					KBEngine::Entity* TargetEntity = const_cast<AServerCharacter*>(TargetCharacter)->GetSelfEntity();
					if (TargetEntity)
					{
						UGameObjectInterface * Interface = TargetCharacter->GetEntityInterface_Cache().GameObjectInterface;
						if (IsValid(Interface) && ((Interface->getEntityFlag() == ENTITY_TYPE::ENTITY_FLAG_NPC) || (Interface->getEntityFlag() == ENTITY_TYPE::ENTITY_FLAG_DOOR) ||
							(Interface->getEntityFlag() == ENTITY_TYPE::ENTITY_FLAG_SPELL) || (Interface->getEntityFlag() == ENTITY_TYPE::ENTITY_FLAG_DROP_BOX)
							|| (Interface->getEntityFlag() == ENTITY_TYPE::ENTITY_FLAG_TELEPORTSTONE)) )
						{
							PlayerController->BP_FKeyGossipWith(TargetCharacter);
						}
					}
				}
				else if (NavigateNPCInfo.GossipWithType == 1)
				{
					PlayerController->BP_FKeyGossipWith(TargetCharacter);
				}
			}
			else
			{
				if (NavigateNPCInfo.NPCScriptID.IsEmpty())
				{
					StopPlayerMove();
				}
			}
		}
		else if (NavigateNPCInfo.TeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportPoint)
		{
			if (IsState(ENTITY_STATE::EntityStateFight))
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(4298);//当前为战斗状态，无法使用传送点进行寻路!
				return;
			}
			StopPlayerMove(); 
			URoleTeleportInterface * RoleTeleportInterface = Cast<URoleTeleportInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTeleportInterface")));
			if (NavigateNPCInfo.PointTeleportType == ENUM_POINT_TELEPORT_TYPE::TELEPORT_BY_TELEPORTSTONE)
			{
				//神行石规则传送
				if (IsValid(RoleTeleportInterface))
				{
					RoleTeleportInterface->TeleportPoint(NavigateNPCInfo.Param1, ENUM_STONE_TELEPORT_TYPE::StoneTeleportTypeNavigate);
				}
			}
			else
			{
				//无条件传送，即任务传送
				if (IsValid(RoleTeleportInterface))
				{
					RoleTeleportInterface->RPC_TeleportPoint(NavigateNPCInfo.Param1,(int32)NavigateNPCInfo.PointTeleportType);
				}
			}
		}
		else if (NavigateNPCInfo.TeleportType == ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportNPC)
		{
			StopPlayerMove();
			if (IsValid(TargetCharacter))
			{
				KBEngine::Entity* TargetEntity = TargetCharacter->GetSelfEntity();
				if (TargetEntity != nullptr)
				{
					UNPCInterface * NPCInterface = Cast<UNPCInterface>(TargetCharacter->GetEntityInterface_Cache().GameObjectInterface);
					if (NPCInterface)
					{
						NPCInterface->RPC_talkWith(NavigateNPCInfo.Param1, FString(""));
					}
					//KBEngine::FVariantArray Args;
					//Args.Add(NavigateNPCInfo.Param1);
					//Args.Add(FString(""));
					//TargetEntity->CellCall(TEXT("talkWith"), Args);
				}
			}
		}
		else
		{
			StopPlayerMove();
		}
		const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
		URolePerformanceInterface * RolePerformanceInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), 0));
		if (IsValid(RolePerformanceInterface) && RolePerformanceInterface->GetCrossMapTargetInfo().Num() <= 0 && FVector::Dist(NavigateNPCInfo.DstPosition, GetActorLocation()) <= NavigateNPCInfo.NearbyRange * 100.0f)
		{
			RolePerformanceInterface->OnNavigateArriveFinalSpace();
		}
	}
	ClearNavigateNPCInfo();
}

void APlayerCharacter::SetCharacterMovementWalkProperty(float InMaxStepHeight, float InWalkableFloorAngle)
{
	this->GetCharacterMovement()->MaxStepHeight = InMaxStepHeight;
	this->GetCharacterMovement()->SetWalkableFloorAngle(InWalkableFloorAngle);
}

void APlayerCharacter::SetCharacterMovementDefaultWalkProperty()
{
	SetCharacterMovementWalkProperty(DefaultMaxStepHeight, DefaultWalkableFloorAngle);
}

void APlayerCharacter::HoldPet(FName AttachMeshID)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::HoldPet EntityID[%d] AttachMeshID=%s"), EntityId, *(FNAME_TO_FSTRING(AttachMeshID)));
	BindMesh(AttachMeshID);
}

void APlayerCharacter::DownPet(FName AttachMeshID)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::DownPet EntityID[%d] AttachMeshID=%s"), EntityId, *(FNAME_TO_FSTRING(AttachMeshID)));
	UnBindMesh(AttachMeshID);
}

void APlayerCharacter::HoldJinDan(FName AttachMeshID, float buffRemainTime, float TimerInterval)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::HoldJinDan EntityID[%d] AttachMeshID=%s buffRemainTime=%f,TimerInterval=%f"), EntityId, *(FNAME_TO_FSTRING(AttachMeshID)), buffRemainTime, TimerInterval);
	BindMesh(AttachMeshID);
	OnHoldJinDanBP(buffRemainTime, TimerInterval);
}

void APlayerCharacter::DownJinDan(FName AttachMeshID)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::DownJinDan EntityID[%d] AttachMeshID=%s "), EntityId, *(FNAME_TO_FSTRING(AttachMeshID)));
	UnBindMesh(AttachMeshID);
	OnDownJinDanBP(); 
}

void APlayerCharacter::OnJumped_Implementation()
{
	///JumpComponent....
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::JumpJump EntityID[%d] Successful JumpCurrentCount=%d"), EntityId, JumpCurrentCount);
}

void APlayerCharacter::Falling()
{
	IsNotifyServerLandFalling = true;
}

void APlayerCharacter::Landed(const FHitResult& Hit)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::Landed EntityID[%d] "), EntityId);
	KBEngine::Entity* SelfEntity = GetSelfEntity();
	if (SelfEntity == nullptr)return;

	if (!ActorIsPlayer())
	{	
		// 一般非本地玩家不走这个流程
		return;
	}

	// 跳伞相关
	if (IsSkyParachuteState())
	{
		FlyPatrolComponent->LandYCJMDParachute();
		FlyPatrolComponent->LandYCJMDSkyDiving();
	}
	else
	{
		//检测死亡功能
		if (IsNotifyServerLandFalling)
		{
			FVector LastVelocity = GetCharacterMovement()->GetLastUpdateVelocity();
			LastVelocity.X = 0.0f;
			LastVelocity.Y = 0.0f;
			float LastVelocitySize = LastVelocity.Size();
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===LastVelocity[EntityId=%d,  LastVelocitySizee=%f,  LastVelocity(%f, %f, %f)]"),
				EntityId, LastVelocitySize, LastVelocity.X, LastVelocity.Y, LastVelocity.Z);
			
			URoleInterface * RoleInterface = Cast<URoleInterface>(UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.GameObjectInterface : nullptr);
			if (RoleInterface)
			{
				RoleInterface->LandEndFalling(LastVelocitySize*0.01);
			}
			IsNotifyServerLandFalling = false;
		}
	}

	//跳跃相关
	if (IsValid(JumpComponent) && !IsJumpParachuteState() && ActorIsPlayer())
	{
		JumpComponent->IsJumpState = false;
		JumpComponent->IsTheLand = true;

		if (IsActiveMoveing())//是否在移动中[区别:跑着着陆or原地着陆]
		{
			JumpComponent->ChangeJumpStateToServer(JUMP_SHOW_STATE::JUMP_SHOW_STATE_MLAND);
		}
		else
		{
			JumpComponent->ChangeJumpStateToServer(JUMP_SHOW_STATE::JUMP_SHOW_STATE_SLAND);
		}

		const FCHARACTER_MOVE_CACHE_DATA& CharacterMoveData = GetCharacterMoveCacheData();
		SetGravityScale(CharacterMoveData.GravityScale);///还原重力系数
	}

	//云梯相关(只有本地玩家才需要进入攀爬的逻辑)
	if (IsValid(LadderCustomMovmentCpt) && ActorIsPlayer())
	{
		LadderCustomMovmentCpt->LadderFallLand();
	}
}

//void APlayerCharacter::OnMovementModeChanged(EMovementMode PrevMovementMode, uint8 PreviousCustomMode /*= 0*/)
//{
//	Super::OnMovementModeChanged(PrevMovementMode, PreviousCustomMode);
//	JumpComponent->MovementModeChanged(PrevMovementMode, PreviousCustomMode);
//}

void APlayerCharacter::CheckJumpInput(float DeltaTime)
{
	//Super::CheckJumpInput(DeltaTime);
	UCharacterMovementComponent *CurCharacterMovement = GetCharacterMovement();
	if (CurCharacterMovement)
	{
		if (bPressedJump)
		{
			// If this is the first jump and we're already falling,
			// then increment the JumpCount to compensate.
			const bool bFirstJump = JumpCurrentCount == 0;
			if (bFirstJump && CurCharacterMovement->IsFalling())
			{
				//JumpCurrentCount++;
			}

			const bool bDidJump = CanJump() && CurCharacterMovement->DoJump(bClientUpdating);
			if (bDidJump)
			{
				// Transition from not (actively) jumping to jumping.
				if (!bWasJumping)
				{
					JumpCurrentCount++;
					OnJumped();
				}
				// Only increment the jump time if successfully jumped and it's
				// the first jump. This prevents including the initial DeltaTime
				// for the first frame of a jump.
				if (!bFirstJump)
				{
					JumpKeyHoldTime += DeltaTime;
				}
			}

			bWasJumping = bDidJump;
		}

		// If the jump key is no longer pressed and the character is no longer falling,
		// but it still "looks" like the character was jumping, reset the counters.
		else if (bWasJumping && !CurCharacterMovement->IsFalling())
		{
			ResetJumpState();
		}
	}
}

float APlayerCharacter::GetMoveSpeed()
{
	if (bIsClient)
	{
		return ClientMoveSpeed;
	}
	return UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, (TEXT("moveSpeed")));
}

float APlayerCharacter::GetMoveDirection()
{
	return ActorIsPlayer() ? CurMoveDirection : OtherMoveDirection;
}

void APlayerCharacter::SyncMoveType(CS3_MOVE_TYPE CurrMoveType)
{
	if (IsValid(this) && GetSelfEntity())
	{
		URoleInterface * RoleInterface = Cast<URoleInterface>(UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.GameObjectInterface : nullptr);
		if (RoleInterface)
		{
			RoleInterface->updateMoveType((int32)CurrMoveType);
		}
		//KBEngine::FVariantArray Args;
		//Args.Add((int32)CurrMoveType);
		//GetSelfEntity()->CellCall(TEXT("updateMoveType"), Args);
	}
}

void APlayerCharacter::UpdateAimOffsetYawAndPitch(float DeltaSeconds)
{
	FRotator TargetRotator = UKismetMathLibrary::NormalizedDeltaRotator(GetControlRotation(),
		GetRootComponent()->RelativeRotation);

	FRotator CurRotator = FRotator(0.0f, CurAimOffsetYaw, CurAimOffsetPitch);
	//FRotator RInterpRotator = UKismetMathLibrary::RInterpTo(CurRotator, TargetRotator, DeltaSeconds, 15.0f);
	CurAimOffsetYaw = UKismetMathLibrary::ClampAngle(TargetRotator.Yaw, -90.0f, 90.0f);
	CurAimOffsetPitch = UKismetMathLibrary::ClampAngle(TargetRotator.Pitch, -90.0f, 90.0f);

	URoleInterface * RoleInterface = Cast<URoleInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (IsValid(RoleInterface))
	{
		RoleInterface->RequestAimOffsetBlend(CurAimOffsetYaw, CurAimOffsetPitch);
	}

	/*if (GetSelfEntity() && IsControlled())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("APlayerCharacter::UpdateAimOffsetYawAndPitch   Entity=%d,  CurAimOffsetPitch=%f"),
			GetSelfEntity()->ID(), CurAimOffsetPitch); 
	}*/
}

bool APlayerCharacter::IsCanLedgesJump()
{
	//是否开启辅助跳跃功能
	bool IsOpenLedgesJump = UUECS3GameInstance::Instance->GameDefault->IsOpenLedgesJump;
	if (!IsOpenLedgesJump || !IsLevelOpenLedgesJump)
	{
		return false;
	}

	//是否在动
	bool bIsMoveing = IsMoveing();
	if (!bIsMoveing)
	{
		return false;
	}
	CS3_MOVE_TYPE MoveType = OtherPlayerMoveType;
	if (ActorIsPlayer())///自己控制的玩家
	{
		ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
		if (IsValid(PlayerController))
		{
			MoveType = PlayerController->GetMoveType();
		}
	}

	//是否移动类型满足
	///CS3_Display(CS3DebugType::CL_Undefined, TEXT("MoveType====%d"), (int32)MoveType);
	if (MoveType != CS3_MOVE_TYPE::MOVE_TYPE_CONTROL)
	{
		return false;
	}

	//是否不在跳跃中
	if (IsValid(JumpComponent) && JumpComponent->IsJumpState)
	{
		return false;
	}

	if (GetCharacterMovement()->IsFlying())
	{
		return false;
	}

	return true;
}

void APlayerCharacter::SkillAssisCallBack(FVector& AtkPos)
{
	if (OnSkillAssist.IsBound())
	{
		OnSkillAssist.Broadcast(AtkPos);
		OnSkillAssist.Clear();
	}
}

void APlayerCharacter::onPlayerUnderArea()
{
	if (IsState(ENTITY_STATE::EntityStateDead))
	{
		//一开始就是死亡在深度区
		if (IsNotifyServerUnderArea)
		{
			return;
		}
		if (UUECS3GameInstance::Instance->MapManager->IsPlayerUnderArea())
		{
			IsNotifyServerUnderArea = true;
		}
	}
	else 
	{
		if (!IsFlyPatrolState())
		{
			if (UUECS3GameInstance::Instance->MapManager->IsPlayerUnderArea())
			{
				if (!IsNotifyServerUnderArea)
				{
					if (GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity())
					{
						URoleInterface* RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
						if (RoleInterface)
						{
							RoleInterface->onPlayerUnderArea();
						}
					}
					IsNotifyServerUnderArea = true;
					IsNotifyServerLandFalling = false; //已经死亡则不用通知服务器掉落的高度
				}
			}
			else 
			{
				//出死亡深度区
				if (IsNotifyServerUnderArea)
				{
					IsNotifyServerUnderArea = false;
				}
			}
		}
	}
}

void APlayerCharacter::RefreshModel()
{
	CreateAppearance();
}

void APlayerCharacter::ResetModelPart(MODEL_PART_TYPE PartType)
{
	GameObject* SelfEntity = (GameObject*)GetSelfEntity();
	if (nullptr != SelfEntity && IsValid(GetAppearanceComponent()))
	{
		if (PartType == MODEL_PART_TYPE::MODEL_PART_BODYS_LIGHT)
		{
			PreviewBodyLightEffect("");
		}
		else
		{
			FString PartId = SelfEntity->GetPartIdByType(PartType);
			GetAppearanceComponent()->ChangePart(PartType, PartId);
		}
	}
}

void APlayerCharacter::PreviewBodyLightEffect(FString EffectId)
{
	PreviewBodyLightEffectID = EffectId;
	if (PreviewBodyLightEffectID.IsEmpty())///清除预览的环身ID，显示默认的环身ID
	{
		if (nullptr != GetSelfEntity())
		{
			FString BodyLightEffect = (FString)GetSelfEntity()->GetDefinedProperty(TEXT("bodyLightEffect"));
			ChangeBodyLightEffect(BodyLightEffect);
		}
	}
	else
	{
		ChangeBodyLightEffect(PreviewBodyLightEffectID);
	}
}

void APlayerCharacter::CheckBodyLightEffect()
{
	if (nullptr != GetSelfEntity())
	{
		FString BodyLightEffect = (FString)GetSelfEntity()->GetDefinedProperty(TEXT("bodyLightEffect"));
		if (!BodyLightEffect.IsEmpty() || !PreviewBodyLightEffectID.IsEmpty())
		{
			ChangeBodyLightEffect(BodyLightEffect);
		}
	}
}

void APlayerCharacter::UpdateWeaponState()
{
	KBEngine::Entity* SelfEntity = GetSelfEntity();
	if (SelfEntity && !IsChangeModelState() && !bIsYCJMDCopy)
	{
		int32 Profession = (int32)SelfEntity->GetDefinedProperty(TEXT("profession"));
		bool bIsFightShow = IsState(ENTITY_STATE::EntityStateFight) || IsState(ENTITY_STATE::EntityStateWarn);
		GetAppearanceComponent()->UpdateWeaponLocation(bIsFightShow, Profession);
	}
}

void APlayerCharacter::UpdateWeapontYXFXZ(YXFXZ_COPY_WEAPON_ENUM type)
{
	GetAppearanceComponent()->UpdateWeapontYXFXZ(type);
}

void APlayerCharacter::UpdateWeapontYCJMD(YCJMD_COPY_WEAPON_ENUM Type, const FString& SockeName, const FString& PartId)
{
	GetAppearanceComponent()->UpdateWeapontYCJMD(Type, SockeName, PartId);
}

void APlayerCharacter::GetBackAdornTransfrom(FPART_TRANSFORM& Transfrom)
{
	if (!GetSelfEntity())
	{
		return;
	}
	FString BackAdornParam = GetSelfEntity()->GetDefinedProperty(TEXT("backAdornParam"));
	TArray<FString> BackAdornParamArray = UGolbalBPFunctionLibrary::SplitString(BackAdornParam, false, "|");
	if (BackAdornParamArray.Num() == 2)
	{
		TArray<FString> LocationArray = UGolbalBPFunctionLibrary::SplitString(BackAdornParamArray[0], false, ",");
		TArray<FString> RotationArray = UGolbalBPFunctionLibrary::SplitString(BackAdornParamArray[1], false, ",");
		if (LocationArray.Num() == 3)
		{
			Transfrom.RelativeLocation = FVector(FSTRING_TO_FLOAT(LocationArray[0]), FSTRING_TO_FLOAT(LocationArray[1]), FSTRING_TO_FLOAT(LocationArray[2]));
		}
		if (RotationArray.Num() == 3)
		{
			Transfrom.RelativeRotation = FRotator(FSTRING_TO_FLOAT(RotationArray[0]), FSTRING_TO_FLOAT(RotationArray[1]), FSTRING_TO_FLOAT(RotationArray[2]));
		}
	}
}

void APlayerCharacter::OnClickRightMouseYCJMD()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===APlayerCharacter::OnClickRightMouseYCJMD,  right"));
	bIsYCJMDAimOffsetState = !bIsYCJMDAimOffsetState;
	OnEnterWarnState();
	OnClickRightMouseYCJMD_BP();

	///同步右键瞄准状态
	URoleInterface * RoleInterface = Cast<URoleInterface>(GetEntityInterface_Cache().GameObjectInterface);
	if (IsValid(RoleInterface))
	{
		RoleInterface->RequestYCJMDAimOffsetState(bIsYCJMDAimOffsetState);
	}
	KBEngine::Entity* entity = GetSelfEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_guessGameRoll : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	if (bIsYCJMDAimOffsetState)
	{
		args.Add(1);
	}
	else
	{
		args.Add(0);
	}
	entity->CellCall(TEXT("onYCJMDrClickEvent"), args);
}



void APlayerCharacter::ClientSetAoi(const FString & Radius)
{
	if (!Radius.IsEmpty())
	{
		KBEngine::Entity* Player = GetSelfEntity();
		if (Player == nullptr) 
		{
			CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::ClientSetAoi : Player!"));
			return;
		}
		if (GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity())
		{
			URoleInterface* RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
			if (RoleInterface)
			{
				RoleInterface->onClientSetAoi(Radius);
			}
		}
		
		//FString Method = FString(TEXT("onClientSetAoi"));
		//KBEngine::FVariantArray Args;
		//Args.Add(Radius);
		//Player->CellCall(Method, Args);
	}
}

void APlayerCharacter::ClientResetAoi()
{
	KBEngine::Entity* Player = GetSelfEntity();
	if (Player == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::ClientResetAoi : Player!"));
		return;
	}
	if (GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity())
	{
		URoleInterface* RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
		if (IsValid(RoleInterface))
		{
			RoleInterface->onClientResetAoi();
		}
	}
	
}

const FCAMERA_PARAMS_EVENT_DATA * APlayerCharacter::GetCameraParamsEventData(const FString & CameraParamsEventId)
{
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::GetCameraParamsEventData : Instance->CfgManager!"));
		return nullptr;
	}

	const FCAMERA_PARAMS_EVENT_DATA* CameraParamsEventData =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CAMERA_PARAMS_EVENT)->GetRow<FCAMERA_PARAMS_EVENT_DATA>(CameraParamsEventId);

	return CameraParamsEventData;
}

void APlayerCharacter::SwitchOffFlyOrbitMode()
{
	if (!IsValid(FlyPatrolComponent))
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::SwitchOffFlyOrbitMode : FlyPatrolComponent!"));
		return;
	}
	FlyPatrolComponent->SwitchFlyOrbitMode(false);
}

void APlayerCharacter::SetRoleInteractive(bool IsInteractive)
{
	bIsRoleInteractive = IsInteractive;
	if (IsInteractive)
	{
		StopRandomAction();
	}
}

void APlayerCharacter::StartCheckRandomAction()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::StartCheckRandomAction EntityID[%d] "), EntityId);
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, RandomActionTimerHander, 
			FTimerDelegate::CreateLambda([]()
		{
			UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
			if (IsValid(ControllerModeMgr))
			{
				TArray<FString> OtherValue;
				ControllerModeMgr->ExecuteInputInfor(TEXT("CheckPlayRandomAction"), TEXT(""), 0.0f, OtherValue);
			}
		}), 3.0f, true);
	}
}

void APlayerCharacter::PlayRandomAction(int32 RandomNumber)
{
	int32 ValidRandomCount = RandomActionDatas.Num();
	if (ValidRandomCount > 0)
	{
		int32 index = RandomNumber%ValidRandomCount;
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::ExcetPlayRandomAction[index=%d,  ValidRandomCount=%d]"), index, ValidRandomCount);
		if (RandomActionDatas.IsValidIndex(index))
		{
			FACTION_DATA ActionData = RandomActionDatas[index];
			if (GetBaseAnimInstance())
			{
				GetBaseAnimInstance()->PlayRandomAction(ActionData.Id);
			}
		}
	}
}

void APlayerCharacter::StopRandomAction()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::StopRandomAction EntityID[%d] "), EntityId);
	if (GetBaseAnimInstance())
	{
		GetBaseAnimInstance()->StopActionByType(ACTION_TYPE_ENUM::ACTION_TYPE_RANDOM);
	}
}

void APlayerCharacter::CreateFlyBindActor(FString FlyBindActorID/* = TEXT("1")*/)
{
	if (!IsValid(FlyBindCharacter))
	{
		UClass *FlyBindClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_FlyBindActor"));
		AActor* FlyBindActor = UGolbalBPFunctionLibrary::SpawnActor<AActor>(FlyBindClass);
		FlyBindCharacter = Cast<AFlyBindCharacter>(FlyBindActor);
		auto FlyBindMeshTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_FLY_BIND_MESH_DATA);
		const FFLY_BIND_MESH_DATA* FlyBindMeshData = FlyBindMeshTable->GetRow<FFLY_BIND_MESH_DATA>(FlyBindActorID);
		FlyBindCharacter->GetAppearanceComponent()->CreateAppearance(FlyBindMeshData->FlyModeID);
		FlyBindCharacter->SetActorLocation(FVector::ZeroVector);
		FlyBindCharacter->AttachToComponent(this->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, FlyBindMeshData->FlyModeBindSocket);
		FlyBindCharacter->initFlyBindActor(FlyBindMeshData, EntityId);
	}
}

void APlayerCharacter::DestroyFlyBindActor()
{
	if (IsValid(FlyBindCharacter))
	{
		FDetachmentTransformRules rule(EDetachmentRule::KeepRelative, false);
		FlyBindCharacter->DetachFromActor(rule);
		FlyBindCharacter->Destroy();
		FlyBindCharacter = nullptr;
	}
}

void APlayerCharacter::SetOrientRotationToMovement(bool bValue, bool bIsModeChange, int32 Count, bool bIsReduction)
{
	//获取真实的旋转受影响的值
	bool RealOrientRotation = GetCharacterMovement()->bOrientRotationToMovement;

	//需要还原则还原成当前操作模式的值
	if (bIsReduction)
	{
		if (OrientRotationNum > 0)
		{
			OrientRotationNum -= Count;
		}
		if (OrientRotationNum <= 0)
		{
			GetCharacterMovement()->bOrientRotationToMovement = bModeOrientRotation;
			OrientRotationNum = 0;
		}
		return;
	}

	//如果是操作模式的切换
	if (bIsModeChange)
	{
		bModeOrientRotation = bValue;
		if (OrientRotationNum <= 0)
		{
			GetCharacterMovement()->bOrientRotationToMovement = bModeOrientRotation;
		}
	}
	else
	{		
		OrientRotationNum++;
		GetCharacterMovement()->bOrientRotationToMovement = bValue;
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("~~~~~~~~~  APlayerCharacter::SetOrientRotationToMovement OrientRotationNum=[%i]"), OrientRotationNum);
	}
}

bool APlayerCharacter::GetOrientRotationToMovement()
{
	URoleStateInterface* RoleStateInst = Cast<URoleStateInterface>(GetEntityInterface_Cache().StateInterface);

	if (RoleStateInst && RoleStateInst->IsActionForbid(ACTION_FLAG::ACTION_FORBID_TRANSLATE_DIRECTION))
	{
		return true;
	}

	ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
	if (IsValid(PlayerController) && PlayerController->GetMoveType() == CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE)
	{
		return true;
	}

	//USkillInterface* SkillInter = Cast<USkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("SkillInterface")));
	UAtkStateMar* AtkState = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if (IsValid(AtkState))
	{
		if (AtkState->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT) ||
			AtkState->IsActivateState(EATTACT_STATE::HALF_HOMING_SPELL_ATT))
		{
			if (OrientRotationNum > 0)
			{
				return true;
			}
		}

		if (AtkState->IsActivateState(EATTACT_STATE::BEHAVIOR_GLIDING))
		{
			return false;
		}
	}

	return GetCharacterMovement()->bOrientRotationToMovement;
}

void APlayerCharacter::UpdateFaBao(FString InModelId)
{
	if (!InModelId.IsEmpty())
	{
		CreateFaBao(InModelId);
	}
	else
	{
		DestroyFaBao();
	}
}

void APlayerCharacter::HideFaBao(bool IsHideFaBao)
{
	if (IsValid(FabaoCharacter))
	{
		FabaoCharacter->SetActorHiddenInGame(IsHideFaBao);
	}
}

void APlayerCharacter::SetMeshPartHiddenInGame(MODEL_PART_TYPE MeshPartType, bool IsHiddenInGame)
{
	if (MeshPartType == MODEL_PART_TYPE::MODEL_PART_FABAO)
	{ 
		HideFaBao(IsHiddenInGame);  
	}
	else
	{
		Super::SetMeshPartHiddenInGame(MeshPartType, IsHiddenInGame);
	}
}

void APlayerCharacter::StopPlayerMove()
{
	ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
	if (IsValid(PlayerController))
	{
		PlayerController->StopMove();
	}
}

void APlayerCharacter::CreateFaBao(const FString& InFaBaoModeId) 
{
	if (!IsValid(FabaoCharacter))
	{
		UClass *FaBao = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Magic"));
		AActor* FaBaoActor = UGolbalBPFunctionLibrary::SpawnActor<AActor>(FaBao);
		AMagicCharacter* FabaoActor = Cast<AMagicCharacter>(FaBaoActor);
		//法宝初始化数据
		FabaoActor->Init(this,InFaBaoModeId);
		FabaoCharacter = FabaoActor;
	}
}

void APlayerCharacter::DestroyFaBao()
{
	if (IsValid(FabaoCharacter))
	{
		FabaoCharacter->Destroy();
		FabaoCharacter = nullptr;
	}
}

void APlayerCharacter::SelectOtherPlayer()
{
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (IsValid(ControllerModeMgr))
	{
		TArray<FString> OtherValue;
		OtherValue.Add(INT_TO_FSTRING(bIsShowInvisible));
		OtherValue.Add(INT_TO_FSTRING(EntityId));
		OtherValue.Add(INT_TO_FSTRING(EntityId));
		OtherValue.Add(INT_TO_FSTRING(int32(CHARACTER_TYPE::PLAYER_CHARACTER)));
	
		ControllerModeMgr->ExecuteInputInfor(TEXT("ShowSelectTarget"), TEXT(""), 0.0f, OtherValue);		
	}
}

void APlayerCharacter::SetPlayerTarget(AServerCharacter *InTargetActor)
{
	if (!UUECS3GameInstance::pKBEApp) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::SetTargetEntity : pKBEApp!"));
		return;
	}

	KBEngine::Entity* PlayerEntity = UUECS3GameInstance::pKBEApp->Player();
	if (!PlayerEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::SetTargetEntity : PlayerEntity!"));
		return;
	}

	CS3Role *MyRolePlayer = (CS3Role *)PlayerEntity;
	if (!MyRolePlayer)
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::SetTargetEntity : MyRolePlayer!"));
		return;
	}
	this->OldPlayerTarget = this->CurPlayerTarget;

	AServerCharacter* TargetCharacter = ((AServerCharacter*)InTargetActor);
	if (TargetCharacter)
	{
		//考虑到其他系统需要用entity来确定目标
		KBEngine::Entity* TargetEntity = TargetCharacter->GetSelfEntity();
		if (TargetEntity)
		{
			MyRolePlayer->SetTargetEntityID(TargetEntity->ID());
		}
	}
	else
	{
		MyRolePlayer->SetTargetEntityID(PlayerEntity->ID());
	}
	//玩家自身目标
	this->CurPlayerTarget = InTargetActor;
	//通知其他地方
	OnChangeTarget();
}

void APlayerCharacter::SetWalkOffLedges(bool bCanWalkOffLedges)
{
	if (GetSelfEntity() == nullptr)
	{
		CS3_Warning(TEXT("APlayerCharacter::SetWalkOffLedges no this entity%d"), EntityId);
		return;
	}
	if (GetSelfEntity()->IsPlayer())
	{
		UCharacterMovementComponent* MovementComponent = GetCharacterMovement();
		MovementComponent->bSweepWhileNavWalking = bCanWalkOffLedges;
		MovementComponent->bCanWalkOffLedges = bCanWalkOffLedges;
	}
}

bool APlayerCharacter::GetCanWalkOffLedges()
{
	UCharacterMovementComponent* MovementComponent = GetCharacterMovement();
	if (IsValid(MovementComponent))
	{
		return MovementComponent->CanWalkOffLedges();
	}
	return false;
}

void APlayerCharacter::SetViewTarget(int32 TargetID, FVector DurationTime /*= FVector::ZeroVector*/, float Range /*= 0.0f*/, FVector StartViewRotator /*= FVector::ZeroVector*/, FVector TragetViewRotator /*= FVector::ZeroVector*/, bool bIsResetPlayerCamera /*= true*/)
{
	if (GetSelfEntity() == nullptr)
	{
		CS3_Warning(TEXT("APlayerCharacter::SetViewTarget no this entity%d"), EntityId);
		return;
	}
	AActor* TargetActor = UGolbalBPFunctionLibrary::GetActorByID(TargetID);
	if (IsValid(TargetActor) && GetSelfEntity()->IsPlayer())
	{
		ACS3PlayerController* CS3PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (IsValid(CS3PlayerController))
		{
			AStaticMeshActor* TempActor;
			FRotator LookAtRotation = UKismetMathLibrary::FindLookAtRotation(GetActorLocation() + StartViewRotator, TargetActor->GetActorLocation() + TragetViewRotator);
			CS3PlayerController->SetControlRotation(LookAtRotation);

			FVector  ActorLocation = TargetActor->GetActorLocation() + TragetViewRotator - LookAtRotation.Vector()*Range * 100;
			TempActor = UGolbalBPFunctionLibrary::SpawnActor<AStaticMeshActor>(AStaticMeshActor::StaticClass(), ActorLocation, LookAtRotation);
			CS3PlayerController->SetViewTargetWithBlend(TempActor, DurationTime.X);

			if ((DurationTime.X + DurationTime.Y) > 0.0f)
			{
				FTimerHandle DelayDestroyCameraHandle;
				TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
				TWeakObjectPtr<AStaticMeshActor> DelayTempActorPtr(TempActor);
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayDestroyCameraHandle,
					FTimerDelegate::CreateLambda([DelayTempActorPtr, DurationTime, bIsResetPlayerCamera, DelayThisPtr]() {
					ACS3PlayerController* CS3PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
					if (IsValid(CS3PlayerController) && DelayThisPtr.IsValid())
					{
						APlayerCharacter* ThisPtr = DelayThisPtr.Get();
						if (bIsResetPlayerCamera)
						{
							UGolbalBPFunctionLibrary::SetCameraTargetArmLength(ThisPtr->SpringArmCompent, 1500.0f);
							FRotator Rotation = ThisPtr->GetActorRotation();
							CS3PlayerController->SetControlRotation(Rotation - FRotator(17.0f, 0.0f, 0.0f));
						}

						CS3PlayerController->SetViewTargetWithBlend(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter(), DurationTime.Z > 0 ? DurationTime.Z : 0.0f);
					}
					if (DelayTempActorPtr.IsValid())
					{
						DelayTempActorPtr.Get()->Destroy();
					}
				}), DurationTime.X + DurationTime.Y, false);
			}
			else
			{
				if (bIsResetPlayerCamera)
				{
					UGolbalBPFunctionLibrary::SetCameraTargetArmLength(SpringArmCompent, 1500.0f);
					FRotator Rotation = GetActorRotation();
					CS3PlayerController->SetControlRotation(Rotation - FRotator(17.0f, 0.0f, 0.0f));
				}
				CS3PlayerController->SetViewTargetWithBlend(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter(), DurationTime.Z > 0 ? DurationTime.Z : 0.0f);
			}
		}
	}
}

void APlayerCharacter::ChangeRidePet(FString PreviewCarrierId)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor) && IsValid(PlayerActor->RideCarrierComponent) && GetSelfEntity() != nullptr)
	{
		if (PreviewCarrierId.IsEmpty())
		{
			FString RideCarrierId = (FString)GetSelfEntity()->GetDefinedProperty(TEXT("carrierId"));
			if (RideCarrierId.IsEmpty())
			{
				PlayerActor->RideCarrierComponent->DisRideOnPet();
			}
			else
			{
				PlayerActor->RideCarrierComponent->RideOnPet(RideCarrierId);
			}
		}
		else
		{
			PlayerActor->RideCarrierComponent->RideOnPet(PreviewCarrierId);
		}
	}
}

FString APlayerCharacter::GetRidePetCarrierID()
{
	return (FString)GetSelfEntity()->GetDefinedProperty(TEXT("carrierId"));
}

bool APlayerCharacter::IsRidePetState()
{
	return IsValid(RideCarrierComponent) && RideCarrierComponent->IsRidePetState();
}

bool APlayerCharacter::IsCarrierState()
{
	return IsValid(RideCarrierComponent) && RideCarrierComponent->IsCarrierState();
}

bool APlayerCharacter::IsDisCarrierState()
{
	return IsValid(RideCarrierComponent) && RideCarrierComponent->IsDisCarrierState();
}

ARiderCharacter* APlayerCharacter::GetRiderCharacter()
{
	if (IsValid(RideCarrierComponent))
	{
		return RideCarrierComponent->GetRiderCharacter();
	}
	return nullptr;
}

void APlayerCharacter::CameraApproach(float Dist, float ApproachT, float RemainT, float ApproachBackT)
{
	if (IsValid(CameraControl))
	{
		CameraControl->CameraApproach(Dist, ApproachT, RemainT, ApproachBackT);
	}
}

void APlayerCharacter::RadialBlur(float Intensity, float FadeInT, float RemainT, float FadeOutT)
{
	if (IsValid(CameraControl))
	{
		CameraControl->RadialBlur(Intensity, FadeInT, RemainT, FadeOutT);
	}
}

void APlayerCharacter::CameraShake(float Intensity, float Rate, float Time, int32 Priority)
{
	if (IsValid(CameraControl))
	{
		CameraControl->CameraShake(Intensity, Rate, Time, Priority);
	}
}

void APlayerCharacter::RadialOffsetX(float Offset, float FadeInT, float RemainT, float FadeOutT)
{
	if (IsValid(CameraControl))
	{
		CameraControl->RadialOffsetX(Offset, FadeInT, RemainT, FadeOutT);
	}
}

void APlayerCharacter::RadialOffsetY(float Offset, float FadeInT, float RemainT, float FadeOutT)
{
	if (IsValid(CameraControl))
	{
		CameraControl->RadialOffsetY(Offset, FadeInT, RemainT, FadeOutT);
	}
}

void APlayerCharacter::CameraUp(float Height, float FadeInT, float RemainT, float FadeOutT)
{
	if (IsValid(CameraControl))
	{
		CameraControl->CameraUp(Height, FadeInT, RemainT, FadeOutT);
	}
}

void APlayerCharacter::StopCameraApproach()
{
	if (IsValid(CameraControl))
	{
		CameraControl->StopCameraApproach();
	}
}

void APlayerCharacter::StopRadialBlur()
{
	if (IsValid(CameraControl))
	{
		CameraControl->StopRadialBlur();
	}
}

void APlayerCharacter::StopCameraShake()
{
	if (IsValid(CameraControl))
	{
		CameraControl->StopCameraShake();
	}
}

void APlayerCharacter::StopRadialOffsetX()
{
	if (IsValid(CameraControl))
	{
		CameraControl->StopRadialOffsetX();
	}
}

void APlayerCharacter::StopRadialOffsetY()
{
	if (IsValid(CameraControl))
	{
		CameraControl->StopRadialOffsetY();
	}
}

void APlayerCharacter::StopCameraUp()
{
	if (IsValid(CameraControl))
	{
		CameraControl->StopCameraUp();
	}
}

void APlayerCharacter::OnBindWeatherToCamera(UCameraComponent* CameraComp)
{
	if (IsValid(CameraComp)&& ActorIsPlayer())
	{
		if (IsValid(WeatherParticle))
		{
			FAttachmentTransformRules AttachmentTransformRules(EAttachmentRule::SnapToTarget, EAttachmentRule::KeepWorld, EAttachmentRule::KeepWorld, false);
			WeatherParticle->AttachToComponent(CameraComp, AttachmentTransformRules);
		}
		if (IsValid(UGolbalBPFunctionLibrary::AudioManager()))
		{
			UGolbalBPFunctionLibrary::AudioManager()->UpdateWeatherComp(CameraComp);
		}		
	}
}

void APlayerCharacter::OnSetWeatherParticle(class UParticleSystem* NewTemplate)
{
	if (IsValid(WeatherParticle) && IsValid(NewTemplate))
	{
		WeatherParticle->SetTemplate(NewTemplate);
	}
}

void APlayerCharacter::OnChangeTarget()
{
	//发送给本身蓝图
	BP_OnChangeTarget();
	//通知继承接口的对象

	//以一种广播的形式通知给外部无关的对象
	if (OnChangeTargetDelegate.IsBound())
	{
		OnChangeTargetDelegate.Broadcast();
		//OnChangeTargetDelegate.Clear();
	}
}

void APlayerCharacter::NotifyCreateRoleAppearance()
{
	CreateAppearance();
}

void APlayerCharacter::OnNotifyActionChange(FACTION_DATA ActionData)
{
	if (IsValid(RideCarrierComponent))
	{
		RideCarrierComponent->PlayBindAction(ActionData);
	}
}

void APlayerCharacter::OnNotifyActionChangeFinish(FACTION_DATA ActionData)
{
	CheckPartHideByAction(ActionData);
	UpdateWeaponState();
	CheckBodyLightEffect();
}

void APlayerCharacter::OnPlayShouBaoDaoActionOver(ACharacter *GameCharacter, FACTION_DATA InActionData)
{
	UpdateWeaponState();
}

void APlayerCharacter::OnEnterStallState()
{
	if (GetSelfEntity())
	{
		URoleStallInterface* RoleStallInterface = Cast<URoleStallInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStallInterface"), GetSelfEntity()->ID()));
		if (RoleStallInterface)
		{
			RoleStallInterface->OnEnterStall();
		}
	}
}

void APlayerCharacter::OnWorldPostActorTick()
{	
	if (IsDodgeState && DodgeRotator != FRotator::ZeroRotator)
	{
		IsDodgeState = false;
		SetActorRotation(DodgeRotator);
	}
}

void APlayerCharacter::ClearWorldPostActorTickHandle()
{
	if (FWorldDelegates::OnWorldPostActorTick.IsBoundToObject(this) && WorldPostActorTickHandle.IsValid())
	{
		FWorldDelegates::OnWorldPostActorTick.Remove(WorldPostActorTickHandle);
	}
}

void APlayerCharacter::OnEnterEffectStoryState()
{
	if (!ActorIsPlayer())
	{
		UGStoryManager* GStoryManager = UGolbalBPFunctionLibrary::GStoryManager();
		if (IsValid(GStoryManager))
		{
			///<本地玩家正在播放镜头,其他玩家不显示镜头图标
			if (!GStoryManager->IsPlaying())
			{
				BP_OnUpdatePlayerStoryIcon(true);
			}
		}
	}
}

void APlayerCharacter::OnExitEffectStoryState()
{
	if (!ActorIsPlayer())
	{
		///<其他玩家隐藏镜头图标
		BP_OnUpdatePlayerStoryIcon(false);
	}
}

void APlayerCharacter::InitWeatherComponent()
{
	WeatherParticle = NewObject<UParticleSystemComponent>(this, TEXT("WeatherParticle"));
	WeatherParticle->RegisterComponent();
	FAttachmentTransformRules AttachmentTransformRules(EAttachmentRule::SnapToTarget, EAttachmentRule::KeepWorld, EAttachmentRule::KeepWorld, false);
	if (IsValid(CameraComponent))
	{
		WeatherParticle->AttachToComponent(CameraComponent, AttachmentTransformRules);
	}
}

void APlayerCharacter::UnBindWeatherSoundComp()
{
	if (IsValid(CameraComponent))
	{
		if (IsValid(UGolbalBPFunctionLibrary::AudioManager()) || CameraComponent->GetAttachChildren().Contains(UGolbalBPFunctionLibrary::AudioManager()->WeatherSoundComp))
		{
			UGolbalBPFunctionLibrary::AudioManager()->UnBindWeatherSoundComp();
		}
	}
}

void APlayerCharacter::InitLightComponent()
{
	CS3LightComponent = NewObject<UCS3LightComponent>(this, TEXT("CS3LightComponent"));
	CS3LightComponent->RegisterComponent();
	CS3LightComponent->CreateLight();
	CS3LightComponent->SceneLight->AttachToComponent(SpringArmCompent, FAttachmentTransformRules::KeepRelativeTransform);
	CS3LightComponent->InitLightData();
	CS3LightComponent->SetComponentTickEnabled(false);
}

void APlayerCharacter::ActivateNavigateMoveModeOperation(bool IsActivate, FVector DstPosition, float NearbyRange, FString DstSpaceName, int AutoQuestID, bool IsSearch, bool IsArrived, int32 GossipWithType/* = 0*/)
{
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if ( IsValid(ControllerModeMgr))
	{
		TArray<FString> OtherValue;
		FString DstPositionString = FLOAT_TO_FSTRING(DstPosition.X) + TEXT(" ") + FLOAT_TO_FSTRING(DstPosition.Y) + TEXT(" ") + FLOAT_TO_FSTRING(DstPosition.Z);
		OtherValue.Add(DstPositionString);
		OtherValue.Add(FLOAT_TO_FSTRING(NearbyRange));
		OtherValue.Add(DstSpaceName);
		OtherValue.Add(INT_TO_FSTRING(AutoQuestID));
		OtherValue.Add(INT_TO_FSTRING((int)IsSearch));
		OtherValue.Add(INT_TO_FSTRING((int)IsArrived));
		OtherValue.Add(INT_TO_FSTRING(GossipWithType));
		if (IsActivate)
		{
			ControllerModeMgr->ExecuteInputInfor(TEXT("ActivateNavigateMoveMode"), TEXT(""), 0.0f, OtherValue);
		}
		else
		{
			ControllerModeMgr->ExecuteInputInfor(TEXT("UnActivateNavigateMoveMode"), TEXT(""), 0.0f, OtherValue);
		}		
	}
}

int32 APlayerCharacter::AddWindForce(float _WindSpeed, FVector _WindDirection)
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	if (IsValid(ForceMana))
	{
		int32 WindID = ForceMana->AddForce(this, _WindSpeed, _WindDirection);
		WindIDArr.Add(WindID);

		return WindID;
	}

	CS3_Warning(TEXT("APlayerCharacter::AddWindForce-- UForceManager Is Null!"));
	return -1;
}

bool APlayerCharacter::BeginWindForce(int32 WindID, float _WindSpeed /*= -1.0f*/, FVector _WindDirection /*= FVector::ZeroVector*/)
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	if (IsValid(ForceMana))
	{
		return ForceMana->BeginForce(WindID, _WindSpeed, _WindDirection);
	}

	return false;
}

void APlayerCharacter::BeginAllWindForce()
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	if (IsValid(ForceMana))
	{
		for (int32 WindID : WindIDArr)
		{
			ForceMana->BeginForce(WindID);
		}
	}
}

bool APlayerCharacter::PauseWindForce(int32 WindID)
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	if (IsValid(ForceMana))
	{
		return ForceMana->PauseForce(WindID);
	}

	return false;
}

void APlayerCharacter::PauseAllWindForce()
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	if (IsValid(ForceMana))
	{
		for (int32 WindID : WindIDArr)
		{
			ForceMana->PauseForce(WindID);
		}
	}
}

void APlayerCharacter::StopAllWindForces()
{
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();

	if (IsValid(ForceMana))
	{
		ForceMana->StopAllForces(this, WindIDArr);
	}
}

bool APlayerCharacter::IsLadderMovement()
{
	if (IsValid(LadderCustomMovmentCpt))
	{
		return LadderCustomMovmentCpt->IsLadderMovement();
	}
	return false;
}

int32 APlayerCharacter::GetFinalCamp()
{
	KBEngine::Entity* Entity = GetSelfEntity();
	if (Entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::GetFinalCamp : Entity!"));
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

void APlayerCharacter::EndAutoAttackFriendEntity()
{
	if (AutoAttackFriendEntityHandle.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(AutoAttackFriendEntityHandle);
		}
	}
}

bool APlayerCharacter::SwitchControlToSelf()
{
	//获得玩家控制器
	ACS3PlayerController* playerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	//判断自己是否已经被控制
	if (IsValid(playerController) && playerController->GetPawn() == this)
	{
		return false;
	}

	//获取玩家
	APlayerCharacter* player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(player))
	{
		GameObject* role = (GameObject*)(player->GetSelfEntity());

		if (nullptr != role)
		{

			//KBEngine::FVariantArray Args;

			FVector pos = GetActorLocation();

			//Args.Add(KBEMath::Unreal2KBEnginePosition(pos));
			//role->CellCall(TEXT("setPositionFromClient"), Args);
			if (GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity())
			{
				URoleInterface* RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
				if (RoleInterface)
				{
					RoleInterface->setPositionFromClient(KBEMath::Unreal2KBEnginePosition(pos));
				}
			}
			

			role->BindActorToEntity(this, true);
			playerController->Possess(this);
		
			player->EntityId = -1;

			SetInitialized(true);

			return true;
		}
		else
		{
			return false;
		}
	}
	else
	{
		return false;
	}

}

bool APlayerCharacter::IsActiveMoveing()
{
	bool bIsMoveing = IsMoveing();
	if (!bIsMoveing)
	{
		return false;
	}

	CS3_MOVE_TYPE MoveType = OtherPlayerMoveType;
	if (ActorIsPlayer())///自己控制的玩家
	{
		ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(GetController());
		if (IsValid(PlayerController))
		{
			MoveType = PlayerController->GetMoveType();
		}
	}
	 
	///CS3_Display(CS3DebugType::CL_Undefined, TEXT("MoveTypeMoveType====%d"), (int32)MoveType); 
	if (MoveType != CS3_MOVE_TYPE::MOVE_TYPE_FLY &&
		MoveType != CS3_MOVE_TYPE::MOVE_TYPE_BACK && 
		MoveType != CS3_MOVE_TYPE::MOVE_TYPE_NONE)
	{
		return true;
	}
	return false;
}

void APlayerCharacter::ClearCameraParamsEvent_Implementation()
{
	const FCAMERA_PARAMS_EVENT_DATA* CameraParamsEventData = GetCameraParamsEventData(INT_TO_FSTRING(CameraParamsEventID));

	if (CameraParamsEventData)
	{
		UGStoryManager* GStoryManager = UGolbalBPFunctionLibrary::GStoryManager();
		if (IsValid(GStoryManager))
		{
			if (!GStoryManager->IsPlaying())
			{
				ClientResetAoi();
			}
		}
		else
		{
			ClientResetAoi();
		}
	}
	CameraParamsEventID = 0;
}

void APlayerCharacter::SetCameraParamsEvent_Implementation(const FString & EventID)
{
	const FCAMERA_PARAMS_EVENT_DATA* CameraParamsEventData = GetCameraParamsEventData(EventID);
	if (CameraParamsEventData)
	{
		CameraParamsEventID = FSTRING_TO_INT(EventID);
		ClientSetAoi(CameraParamsEventData->Aoi);
	}
}
void APlayerCharacter::OnEnterMovingPlatform(int32 MovingPlatformID)
{
	KBEngine::Entity* Entity_Player = UUECS3GameInstance::pKBEApp->Player();

	if (nullptr == Entity_Player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::OnEnterMovingPlatform: Entity_Player!"));
		return;
	}

	CS3Entity* pEntity_Player = (CS3Entity*)(Entity_Player);

	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::OnEnterMovingPlatform : pEntity_Player->IsPlayerRole()!"));
		return;
	}

	//if (Entity_Player->ParentID() == MovingPlatformID) 
	//{
	//	CS3_Warning(TEXT("APlayerCharacter::OnEnterMovingPlatform Entity_Player->ParentID()"));
	//	return;
	//}

	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->onLandMovingPlatform(MovingPlatformID);
	}
}
void APlayerCharacter::OnLeaveMovingPlatform(int32 MovingPlatformID)
{
	KBEngine::FVariantArray Args;
	//this->SetRemoteRoleForBackwardsCompat(ROLE_Authority);
	//GetCharacterMovement()->SetMovementMode(MOVE_Walking);
	KBEngine::Entity* Entity_Player = UUECS3GameInstance::pKBEApp->Player();
	
	if (Entity_Player == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::OnLeaveMovingPlatform : Entity_Player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(Entity_Player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::OnLeaveMovingPlatform : pEntity_Player->IsPlayerRole()!"));
		return;
	}

	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->onDeviateMovingPlatform();
	}
}

void APlayerCharacter::BaseChange()
{
	Super::BaseChange();
	
	if (!this->ActorIsPlayer() || this->GetSelfEntity() == nullptr)
		return;

	CurrentBaseActor = GetMovementBaseActor(this);
	if (CurrentBaseActor == NULL)
	{
		UStateInterface* RSInterface = GetEntityInterface_Cache().StateInterface;
		if (this->GetSelfEntity()->ParentID() > 0 && RSInterface->HasEffectState(EFFECT_STATE::EFFECT_STATE_HIT_BACK))
		{
			LeaveMovePlatform_HitBack = true;
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------------APlayerCharacter::BaseChange,LeaveMovePlatform_HitBack----------------------"));
		}
		else if (this->GetSelfEntity()->ParentID() > 0)
		{
			KBEngine::Entity* Entity= UGolbalBPFunctionLibrary::FindEntity(this->GetSelfEntity()->ParentID());
			if (Entity)
			{
				AActor* Actor = Entity->Actor();
				if (IsValid(Actor))
				{
					AMovingPlatformCharacter* MovingPlatform = Cast<AMovingPlatformCharacter>(Actor);
					if (MovingPlatform)
					{
						MovingPlatform->OnPlayerLeaveMovingPlatform();
					}
				}
			}
			LeaveMovePlatform_HitBack = false;
			OnLeaveMovingPlatform(0);
		}
		else
		{
			LeaveMovePlatform_HitBack = false;
			OnLeaveMovingPlatform(0);
		}
	}
	else if (IsValid(CurrentBaseActor))
	{
		AServerCharacter* Actor_S = Cast<AServerCharacter>(CurrentBaseActor);
		AMovingPlatformCharacter* MovingPlatform = Cast<AMovingPlatformCharacter>(CurrentBaseActor);
		if (IsValid(Actor_S))
		{
			GameObject* Entity_M = (GameObject*)Actor_S->GetSelfEntity();
			if (Entity_M && Entity_M->GetActorName().Contains(TEXT("MovingPlatform")))
			{
				OnEnterMovingPlatform(Entity_M->ID());
				if (MovingPlatform)
				{
					MovingPlatform->OnPlayerEnterMovingPlatform();
				}
			}
			else 
			{
				LeaveMovePlatform_HitBack = false;
				OnLeaveMovingPlatform(0);
				if (MovingPlatform)
				{
					MovingPlatform->OnPlayerLeaveMovingPlatform();
				}
			}
		}
		else
		{
			LeaveMovePlatform_HitBack = false;
			OnLeaveMovingPlatform(0);
			if (MovingPlatform)
			{
				MovingPlatform->OnPlayerLeaveMovingPlatform();
			}
		}
	}
}

void APlayerCharacter::CreatePartMapByServer(TMap<MODEL_PART_TYPE, FString>& InPartDataMap)
{
	GameObject* SelfEntity = (GameObject*)GetSelfEntity();
	if (SelfEntity)
	{
		FString newValue = (FString)SelfEntity->GetDefinedProperty(TEXT("extraModelNumber"));
		if (!newValue.IsEmpty())
		{
			return;
		}
		InPartDataMap = GetAppearanceComponent()->GetPartDataMapByModelInfo(SelfEntity->GetModelInfo());
	}
}

void APlayerCharacter::OnBindToEntity()
{
	Super::OnBindToEntity();

	SetInitialized(true);
	OnActorCreateFinish.Broadcast();
}

void APlayerCharacter::InitCharacterComponent( )
{
	Super::InitCharacterComponent();
	if (GetSelfEntity()->IsPlayer())
	{
		Tags.AddUnique(TEXT("Account"));

		InitPosSyncComponent();
		InitCameraComponent();
		StartCheckRandomAction();
		InitPlayerControllerMoveComopnent();
	}
	CreateAppearance();
}

void APlayerCharacter::SetPosition(const FVector& newVal, int32 parentID /*= 0*/)
{
	AServerCharacter::SetPosition(newVal, parentID);
	bUpdatePos = true;
}

void APlayerCharacter::OnPlayerPositionSet(const FVector& newVal)
{
	if (ActorIsPlayer())
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::OnPlayerPositionSet EntityID[%d] Pos x=%f y=%f z=%f"), EntityId, newVal.X, newVal.Y, newVal.Z);

		//获取行为interface
		URolePerformanceInterface* Performance = Cast<URolePerformanceInterface>
			(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface")));
		if (IsValid(Performance))
		{
			Performance->OnGoToSameLevel();
		}
	}
}

void APlayerCharacter::InitFilterActorComponent()
{
	bool IsStartActiveFilter;
	if (GetSelfEntity()->IsPlayer())
	{
		SetFilterComponent(NewObject<UDumbFilterActorComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr));
		IsStartActiveFilter = false;
	}
	else
	{
		SetFilterComponent(NewObject<URoleFilterActorComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr));
		IsStartActiveFilter = true;
	}
	GetFilterComponent()->RegisterComponent();
	GetFilterComponent()->InitFilter(IsStartActiveFilter);
}

void APlayerCharacter::InitPosSyncComponent()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::InitPosSyncComponent EntityID[%d]"), EntityId);
	PosSyncComp = NewObject<UPosSyncComponent>(this, "TransFormControl", RF_NoFlags, nullptr, false, nullptr);
	PosSyncComp->RegisterComponent();
	PosSyncComp->Init(EntityId);
	PosSyncComp->setTickDoing(true);
}


void APlayerCharacter::InitCameraComponent()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::InitCameraComponent EntityID[%d]"), EntityId);
	CameraComponent->Activate();
	if (APlayerController* controller = UGolbalBPFunctionLibrary::GetCS3PlayerController())
	{
		controller->SetViewTargetWithBlend(this);
	}
}

void APlayerCharacter::InitPlayerControllerMoveComopnent()
{
	ACS3PlayerController* CS3PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(CS3PlayerController) && ActorIsPlayer())
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::InitPlayerControllerMoveComopnent EntityID[%d]"), EntityId);
		CS3PlayerController->SetPlayerControllerMoveComponentTickEnabled(true);
	}
}

void APlayerCharacter::DeactivatePlayerControllerMoveComopnent()
{
	ACS3PlayerController* CS3PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(CS3PlayerController) && ActorIsPlayer())
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::DeactivatePlayerControllerMoveComopnent EntityID[%d]"), EntityId);
		CS3PlayerController->SetPlayerControllerMoveComponentTickEnabled(false);
	}
}

void APlayerCharacter::reqNetwordTime()
{
	CS3Role* owner = (CS3Role*)GetSelfEntity();
	if (owner != nullptr)
	{
		owner->networkTest();
	}
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(reqNetwordTimeHandle, this, &APlayerCharacter::reqNetwordTime, 4.0f, false);
}

void APlayerCharacter::clearNetwordTime()
{
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(reqNetwordTimeHandle);
}

void APlayerCharacter::OnSetNetworkTime_Implementation(int32 t)
{

}

void APlayerCharacter::ResetCameraData()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("APlayerCharacter::ResetCameraData EntityID[%d]"), EntityId);
	UGolbalBPFunctionLibrary::SetCameraTargetArmLength(SpringArmCompent, 1500.0f);

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	//玩家默认设置
	if (IsValid(PlayerController))
	{
		PlayerController->SetControlRotation(GetActorRotation() - FRotator(17.0f, 0.0f, 0.0f));
	}	
}

void APlayerCharacter::GetPenetrationAdjustment()
{
	// 所有的客户端控制的移动只对本地玩家生效
	if (EntityId == UGolbalBPFunctionLibrary::GetPlayerID() && GetCharacterMovement()->CurrentFloor.HitResult.bStartPenetrating)
	{
		// 这个函数主要是用来修正玩家被模型卡住了，向外推的
		FHitResult Hit(GetCharacterMovement()->CurrentFloor.HitResult);
		Hit.TraceEnd = Hit.TraceStart + FVector(0.f, 0.f, 2.4f);
		FVector RequestedAdjustment = Cast<UMovementComponent>(GetCharacterMovement())->GetPenetrationAdjustment(Hit);
		if (FMath::IsNearlyZero(RequestedAdjustment.Size()))
		{
			return;
		}
		// 当前碰撞的组件
		UPrimitiveComponent* Component = GetCharacterMovement()->CurrentFloor.HitResult.Component.Get();

		// 边界范围
		FBoxSphereBounds Bounds;

		if (Cast<USkeletalMeshComponent>(Component))
		{
			Bounds = Cast<USkeletalMeshComponent>(Component)->SkeletalMesh->GetBounds();
			// 计算放缩
			Bounds.BoxExtent = Bounds.BoxExtent * Component->GetComponentScale();
			Bounds.Origin = Bounds.Origin * Component->GetComponentScale();
		}
		else if (Cast<UStaticMeshComponent>(Component))
		{
			Bounds = Cast<UStaticMeshComponent>(Component)->GetStaticMesh()->GetBounds();
			Bounds.BoxExtent = Bounds.BoxExtent * Component->GetComponentScale();
			Bounds.Origin = Bounds.Origin * Component->GetComponentScale();
		}
		else if (Cast<UShapeComponent>(Component))
		{
			Bounds = Cast<UShapeComponent>(Component)->CalcBounds(Component->GetComponentTransform());
			Bounds.Origin = Bounds.Origin - Component->GetComponentLocation();
		}

		// 判断下有没有边界信息
		if (!FMath::IsNearlyZero(Bounds.SphereRadius))
		{
			//射线检测的方向
			FVector Direction;

			//射线检测的长度
			float TraceLength;

			// 计算射线检测的长度
			TraceLength = Bounds.BoxExtent.X > Bounds.BoxExtent.Y ? Bounds.BoxExtent.X : Bounds.BoxExtent.Y;
			TraceLength += GetCapsuleComponent()->GetScaledCapsuleRadius();
			FVector OtherOrigin = FVector(FVector2D(Bounds.Origin + Component->GetOwner()->GetActorLocation()), GetActorLocation().Z);
			Direction = (GetActorLocation() - OtherOrigin).GetSafeNormal();
			// 射线起点
			FVector Start = OtherOrigin + Direction * TraceLength;
			FCollisionQueryParams TraceParams;
			// 忽略自己
			TraceParams.AddIgnoredActor(this);
			// 忽略组件
			TArray<USceneComponent*> ComponentList;
			Component->GetOwner()->GetRootComponent()->GetChildrenComponents(false, ComponentList);
			ComponentList.Remove(Component);
			for (int i = 0; i < ComponentList.Num(); i++)
			{
				TraceParams.AddIgnoredComponent(Cast<UPrimitiveComponent>(ComponentList[i]));
			}
			// 用射线检测边界
			TArray<FHitResult> HitResultList;
			GetWorld()->LineTraceMultiByChannel(HitResultList, Start, OtherOrigin, ECC_Visibility, TraceParams);
			//DrawDebugLine(GetWorld(), Start, OtherOrigin, FColor::Red, false, 50);

			FVector HitResultPoint = FVector(0);
			for (int32 i = 0; i < HitResultList.Num(); i++)
			{
				if (HitResultList[i].Component.Get() == Component)
				{
					HitResultPoint = HitResultList[i].Location;
					break;
				}
			}

			// 没有碰到的情况下，直接用射线的起点作为碰撞点
			if (FMath::IsNearlyZero(HitResultPoint.Size()) && (Start - GetActorLocation()).Size() < 500.f)
			{
				HitResultPoint = Start;
			}

			FVector Distance = HitResultPoint + GetCapsuleComponent()->GetScaledCapsuleRadius() * Direction;
			if (FMath::Abs(FloorTrace(Distance).Z - Distance.Z) > 500.f) return;

			RequestedAdjustment = Distance - GetActorLocation();

			//DrawDebugPoint(GetWorld(), HitResultPoint,5, FColor::Black, false, 50);
			//DrawDebugPoint(GetWorld(), Distance, 5, FColor::White, false, 50);


			// 用导航判断是否可到达指定的地点
			AController* TempController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

			if (TempController)
			{
				//UNavigationSystem* NavSys = UNavigationSystem::GetCurrent(Controller->GetWorld());
				UNavigationSystemV1* NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(TempController->GetWorld());
				//UPathFollowingComponent* PFollowComp = nullptr;
				//UObject* PFollowComp = nullptr;
				//Controller->InitNavigationControl(PFollowComp);
				UPathFollowingComponent* PFollowComp = UGolbalBPFunctionLibrary::InitNavigationControl(*TempController);
				const ANavigationData* NavData = Cast<ANavigationData>(NavSys->GetNavDataForProps(TempController->GetNavAgentPropertiesRef()));

				if (NavData)
				{
					FPathFindingQuery Query(TempController, *NavData, TempController->GetNavAgentLocation(), RequestedAdjustment + GetActorLocation());
					FPathFindingResult Result = NavSys->FindPathSync(Query);

					if (Result.IsSuccessful())
					{
						// 这边不适用ResolvePenetration的原因是这个函数的内部会去调用碰撞的事件，这个函数也是碰撞事件那边调用过来的，如果出不去就会造成死循环
						// 可以适当把距离调大一些，但是边界的范围可能比模型大很多，不是很好看，所以直接设置玩家的位置了
						AddActorWorldOffset(RequestedAdjustment, false, nullptr, ETeleportType::TeleportPhysics);
						GetCharacterMovement()->bForceNextFloorCheck = true;
						SetActorLocation(FloorTrace(GetActorLocation()));
					}
				}
			}

			// 通知组件碰撞事件，除了玩家
			if (!Cast<APlayerCharacter>(Hit.Actor.Get()) && Hit.Component->BodyInstance.bNotifyRigidBodyCollision)
			{
				Hit.Component->OnComponentHit.Broadcast(Hit.Component.Get(), this, GetCapsuleComponent(), RequestedAdjustment.GetSafeNormal2D(), Hit);
				//重置弹开事件
				bOnHitBack = false;
				LastHit = FHitResult();
			}

		}
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("Bounds :%f ,%f ,%f"), Bounds.BoxExtent.X * 2, Bounds.BoxExtent.Y * 2, Bounds.BoxExtent.Z * 2);
	}
}

void APlayerCharacter::DispatchHitEvent()
{
	if (EntityId == UGolbalBPFunctionLibrary::GetPlayerID())
	{
		FHitResult Hit;

		// 没有分配碰撞事件，本帧分配，并重置
		if (bOnHitBack)
		{
			LastHit.Component->OnComponentHit.Broadcast(LastHit.Component.Get(), this, GetCapsuleComponent(), LastHit.Location, LastHit);
			LastHit = Hit;
			bOnHitBack = false;
		}

		Hit = GetCharacterMovement()->CurrentFloor.HitResult;
		// 检测到了有弹开事件发生，但是后续会检查是否非陪碰撞事件
		if (Hit.bBlockingHit && Hit.bStartPenetrating && Hit.Component->BodyInstance.bNotifyRigidBodyCollision)
		{
			bOnHitBack = true;
			LastHit = Hit;
		}
	}
}

void APlayerCharacter::StartCheckingInteractiveTarget()
{
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(InteractiveTimerHandle, this, &APlayerCharacter::RefreshInteractiveTarget, 2.0f, true);
}

void APlayerCharacter::StopCheckingInteractiveTarget()
{
	if (InteractiveTimerHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(InteractiveTimerHandle);
	}
	ResetInteractiveData();
}

void APlayerCharacter::RefreshInteractiveTarget()
{
	///<死亡状态下不
	if (IsState(ENTITY_STATE::EntityStateDead))
	{
		SetInteractiveTarget(nullptr);
		return;
	}

	///<当前状态为NONE 或者选中可交互目标没有按F键的时候
	if ((EPlayerInteractiveState == APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_NODE) ||
		(EPlayerInteractiveState == APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_SECLECTTARGET) ||
		(EPlayerInteractiveState == APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_SUCCESS))
	{
		///<当前玩家目标在玩家可交互范围时，交互目标设置为当前玩家目标
		if (IsValid(CurPlayerTarget) && InteractivityList.Contains(CurPlayerTarget) && CurPlayerTarget->CanGossipWith())
		{
			SetInteractiveTarget(CurPlayerTarget);
		}
		else
		{
			if (InteractivityList.Num() > 0)
			{
				SetInteractiveTarget(SortInteractiveTarget());
			}
		}
	}
}

void APlayerCharacter::SetInteractiveTarget(AServerCharacter* Target)
{
	if (IsValid(Target))
	{
		EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_SECLECTTARGET;
		CurInteractiveTarget = Target;
		OnInteractiveTargetChange();
	}
	else
	{
		EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_NODE;
		CurInteractiveTarget = nullptr;
		OnInteractiveTargetChange();
	}
}

AServerCharacter* APlayerCharacter::SortInteractiveTarget()
{
	if (IsValid(this) && ActorIsPlayer() && InteractivityList.Num() > 0)
	{
		UStateInterface* StateInterface = GetEntityInterface_Cache().StateInterface;
		///如果当前状态为受保护状态时 不会添加新的目标对象
		if (IsValid(StateInterface)&& StateInterface->HasEffectState(EFFECT_STATE::EFFECT_STATE_PROTECT))
		{
			return nullptr;
		}
		///<清除数组中无效数据	
		for (auto TempInteractivity = InteractivityList.CreateIterator(); TempInteractivity; ++TempInteractivity)
		{
			if (!IsValid(*TempInteractivity))
			{
				InteractivityList.RemoveAt(TempInteractivity.GetIndex());
			}
		}
		///< 距离》45°逆时钟》类型(掉落》NPC》SpellBox)
		InteractivityList.Sort([this](AServerCharacter& a, AServerCharacter& b) -> bool
		{
			///<当前不可交互往后移
			if (!((&a)->CanGossipWith()))
			{
				//CS3_Warning(TEXT("APlayerCharacter::SortInteractiveTarget !((&a)->CanGossipWith())"));
				return true;
			}
			if (IsValid(this) && IsValid(&a) && IsValid(&b))
			{
				float da = UGolbalBPFunctionLibrary::GetActorDistance(&a, this);
				float db = UGolbalBPFunctionLibrary::GetActorDistance(&b, this);
				if (da == db)
				{
					//CS3_Warning(TEXT("APlayerCharacter::SortInteractiveTarget da == db"));
					//获取玩家与A的向量
					FRotator PALookRotation = UKismetMathLibrary::FindLookAtRotation(this->GetActorLocation(), (&a)->GetActorLocation());
					FRotator PARotator = UKismetMathLibrary::NormalizedDeltaRotator(PALookRotation, this->GetActorRotation());
					float PAYaw = PARotator.Yaw;

					//获取玩家与B的向量
					FRotator PBLookRotation = UKismetMathLibrary::FindLookAtRotation(this->GetActorLocation(), (&b)->GetActorLocation());
					FRotator PBRotator = UKismetMathLibrary::NormalizedDeltaRotator(PBLookRotation, this->GetActorRotation());
					float PBYaw = PBRotator.Yaw;

					if (PAYaw == PBYaw)
					{
						//CS3_Warning(TEXT("APlayerCharacter::SortInteractiveTarget PAYaw == PBYaw"));
						if ((&a)->CharacterClassName == TEXT("DropBoxCharacter"))
						{
							//CS3_Warning(TEXT("APlayerCharacter::SortInteractiveTarget (&a)->CharacterClassName == DropBoxCharacter"));
							return false;
						}
						else if ((&a)->CharacterClassName == TEXT("NPCCharacter"))
						{
							if ((&b)->CharacterClassName == TEXT("DropBoxCharacter"))
							{
								return true;
							}
							return false;
						}
						else if ((&a)->CharacterClassName == TEXT("SpellBoxCharacter"))
						{
							if ((&b)->CharacterClassName == TEXT("DropBoxCharacter") || (&b)->CharacterClassName == TEXT("NPCCharacter"))
							{
								return true;
							}
							return false;
						}
					}
					else if (PAYaw >= 0 && PAYaw <= 45)
					{
						//CS3_Warning(TEXT("APlayerCharacter::SortInteractiveTarget PAYaw >= 0 && PAYaw <= 45"));
						if (PBYaw >= 0 && PBYaw <= 45)
						{
							return PAYaw < PBYaw;
						}
						///<PAYaw 优先于 PBYaw 
						return false;
					}
					else if (PAYaw >= -180 && PAYaw < 0)
					{
						if (PBYaw >= 0 && PBYaw <= 45)
						{
							return true;
						}
						else if (PBYaw > 45 && PBYaw <= 180)
						{
							return false;
						}
						return PAYaw > PBYaw;
					}
					else if (PAYaw > 45 && PAYaw <= 180)
					{
						if (PBYaw >= 0 && PBYaw <= 45)
						{
							return true;
						}
						else if (PBYaw >= -180 && PBYaw < 0)
						{
							return true;
						}
						return PAYaw > PBYaw;
					}
				}
				else
				{
					//CS3_Warning(TEXT("APlayerCharacter::SortInteractiveTarget da < db da=%f  db=%f"), da, db);
					return da < db;
				}
			}
			return false;
		});

		for (auto Actor : InteractivityList)
		{
			if (IsValid(Actor) && Actor->CanGossipWith())
			{
				//CS3_Warning(TEXT("APlayerCharacter::SortInteractiveTarget Actor->CanGossipWith() return Actor"));
				return Actor;
			}
		}
	}
	return nullptr;
}

void APlayerCharacter::AddToInteractivityList(AServerCharacter * Target)
{
	if (IsValid(Target))
	{
		if (!InteractivityList.Contains(Target))
		{
			InteractivityList.Add(Target);
			RefreshInteractiveTarget();
		}
	}
}

void APlayerCharacter::RemoveFromInteractivityList(AServerCharacter * Target)
{
	if (IsValid(Target))
	{
		if (InteractivityList.Contains(Target))
		{
			InteractivityList.Remove(Target);
		}
		if (IsValid(CurInteractiveTarget) && CurInteractiveTarget == Target)
		{
			SetInteractiveTarget(nullptr);
			RefreshInteractiveTarget();
		}
	}
}

void APlayerCharacter::RotateRroundToTarget(AActor* Target, float Speed = 100.0f, float Disatance = 100.0f, float Height = 0.0f, float angle = 0.0f)
{
	if (!RotateToTargetTimerHander.IsValid()&&IsValid(Target))
	{
		TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, RotateToTargetTimerHander, FTimerDelegate::CreateLambda([DelayThisPtr, Speed, angle, Target, Disatance, Height]()
		{
	
			float NewX = UKismetMathLibrary::DegCos(DelayThisPtr->GetWorld()->GetTimeSeconds() * Speed)* Disatance + Target->GetActorLocation().X;
			float NewY = UKismetMathLibrary::DegSin(DelayThisPtr->GetWorld()->GetTimeSeconds() * Speed)* Disatance + Target->GetActorLocation().Y;
			float NewZ = Target->GetActorLocation().Z + Height;
			DelayThisPtr->SetActorLocation(FVector(NewX, NewY, NewZ));
			FRotator NewRot = UGolbalBPFunctionLibrary::GetLookAtRotator(DelayThisPtr->GetActorLocation(),Target->GetActorLocation());
			DelayThisPtr->SetActorRotation(NewRot);
			DelayThisPtr->CameraComponent->SetRelativeRotation(FRotator(angle, 0.0f, 0.0f));

		}), 0.01f, true);
	}
}

void APlayerCharacter::StopRoateToTarget()
{
	if (RotateToTargetTimerHander.IsValid())
	{
		this->CameraComponent->SetRelativeRotation(FRotator::ZeroRotator);
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(RotateToTargetTimerHander); 
	}
}

void APlayerCharacter::ResetInteractiveData()
{
	SetInteractiveTarget(nullptr);
	InteractivityList.Reset();
}

void APlayerCharacter::UpdateCurrentFloor()
{
	UCharacterMovementComponent* MovementComponent = GetCharacterMovement();

	//更新当前的地板
	MovementComponent->FindFloor(MovementComponent->UpdatedComponent->GetComponentLocation(), MovementComponent->CurrentFloor, false, NULL);

	//处理是否有弹开发生，如果有并被卡住，则会继续调用GetPenetrationAdjustment()强制弹开
	//更新地板数据时，请保持碰撞物体每次移动小于当前胶囊体半径
	if (MovementComponent->CurrentFloor.HitResult.bStartPenetrating)
	{
		// The floor check failed because it started in penetration
		// We do not want to try to move downward because the downward sweep failed, rather we'd like to try to pop out of the floor.
		FHitResult Hit(MovementComponent->CurrentFloor.HitResult);
		Hit.TraceEnd = Hit.TraceStart + FVector(0.f, 0.f, 2.4f);
		const FVector RequestedAdjustment = Cast<UMovementComponent>(MovementComponent)->GetPenetrationAdjustment(Hit);
		MovementComponent->ResolvePenetration(RequestedAdjustment, Hit, GetCharacterMovement()->UpdatedComponent->GetComponentQuat());
		MovementComponent->bForceNextFloorCheck = true;
	}
}

void APlayerCharacter::RPC_logoff()
{
	CS3Role* owner = (CS3Role*)GetSelfEntity();
	//KBEngine::Entity* entity = GetSelfEntity();
	if (owner == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_logoff : owner!"));
		return;
	}
	//KBEngine::FVariantArray args;
	//Entity->BaseCall(TEXT("logoff"), args);
	owner->Logoff();
}

void APlayerCharacter::RPC_logout()
{
	CS3Role* owner = (CS3Role*)GetSelfEntity();
	//KBEngine::Entity* entity = GetSelfEntity();
	if (owner == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_logout : owner!"));
		return;
	}
	owner->Logout();
	//KBEngine::FVariantArray args;

	//owner->BaseCall(TEXT("logout"), args);
}

void APlayerCharacter::RPC_SetBlendDir(const int32& INT32_1)
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (IsValid(RoleInterface))
	{
		RoleInterface->RequestBlendDir(float(INT32_1));
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_SetBlendDir : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;
	//args.Add(INT32_1);

	//entity->CellCall(TEXT("SetBlendDir"), args);
}

void APlayerCharacter::RPC_onClientSetAoi(const FString& STRING_1)
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->onClientSetAoi(STRING_1); 
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_onClientSetAoi : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;
	//args.Add(STRING_1);

	//entity->CellCall(TEXT("onClientSetAoi"), args);
}

void APlayerCharacter::RPC_onClientResetAoi()
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->onClientResetAoi();
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_onClientResetAoi : entity!"));
	//	return;
	//}
	//
	//	KBEngine::FVariantArray args;
	//
	//entity->CellCall(TEXT("onClientResetAoi"), args);
}

void APlayerCharacter::RPC_onPlayerUnderArea()
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->onPlayerUnderArea();
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_onPlayerUnderArea : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;

	//entity->CellCall(TEXT("onPlayerUnderArea"), args);
}

void APlayerCharacter::RPC_enterWaterArea()
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->enterWaterArea();
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_enterWaterArea : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;

	//entity->CellCall(TEXT("enterWaterArea"), args);
}

void APlayerCharacter::RPC_leaveWaterArea()
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->leaveWaterArea();
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_leaveWaterArea : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;

	//entity->CellCall(TEXT("leaveWaterArea"), args);
}

void APlayerCharacter::RPC_enterMaterialArea(const FString& STRING_1)
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->enterMaterialArea(STRING_1);
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_enterMaterialArea : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;
	//args.Add(STRING_1);

	//entity->CellCall(TEXT("enterMaterialArea"), args);
}

void APlayerCharacter::RPC_leaveMaterialArea(const FString& STRING_1)
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->leaveMaterialArea(STRING_1);
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_leaveMaterialArea : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;
	//args.Add(STRING_1);

	//entity->CellCall(TEXT("leaveMaterialArea"), args);
}

void APlayerCharacter::RPC_RequestPlayRandomAction()
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->RequestPlayRandomAction();
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_RequestPlayRandomAction : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;

	//entity->CellCall(TEXT("RequestPlayRandomAction"), args);
}

void APlayerCharacter::RPC_setPositionFromClient(const FVector& POSITION_1)
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->setPositionFromClient(POSITION_1);
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_setPositionFromClient : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;
	//args.Add(POSITION_1);

	//entity->CellCall(TEXT("setPositionFromClient"), args);
}

void APlayerCharacter::AtuoAdjustViewTargetWithBlend()
{
	if (!ActorIsPlayer())return;

	AtuoAdjustView = false;
	if (IsValid(UUECS3GameInstance::Instance))
	{
		TWeakObjectPtr<APlayerCharacter> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, SetViewTargetWithBlendHandle, FTimerDelegate::CreateLambda([DelayThisPtr]() {
			if (DelayThisPtr.IsValid())
			{
				ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
				if (!IsValid(PlayerController))
				{
					CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::AtuoAdjustViewTargetWithBlend : FlyPatrolComponent!"));
					return;
				}
				if (IsValid(PlayerController->GetAtkStateMar())&& !PlayerController->GetAtkStateMar()->IsHaveState(EATTACT_STATE::NAVIGATE_MOVE))
				{
					DelayThisPtr->UnAdjustViewTargetWithBlend();
					return;
				}
				bool IsMouseXDown = PlayerController->IsInputKeyDown(EKeys::LeftMouseButton);
				bool IsMouseYDown = PlayerController->IsInputKeyDown(EKeys::RightMouseButton);
				if (IsMouseXDown || IsMouseYDown)
				{
					DelayThisPtr->AtuoAdjustedPitchAlpha = 0.0f;
					DelayThisPtr->AtuoAdjustView = false;
					DelayThisPtr->AtuoAdjustYawAlpha = 0.0f;
					return;
				}
				//获取玩家控制转向
				FRotator ControlRotator = DelayThisPtr->GetControlRotation();
				//获取相对玩家的前方向
				FVector ForwardByControl = UKismetMathLibrary::GetForwardVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));
				//获取玩家控制转向
				FRotator ActorRotator = DelayThisPtr->GetActorRotation() - FRotator(17.0f, 0.0f, 0.0f);
				//获取相对玩家的前方向
				FVector ForwardByActor = UKismetMathLibrary::GetForwardVector(FRotator(0.0f, ActorRotator.Yaw, 0.0f));

				float dotResult = FVector::DotProduct(UKismetMathLibrary::Normal(ForwardByActor), UKismetMathLibrary::Normal(ForwardByControl));
				float AimAtAngle = FMath::RadiansToDegrees(FMath::Acos(dotResult));

				if (!FMath::IsNearlyZero(AimAtAngle))
				{
					if (!DelayThisPtr->AtuoAdjustView)
					{
						DelayThisPtr->AtuoAdjustedPitchAlpha = 0.0f;
						DelayThisPtr->AtuoAdjustYawAlpha = 0.0f;
						DelayThisPtr->AtuoAdjustView = true;
					}

					FRotator RotatorYaw, RotatorPitch;

					if (DelayThisPtr->AtuoAdjustYawAlpha < 1.0f)
					{
						DelayThisPtr->AtuoAdjustYawAlpha += 0.0001f;
						RotatorYaw = UKismetMathLibrary::REase(ControlRotator, FRotator(ControlRotator.Pitch, ActorRotator.Yaw, ControlRotator.Roll), DelayThisPtr->AtuoAdjustYawAlpha, true, EEasingFunc::Linear);
					}
					else
					{
						DelayThisPtr->AtuoAdjustYawAlpha = 1.0f;
						RotatorYaw = FRotator(ControlRotator.Pitch, ActorRotator.Yaw, ControlRotator.Roll);
					}

					if (DelayThisPtr->AtuoAdjustedPitchAlpha < 1.0f)
					{
						DelayThisPtr->AtuoAdjustedPitchAlpha += 0.001f;
						RotatorPitch = UKismetMathLibrary::REase(ControlRotator, FRotator(ActorRotator.Pitch, ControlRotator.Yaw, ControlRotator.Roll), DelayThisPtr->AtuoAdjustedPitchAlpha, true, EEasingFunc::Linear);
					}
					else
					{
						DelayThisPtr->AtuoAdjustedPitchAlpha = 1.0f;
						RotatorPitch = FRotator(ActorRotator.Pitch, ControlRotator.Yaw, ControlRotator.Roll);
					}

					if (FMath::IsNearlyEqual(DelayThisPtr->AtuoAdjustYawAlpha, 1.0f) && FMath::IsNearlyEqual(DelayThisPtr->AtuoAdjustedPitchAlpha, 1.0f))
					{
						DelayThisPtr->AtuoAdjustView = false;
						DelayThisPtr->AtuoAdjustedPitchAlpha = 0.0f;
						DelayThisPtr->AtuoAdjustYawAlpha = 0.0f;
						PlayerController->SetControlRotation(ActorRotator);
						return;
					}
					FRotator RotatorVector = FRotator(RotatorPitch.Pitch, RotatorYaw.Yaw, ControlRotator.Roll);
					PlayerController->SetControlRotation(RotatorVector);
				}
				else
				{
					DelayThisPtr->AtuoAdjustView = false;
					DelayThisPtr->AtuoAdjustedPitchAlpha = 0.0f;
					DelayThisPtr->AtuoAdjustYawAlpha = 0.0f;
					PlayerController->SetControlRotation(ActorRotator);
				}
			}
		}), 0.02f, true);
	}
}

void APlayerCharacter::UnAdjustViewTargetWithBlend()
{
	if (!ActorIsPlayer())return;
	if (SetViewTargetWithBlendHandle.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(SetViewTargetWithBlendHandle);
		}
	}
}

void APlayerCharacter::RPC_verifyClientTime(const int32& INT32_1)
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->verifyClientTime(INT32_1);
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_verifyClientTime : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;
	//args.Add(INT32_1);

	//entity->CellCall(TEXT("verifyClientTime"), args);
}

void APlayerCharacter::RPC_updateMoveType(const int32& INT32_1)
{
	GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (CS3PlayerEntity == nullptr) return;

	URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
	if (RoleInterface)
	{
		RoleInterface->updateMoveType(INT32_1);
	}
	//KBEngine::Entity* entity = GetSelfEntity();
	//if (entity == nullptr)
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:APlayerCharacter::RPC_updateMoveType : entity!"));
	//	return;
	//}

	//KBEngine::FVariantArray args;
	//args.Add(INT32_1);

	//entity->CellCall(TEXT("updateMoveType"), args);
}


CONTROL_COMPILE_OPTIMIZE_END
