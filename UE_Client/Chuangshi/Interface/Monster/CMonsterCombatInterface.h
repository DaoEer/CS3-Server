// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3Base/CS3EntityInterface.h"
#include "interface/CombatInterface.h"
#include "CMonsterCombatInterface.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UCMonsterCombatInterface : public UCombatInterface
{
	GENERATED_BODY()
	//typedef UCS3EntityInterface Supper;
	typedef UCombatInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	static FString GetName() { return TEXT("CombatInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_CMonsterCombatInterface.BP_CMonsterCombatInterface_C'"); } //获取蓝图对象路径	

	virtual void Set_HP(const int32& newVal, const int32& oldVal) override;
	virtual void Set_HP_Max(const int32& newVal, const int32& oldVal) override;
};
