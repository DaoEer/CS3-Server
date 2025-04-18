#include "Actor/Particle/ParticleModuleEx/ParticleModuleSkeletalMesh.h"
#include "Particles/ParticleModule.h"
#include "Particles/ParticleLODLevel.h"
#include "ParticleEmitterInstances.h"
#include "Particles/ParticleSystem.h"
#include "Particles/ParticleModuleRequired.h"
#include "Particles/ParticleSystemComponent.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Components/SkeletalMeshComponent.h"
#include "ParticleSkeletalMeshEmitterInstances.h"
#include "Util/CS3Debug.h"

UParticleModuleSkeletalMesh::UParticleModuleSkeletalMesh(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer),
	MaxParticleNum(5)
{
	bSpawnModule = true;
	bUpdateModule = true;
}
					
#if WITH_EDITOR
void UParticleModuleSkeletalMesh::PostEditChangeProperty(FPropertyChangedEvent& PropertyChangedEvent)
{
}
#endif 
// WITH_EDITOR

void UParticleModuleSkeletalMesh::PostInitProperties()
{
	Super::PostInitProperties();
}

void UParticleModuleSkeletalMesh::Spawn(FParticleEmitterInstance* Owner, int32 Offset, float SpawnTime, FBaseParticle* ParticleBase)
{
	//发射器是skeletalMeshEmitterInstance才spawn
	if (!IsSkMeshEmitterInstance(Owner))
		return;
	// 光效希望看见这个模型的大小，不强制显示模型的情况下，PIE和Game才生成
	if (!VisibleMesh)
	{
		// world类型是PIE和Game的时候spawn，否则可能会出现一个多余的静态模型
		UWorld* world = Owner->GetWorld();
		check(world);
		if (!(EWorldType::Game == world->WorldType || EWorldType::PIE == world->WorldType))
			return;
	}
	else // 如果是开启的需要关闭，开启visible仅允许给光效调效果用
	{
		//CS3_Warning(TEXT("ParticleSystem: %s, ParticleModuleSkeletalMesh's Visible is true, it must be false"), *Owner->Component->GetFullName());
		UE_LOG(LogClass, Error, TEXT("ParticleSystem: %s, ParticleModuleSkeletalMesh's Visible is true, it must be false"), *Owner->Component->GetFullName());
	}

	SpawnEx(Owner, Offset, SpawnTime, NULL, ParticleBase);
}

uint32 UParticleModuleSkeletalMesh::RequiredBytes(UParticleModuleTypeDataBase* TypeData)
{
	return sizeof(FSkMeshParticlePayload);
}

void UParticleModuleSkeletalMesh::SpawnEx(FParticleEmitterInstance* Owner, int32 Offset, float SpawnTime, struct FRandomStream* InRandomStream, FBaseParticle* ParticleBase)
{
	SPAWN_INIT;
	PARTICLE_ELEMENT(FSkMeshParticlePayload, MeshData);
		MeshData.MeshId = SpawnSkMesh(MeshData, Particle, Owner);
}

