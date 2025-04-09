// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/CombatInterface.h"
#include "MonsterCombatInterface.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UMonsterCombatInterface : public UCombatInterface
{
	GENERATED_BODY()
	typedef UCombatInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		FString titleStr;

	static FString GetName() { return TEXT("CombatInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_MonsterCombatInterface.BP_MonsterCombatInterface_C'"); } //获取蓝图对象路径

	virtual void Set_HP(const int32& newVal, const int32& oldVal) override;
	virtual void Set_HP_Max(const int32& newVal, const int32& oldVal) override;
	virtual void Set_camp(const int32& newVal, const int32& oldVal)override;
	virtual void Set_gangQiValue(const int32& newVal, const int32& oldVal)override;
	virtual void Set_gangQiValue_Max(const int32& newVal, const int32& oldVal)override;
	virtual void Set_gangQiState(const int32& newVal, const int32& oldVal)override;
	virtual void Set_tempCamp(const int32& newVal, const int32& oldVal)override;
	virtual void Set_gangQi_qiJieProgress(const int32& newVal, const int32& oldVal)override;

	virtual void Set_title(const FString& newVal, const FString& oldVal);

	///打开移动的防护罩
	void OpenMoveShield(const int32& ID, const FString& Effect1, float IntervalTime1, float Angel1, const FString& Effect2, float IntervalTime2, float Angel2);
	void PlayShieldParticle(const FString& EffectId, int32 index, float IntervalTime, float Angel);
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|MonsterInterface")
		void OpenMoveShield_BP(const int32& ID, const FVector& Position);
	///关闭移动的防护罩
	void CloseMoveShield(const int32& ID);
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|MonsterInterface")
		void CloseMoveShield_BP(const int32& ID);
private:
	int32 EffectUId1;
	int32 EffectUId2;
};
