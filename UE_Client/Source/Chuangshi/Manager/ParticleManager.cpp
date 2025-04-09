// Fill out your copyright notice in the Description page of Project Settings.


#include "ParticleManager.h"
// UE4类型
#include "Particles/ParticleModule.h"
#include "GameDelegates.h"
#include "Sound/SoundBase.h"
#include "Kismet/GameplayStatics.h"
// CS3类型
#include"Chuangshi.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CfgManager.h"
#include "Manager/ResourceManager.h"
#include "Actor/ServerCharacter.h"
#include "Actor/Particle/EffectEmitter.h"
#include "Actor/Particle/FlyEffectEmitter.h"
#include "Particles/Emitter.h"
#include "Sound/SoundBase.h"
#include "Particles/ParticleSystemComponent.h"
#include "Kismet/GameplayStatics.h"

///<一帧创建的最大粒子数量
#define MaxCreateCount 100
///<简单粒子最大缓存数量
#define MaxSimpleCacheCount 500	
///<飞行粒子最大缓存数量
#define MaxFlyCacheCount 50

CONTROL_COMPILE_OPTIMIZE_START

static int32 GEnableParticleSystem = 1;
static FAutoConsoleVariableRef ParticleSystemSwitch(
	TEXT("GEnableParticleSystem"),
	GEnableParticleSystem,
	TEXT("if true enable particle system.\n"),
	ECVF_Default
);

UParticleManager* UParticleManager::GetInstance()
{
	cs3_checkNoReentry();
	//预加载数据

	UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PARTICLE);
	UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PARTICLE_TEST);
	UParticleManager* Instacne = (UParticleManager*)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_ParticleManager")));
	Instacne->Init();
	return Instacne;
}

void UParticleManager::Init()
{
	BP_SimpleEffect = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SimpleEffect"));
	BP_FlyEffect = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_FlyEffect"));
	// 绑定地图结束和切换地图事件
	FGameDelegates::Get().GetEndPlayMapDelegate().AddUObject(this, &UParticleManager::OnEndPlayMap);
	FCoreUObjectDelegates::PreLoadMap.AddUObject(this, &UParticleManager::OnPreLoadMap);
}

void UParticleManager::Tick(float DeltaTime)
{
	// 有默认对象的存在，判断下是不是游戏实例中的管理器对象
	if (this != UGolbalBPFunctionLibrary::ParticleManager())
	{
		return;
	}
	// 清空上一帧创建计数
	CurrentTickCreateEffect = 0;

	// 延迟创建
	DeferSpawnEmitter(DeltaTime);
}

void UParticleManager::DeferSpawnEmitter(float DeltaTime)
{
	// 默认返回
	if (CahceType == ParticleCacheType::Default)
	{
		return;
	}
	// 帧数不够返回
	int32 Count = 0;
	if (DeltaTime < 0.02f)
	{
		Count = 2;
	}
	else if (DeltaTime < 0.025f)
	{
		Count = 1;
	}
	else
	{
		return;
	}

	FTransform Transform = FTransform();
	AEffectEmitter* Emitter = nullptr;
	UClass* CurrentClass = nullptr;

	// 缓存光效对象
	if (CahceType == ParticleCacheType::SimpleEffect)
	{
		CurrentClass = BP_SimpleEffect;
	}
	else
	{
		CurrentClass = BP_FlyEffect;
	}

	for (size_t i = 0; i < Count; i++)
	{
		Emitter = Cast<AEffectEmitter>(UGolbalBPFunctionLibrary::BeginDeferredActorSpawnFromClass(CurrentClass, Transform));
		if (Emitter)
		{
			ParticleDeferSpawnPool.Add(Emitter);
		}
	}

	int32 BufferPoolSize = ParticleBufferPool.Num();
	int32 DeferPoolSize = ParticleDeferSpawnPool.Num();

	// 缓存已满就不缓存了
	if (CahceType == ParticleCacheType::SimpleEffect && DeferPoolSize + BufferPoolSize >= MaxSimpleCacheCount)
	{
		CahceType = ParticleCacheType::Default;
	}
	else if (CahceType == ParticleCacheType::FlyEffect && DeferPoolSize >= MaxFlyCacheCount)
	{
		CahceType = ParticleCacheType::Default;
	}
}