uint64 UParticleModuleSkeletalMesh::SpawnSkMesh(const FSkMeshParticlePayload& Payload, FBaseParticle& Particle, FParticleEmitterInstance* Owner)
{
	uint64 MeshId = 0;
	if (!Owner)
	{
		return 0;
	}
	UParticleSystemComponent* ParticleSystem = Owner->Component;
	if (!ParticleSystem)
	{
		return 0;
	}
	FParticleSkeletalMeshEmitterInstance* Inst = static_cast<FParticleSkeletalMeshEmitterInstance*>(Owner);
	if (Inst == nullptr)
		return 0;

	AActor* Container = ParticleSystem->GetOwner();

	if (!Container || Container->IsPendingKillPending())
	{
		return 0;
	}	
// 	// 粒子数量超过最大值
// 	if (Inst->Meshes.Num() >= MaxParticleNum)
// 	{
// 		MeshId = Inst->FindInactiveParticle();
// 	}
// 	else// 
	{
		// Construct the new component and attach as needed		
		USkeletalMeshComponent* SkMeshComponent = NewObject<USkeletalMeshComponent>(Container, USkeletalMeshComponent::StaticClass());

		//USkeletalMeshComponent* SkMeshComponent = LoadObject<USkeletalMeshComponent>(nullptr, TEXT("/Content/Effects/Meshs/SkeletonMeshs/10750_Posui01.10750_Posui01"));
		if (SkMeshComponent)
		{
			MeshId = (uint64)SkMeshComponent;
			USceneComponent* RootComponent = Container->GetRootComponent();
			USceneComponent* AttachParent = ParticleSystem->GetAttachParent();
			//SkMeshComponent->AddToRoot();
			if (AttachParent)
			{
				SkMeshComponent->SetupAttachment(AttachParent, ParticleSystem->GetAttachSocketName());
			}
			else if (RootComponent)
			{
				SkMeshComponent->SetupAttachment(RootComponent);
			}
			else
			{
				SkMeshComponent->SetupAttachment(ParticleSystem);
			}
			//SkMeshComponent->SetCastShadows(bShadowCastingLights);
			SkMeshComponent->RegisterComponent();

			Inst->Meshes.Add(SkMeshComponent);
			int32 ScreenAlignment;
			FVector ComponentScale;
			Owner->GetScreenAlignmentAndScale(ScreenAlignment, ComponentScale);
			//UpdateHQLight(LightComponent, Payload, Particle, ScreenAlignment, ComponentScale, Owner->UseLocalSpace(), nullptr, false);
			if (!Inst->SkMeshTypeData)
				return 0;
			SkMeshComponent->SetSkeletalMesh(Inst->SkMeshTypeData->Mesh);
			SkMeshComponent->PlayAnimation(Inst->SkMeshTypeData->Animation, Inst->SkMeshTypeData->AnimationLoop);
			SkMeshComponent->SetVisibility(false);
			SkMeshComponent->SetTranslucentSortPriority(TranslucentSortPriority);
			// 不启动游戏在编辑器中也更新动画
			SkMeshComponent->SetUpdateAnimationInEditor(true);
			const FMeshRotationPayloadData* PayloadData = (FMeshRotationPayloadData*)((uint8*)&Particle + Inst->MeshRotationOffset);
			//UpdateSkMesh(SkMeshComponent, PayloadData, Particle, Owner->UseLocalSpace());
			// 指定材质
			int32 SetMatNum = Inst->CurrentMaterials.Num();
			int32 CompMatNum = SkMeshComponent->GetNumMaterials();
			int32 MinMatNum = SetMatNum > CompMatNum ? CompMatNum : SetMatNum;
			if (MinMatNum > 0)
				for (int i = 0; i < MinMatNum; i++)
				{
					SkMeshComponent->CreateDynamicMaterialInstance(i, Inst->CurrentMaterials[i]);
				}
		}
	}
	return MeshId;
}

