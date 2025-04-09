// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/CombatInterface.h"
#include "VehiclePetCombatInterface.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UVehiclePetCombatInterface : public UCombatInterface
{
	GENERATED_BODY()
	typedef UCombatInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		FString titleStr;

	static FString GetName() { return TEXT("CombatInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_VehiclePetCombatInterface.BP_VehiclePetCombatInterface_C'"); } //获取蓝图对象路径
	
	virtual void Set_HP(const int32& newVal, const int32& oldVal) override;
	virtual void Set_HP_Max(const int32& newVal, const int32& oldVal) override;
	virtual void Set_camp(const int32& newVal, const int32& oldVal)override;
	virtual void Set_gangQiValue(const int32& newVal, const int32& oldVal)override;
	virtual void Set_gangQiValue_Max(const int32& newVal, const int32& oldVal)override;
	virtual void Set_gangQiState(const int32& newVal, const int32& oldVal)override;
	virtual void Set_tempCamp(const int32& newVal, const int32& oldVal)override;
	virtual void Set_gangQi_qiJieProgress(const int32& newVal, const int32& oldVal)override;
	virtual void Set_title(const FString& newVal, const FString& oldVal);
};
