// Fill out your copyright notice in the Description page of Project Settings.


#include "Actor/Particle/EffectEmitter.h"
// UE4
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"
#include "Components/SplineComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/AudioComponent.h"
#include "Particles/ParticleSystemComponent.h"
#include "Particles/ParticleModule.h"
#include "Particles/ParticleLODLevel.h"
#include "Particles/ParticleSystem.h"
#include "Particles/ParticleEmitter.h"
// 数据类型
#include "GameData/BaseSplineAsset.h"
// CS3类型
#include "CS3Base/CS3Entity.h"
#include "Actor/GameCharacter.h"
#include "Actor/ServerCharacter.h"
#include "Actor/Particle/ParticleModuleEx/ParticleModuleColorOverLifeEX.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Pet/PetCharacter.h"
#include "Manager/ParticleManager.h"
#include "Manager/AudioManager.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Component/PerformanceComponent.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Interface/SkillInterface.h"
#include "CS3Base/GameObject.h"

#if WITH_EDITOR
#include "Actor/Tool/SpawnBase.h"
#endif //WITH_EDITOR
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "GameFramework/WorldSettings.h"
#include "GameData/EffectEmitterData.h"
#include "Manager/MotionBlurManager.h"
#include "Util/CustomEffect/Blur/MeshBlur.h"
#include "Util/CustomEffect/Blur/PoseableBlur.h"
#include "DelegateSignatureImpl.inl"

// 光效显示的距离，10米和40米
#define NEARDIS 1000.f
#define FARDIS  4000.f

DECLARE_CYCLE_STAT(TEXT("InitBeforeBeginPlay"), STAT_InitBeforeBeginPlay, STATGROUP_AEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("PrepareData"), STAT_PrepareData, STATGROUP_AEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("ClearData"), STAT_ClearData, STATGROUP_AEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("ClearDataAndAddToBufferPool"), STAT_ClearDataAndAddToBufferPool, STATGROUP_AEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("StartPlay"), STAT_StartPlay, STATGROUP_AEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("Stop"), STAT_Stop, STATGROUP_AEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("OnEmitterCollisionBegin"), STAT_OnEmitterCollisionBegin, STATGROUP_AEffectEmitter);
DECLARE_CYCLE_STAT(TEXT("OnEmitterCollisionEnd"), STAT_OnEmitterCollisionEnd, STATGROUP_AEffectEmitter);

CONTROL_COMPILE_OPTIMIZE_START

AEffectEmitter::AEffectEmitter()
{
	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);
	SceneTransformComp= CreateDefaultSubobject<USceneComponent>(TEXT("SceneTransform"));
	SceneTransformComp->AttachToComponent(Root, FAttachmentTransformRules::KeepRelativeTransform);
	GetParticleSystemComponent()->AttachToComponent(SceneTransformComp, FAttachmentTransformRules::KeepRelativeTransform);
}

///Spawn之后BeginPlay之前初始化
void AEffectEmitter::InitBeforeBeginPlay(FString InEffectID, int32 TempUID, AActor* TempFirstTarget, AActor* TempSecondTarget, float TempEffectSendAngle, const FEFFECT_EMITTER_DATA* TempEffectEmitterData, void* TempOnEffectCreate)
{
	SCOPE_CYCLE_COUNTER(STAT_InitBeforeBeginPlay);
	// 根据粒子管理器的数据初始化粒子数据
	this->ID = InEffectID;							//当前的粒子ID
	this->UID = TempUID;								//当前粒子的UID	
	this->EffectSendAngle = TempEffectSendAngle;		//服务器传来的光效偏移，对路径生效
	this->EffectEmitterData = TempEffectEmitterData;
	this->EmitterCollisionProxyId = -1;

	// 根据配置调整光效的目标		
	this->FirstTarget = TempEffectEmitterData->EffectData.BaseEffectData.bIsSwap ? TempSecondTarget : TempFirstTarget;
	this->SecondTarget = TempEffectEmitterData->EffectData.BaseEffectData.bIsSwap ? TempFirstTarget : TempSecondTarget;
	
	// 光效创建的回调函数
	this->OnEffectCreate = TempOnEffectCreate;

	// 设置模板和资源
	SetTemplate(this->EffectEmitterData->ParticleData.ParticleSystemAsset.Get());
	// 不激活粒子
	GetParticleSystemComponent()->SetActive(false);
	GetParticleSystemComponent()->SetRelativeTransform(this->EffectEmitterData->ParticleData.ParticleSystemTransform);
	// 根据资源动态得添加组件
	if (TempEffectEmitterData->StaticMesh.StaticMeshAsset.Get())
	{
		STComponent = NewObject<UStaticMeshComponent>(this, TEXT("STComponent"));
		STComponent->RegisterComponent();
		STComponent->AttachToComponent(GetParticleSystemComponent(), FAttachmentTransformRules::KeepRelativeTransform);
		STComponent->SetHiddenInGame(true);
		STComponent->OnComponentBeginOverlap.AddDynamic(this, &AEffectEmitter::OnEmitterCollisionBegin);
		STComponent->OnComponentEndOverlap.AddDynamic(this, &AEffectEmitter::OnEmitterCollisionEnd);
		STComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		STComponent->bReceivesDecals = false;
		STComponent->ComponentTags.Add("NoUpdateVisible");
		STComponent->SetComponentTickInterval(0.1f);

		STComponent->SetStaticMesh(TempEffectEmitterData->StaticMesh.StaticMeshAsset.Get());
		STComponent->SetRelativeTransform(TempEffectEmitterData->StaticMesh.StaticMeshTransform);
	}

	if (TempEffectEmitterData->SkeletalMesh.SkeletalMeshAsset.Get())
	{
		SKComponent = NewObject<USkeletalMeshComponent>(this, TEXT("SKComponent"));
		SKComponent->RegisterComponent();
		SKComponent->AttachToComponent(GetParticleSystemComponent(), FAttachmentTransformRules::KeepRelativeTransform);
		SKComponent->OnComponentBeginOverlap.AddDynamic(this, &AEffectEmitter::OnEmitterCollisionBegin);
		SKComponent->OnComponentEndOverlap.AddDynamic(this, &AEffectEmitter::OnEmitterCollisionEnd);
		SKComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		SKComponent->bReceivesDecals = false;
		SKComponent->SetComponentTickInterval(0.1f);

		SKComponent->SetSkeletalMesh(TempEffectEmitterData->SkeletalMesh.SkeletalMeshAsset.Get());
		SKComponent->SetVisibility(false);
		SKComponent->SetRelativeTransform(TempEffectEmitterData->SkeletalMesh.SkeletalMeshTransform);
	}

	if (TempEffectEmitterData->EffectData.FlyData.MotionBlurMeshAsset.Get())
	{
		MotionBlurComponent = NewObject<UStaticMeshComponent>(this, TEXT("MotionBlurComponent"));
		MotionBlurComponent->RegisterComponent();
		MotionBlurComponent->AttachToComponent(GetParticleSystemComponent(), FAttachmentTransformRules::KeepRelativeTransform);
		MotionBlurComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		MotionBlurComponent->bReceivesDecals = false;

		MotionBlurComponent->SetStaticMesh(TempEffectEmitterData->EffectData.FlyData.MotionBlurMeshAsset.Get());
		MotionBlurComponent->SetVisibility(false);
		MotionBlurComponent->SetRelativeTransform(TempEffectEmitterData->EffectData.FlyData.MotionBlurMeshTransform);
	}
	//提前加载死亡特效 @CST-8885
	for (auto DeathID : TempEffectEmitterData->EffectData.BaseEffectData.DeathEffectList)
	{
		if (IsValid(UUECS3GameInstance::Instance))
			UGolbalBPFunctionLibrary::ParticleManager()->LoadParticleAsset(DeathID);
	}

	if (this->EffectEmitterData->CollisionResponse.Num()>0)
	{
		if (this->EffectEmitterData->CollisionResponse[0].bIsObstructible)
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(BulletBuffEventHandle, this, &AEffectEmitter::TranceBulletEvent, 0.05f, true);
		}
	}
	//CST-10243 程序功能需求（0级）——模型的表面创建粒子
	FParticleSysParam SysParam;
	SysParam.Actor = TempSecondTarget;
	SysParam.ParamType = EParticleSysParamType::PSPT_Actor;
	SysParam.Name = TEXT("EffectSysValue");
	this->GetParticleSystemComponent()->InstanceParameters.Add(SysParam);
	if (EffectEmitterData->ParticleData.TargetSortIndex!=0)
	{
		this->GetParticleSystemComponent()->TranslucencySortPriority = EffectEmitterData->ParticleData.TargetSortIndex;
	}
}

