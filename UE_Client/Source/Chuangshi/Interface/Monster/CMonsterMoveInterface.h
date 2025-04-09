// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3Base/CS3EntityInterface.h"
#include "CMonsterMoveInterface.generated.h"


enum EMoveScriptType
{
	NONE = 0,
	CHASE_ACTOR,
	FOLLOW,
	RANDOM_WALK,
};



/**
 * 
 */
UCLASS()
class CHUANGSHI_API UCMonsterMoveInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;

public:
	static FString GetName() { return TEXT("StateInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.CMonsterMoveInterface'"); } //获取蓝图对象路径

	bool CanMoveCheck(EMoveScriptType Type);
	void StopMove();
	void RandomMove(float range);
	void ChaseActor(int32 targetID);

	EMoveScriptType GetMoveScriptType();

private:
	EMoveScriptType MoveScriptType;
};
