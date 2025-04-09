// Fill out your copyright notice in the Description page of Project Settings.

#include "GameCharacter.h"
#include "Kismet/KismetMathLibrary.h"
#include "Components/CapsuleComponent.h"
#include "Manager/ResourceManager.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Action/BaseAnimInstance.h"
#include "Actor/Particle/EffectEmitter.h"
#include "Component/AppearanceComponent.h"
#include "Component/CollisionComponent.h"
#include "Component/PerformanceComponent.h"
#include "Component/ActorTraceMoveComponent.h"
#include "Manager/ParticleManager.h"
#include "Util/ConvertUtil.h"
#include "Manager/CfgManager.h"
#include "Util/CS3Debug.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameDevelop/CS3GameViewportClient.h"
#include "Manager/ModifyFaceManager.h"
#include "Kismet/KismetSystemLibrary.h"
#include "SignificanceManager.h"
#include "SceneManagement.h"
#include "Kismet/GameplayStatics.h"
#include "GameData/GameDefault.h"
#include "GameData/RoleJumpData.h"

CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("CreateAllMesh"), STAT_CreateAllMesh, STATGROUP_AGameCharacter);
DECLARE_CYCLE_STAT(TEXT("InitBaseComponent"), STAT_InitBaseComponent, STATGROUP_AGameCharacter);
DECLARE_CYCLE_STAT(TEXT("PixelsBeyondBounds"), STAT_PixelsBeyondBounds, STATGROUP_AGameCharacter);
DECLARE_CYCLE_STAT(TEXT("PlayAction"), STAT_AGameCharacter_PlayAction, STATGROUP_AGameCharacter);
DECLARE_CYCLE_STAT(TEXT("PlayContinuousActions"), STAT_AGameCharacter_PlayContinuousActions, STATGROUP_AGameCharacter);
DECLARE_CYCLE_STAT(TEXT("CheckPartHideByAction"), STAT_CheckPartHideByAction, STATGROUP_AGameCharacter);
DECLARE_CYCLE_STAT(TEXT("OnCreateApperanceOver"), STAT_OnCreateApperanceOver, STATGROUP_AGameCharacter);
DECLARE_CYCLE_STAT(TEXT("UpdateCapsuleComponent"), STAT_UpdateCapsuleComponent, STATGROUP_AGameCharacter);
DECLARE_CYCLE_STAT(TEXT("BindMesh"), STAT_BindMesh, STATGROUP_AGameCharacter);
DECLARE_CYCLE_STAT(TEXT("UnBindMesh"), STAT_UnBindMesh, STATGROUP_AGameCharacter);

AGameCharacter::AGameCharacter():BaseAnimInstance(nullptr), InitActionId("None")
{
	ActionDatas.Empty();
	RandomActionDatas.Empty();
	MeshPartComponentDatas.Empty();
	IsHitMaterialCreated = false;

	BindMeshComponentDatas.Empty();
	BindMeshEffectUID.Empty();
	CharacterClassName = TEXT("GameCharacter");
	AutoPossessAI = EAutoPossessAI::Disabled;	
	CreateBaseMesh();
	InitBaseComponent();
	GetCharacterMovement()->SetAutoActivate(false);
}

void AGameCharacter::BeginPlay()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		OnEndPlay.AddUniqueDynamic(UUECS3GameInstance::Instance, &UUECS3GameInstance::OnActorEndPlay);
	}
	// character需要开启头顶信息，重写此方法
	ReSetOpenScen3DUI();
	if (!OpenScene3DUI&&IsValid(HeadInfo3DUI))
	{
		HeadInfo3DUI->DestroyComponent();
		HeadInfo3DUI = nullptr;
	}
	SetMeshMasterPoseComponent(); 
	SynchronousMeshTick();

	Super::BeginPlay();

	// 向重要度管理器注册信息
 	if (USignificanceManager* SignificanceManager = FSignificanceManagerModule::Get(GetWorld()))
 	{
 		SignificanceManager->RegisterObject(this, CharacterClassName, [](USignificanceManager::FManagedObjectInfo* ManagedObjectInfo, const FTransform& ViewTransform)
 			{
 				// 计算完Significance
				if (AGameCharacter* GameCharacter = Cast<AGameCharacter>(ManagedObjectInfo->GetObject()))
				{
					if (UCS3GameViewportClient* CS3GameViewportClient = Cast<UCS3GameViewportClient>(GameCharacter->GetWorld()->GetGameViewport()))
					{
						const float ScreenDistance = FVector::Dist(GameCharacter->GetActorLocation(), ViewTransform.GetLocation());
						float ScreenSize = ComputeBoundsScreenSize(FVector::ZeroVector, GameCharacter->GetBoundRadius(), FVector(0.0f, 0.0f, ScreenDistance), CS3GameViewportClient->ProjMatrix);

						float a = FVector::DotProduct(ViewTransform.Rotator().Vector(), GameCharacter->GetActorLocation() - ViewTransform.GetLocation());
						if (a <= 0) //是否在摄像机后方
						{
							ScreenSize = 0.f;
						}

						return ScreenSize;
					}

				}
 				return 0.0f;
 			}, USignificanceManager::EPostSignificanceType::Concurrent, [](USignificanceManager::FManagedObjectInfo* ManagedObjectInfo, float OldSignificance, float NewSignificance, bool IsCancellation)
 			{
 				// 计算完Significance后的处理函数
				if (!IsCancellation)
				{
					const TArray<float>& SignificanceLOD = UGameDefault::StaticClass()->GetDefaultObject<UGameDefault>()->SignificanceLOD;
					if (AGameCharacter* GameCharacter = Cast<AGameCharacter>(ManagedObjectInfo->GetObject()))
					{
						GameCharacter->OldSignificance = GameCharacter->Significance;

						if (NewSignificance <= SignificanceLOD[3])
						{
							GameCharacter->Significance = SignificanceType::Incomplete;
						}
						else if (NewSignificance <= SignificanceLOD[2])
						{
							GameCharacter->Significance = SignificanceType::Bald;
						}
						else if (NewSignificance <= SignificanceLOD[1])
						{
							GameCharacter->Significance = SignificanceType::Defect;
						}
						else if (NewSignificance <= SignificanceLOD[0])
						{
							GameCharacter->Significance = SignificanceType::Near;
						}
						else
						{
							GameCharacter->Significance = SignificanceType::Complete;
						}
					}
				}
 			});
		// 开始时触发一次
		OnSignificanceChange();
 	}
}

void AGameCharacter::PostInitProperties()
{
	Super::PostInitProperties();
	IsApperanceLoadingOver = false;

}

void AGameCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("AGameCharacter::EndPlay Name[%s]") , *GetName());
 	// 向重要度管理器注销信息
 	if (USignificanceManager* SignificanceManager = FSignificanceManagerModule::Get(GetWorld()))
 	{
 		SignificanceManager->UnregisterObject(this);
 	}

	if (!BaseAnimInstance)
	{
		BaseAnimInstance = nullptr;
	}

	ActionDatas.Empty();
	RandomActionDatas.Empty();
	OnModelChangeAppearanceOverDelegate.Clear();
	TArray<AActor*> Actors;
	this->GetAttachedActors(Actors);
	for (auto attachActor : Actors)
	{
		if (Cast<AEffectEmitter>(attachActor))
		{
#if WITH_EDITOR
			if (!UUECS3GameInstance::Instance)
			{
				attachActor->Destroy();
			}
			else
			{
#endif	
				UUECS3GameInstance::Instance->ParticleManager->Stop(Cast<AEffectEmitter>(attachActor),true, true, true, false);
#if WITH_EDITOR
			}
#endif
		}
		else
		{
			attachActor->Destroy();
		}
	}
	Super::EndPlay(EndPlayReason);
}

void AGameCharacter::Destroyed()
{
	CS3_Log(TEXT("Destroy GameCharacter Name[%s]"), *GetName());
	Super::Destroyed();
}

void AGameCharacter::BeginDestroy()
{
	Super::BeginDestroy();
}

void AGameCharacter::CreateBaseMesh()
{
	USkeletalMeshComponent* SKRootMesh_Body = GetMesh();
	SKRootMesh_Body->OnAnimUpdateRateParamsCreated.BindLambda([](FAnimUpdateRateParameters* Parameters) // 设置骨骼模型的更新速率Lod参数,适用于其他的骨骼模型组件
		{
			if (Parameters)
			{
				Parameters->bShouldUseLodMap = false;
				Parameters->bInterpolateSkippedFrames = true;
				//如果出现动画丢帧,就尝试调大AnimUpdateRateLOD值,找到一个平衡点
				Parameters->BaseVisibleDistanceFactorThesholds.Reset(3);
				Parameters->BaseVisibleDistanceFactorThesholds.Append(UGameDefault::StaticClass()->GetDefaultObject<UGameDefault>()->AnimUpdateRateLOD);
			}
		});
	SKRootMesh_Body->bEnableUpdateRateOptimizations = false;///是否开启更新率优化[开启后可能会丢帧，导致表现变差CST-7715]
	SKRootMesh_Body->bDisplayDebugUpdateRateOptimizations = UGameDefault::StaticClass()->GetDefaultObject<UGameDefault>()->bDisplayDebugAnimUpdateRateLOD;

	SKRootMesh_Body->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	SKRootMesh_Body->SetCollisionObjectType(ECC_Pawn);
	SKRootMesh_Body->bLocalSpaceSimulation = true;///是否应用空间模拟1
	SKRootMesh_Body->bReceivesDecals = false;///是否接受贴花
	SKRootMesh_Body->bUseAttachParentBound = false;///是否在附加时使用父边界1
	//SKRootMesh_Body->bPerBoneMotionBlur = false;///是否每块骨骼应用运动模糊
	SKRootMesh_Body->bComponentUseFixedSkelBounds = true;///组件使用固定的骨架边界1
	SKRootMesh_Body->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::OnlyTickPoseWhenRendered;
	SKRootMesh_Body->bUpdateOverlapsOnAnimationFinalize = false;
	SKRootMesh_Body->bSyncAttachParentLOD = false;

	//只需透视功能：bRenderCustomDepth = true
	//使部件不受场景光照影响：下面三个参数都需要(true、1、true)
	SKRootMesh_Body->bRenderCustomDepth = true;///是否开启自定义深度(CST-7692透视效果)
	SKRootMesh_Body->CustomDepthStencilValue = 1;///自定义深度模具值(0~255)
	//SKRootMesh_Body->LightingChannels.bChannel3 = true;///设置光照通道为3（匹配场景的光照FightSource）
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_BODYS, SKRootMesh_Body);

	//默认静态组件
	STMesh_DefaultStatic = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Default_Static"));
	SetStaticMeshCptBaseProperty(STMesh_DefaultStatic);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_STATIC, STMesh_DefaultStatic);
}

void AGameCharacter::CreateRoleMesh()
{
	SCOPE_CYCLE_COUNTER(STAT_CreateAllMesh);
	//头部 
	SKMesh_Heads = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Heads"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Heads);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_HEADS, SKMesh_Heads);
	//套装
	SKMesh_Suits = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Suits"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Suits);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_SUITS, SKMesh_Suits);
	//头发
	SKMesh_Hair = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Hair"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Hair);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_HAIRS, SKMesh_Hair);
	//发饰
	SKMesh_Adorn = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Adorn"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Adorn);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_ADORN, SKMesh_Adorn);
	//头饰
	SKMesh_HeadAdorn = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_HeadAdorn"));
	SetSkeletalMeshCptBaseProperty(SKMesh_HeadAdorn, "Socket_Toushi");
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_HEAD_ADORN, SKMesh_HeadAdorn);
	//面饰
	SKMesh_FaceAdorn = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_FaceAdorn"));
	SetSkeletalMeshCptBaseProperty(SKMesh_FaceAdorn, "Socket_MianShi");
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_FACE_ADORN, SKMesh_FaceAdorn);
	//背饰
	SKMesh_BackAdorn = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_BackAdorn"));
	SetSkeletalMeshCptBaseProperty(SKMesh_BackAdorn, "Socket_Beishi");
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_BACK_ADORN, SKMesh_BackAdorn);
	//腰饰
	SKMesh_WristAdorn = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_WristAdorn"));
	SetSkeletalMeshCptBaseProperty(SKMesh_WristAdorn, "Socket_Yaoshi");
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_WAIST_ADORN, SKMesh_WristAdorn);
	//帽子
	SKMesh_Hat = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Hat"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Hat);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_HAT, SKMesh_Hat);
	//上衣
	SKMesh_Coats = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Coats"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Coats);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_COATS, SKMesh_Coats);
	//护腕
	SKMesh_Wrist = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Wrist"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Wrist);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_WRIST, SKMesh_Wrist);
	//手套
	SKMesh_Gloves = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Gloves"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Gloves);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_GLOVES, SKMesh_Gloves);
	//腰带
	SKMesh_Belt = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SKMesh_Belt"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Belt);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_WAIST, SKMesh_Belt);
	//项链
	SKMesh_Necklace = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SKMesh_Necklace"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Necklace);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_NECKLACE, SKMesh_Necklace);
	//戒指左
	SKMesh_L_RING = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SKMesh_L_RING"));
	SetSkeletalMeshCptBaseProperty(SKMesh_L_RING);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_LHAND_RING, SKMesh_L_RING);
	//戒指右
	SKMesh_R_RING = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SKMesh_R_RING"));
	SetSkeletalMeshCptBaseProperty(SKMesh_R_RING);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_RHAND_RING, SKMesh_R_RING);
	//裤子
	SKMesh_Pants = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Pants"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Pants);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_PANTS, SKMesh_Pants);
	//鞋子
	SKMesh_Shoes = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Shoes"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Shoes);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_SHOES, SKMesh_Shoes);
	//披风
	SKMesh_Cloak = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("SK_Cloak"));
	SetSkeletalMeshCptBaseProperty(SKMesh_Cloak);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_CLOAK, SKMesh_Cloak);

	//武器左
	STMesh_LHweapon = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LHweapon_Static"));
	SetStaticMeshCptBaseProperty(STMesh_LHweapon);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_LWEAPON, STMesh_LHweapon);
	//武器右
	STMesh_RHweapon = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("RHweapon_Static"));
	SetStaticMeshCptBaseProperty(STMesh_RHweapon);
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_RWEAPON, STMesh_RHweapon);

	//武器左（带骨架）
	STMesh_S_LHweapon = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("LHweapon_Skeletal"));
	SetSkeletalMeshCptBaseProperty(STMesh_S_LHweapon, "Socket_Weapon_L");
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON, STMesh_S_LHweapon);
	//武器右（带骨架）
	STMesh_S_RHweapon = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("RHweapon_Skeletal"));
	SetSkeletalMeshCptBaseProperty(STMesh_S_RHweapon, "Socket_Weapon_R");
	MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON, STMesh_S_RHweapon);

	bIsCreateRoleMesh = true;
}

