// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Level/CS3LevelScriptActor.h"
#include "SelectCampLevel.generated.h"

/*
* 文件名称：SelectCampLevel.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：shuqingping
* 创建时间：2017-06-21
*/

class UBaseWindow;

UCLASS(BlueprintType)
class CHUANGSHI_API ASelectCampLevel : public ACS3LevelScriptActor
{
	GENERATED_BODY()
	
public:
	virtual void BeginPlay() override;
	virtual void CreateDynamicRes() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

	virtual void OnLoadLevelFinished() override;
};
