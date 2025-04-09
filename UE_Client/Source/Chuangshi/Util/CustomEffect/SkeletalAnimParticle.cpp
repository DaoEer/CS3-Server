// Fill out your copyright notice in the Description page of Project Settings.


#include "SkeletalAnimParticle.h"
#include "Animation/AnimSingleNodeInstance.h"
#include "Actor/ServerCharacter.h"
#include "Manager/ParticleManager.h"
#include "Particles/ParticleSystem.h"
#include "Component/RoleFilterActorComponent.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Actor/Action/BaseAnimInstance.h"
#include "Actor/Particle/EffectEmitter.h"
#include "../CS3Debug.h"
#include "Components/SceneComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Particles/ParticleSystemComponent.h"
#include "Engine/EngineTypes.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Distributions/DistributionFloat.h"
#include "Engine/Texture2D.h"
#include "Engine/SkeletalMesh.h"
#include "Animation/AnimationAsset.h"
#include "Animation/AnimSequenceBase.h"
#include "GameData/CharacterData.h"
#include "Component/AvatarFilterActorComponent.h"
#include "Component/FilterActorComponent.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/CustomEffect/CS3ParitcleAnimNotify.h"
#include "Util/CustomEffect/AnimNotifyState_CS3_TimedParticleEffect.h"
#include "Util/CustomEffect/AnimNotify_CustomSkeletalAnim.h"
//#include "../../CS3Debug.h"


CONTROL_COMPILE_OPTIMIZE_START

// Sets default values
ASkeletalAnimParticle::ASkeletalAnimParticle()
	:Created(false),
	DestroyTime(0.0f),
	RecordDestroyTime(0.0f),
	BaseAnimInstance(nullptr), 
	bLifePause(false)	
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	DefaultSceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	
	SkeletalMeshComp = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("MainSkeletalMesh"));
	SkeletalMeshComp->AttachToComponent(DefaultSceneRoot, FAttachmentTransformRules(EAttachmentRule::KeepRelative, false));
 	
	ParticleComp = CreateDefaultSubobject<UParticleSystemComponent>(TEXT("ParticleSystem"));
 	ParticleComp->AttachToComponent(DefaultSceneRoot, FAttachmentTransformRules(EAttachmentRule::KeepRelative, false));
	UsedFade = false;
	UseDissolve = false;
	TimeCount = 0; 
	bBreakWhenStopNotify = false;
}

bool ASkeletalAnimParticle::ShouldTickIfViewportsOnly() const
{
	return true;
}

void ASkeletalAnimParticle::CheckDestroy()
{
	if (IsValid(SkeletalMeshComp))
	{
		UAnimSingleNodeInstance* SingleNodeInstance = SkeletalMeshComp->GetSingleNodeInstance();
		if (SingleNodeInstance)
		{
			if (SingleNodeInstance->GetCurrentTime() >= SingleNodeInstance->GetLength())
			{
				this->Destroy();
			}
		}
	}
}

void ASkeletalAnimParticle::PostActorCreated()
{
	Super::PostActorCreated();
#ifdef SEQUENCER_ICESWORD_ON
	ISBControler.CheckInSequencer(this);
#endif
}

// Called when the game starts or when spawned
void ASkeletalAnimParticle::BeginPlay()
{
	Super::BeginPlay();
}

void ASkeletalAnimParticle::BeginDestroy()
{
	Super::BeginDestroy();
}

void ASkeletalAnimParticle::FinishDestroy()
{
	Super::FinishDestroy();
}


void ASkeletalAnimParticle::Destroyed()
{
	SkeletalMeshComp->Stop();

	ClearWeaponBindObjData();

	DestroyAnimNotifyRelated(SkeletalMeshComp);
}