void AEffectEmitter::PrepareData()
{
	SCOPE_CYCLE_COUNTER(STAT_PrepareData);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("particle system : Particle UID named %d is beginplay"), UID);

	if (bHidden)
	{
		SetActorHiddenInGame(false);
	}

	// 初始与配置不一致的数据
	InitFromConfig();

	// 在编辑器模式下播放，给粒子在世界大纲添加标签
#if WITH_EDITOR
	if (GetWorld()->WorldType == EWorldType::PIE)
	{
		SetActorLabel(ActorName.ToString() + FString("(") + ID + FString(")") + FString("(") + INT_TO_FSTRING(UID) + FString(")"));
	}
#endif

	// 初始化位置
	InitEmitterTransform();

	// 添加粒子数据到管理器
	AddDataToManager();

	// 获取设置服务器传来的光效骨骼插槽
	if (Cast<AServerCharacter>(FirstTarget))
	{
		Cast<AServerCharacter>(FirstTarget)->GetEffectDynamicData(FirstTransform->BindSocket, FirstTransform->Transform);
	}

	// 判断此光效是否要打开Tick
	if (EffectEmitterData->ParticleData.bGraduallyHidden || Spline || EffectEmitterData->ParticleData.bUseConstAlpha || EffectEmitterData->ParticleData.bSortEffect || EffectEmitterData->ParticleData.bAlwaysRender)
	{
		SetActorTickEnabled(true);

		// 是否要进行透明处理
		if (EffectEmitterData->ParticleData.bGraduallyHidden || EffectEmitterData->ParticleData.bUseConstAlpha)
		{
			AddAlphaModule();
		}
	}

	// 该粒子是否需要排序
	if (EffectEmitterData->ParticleData.bSortEffect)
	{
		UUECS3GameInstance::Instance->ParticleManager->AddToSortList(UID);
	}

	// 绑定光效抵达回掉事件
	OnEffectArrived.AddDynamic(this, &AEffectEmitter::OnEmitterEffectArrived);

	// 触发回调，特殊光效可以用来后期设置位置使用
	(*(const FEffectCreate*)OnEffectCreate).ExecuteIfBound(UID);

	// 播放粒子
	Play();
}

void AEffectEmitter::ClearData()
{
	SCOPE_CYCLE_COUNTER(STAT_ClearData);

	// 清除路径资源
	if (IsValid(Spline))
	{
		Spline->Destroy();
		Spline = nullptr;
	}

	// 该粒子是否添加了动态模块，移除模块
	if (EffectEmitterData->ParticleData.bGraduallyHidden || EffectEmitterData->ParticleData.bUseConstAlpha)
	{
		RemoveModule();
	}

	// 该粒子是否需要排序,在没有经过Stop销毁时，做的处理
	if (EffectEmitterData->ParticleData.bSortEffect)
	{
		UUECS3GameInstance::Instance->ParticleManager->RemoveToSortList(UID);
	}

	// 清除管理器数据
	RemoveDataFormManager();
	///清除播放定时器
	ClearDelayPlayHandle();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("particle system :Particle UID named %d is endplay"), UID);
}

void AEffectEmitter::AddDataToManager()
{
	// 把光效加入管理器列表
	UParticleManager* ParticleManager = UUECS3GameInstance::Instance->ParticleManager;
	FInternal_EffectData& EffectInternalData = ParticleManager->UEffectMap[UID];
	EffectInternalData.EffectInstance = EffectEmitterData->EffectInstance.Get();
	EffectInternalData.Parent = SetEffectVisible();
	EffectInternalData.Owner = this;

	// 根据配置更新光效可见性
	UpdateVisibilityData(true);
}

void AEffectEmitter::RemoveDataFormManager()
{
	// 根据配置更新光效可见性
	UpdateVisibilityData(false);

	// 粒子管理器中已经不存在这个UID了，改为-1
	UID = -1;
}

void AEffectEmitter::ClearDataAndAddToBufferPool()
{
	SCOPE_CYCLE_COUNTER(STAT_ClearDataAndAddToBufferPool);

	// 清空所有数据，放到粒子缓冲池中
	OnEffectStop.Clear();
	OnEffectArrived.Clear();
	ChildrenEffectUID.Empty();

	CurrentTime = 0.0f;
	OnEffectCreate = nullptr;
	MoveSpeed = 0.0f;
	AnimAsset.Empty();
	ModuleList.Empty();

	UParticleSystemComponent* ParticleComponent = GetParticleSystemComponent();
	ParticleComponent->SetTemplate(nullptr);
	ParticleComponent->SetAbsolute(false, false, false);
	ParticleComponent->SetRelativeTransform(FTransform());
	ParticleComponent->SetComponentTickEnabled(false);


	if (STComponent)
	{
		// 加入缓存池
		STComponent->DestroyComponent();
		STComponent = nullptr;
	}

	if (SKComponent)
	{
		// 加入缓存池
		SKComponent->DestroyComponent();
		SKComponent = nullptr;
	}

	// 清空额外的组件
	TSet<UActorComponent*> Components = GetComponents();
	Components.Remove(GetRootComponent());
	Components.Remove(GetParticleSystemComponent());
	Components.Remove(SceneTransformComp);
	for (auto Component : Components)
	{
		Component->DestroyComponent();
	}
	
	DetachFromActor(FDetachmentTransformRules::KeepWorldTransform);
	SetActorScale3D(FVector(1.f));
	if (IsValid(SceneTransformComp))
	{
		SceneTransformComp->ResetRelativeTransform();
	}
	UUECS3GameInstance::Instance->CustomTimerManager->ClearAllTimersForObject(this);
	SetActorTickEnabled(false);
	UUECS3GameInstance::Instance->ParticleManager->AddToParticleBufferPool(this);

#if WITH_EDITOR
	// 被回收的光效恢复原来的名字，在下一次Tick的时候改变，在GC中使用SetActorLabel会导致崩溃
	if (GetWorld()->WorldType == EWorldType::PIE)
	{
		TWeakObjectPtr<AEffectEmitter> ThisPtr(this);
		GetWorld()->GetTimerManager().SetTimerForNextTick(FTimerDelegate::CreateLambda([ThisPtr]()
		{
			if (ThisPtr.IsValid())
			{
				AEffectEmitter* Effect = ThisPtr.Get();
				// 是否在缓冲池中
				if (UUECS3GameInstance::Instance->ParticleManager->CheckOnBufferPool(Effect))
				{
					Effect->SetActorLabel(Effect->ActorName.ToString());
				}
			}
		}));
	}
#endif
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("particle add to buffer pool : %s,%d"), *ID, UID);
}

void AEffectEmitter::BeginPlay()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		OnEndPlay.AddUniqueDynamic(UUECS3GameInstance::Instance, &UUECS3GameInstance::OnActorEndPlay);
	}

#if WITH_EDITOR
	// 编辑器下保存下Actor的名字，用于设置世界大纲显示的名称
	ActorName = GetFName();

	bDefer = false;
#endif
	// 关闭Tick
	PrimaryActorTick.bCanEverTick = true;
	SetActorTickEnabled(false);

	// 准备所有的粒子数据
	PrepareData();

	Super::BeginPlay();
}