void UParticleManager::OnEndPlayMap()
{
	// 每次切换地图时清理数据
	for (auto Emitter : ParticleDeferSpawnPool)
	{
		Emitter->RemoveFromRoot();
	}
	ParticleDeferSpawnPool.Empty();
	ParticleBufferPool.Empty();

	for (auto Asset : EmitterPreLoadAssetList)
	{
		Asset->RemoveFromRoot();
	}
	EmitterPreLoadAssetList.Empty();
}

void UParticleManager::OnPreLoadMap(const FString& Level)
{
	OnEndPlayMap();
	// 重置状态，又要开始预加载了
	CahceType = ParticleCacheType::SimpleEffect;
	// 预加载粒子资源
	UpdatePreLoadAsset(Level);
}

void UParticleManager::UpdatePreLoadAsset(const FString& Level)
{
	// 获取逻辑关卡的名字
	FString LevelName = UGolbalBPFunctionLibrary::SplitString(Level, false, "/").Pop();
	if (LevelName.IsEmpty())
	{
		return;
	}

	// 读取本地图预加载资源
	if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager)
	{
		auto EffectTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_EFFECT_PRELOAD_DATA);
		const FEFFECT_PRELOAD_DATA* PreloadData = EffectTable->GetRow<FEFFECT_PRELOAD_DATA>(LevelName);
		if (!PreloadData)
		{
			return;
		}

		// 预加载资源
		for (auto EffectID: PreloadData->PreLoadList)
		{
			LoadParticleAsset(EffectID);
		}
	}
}

void UParticleManager::UpdateParticleDiaplayConfig(FVIDEOSETTING_DATA& Data)
{
	if (CurrentSetting == Data.ScreenPercentage)
	{
		return;
	}
	// 设置当前状态
	CurrentSetting = Data.ScreenPercentage;
	// 更新粒子规则图
	UpdateParticleDisplayConfig();
}

int32 UParticleManager::PlayParticle(const FString& EffectID, const float EffectSendAngle, AActor* Target1, AActor* Target2, FEffectCreate OnComplete/* = nullptr*/)
{
	if (!GEnableParticleSystem)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("The Particle System is down"));
		return EffectUID++;
	}

	const FEFFECT_EMITTER_DATA* EffectEmitterData = GetEffectData(EffectID);

	if (EffectEmitterData)
	{
		//获取光效数据成功，在光效管理器中创建此粒子的唯一标记
		UEffectMap.Add(EffectUID, FInternal_EffectData(EffectID));
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Particle ID named %d have been added"), EffectUID);

		//获取要加载的资源路径
		TArray<TSoftObjectPtr<UObject>> AssetArr;
		AssetArr.Add(EffectEmitterData->ParticleData.ParticleSystemAsset);
		AssetArr.Add(EffectEmitterData->SkeletalMesh.SkeletalMeshAsset);
		for (auto Asset : EffectEmitterData->SkeletalMesh.AnimAssetList)
		{
			AssetArr.Add(Asset);
		}
		AssetArr.Add(EffectEmitterData->StaticMesh.StaticMeshAsset);
		AssetArr.Add(EffectEmitterData->Audio.AudioAsset);

		//添加要加载的资源
		TArray<FStringAssetReference> AssetReferenceArr;
		for (TSoftObjectPtr<UObject> Ass : AssetArr)
		{
			if (Ass.ToSoftObjectPath().IsValid())
			{
				AssetReferenceArr.Add(Ass.ToSoftObjectPath());
			}
		}

		AssetReferenceArr.Add(EffectEmitterData->Spline.SplineAsset.ToSoftObjectPath());
		AssetReferenceArr.Add(EffectEmitterData->EffectInstance.ToSoftObjectPath());
		//加载资源
		TWeakObjectPtr<AActor> DelayTarget1Ptr(Target1);
		TWeakObjectPtr<AActor> DelayTarget2Ptr(Target2);
		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, AssetReferenceArr,
			FStreamableDelegate::CreateLambda([this, EffectSendAngle, EffectEmitterData, DelayTarget1Ptr, DelayTarget2Ptr, OnComplete, EffectID, UID = EffectUID]()
		{
			this->SpawnParticle(DelayTarget1Ptr, DelayTarget2Ptr, OnComplete, EffectID, UID, EffectSendAngle, EffectEmitterData);

		}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_EFFECT);

		return EffectUID++;
	}
	else
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("EffectID : the effect %s none config data in EffectConfig"), *EffectID);
	}
	return EffectUID++;
}