// Called every frame
void ASkeletalAnimParticle::Tick( float DeltaTime )
{
	CheckDestroy();

#ifdef SEQUENCER_ICESWORD_ON
	{
		if (ISBControler.Available())
		{
			DeltaTime = ISBControler.CalculateLastTime();
			if (DeltaTime < 0.0f)
			{
				Destroy();
				return;
			}
		}
	}
#endif

	if (bLifePause)
		return;

	Super::Tick( DeltaTime );

	TimeCount += DeltaTime;

// 	RecordDestroyTime += DeltaTime;
// 	if (Created && RecordDestroyTime >= DestroyTime)
// 	{
// 		this->Destroy();
// 		ClearWeaponBindObjData();
// 	}

	UpdateMaterial(TimeCount/* / Lifetime*/);
#ifndef SEQUENCER_ICESWORD_ON
	UpdateAnimNotifyRelated(SkeletalMeshComp);
#endif
}

void ASkeletalAnimParticle::OnActionReadyChangeEvent(FACTION_DATA ActionData)
{
	// 这里本来有清理 所有动作改变的监听事件，但是clear会把其他监听事件一起清理掉。
	// 而event调用之后会自动把自己删掉，所以这里没必要做清理的操作，zxm，2019年8月21日15:57:48
	//当新动作准备改变时，清理当前播放的动作的链条动作
//	CS3_Display(CS3DebugType::CL_Undefined, TEXT("[ASkeletalAnimParticle::CallOnActionBreakEvent ...]"));
// 	if (BaseAnimInstance)
// 	{
// 		BaseAnimInstance->OnActionReadyChange.Clear();
// 	}
	this->Destroy();
	ClearWeaponBindObjData();
}

void ASkeletalAnimParticle::StratFadeInFadeOut(FRawDistributionFloat InputValue)
{
	UsedFade = true;
	AlphaValue = InputValue;
}

void ASkeletalAnimParticle::StratDissolve(FRawDistributionFloat Value, UTexture2D* Texture)
{
	UseDissolve = true;
	DissolveValue = Value;
	DissolveTexture = Texture;
}

bool ASkeletalAnimParticle::InitLianRen(USkeletalMeshComponent* MeshComp, USkeletalMesh* SkeletalMesh,
	UAnimationAsset* Animation, UMaterialInterface* Material, 
	float MeshScale, float AnimStartTime, float AnimRate,
	UParticleSystem* BindParticle, FName SocketName, bool BreakWhenAnimStop)
{
	if (!IsValid(SkeletalMesh) || !IsValid(Animation) )
	{
		CS3_Warning(TEXT("-->Null Pointer error:ASkeletalAnimParticle::Init: SkeletalMesh || Animation!"));
		return false;
	}

	//侦听武器绑定对象
	if (IsValid(MeshComp))
	{
		CurActor = MeshComp->GetOwner();
		if (IsValid(CurActor))
		{
			AServerCharacter* ServerCharacter = Cast<AServerCharacter>(CurActor);
			if (IsValid(ServerCharacter))
			{
				ServerCharacter->OnSkillWeaponBindObj.AddUObject(this, &ASkeletalAnimParticle::OnCheckWeaponBindObj);
			}
		}
		if (BreakWhenAnimStop)// 当需要中断的时候才销毁
		{
			//侦听动作中断时，销毁链条
			BaseAnimInstance = Cast<UBaseAnimInstance>(MeshComp->GetAnimInstance());
			if (IsValid(BaseAnimInstance))
			{
				//CS3_Display(CS3DebugType::CL_Undefined, TEXT("[ASkeletalAnimParticle::InitLianRen ...]"));
				BaseAnimInstance->OnActionReadyChange.AddUObject(this, &ASkeletalAnimParticle::OnActionReadyChangeEvent);
			}
		}
	}
	bBreakWhenAnimStop = BreakWhenAnimStop;
	SkeletalMeshComp->SetRelativeScale3D(FVector::OneVector * MeshScale);
	//SkeletalMeshComp->SetWorldScale3D(FVector::OneVector * MeshScale);
	SkeletalMeshComp->SetSkeletalMesh(SkeletalMesh); 
	SkeletalMeshComp->PlayAnimation(Animation, false);
	SkeletalMeshComp->SetPosition(AnimStartTime);
	SkeletalMeshComp->SetPlayRate(AnimRate);

	UAnimInstance* ExistingAnimInstance = SkeletalMeshComp->GetAnimInstance();

	//UAnimBaseAnimInstanceance* BaseAnimInstanceance = UAnimCustomInstance::BindToSkeletalMeshComponent<UAnimBaseAnimInstanceance>(SkeletalMeshComp);
	SkeletalMeshComp->SetUpdateAnimationInEditor(true);
// 	if (SkeletalMeshComp->PoseTickedThisFrame() /*|| (BaseAnimInstanceance && BaseAnimInstanceance != ExistingAnimInstance)*/)
// 	{
// 		SkeletalMeshComp->TickAnimation(0.f, false);
// 
// 		SkeletalMeshComp->RefreshBoneTransforms();
// 		SkeletalMeshComp->RefreshSlaveComponents();
// 		SkeletalMeshComp->UpdateComponentToWorld();
// 		SkeletalMeshComp->FinalizeBoneTransform();
// 		SkeletalMeshComp->MarkRenderTransformDirty();
// 		SkeletalMeshComp->MarkRenderDynamicDataDirty();
// 	}

	if (IsValid(Material))
	{
		int MaterialNum = SkeletalMeshComp->GetNumMaterials();
		for (int i = 0; i < MaterialNum; i++)
		{
			SkeletalMeshComp->SetMaterial(i, Material);
		}
	}
	Lifetime = (SkeletalMeshComp->GetSingleNodeInstance()->GetLength() - AnimStartTime) / AnimRate;
	DestroyTime = Lifetime;
	Created = true;
		
	if (BindParticle)
	{
		ParticleComp->SetTemplate(BindParticle);
		ParticleComp->AttachToComponent(SkeletalMeshComp, FAttachmentTransformRules(EAttachmentRule::KeepRelative, false), SocketName);
	}
	//如果放在第一帧，需要这里检测
	OnCheckWeaponBindObj();
	//如果是第一帧，手动调用一次更新相关的骨骼模型UpdateAnimNotifyRelated
#ifndef SEQUENCER_ICESWORD_ON
	UpdateAnimNotifyRelated(SkeletalMeshComp);
#endif
	return true;
}

