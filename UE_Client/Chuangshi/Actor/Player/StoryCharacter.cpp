// Fill out your copyright notice in the Description page of Project Settings.


#include "StoryCharacter.h"
#include "PlayerCharacter.h"
#include "Animation/AnimSequenceBase.h"
#include "Animation/AnimSequence.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Component/AppearanceComponent.h"
#include "Manager/ResourceManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/StoryManager.h"
#include "Manager/ParticleManager.h"
#include "Materials/MaterialInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/GameStatus.h"
#include "Manager/ModifyFaceManager.h"
#include "../Pet/RiderCharacter.h"
#include "../Action/HeadBaseAnimInstance.h"
#include "../GameCharacter.h"
#include "Engine/World.h"
#include "Interface/Role/RoleTeamInterface.h"
#include "Kismet/KismetMathLibrary.h"
#include "AnimSequencerInstance.h"
#include "Animation/AnimTypes.h"
#include "Animation/AnimNotifies/AnimNotifyState.h"
#include "Animation/AnimInstance.h"
#include "Util/CustomEffect/CS3AnimNotify.h"
#include "Util/CustomEffect/CS3AnimNotifyState.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Kismet/BlueprintPathsLibrary.h"
#include "Materials/MaterialInstance.h"
#include "Private/Materials/MaterialInstanceSupport.h"
#include "CS3Base/GameObject.h"
#include "DestructibleComponent.h"
#include "Manager/MotionBlurManager.h"
#include "Util/CustomEffect/Blur/SkeletalMeshBlur.h"
#include "Util/CustomEffect/Blur/PoseableBlur.h"
#include "Components/PoseableMeshComponent.h"
#include "Components/MeshComponent.h"
#include "../../../../../../Source/TransparentPrimitive/Public/TransActorCapture.h"

DECLARE_CYCLE_STAT(TEXT("PlayAnim"), STAT_AStoryCharacter_PlayAnim, STATGROUP_AStoryCharacter);
DECLARE_CYCLE_STAT(TEXT("InitPlayer"), STAT_AStoryCharacter_InitPlayer, STATGROUP_AStoryCharacter);
DECLARE_CYCLE_STAT(TEXT("PlaySeqSetModelByPartsuence"), STAT_SetModelByParts, STATGROUP_AStoryCharacter);
DECLARE_CYCLE_STAT(TEXT("RegisterComponent"), STAT_AStoryCharacter_RegisterComponent, STATGROUP_AStoryCharacter);
DECLARE_CYCLE_STAT(TEXT("SetUpdateAnimationInEditor"), STAT_SetUpdateAnimationInEditor, STATGROUP_AStoryCharacter);


CONTROL_COMPILE_OPTIMIZE_START
void AStoryCharacter::PostInitProperties()
{
	Super::PostInitProperties();
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryCharacter::PostInitProperties()"));
}

#if WITH_EDITOR
void AStoryCharacter::PostEditChangeProperty(FPropertyChangedEvent& PropertyChangedEvent)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryCharacter::PostEditChangeProperty()"));
	Super::PostEditChangeProperty(PropertyChangedEvent);
}
#endif

AStoryCharacter::AStoryCharacter()
	:bRetainCamera(false)
{
	CharacterClassName = TEXT("StoryCharacter");
	PrimaryActorTick.bCanEverTick = true;
	OldAnim = nullptr;
	CreateRoleMesh();
	UpdateMeshPorperty();
	InitBaseComponent();
	ClearAnimData();
}

AStoryCharacter::~AStoryCharacter()
{
	OldAnim = nullptr;
}

void AStoryCharacter::BeginPlay()
{
	Super::BeginPlay();
	WorldPostActorTickHandle = FWorldDelegates::OnWorldPostActorTick.AddUFunction(this, TEXT("OnWorldPostActorTick"));
	PlayBornEffect();

	// 由于在定序器中生成破碎网格物的包围盒会在原点,导致经常看不见,这里强制刷新状态
	GetWorld()->GetTimerManager().SetTimerForNextTick(FTimerDelegate::CreateWeakLambda(this, [=]()
		{
			for (auto c : GetComponents())
			{
				if (UDestructibleComponent * sc = Cast<UDestructibleComponent>(c))
				{
					FVector a = sc->Bounds.Origin;
					FVector b = sc->GetComponentLocation();
					if (a != b)
					{
						sc->RecreatePhysicsState();
					}
				}
			}
		}));
}

void AStoryCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	ClearAnimData();
	ClearModelData();
	ClearWorldPostActorTickHandle();
	Super::EndPlay(EndPlayReason);
}

void AStoryCharacter::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);

	if (!bIsVisibilityPlayerTeamMemb && IsPlayerTeamMemb)
	{
		UGolbalBPFunctionLibrary::SetActorAndCompVisibility(this, UPrimitiveComponent::StaticClass());
		return;
	}
	BP_AdjustHeadUIPositionHuman();
	SetModelAlpha();
	SetModelonLandInEditor();
	SetHeadInfo();
	SetPlayerState(IsShowWeapon, CurState, ProfessionID);
	SetStoneOpacity();
	SetEmissiveColor();
	SetDissolveColor();
	ForceClothNextUpdateTeleport();
	AfterimageEffectEvent();
}

void AStoryCharacter::SetModelonLandInEditor()
{
	///<在非游戏中
	if (!IsValid(UUECS3GameInstance::Instance))
	{
		OnWorldPostActorTick();
	}
}

void AStoryCharacter::ClearWorldPostActorTickHandle()
{
	if (FWorldDelegates::OnWorldPostActorTick.IsBoundToObject(this) && WorldPostActorTickHandle.IsValid())
	{
		FWorldDelegates::OnWorldPostActorTick.Remove(WorldPostActorTickHandle);
	}
}

void AStoryCharacter::OnWorldPostActorTick()
{
	if (IsMoveOnLand && IsValid(this))
	{
		UGolbalBPFunctionLibrary::SetModelonLand(this, GetCapsuleComponent(), ModelScale, 2000.0f);
	}
	if (!bIsVisibilityPlayer)
	{
		SkipAnimNotifies();
	}
}

void AStoryCharacter::UpdateMeshPorperty()
{
	for (TMap<MODEL_PART_TYPE, UMeshComponent *>::TIterator Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
		if (!IsValid(MeshComponent))
		{
			continue;
		}
		if (Component.Key() == MODEL_PART_TYPE::MODEL_PART_HAIRS)
		{
			MeshComponent->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPose;
		}
		else if (Component.Key() == MODEL_PART_TYPE::MODEL_PART_COATS)
		{
			MeshComponent->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
		}
		else
		{
			MeshComponent->bEnableUpdateRateOptimizations = false;
		}
	}
}

void AStoryCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<URoleAppearanceComponent>(TEXT("RoleAppearanceComponent"));
	isStarScene3D = true;
}

void AStoryCharacter::PlayStroyAction(FName ActionId, bool IsBreakAction)
{
	PlayAction(ActionId);
}

void AStoryCharacter::StopStroyAction()
{
	StopAction();
}

void AStoryCharacter::PlayAnimByName(FString AnimName, float PlayRate/* = 1.0f*/, bool bLoop /*= false*/)
{
	const FSTORY_ANIM_EVENT* StoryAnimEventData = GetStoryAnimEventData(AnimName);
	CS3_Warning(TEXT("~~~~~~~AStoryCharacter::PlayAnimByName: AnimName=%s PlayRate=%f bLoop=%d!"), *AnimName, PlayRate, bLoop == true ? 1 : 0);
	if (StoryAnimEventData)
	{
		if ((ProfessionID >= 0) && (ProfessionID < StoryAnimEventData->AnimPath.Num()))
		{
			if (!StoryAnimEventData->AnimPath[ProfessionID].IsNull())
			{
				UObject* AnimObj = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(StoryAnimEventData->AnimPath[ProfessionID].ToSoftObjectPath());
				if (IsValid(AnimObj))
				{
					UAnimSequenceBase* AnimSeq = Cast<UAnimSequenceBase>(AnimObj);
					if (IsValid(AnimSeq))
					{
						PlayAnim(AnimSeq, PlayRate, bLoop);
					}
				}
			}
		}
	}
}

bool AStoryCharacter::ShouldTickIfViewportsOnly() const
{
	return true;
}

void AStoryCharacter::SetActorPart(MODEL_PART_TYPE PartPos, FMODEL_PART_DATA PartData)
{
	AppearanceComponent->UpdatePartMap(PartPos, FNAME_TO_FSTRING(PartData.RowName));
	UObject* PartMesh = UGolbalBPFunctionLibrary::LoadObjectByAssetPath(PartData.ModelPartPath);
	//因为剧情模型加载不是走统一加载流程，是从此函数中让部件逐个的加载，所以头发部件的动画蓝图需要在这里加载，否则后面动画蓝图使用为空
	if (PartData.PartAnimBpPath.ToSoftObjectPath().IsValid())
	{
		TSoftObjectPtr<UAnimInstance> PartAnimBpPath = TSoftObjectPtr<UAnimInstance>(PartData.PartAnimBpPath.ToSoftObjectPath());
		UGolbalBPFunctionLibrary::LoadObjectByAssetPath(PartAnimBpPath);
	}

	if (PartMesh)
	{
		AppearanceComponent->AddActorPart(PartPos, PartData);
	}
	else
	{
		AppearanceComponent->CancelActorPart(PartPos);
	}
}

void AStoryCharacter::PlayAnim(UAnimSequenceBase* AnimSequenceBase, float PlayRate, bool bLoop)
{
	SCOPE_CYCLE_COUNTER(STAT_AStoryCharacter_PlayAnim);
	if (!IsValid(AnimSequenceBase))
	{
		CS3_Warning(TEXT("-->Null Pointer error:AStoryCharacter::PlayAnim : AnimSequenceBase!"));
		return;
	}
	if (GetMesh()->IsPlaying())
	{
		GetMesh()->Stop();
	}

	UAnimSequence* AnimSequence = Cast<UAnimSequence>(AnimSequenceBase);
	if (IsValid(AnimSequence))
	{
		bool bEnableRootMotion = AnimSequence->bEnableRootMotion;
		if (bEnableRootMotion)
		{
			AnimSequence->bEnableRootMotion = false;
			FSTORY_CHARACTER_ANIM temp;
			temp.bDefaultEnableRootMotion = true;
			temp.AnimSequenceBase = AnimSequence;
			CharacterAnims.Add(temp);
		}
	}

	GetMesh()->SetAnimationMode(EAnimationMode::AnimationSingleNode);
	GetMesh()->SetAnimation(AnimSequenceBase);
	GetMesh()->SetPosition(0.0f);
	GetMesh()->SetPlayRate(PlayRate);
	GetMesh()->Play(bLoop);
}

void AStoryCharacter::StopAnim()
{
	if (IsValid(GetMesh()))
	{
		GetMesh()->Stop();
	}
}

void AStoryCharacter::PlayHeadAction(UAnimSequenceBase* AnimSequenceBase,
	float PlayRate /*= 1.0f*/, float StartPosition /*= 0.0f*/, bool bLoop /*= true*/)
{
	UHeadBaseAnimInstance* HeadBaseAnim = Cast<UHeadBaseAnimInstance>(SKMesh_Heads->GetAnimInstance());
	if (HeadBaseAnim)
	{
		if (AnimSequenceBase)
		{
			HeadBaseAnim->CurAnimSquenceBase = AnimSequenceBase;
			HeadBaseAnim->PlayRate = PlayRate;
			HeadBaseAnim->StartPosition = StartPosition;
			HeadBaseAnim->bLoop = bLoop;
		}
		else
		{
			HeadBaseAnim->CurAnimSquenceBase = nullptr;
			HeadBaseAnim->PlayRate = 1.0f;
			HeadBaseAnim->StartPosition = 0.0f;
			HeadBaseAnim->bLoop = true;
		}
	}
}

void AStoryCharacter::StopHeadAction()
{
	UHeadBaseAnimInstance* HeadBaseAnim = Cast<UHeadBaseAnimInstance>(SKMesh_Heads->GetAnimInstance());
	if (HeadBaseAnim)
	{
		HeadBaseAnim->CurAnimSquenceBase = nullptr;
		HeadBaseAnim->PlayRate = 1.0f;
		HeadBaseAnim->StartPosition = 0.0f;
		HeadBaseAnim->bLoop = true;
	}
}

void AStoryCharacter::ClearAnimData()
{
	for (auto& anim : CharacterAnims)
	{
		if (anim.AnimSequenceBase)
		{
			UAnimSequence* AnimSequence = Cast<UAnimSequence>(anim.AnimSequenceBase);
			if (!AnimSequence)
			{
				CS3_Warning(TEXT("-->Null Pointer error:AStoryCharacter::ClearAnimData : AnimSequence!"));
				return;
			}
			AnimSequence->bEnableRootMotion = anim.bDefaultEnableRootMotion;
		}
	}
	CharacterAnims.Reset();
}

