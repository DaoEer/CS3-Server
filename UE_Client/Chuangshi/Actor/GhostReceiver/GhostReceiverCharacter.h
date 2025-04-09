// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Actor/NPCBaseCharacter.h"
#include "GhostReceiverCharacter.generated.h"

/*
* 文件名称：GhostReceiverCharacter.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2017-08-10
*/
UCLASS(BlueprintType)
class CHUANGSHI_API AGhostReceiverCharacter : public ANPCBaseCharacter
{
	GENERATED_BODY()
	
public:
	AGhostReceiverCharacter();
	
protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	
};