bool ASkeletalAnimParticle::InitOther(USkeletalMeshComponent* MeshComp, USkeletalMesh* SkeletalMesh, 
	UAnimationAsset* Animation, FVector Scale3DOffset, float AnimRate, FName SocketName, 
	bool IsLoop, bool IsAutoDesotry)
{
	UAnimSequenceBase * AnimSequenceBase = Cast<UAnimSequenceBase>(Animation);
	if (!IsValid(SkeletalMesh) || !IsValid(AnimSequenceBase))
	{
		CS3_Warning(TEXT("-->Null Pointer error:ASkeletalAnimParticle::Init: SkeletalMesh || Animation!"));
		return false;
	}

	CurActor = MeshComp->GetOwner();
	SkeletalMeshComp->SetRelativeScale3D(Scale3DOffset);
	SkeletalMeshComp->SetSkeletalMesh(SkeletalMesh);
	SkeletalMeshComp->PlayAnimation(AnimSequenceBase, IsLoop);
	SkeletalMeshComp->SetPlayRate(AnimRate); 
	float PlayRate = SkeletalMeshComp->GetPlayRate() * AnimSequenceBase->RateScale;
	if (IsAutoDesotry)///通知状态（AnimNotifyState_AttchSkeletaAnim）是结束销毁，只有通知是绑定动作播完销毁
	{ 
		float AnimLength = AnimSequenceBase->GetPlayLength();
		DestroyTime = AnimLength / PlayRate;
		Created = true;
	}
	return true;
}