void AEffectEmitter::AddAlphaModule(UParticleSystemComponent* ParticleComponent/* = nullptr*/)
{
	if (!ParticleComponent)
	{
		ParticleComponent = GetParticleSystemComponent();
	}
	if (!ParticleComponent->Template)
		return;
	//给粒子添加透明度模块
	UParticleEmitter* CurEmitters;
	UParticleLODLevel* CurLOD;
	for (int i = 0; i < ParticleComponent->Template->Emitters.Num(); i++)
	{
		CurEmitters = ParticleComponent->Template->Emitters[i];
		
		for (int j = 0; j < CurEmitters->LODLevels.Num(); j++)
		{
			CurLOD = CurEmitters->LODLevels[j];

			if (CurLOD->Modules.Num())
			{
				if (!CurLOD->Modules[CurLOD->Modules.Num() - 1]->IsA(UParticleModuleColorOverLifeEX::StaticClass()))
				{
					UParticleModuleColorOverLifeEX* NewModule = NewObject<UParticleModuleColorOverLifeEX>(CurEmitters->GetOuter());
					// 添加模块到管理列表
					AddModule(NewModule, i, j);
					CurLOD->Modules.Add(NewModule);
					CurLOD->SpawnModules.Add(NewModule);
					CurLOD->UpdateModules.Add(NewModule);
				}
				else
				{
					// 添加模块到管理列表
					AddModule(CurLOD->Modules[CurLOD->Modules.Num() - 1], i, j);
				}
			}
		}
	}
}

AActor* AEffectEmitter::SetEffectVisible()
{
	AActor* Target = FirstTarget;
	AServerCharacter* ServerTarget = Cast<AServerCharacter>(Target);

	bool visible = false;				// 默认显示，因为使用hidden设置的，所以相反

	if (FirstTransform->bIsBind)	// 判断是否绑定
	{
		Target = nullptr;
	}
	
	if (EffectData->BaseEffectData.bIsBindingVisibility)	// 非绑定光效是否绑定可见性
	{
		if (ServerTarget)				// 判断是否是服务器对象
		{
			visible = ServerTarget->VisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
		}
		else if (Target)
		{
			visible = Target->bHidden;
		}
	}

	SetActorHiddenInGame(visible);
	
	if (!visible && STComponent)
	{
		STComponent->SetVisibility(EffectEmitterData->StaticMesh.StaticMeshVisibility);
		STComponent->SetHiddenInGame(false);
	}

	return Target;
}

void AEffectEmitter::InitFromConfig()
{
	EffectData = &(EffectEmitterData->EffectData);
	
	// 位置
	FirstTransform = &(EffectData->BaseEffectData.bIsSwap ? EffectData->BaseEffectData.SecondTransform : EffectData->BaseEffectData.FirstTransform);
	SecondTransform = &(EffectData->BaseEffectData.bIsSwap ? EffectData->BaseEffectData.FirstTransform : EffectData->BaseEffectData.SecondTransform);

	// 生命周期
	LifeTime			= EffectData->BaseEffectData.LifeTime < 0.f ? 99999.f : EffectData->BaseEffectData.LifeTime;

	// 透明度
	FadeInTime			= EffectEmitterData->ParticleData.FadeInTime < 0 ? 0: EffectEmitterData->ParticleData.FadeInTime;
	FadeInTime			= FadeInTime <= LifeTime ? FadeInTime : LifeTime;
	FadeOutTime			= EffectEmitterData->ParticleData.FadeOutTime < 0 ? LifeTime : EffectEmitterData->ParticleData.FadeOutTime;
	FadeOutTime			= LifeTime - FadeOutTime >= FadeInTime ? FadeOutTime : LifeTime - FadeInTime;
	Alpha				= FMath::Abs(FadeInTime - 0.0f) < 0.01f || !EffectEmitterData->ParticleData.bGraduallyHidden ? 1.0f : 0.0f;

	// Mesh相关
	for (auto CurrentAsset : EffectEmitterData->SkeletalMesh.AnimAssetList)
	{
		AnimAsset.Add(CurrentAsset.Get());
	}

	// 路径
	if (EffectEmitterData->Spline.SplineAsset)
	{
		// 生成路径实例
		InitSplineFromConfig();
	}
}

void AEffectEmitter::InitSplineFromConfig()
{
	const FSPLINE_ASSET& SplineData = EffectEmitterData->Spline;
	FTransform Transform = FTransform();
	Transform.SetLocation(GetActorLocation());
	Transform.SetRotation(GetActorQuat());

	// DeferredSpawn
	Spline = Cast<ABaseSplineAsset>(UGolbalBPFunctionLibrary::BeginDeferredActorSpawnFromClass(SplineData.SplineAsset.Get(), Transform));
	if (Spline)
	{
		// 在BeginPlay之前初始化一些必要的数据
		Spline->LoopNumber = SplineData.LoopNumber ? SplineData.LoopNumber : 99999999;
		Spline->MoveSpeed = MoveSpeed = SplineData.MoveSpeed;
		Spline->AttachToActor(this, FAttachmentTransformRules::SnapToTargetIncludingScale);		
		Spline->SplineComponent->SetAbsolute(SplineData.IsLocationOnWorld, SplineData.IsRotationOnWorld, SplineData.IsScaleOnWorld);
		UGameplayStatics::FinishSpawningActor(Spline, Transform);
		Spline->SplineComponent->SetRelativeTransform(SplineData.SplineTransform);
	}
}

void AEffectEmitter::InitEmitterTransform()
{
	// 设置位置，默认情况下是按给受术者的位置进行设置，是SecondTarget，当然总有例外，后续可能会扩展
	// 目前是按照受术者定义

	ACharacter* Character = Cast<ACharacter>(SecondTarget);
	if (SecondTransform->bIsBind)
	{
		this->GetRootComponent()->SetAbsolute(0, 0, 0);
		AttachToComponent(Character ? GetBindComponent() : SecondTarget->GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform, FName(*SecondTransform->BindSocket));
		SetActorRelativeTransform(SecondTransform->Transform, true);
	}
	else
	{
		//不绑定的光效，如果是Charcter设置在Mesh组件的位置，如果是Actor，设置在Actor根组件的位置
		SetActorTransform(Character ? Character->GetMesh()->GetSocketTransform(FName(*SecondTransform->BindSocket)) : SecondTarget->GetActorTransform());
		AddActorLocalOffset(SecondTransform->Transform.GetLocation());
		AddActorLocalRotation(SecondTransform->Transform.GetRotation());
		SetActorScale3D(SecondTransform->Transform.GetScale3D());
	}

	//如果不是Character，给光效加90°的偏移，因为骨骼和胶囊体的坐标不一致，骨骼相对于胶囊体旋转了-90°
	if (!Character)
	{
		AddActorLocalRotation(FRotator(0, -90, 0));
	}

	//在改变变换方式前保存当前的位置，下面涉及到绑定关系
	FVector CurLocation = GetActorLocation();

	//设置变换方式
	this->GetRootComponent()->SetAbsolute(SecondTransform->bIsLocationOnWorld, SecondTransform->bIsRotationOnWorld, SecondTransform->bIsScaleOnWorld);

	//绑定的光效在绝对位置的情况下为目标位置，不绑定光效在绝对位置下位所填的位置
	if (SecondTransform->bIsLocationOnWorld)
	{
		if (SecondTransform->bIsBind)
		{
			SetActorLocation(CurLocation);
		}
		else
		{
			SetActorLocation(SecondTransform->Transform.GetLocation());
		}
	}

	//不绑定的光效在绝对旋转的情况下为所填的旋转
	if (SecondTransform->bIsRotationOnWorld && !SecondTransform->bIsBind)
	{
		SetActorRotation(SecondTransform->Transform.GetRotation());
	}

	//没有对缩放进行处理，如果有需要，可以做处理

	//表现组件中添加此光效，为了在Actor销毁时，正确的销毁此对象
	if (Cast<AGameCharacter>(SecondTarget) && (SecondTransform->bIsBind || EffectData->BaseEffectData.bIsBindingVisibility))
	{
		Cast<AGameCharacter>(SecondTarget)->GetPerformanceComponent()->AddEffect(UID);
	}

	//有路径资源的光效在蓝图中初始化位置
	if (IsValid(Spline))
	{
		InitSplineTransform();
	}
}

