// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Level/CS3LevelScriptActor.h"
#include "LoginSelectLevel.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API ALoginSelectLevel : public ACS3LevelScriptActor
{
	GENERATED_BODY()

public:
	virtual void BeginPlay() override;

	void OnBeginPlayCGEvent();///<开始播放开场CG

	void PlayCG(); ///播放开场CG

	void PlayerCGFinished(); ///<播放CG结束
};