void AStoryCharacter::ForceClothNextUpdateTeleport()
{
	if (!IsValid(this))return;

	if (LastTranform.Equals(this->GetActorTransform()))
	{
		bIsConstantTranform = true;
	}
	else
	{
		if (bIsConstantTranform)
		{
			MeshForceClothNextUpdateTeleport();
		}
		LastTranform = this->GetActorTransform();
		bIsConstantTranform = false;
	}
}

void AStoryCharacter::ResetSkeletalMeshPosition()
{
	for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		//清空
		if (IsValid(Component.Value()))
		{
			USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
			if (IsValid(MeshComponent) && IsValid(GetMesh()) && MeshComponent != GetMesh())
			{
				bool IsAttachedToMesh = MeshComponent->IsAttachedTo(GetMesh());
				if (!IsAttachedToMesh)
				{
					MeshComponent->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
				}
				MeshComponent->SetRelativeTransform(FTransform());
			}
			else
			{
				UStaticMeshComponent* StaticMeshComponent = Cast<UStaticMeshComponent>(Component.Value());
				if (IsValid(StaticMeshComponent) && IsValid(GetMesh()))
				{
					bool IsAttachedToMesh = StaticMeshComponent->IsAttachedTo(GetMesh());
					if (!IsAttachedToMesh)
					{
						StaticMeshComponent->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
					}
					StaticMeshComponent->SetRelativeTransform(FTransform());
				}
			}
		}
	}
}

void AStoryCharacter::SetMaterialsParam(FName ParamName, float Value, int32 type, bool OpenStaticMaterial)
{
	for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		if (IsValid(Component.Value()))
		{
			USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
			if (IsValid(MeshComponent))
			{
				if (IsValid(MeshComponent->SkeletalMesh))
				{
					TArray<class UMaterialInterface*> MaterialsList = MeshComponent->GetMaterials();
					for (int i = 0; i < MaterialsList.Num(); i++)
					{
						if (IsValid(MaterialsList[i]))
						{
							UMaterialInstanceDynamic* MaterialInstanceDynamic = MeshComponent->UPrimitiveComponent::CreateDynamicMaterialInstance(i, MaterialsList[i]);

							if (type == 1 && MeshComponent == this->SKMesh_Hair)
							{
								//为解决头发的遮挡关系 让头发透明度多加0.1
								MaterialInstanceDynamic->SetScalarParameterValue(ParamName, Value + 0.1f);
							}
							MaterialInstanceDynamic->SetScalarParameterValue(ParamName, Value);
						}
					}
				}
			}
			else
			{
				if (!OpenStaticMaterial)continue;//根据参数传递值判断跳过静态网格物体的材质操作
				UStaticMeshComponent* StaticMeshComponent = Cast<UStaticMeshComponent>(Component.Value());
				if (IsValid(StaticMeshComponent))
				{
					TArray<class UMaterialInterface*> ST_MaterialsList = StaticMeshComponent->GetMaterials();
					for (int i = 0; i < ST_MaterialsList.Num(); i++)
					{
						if (IsValid(ST_MaterialsList[i]))
						{
							UMaterialInstanceDynamic* StaticMeshMaterialInstanceDynamic = StaticMeshComponent->UPrimitiveComponent::CreateDynamicMaterialInstance(i, ST_MaterialsList[i]);
							StaticMeshMaterialInstanceDynamic->SetScalarParameterValue(ParamName, Value);
						}
					}
				}
			}
		}
	}
}

void AStoryCharacter::SetMaterialsParam(FName ParamName, FLinearColor Value, bool OpenStaticMaterial)
{
	for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		if (IsValid(Component.Value()))
		{
			USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
			if (IsValid(MeshComponent))
			{
				if (IsValid(MeshComponent->SkeletalMesh))
				{
					TArray<class UMaterialInterface*> MaterialsList = MeshComponent->GetMaterials();
					for (int i = 0; i < MaterialsList.Num(); i++)
					{
						if (IsValid(MaterialsList[i]))
						{
							if (!OpenStaticMaterial)
							{
								if (MeshComponent == STMesh_S_LHweapon || MeshComponent == STMesh_S_RHweapon)
								{
									continue;//链刃角色骨骼中的链子为骨架网格物体
								}
							}
							UMaterialInstanceDynamic* MaterialInstanceDynamic = MeshComponent->UPrimitiveComponent::CreateDynamicMaterialInstance(i, MaterialsList[i]);
							UMaterialInstance* ParentMaterial = Cast<UMaterialInstance>(MaterialInstanceDynamic->Parent);
							MaterialInstanceDynamic->SetVectorParameterValue(ParamName, Value);
						}
					}
				}
			}
			else
			{
				if (!OpenStaticMaterial)continue;//根据参数传递值判断跳过静态网格物体的材质操作
				UStaticMeshComponent* StaticMeshComponent = Cast<UStaticMeshComponent>(Component.Value());
				if (IsValid(StaticMeshComponent))
				{
					TArray<class UMaterialInterface*> ST_MaterialsList = StaticMeshComponent->GetMaterials();
					for (int i = 0; i < ST_MaterialsList.Num(); i++)
					{
						if (IsValid(ST_MaterialsList[i]))
						{
							UMaterialInstanceDynamic* StaticMeshMaterialInstanceDynamic = StaticMeshComponent->UPrimitiveComponent::CreateDynamicMaterialInstance(i, ST_MaterialsList[i]);
							StaticMeshMaterialInstanceDynamic->SetVectorParameterValue(ParamName, Value);
						}
					}
				}
			}
		}
	}
}

void AStoryCharacter::SetStaticMaterialsParam(FName ParamName, FLinearColor Value)
{
	for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		if (IsValid(Component.Value()))
		{
			USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
			if (IsValid(MeshComponent))
			{
				if (IsValid(MeshComponent->SkeletalMesh))
				{
					if (MeshComponent == STMesh_S_LHweapon || MeshComponent == STMesh_S_RHweapon)
					{
						TArray<class UMaterialInterface*> MaterialsList = MeshComponent->GetMaterials();
						for (int i = 0; i < MaterialsList.Num(); i++)
						{
							if (IsValid(MaterialsList[i]))
							{
								UMaterialInstanceDynamic* MaterialInstanceDynamic = MeshComponent->UPrimitiveComponent::CreateDynamicMaterialInstance(i, MaterialsList[i]);
								UMaterialInstance* ParentMaterial = Cast<UMaterialInstance>(MaterialInstanceDynamic->Parent);
								MaterialInstanceDynamic->SetVectorParameterValue(ParamName, Value);
							}
						}
					}
				}
			}

			UStaticMeshComponent* StaticMeshComponent = Cast<UStaticMeshComponent>(Component.Value());
			if (IsValid(StaticMeshComponent))
			{
				TArray<class UMaterialInterface*> ST_MaterialsList = StaticMeshComponent->GetMaterials();
				for (int i = 0; i < ST_MaterialsList.Num(); i++)
				{
					if (IsValid(ST_MaterialsList[i]))
					{
						UMaterialInstanceDynamic* StaticMeshMaterialInstanceDynamic = StaticMeshComponent->UPrimitiveComponent::CreateDynamicMaterialInstance(i, ST_MaterialsList[i]);
						StaticMeshMaterialInstanceDynamic->SetVectorParameterValue(ParamName, Value);
					}
				}
			}
		}
	}
}

