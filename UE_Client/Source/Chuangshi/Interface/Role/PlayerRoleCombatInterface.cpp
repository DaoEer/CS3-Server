// Fill out your copyright notice in the Description page of Project Settings.


#include "PlayerRoleCombatInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UPlayerRoleCombatInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UPlayerRoleCombatInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(corporeity, &UPlayerRoleCombatInterface::Set_corporeity, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(strength, &UPlayerRoleCombatInterface::Set_strength, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(intellect, &UPlayerRoleCombatInterface::Set_intellect, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(dexterity, &UPlayerRoleCombatInterface::Set_dexterity, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(damage, &UPlayerRoleCombatInterface::Set_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(magic_damage, &UPlayerRoleCombatInterface::Set_magic_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(armor, &UPlayerRoleCombatInterface::Set_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(magic_armor, &UPlayerRoleCombatInterface::Set_magic_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(criticalstrike, &UPlayerRoleCombatInterface::Set_criticalstrike, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(discern, &UPlayerRoleCombatInterface::Set_discern, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(parry, &UPlayerRoleCombatInterface::Set_parry, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(speed, &UPlayerRoleCombatInterface::Set_speed, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(hitrate, &UPlayerRoleCombatInterface::Set_hitrate, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(dodgerate, &UPlayerRoleCombatInterface::Set_dodgerate, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(healingrate, &UPlayerRoleCombatInterface::Set_healingrate, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(feats, &UPlayerRoleCombatInterface::Set_feats, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(potential, &UPlayerRoleCombatInterface::Set_potential, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(xiuwei, &UPlayerRoleCombatInterface::Set_xiuwei, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(xiuweiLevel, &UPlayerRoleCombatInterface::Set_xiuweiLevel, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(cure, &UPlayerRoleCombatInterface::Set_cure, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(ice_damage, &UCombatInterface::Set_ice_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(fire_damage, &UCombatInterface::Set_fire_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(thunder_damage, &UCombatInterface::Set_thunder_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(xuan_damage, &UCombatInterface::Set_xuan_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(ice_armor, &UCombatInterface::Set_ice_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(fire_armor, &UCombatInterface::Set_fire_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(thunder_armor, &UCombatInterface::Set_thunder_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(xuan_armor, &UCombatInterface::Set_xuan_armor, int32)
CS3_END_INTERFACE_PROPERTY_MAP()


void UPlayerRoleCombatInterface::Set_corporeity(const int32& newVal, const int32& oldVal)
{
	corporeity = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnCorporeityChanged.Broadcast( corporeity ) ;
	}
}

void UPlayerRoleCombatInterface::Set_strength(const int32& newVal, const int32& oldVal)
{
	strength = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnStrengthChanged.Broadcast( strength ) ;
	}
}

void UPlayerRoleCombatInterface::Set_intellect(const int32& newVal, const int32& oldVal)
{
	intellect = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnIntellectChanged.Broadcast( intellect ) ;
	}
}

void UPlayerRoleCombatInterface::Set_dexterity(const int32& newVal, const int32& oldVal)
{
	dexterity = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnDexterityChanged.Broadcast( dexterity ) ;
	}
}

void UPlayerRoleCombatInterface::Set_damage(const int32& newVal, const int32& oldVal)
{
	damage = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnDamageChanged.Broadcast( damage ) ;
	}
}

void UPlayerRoleCombatInterface::Set_magic_damage(const int32& newVal, const int32& oldVal)
{
	magic_damage = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnMagicDamageChanged.Broadcast( magic_damage ) ;
	}
}

void UPlayerRoleCombatInterface::Set_armor(const int32& newVal, const int32& oldVal)
{
	armor = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnArmorChanged.Broadcast( armor ) ;
	}
}

void UPlayerRoleCombatInterface::Set_magic_armor(const int32& newVal, const int32& oldVal)
{
	magic_armor = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnMagicArmorChanged.Broadcast( magic_armor ) ;
	}
}