void ASkeletalAnimParticle::OnCheckWeaponBindObj()
{
	if (!IsValid(CurActor))
		return;
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(CurActor);
	if (!IsValid(ServerCharacter))
	{
		//CS3_Warning(TEXT("-->Null Pointer error:ASkeletalAnimParticle::OnCheckWeaponBindObj: ServerCharacter!"));
		return;
	}
	for (FPART_SLOT_BIND_OBJ_DATA& ObjData : ServerCharacter->WeaponBindObjData)
	{
		if (ObjData.bBind)
		{
			continue;
		}
		if (ObjData.BindObjType == PART_SLOT_BIND_OBJ_ENUM::PART_SLOT_BIND_OBJ_ACTOR)
		{
			WeaponBindActor(ObjData);
		}
		else if (ObjData.BindObjType == PART_SLOT_BIND_OBJ_ENUM::PART_SLOT_BIND_OBJ_PARTICLE)
		{
			WeaponBindParticle(ObjData);
		}
	}
}

void ASkeletalAnimParticle::WeaponBindActor(FPART_SLOT_BIND_OBJ_DATA& InObjData)
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		return;
	}
	KBEngine::Entity* MainEntity = UUECS3GameInstance::pKBEApp->FindEntity(InObjData.MainEntityID);
	KBEngine::Entity* ByBindEntity = UUECS3GameInstance::pKBEApp->FindEntity(InObjData.ByBindEntityID);
	if (MainEntity && ByBindEntity && IsValid(MainEntity->Actor()) && IsValid(ByBindEntity->Actor()))
	{
		AServerCharacter* ByBindActor = Cast<AServerCharacter>(ByBindEntity->Actor());
		//关闭碰撞
		ByBindActor->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		ByBindActor->GetMesh()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		//绑定到链条上的插槽
		const FAttachmentTransformRules AttachmentRules = FAttachmentTransformRules::SnapToTargetNotIncludingScale;
		ByBindActor->AttachToComponent(SkeletalMeshComp, AttachmentRules, InObjData.SoketName);
		FRotator Rotator(InObjData.RelativeDirection.Y, InObjData.RelativeDirection.Z, InObjData.RelativeDirection.X);
		//设置相对偏移量及相对方向
		ByBindActor->SetActorRelativeLocation(InObjData.RelativePosition);
		ByBindActor->SetActorRelativeRotation(Rotator);

		if (ByBindEntity->ClassName() == "Role")
		{
			//关闭重力
			ByBindActor->Controller->StopMovement();
			ByBindActor->GetCharacterMovement()->Velocity = FVector();
			ByBindActor->GetCharacterMovement()->SetMovementMode(EMovementMode::MOVE_Flying);
			ByBindActor->SetBaseGravityScale(0.0f);
			
			//关闭服务器位置同步
			UFilterActorComponent* MFilterComponent = ByBindActor->GetFilterComponent();
			URoleFilterActorComponent* FilterComp = Cast<URoleFilterActorComponent>(ByBindActor->GetFilterComponent());
			if (IsValid(FilterComp))
			{
				//FilterComp->IsIgnoreServerPos = true;
			}
				
		}
		else
		{
			//关闭服务器位置同步
			UFilterActorComponent* MFilterComponent = ByBindActor->GetFilterComponent();
			UAvatarFilterActorComponent* FilterComp = Cast<UAvatarFilterActorComponent>(MFilterComponent);
			if (IsValid(FilterComp))
			{
				//FilterComp->IsIgnoreServerPosValue = true;
			}
		}
	}
}

void ASkeletalAnimParticle::WeaponBindParticle(FPART_SLOT_BIND_OBJ_DATA& InObjData)
{
	UParticleManager *ParticleManager = UUECS3GameInstance::Instance->ParticleManager;
	ParticleManager->PlayParticle(InObjData.ParticleId, 0.0f, this, this,
		FEffectCreate::CreateLambda([=](int32 UID)
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(UID);
	}));
}

void ASkeletalAnimParticle::ClearWeaponBindObjData()
{
	if (!IsValid(CurActor))
		return;
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(CurActor);
	if (IsValid(ServerCharacter))
	{
		ServerCharacter->OnSkillWeaponBindObj.Clear();
		ServerCharacter->RemoveAllPartSlotBindObj();
	}
}