const FSTORY_ANIM_EVENT* AStoryCharacter::GetStoryAnimEventData(const FString& AnimName)
{
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager)) return nullptr;

	const FSTORY_ANIM_EVENT* StroyAnimEventData =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STORY_ANIM_EVENT)->GetRow<FSTORY_ANIM_EVENT>(AnimName);
	if (!StroyAnimEventData) CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::GetStoryAnimEventData : StroyAnimEventData!"));

	return StroyAnimEventData;
}

void AStoryCharacter::LoadNewMaterial(float model)
{
	FStreamableManager StreamManager;
	for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		if (IsValid(Component.Value()))
		{
			USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
			if (IsValid(MeshComponent))
			{
				if (IsValid(MeshComponent->SkeletalMesh))
				{
					TArray<class UMaterialInterface*> MaterialsList = MeshComponent->GetMaterials();
					for (int i = 0; i < MaterialsList.Num(); i++)
					{
						if (IsValid(MaterialsList[i]))
						{
							UMaterialInstanceDynamic* MaterialInstanceDynamic = MeshComponent->UPrimitiveComponent::CreateDynamicMaterialInstance(i, MaterialsList[i]);
							UMaterialInstance* ParentMaterial = Cast<UMaterialInstance>(MaterialInstanceDynamic->Parent);
							FString ParentPathName = UKismetSystemLibrary::GetPathName(ParentMaterial->Parent);
							FString PathPart, FilePart, ExtensionPart;
							UBlueprintPathsLibrary::Split(ParentPathName, PathPart, FilePart, ExtensionPart);
							if (model == 1)
							{
								FString left, right;
								PathPart.Split("_", &left, &right, ESearchCase::IgnoreCase, ESearchDir::FromEnd);
								PathPart += "/" + left + "." + left;
							}
							else if (model == 2)
							{
								FilePart += "_Tran";
								PathPart += "/" + FilePart + "." + FilePart;
							}
							UObject* MaterialObj = StreamManager.LoadSynchronous(PathPart, false);
							if (MaterialObj)
							{
								ParentMaterial->Parent = Cast<UMaterialInterface>(MaterialObj);
							}
						}
					}
				}
			}
			else
			{
				UStaticMeshComponent* StaticMeshComponent = Cast<UStaticMeshComponent>(Component.Value());
				if (IsValid(StaticMeshComponent))
				{
					TArray<class UMaterialInterface*> ST_MaterialsList = StaticMeshComponent->GetMaterials();
					for (int i = 0; i < ST_MaterialsList.Num(); i++)
					{
						if (IsValid(ST_MaterialsList[i]))
						{
							UMaterialInstanceDynamic* MaterialInstanceDynamic = StaticMeshComponent->UPrimitiveComponent::CreateDynamicMaterialInstance(i, ST_MaterialsList[i]);
							UMaterialInstance* ParentMaterial = Cast<UMaterialInstance>(MaterialInstanceDynamic->Parent);
							FString ParentPathName = UKismetSystemLibrary::GetPathName(ParentMaterial->Parent);
							FString PathPart, FilePart, ExtensionPart;
							UBlueprintPathsLibrary::Split(ParentPathName, PathPart, FilePart, ExtensionPart);
							if (model == 1)
							{
								FString left, right;
								PathPart.Split("_", &left, &right, ESearchCase::IgnoreCase, ESearchDir::FromEnd);
								PathPart += "/" + left + "." + left;
							}
							else if (model == 2)
							{
								FilePart += "_Tran";
								PathPart += "/" + FilePart + "." + FilePart;
							}
							UObject* MaterialObj = StreamManager.LoadSynchronous(PathPart, false);
							if (MaterialObj)
							{
								ParentMaterial->Parent = Cast<UMaterialInterface>(MaterialObj);
							}
						}
					}
				}
			}
		}
	}
}

void AStoryCharacter::SkipAnimNotifies()
{
	USkeletalMeshComponent* SkelMeshComp = GetMesh();
	if (IsValid(SkelMeshComp))
	{
		UAnimInstance* ExistingAnimInstance = SkelMeshComp->GetAnimInstance();
		UAnimSequencerInstance* SequencerInstance = UAnimCustomInstance::BindToSkeletalMeshComponent<UAnimSequencerInstance>(SkelMeshComp);

		TArray<FAnimNotifyEventReference> AnimNotifies;
		TArray<FAnimNotifyEvent> ActiveAnimNotifyStates;
		if (IsValid(ExistingAnimInstance))
		{
			// Tick currently active AnimNotifyState
			ActiveAnimNotifyStates = ExistingAnimInstance->ActiveAnimNotifyState;
			AnimNotifies = ExistingAnimInstance->NotifyQueue.AnimNotifies;
		}
		else if (IsValid(SequencerInstance))
		{
			// Tick currently active AnimNotifyState
			ActiveAnimNotifyStates = SequencerInstance->ActiveAnimNotifyState;
			AnimNotifies = SequencerInstance->NotifyQueue.AnimNotifies;
		}

		for (int32 Index = 0; Index < ActiveAnimNotifyStates.Num(); Index++)
		{
			const FAnimNotifyEvent& AnimNotifyEvent = ActiveAnimNotifyStates[Index];
			//AnimNotifyEvent.NotifyStateClass->NotifyEnd(SkelMeshComp, Cast<UAnimSequenceBase>(AnimNotifyEvent.NotifyStateClass->GetOuter()));

			if (UCS3AnimNotifyState * CS3AnimNotifyState = Cast<UCS3AnimNotifyState>(AnimNotifyEvent.NotifyStateClass))
			{
				CS3AnimNotifyState->StopNotifyEffect(SkelMeshComp, Cast<UAnimSequenceBase>(CS3AnimNotifyState->GetOuter()));
			}
			else
			{
				AnimNotifyEvent.NotifyStateClass->NotifyEnd(SkelMeshComp, Cast<UAnimSequenceBase>(AnimNotifyEvent.NotifyStateClass->GetOuter()));
			}
		}
		if (IsValid(ExistingAnimInstance))
		{
			ExistingAnimInstance->ActiveAnimNotifyState.Reset();
		}
		else if (IsValid(SequencerInstance))
		{
			SequencerInstance->ActiveAnimNotifyState.Reset();
		}

		for (int32 Index = 0; Index < AnimNotifies.Num(); Index++)
		{
			if (const FAnimNotifyEvent * AnimNotifyEvent = AnimNotifies[Index].GetNotify())
			{
				if (UCS3AnimNotify * AnimNotify = Cast<UCS3AnimNotify>(AnimNotifyEvent->Notify))
				{
					AnimNotify->StopNotifyEffect(SkelMeshComp, Cast<UAnimSequenceBase>(AnimNotify->GetOuter()));
				}
			}
		}
	}
}