void AEffectEmitter::InitSplineTransform()
{
	const FSPLINE_ASSET& SplineData = EffectEmitterData->Spline;

	if (SplineData.IsLocationOnWorld)
	{
		Spline->SetActorLocation(GetTargetLocation());
	}

	if (SplineData.IsRotationOnWorld)
	{
		Spline->SetActorRotation(GetActorRotation());
	}

	Spline->AddActorWorldRotation(FRotator(0, EffectSendAngle, 0));

	// 初始化粒子的位置，在曲线的起点
	if (IsValid(Spline->SplineComponent))
	{
		Spline->SceneComponentMoveOnSpline(SceneTransformComp, true, 0.0f);
	}
}

void AEffectEmitter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (UID != -1)
	{
		ClearData();
	}

	Super::EndPlay(EndPlayReason);
}

#if WITH_EDITOR
void AEffectEmitter::Destroyed()
{
	if (UUECS3GameInstance::Instance && bDefer)
	{
		RemoveFromRoot();
		UUECS3GameInstance::Instance->ParticleManager->RemoveFromParticleDeferSpawnPool(this);
	}
	Super::Destroyed();
}
#endif

void AEffectEmitter::Play()
{

#if WITH_EDITOR
	if (bIsInEdit)
	{
		StartPlay();
		return;
	}
#endif // WITH_EDITOR


	if (bPlaying)
	{
		return;
	}

	if (EffectData->BaseEffectData.DelayPlayTime > 0)
	{
		ClearDelayPlayHandle();
		//延时播放
		if (IsValid(UUECS3GameInstance::Instance))
		{
			if (GetParticleSystemComponent()->bVisible)
			{
				GetParticleSystemComponent()->SetVisibility(false);
			}
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayPlayHandle, this, &AEffectEmitter::StartPlay, EffectData->BaseEffectData.DelayPlayTime, false);
		}
	}
	else
	{
		StartPlay();
	}
}

void AEffectEmitter::OnPlay()
{

}

void AEffectEmitter::ClearDelayPlayHandle()
{
	if (IsValid(UUECS3GameInstance::Instance) && DelayPlayHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayPlayHandle);
	}
}

void AEffectEmitter::PlayAnimation()
{
	if (!SKComponent)
	{
		return;
	}

	if (AnimAsset.Num() && AnimAsset[0])
	{

		//播放动作
		SKComponent->PlayAnimation(AnimAsset[0], true);
		SKComponent->SetPlayRate(EffectEmitterData->SkeletalMesh.PlayRate);

		//在光效预创建时 会有模型残留问题 具体JIRA CST-8649
		FTimerHandle DelayHandle;
		TWeakObjectPtr<AEffectEmitter> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle, FTimerDelegate::CreateLambda([DelayThisPtr]()
			{
				DelayThisPtr->SKComponent->SetVisibility(true);
			}), 0.05f, false);
	}
	else
	{
		SKComponent->SetVisibility(true);
	}

}

void AEffectEmitter::SetBuffBulletData(const int32 BuffIndex, const int32 ProxyID, const int32 OwnerID, const int32 EffectIndex,const int32 EffectCustomIndex)
{
	BulletBuffIndex = BuffIndex;
	BulletBuffProxyId = ProxyID;
	BulletBuffOwnerId = OwnerID;
	BulletBuffEffectIndex = EffectIndex;
	BulletBuffEffectCustomIndex = EffectCustomIndex;
}

void AEffectEmitter::SetEmitterCollisionData(const int32 ProxyID)
{
	EmitterCollisionProxyId = ProxyID;
}

void AEffectEmitter::ResetTarget(AActor * Target1, AActor * Target2)
{
	if (EffectEmitterData)
	{   
		// 根据配置调整光效的目标		
		this->FirstTarget = EffectEmitterData->EffectData.BaseEffectData.bIsSwap ? Target2 : Target1;
		this->SecondTarget = EffectEmitterData->EffectData.BaseEffectData.bIsSwap ? Target1 : Target2;
		InitEmitterTransform();
	}

}

void AEffectEmitter::Stop(bool notDelay, bool notDelayDestroyChildren, bool bPlayDeathParticle, bool bAddParticleBufferPool)
{
	SCOPE_CYCLE_COUNTER(STAT_Stop);

	//在播放状态才可以停止
	if (!bPlaying)
	{
		if (DelayPlayHandle.IsValid())
		{
			/// 在延时播放时情况
			ClearDelayPlayHandle();
		}
		else
		{
			/// 资源加载中情况
			UUECS3GameInstance::Instance->ParticleManager->SetEffectValidByID(UID, false);
			return;
		}
	}

	//先关闭碰撞，触发光效离开碰撞逻辑
	SetMeshComponentCollision(false);

	//停止播放
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
	{
		UUECS3GameInstance::Instance->AudioManager->Stop3DSound(AudioComponent);
		AudioComponent = nullptr;
	}	

	bPlaying = false;

	// 停止播放粒子
	GetParticleSystemComponent()->SetActive(false);

	//光效停止的回调
	OnEffectStop.Broadcast();

	// 销毁子对象
	if (EffectData->BaseEffectData.bIsDestroyChildren)
	{
		for (auto EffectUID : ChildrenEffectUID)
		{
			UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(EffectUID, notDelayDestroyChildren, notDelayDestroyChildren, bPlayDeathParticle, bAddParticleBufferPool);
		}
	}

	// 如果有路径，把光效本身设置到粒子组件的位置，此时粒子已经播放完毕，碰撞已经关闭，改变位置亦不会有其他影响
	if (Spline)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("particle system : Reset particle location beacuse the particle has spline asset! particle id: %s"), *ID);
		SetActorLocation(GetParticleSystemComponent()->GetComponentLocation());
		GetParticleSystemComponent()->SetRelativeLocation(FVector::ZeroVector);
	}

	// 播放死亡光效
	if (bPlayDeathParticle)
	{
		PlayDeathParticle();
	}

	// 销毁或者延时销毁
	if (EffectData->BaseEffectData.DelayDestroyTime > 0.0f && !notDelay)//延时销毁
	{
		FTimerHandle DelayDestroyHandle;
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayDestroyHandle,
				FTimerDelegate::CreateUObject(this, &AEffectEmitter::DestroyEffect, bAddParticleBufferPool), EffectData->BaseEffectData.DelayDestroyTime, false);
		}
		DelayDestroySetting();
	}
	else
	{
		DestroyEffect(bAddParticleBufferPool);
	}

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("particle system : stop particle! particle id: %s"), *ID);
}

void AEffectEmitter::StartPlay()
{	
#if WITH_EDITOR
	if (bIsInEdit)
	{
		ClearDelayPlayHandle();
		PlayAnimation();					//播放动画
		Activate();							//播放粒子
		PlayChildParticle();				//播放子光效
		return;
	}
#endif

	SCOPE_CYCLE_COUNTER(STAT_StartPlay);
	// 上一波操作中光效可能被隐藏，准备数据的时候重置，下面还会再次设置可见性
	if (!GetParticleSystemComponent()->bVisible)
	{
		GetParticleSystemComponent()->SetVisibility(true);
	}
	ClearDelayPlayHandle();
	// 如果是0秒光效，强制给一个时间0.01秒，我们走正规流程
	LifeTime = FMath::Abs(LifeTime - 0.0f) > 0.01f ? LifeTime : 0.01f;

	if (LifeTime > 0.0f)
	{
		// 延时销毁
		FTimerHandle DelayStopHandle;
		if (UUECS3GameInstance::Instance)
		{
			TWeakObjectPtr<AEffectEmitter> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayStopHandle,
				FTimerDelegate::CreateLambda([DelayThisPtr]()
			{
				DelayThisPtr->Stop(false, false);
			}), LifeTime, false);
		}
	}


	bPlaying = true;													//设置播放状态
	PlayAnimation();													//播放动画
	GetParticleSystemComponent()->SetActive(true, true);				//播放粒子
	PlayChildParticle();												//播放子光效
	SetMeshComponentCollision(true, EffectEmitterData->StaticMesh.CollisionResponse);									//开启碰撞

	// 播放粒子附带的音效
	if (IsValid(UUECS3GameInstance::Instance->AudioManager))
	{
		AudioComponent = UUECS3GameInstance::Instance->AudioManager->Play3DSoundByAsset(this, 
			EffectEmitterData->Audio.AudioAsset.Get(), FVector::ZeroVector, EAUDIOCOMPTYLE::NONE, 
			EffectEmitterData->Audio.bIsLoop, GetParticleSystemComponent());
	}
}

