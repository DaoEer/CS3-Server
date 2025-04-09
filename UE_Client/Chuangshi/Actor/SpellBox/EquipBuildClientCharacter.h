// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/NPC/ClientGameCharacter.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "EquipBuildClientCharacter.generated.h"

/**
* 文件名称：EquipBuildClientCharacter.h
* 功能说明：帮会掠夺战器械虚影
* 文件作者：liyuxia
* 创建时间：2020-08-19
*/
UCLASS()
class CHUANGSHI_API AEquipBuildClientCharacter : public AClientGameCharacter
{
	GENERATED_BODY()
public:
	virtual void BeginPlay()override;
	virtual void Tick(float DeltaSeconds) override;
	virtual void OnCreateApperanceOver() override;
	bool CanBuild();
private:
	void InitModelMaterial();
	void UpdateModelMaterialColor();
	void UpdateActorLocationAndRotation();
	void ChangeModelMaterial(int32 ColorIndex);//1:red 2:blue;
	FVector GetBoxExtent();/** Holds the extent of the bounding box. */
private:
	FVector2D lastMouseScreenPos;
	bool bCanBuild;
	UPROPERTY()
	UMaterialInstanceDynamic* TransBlue_Inst;
	UPROPERTY()
	UMaterialInstanceDynamic* TransRed_Inst;
	int32 curState;
};