void AStoryCharacter::AfterimageEffectEvent()
{
	if (bIsAfterimage)
	{
		AfterimageTimer += UGolbalBPFunctionLibrary::GetDeltaTime();
		if (AfterimageTimer>= CreateInterval)
		{
			CreateMontionVlurEvent();
			AfterimageTimer = 0;
		}
 		AfterimageClear = true;
	}
	else
	{
		AfterimageTimer = 100000.0f;
		bIsMontionBlurChange = true;
		if (AfterimageTime != CreateInterval)
		{
			AfterimageTime = CreateInterval;
		}
		if (AfterimageClear)
		{
			if (BlurMeshs.Num() > 0)
			{
				for (auto Blur : BlurMeshs)
				{
					if (IsValid(Blur))
					{
						Blur->Destroy();
					}
				}
			}
			AfterimageClear = false;
			BlurMeshs.Empty();
		}
// 		if (MontionBlurEventHandle.IsValid())
// 		{
// 			GetWorld()->GetTimerManager().ClearTimer(MontionBlurEventHandle);
// 		}
	}
}

void AStoryCharacter::CreateMontionVlurEvent()
{
	if (bIsAfterimageMaterial)
	{
		APoseableBlur* BlurMesh = UMotionBlurManager::GetInstance()->CreateBlurMeshesDirect(GetMesh(), AfterimageLifeTime, nullptr, nullptr, bIsAfterimageSync);
		if (IsValid(BlurMesh))
		{
			BlurMeshs.Add(BlurMesh);
			//ASkeletalMeshBlur* SkeletalBlur = Cast<ASkeletalMeshBlur>(val);
			//float CurDegree = UKismetMathLibrary::Ease(0.0f, 1.0f, 1.0f - AfterimageAphla, EEasingFunc::Linear);
			float CurDegree = UKismetMathLibrary::Ease(0.43f, 0.801f, 1.0f - AfterimageAphla, EEasingFunc::Linear);

			//SkeletalBlur->ParentPoseMesh = GetMesh();
			BlurMesh->SetActorLocation(BlurMesh->GetActorLocation() + AfterimageDeviation);
			for (UMeshComponent* mesh : BlurMesh->m_MesheComps)
			{
				mesh->SetScalarParameterValueOnMaterials(TEXT("CloakOpacity"), CurDegree);
				mesh->SetScalarParameterValueOnMaterials(TEXT("FinalCloakIntensity"), 0.0f);
			}
		}
	}
	else
	{
		TArray<UMaterialInterface*> Materials;
		UMaterial* Material = LoadObject<UMaterial>(NULL, TEXT("/Game/BluePrints/GameCopy/StoryMaterial/AfterimageMaterial.AfterimageMaterial"), NULL, LOAD_None, NULL);
		if (IsValid(Material))
		{
			UMaterialInstanceDynamic* MaterialInstanceDynamic = UMaterialInstanceDynamic::Create(Material, this);
			MaterialInstanceDynamic->SetScalarParameterValue("AfterimageAphla", AfterimageAphla);
			MaterialInstanceDynamic->SetVectorParameterValue("AfterimageColor", AfterimageColor);
			APoseableBlur* BlurMesh = UMotionBlurManager::GetInstance()->CreateBlurMeshesDirect(GetMesh(), AfterimageLifeTime, MaterialInstanceDynamic, nullptr, bIsAfterimageSync);
			if (IsValid(BlurMesh))
			{
				BlurMesh->SetActorLocation(BlurMesh->GetActorLocation() + AfterimageDeviation);
				BlurMeshs.Add(BlurMesh);
			}
		}
	}
}

void AStoryCharacter::SetModleByPartMap(AGameCharacter* GameCharacter)
{
	if (GameCharacter)
	{
		APlayerCharacter* Player = Cast<APlayerCharacter>(GameCharacter);
		ARiderCharacter* Rider = nullptr;
		AGameCharacter* ApperanceCharacter = GameCharacter;
		if (IsValid(Player))
		{
			Rider = Player->GetRiderCharacter();
			if (IsValid(Rider))
			{
				ApperanceCharacter = (AGameCharacter*)Rider;
			}
			this->ProfessionID = Player->ProfessionID;
		}
		if (ApperanceCharacter)
		{
			TSharedPtr<FMODEL_DATA> ModelData = ApperanceCharacter->GetCurModelData();
			if (ModelData.IsValid())
			{
				FString ModelNumber = ApperanceCharacter->GetCurModelData()->RowName.ToString();
				TMap<MODEL_PART_TYPE, FString> NewPartMap = ApperanceCharacter->GetAppearanceComponent()->GetPartMap();
				SetModelByParts(NewPartMap, ModelNumber);
			}
		}
	}
}

void AStoryCharacter::SetPlayerState(bool InIsShowWeapon, ENTITY_STATE InState, int32 InProfession)
{
	IsFightState = InState == ENTITY_STATE::EntityStateFight;
	ProfessionID = InProfession;

	if (!InIsShowWeapon)
	{
		SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_BWEAPON, true);
		SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_LWEAPON, true);
		SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_RWEAPON, true);
		SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON, true);
		SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON, true);
	}
	else
	{
		SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_BWEAPON, false);
		SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_LWEAPON, false);
		SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_RWEAPON, false);
		SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON, false);
		SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON, false);

		GetAppearanceComponent()->UpdateWeaponLocation(IsFightState, ProfessionID);
		UpdateWeaponRightToLeft(IsWeaponRightToLeft, ProfessionID);
	}
}

