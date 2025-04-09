// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/GameCharacter.h"
#include "BeCatchedCharacter.generated.h"

/*
* 文件名称：BeCatchedCharacter.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：wuxiaoou
* 创建时间：2018-02-08
*/
UCLASS()
class CHUANGSHI_API ABeCatchedCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	ABeCatchedCharacter();
	virtual void BeginPlay()override;

	virtual void SetInitAction() override;///<重写SetInitAction

										  //创建完毕回调
	virtual void OnCreateApperanceOver()override;

	//void InitAppearanceComponent();///<重写InitBaseComponent
public:
	//创建完毕后要播放的动作
	FName m_AnimId;
	
};