void ASkeletalAnimParticle::UpdateMaterial(float TimeProgress)
{
	float FadeV = 1.0;
	float DissolveV = 1.0;
	if ((UsedFade || UseDissolve) && IsValid(SkeletalMeshComp))
	{
		if (UsedFade)
			FadeV = AlphaValue.GetValue(TimeProgress);
		if (UseDissolve)
			DissolveV = DissolveValue.GetValue(TimeProgress);

		int MaterialNum = SkeletalMeshComp->GetNumMaterials();
		for (int i = 0; i < MaterialNum; i++)
		{
			auto material = SkeletalMeshComp->GetMaterial(i);
			if (IsValid(material))
			{
				auto DM = Cast<UMaterialInstanceDynamic>(material);
				if (!IsValid(DM))
				{
					DM = UMaterialInstanceDynamic::Create(material, GetWorld());
					check(DM);
					SkeletalMeshComp->SetMaterial(i, DM);
					DM->SetTextureParameterValue(FName(L"溶解贴图M"), DissolveTexture);
				}
				if (UsedFade)
					DM->SetScalarParameterValue(FName(L"不透明度"), FadeV);
				if (UseDissolve)
				{
					DM->SetScalarParameterValue(FName(L"溶解度"), DissolveV);
				}

			}
		}
	}
}