void UParticleModuleSkeletalMesh::UpdateSkMesh(USkeletalMeshComponent* MeshComponent, const FMeshRotationPayloadData* Payload, const FBaseParticle& Particle, bool bLocalSpace)
{
	//NewRotation = Particle.Rotation + DeltaTime * Particle.RotationRate;
	if (bLocalSpace)
	{
		MeshComponent->SetRelativeLocation(Particle.Location);
		//MeshComponent->SetRelativeRotation(Payload->Rotation.Rotation());
		MeshComponent->SetRelativeScale3D(Particle.Size);
// 		FString DebugString = FString::Printf(TEXT("Rotation(Vector): ")) + Payload->Rotation.ToString();
// 		GEngine->AddOnScreenDebugMessage(INDEX_NONE, 0.f, FColor::Yellow, DebugString, false);
// 		FString DebugString2 = FString::Printf(TEXT("Rotation(FRotator): ")) + Payload->Rotation.Rotation().ToString();
// 		GEngine->AddOnScreenDebugMessage(INDEX_NONE, 0.f, FColor::Green, DebugString2, false);

		// 获取Rotation的方式直接用Payload->Rotation.Rotation()有问题
		// 因为旋转值是直接存在Payload->Rotation的Vector里面，直接获取MakeFromEuler(Payload->Rotation)才对
		// 参照ParticleSystemRender.cpp :FDynamicMeshEmitterData::CalculateParticleTransform 2361行
		float fRot = Particle.Rotation * 180.0f / PI;
		FVector kRotVec = FVector(fRot, fRot, fRot);
		FRotator kRotator = FRotator::MakeFromEuler(kRotVec);
		kRotator += FRotator::MakeFromEuler(Payload->Rotation);
		MeshComponent->SetRelativeRotation(kRotator);

// 		FString DebugString1 = FString::Printf(TEXT("GetRotation: ")) + kRotator.ToString();
// 		GEngine->AddOnScreenDebugMessage(INDEX_NONE, 0.f, FColor::Red, DebugString1, false);

	}
	else
	{
		MeshComponent->SetWorldLocation(Particle.Location);
		//MeshComponent->SetWorldRotation(Payload->RotationRate.Rotation());
		MeshComponent->SetWorldScale3D(Particle.Size);

		float fRot = Particle.Rotation * 180.0f / PI;
		FVector kRotVec = FVector(fRot, fRot, fRot);
		FRotator kRotator = FRotator::MakeFromEuler(kRotVec);
		kRotator += FRotator::MakeFromEuler(Payload->Rotation);
		MeshComponent->SetWorldRotation(kRotator);
	}
	if (!MeshComponent->IsVisible())
		MeshComponent->SetVisibility(true);
}

void UParticleModuleSkeletalMesh::UpdateMaterial(USkeletalMeshComponent* MeshComponent, const FBaseParticle& Particle, const FParticleEmitterInstance* Owner)
{
	FLinearColor Dynamic;
	const int32 DynParamOffset = Owner->DynamicParameterDataOffset;
	if (DynParamOffset > 0)
	{
		// Override dynamic parameters to allow vertex colors to be used
		FEmitterDynamicParameterPayload& DynamicPayload = *((FEmitterDynamicParameterPayload*)((uint8*)&Particle + DynParamOffset));
		Dynamic = FLinearColor(DynamicPayload.DynamicParameterValue[0], DynamicPayload.DynamicParameterValue[1], DynamicPayload.DynamicParameterValue[2], DynamicPayload.DynamicParameterValue[3]);
	}
	TArray<class UMaterialInterface *> Mats = MeshComponent->GetMaterials();
	
	for (int i = 0; i < Mats.Num(); i++)
	{
		UMaterialInstanceDynamic * dyMat = Cast<UMaterialInstanceDynamic>(Mats[i]);
		if (dyMat)
		{
			dyMat->SetVectorParameterValue(TEXT("ColorParam"), Particle.Color);
			dyMat->SetVectorParameterValue(TEXT("DynamicParam"), Dynamic);
		}
	}
}

bool UParticleModuleSkeletalMesh::IsSkMeshEmitterInstance(FParticleEmitterInstance* Owner)
{
	// 当还没有添加ParticleModuleTypeDataSkeletalMesh这个模组的时候，直接添加模组UParticleModuleSkeletalMesh会有问题
	// Instance并不是FParticleSkeletalMeshEmitterInstance， 只是一个普通的FParticleSpriteEmitterInstance
	// static_cast类型不安全判断不了，所以采用下面的方法来进行判断
	check(Owner);
	UParticleLODLevel* LODLevel = Owner->SpriteTemplate->GetLODLevel(0);
	check(LODLevel);
	UParticleModuleTypeDataSkeletalMesh* SkMeshTypeData = Cast<UParticleModuleTypeDataSkeletalMesh>(LODLevel->TypeDataModule);
	return IsValid(SkMeshTypeData);
}

