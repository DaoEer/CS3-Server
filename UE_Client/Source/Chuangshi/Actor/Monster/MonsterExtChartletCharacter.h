// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "MonsterExtChartletCharacter.generated.h"

/*
* 文件名称：MonsterExtChartletCharacter.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2018-04-11
*/

class ADecalEffectEmitter;

UCLASS()
class CHUANGSHI_API AMonsterExtChartletCharacter : public AMonsterCharacter
{
	GENERATED_BODY()
	
	
public:
	AMonsterExtChartletCharacter();
	virtual void BeginPlay()override;
	virtual void OnCreateApperanceOver() override;

	/*----------------五行画卷渐隐功能相关---------------------------*/
	void onDisplayChartlet();
	void onDisappearChartlet(const int32& type);


	ADecalEffectEmitter* DecalEffectEmitter;

	FTimerHandle ChartletTimeHandle;
};
