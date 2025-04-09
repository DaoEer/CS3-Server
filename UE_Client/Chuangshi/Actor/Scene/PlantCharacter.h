// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Scene/SceneCharacter.h"
#include "GameData/LingTianPlantData.h"
#include "PlantCharacter.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API APlantCharacter : public ASceneCharacter
{
	GENERATED_BODY()

		typedef ASceneCharacter Supper;

	APlantCharacter();
public:
	virtual void BeginPlay()override;
	void InitPlantData(const LINGTIAN_DATA PlantData_);

	void CreateAppearance();
	const FLING_TIAN_PLANT_DATA* GetCurLingTianData();

	// 获取当前种子的生长阶段数据(因为成熟期 ，跟最后一阶段用的模型一样)
	FGROWTHSTAGEMODELNUMBER GetCurSeedGrowData(const FLING_TIAN_PLANT_DATA* curSeedData);

private:
	virtual void OnCreateApperanceOver() override;

	
	void CheckGrowthStage();
	// 数据同步一次，后面客户端模拟
	void AddGrowthStage();
	void BeginCreateMesh();
	void CheckMeshComponent(const TArray<FVector>& PosList);

public:
	UPROPERTY(BlueprintReadOnly)
		UStaticMesh* TempMesh;

private:
	// 种子序号
	int32 seedNum;
	// 成长阶段
	int8 growthStage;
	// 该阶段开始时间（对应服务器time.time()）
	uint32 growTime;

	TArray<UStaticMeshComponent*> CropMeshComponents;
	int32 CurCreateMeshIndex;

	FTimerHandle DelayGrowHandle;
};