void AGameCharacter::CreateDynamicRoleMesh()
{
	//头部
	if (!IsValid(SKMesh_Heads))
	{
		SKMesh_Heads = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Heads"));
		SKMesh_Heads->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Heads);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_HEADS, SKMesh_Heads);
	}
	//套装
	if (!IsValid(SKMesh_Suits))
	{
		SKMesh_Suits = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Suits"));
		SKMesh_Suits->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Suits);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_SUITS, SKMesh_Suits);
	}
	//头发
	if (!IsValid(SKMesh_Hair))
	{
		SKMesh_Hair = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Hair"));
		SKMesh_Hair->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Hair);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_HAIRS, SKMesh_Hair);
	}
	//发饰
	if (!IsValid(SKMesh_Adorn))
	{
		SKMesh_Adorn = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Adorn"));
		SKMesh_Adorn->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Adorn);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_ADORN, SKMesh_Adorn);
	}
	//头饰
	if (!IsValid(SKMesh_HeadAdorn))
	{
		SKMesh_HeadAdorn = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_HeadAdorn"));
		SKMesh_HeadAdorn->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_HeadAdorn, "Socket_Toushi");
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_HEAD_ADORN, SKMesh_HeadAdorn);
	}
	//面饰
	if (!IsValid(SKMesh_FaceAdorn))
	{
		SKMesh_FaceAdorn = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_FaceAdorn"));
		SKMesh_FaceAdorn->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_FaceAdorn, "Socket_MianShi");
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_FACE_ADORN, SKMesh_FaceAdorn);
	}
	//背饰
	if (!IsValid(SKMesh_BackAdorn))
	{
		SKMesh_BackAdorn = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_BackAdorn"));
		SKMesh_BackAdorn->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_BackAdorn, "Socket_Beishi");
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_BACK_ADORN, SKMesh_BackAdorn);
	}
	//腰饰
	if (!IsValid(SKMesh_WristAdorn))
	{
		SKMesh_WristAdorn = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_WristAdorn"));
		SKMesh_WristAdorn->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_WristAdorn, "Socket_Yaoshi");
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_WAIST_ADORN, SKMesh_WristAdorn);
	}
	//帽子
	if (!IsValid(SKMesh_Hat))
	{
		SKMesh_Hat = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Hat"));
		SKMesh_Hat->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Hat);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_HAT, SKMesh_Hat);
	}
	//上衣
	if (!IsValid(SKMesh_Coats))
	{
		SKMesh_Coats = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Coats"));
		SKMesh_Coats->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Coats);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_COATS, SKMesh_Coats);
	}
	//护腕
	if (!IsValid(SKMesh_Wrist))
	{
		SKMesh_Wrist = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Wrist"));
		SKMesh_Wrist->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Wrist);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_WRIST, SKMesh_Wrist);
	}
	//手套
	if (!IsValid(SKMesh_Gloves))
	{
		SKMesh_Gloves = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Gloves"));
		SKMesh_Gloves->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Gloves);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_GLOVES, SKMesh_Gloves);
	}
	//腰带
	if (!IsValid(SKMesh_Belt))
	{
		SKMesh_Belt = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SKMesh_Belt"));
		SKMesh_Belt->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Belt);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_WAIST, SKMesh_Belt);
	}
	//项链
	if (!IsValid(SKMesh_Necklace))
	{
		SKMesh_Necklace = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SKMesh_Necklace"));
		SKMesh_Necklace->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Necklace);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_NECKLACE, SKMesh_Necklace);
	}
	//戒指左
	if (!IsValid(SKMesh_L_RING))
	{
		SKMesh_L_RING = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SKMesh_L_RING"));
		SKMesh_L_RING->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_L_RING);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_LHAND_RING, SKMesh_L_RING);
	}
	//戒指右
	if (!IsValid(SKMesh_R_RING))
	{
		SKMesh_R_RING = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SKMesh_R_RING"));
		SKMesh_R_RING->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_R_RING);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_RHAND_RING, SKMesh_R_RING);
	}
	//裤子
	if (!IsValid(SKMesh_Pants))
	{
		SKMesh_Pants = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Pants"));
		SKMesh_Pants->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Pants);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_PANTS, SKMesh_Pants);
	}
	//鞋子
	if (!IsValid(SKMesh_Shoes))
	{
		SKMesh_Shoes = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Shoes"));
		SKMesh_Shoes->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Shoes);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_SHOES, SKMesh_Shoes);
	}
	//披风
	if (!IsValid(SKMesh_Cloak))
	{
		SKMesh_Cloak = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("SK_Cloak"));
		SKMesh_Cloak->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(SKMesh_Cloak);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_CLOAK, SKMesh_Cloak); 
	}
	//武器左
	if (!IsValid(STMesh_LHweapon))
	{
		STMesh_LHweapon = NewObject<UStaticMeshComponent>(this, UStaticMeshComponent::StaticClass(), TEXT("LHweapon_Static"));
		STMesh_LHweapon->RegisterComponent();
		SetStaticMeshCptBaseProperty(STMesh_LHweapon);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_LWEAPON, STMesh_LHweapon);
	}
	//武器右
	if (!IsValid(STMesh_RHweapon))
	{
		STMesh_RHweapon = NewObject<UStaticMeshComponent>(this, UStaticMeshComponent::StaticClass(), TEXT("RHweapon_Static"));
		STMesh_RHweapon->RegisterComponent();
		SetStaticMeshCptBaseProperty(STMesh_RHweapon);
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_RWEAPON, STMesh_RHweapon);
	}
	//武器左（带骨架）
	if (!IsValid(STMesh_S_LHweapon))
	{
		STMesh_S_LHweapon = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("LHweapon_Skeletal"));
		STMesh_S_LHweapon->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(STMesh_S_LHweapon, "Socket_Weapon_L");
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON, STMesh_S_LHweapon);
	}
	//武器右（带骨架）
	if (!IsValid(STMesh_S_RHweapon))
	{
		STMesh_S_RHweapon = NewObject<USkeletalMeshComponent>(this, USkeletalMeshComponent::StaticClass(), TEXT("RHweapon_Skeletal"));
		STMesh_S_RHweapon->RegisterComponent();
		SetSkeletalMeshCptBaseProperty(STMesh_S_RHweapon, "Socket_Weapon_R");
		MeshPartComponentDatas.Add(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON, STMesh_S_RHweapon);
	}
	bIsCreateRoleMesh = true;
}