void UParticleManager::SpawnParticle(TWeakObjectPtr<AActor> DelayTarget1Ptr, TWeakObjectPtr<AActor> DelayTarget2Ptr, FEffectCreate OnComplete,
	FString EffectID, int32 UID, float EffectSendAngle, const FEFFECT_EMITTER_DATA* EffectEmitterData)
{
	if (CurrentTickCreateEffect >= MaxCreateCount)
	{
		GetWorld()->GetTimerManager().SetTimerForNextTick(FTimerDelegate::CreateLambda([this, EffectSendAngle, EffectEmitterData, DelayTarget1Ptr, DelayTarget2Ptr, OnComplete, EffectID, UID]
		{
			this->SpawnParticle(DelayTarget1Ptr, DelayTarget2Ptr, OnComplete, EffectID, UID, EffectSendAngle, EffectEmitterData);
		}));

		CS3_Display(CS3DebugType::CL_Undefined, TEXT("The number of spwan-particle more than MaxCreateCount, Create it next frame"));
		return;
	}
	
	// 判断下对象是否有效或者等待被销毁
	if (!DelayTarget1Ptr.IsValid() || !DelayTarget2Ptr.IsValid())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("The particle release target is invalid, EffectID:"), *EffectID);
		RemoveInvalidEffect(UID);
		return;
	}

	// 判断光效是否已经被销毁
	if (!UEffectMap[UID].bIsValid)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("The particle has been destroyed before it is created, EffectID:"), *EffectID);
		RemoveInvalidEffect(UID);
		return;
	}

	// 每一帧创建粒子计数
	CurrentTickCreateEffect++;

	AEffectEmitter* Effect = nullptr;
	
	// 延迟创建标志
	bool bDefer = true;

	// 当取缓存标志为Simple的时候，预缓冲池肯定是有对象的
	if (EffectEmitterData->EffectInstance.Get() == BP_SimpleEffect)
	{
		if (GetType == ParticleCacheType::SimpleEffect)
		{
			if (ParticleDeferSpawnPool.Num() > 0)
			{
				Effect = ParticleDeferSpawnPool.Pop();
			}
			else if (ParticleBufferPool.Num() > 0)
			{		
				while ( ParticleBufferPool.Num() > 0 )
				{
					Effect = ParticleBufferPool.Pop();
					if (!IsValid(Effect) || Effect->IsPendingKillPending() || Effect->HasAnyFlags(RF_BeginDestroyed))
					{
						Effect = nullptr;
						continue;
					}
					bDefer = false;
					break;
				}
			}
			// 设置缓存状态和取缓存状态
			if (ParticleDeferSpawnPool.Num() + ParticleBufferPool.Num() < MaxSimpleCacheCount)
			{
				CahceType = ParticleCacheType::SimpleEffect;
			}
			else if (ParticleDeferSpawnPool.Num() == 0)
			{
				CahceType = GetType = ParticleCacheType::FlyEffect;
			}
		}
		else
		{
			if (ParticleBufferPool.Num() > 0)
			{
				bDefer = false;
				Effect = ParticleBufferPool.Pop();
			}
		}
	}
	else if (GetType == ParticleCacheType::FlyEffect && EffectEmitterData->EffectInstance.Get() == BP_FlyEffect)
	{
		if (ParticleDeferSpawnPool.Num() > 0)
		{
			Effect = ParticleDeferSpawnPool.Pop();
			// 重置缓存状态
			CahceType = ParticleCacheType::FlyEffect;
		}
	}

	FTransform Transform = FTransform();

	// DeferredSpawn
	if (!Effect)
	{
		if (!EffectEmitterData->EffectInstance.IsValid())
		{
			CS3_Warning(TEXT("EffectInstance is none, EffectID:"), *EffectID);
			return;
		}
		Effect = Cast<AEffectEmitter>(UGolbalBPFunctionLibrary::BeginDeferredActorSpawnFromClass(EffectEmitterData->EffectInstance.Get(), Transform));
	}
	
	AActor* Target1Ptr = DelayTarget1Ptr.Get();
	AActor* Target2Ptr = DelayTarget2Ptr.Get();

	// 延迟创建初始化
	if (bDefer)
	{
		// 在BeginPlay之前初始化一些必要的数据
		Effect->InitBeforeBeginPlay(EffectID, UID, Target1Ptr, Target2Ptr, EffectSendAngle, EffectEmitterData, (void*)&OnComplete);
		UGameplayStatics::FinishSpawningActor(Effect, Transform);
	}
	// 缓存创建，调用正常流程方法
	else
	{
		Effect->GetParticleSystemComponent()->SetComponentTickEnabled(true);
		Effect->InitBeforeBeginPlay(EffectID, UID, Target1Ptr, Target2Ptr, EffectSendAngle, EffectEmitterData, (void*)&OnComplete);
		Effect->PrepareData();
	}
}