void AStoryCharacter::SetForceMipStreaming()
{
	if (!IsForceMipStreaming)return;

	for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		if (IsValid(Component.Value()))
		{
			USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
			if (IsValid(MeshComponent))
			{
				MeshComponent->bForceMipStreaming = true;
			}
			else
			{
				UStaticMeshComponent* StaticMeshComponent = Cast<UStaticMeshComponent>(Component.Value());
				if (IsValid(StaticMeshComponent))
				{
					StaticMeshComponent->bForceMipStreaming = true;
				}
			}
		}
	}
}

void AStoryCharacter::RefreshTrackData()
{
	ModelId = (!ModelIdTrack.IsEmpty()) ? FSTRING_TO_FNAME(ModelIdTrack) : ModelId;
	if (!IsPlayer)
	{
		UNameTrack = (!UName.IsNone()) ? FNAME_TO_FSTRING(UName) : UNameTrack;
	}
}

void AStoryCharacter::SetHeadInfo_Implementation()
{

}

void AStoryCharacter::UpdateWeaponRightToLeft(bool IsRightToLeft, int32 InProfession)
{
	GetAppearanceComponent()->UpdateWeaponRightToLeft(IsRightToLeft, ProfessionID);
}

void AStoryCharacter::MeshForceClothNextUpdateTeleport()
{
	if (!IsValid(this) || !IsValid(GetMesh()))return;

	GetMesh()->ForceClothNextUpdateTeleport();
	if (IsValid(SKMesh_Adorn))
	{
		SKMesh_Adorn->ForceClothNextUpdateTeleport();
	}
	if (IsValid(SKMesh_Coats))
	{
		SKMesh_Coats->ForceClothNextUpdateTeleport();
	}
}

void AStoryCharacter::SetDissolveValue(float DissolveDegreeValue)
{
	float num = DissolveDegreeValue * 0.7;
	// 	if (num>=0.64f)
	// 	{
	// 		CurDegree = 1.0f;z	
	// 	}
	this->SetMaterialsParam(TEXT("DissolveDegree"), num);
}

void AStoryCharacter::SetDissolveDirectionValue(float DissolveDirectionValue)
{
	if (DissolveDirectionValue != CurDissolveDirection)
	{
		CurDissolveDirection = DissolveDirectionValue;
		int32 value = DissolveDirectionValue;
		FLinearColor ColorValue;
		switch (value)
		{
		case 1:ColorValue = FLinearColor(0.0f, 0.0f, 1.0f, 0.0f); break;//上
		case 2:ColorValue = FLinearColor(0.0f, 0.0f, 1.0f, 1.0f); break;//下
		case 3:ColorValue = FLinearColor(1.0f, 0.0f, 0.0f, 0.0f); break;//左
		case 4:ColorValue = FLinearColor(1.0f, 0.0f, 0.0f, 1.0f); break;//右 
		default:ColorValue = FLinearColor(0.0f, 0.0f, 0.0f, 0.0f);//整体消融
			break;
		}
		this->SetMaterialsParam(TEXT("DissolveDirection"), ColorValue);
	}
}

FName AStoryCharacter::GetWeaponSockName(bool IsLeft)
{
	ROLE_PROFESSION_ENUM RoleProfession = (ROLE_PROFESSION_ENUM)ProfessionID;
	if (!IsFightState && RoleProfession == ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_SHE_SHOU)
	{
		return IsLeft ? TEXT("Socket_Weapon_Whip_Spine_L") : TEXT("Socket_Weapon_Whip_Spine_R");
	}
	return IsLeft ? TEXT("Socket_Weapon_L") : TEXT("Socket_Weapon_R");
}

void AStoryCharacter::InitProfessionID()
{
	if (!IsPlayer)
	{
		if (ProfessionIDByCinematics < 1 || ProfessionIDByCinematics>4)
		{
			ProfessionID = 1;
		}
		else
		{
			ProfessionID = ProfessionIDByCinematics;
		}
	}
	else
	{
		if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->GameStatus) ||
			UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() != EGameStatus::InWorld)
		{
			ProfessionID = ProfessionIDByCinematics;
		}
	}
}

void AStoryCharacter::InitSpawnModel()
{
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->GameStatus) ||
		UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() != EGameStatus::InWorld)
	{
		InitModelByModelID();
	}
	else
	{
		if (IsPlayer)
		{
			InitPlayer();
		}
		else if (IsPlayerTeamMemb && PlayerTeamMembIndex > -1)
		{
			InitPlayerTeamMemb();
		}
		else
		{
			InitModelByModelID();
		}
	}
	//初始化模型半透明参数
	SetMaterialsParam(TEXT("FinalCloakIntensity"), 0.0f);
}

void AStoryCharacter::SetModelAlpha()
{
	if (CurrOpacity != Opacity)
	{
		CurrOpacity = Opacity;
		ChangeModelAlpha();
		SetHeadAlphaInfo();
	}
}
bool AStoryCharacter::SetHeadAlphaInfo_Implementation()
{
	return true;
}
void AStoryCharacter::InitPlayer()
{
	SCOPE_CYCLE_COUNTER(STAT_AStoryCharacter_InitPlayer);
	AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(PlayerCharacter))
	{
		int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
		int32 Gender = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "gender");
		if ((IsFemalePlayer && Gender == 1) || (!IsFemalePlayer && Gender == 2))
		{
			UName = "";
			UNameTrack = "";
			bIsVisibilityPlayer = false;
			//SetModleByPartMap(PlayerCharacter);
			SkipAnimNotifies();
			SetActorHiddenInGame(true);
		}
		else
		{
			GetMesh()->SetVisibility(false, true);
			ClearModelData();
			SetModleByPartMap(PlayerCharacter);
			GetMesh()->SetVisibility(true, true);
			bIsVisibilityPlayer = true;
			FString PlayerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerId, TEXT("playerName"));
			UName = FSTRING_TO_FNAME(PlayerName);
			UNameTrack = PlayerName;
			UUECS3GameInstance::Instance->ModifyFaceManager->SetBoneRef(this);
			UUECS3GameInstance::Instance->ModifyFaceManager->SetActorFaceData(this, PlayerCharacter->ModifyFaceDatas, PlayerCharacter->FaceStyleDatas);
		}
	}
	else
	{
		InitModelByModelID();
	}
}

