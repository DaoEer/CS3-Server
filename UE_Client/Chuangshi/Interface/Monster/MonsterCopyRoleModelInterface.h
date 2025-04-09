// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "MonsterCopyRoleModelInterface.generated.h"

/*
* 文件名称：MonsterCopyRoleModelInterface.h
* 功能说明：用于心魔、分身、替身等怪物Copy玩家的模型（时装、捏脸）
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020/12/9
*/

UCLASS()
class CHUANGSHI_API UMonsterCopyRoleModelInterface : public UMonsterInterface
{
	GENERATED_BODY()
	
public:
	//获取控制自身的玩家的ID
	int32 GetOwnerID();
	// 如果归宿玩家还没创建好，就延迟创建
	void DelayCreateApperance();


private:
	FTimerHandle DelayCreateAppearHandle;
	int8 WaitTime;					// 等待copy对象的次数，10次（10秒）模型就创建失败了 			
};