AEffectEmitter* UParticleManager::PlayParticleOfEdit(const FName& EffectID, AActor* Target)
{
	if (!Target)
	{
		return nullptr;
	}

	const FEFFECT_EMITTER_DATA* EffectEmitterData = GetEffectData(FNAME_TO_FSTRING(EffectID));

	if (EffectEmitterData)
	{
		//获取要加载的资源路径
		TArray<TSoftObjectPtr<UObject>> AssetArr;
		AssetArr.Add(EffectEmitterData->ParticleData.ParticleSystemAsset);
		if (EffectEmitterData->SkeletalMesh.AnimAssetList.Num())
		{
			AssetArr.Add(EffectEmitterData->SkeletalMesh.AnimAssetList[0]);
		}
		AssetArr.Add(EffectEmitterData->SkeletalMesh.SkeletalMeshAsset);
		AssetArr.Add(EffectEmitterData->StaticMesh.StaticMeshAsset);
		
		TArray<FStringAssetReference> AssetReferenceArr;

		//添加要加载的资源
		for (TSoftObjectPtr<UObject> Ass : AssetArr)
		{
			if (Ass.ToSoftObjectPath().IsValid() && !IsValid(Ass.Get()))
			{
				AssetReferenceArr.Add(Ass.ToSoftObjectPath());
			}
		}
		AssetReferenceArr.Add(EffectEmitterData->EffectInstance.ToSoftObjectPath());

		FActorSpawnParameters SpawnParameters;
		SpawnParameters.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		SpawnParameters.bAllowDuringConstructionScript = true;
		AEffectEmitter* Effect = Cast<AEffectEmitter>(Target->GetWorld()->SpawnActor(EffectEmitterData->EffectInstance.Get(), nullptr, nullptr, SpawnParameters));

		if (AssetReferenceArr.Num())
		{
			//加载资源
			FStreamableManager StreamManager;
			for (auto Asset : AssetReferenceArr)
			{
				StreamManager.LoadSynchronous(Asset);
			}
		}

		//加载完毕后设置到组件
		if (Effect)
		{
			//设置及初始化
			Effect->InitBeforeBeginPlay(FNAME_TO_FSTRING(EffectID), 0, Target, Target, 0, EffectEmitterData, nullptr);
			Effect->InitFromConfig();
			Effect->InitEmitterTransform();
#if WITH_EDITOR
			Effect->bIsInEdit = true;
#endif // WITH_EDITOR
			Effect->Play();
			return Effect;
		}
	}
	else
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("EffectID : the effect is none config data in EffectConfig"));
	}

	return nullptr;
}

const FEFFECT_EMITTER_DATA* UParticleManager::GetEffectData(const FString& EffectID)
{
	// 获取配置数据
	const FEFFECT_EMITTER_DATA* EffectData = nullptr;
	if (UUECS3GameInstance::Instance)
	{
		auto EffectTestTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PARTICLE_TEST);
		EffectData = EffectTestTable->GetRow<FEFFECT_EMITTER_DATA>(EffectID);
		if (EffectData == nullptr)
		{
			auto EffectTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PARTICLE);
			EffectData = EffectTable->GetRow<FEFFECT_EMITTER_DATA>(EffectID);
		}
	}