void AGameCharacter::InitBaseComponent()
{
	SCOPE_CYCLE_COUNTER(STAT_InitBaseComponent);
	InitCapsuleComponent();
	InitMovementComponent();
	InitCollisionComponent();
	InitPerformanceComponent();
	InitScene3DUIComponent();
}

void AGameCharacter::InitMovementComponent()
{
	UCharacterMovementComponent* MovementComponent = GetCharacterMovement();
	SetBaseGravityScale(5.0f);
	MovementComponent->MaxAcceleration = 2048.0f;
	MovementComponent->BrakingFrictionFactor = 0.0f;
	MovementComponent->bUseSeparateBrakingFriction = true;
	MovementComponent->bOrientRotationToMovement = true;
	MovementComponent->JumpZVelocity = 2800.0f;
	MovementComponent->BrakingDecelerationFalling = 256.0f;
	MovementComponent->AirControlBoostMultiplier = 10.0f;
	MovementComponent->NavAgentProps.bCanFly = true;
	SetCharacterMoveCacheData();
}

void AGameCharacter::InitCapsuleComponent()
{
	//设置胶囊体的碰撞预设类型
	GetCapsuleComponent()->SetCollisionResponseToChannel(ECC_Visibility, ECollisionResponse::ECR_Block);

	UCapsuleComponent* CharacterCapsuleComponent = GetCapsuleComponent();
	CharacterCapsuleComponent->SetCapsuleRadius(34.0f);
	CharacterCapsuleComponent->SetCapsuleHalfHeight(100.0f);
	GetMesh()->SetRelativeLocationAndRotation(FVector(0.0f, 0.0f, 0.0f), FRotator(0.0f, -90.0f, 0.0f));
	bUseControllerRotationYaw = false;
}

void AGameCharacter::InitScene3DUIComponent()
{
	HeadInfo3DUI = CreateDefaultSubobject<UScene3DUIComponent>(TEXT("HeadInfo3DUI"));
	HeadInfo3DUI->Scale = 1.0f;
	HeadInfo3DUI->SetWorldScale3D(FVector(1.0f, 1.0f, 1.0f));
	HeadInfo3DUI->SetReceivesDecals(false);
}

void AGameCharacter::InitCollisionComponent()
{
	CollisionComponent = CreateDefaultSubobject<UCollisionComponent>(TEXT("CollisionComponent"));
}

void AGameCharacter::InitPerformanceComponent()
{
	if (!PerformanceComponent)
	{
		PerformanceComponent = CreateDefaultSubobject<UPerformanceComponent>(TEXT("PerformanceComponent"));
	}
}

void AGameCharacter::SetMeshMasterPoseComponent()
{
	if (!IsValid(this))
	{
		CS3_Warning(TEXT("-->Null Pointer error:AStoryCharacter::UpdateMasterBoneMap: Actor!"));
		return;
	}
	UMeshComponent *MeshPartCom = *MeshPartComponentDatas.Find(MODEL_PART_TYPE::MODEL_PART_BODYS);
	if (IsValid(MeshPartCom))
	{
		USkeletalMeshComponent* BodyMeshComponent = Cast<USkeletalMeshComponent>(MeshPartCom);
		if (IsValid(BodyMeshComponent))
		{
			for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
			{
				if (!IsValid(Component.Value()))
				{
					continue;
				}
				USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
				if (!IsValid(MeshComponent))
				{
					continue;
				}

				if (Component.Key() == MODEL_PART_TYPE::MODEL_PART_COATS || Component.Key() == MODEL_PART_TYPE::MODEL_PART_ADORN)
				{
					MeshComponent->SetMasterPoseComponent(BodyMeshComponent);
				}
				else
				{
					MeshComponent->SetMasterPoseComponent(nullptr);
				}
			}
		}
	}
}

void AGameCharacter::SynchronousMeshTick()
{
	USkeletalMeshComponent* SKRootMesh_Body = GetMesh();
	if (IsValid(SKRootMesh_Body))
	{
		if (IsValid(SKMesh_Heads))
		{
			SKMesh_Heads->PrimaryComponentTick.AddPrerequisite(SKRootMesh_Body,
				SKRootMesh_Body->PrimaryComponentTick);
		}
		if (IsValid(SKMesh_Hair))
		{
			SKMesh_Hair->PrimaryComponentTick.AddPrerequisite(SKRootMesh_Body,
				SKRootMesh_Body->PrimaryComponentTick);
		}
	}
}

void AGameCharacter::SetSkeletalMeshCptBaseProperty(USkeletalMeshComponent* PartCpt, FString Socket/*=""*/)
{
	if (Socket.IsEmpty())
	{
		PartCpt->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
	}
	else
	{
		PartCpt->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, FSTRING_TO_FNAME(Socket));
	}

	PartCpt->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	PartCpt->bLocalSpaceSimulation = true;
	PartCpt->bReceivesDecals = false;
	PartCpt->bUseAttachParentBound = true;
	//PartCpt->bPerBoneMotionBlur = false;
	PartCpt->bComponentUseFixedSkelBounds = true;
	if (PartCpt == SKMesh_Coats || PartCpt == SKMesh_Adorn)
	{
		PartCpt->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::OnlyTickMontagesWhenNotRendered;
	}
	else
	{
		PartCpt->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::OnlyTickPoseWhenRendered;
	}
	PartCpt->bEnableUpdateRateOptimizations = false; //是否应用动画帧率优化，只要用的角色模型部件这个值就不能优化，否则会导致稍远距离播放动作时头和身体分离
	PartCpt->bUpdateOverlapsOnAnimationFinalize = false;
	PartCpt->bRenderCustomDepth = true;
	PartCpt->CustomDepthStencilValue = 1;
	//PartCpt->LightingChannels.bChannel3 = true;
	PartCpt->bSyncAttachParentLOD = false;
}