void ASkeletalAnimParticle::UpdateAnimNotifyRelated(USkeletalMeshComponent * SkelMeshComp)
{
	UAnimInstance* CurAnimInstance = SkelMeshComp->GetAnimInstance();
	if (CurAnimInstance)
	{
		TArray<FAnimNotifyEventReference> AnimNotifies = CurAnimInstance->NotifyQueue.AnimNotifies;
		TArray<FAnimNotifyEvent> ActiveAnimNotifyState = CurAnimInstance->ActiveAnimNotifyState;
		for (int32 Index = 0; Index < AnimNotifies.Num(); Index++)
		{
			if (const FAnimNotifyEvent* AnimNotifyEvent = AnimNotifies[Index].GetNotify())
			{			
				if (UAnimNotifyState_CS3_TimedParticleEffect* ParAnimNotifyState = Cast<UAnimNotifyState_CS3_TimedParticleEffect>(AnimNotifyEvent->NotifyStateClass))
				{
					if (ParAnimNotifyState->PSC)
					{
						ParAnimNotifyState->PSC->CustomTimeDilation = SkelMeshComp->GetSingleNodeInstance()->GetPlayRate();
						ChildAnimNotifyParticle.AddUnique(ParAnimNotifyState->PSC);
					}
				}
				if (UCS3ParitcleAnimNotify* ParAnimNotify = Cast<UCS3ParitcleAnimNotify>(AnimNotifyEvent->Notify))
				{
					if (ParAnimNotify->PSC)
					{
						ParAnimNotify->PSC->CustomTimeDilation = SkelMeshComp->GetSingleNodeInstance()->GetPlayRate();
						ChildAnimNotifyParticle.AddUnique(ParAnimNotify->PSC);
					}
				}
				if (UAnimNotify_CustomSkeletalAnim* SkMeshNotify = Cast<UAnimNotify_CustomSkeletalAnim>(AnimNotifyEvent->Notify))
				{
					if (SkMeshNotify->SkelParticle)
					{
						ChildAnimNotifySkMesh.AddUnique(SkMeshNotify->SkelParticle);

						CS3_Display(CS3DebugType::CL_Undefined, TEXT("=======SkMeshNotify->SkelParticle=%s"), *(SkMeshNotify->SkelParticle->GetName()));
						//CS3_Warning(TEXT("======SkMeshNotify->SkelParticle=%s"), *(SkMeshNotify->SkelParticle->GetName()));
						//第二层骨骼动画通知的第一帧如果有通知，加入到处理数组
						if (SkMeshNotify->SkelParticle->SkeletalMeshComp && SkMeshNotify->SkelParticle->SkeletalMeshComp->GetSingleNodeInstance())
						{
							TArray<FAnimNotifyEventReference> SkMeshAnimNotifies = SkMeshNotify->SkelParticle->SkeletalMeshComp->GetSingleNodeInstance()->NotifyQueue.AnimNotifies;
							for (int32 NtyIndex = 0; NtyIndex < SkMeshAnimNotifies.Num(); NtyIndex++)
							{
								if (const FAnimNotifyEvent* SkMeshAnimNotifyEvent = SkMeshAnimNotifies[NtyIndex].GetNotify())
								{
									if (UAnimNotifyState_CS3_TimedParticleEffect* SkMeshParAnimNotifyState = Cast<UAnimNotifyState_CS3_TimedParticleEffect>(SkMeshAnimNotifyEvent->NotifyStateClass))
									{
										if (SkMeshParAnimNotifyState->PSC)
										{
											ChildAnimNotifyParticle.AddUnique(SkMeshParAnimNotifyState->PSC);
										}
									}
									if (UCS3ParitcleAnimNotify* SkMeshParAnimNotify = Cast<UCS3ParitcleAnimNotify>(SkMeshAnimNotifyEvent->Notify))
									{
										if (SkMeshParAnimNotify->PSC)
										{
											ChildAnimNotifyParticle.AddUnique(SkMeshParAnimNotify->PSC);
										}
									}
									if (UAnimNotify_CustomSkeletalAnim* SkMeshNotify_2 = Cast<UAnimNotify_CustomSkeletalAnim>(SkMeshAnimNotifyEvent->Notify))
									{
										if (SkMeshNotify_2->SkelParticle)
										{
	// 										USkeletalMeshComponent* CurSkMeshComp = SkMeshNotify_2->SkelParticle->SkeletalMeshComp;
	// 										if (CurSkMeshComp)
	// 										{
	// 											CurSkMeshComp->GetSingleNodeInstance()->SetPlayRate(SeqRate);
	// 										}
											ChildAnimNotifySkMesh.AddUnique(SkMeshNotify_2->SkelParticle);
											//GEngine->AddOnScreenDebugMessage(1, 10.f, FColor::Red, SkMeshNotify_2->SkelParticle->GetName());
											CS3_Display(CS3DebugType::CL_Undefined, TEXT("===SkMeshNotify_2->SkelParticle=%s"), *(SkMeshNotify_2->SkelParticle->GetName()));
										}
									}
								}
							}
						}
						

					}
				}
			}
		}
// 		for (int32 Idx = ActiveAnimNotifyState.Num() - 1; Idx >= 0; --Idx)
// 		{
// 			FAnimNotifyEvent& AnimNotifyState = ActiveAnimNotifyState[Idx];
// 			if (AnimNotifyState.NotifyStateClass)
// 			{
// 				if (UAnimNotifyState_CS3_TimedParticleEffect* ParAnimNotifyState = Cast<UAnimNotifyState_CS3_TimedParticleEffect>(AnimNotifyState.NotifyStateClass))
// 				{
// 					if (ParAnimNotifyState->PSC)
// 					{
// 						ParAnimNotifyState->PSC->CustomTimeDilation = SkeletalMeshComp->GetSingleNodeInstance()->GetPlayRate();
// 					}
// 				}
// 			}
// 			if (UCS3ParitcleAnimNotify* ParAnimNotify = Cast<UCS3ParitcleAnimNotify>(AnimNotifyState.Notify))
// 			{
// 				if (ParAnimNotify->PSC)
// 				{
// 					ParAnimNotify->PSC->CustomTimeDilation = SkeletalMeshComp->GetSingleNodeInstance()->GetPlayRate();
// 				}
// 			}
// 			if (UAnimNotify_CustomSkeletalAnim* SkMeshNotify = Cast<UAnimNotify_CustomSkeletalAnim>(AnimNotifyState.Notify))
// 			{
// 				if (SkMeshNotify->SkelParticle)
// 				{
// 					USkeletalMeshComponent* CurSkMeshComp = SkMeshNotify->SkelParticle->SkeletalMeshComp;
// 					if (CurSkMeshComp)
// 					{
// 						CurSkMeshComp->GetSingleNodeInstance()->SetPlayRate(SkeletalMeshComp->GetSingleNodeInstance()->GetPlayRate());
// 					}
// 					ChildAnimNotifySkMesh.AddUnique(SkMeshNotify->SkelParticle);
// 				}
// 			}
// 			
// 		}
		if (ChildAnimNotifyParticle.Num() != 0)
		{
			for (auto It = ChildAnimNotifyParticle.CreateIterator() + ChildAnimNotifyParticle.Num() - 1; It; It--)
			{
				if (IsValid(*It))
				{
					if ((*It)->bIsActive)
					{
						(*It)->CustomTimeDilation = SkeletalMeshComp->GetSingleNodeInstance()->GetPlayRate();
					}
					else {
						It.RemoveCurrent();
					}
				}
			}
		}
		if (ChildAnimNotifySkMesh.Num() != 0)
		{
			for (auto It = ChildAnimNotifySkMesh.CreateIterator() + ChildAnimNotifySkMesh.Num() - 1; It; It--)
			{
				if (IsValid(*It))
				{
					if ((*It)->SkeletalMeshComp)
					{
						UAnimSingleNodeInstance* SkMeshAnimInstance = (*It)->SkeletalMeshComp->GetSingleNodeInstance();
						if (SkMeshAnimInstance->GetCurrentTime() >= SkMeshAnimInstance->GetLength())
						{
							It.RemoveCurrent();
						}
						else
						{
							SkMeshAnimInstance->SetPlayRate(SkeletalMeshComp->GetSingleNodeInstance()->GetPlayRate());
						}
					}
				}
			}
		}
	}
}