#if WITH_EDITOR
	else
	{
		// 编辑器粒子
		FStreamableManager StreamManager;
		auto EffectTestTable = (UDataTable*)StreamManager.LoadSynchronous(FSoftObjectPath(*FString("DataTable'/Game/Miscs/ContentConfig/Effect/DT_EffectCfg_Test.DT_EffectCfg_Test'")));
		auto EffectTable = (UDataTable*)StreamManager.LoadSynchronous(FSoftObjectPath(*FString("DataTable'/Game/Miscs/ContentConfig/Effect/DT_EffectCfg.DT_EffectCfg'")));

		if (EffectTestTable)
		{
			FName ID = FSTRING_TO_FNAME(EffectID);
			for (auto Row : EffectTestTable->GetRowMap())
			{
				if (ID == Row.Key)
				{
					EffectData = (const FEFFECT_EMITTER_DATA*)Row.Value;
					break;
				}
			}
		}
		if (EffectTable && EffectData == nullptr)
		{
			FName ID = FSTRING_TO_FNAME(EffectID);
			for (auto Row : EffectTable->GetRowMap())
			{
				if (ID == Row.Key)
				{
					EffectData = (const FEFFECT_EMITTER_DATA*)Row.Value;
					break;
				}
			}
		}
	}
#endif //  WITH_EDITOR

	return EffectData;

}

void UParticleManager::Stop(AEffectEmitter * Effect, bool notDelay /*= false*/, bool notDelayDestroyChildren /*= false*/, bool bPlayDeathParticle /*= true*/, bool bAddParticleBufferPool /*= true*/)
{
	Effect->Stop(notDelay, notDelayDestroyChildren, bPlayDeathParticle, bAddParticleBufferPool);
}

void UParticleManager::StopEffectByID(FString EffectID)
{
	for (TMap<int32, FInternal_EffectData>::TIterator TBegin = UEffectMap.CreateIterator(); TBegin; ++TBegin)
	{
		if (TBegin.Value().EffectID == EffectID)
		{
			if (IsValid(TBegin.Value().Owner))
			{
				TBegin.Value().Owner->Stop();
			}
		}
	}
}

void UParticleManager::Hide(AEffectEmitter* Effect)
{
	Effect->SetActorHiddenInGame(true);
}

void UParticleManager::HideByID(FString EffectID)
{
	for (TMap<int32, FInternal_EffectData>::TIterator TBegin = UEffectMap.CreateIterator(); TBegin; ++TBegin)
	{
		if (TBegin.Value().EffectID == EffectID)
		{
			if (IsValid(TBegin.Value().Owner))
			{
				TBegin.Value().Owner->SetActorHiddenInGame(true);
			}
		}
	}
}

void UParticleManager::HideByUID(int32 UID)
{
	FInternal_EffectData* EffectData = UEffectMap.Find(UID);

	if (EffectData != nullptr)
	{
		if (IsValid(EffectData->Owner))
		{
			EffectData->Owner->SetActorHiddenInGame(true);
		}
	}
}


void UParticleManager::ShowByUID(int32 UID)
{
	FInternal_EffectData* EffectData = UEffectMap.Find(UID);

	if (EffectData != nullptr)
	{
		if (IsValid(EffectData->Owner))
		{
			EffectData->Owner->SetActorHiddenInGame(false);
		}
	}
}

void UParticleManager::SetVisiableByActor(AActor* Parent, bool visible)
{
	for (TMap<int32, FInternal_EffectData>::TIterator TBegin = UEffectMap.CreateIterator(); TBegin; ++TBegin)
	{
		if (TBegin.Value().Parent == Parent && IsValid(TBegin.Value().Parent))
		{
			if (IsValid(TBegin.Value().Owner) && TBegin.Value().Owner->EffectData->BaseEffectData.bIsBindingVisibility)
			{
				TBegin.Value().Owner->SetActorHiddenInGame(!visible);
			}
		}
	}
}

