// Fill out your copyright notice in the Description page of Project Settings.


#include "DecalManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Particles/ParticleSystem.h"
#include "Particles/ParticleEmitter.h"
#include"Chuangshi.h"
CONTROL_COMPILE_OPTIMIZE_START

UDecalManager* UDecalManager::Instance = nullptr;

UDecalManager::UDecalManager()
{
}

UDecalManager::~UDecalManager()
{
	if (CurDecalData)
	{
		delete CurDecalData;
		CurDecalData = nullptr;
	}
}

UDecalManager* UDecalManager::GetInstance()
{
	//游戏启动了
	if (UUECS3GameInstance::Instance)
	{
		//如果游戏实例有值就用此值，管理器自身的Instance可能被回收
		if (UUECS3GameInstance::Instance->DecalManager)
		{
			return UUECS3GameInstance::Instance->DecalManager;
		}

		//管理器无效或者是编辑器创建的就清空重新创建
		if (!IsValid(Instance))
		{
			CS3_Warning(TEXT("-->Null Pointer error: UDecalManager::GetInstance: Instance !"));
			Instance = nullptr;
		}
		else if(!Instance->bOnGame)
		{
			Instance->RemoveFromRoot();
			Instance = nullptr;
		}
		//创建管理器并设置为游戏状态下创建的
		if (!Instance)
		{
			Instance = NewObject<UDecalManager>();
			Instance->bOnGame = true;
		}
	}
	//游戏未启动
	else
	{
		if (!IsValid(Instance))
		{
			Instance = NewObject<UDecalManager>();

	//游戏未启动时加入根集，未加入根集会导致指针被垃圾回收，但是静态变量依然存在内存中，导致内存不断增长
#if WITH_EDITOR
			Instance->AddToRoot();
#endif 

		}
	}

	return Instance;
	//return NewObject<UDecalManager>();
}

void UDecalManager::ClearInstance()
{
	Instance = nullptr;
}

void UDecalManager::BeginDestroy()
{
	for (int i = 0; i < Decals.Num(); i++)
	{
		Decals[i]->Destroy();
	}
	Decals.Empty();
	Super::BeginDestroy();
}

TArray<ADecalEffect*> UDecalManager::CreateDecalEffect(UParticleSystem* ParticleSys, USceneComponent* Parent)
{
	LastCreate.Empty();

	if (!ParticleSys)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UDecalManager::CreateDecalEffect : ParticleSys!"));
		return LastCreate;
	}

	TArray<class UParticleEmitter*> emitters = ParticleSys->Emitters;
	for (int i = 0; i < emitters.Num(); i++)
	{
		UParticleEmitter* emit = emitters[i];
		if (emit->EmitterName.ToString().Contains("Decal"))
		{
			FEmitterData emitterData(emit);
			
			//在编辑器模式需要在第一次Tick上执行贴花组件绑定到粒子根结点
			if (UUECS3GameInstance::Instance && (!Parent || (Parent->GetWorld() == UUECS3GameInstance::Instance->GetWorld())))
			{
				emitterData.bOnMesh = false;
			}
			else
			{
				emitterData.bOnMesh = true;
			}

			//emitterData.InitialHeight = Height;
			ADecalEffect* decal = _BuildDecalEffect(&emitterData, Parent);
			if (decal)
				LastCreate.Add(decal);
		}
	}
	return LastCreate;
}

void UDecalManager::DestroyDecalEffect(ADecalEffect* DecalEffect)
{
	int idx = 0;
	if (Decals.Find(DecalEffect, idx))
	{
		Decals[idx]->Destroy();
		Decals.RemoveAt(idx);
	}
}

ADecalEffect* UDecalManager::_BuildDecalEffect(const FEmitterData* DecalData, USceneComponent* Parent)
{
	if (!DecalData->DecalMaterial)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UDecalManager::_BuildDecalEffect : DecalData->DecalMaterial!"));
		return NULL;
	}

	UWorld* World = Parent ? Parent->GetWorld() : GetWorld();
	if (!World)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UDecalManager::_BuildDecalEffect : World!"));
		return NULL;
	}

	//更新数据前先销毁上一个
	if (CurDecalData)
	{
		delete CurDecalData;
		CurDecalData = nullptr;
	}

	CurDecalData = new FEmitterData(DecalData);//UDecalManager::_BuildDecalEffect和UDecalManager::~UDecalManager中释放

	ADecalEffect* Decal = World->SpawnActor<ADecalEffect>(ADecalEffect::StaticClass());

	//Decal->Init(DecalData, LocationOffset, DecalData->Delay, Attached, Parent, AttachPointName);
	//创建贴花光效后直接返回，贴花内部会去自己处理绑定和初始化数据
	Decals.Add(Decal);
	return Decal;
}

CONTROL_COMPILE_OPTIMIZE_END