void AGameCharacter::SetStaticMeshCptBaseProperty(UStaticMeshComponent* PartCpt, FString Socket /*= ""*/)
{
	if (Socket.IsEmpty())
	{
		PartCpt->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
	}
	else
	{
		PartCpt->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, FSTRING_TO_FNAME(Socket));
	}
	PartCpt->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	PartCpt->bReceivesDecals = false;
	PartCpt->bUseAttachParentBound = true;
	PartCpt->bRenderCustomDepth = true;
	//PartCpt->LightingChannels.bChannel3 = true;
}

float AGameCharacter::GetBoundRadius()
{
	float SphereRadius_Mesh = GetMesh()->Bounds.SphereRadius;
	float SphereRadius__DefaultStatic = IsValid(STMesh_DefaultStatic)? STMesh_DefaultStatic->Bounds.SphereRadius : 0;
	if (SphereRadius_Mesh >= SphereRadius__DefaultStatic) // AGameCharacter中只要有外观的都至少有使用这两个模型的其中一个,所以这里只用这两个模型的包围盒计算
	{
		return SphereRadius_Mesh;
	}
	else
	{
		return SphereRadius__DefaultStatic;
	}
}

void AGameCharacter::OnSignificanceChange()
{
	// 这里可能会调用的比较频繁,最好不要在这处理消耗较大的东西

	auto SetHeadInfo3DUI_MaxWidgetRenderDeltaTime = [=](float Time)
	{
		if (!HeadInfo3DUI) return;
		HeadInfo3DUI->MaxWidgetRenderDeltaTime = Time;
	};

	const UGameDefault& GameDefault = *UGameDefault::StaticClass()->GetDefaultObject<UGameDefault>();

	uint8 SignificanceLOD = (uint8)Significance;
	SetHeadInfo3DUI_MaxWidgetRenderDeltaTime(GameDefault.SignificanceLOD_TickInterval_HeadInfo3DUI[SignificanceLOD]);
	SetGameCharacterTickInterval(GameDefault.SignificanceLOD_TickInterval_GameCharacter[SignificanceLOD]);
	SetActorTickInterval(GameDefault.SignificanceLOD_TickInterval_Actor[SignificanceLOD]);
}

bool AGameCharacter::IsShowEffect(const SignificanceType TargetSignificance)
{
	return (uint8)Significance <= (uint8)TargetSignificance;
}

void AGameCharacter::SetGameCharacterTickInterval(float TickInterval)
{
	GetMovementComponent()->SetComponentTickInterval(TickInterval);
}

void AGameCharacter::PixelsBeyondBounds()
{
	SCOPE_CYCLE_COUNTER(STAT_PixelsBeyondBounds);
	if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager)
	{
		if (IsValid(GetMesh()->SkeletalMesh))
		{
			FString MeshName = UKismetSystemLibrary::GetDisplayName(GetMesh()->SkeletalMesh);
			auto ModelPartTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PART_MODEL);
			const FMODEL_PART_DATA* ModelPartData = ModelPartTable->GetRow<FMODEL_PART_DATA>(MeshName);
			if (ModelPartData)
			{
				GetMesh()->bUseAttachParentBound = ModelPartData->UseAttachParentBound;
				if (!ModelPartData->UseAttachParentBound)
				{
					GetMesh()->SetBoundsScale(50.0f);
				}
			}
		}
		UMeshComponent* DefaultStaticComponent = this->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC);
		UStaticMeshComponent* StaticMeshComponet = Cast<UStaticMeshComponent>(DefaultStaticComponent);
		if (IsValid(StaticMeshComponet->GetStaticMesh()))
		{
			FString MeshName ;
			FMODEL_DATA* ModelData = GetCurModelData().Get();
			if (ModelData != nullptr) 
			{
				for (auto part : ModelData->PartArray)
				{
					if (part.posType == MODEL_PART_TYPE::MODEL_PART_STATIC)
					{
						MeshName = part.PartID;
					}
				}
				auto ModelPartTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PART_MODEL);
				const FMODEL_PART_DATA* ModelPartData = ModelPartTable->GetRow<FMODEL_PART_DATA>(MeshName);
				if (ModelPartData)
				{
					StaticMeshComponet->bUseAttachParentBound = ModelPartData->UseAttachParentBound;
					if (!ModelPartData->UseAttachParentBound)
					{
						StaticMeshComponet->SetBoundsScale(50.0f);
					}
				}
			}
		}
	}
}

void AGameCharacter::SetOpenScene3DUI(const bool & IsOpen)
{
	OpenScene3DUI = IsOpen;
}

void AGameCharacter::ReSetOpenScen3DUI()
{
	OpenScene3DUI = false;
}

KBEngine::Entity* AGameCharacter::GetSelfEntity() const
{
	return nullptr;
}

void AGameCharacter::PlayAction(FName InActionId, float InStartPostion /*= 0.0f*/, 
	const FActionOverDelegate& InActionOverDelegate /*= FActionOverDelegate()*/,
	const FActionBlendOutDelegate& InActionBlendOutDelegate /*= FActionBlendOutDelegate()*/)
{
	SCOPE_CYCLE_COUNTER(STAT_AGameCharacter_PlayAction);
	if (bIsChangeAppearanceling)
	{
		TWeakObjectPtr<AGameCharacter> DelayThisPtr(this);
		if (PlayActionHandle.IsValid())
		{
			OnModelChangeAppearanceOverDelegate.Remove(PlayActionHandle);
			PlayActionHandle.Reset();
		}
		PlayActionHandle = OnModelChangeAppearanceOverDelegate.AddLambda([DelayThisPtr, InActionId,
			InStartPostion, InActionOverDelegate, InActionBlendOutDelegate]()
		{
			if (DelayThisPtr.IsValid())
			{
				AGameCharacter* ThisPtr = DelayThisPtr.Get();
				if (ThisPtr->BaseAnimInstance)
				{
					ThisPtr->BaseAnimInstance->PlayAction(InActionId, InStartPostion, 
						InActionOverDelegate, 0, InActionBlendOutDelegate);
				}
				ThisPtr->OnModelChangeAppearanceOverDelegate.Remove(ThisPtr->PlayActionHandle);
			}
		});
	}
	else
	{
		if (BaseAnimInstance)
		{
			BaseAnimInstance->PlayAction(InActionId, InStartPostion, InActionOverDelegate, 0, InActionBlendOutDelegate);
		}
	}
}

