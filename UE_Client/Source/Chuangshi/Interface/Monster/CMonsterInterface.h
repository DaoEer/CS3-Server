// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "CMonsterInterface.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UCMonsterInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_CMonsterInterface.BP_CMonsterInterface_C'"); } //获取蓝图对象路径

};