void AEffectEmitter::OnEmitterCollisionBegin(UPrimitiveComponent* OverlappedComp, AActor* Other, 
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	CS3_Display(CS3DebugType::CL_Undefined,
		TEXT("AEffectEmitter::OnEmitterCollision[Begin]=%s,"), *Other->GetName());

	SCOPE_CYCLE_COUNTER(STAT_OnEmitterCollisionBegin);
	/*光效的具体碰撞结果SweepResult无效值，只是进行了碰撞检测，如需要具体结果，请在STComponent移动时把bSweep属性设置为true，但是消耗会变大，必要时可配置处理*/

	if (!bPlaying) return;
	// 判断碰撞的时机
	for (auto CollisionData : EffectEmitterData->CollisionResponse)
	{	// 判断碰撞类型
		if (CollisionData.TriggerType == RESPONSE_TYPE::BEGIN_COLLISION)
		{
			if (!CollisionData.ActorType || Other->IsA(CollisionData.ActorType))
			{
				AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Other);
				
				// 判断服务器类型
				if ((CollisionData.EntityType != "" && IsValid(ServerCharacter) && ServerCharacter->GetSelfEntity() &&
					*ServerCharacter->GetSelfEntity()->ClassName() == CollisionData.EntityType) || 
					CollisionData.EntityType == "")
				{	// 循环触发方法
					for (FMETHOD_NAME MethodData : CollisionData.MethodList)
					{
						KBEngine::FVariantArray args;
						// 循环填充参数
						for (PARAMS_TYPE MethodParams : MethodData.ParamsList)
						{
							if (MethodParams == PARAMS_TYPE::BULLETBUFF)
							{
								UCapsuleComponent* OtherCapsuleCpt = Cast<UCapsuleComponent>(OtherComp);
								if (IsValid(OtherCapsuleCpt))///是胶囊体对象
								{
									CollisionList.Add(Other, 0.0f);
									AddBulletMsgBegin(&args, ServerCharacter); 
								}
								else
								{
									if (IsValid(ServerCharacter))
									{
										UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(ServerCharacter->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
										if (OtherComp == DefaultStaticMeshCpt)///是默认静态物体对象
										{
											CollisionList.Add(Other, 0.0f);
											AddBulletMsgBegin(&args, ServerCharacter);
										}
									}
								}
							}
							else if (MethodParams == PARAMS_TYPE::OtherEntityID)
							{
								args.Add(INT_TO_FSTRING(GetEntityID(ServerCharacter)));
							}
							else if (MethodParams == PARAMS_TYPE::SKILLID)
							{
								args.Add(INT_TO_FSTRING(CollisionData.ResponseSkillID));
							}
						}
						
						//DrawDebugPoint(GetWorld(), SweepResult.ImpactPoint, 5, FColor::Green, false, 50);
						//DrawDebugBox(GetWorld(), OverlappedComp->GetComponentLocation(), Cast<UStaticMeshComponent>(OverlappedComp)->GetStaticMesh()->GetBounds().BoxExtent * 2 * OverlappedComp->GetComponentScale(), OverlappedComp->GetComponentRotation().Quaternion(), FColor::Red, false, 2.f);
						CS3_Display(CS3DebugType::CL_Undefined, TEXT("Drive back to sleep enter:%s,%s,%s"), *OtherComp->GetName(), *Other->GetName(), *OverlappedComp->GetName());
						
						// 调用服务器方法
						KBEngine::Entity* Player = UUECS3GameInstance::pKBEApp->Player();
						CS3Entity* pEntity_Player = (CS3Entity*)(Player);
						if (pEntity_Player && pEntity_Player->IsPlayerRole() && (EmitterCollisionProxyId == -1 || EmitterCollisionProxyId == pEntity_Player->ID()))
						{
							// 如果不是子弹Buff，并且碰撞的对象是玩家且不是本地玩家，就不发送
							if (!MethodData.ParamsList.Contains(PARAMS_TYPE::BULLETBUFF) &&
								Cast<APlayerCharacter>(ServerCharacter) &&
								ServerCharacter->EntityId != pEntity_Player->ID())
							{
								continue;
							}
							pEntity_Player->CellCall(MethodData.MethodName, args);
						}
					}
				}
			}
		}
	}
}

void AEffectEmitter::OnEmitterCollisionEnd(UPrimitiveComponent* OverlappedComp, AActor* Other, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{
	SCOPE_CYCLE_COUNTER(STAT_OnEmitterCollisionEnd);

	CS3_Display(CS3DebugType::CL_Undefined,
		TEXT("AEffectEmitter::OnEmitterCollision[End]=%s,"), *Other->GetName());

	if (!bPlaying) return;
	AServerCharacter *OtherCharacter = Cast<AServerCharacter>(Other);
	UCapsuleComponent *OtherCapsuleCpt = Cast<UCapsuleComponent>(OtherComp);
	//移除子弹Buff对象
	if (IsValid(OtherCharacter))
	{
		UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(OtherCharacter->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
		if (IsValid(OtherCapsuleCpt) || OtherComp == DefaultStaticMeshCpt)
		{
			CollisionList.Remove(Other);
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Drive back to sleep leave:%s,%s,%s"), *OtherComp->GetName(), *Other->GetName(), *OverlappedComp->GetName());
		}
	}

	//判断碰撞的时机
	for (auto CollisionData : EffectEmitterData->CollisionResponse)
	{	//判断碰撞类型
		if (CollisionData.TriggerType == RESPONSE_TYPE::END_COLLISION)
		{
			if (!CollisionData.ActorType || Other->IsA(CollisionData.ActorType))
			{
				AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Other);
				//判断服务器类型
				if ((CollisionData.EntityType != "" && ServerCharacter && ServerCharacter->GetSelfEntity() && *ServerCharacter->GetSelfEntity()->ClassName() == CollisionData.EntityType) || CollisionData.EntityType == "")
				{	//循环触发方法
					for (FMETHOD_NAME MethodData : CollisionData.MethodList)
					{
						KBEngine::FVariantArray args;
						//循环填充参数
						for (PARAMS_TYPE MethodParams : MethodData.ParamsList)
						{
							if (MethodParams == PARAMS_TYPE::OtherEntityID)
							{
								args.Add(INT_TO_FSTRING(GetEntityID(ServerCharacter)));
							}
						}
						//调用服务器方法
						KBEngine::Entity* Player = UUECS3GameInstance::pKBEApp->Player();
						CS3Entity* pEntity_Player = (CS3Entity*)(Player);
						if (pEntity_Player && pEntity_Player->IsPlayerRole() && (EmitterCollisionProxyId == -1 || EmitterCollisionProxyId == pEntity_Player->ID()))
						{
							// 如果不是子弹Buff，并且碰撞的对象是玩家且不是本地玩家，就不发送
							if (!MethodData.ParamsList.Contains(PARAMS_TYPE::BULLETBUFF) && Cast<APlayerCharacter>(ServerCharacter) && ServerCharacter->EntityId != pEntity_Player->ID())
							{
								continue;
							}
							pEntity_Player->CellCall(MethodData.MethodName, args);
						}
					}
				}
			}
		}
	}
	
	//碰撞结束处理（暂不启用）
	/*
	if (BuffProxyId == -1)
	{
		if (UGolbalBPFunctionLibrary::GetCS3PlayerCharacter() == Other)
		{
			TArray<FString> Arguments;
			FString MethodName = TEXT("onBulletCollisionEnd");
			Arguments.Add(INT_TO_FSTRING(BuffOwnerId));
			Arguments.Add(INT_TO_FSTRING(UGolbalBPFunctionLibrary::GetPlayerID()));
			UGolbalBPFunctionLibrary::CellCall(UGolbalBPFunctionLibrary::GetPlayerID(), MethodName, Arguments);
		}
	}
	else if (BuffProxyId == UGolbalBPFunctionLibrary::GetPlayerID())
	{
		if (AServerCharacter* Target = Cast<AServerCharacter>(Other))
		{
			TArray<FString> Arguments;
			FString MethodName = TEXT("onBulletCollisionEnd");
			Arguments.Add(INT_TO_FSTRING(BuffOwnerId));
			Arguments.Add(INT_TO_FSTRING(Target->EntityId));
			UGolbalBPFunctionLibrary::CellCall(UGolbalBPFunctionLibrary::GetPlayerID(), MethodName, Arguments);
		}
	}
	*/
}

void AEffectEmitter::PlayChildParticle()
{
#if WITH_EDITOR
	if (bIsInEdit)
	{
		UParticleManager* ParticleManager = NewObject<UParticleManager>();

		if (IsValid(ParticleManager))
		{
			for (FString ChildID : EffectData->BaseEffectData.ChildrenEffectList)
			{
				const FEFFECT_EMITTER_DATA* TempEffectData = ParticleManager->GetEffectData(ChildID);
				ASpawnBase* SpawnBase = Cast<ASpawnBase>(FirstTarget);

				if (SpawnBase && TempEffectData)
				{
					AEffectEmitter* Effect= ParticleManager->PlayParticleOfEdit(FSTRING_TO_FNAME(ChildID), FirstTarget);
					if (Effect)
					{
						SpawnBase->CurEffect.Add(Effect);
					}
				}
			}
		}

		return;
	}
#endif //WITH_EDITOR

	// 子光效会跟随销毁
	int32 ChildUID;
	for (FString ChildID : EffectData->BaseEffectData.ChildrenEffectList)
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			ChildUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(ChildID, 0.0f, FirstTarget, SecondTarget);
		}
		this->ChildrenEffectUID.Add(ChildUID);
	}
}