void AGameCharacter::PlayContinuousActions(int32 InContinuousId, TArray<FName>& InActionIds, 
	TArray<float>& InActionStartTimes, 
	const FActionContinuousOverDelegate& InActionOverDelegate /*= FActionOneByOneOverDelegate()*/)
{
	SCOPE_CYCLE_COUNTER(STAT_AGameCharacter_PlayContinuousActions);
	if (bIsChangeAppearanceling)
	{ 
		TWeakObjectPtr<AGameCharacter> DelayThisPtr(this);
		if (PlayContinuousActionsHandle.IsValid())
		{
			OnModelChangeAppearanceOverDelegate.Remove(PlayContinuousActionsHandle);
			PlayContinuousActionsHandle.Reset();
		}
		PlayContinuousActionsHandle = OnModelChangeAppearanceOverDelegate.AddLambda([DelayThisPtr, InContinuousId, InActionIds,
			InActionStartTimes, InActionOverDelegate]()
		{
			if (DelayThisPtr.IsValid())
			{
				AGameCharacter* ThisPtr = DelayThisPtr.Get();
				if (ThisPtr->BaseAnimInstance)
				{
					FACTION_CONTINUOUS ActionContinuous = FACTION_CONTINUOUS();
					ActionContinuous.Id = InContinuousId;
					ActionContinuous.ActionIds = InActionIds;
					ActionContinuous.ActionStartTimes = InActionStartTimes;
					ThisPtr->BaseAnimInstance->PlayContinuousActions(ActionContinuous, InActionOverDelegate);
				}
				ThisPtr->OnModelChangeAppearanceOverDelegate.Remove(ThisPtr->PlayContinuousActionsHandle);
			}
		});
	}
	else
	{
		if (BaseAnimInstance)
		{
			FACTION_CONTINUOUS ActionContinuous = FACTION_CONTINUOUS();
			ActionContinuous.Id = InContinuousId;
			ActionContinuous.ActionIds = InActionIds;
			ActionContinuous.ActionStartTimes = InActionStartTimes;
			BaseAnimInstance->PlayContinuousActions(ActionContinuous, InActionOverDelegate);
		}
	}
}

void AGameCharacter::StopAction()
{
	if (BaseAnimInstance && IsCanPlayAction())
	{
		BaseAnimInstance->StopAction();
	}
}

void AGameCharacter::StopFrontAction()
{
	if (BaseAnimInstance && IsCanPlayAction())
	{
		BaseAnimInstance->StopFrontAction();
	}
}

void AGameCharacter::StopActionById(FName ActionId)
{
	if (BaseAnimInstance)
	{
		BaseAnimInstance->StopActionById(ActionId);
	}
}

void AGameCharacter::StopContinuousAction(int32 InContinuousId)
{
	if (BaseAnimInstance)
	{
		BaseAnimInstance->StopContinuousAction(InContinuousId);
	}
}

void AGameCharacter::SetInitAction()
{
	InitActionId = "None";
}

FName AGameCharacter::GetInitActionId()
{
	return InitActionId;
}

bool AGameCharacter::IsCanPlayAction()
{
	return true;
}

void AGameCharacter::CheckPartHideByAction(FACTION_DATA ActionData)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckPartHideByAction);
	int32 length = (int32)MODEL_PART_TYPE::MODEL_PART_NUM;
	for (int32 i = 0; i < length; i++)
	{
		MODEL_PART_TYPE PartTypeKey = (MODEL_PART_TYPE)i;
		int32 Index = ActionData.HidePartDatas.IndexOfByKey(PartTypeKey);
		if (Index != INDEX_NONE)
		{
			SetMeshPartHiddenInGame(PartTypeKey, true);
		}
		else
		{
			SetMeshPartHiddenInGame(PartTypeKey, false);
		}
	}
}

void AGameCharacter::SetAnimRate(float InRate)
{
	GetMesh()->GlobalAnimRateScale = InRate;
}

void AGameCharacter::SetBaseGravityScale(float InGravityScaleValue)
{
	GravityScaleBase = InGravityScaleValue;
	///重力系数=系数基础值*(系数百分比值+1)+系数固增益值
	float NewGravityScale = GravityScaleBase * (GravityScalePercentage + 1.0f) + GravityScaleAddFixed;
	SetGravityScale(NewGravityScale);
}

void AGameCharacter::SetGravityScale(float InGravityScale)
{
	GetCharacterMovement()->GravityScale = InGravityScale < 0.0f ? 0.0f: InGravityScale;
}

float AGameCharacter::GetGravityScale()
{
	return GetCharacterMovement()->GravityScale;
}

void AGameCharacter::SetBrakingDecelerationFalling(float InBrakingDecelerationFalling)
{
	GetCharacterMovement()->BrakingDecelerationFalling = InBrakingDecelerationFalling;
}

void AGameCharacter::SetMaxWalkSpeed(float InMaxWalkSpeed)
{
	GetCharacterMovement()->MaxWalkSpeed = InMaxWalkSpeed;
}

void AGameCharacter::SetCharacterMoveCacheData()
{
	CharacterMoveCacheData = FCHARACTER_MOVE_CACHE_DATA();
	CharacterMoveCacheData.GravityScale = GetCharacterMovement()->GravityScale;
	CharacterMoveCacheData.MaxAcceleration = GetCharacterMovement()->MaxAcceleration;
	CharacterMoveCacheData.BrakingDecelerationFalling = GetCharacterMovement()->BrakingDecelerationFalling;
	CharacterMoveCacheData.MaxWalkSpeed = GetCharacterMovement()->MaxWalkSpeed;
	CharacterMoveCacheData.JumpZVelocity = GetCharacterMovement()->JumpZVelocity;
}

TSharedPtr<FMODEL_DATA> AGameCharacter::GetCurModelData()
{
	return GetAppearanceComponent()->GetModelData();
}

void AGameCharacter::CheckCreateDynamicPartCpt(FString NewModelId)
{
	if (!bIsCreateRoleMesh)
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		auto ModelTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_MODEL);
		const FMODEL_DATA* ModelData = ModelTable->GetRow<FMODEL_DATA>(NewModelId);
		if (ModelData && ModelData->PartArray.Num() > 1)
		{
			CreateDynamicRoleMesh();
			SetMeshMasterPoseComponent();
		}
	}
}

bool AGameCharacter::IsMoveing()
{
	if (bIsClient)
	{
		return ClientFilterSpeed > 0.0f ? true : false;
	}
	FVector CharacterVelocity = GetVelocity();
	CharacterVelocity.Z = 0;
	return CharacterVelocity.Size() > 0.0f ? true : false;
}

bool AGameCharacter::IsActiveMoveing()
{
	return IsMoveing();
}

float AGameCharacter::GetMoveSpeed()
{
	if (bIsClient)
	{
		return ClientMoveSpeed;
	}
	return 0.0f;
}

bool AGameCharacter::IsLadderMovement()
{
	return false;
}

void AGameCharacter::OnCreateModelOver()
{
	OnCreateApperanceOver();
	OnBroadCreateModelOver.ExecuteIfBound();
	OnModelChangeAppearanceOverDelegate.Broadcast();
}

void AGameCharacter::OnCreateApperanceOver()
{
	SCOPE_CYCLE_COUNTER(STAT_OnCreateApperanceOver);
	OnBPCreateApprearanceOver();
	IsApperanceLoadingOver = true;
	bIsChangeAppearanceling = false;

	isStarScene3D = true;

	///CST-6215	Bug（0级）——Actor异常频闪
	PixelsBeyondBounds();
}

