// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "../Util/CustomEffect/DecalEffect.h"
#include "GameData/CS3Object.h"
#include "DecalManager.generated.h"

/*
* 文件名称：DecalManager.h
* 功能说明：贴花粒子管理器
* 文件作者：zhengxuemei
* 目前维护：zhangfudong
* 创建时间：2017-08-18
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UDecalManager : public UCS3Object
{
	GENERATED_BODY()

public:
	UDecalManager();
	~UDecalManager();

	//编辑器模式下会使用的单例，做特殊处理
	static UDecalManager* GetInstance();
	static void ClearInstance();

	virtual void BeginDestroy()override;

	// 创建贴花粒子，绑定在Mesh的AttachPoint上
	UFUNCTION(BlueprintCallable, Category = "DecalEffect")
	TArray<ADecalEffect*> CreateDecalEffect(UParticleSystem* ParticleSys, USceneComponent* Parent);

	// 删除贴花
	UFUNCTION(BlueprintCallable, Category = "DecalEffect")
	void DestroyDecalEffect(ADecalEffect* DecalEffect);

private:
	ADecalEffect* _BuildDecalEffect(const FEmitterData* DecalData, USceneComponent* Parent);

	TArray<ADecalEffect*> Decals;
	TArray<ADecalEffect*> LastCreate;

public:
	const FEmitterData* CurDecalData = nullptr;

private:
	static UDecalManager* Instance;
	bool bOnGame = false;
};