void AEffectEmitter::PlayDeathParticle()
{
	// 死亡光效不会跟随销毁，所以把目标给了世界
	FVector Location;
	for (auto DeathID : EffectData->BaseEffectData.DeathEffectList)
	{
		Location = this->GetActorLocation();
		if (IsValid(UUECS3GameInstance::Instance))
		{
			TWeakObjectPtr<AActor> DelayTargetPtr(this);
			UUECS3GameInstance::Instance->ParticleManager->PlayParticle(DeathID, 0.0f, GetWorld()->GetWorldSettings(), GetWorld()->GetWorldSettings(), FEffectCreate::CreateLambda([Location, DelayTargetPtr](int32 UID)
			{
				AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
				if (Effect)
				{
					Effect->AddActorWorldOffset(Location);
					if (IsValid(DelayTargetPtr.Get()))
					{						 
						Cast<AEffectEmitter>(Effect)->ResetTarget(DelayTargetPtr.Get(), DelayTargetPtr.Get());
					}
				}
			}));
		}
	}
}

void AEffectEmitter::DestroyEffect(bool bAddParticleBufferPool)
{
	// 获取粒子的类，直接通过配置表get会崩溃
	UClass* Class = nullptr;
	if (UUECS3GameInstance::Instance->ParticleManager->UEffectMap.Contains(UID))
	{
		Class = UUECS3GameInstance::Instance->ParticleManager->UEffectMap[UID].EffectInstance;
	}

	ClearData();

	if (bAddParticleBufferPool && UUECS3GameInstance::Instance->ParticleManager->IsCacheClass(Class))
	{
		ClearDataAndAddToBufferPool();
	}
	else
	{
		Destroy();
	}
}

void AEffectEmitter::OnEmitterEffectArrived()
{
	RPC_onBulletCollisionArrive();
}

void AEffectEmitter::RPC_onBulletCollisionArrive()
{
	KBEngine::FVariantArray args;
	AddBulletMsgBegin(&args, SecondTarget);

	if (!IsValid(UUECS3GameInstance::Instance))
	{
		return;
	}
		
	KBEngine::Entity* Player = UUECS3GameInstance::pKBEApp->Player();
	CS3Entity* pEntity_Player = (CS3Entity*)(Player);

	if (pEntity_Player && pEntity_Player->IsPlayerRole())
	{
		USkillInterface * SkillInterface = ((GameObject*)pEntity_Player)->Interface_Cache.SkillInterface;
		if (SkillInterface)
		{
			SkillInterface->onBulletCollisionArrive(args);
		}
		//pEntity_Player->CellCall(TEXT("onBulletCollisionArrive"), args);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Drive back to sleep arrived:%s"), *ID);
	}
}

void AEffectEmitter::SetMeshComponentCollision(bool State, ECollisionResponse CollisionResponse)
{
	// 只是设置了STComponent，因为只有STComponent做碰撞检测
	if (!STComponent)
	{
		return;
	}

	if (State)
	{
		STComponent->SetCollisionResponseToAllChannels(CollisionResponse);
		STComponent->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	}
	else
	{
		STComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
}

USceneComponent* AEffectEmitter::GetBindComponent()
{
	AGameCharacter* Character = Cast<AGameCharacter>(SecondTarget);
	if (SecondTransform->BindCompoent == BIND_COMPOENT_TYPE::DEFAULT_Mesh)
	{
		return Character->GetMesh();
	}
	else if (SecondTransform->BindCompoent == BIND_COMPOENT_TYPE::WAISTADORN_Mesh)
	{
		return Character->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_WAIST_ADORN);
	}
	else if (SecondTransform->BindCompoent == BIND_COMPOENT_TYPE::HAIRADORN_Mesh)
	{
		return Character->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_ADORN);
	}
	else if (SecondTransform->BindCompoent == BIND_COMPOENT_TYPE::HEADADORN_Mesh)
	{
		return Character->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_HEAD_ADORN);
	}
	else if (SecondTransform->BindCompoent == BIND_COMPOENT_TYPE::BACKADORN_Mesh)
	{
		return Character->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_BACK_ADORN);
	}
	else if (SecondTransform->BindCompoent == BIND_COMPOENT_TYPE::BWEAPON_Mesh)
	{
		return Character->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_BWEAPON);
	}
	else if (SecondTransform->BindCompoent == BIND_COMPOENT_TYPE::LWEAPON_Mesh)
	{
		return Character->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_LWEAPON);
	}
	else if (SecondTransform->BindCompoent == BIND_COMPOENT_TYPE::RWEAPON_Mesh)
	{
		return Character->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_RWEAPON);
	}
	else if (SecondTransform->BindCompoent == BIND_COMPOENT_TYPE::S_LWEAPON_Mesh)
	{
		return Character->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON);
	}
	else if (SecondTransform->BindCompoent == BIND_COMPOENT_TYPE::S_RWEAPON_Mesh)
	{
		return Character->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON);
	}
	return nullptr;
}

void AEffectEmitter::UpdateTransparency(float DeltaSeconds)
{
	if (EffectEmitterData->ParticleData.bGraduallyHidden)
	{
		if (FadeInTime > CurrentTime)
		{
			// 淡入
			Alpha += DeltaSeconds / FadeInTime;
		}
		else if (LifeTime - CurrentTime < FadeOutTime)
		{
			// 淡出
			Alpha -= DeltaSeconds / FadeOutTime;
		}
		else
		{
			Alpha = 1.0f;
		}
	}
}

void AEffectEmitter::Tick(float DeltaTime)
{
	if (bPlaying)
	{
		CurrentTime += DeltaTime;

		// 持续更新粒子发射器数据
		if (EffectEmitterData->ParticleData.bAlwaysRender && GetWorld()->TimeSeconds > GetParticleSystemComponent()->LastRenderTime)
		{
			GetParticleSystemComponent()->LastRenderTime = 999.f;		//设置上次渲染的时间
		}
		
		// 粒子排序
		if (EffectEmitterData->ParticleData.bSortEffect)
		{
			SortEffect();
		}

		// 光效逐渐消散
		UpdateTransparency(DeltaTime);

		// 持续响应子弹Buff受击
		CycleResponseCollisionEvent(DeltaTime);
		
		// 光效在路径上移动
		if (IsValid(Spline) && IsValid(Spline->SplineComponent))
		{
			Spline->SceneComponentMoveOnSpline(SceneTransformComp, true, DeltaTime);
		}
	}

	Super::Tick(DeltaTime);
}