void UParticleManager::StopEffectByUID(int32 UID, bool notDelay /*= false*/, bool notDelayDestroyChildren /*= false*/, bool bPlayDeathParticle/* = true*/, bool bAddParticleBufferPool/* = true*/)
{
	//我们只管停播，移除列表的事情交由光效自己处理
	FInternal_EffectData* EffectData = UEffectMap.Find(UID);

	if (EffectData != nullptr)
	{
		if (IsValid(EffectData->Owner))
		{
			EffectData->Owner->Stop(notDelay, notDelayDestroyChildren, bPlayDeathParticle, bAddParticleBufferPool);
		}
		else
		{
			EffectData->bIsValid = false;
		}
	}
}


void UParticleManager::SetEffectValidByID(int32 UID, bool bIsValid)
{
	FInternal_EffectData* EffectData = UEffectMap.Find(UID);

	if (EffectData != nullptr)
	{
		EffectData->bIsValid = bIsValid;
	}
}

FString UParticleManager::FindEffectIDByUID(int32 UID)
{
	FInternal_EffectData* EffectData = UEffectMap.Find(UID);

	if (UID > 0)
	{
		ensureMsgf(EffectData != nullptr, TEXT("The particle named %d was no found"), UID);
	}

	if (EffectData != nullptr)
	{
		return EffectData->EffectID;
	}
	return "";
}

AActor* UParticleManager::FindEmitterByUID(int32 UID)
{
	FInternal_EffectData* EffectData = UEffectMap.Find(UID);

	if (EffectData != nullptr)
	{
		if (IsValid(EffectData->Owner))
		{
			return EffectData->Owner;
		}
	}

	return nullptr;
}

void UParticleManager::UpdateParticleDisplayConfig_Implementation()
{
	// 蓝图实现
}

void UParticleManager::AddToSortList(int32 UID)
{
	if (!UEffectMap.Contains(UID))
	{
		return;
	}

	SortList.Add(UID);
	SortList.Sort([this](const int32 UID1,const int32 UID2)
	{
		return UEffectMap[UID1].Owner->GetSortIndex() > UEffectMap[UID2].Owner->GetSortIndex();
	});
}

void UParticleManager::RemoveToSortList(int32 UID)
{
	SortList.Remove(UID);
	if (!SortList.Num())
	{
		ResetSort();
	}
}

bool UParticleManager::IsNeedSort(int32 UID)
{
	if (SortList.Num())
	{
		return SortList[0] == UID;
	}

	return false;
}