void AGameCharacter::CreatePartMapByServer(TMap<MODEL_PART_TYPE, FString>& InPartDataMap)
{

}

void AGameCharacter::OnChangePartOver()
{

}

void AGameCharacter::CreateAppearance()
{
}

void AGameCharacter::UpdateCapsuleComponent()
{
	SCOPE_CYCLE_COUNTER(STAT_UpdateCapsuleComponent);
	FMODEL_DATA *ModelData = GetCurModelData().Get();
	UCapsuleComponent* CharacterCapsuleComponent = GetCapsuleComponent();
	float CapsuleRadius = CharacterCapsuleComponent->GetUnscaledCapsuleRadius();
	float CapsuleHalfHeight = CharacterCapsuleComponent->GetUnscaledCapsuleHalfHeight();
	if ( !FMath::IsNearlyEqual(CapsuleRadius, ModelData->CapsuleShapeData.CapsuleRadius) ||
		!FMath::IsNearlyEqual(CapsuleHalfHeight, ModelData->CapsuleShapeData.CapsuleHalfHeight) ||
		!FMath::IsNearlyEqual(-100.0f, ModelData->CapsuleShapeData.MeshRelativeLocationZ))
	{
		CharacterCapsuleComponent->SetCapsuleSize(ModelData->CapsuleShapeData.CapsuleRadius,
			ModelData->CapsuleShapeData.CapsuleHalfHeight);
		GetMesh()->SetRelativeLocation(FVector(0.0f, 0.0f, ModelData->CapsuleShapeData.MeshRelativeLocationZ));

		UpdateActorPositionToGround();
	}
}

void AGameCharacter::UpdateActorPositionToGround()
{

}

void AGameCharacter::UpdateActionPosition(FVector NewPosition)
{
	SetActorLocation(NewPosition);
}

void AGameCharacter::UpdateActorDirection(FRotator NewRotation)
{
	SetActorRotation(NewRotation);
}

void AGameCharacter::ChangeBodyLightEffect(FString EffectId)
{
	UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(BodyLightEffectUID);
	//商城预览的优先级高于本身已拥有环身
	FString PlayEffectId = PreviewBodyLightEffectID.IsEmpty() ? EffectId : PreviewBodyLightEffectID;
	if (!PlayEffectId.IsEmpty())
	{
		if (IsValid(BaseAnimInstance) && BaseAnimInstance->IsStandByState())
		{
			BodyLightEffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(PlayEffectId, 0.0f, this, this);
		}
	}
}

bool AGameCharacter::IsBindMeshState()
{
	return bIsBindMeshState;
}

void AGameCharacter::BindMesh(FName AttachMeshID)
{
	SCOPE_CYCLE_COUNTER(STAT_BindMesh);
	if (!UUECS3GameInstance::Instance)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AGameCharacter::BindMesh : Instance!"));
		return;
	}

	bIsBindMeshState = true;

	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_HOLD_PET_MESH_DATA);
	FMESH_BIND_DATA* MeshBindData = const_cast<FMESH_BIND_DATA*>(ConfigTable->GetRow<FMESH_BIND_DATA>(AttachMeshID));
	if (!MeshBindData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AGameCharacter::BindMesh : MeshBindData!"));
		return;
	}

	//判断如果没有骨架，就肯定没有模型了
	if (MeshBindData->SkeletalMeshPath.ToSoftObjectPath().IsValid())
	{
		TArray<FStringAssetReference> LoadPartArray;
		LoadPartArray.Add(MeshBindData->SkeletalMeshPath.ToSoftObjectPath());
		LoadPartArray.Add(MeshBindData->AnimationAssetPath.ToSoftObjectPath());

		TWeakObjectPtr<AGameCharacter> DelayThisPtr(this);
		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, LoadPartArray,
			FStreamableDelegate::CreateLambda([DelayThisPtr, MeshBindData, AttachMeshID]()
		{
			if (DelayThisPtr.IsValid())
			{
				AGameCharacter* ThisPtr = DelayThisPtr.Get();
				FString ComponentName = "SKelMeshCom";
				ComponentName.Append(AttachMeshID.ToString());

				USkeletalMeshComponent* AttachMeshPartComponent = NewObject<USkeletalMeshComponent>(ThisPtr, USkeletalMeshComponent::StaticClass(), FSTRING_TO_FNAME(ComponentName));
				AttachMeshPartComponent->RegisterComponent();
				AttachMeshPartComponent->AttachToComponent(ThisPtr->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, MeshBindData->SocketName);
				ThisPtr->BindMeshComponentDatas.Add(FSTRING_TO_FNAME(ComponentName), AttachMeshPartComponent);

				USkeletalMesh* SkeletalMesh = MeshBindData->SkeletalMeshPath.Get();
				AttachMeshPartComponent->SetReceivesDecals(false);
				AttachMeshPartComponent->SetHiddenInGame(true);
				AttachMeshPartComponent->SetSkeletalMesh(SkeletalMesh);
				AttachMeshPartComponent->SetRelativeLocation(MeshBindData->PartTransform.RelativeLocation);
				AttachMeshPartComponent->SetRelativeRotation(MeshBindData->PartTransform.RelativeRotation);
				AttachMeshPartComponent->SetRelativeScale3D(MeshBindData->PartTransform.RelativeScale3D);
				AttachMeshPartComponent->bUseAttachParentBound = false;

				UAnimationAsset* ActionAnimation = MeshBindData->AnimationAssetPath.Get();
				AttachMeshPartComponent->PlayAnimation(ActionAnimation, true);

				if (MeshBindData->IsCollision)
				{
					AttachMeshPartComponent->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
					AttachMeshPartComponent->SetCollisionResponseToAllChannels(ECR_Ignore);
				}

				TWeakObjectPtr<USkeletalMeshComponent> DelayAttachMeshPartComponentPtr(AttachMeshPartComponent);
				FTimerHandle MeshHideTimerHandle;
				if (IsValid(UUECS3GameInstance::Instance))
				{
					UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(ThisPtr, MeshHideTimerHandle, FTimerDelegate::CreateLambda([DelayAttachMeshPartComponentPtr]()
					{
						if (DelayAttachMeshPartComponentPtr.IsValid())
						{
							DelayAttachMeshPartComponentPtr.Get()->SetHiddenInGame(false);
						}
					}), 0.1f, false);
				}
			}
		}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER, GetActorLocation());
	}

	//添加静态网格
	if (MeshBindData->StaticMeshPath.ToSoftObjectPath().IsValid())
	{
		TWeakObjectPtr<AGameCharacter> DelayThisPtr(this);
		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad
		(this, MeshBindData->StaticMeshPath.ToSoftObjectPath(),
			FStreamableDelegate::CreateLambda([DelayThisPtr, MeshBindData, AttachMeshID]()
		{
			if (DelayThisPtr.IsValid())
			{
				AGameCharacter* ThisPtr = DelayThisPtr.Get();
				FString ComponentName = "StaMeshCom";
				ComponentName.Append(AttachMeshID.ToString());

				UStaticMeshComponent* AttachMeshPartComponent = NewObject<UStaticMeshComponent>(ThisPtr, UStaticMeshComponent::StaticClass(), FSTRING_TO_FNAME(ComponentName));
				AttachMeshPartComponent->RegisterComponent();
				AttachMeshPartComponent->AttachToComponent(ThisPtr->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, MeshBindData->SocketName);
				ThisPtr->BindMeshComponentDatas.Add(FSTRING_TO_FNAME(ComponentName), AttachMeshPartComponent);

				UStaticMesh* StaticMesh = MeshBindData->StaticMeshPath.Get();
				AttachMeshPartComponent->SetStaticMesh(StaticMesh);
				AttachMeshPartComponent->SetRelativeLocation(MeshBindData->PartTransform.RelativeLocation);
				AttachMeshPartComponent->SetRelativeRotation(MeshBindData->PartTransform.RelativeRotation);
				AttachMeshPartComponent->SetRelativeScale3D(MeshBindData->PartTransform.RelativeScale3D);
			}
		}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER, GetActorLocation());
	}

	//添加光效
	if (!MeshBindData->EffectID.IsEmpty())
	{
		int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(MeshBindData->EffectID, 0.0f, this, this);
		BindMeshEffectUID.Add(MeshBindData->RowName, EffectUID);
	}
}

