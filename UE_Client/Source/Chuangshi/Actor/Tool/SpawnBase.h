// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/ModelPartData.h"
#include "GameData/EffectEmitterData.h"
#include "Actor/GameCharacter.h"
#include "SpawnBase.generated.h"
/*
* 文件名称：SpawnBase.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2017-05-26
*/

class UParticleManager;
class UParticleSystemComponent;
class AEffectEmitter;

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSpawnPointRange
{
	GENERATED_BODY()
public:
	///范围/领域的名字（只为了区分范围）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RangeName")
		FString RangeName;

	///贴花材质（以后有了新贴花材质可以用不同材质区分范围）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "DecalMaterial")
		UMaterialInterface* DecalMaterial;

	///范围的大小
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RangeVaule")
		float RangeVaule = 0.0f;
};

UCLASS(BlueprintType)
class CHUANGSHI_API ASpawnBase : public AGameCharacter
{
	GENERATED_BODY()

public:
	ASpawnBase();

public:
	/**
	* 设置待机动作
	* @param  AnimData		动作资源表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SpawnBase")
	void SetAnimationOfStand(UDataTable* AnimData);

	/**
	* 播放粒子
	* @param  EffectDataTable		光效数据表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SpawnBase")
		void PlayEffect(FName EffectID);

	UFUNCTION(BlueprintCallable, Category = "SpawnBase")
		void ClearEffect();///<清除光效

	UFUNCTION(BlueprintCallable, Category = "SpawnBase")
		void SetActorPart(MODEL_PART_TYPE PartPos, FMODEL_PART_DATA PartData);

protected:
	void EffectStartPlay(FEFFECT_DATA EffectData);///<开始播光效


public:
	UPROPERTY(BlueprintReadWrite, Category = "EffectComponent")
		UParticleSystemComponent* EffectComponent;

	//光效是否绑定
	bool IsEffectBind;

	///能否看到光效
	UPROPERTY(BlueprintReadWrite, EditAnywhere, Category = "EffectComponent")
		bool IsCanSpawnEffect;

	///当前光效
	UPROPERTY(BlueprintReadWrite, EditAnywhere, Category = "EffectComponent")
		TArray<AEffectEmitter*> CurEffect;

private:
	void InitBaseComponent();

};