void UParticleModuleSkeletalMesh::Update(FParticleEmitterInstance* Owner, int32 Offset, float DeltaTime)
{
	if ((Owner == NULL) || (Owner->ActiveParticles <= 0) ||
		(Owner->ParticleData == NULL) || (Owner->ParticleIndices == NULL))
	{
		return;
	}
	UWorld* OwnerWorld = Owner->GetWorld();
	FSceneInterface* OwnerScene = nullptr;
	if (OwnerWorld)
	{
		OwnerScene = OwnerWorld->Scene;
	}
	if (!IsSkMeshEmitterInstance(Owner))
		return;
	FParticleSkeletalMeshEmitterInstance* Inst = static_cast<FParticleSkeletalMeshEmitterInstance*>(Owner);
	if (Inst == nullptr)
		return;
	FPlatformMisc::Prefetch(Owner->ParticleData, (Owner->ParticleIndices[0] * Owner->ParticleStride));
	FPlatformMisc::Prefetch(Owner->ParticleData, (Owner->ParticleIndices[0] * Owner->ParticleStride) + PLATFORM_CACHE_LINE_SIZE);
	const bool bUseLocalSpace = Owner->UseLocalSpace();
	int32 ScreenAlignment;
	FVector ComponentScale;
	Owner->GetScreenAlignmentAndScale(ScreenAlignment, ComponentScale);
	BEGIN_UPDATE_LOOP;
	{
		PARTICLE_ELEMENT(FSkMeshParticlePayload, Data);
		// 		const float Brightness = BrightnessOverLife.GetValue(Particle.RelativeTime, Owner->Component);
		// 		Data.ColorScale = ColorScaleOverLife.GetValue(Particle.RelativeTime, Owner->Component) * Brightness;
		//if (bHighQualityLights && (Data.MeshId != 0))
		if (Data.MeshId != 0)
		{
			// 			FString DebugString = FString::Printf(TEXT("ActiveMeshes :(%d) RelativeTime:(%f)"),	Data.MeshId, Particle.RelativeTime);
			// 			GEngine->AddOnScreenDebugMessage(INDEX_NONE, 0.f, FColor::Red, DebugString, false);
			//for now we can do this
			USkeletalMeshComponent* MeshComponent = (USkeletalMeshComponent*)Data.MeshId;
			if (MeshComponent && IsValid(MeshComponent))
			{
				const FMeshRotationPayloadData* PayloadData = (FMeshRotationPayloadData*)((uint8*)&Particle + Inst->MeshRotationOffset);
				UpdateSkMesh(MeshComponent, PayloadData, Particle, bUseLocalSpace);
				UpdateMaterial(MeshComponent, Particle, Owner);
			}
		}
	}
	END_UPDATE_LOOP;
	// lifetime生命结束后就不会再调用此update，所以后面这一段只能等到下一个粒子模组更新才能删除Mesh，所以造成Mesh删除不及时。
	// 重载EmitterInstance的KillParticle来做删除操作，zxm，2019年4月9日15:26:05
	//remove any dead Meshes.
	// 	FParticleSkeletalMeshEmitterInstance* Inst = static_cast<FParticleSkeletalMeshEmitterInstance*>(Owner);
	// 	if (Inst == nullptr)
	// 		return ;
	// 
	// 	{
	// 		for (int32 i = 0; i < Inst->Meshes.Num(); ++i)
	// 		{
	// 			USkeletalMeshComponent* MeshComponent = Inst->Meshes[i];
	// 
	// 			FString DebugString = FString::Printf(TEXT("Instance Mesh:(%d)"), (uint64)MeshComponent);
	// 
	// 			GEngine->AddOnScreenDebugMessage(INDEX_NONE, 0.f, FColor::Green, DebugString, false);
	// 
	// 			if (MeshComponent && !ActiveMeshes.Contains((uint64)MeshComponent))
	// 			{
	// 				MeshComponent->SetVisibility(false);
	// 				MeshComponent->Modify();
	// 				MeshComponent->DestroyComponent(false);
	// 				Inst->Meshes.RemoveAtSwap(i);
	// 				--i;
	// 
	// 				DebugString = FString::Printf(TEXT("Destroy Mesh:(%d)"), (uint64)MeshComponent);
	// 
	// 				GEngine->AddOnScreenDebugMessage(INDEX_NONE, 2.f, FColor::Yellow, DebugString, false);
	// 			}
	// 		}
	// 	}
}
 	