void AStoryCharacter::InitPlayerTeamMemb()
{
	bIsVisibilityPlayerTeamMemb = true;;
	URoleTeamInterface* RoleTeamInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.RoleTeamInterface : nullptr;
	if (IsValid(RoleTeamInterface))
	{
		TArray<FTeamMemberData> Members = RoleTeamInterface->Members;
		if (Members.Num() > PlayerTeamMembIndex)
		{
			for (int i = 0; i < Members.Num(); i++)
			{
				FTeamMemberData  PlayerTeamData = Members[i];
				bool IsFindTeamMemb = (i == PlayerTeamMembIndex) ? true : false;
				///<等于玩家自己
				if (PlayerTeamData.EntityID == (UGolbalBPFunctionLibrary::GetPlayerID()) || PlayerTeamData.EntityID == 0 || PlayerTeamData.OnLineState == 0)
				{
					if ((PlayerTeamMembIndex + 1) < Members.Num())
					{
						PlayerTeamData = Members[PlayerTeamMembIndex + 1];
						IsFindTeamMemb = true;
					}
				}
				if (IsFindTeamMemb)
				{
					ProfessionIDByCinematics = PlayerTeamData.Profession;
					ProfessionID = PlayerTeamData.Profession;
					KBEngine::Entity* entity = UGolbalBPFunctionLibrary::FindEntity(PlayerTeamData.EntityID);
					if (entity != nullptr)
					{
						CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------AStoryCharacter::InitPlayerTeamMemb TeamMember-----------%d"), entity->ID());
						APlayerCharacter* PlayerTeamMembCharacter = Cast<APlayerCharacter>(entity->Actor());
						GetMesh()->SetVisibility(false, true);
						ClearModelData();
						if (IsValid(PlayerTeamMembCharacter))
						{
							AppearanceComponent->CopyCharacterFromClientAppearance(PlayerTeamMembCharacter);
						}
						else
						{
							FString modelNumber = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerTeamData.EntityID, TEXT("modelNumber"));
							TMap<MODEL_PART_TYPE, FString> InNewPartMap = GetAppearanceComponent()->GetPartDataMapByModelNumber(modelNumber);
							SetModelByParts(InNewPartMap, modelNumber);
						}
						GetMesh()->SetVisibility(true, true);
						FString PlayerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerTeamData.EntityID, TEXT("playerName"));
						UName = FSTRING_TO_FNAME(PlayerName);
						UNameTrack = PlayerName;
						return;
					}
					break;
				}
			}
		}
	}
	GetMesh()->SetVisibility(false, true);
	bIsVisibilityPlayerTeamMemb = false;
}

void AStoryCharacter::InitModelByModelID()
{
#if WITH_EDITOR
	ResetSkeletalMeshPosition();
#endif 

	if (bUseModelId || IsPlayer)
	{
		ClearModelData();

		TMap<MODEL_PART_TYPE, FString> InNewPartMap;
		if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->GameStatus) || UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() != EGameStatus::InWorld)
		{
			InitSpawnModelByEditor(InNewPartMap);
		}
		else
		{
			InNewPartMap = GetAppearanceComponent()->GetPartDataMapByModelNumber(FNAME_TO_FSTRING(ModelId));
		}

		SetModelByParts(InNewPartMap, FNAME_TO_FSTRING(ModelId));
	}
}

void AStoryCharacter::ClearModelData()
{
	for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		//清空
		if (IsValid(Component.Value()))
		{
			USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
			if (IsValid(MeshComponent))
			{
				if (IsValid(MeshComponent->SkeletalMesh))
				{
					MeshComponent->SetSkeletalMesh(nullptr);
				}
			}
			else
			{
				UStaticMeshComponent* StaticMeshComponent = Cast<UStaticMeshComponent>(Component.Value());
				if (IsValid(StaticMeshComponent))
				{
					StaticMeshComponent->SetStaticMesh(nullptr);
				}
			}
		}
	}
}

void AStoryCharacter::SetModelByParts(TMap<MODEL_PART_TYPE, FString> PartMap, FString ModelNumber)
{
	SCOPE_CYCLE_COUNTER(STAT_SetModelByParts);
	for (TPair<MODEL_PART_TYPE, FString> Part : PartMap)
	{
		if (!Part.Value.IsEmpty())
		{
			const FMODEL_PART_DATA* pPartData;
			if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->GameStatus) || UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() != EGameStatus::InWorld)
			{
				if (!IsValid(PartTable))
				{
					return;
				}
				pPartData = PartTable->GetRow<FMODEL_PART_DATA>(Part.Value);
			}
			else
			{
				pPartData = GetAppearanceComponent()->GetPartDataFromCfg(Part.Value);
			}

			if (pPartData)
			{
				FMODEL_PART_DATA ActorPartData = *pPartData;
				SetActorPart(Part.Key, ActorPartData);
			}
		}
	}
	SetMeshMasterPoseComponent();

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GameStatus) &&
		UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == EGameStatus::InWorld)
	{
		const FMODEL_DATA* ModelData = GetAppearanceComponent()->GetModelDataFromCfg(ModelNumber);
		if (ModelData == nullptr)
		{
			return;
		}
		EffectIds = ModelData->EffectIdArray;
		PixelsBeyondBounds();
	}
}

void AStoryCharacter::GetModelTable()
{
	FStreamableManager StreamManager;
	if (!IsValid(ModelTable))
	{
		UObject* ModelTableObj = StreamManager.LoadSynchronous(FSoftObjectPath(*FString("DataTable'/Game/Miscs/ContentConfig/DT_ModelCfg.DT_ModelCfg'")));
		checkf(IsValid(ModelTableObj), TEXT("加载type配置表失败：\t%s"), *FString("DataTable'/Game/Miscs/ContentConfig/DT_ModelCfg.DT_ModelCfg'"));
		ModelTable = UConfigTable::CreateCfgTable((UDataTable*)ModelTableObj);
	}
	if (!IsValid(PartTable))
	{
		UObject* PartTableObj = StreamManager.LoadSynchronous(FSoftObjectPath(*FString("DataTable'/Game/Miscs/ContentConfig/DT_ModelPartCfg.DT_ModelPartCfg'")));
		checkf(IsValid(PartTableObj), TEXT("加载type配置表失败：\t%s"), *FString("DataTable'/Game/Miscs/ContentConfig/DT_ModelPartCfg.DT_ModelPartCfg'"));
		PartTable = UConfigTable::CreateCfgTable((UDataTable*)PartTableObj);
	}
}