void UPlayerRoleCombatInterface::Set_criticalstrike(const int32& newVal, const int32& oldVal)
{
	criticalstrike = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnCriticalstrikeChanged.Broadcast( criticalstrike ) ;
	}
}

void UPlayerRoleCombatInterface::Set_discern(const int32& newVal, const int32& oldVal)
{
	discern = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnDiscernChanged.Broadcast( discern ) ;
	}
}

void UPlayerRoleCombatInterface::Set_parry(const int32& newVal, const int32& oldVal)
{
	parry = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnParryChanged.Broadcast( parry ) ;
	}
}

void UPlayerRoleCombatInterface::Set_speed(const int32& newVal, const int32& oldVal)
{
	speed = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnSpeedChanged.Broadcast( speed ) ;
	}
}

void UPlayerRoleCombatInterface::Set_hitrate(const int32& newVal, const int32& oldVal)
{
	hitrate = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnHitrateChanged.Broadcast( hitrate ) ;
	}
}

void UPlayerRoleCombatInterface::Set_dodgerate(const int32& newVal, const int32& oldVal)
{
	dodgerate = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnDodgerateChanged.Broadcast( dodgerate ) ;
	}
}

void UPlayerRoleCombatInterface::Set_healingrate(const int32& newVal, const int32& oldVal)
{
	healingrate = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnHealingrateChanged.Broadcast( healingrate ) ;
	}
}

void UPlayerRoleCombatInterface::Set_feats(const int32& newVal, const int32& oldVal)
{
	feats = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnFeatsChanged.Broadcast(feats);
	}
}

void UPlayerRoleCombatInterface::Set_potential(const int32& newVal, const int32& oldVal)
{
	potential = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnPotentialChange.Broadcast( potential ) ;
	}
}

void UPlayerRoleCombatInterface::Set_xiuwei(const int32& newVal, const int32& oldVal)
{
	xiuwei = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnXiuweiChanged.Broadcast(xiuwei);
	}
}

void UPlayerRoleCombatInterface::Set_xiuweiLevel(const int32& newVal, const int32& oldVal)
{
	xiuweiLevel = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnXiuweiLevelChanged.Broadcast( xiuweiLevel ) ;
	}
}

void UPlayerRoleCombatInterface::Set_cure(const int32 & newVal, const int32 & oldVal)
{
	cure = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnCureChanged.Broadcast(cure);
	}
}

void UPlayerRoleCombatInterface::Set_ice_damage(const int32& newVal, const int32& oldVal)
{
	ice_damage = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnIceDamageChanged.Broadcast(ice_damage);
	}
}

void UPlayerRoleCombatInterface::Set_fire_damage(const int32& newVal, const int32& oldVal)
{
	fire_damage = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnFireDamageChanged.Broadcast(fire_damage);
	}
}

void UPlayerRoleCombatInterface::Set_thunder_damage(const int32& newVal, const int32& oldVal)
{
	thunder_damage = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnThunderDamageChanged.Broadcast(thunder_damage);
	}
}

void UPlayerRoleCombatInterface::Set_xuan_damage(const int32& newVal, const int32& oldVal)
{
	xuan_damage = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnXuanDamageChanged.Broadcast(xuan_damage);
	}
}

void UPlayerRoleCombatInterface::Set_ice_armor(const int32& newVal, const int32& oldVal)
{
	ice_armor = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnIceArmorChanged.Broadcast(ice_armor);
	}
}

void UPlayerRoleCombatInterface::Set_fire_armor(const int32& newVal, const int32& oldVal)
{
	fire_armor = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnFireArmorChanged.Broadcast(fire_armor);
	}
}

void UPlayerRoleCombatInterface::Set_thunder_armor(const int32& newVal, const int32& oldVal)
{
	thunder_armor = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnThunderArmorChanged.Broadcast(thunder_armor);
	}
}

void UPlayerRoleCombatInterface::Set_xuan_armor(const int32& newVal, const int32& oldVal)
{
	xuan_armor = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnXuanArmorChanged.Broadcast(xuan_armor);
	}
}
