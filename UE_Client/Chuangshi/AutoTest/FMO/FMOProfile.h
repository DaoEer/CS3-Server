// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "AutoTest/BaseTest/BaseProfile.h"
#include "FMOProfile.generated.h"

/*
* 文件名称：FMOProfile.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UFMOProfile : public UBaseProfile
{
	GENERATED_BODY()
	
public:
	UFMOProfile();
	virtual void LoadCfg() override;
	virtual void EndRecord() override;
	virtual void StartTickTask() override;

	
};