void AStoryCharacter::InitSpawnModelByEditor(TMap<MODEL_PART_TYPE, FString>& InNewPartMap)
{
	GetModelTable();
	if (!IsValid(ModelTable))
	{
		return;
	}
	const FMODEL_DATA* ModelData = ModelTable->GetRow<FMODEL_DATA>(FNAME_TO_FSTRING(ModelId));
	if (ModelData == nullptr)
	{
		return;
	}
	for (FPartItem PratItem : ModelData->PartArray)
	{
		InNewPartMap.Add(PratItem.posType, PratItem.PartID);
	}
}


void AStoryCharacter::SetStoneOpacity()
{
	if (!IsPlayer && StoneOpacity != CurrStoneOpacity)
	{
		CurrStoneOpacity = StoneOpacity;
		this->SetMaterialsParam(TEXT("StonePetrifiedAlpha"), StoneOpacity);
	}
}

void AStoryCharacter::SetEmissiveColor()
{
	if (OldEnableEdge != EnableEdge)
	{
		bIsEnableEdgeChanged = true;
		OldEnableEdge = EnableEdge;
	}
	if (bIsEnableEdgeChanged)
	{
		SetMaterialsParam(TEXT("EdgeGlowColor"), EdgeGlowColor);
		SetMaterialsParam(TEXT("EnableEdge"), EnableEdge);
		SetMaterialsParam(TEXT("EdgeGlowWidth"), EdgeGlowWidth);
	}
}

void AStoryCharacter::SetDissolveColor()
{
	if (bIsDissolve)
	{
		M_DissableSwitch = false;
		this->SetMaterialsParam(TEXT("DissolveEnable"), 1.0f);
		this->SetMaterialsParam(TEXT("DissolveColor"), DissolveColor);
		this->SetMaterialsParam(TEXT("DissolveDegree"), DissolveDegree);
		this->SetMaterialsParam(TEXT("FringeAmount"), FringeAmount);
		SetDissolveDirectionValue(DissolveDirection);
		if (DissolveBoundsSet)
		{
			this->SetMaterialsParam(TEXT("DissolveBoundsSet"), 1.0f);
			this->SetMaterialsParam(TEXT("LocalBoundsMin"), LocalBoundsMin, !DissolveBounds_W);
			this->SetMaterialsParam(TEXT("LocalBoundsSize"), LocalBoundsSize, !DissolveBounds_W);
			if (DissolveBounds_W)
			{
				this->SetStaticMaterialsParam(TEXT("LocalBoundsMin"), LocalBoundsMin_W);
				this->SetStaticMaterialsParam(TEXT("LocalBoundsSize"), LocalBoundsSize_W);
			}
		}

	}
	else
	{
		if (M_DissableSwitch)return;
		M_DissableSwitch = true;;
		this->SetMaterialsParam(TEXT("DissolveEnable"), 0.0f);
	}
}

void AStoryCharacter::PlayBornEffect()
{
	if (EffectIds.Num() > 0)
	{
		if (IsValid(UGolbalBPFunctionLibrary::ParticleManager()))
		{
			for (auto Id : EffectUIds)
			{
				UGolbalBPFunctionLibrary::ParticleManager()->StopEffectByUID(Id);
			}
			EffectUIds.Reset();
			for (auto effectId : EffectIds)
			{
				int32 UId = UGolbalBPFunctionLibrary::ParticleManager()->PlayParticle(effectId, 0.0f, this, this, nullptr);
				EffectUIds.Add(UId);
			}
		}
	}
}

void AStoryCharacter::BindAnimationEvent()
{
	if (IsPlayer && IsValid(UGolbalBPFunctionLibrary::GStoryManager()))
	{
		UGolbalBPFunctionLibrary::GStoryManager()->OnPlayAnimEventDelegate.AddDynamic(this, &AStoryCharacter::PlayAnim);
		UGolbalBPFunctionLibrary::GStoryManager()->OnStopAnimEventDelegate.AddDynamic(this, &AStoryCharacter::StopAnim);
	}
}

void AStoryCharacter::RegisterComponent(bool bIsRegister/* = true*/)
{
	SCOPE_CYCLE_COUNTER(STAT_AStoryCharacter_RegisterComponent);
	for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		if (Component.Key() == MODEL_PART_TYPE::MODEL_PART_BODYS)
		{
			continue;
		}
		//清空
		if (IsValid(Component.Value()))
		{
			USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
			if (IsValid(MeshComponent))
			{
				if (bIsRegister)
				{
					MeshComponent->RegisterComponent();
				}
				else
				{
					MeshComponent->UnregisterComponent();
				}
			}
		}
	}
}

void AStoryCharacter::SetUpdateAnimationInEditor()
{
	SCOPE_CYCLE_COUNTER(STAT_SetUpdateAnimationInEditor);
	if (IsValid(SKMesh_Hair->SkeletalMesh) && IsValid(SKMesh_Hair->SkeletalMesh->Skeleton))
	{
		SKMesh_Hair->bEnablePerPolyCollision = true;
	}
	for (auto Component = MeshPartComponentDatas.CreateIterator(); Component; ++Component)
	{
		if (Component.Key() == MODEL_PART_TYPE::MODEL_PART_BODYS)
		{
			continue;
		}
		//清空
		if (IsValid(Component.Value()))
		{
			USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component.Value());
			if (IsValid(MeshComponent))
			{
				MeshComponent->SetUpdateAnimationInEditor(true);
			}
		}
	}

}
void AStoryCharacter::ChangeModelAlpha()
{
	//CST-9212中提到 觉得0-1不太好理解 故把他取反
//因材质限制所以限定为0.0-2.0的范围才是正确的
	if (CurrOpacity == 1)
	{
		this->SetMaterialsParam(TEXT("CloakOpacity"), 0.0f);
	}
	else
	{
		if (StartNewOpacity)
		{
			if (IsValid(UUECS3GameInstance::Instance))
			{
				ATransActorCapture::SetTransActor(this, CurrOpacity);
			}
			else
			{
				float CurDegree = UKismetMathLibrary::Ease(0.43f, 0.801f, 1.0f - CurrOpacity, EEasingFunc::Linear);
				this->SetMaterialsParam(TEXT("CloakOpacity"), CurDegree, 1);
			}
		}
		else
		{
			float CurDegree = UKismetMathLibrary::Ease(0.43f, 0.801f, 1.0f - CurrOpacity, EEasingFunc::Linear);
			this->SetMaterialsParam(TEXT("CloakOpacity"), CurDegree, 1);
		}
	}
	// 	if (CurModel != 2)
	// 	{
	// 		CurModel = 2;
	// 		LoadNewMaterial(CurModel);
	// 	}
}


CONTROL_COMPILE_OPTIMIZE_END