void UParticleManager::SortEffect(const FVector& CameraLocation, const FRotator CameraRotation)
{
	if (!SortList.Num())
	{
		return;
	}

	//摄像机前面的粒子
	TArray<AEffectEmitter*> FNormalEffect;
	//摄像机后面的粒子
	TArray<AEffectEmitter*> BNormalEffect;
	//排序的粒子
	TArray<AEffectEmitter*> SortEffect;
	//位置
	FVector Location;
	UParticleSystemComponent* ParticleSystemComponent;

	for (auto it = UEffectMap.CreateIterator(); it; ++it)
	{
		// 可能粒子还在加载
		if (!IsValid(it.Value().Owner))
		{
			continue;
		}

		ParticleSystemComponent = it.Value().Owner->GetParticleSystemComponent();
		if (IsValid(ParticleSystemComponent))
		{
			continue;
		}
		Location = FTransform(CameraRotation.Quaternion(), CameraLocation, FVector(1.f)).InverseTransformPosition(ParticleSystemComponent->GetComponentLocation());

		if (it.Value().Owner->GetSortIndex() > 0)
		{
			// 判断盒子在相机前
			if (Location.X > 0)
			{
				SortEffect.Add(it.Value().Owner);
			}
			// 相机在粒子的包围盒内
			else
			{
				Location = ParticleSystemComponent->GetComponentTransform().InverseTransformPosition(CameraLocation);
				if (FMath::Abs(Location.X) < ParticleSystemComponent->Bounds.BoxExtent.X &&
					FMath::Abs(Location.Y) < ParticleSystemComponent->Bounds.BoxExtent.Y &&
					FMath::Abs(Location.Z) < ParticleSystemComponent->Bounds.BoxExtent.Z)
				{
					SortEffect.Add(it.Value().Owner);
				}
			}
		}
		else
		{
			if (Location.X > 0)
			{
				FNormalEffect.Add(it.Value().Owner);
			}
			else
			{
				BNormalEffect.Add(it.Value().Owner);
			}
		}
	}
	// 按自定义的属性排序
	SortEffect.Sort([](AEffectEmitter& Effect1, AEffectEmitter& Effect2)
	{
		return Effect1.GetSortIndex() > Effect2.GetSortIndex();
	});
	// 按距离排序
	FNormalEffect.Sort([CameraLocation](AEffectEmitter& Effect1, AEffectEmitter& Effect2)
	{
		return (Effect1.GetParticleSystemComponent()->GetComponentLocation() - CameraLocation).Size() >
			(Effect2.GetParticleSystemComponent()->GetComponentLocation() - CameraLocation).Size();
	});
	// 按距离排序
	BNormalEffect.Sort([CameraLocation](AEffectEmitter& Effect1, AEffectEmitter& Effect2)
	{
		return (Effect1.GetParticleSystemComponent()->GetComponentLocation() - CameraLocation).Size() <
			(Effect2.GetParticleSystemComponent()->GetComponentLocation() - CameraLocation).Size();
	});

	// 摄像机后面的排序
	int32 Total = BNormalEffect.Num() + FNormalEffect.Num() + SortEffect.Num();
	for (int32 i = 0; i < BNormalEffect.Num(); i++)
	{
		BNormalEffect[i]->GetParticleSystemComponent()->SetTranslucentSortPriority(Total);
	}

	float Distance = (UEffectMap[SortList[0]].Owner->GetParticleSystemComponent()->GetComponentLocation() - CameraLocation).Size();

	// 摄像机前面的和需要范围排序的排序
	int32 Count = 0;
	for (int32 i = 0; i < FNormalEffect.Num(); i++)
	{
		if ((FNormalEffect[i]->GetParticleSystemComponent()->GetComponentLocation() - CameraLocation ).Size()< Distance)
		{
			FNormalEffect[i]->GetParticleSystemComponent()->SetTranslucentSortPriority(Total);
		}
		// 中断排序，因为距离已经到要遮蔽的粒子了
		else
		{
			Count = i;
			break;
		}
	}

	// 需要排序的粒子开始排序
	for (int32 i = 0; i < SortEffect.Num(); i++)
	{
		SortEffect[i]->GetParticleSystemComponent()->SetTranslucentSortPriority(FNormalEffect.Num() + SortEffect.Num() - Count - i);
	}

	// 需要排序的粒子开始排序
	for (int32 i = Count; i < FNormalEffect.Num(); i++)
	{
		FNormalEffect[i]->GetParticleSystemComponent()->SetTranslucentSortPriority(0);
	}


	///获取粒子视锥体的大小

	/*********************************************/
	//		 /-------------------/
	//		/					/|	粒子包围盒
	//     /				   / |
	//    /					  /  |
	//	 |--------------------|	 |
	//	 |		粒子		  |  /
	//	 |					  | /
	//	 |--------------------|/
	//   
	//									·相机点
	//
	//
	/*********************************************/
}

void UParticleManager::ResetSort()
{
	for (auto it = UEffectMap.CreateIterator(); it; ++it)
	{
		if (it.Value().Owner)
		{
			it.Value().Owner->GetParticleSystemComponent()->SetTranslucentSortPriority(0);
		}
	}
}

void UParticleManager::AddModule(UParticleModule* ParticleModule)
{
	if (ModuleMap.Contains(ParticleModule))
	{
		ModuleMap[ParticleModule] += 1;
	}
	else
	{
		ModuleMap.Add(ParticleModule, 1);
		ParticleModule->AddToRoot();
	}
}

bool UParticleManager::RemoveModule(UParticleModule* ParticleModule)
{
	if(ModuleMap.Contains(ParticleModule))
	{
		ModuleMap[ParticleModule] -= 1;
		if (ModuleMap[ParticleModule] == 0)
		{
			ModuleMap.Remove(ParticleModule);
			ParticleModule->RemoveFromRoot();
			return true;
		}
	}

	return false;
}

AActor* UParticleManager::GetWorldSetting()
{
	if (GetWorld())
	{
		GetWorld()->GetWorldSettings();
	}

	return nullptr;
}


