// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/Role/RoleCombatInterface.h"
#include "PlayerRoleCombatInterface.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UPlayerRoleCombatInterface : public URoleCombatInterface
{
	GENERATED_BODY()
	typedef URoleCombatInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	static FString GetName() { return TEXT("CombatInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Blueprint'/Game/BluePrints/Entity/Interface/BP_PlayerRoleCombatInterface.BP_PlayerRoleCombatInterface_C'"); } //获取蓝图对象路径

	virtual void Set_corporeity(const int32& newVal, const int32& oldVal) override;
	virtual void Set_strength(const int32& newVal, const int32& oldVal)override;
	virtual void Set_intellect(const int32& newVal, const int32& oldVal)override;
	virtual void Set_dexterity(const int32& newVal, const int32& oldVal)override;
	virtual void Set_damage(const int32& newVal, const int32& oldVal)override;
	virtual void Set_magic_damage(const int32& newVal, const int32& oldVal)override;
	virtual void Set_armor(const int32& newVal, const int32& oldVal)override;
	virtual void Set_magic_armor(const int32& newVal, const int32& oldVal)override;
	virtual void Set_criticalstrike(const int32& newVal, const int32& oldVal)override;
	virtual void Set_discern(const int32& newVal, const int32& oldVal)override;
	virtual void Set_parry(const int32& newVal, const int32& oldVal)override;
	virtual void Set_speed(const int32& newVal, const int32& oldVal)override;
	virtual void Set_hitrate(const int32& newVal, const int32& oldVal)override;
	virtual void Set_dodgerate(const int32& newVal, const int32& oldVal)override;
	virtual void Set_healingrate(const int32& newVal, const int32& oldVal)override;
	virtual void Set_feats(const int32& newVal, const int32& oldVal);
	virtual void Set_potential(const int32& newVal, const int32& oldVal)override;
	virtual void Set_xiuwei(const int32& newVal, const int32& oldVal)override;
	virtual void Set_xiuweiLevel(const int32& newVal, const int32& oldVal)override;
	virtual void Set_cure(const int32& newVal, const int32& oldVal)override;
	virtual void Set_ice_damage(const int32& newVal, const int32& oldVal);
	virtual void Set_fire_damage(const int32& newVal, const int32& oldVal);
	virtual void Set_thunder_damage(const int32& newVal, const int32& oldVal);
	virtual void Set_xuan_damage(const int32& newVal, const int32& oldVal);
	virtual void Set_ice_armor(const int32& newVal, const int32& oldVal);
	virtual void Set_fire_armor(const int32& newVal, const int32& oldVal);
	virtual void Set_thunder_armor(const int32& newVal, const int32& oldVal);
	virtual void Set_xuan_armor(const int32& newVal, const int32& oldVal);
};