void AGameCharacter::UnBindMesh(FName AttachMeshID)
{
	SCOPE_CYCLE_COUNTER(STAT_UnBindMesh);
	FString ComponentName = "SKelMeshCom";
	ComponentName.Append(AttachMeshID.ToString());

	TArray<UMeshComponent*> MeshArray;
	if (BindMeshComponentDatas.Contains(FSTRING_TO_FNAME(ComponentName)))
	{
		MeshArray.Add(BindMeshComponentDatas[FSTRING_TO_FNAME(ComponentName)]);
	}

	ComponentName = "StaMeshCom";
	ComponentName.Append(AttachMeshID.ToString());

	if (BindMeshComponentDatas.Contains(FSTRING_TO_FNAME(ComponentName)))
	{
		MeshArray.Add(BindMeshComponentDatas[FSTRING_TO_FNAME(ComponentName)]);
	}

	for (auto AttachMeshPartComponent : MeshArray)
	{
		this->RemoveOwnedComponent(AttachMeshPartComponent);

		AttachMeshPartComponent->UnregisterComponent();
		AttachMeshPartComponent = nullptr;
	}
	BindMeshComponentDatas.Remove(AttachMeshID);


	if (BindMeshEffectUID.Contains(AttachMeshID))
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(*BindMeshEffectUID.Find(AttachMeshID));
	}

	bIsBindMeshState = false;
}

void AGameCharacter::SetCurModifyFaceData()
{
	ModifyFaceDatas = UGolbalBPFunctionLibrary::ModifyFaceManager()->GetBoneReference(0);
}

void AGameCharacter::SetMeshPartHiddenInGame(MODEL_PART_TYPE MeshPartType, bool IsHiddenInGame)
{
	UMeshComponent *MeshPartCom = GetPartMeshComponent(MeshPartType);
	if (MeshPartCom)
	{
		MeshPartCom->SetHiddenInGame(IsHiddenInGame);
	}
}

class UMeshComponent* AGameCharacter::GetPartMeshComponent(MODEL_PART_TYPE PartType)
{
	if (!MeshPartComponentDatas.Contains(PartType))
	{
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("AGameCharacter::GetPartMeshComponent, Not Find MeshPart!"), );
		return nullptr;
	}
	UMeshComponent *MeshPartCom = *MeshPartComponentDatas.Find(PartType);
	return MeshPartCom;
}

void AGameCharacter::ChangeModelPart(MODEL_PART_TYPE PartType, FString PartID)
{
	if (IsValid(GetAppearanceComponent()))
	{
		if (PartType == MODEL_PART_TYPE::MODEL_PART_BODYS_LIGHT)
		{
			ChangeBodyLightEffect(PartID);
		}
		else
		{
			GetAppearanceComponent()->ChangePart(PartType, PartID);
		}
	}
}

FName AGameCharacter::GetWeaponSockName(bool IsLeft)
{
	ROLE_PROFESSION_ENUM RoleProfession = (ROLE_PROFESSION_ENUM)ProfessionID;
	if (RoleProfession == ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_SHE_SHOU )
	{
		return IsLeft ? TEXT("Socket_Weapon_Whip_Spine_L") : TEXT("Socket_Weapon_Whip_Spine_R");
	}
	return IsLeft ? TEXT("Socket_Weapon_L") : TEXT("Socket_Weapon_R");
}

bool AGameCharacter::GetApperanceLoadingOver()
{
	return IsApperanceLoadingOver;
}

void AGameCharacter::BP_AdjustHeadUIPositionHuman()
{
	if (!GetMesh()|| !HeadInfo3DUI)
	{
		return;
	}

	static FName HeadSocketName = FName("Socket_Head");
	FVector HeadLocation = GetMesh()->GetSocketLocation(HeadSocketName);

	if (isStarScene3D)
	{
		float finalZ = 0;
		if (BonesNum == 0)
		{
			BonesNum = GetMesh()->GetNumBones();
			SocketHeadPos = HeadLocation;
		}
		// GetBoneName中的索引用1或2骨骼都可以
		finalZ = GetMesh()->GetSocketLocation(GetMesh()->GetBoneName(1)).Z + (GetActorScale().Z * 100.0f);
		if (finalZ > HeadLocation.Z)
		{
			HeadInfo3DUI->SetWorldLocation(FVector(GetCapsuleComponent()->GetComponentLocation().X, GetCapsuleComponent()->GetComponentLocation().Y, finalZ));
		}
		else
		{
			HeadInfo3DUI->SetWorldLocation(HeadLocation);
		}
	}
}

TAsyncLoadPriority AGameCharacter::GetLoadPriority()
{
	AServerCharacter *PlayerCharater = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(PlayerCharater))
	{
		return (int32)UGolbalBPFunctionLibrary::GetActorDistance(PlayerCharater, Cast<AServerCharacter>(this));
	} 
	else
	{
		return 0;
	}
}

void AGameCharacter::SetBaseAnimInstance(UBaseAnimInstance* InAnimInstance)
{
	BaseAnimInstance = InAnimInstance;
}

UBaseAnimInstance* AGameCharacter::GetBaseAnimInstance()
{
	return BaseAnimInstance;
}

void AGameCharacter::SetGameCharacterAlpha(float InAlpha)
{

}

void AGameCharacter::SetGameCharacterFadeOut(float InPeriodOfTime)
{

}

void AGameCharacter::SetGameCharacterDisplay(float InPeriodOfTime)
{

}

CONTROL_COMPILE_OPTIMIZE_END