void UParticleManager::RemoveInvalidEffect(int32 UID)
{
	if (!UEffectMap.Contains(UID))
	{
		return;
	}
	FInternal_EffectData& Data = UEffectMap[UID];
	//-------------------------移除------------------------------
	// 只有显示的算进去
	if (Data.bVisible)
	{
		// 移除粒子
		switch (Data.LODType)
		{
		case LOD_TYPE::NEAR_DIS:
			if (CurrentParticleDisplayConfig.NEARCount.Contains(Data.Type))
			{
				CurrentParticleDisplayConfig.NEARCount[Data.Type] -= 1;
			}			
			break;
		case LOD_TYPE::MIDDEL_DIS:
			if (CurrentParticleDisplayConfig.MIDDELCount.Contains(Data.Type))
			{
				CurrentParticleDisplayConfig.MIDDELCount[Data.Type] -= 1;
			}
			break;
		case LOD_TYPE::FAR_DIS:
			if (CurrentParticleDisplayConfig.FARCount.Contains(Data.Type))
			{
				CurrentParticleDisplayConfig.FARCount[Data.Type] -= 1;
			}			
			break;
		default:
			break;
		}
		CurrentParticleDisplayConfig.MaxCount -= 1;
	}
	UEffectMap.Remove(UID);
}

void UParticleManager::LoadParticleAsset(FString EffectID)
{
	const FEFFECT_EMITTER_DATA* EffectEmitterData = GetEffectData(EffectID);
	if (!EffectEmitterData)
	{
		return;
	}

	TArray<TSoftObjectPtr<UObject>> AssetArr;
	AssetArr.Add(EffectEmitterData->ParticleData.ParticleSystemAsset);
	AssetArr.Add(EffectEmitterData->SkeletalMesh.SkeletalMeshAsset);
	for (auto Asset : EffectEmitterData->SkeletalMesh.AnimAssetList)
	{
		AssetArr.Add(Asset);
	}
	AssetArr.Add(EffectEmitterData->StaticMesh.StaticMeshAsset);
	AssetArr.Add(EffectEmitterData->Audio.AudioAsset);

	//添加要加载的资源
	TArray<FStringAssetReference> AssetReferenceArr;
	for (TSoftObjectPtr<UObject> Ass : AssetArr)
	{
		if (Ass.ToSoftObjectPath().IsValid())
		{
			AssetReferenceArr.Add(Ass.ToSoftObjectPath());
		}
	}

	//加载资源
	UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, AssetReferenceArr,
		FStreamableDelegate::CreateLambda([this, EffectEmitterData]()
			{
				// 添加到根集
				if (EffectEmitterData->ParticleData.ParticleSystemAsset.Get())
				{
					EffectEmitterData->ParticleData.ParticleSystemAsset.Get()->AddToRoot();
					this->EmitterPreLoadAssetList.Add(EffectEmitterData->ParticleData.ParticleSystemAsset.Get());
				}

				if (EffectEmitterData->SkeletalMesh.SkeletalMeshAsset.Get())
				{
					EffectEmitterData->SkeletalMesh.SkeletalMeshAsset.Get()->AddToRoot();
					this->EmitterPreLoadAssetList.Add(EffectEmitterData->SkeletalMesh.SkeletalMeshAsset.Get());
				}

				if (EffectEmitterData->Audio.AudioAsset.Get())
				{
					EffectEmitterData->Audio.AudioAsset.Get()->AddToRoot();
					this->EmitterPreLoadAssetList.Add(EffectEmitterData->Audio.AudioAsset.Get());
				}

				if (EffectEmitterData->StaticMesh.StaticMeshAsset.Get())
				{
					EffectEmitterData->StaticMesh.StaticMeshAsset.Get()->AddToRoot();
					this->EmitterPreLoadAssetList.Add(EffectEmitterData->StaticMesh.StaticMeshAsset.Get());
				}

				for (auto Asset : EffectEmitterData->SkeletalMesh.AnimAssetList)
				{
					if (Asset.Get())
					{
						Asset.Get()->AddToRoot();
						this->EmitterPreLoadAssetList.Add(Asset.Get());
					}
				}
			}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_EFFECT);
}

CONTROL_COMPILE_OPTIMIZE_END