void AEffectEmitter::CycleResponseCollisionEvent(float DeltaTime)
{
	const TArray<FEFFECT_COLLISION_RESPONSE>& CollisionResponseData = EffectEmitterData->CollisionResponse;

	// 这个地方只有第一份数据是保持的是否循环触发
	if (CollisionResponseData.Num() && CollisionResponseData[0].bIsLoopResponse)
	{
		// 子弹Buff持续受击判断
		for (TMap<AActor*, float>::TIterator TBegin = CollisionList.CreateIterator(); TBegin; ++TBegin)
		{
			if (IsValid(TBegin->Key))
			{
				TBegin->Value += DeltaTime;
				if (TBegin->Value > CollisionResponseData[0].LoopTime)
				{
					KBEngine::FVariantArray args;
					AddBulletMsgBegin(&args, TBegin->Key);

					KBEngine::Entity* Player = UUECS3GameInstance::pKBEApp->Player();
					CS3Entity* pEntity_Player = (CS3Entity*)(Player);
					if (pEntity_Player && pEntity_Player->IsPlayerRole() && (EmitterCollisionProxyId == -1 || EmitterCollisionProxyId == pEntity_Player->ID()))
					{
						USkillInterface * SkillInterface = ((GameObject*)pEntity_Player)->Interface_Cache.SkillInterface;
						if (SkillInterface && args.Num() == 6)
						{
							SkillInterface->RPC_onBulletCollisionBegin(args);
						}
					}
					TBegin->Value = 0.0f;
				}
			}
			else
			{
				TBegin.RemoveCurrent();
			}
		}
	}
}

void AEffectEmitter::DelayDestroySetting()
{
	//停止播放动作
	if (SKComponent)
	{
		SKComponent->Stop();
	}
	if (!EffectData->BaseEffectData.bIsDelayDestroyVisibility)
	{
		SetActorHiddenInGame(true);
	}
}

void AEffectEmitter::SetActorHiddenInGame(bool bNewHidden)
{
	Super::SetActorHiddenInGame(bNewHidden);
	///隐藏状态下设置为激活没有用，在刷新粒子的可见性时再次激活粒子
	if (!bNewHidden && bPlaying && !IsActive())
	{
		Activate();
	}
}

void AEffectEmitter::UpdateVisibilityData(bool bCreate)
{
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->ParticleManager))
	{
		return;
	}
	UParticleManager* ParticleManager = UUECS3GameInstance::Instance->ParticleManager;
	if (!bCreate)
	{
		ParticleManager->RemoveInvalidEffect(UID);
		return;
	}
	if (!ParticleManager->UEffectMap.Contains(UID))
	{
		return;
	}
	FInternal_EffectData& Data = ParticleManager->UEffectMap[UID];
	

//-------------------------添加------------------------------

	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	// 没有玩家的时候，一般为创建角色的时候，直接给类型
	if (!Player)
	{
		Data.LODType = LOD_TYPE::NEAR_DIS;
		Data.Type = PARTICLE_TYPE::TYPE_PARTICLE_SCENE;
		Data.bVisible = true;

		ParticleManager->CurrentParticleDisplayConfig.NEARCount[Data.Type] += 1;
		ParticleManager->CurrentParticleDisplayConfig.MaxCount += 1;
		return;
	}

	float Distance = (Player->CameraComponent->GetComponentLocation() - GetActorLocation()).Size();

	if (Distance < NEARDIS)
	{
		Data.LODType = LOD_TYPE::NEAR_DIS;
	}
	else if (Distance < FARDIS)
	{
		Data.LODType = LOD_TYPE::MIDDEL_DIS;
	}
	else
	{
		Data.LODType = LOD_TYPE::FAR_DIS;
	}
	
	AServerCharacter* FActor = Cast<AServerCharacter>(FirstTarget);
	AServerCharacter* SActor = Cast<AServerCharacter>(SecondTarget);

	// 本地玩家的宠物
	AActor* PetActor = Player->GetSelfEntity() ? Player->GetSelfEntity()->Actor() : nullptr;

	// 指定的目标是玩家或玩家的宠物
	if (SActor == Player || SActor == PetActor)
	{
		Data.Type = PARTICLE_TYPE::TYPE_PARTICLE_PLAYER;
	}

	// 指定的目标是其他玩家或者其他玩家的宠物
	else if (SActor && (SActor->IsA(APlayerCharacter::StaticClass()) || SActor->IsA(APetCharacter::StaticClass())))
	{
		Data.Type = PARTICLE_TYPE::TYPE_PARTICLE_OTHERPLAYER;
	}

	// 施法的是玩家
	else if (FActor == Player)
	{
		Data.Type = PARTICLE_TYPE::TYPE_PARTICLE_PIN;
	}

	// 施法的是其他玩家
	else if (FActor && FActor->IsA(APlayerCharacter::StaticClass()))
	{
		Data.Type = PARTICLE_TYPE::TYPE_PARTICLE_PIOP;
	}

	// 被施法的是客户端对象
	else if(SActor && SActor->IsA(AServerCharacter::StaticClass()))
	{
		Data.Type = PARTICLE_TYPE::TYPE_PARTICLE_NPC;
	}

	// 其他
	else
	{
		Data.Type = PARTICLE_TYPE::TYPE_PARTICLE_SCENE;
	}
	
	bool bVisible = false;

	// 添加粒子
	switch (Data.LODType)
	{
		case LOD_TYPE::NEAR_DIS:
			if (ParticleManager->ParticleDisplayConfig.NEARCount[Data.Type] >= ParticleManager->CurrentParticleDisplayConfig.NEARCount[Data.Type] + 1)
			{
				ParticleManager->CurrentParticleDisplayConfig.NEARCount[Data.Type] += 1;
				bVisible = true;
			}
			break;
		case LOD_TYPE::MIDDEL_DIS:
			if (ParticleManager->ParticleDisplayConfig.MIDDELCount[Data.Type] >= ParticleManager->CurrentParticleDisplayConfig.MIDDELCount[Data.Type] + 1)
			{
				ParticleManager->CurrentParticleDisplayConfig.MIDDELCount[Data.Type] += 1;
				bVisible = true;
			}
			break;
		case LOD_TYPE::FAR_DIS:
			if (ParticleManager->ParticleDisplayConfig.FARCount[Data.Type] >= ParticleManager->CurrentParticleDisplayConfig.FARCount[Data.Type] + 1)
			{
				ParticleManager->CurrentParticleDisplayConfig.FARCount[Data.Type] += 1;
				bVisible = true;
			}
			break;
		default:
			break;
	}
	
	if (ParticleManager->ParticleDisplayConfig.MaxCount < ParticleManager->CurrentParticleDisplayConfig.MaxCount + 1)
	{
		bVisible = false;
	}
	else
	{
		ParticleManager->CurrentParticleDisplayConfig.MaxCount += 1;
	}
	
	if (!bVisible)
	{
		switch (Data.LODType)
		{
			case LOD_TYPE::NEAR_DIS:
				ParticleManager->CurrentParticleDisplayConfig.NEARCount[Data.Type] -= 1;
				break;
			case LOD_TYPE::MIDDEL_DIS:
				ParticleManager->CurrentParticleDisplayConfig.MIDDELCount[Data.Type] -= 1;
				break;
			case LOD_TYPE::FAR_DIS:
				ParticleManager->CurrentParticleDisplayConfig.FARCount[Data.Type] -= 1;
				break;
		}
	}
		
	Data.bVisible = bVisible;

	//设置可见性
	if (!bVisible)
	{
		GetParticleSystemComponent()->SetVisibility(bVisible);
		if (STComponent)
		{
			STComponent->SetVisibility(bVisible);
		}
		if (SKComponent)
		{
			SKComponent->SetVisibility(bVisible);
		}
	}
}