void ASkeletalAnimParticle::DestroyAnimNotifyRelated(USkeletalMeshComponent* SkelMeshComp)
{
	if (IsValid(SkelMeshComp))
	{
		UAnimInstance* CurAnimInstance = SkelMeshComp->GetAnimInstance();
		if (CurAnimInstance)
		{
			for (int32 i = ChildAnimNotifyParticle.Num() - 1; i >= 0; i--)
			{
				UParticleSystemComponent* comp = ChildAnimNotifyParticle[i];
				if (IsValid(comp) && (comp->bIsActive)|| bBreakWhenStopNotify)
				{
					comp->DestroyComponent();
					ChildAnimNotifyParticle.RemoveAt(i);
				}
			}
			for (int32 i = ChildAnimNotifySkMesh.Num() - 1; i >= 0; i--)
			{
				ASkeletalAnimParticle* par = ChildAnimNotifySkMesh[i];
				if (IsValid(par) &&( par->SkeletalMeshComp && par->bBreakWhenAnimStop)|| bBreakWhenStopNotify)
				{
					par->Destroy();
					ChildAnimNotifySkMesh.RemoveAt(i);
				}
			}
			//ChildAnimNotifyParticle.Empty();
			//ChildAnimNotifySkMesh.Empty();
		}

	}
}

void ASkeletalAnimParticle::DestroyChilds()
{
	TArray<AActor*> AttachedActors;
	this->GetAttachedActors(AttachedActors);

	for (AActor* AttachedActor : AttachedActors)
	{
		AttachedActor->Destroy();
	}
}

void ASkeletalAnimParticle::SetPlayRate(float Rate)
{
	SkeletalMeshComp->SetPlayRate(Rate);
}

void ASkeletalAnimParticle::SetLifeTime(float lifetime)
{
	DestroyTime = lifetime;
}

void ASkeletalAnimParticle::SetAnimPostion(float InPos)
{
	bLifePause = true;
	SkeletalMeshComp->Stop();
	SkeletalMeshComp->SetPosition(InPos, true);
	SkeletalMeshComp->CompleteParallelAnimationEvaluation(true);
}

void ASkeletalAnimParticle::SetPause(bool pause)
{
	bLifePause = true;
}

void ASkeletalAnimParticle::StopNotifyEffect()
{
	bBreakWhenStopNotify = true;
	this->Destroy();
}


CONTROL_COMPILE_OPTIMIZE_END