void AEffectEmitter::SortEffect()
{
	if (UUECS3GameInstance::Instance->ParticleManager->IsNeedSort(UID))
	{
		APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		if (Player)
		{
			UUECS3GameInstance::Instance->ParticleManager->SortEffect(Player->CameraComponent->GetComponentLocation(),
				Player->CameraComponent->GetComponentRotation());
		}
	}
}

void AEffectEmitter::AddModule(class UParticleModule* ParticleModule, int32 EmitterIndex, int32 LODIndex)
{
	ModuleLODData Data;
	Data.EmitterIndex = EmitterIndex;
	Data.LODIndex = LODIndex;
	ModuleList.Add(ParticleModule, Data);
	UUECS3GameInstance::Instance->ParticleManager->AddModule(ParticleModule);
}

void AEffectEmitter::RemoveModule()
{
	UParticleLODLevel* CurLevel;
	for (auto Module : ModuleList)
	{
		if (UUECS3GameInstance::Instance->ParticleManager->RemoveModule(Module.Key))
		{
			CurLevel = GetParticleSystemComponent()->Template->Emitters[Module.Value.EmitterIndex]->LODLevels[Module.Value.LODIndex];
			if (CurLevel->Modules.Num())
			{
				CurLevel->Modules.RemoveAt(CurLevel->Modules.Num() - 1);
				CurLevel->SpawnModules.RemoveAt(CurLevel->SpawnModules.Num() - 1);
				CurLevel->UpdateModules.RemoveAt(CurLevel->UpdateModules.Num() - 1);
			}
		}
	}
}

int32 AEffectEmitter::GetEntityID(AActor* Actor)
{
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
	if (!ServerCharacter)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AEffectEmitter::GetEntityID : ServerCharacter!"));
		return 0;
	}

	return ServerCharacter->EntityId;
}

void AEffectEmitter::AddBulletMsgBegin(KBEngine::FVariantArray* args, AActor* Actor)
{
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
	if (!IsValid(ServerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:AEffectEmitter::AddBulletMsgBegin : ServerCharacter!"));
		return;
	}
	args->Add(INT_TO_FSTRING(BulletBuffOwnerId));
	args->Add(INT_TO_FSTRING(BulletBuffIndex));
	if (BulletBuffProxyId == -1 && UGolbalBPFunctionLibrary::GetCS3PlayerCharacter() == ServerCharacter)
	{
		args->Add(INT_TO_FSTRING(UGolbalBPFunctionLibrary::GetPlayerID()));
	}
	else if (BulletBuffProxyId == UGolbalBPFunctionLibrary::GetPlayerID())
	{
		args->Add(INT_TO_FSTRING(ServerCharacter->EntityId));
	}
	args->Add(ID);
	args->Add(INT_TO_FSTRING(BulletBuffEffectIndex));
	args->Add(INT_TO_FSTRING(BulletBuffEffectCustomIndex));
}

void AEffectEmitter::TranceBulletEvent()
{
	
	FVector Star = GetParticleSystemComponent()->GetComponentLocation();
	FVector End = Star + (this->GetActorForwardVector() * 2);
	FVector HalfSize = this->EffectEmitterData->CollisionResponse[0].HalfSize;
	FVector HalfRotator = this->EffectEmitterData->CollisionResponse[0].HalfRotator;
	
	FRotator Orientation = FRotator(HalfRotator.X, HalfRotator.Y, HalfRotator.Z)+ this->GetActorRotation();
	TArray<AActor*> ActorsToIgnore ;
	EDrawDebugTrace::Type DrawDebugType = EDrawDebugTrace::Type::None;
	if (this->EffectEmitterData->CollisionResponse[0].bIsDebug)
	{
		DrawDebugType = EDrawDebugTrace::Type::ForDuration;
	}
	TArray<FHitResult> OutHits;

	bool bIsSuccess = UKismetSystemLibrary::BoxTraceMulti(this, Star, End, HalfSize, Orientation, ETraceTypeQuery::TraceTypeQuery1,false, ActorsToIgnore, DrawDebugType, OutHits,true);
	if (bIsSuccess)
	{
		bool isAOther= false;
		FHitResult OutvalHit;
		for (FHitResult Outval : OutHits)
		{
			for (TSubclassOf<AActor> val : this->EffectEmitterData->CollisionResponse[0].ActorsToIgnore)
			{
				if (!IsValid(Outval.GetActor()))
					continue;
				if (!IsValid(val))
					continue;
				if (Outval.GetActor()->IsA(val))
				{
					isAOther = true;
					return;
				}
			}
			OutvalHit = Outval;
		}
		if (!isAOther)
		{
			FVector HitLocation = OutvalHit.Location;
			// 调用服务器方法
			KBEngine::FVariantArray args;
			KBEngine::Entity* Player = UUECS3GameInstance::pKBEApp->Player();
			CS3Entity* pEntity_Player = (CS3Entity*)(Player);
			if (pEntity_Player && pEntity_Player->IsPlayerRole())
			{
				args.Add(INT_TO_FSTRING(BulletBuffOwnerId));
				args.Add(INT_TO_FSTRING(BulletBuffIndex));
				args.Add(HitLocation);
				args.Add(ID);
				args.Add(INT_TO_FSTRING(BulletBuffEffectIndex));
				args.Add(INT_TO_FSTRING(BulletBuffEffectCustomIndex));
				// 如果不是子弹Buff，并且碰撞的对象是玩家且不是本地玩家，就不发送
				pEntity_Player->CellCall("onBulletCollisionPosBegin", args);
			}
			if (IsValid(UUECS3GameInstance::Instance))
			{
				if (BulletBuffEventHandle.IsValid())
				{
					UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(BulletBuffEventHandle);
				}
			}
			///CST-10306 - 程序功能需求——尸体，旗帜，箭矢残留效果
			if (EffectEmitterData->EffectData.FlyData.MotionBlurMeshAsset.Get())
			{
				if (AGameCharacter* CollisionActor = Cast<AGameCharacter>(OutvalHit.Actor))
				{
					APoseableBlur* BlurMesh = UMotionBlurManager::GetInstance()->CreateBlurMeshesDirect(MotionBlurComponent, EffectEmitterData->EffectData.FlyData.bIsMotionBlurTime,nullptr,false);
					if (IsValid(BlurMesh))
					{
						BlurMesh->AttachToComponent(CollisionActor->GetCapsuleComponent(), FAttachmentTransformRules::KeepWorldTransform);
					}
				}
				else
				{
					UMotionBlurManager::GetInstance()->CreateBlurMeshes(MotionBlurComponent, EffectEmitterData->EffectData.FlyData.bIsMotionBlurTime);
				}

			}
			Stop();
		}
	}
}

bool AEffectEmitter::IsPlaying()
{ 
	return bPlaying;
}

FString AEffectEmitter::GetEffectID()
{ 
	return ID;
}

float AEffectEmitter::GetInitAlpha()
{ 
	return EffectEmitterData->ParticleData.InitAlpha;
}

float AEffectEmitter::GetAlpha()
{ 
	return Alpha; 
}

bool AEffectEmitter::IsGraduallyHidden()
{
	return EffectEmitterData->ParticleData.bGraduallyHidden;
}

bool AEffectEmitter::IsUseConstAlpha()
{
	return EffectEmitterData->ParticleData.bUseConstAlpha;
}

int32 AEffectEmitter::GetSortIndex()
{
	return EffectEmitterData->ParticleData.SortIndex;
}

void AEffectEmitter::GetBaseParticleLocationAndRotation_Implementation(const FVector& Location, const FRotator& Rotation, int32 MoudelIndex, int32 BaseParticleIndex, bool bTrace, const FVector& ImpactPoint, UParticleSystem* Template)
{

}

void AEffectEmitter::ParticleUpdateLoopEnd_Implementation()
{

}

CONTROL_COMPILE_OPTIMIZE_END
