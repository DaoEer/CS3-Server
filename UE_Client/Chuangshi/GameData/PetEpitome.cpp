// Fill out your copyright notice in the Description page of Project Settings.


#include "PetEpitome.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Manager/EventManager.h"

UPetEpitome::UPetEpitome()
{
	PtrMap.Add(TEXT("ability"), &UPetEpitome::OnRep_ability);
	PtrMap.Add(TEXT("ability_Max"), &UPetEpitome::OnRep_ability_Max);
	PtrMap.Add(TEXT("step"), &UPetEpitome::OnRep_step);
	PtrMap.Add(TEXT("name"), &UPetEpitome::OnRep_name);
	PtrMap.Add(TEXT("sleepTime"), &UPetEpitome::OnRep_sleepTime);
	PtrMap.Add(TEXT("attrSkillBox"), &UPetEpitome::OnRep_attrSkillBox);
	PtrMap.Add(TEXT("passiveSkillBox"), &UPetEpitome::OnRep_passiveSkillBox);
	PtrMap.Add(TEXT("noLearnedSkillBox"), &UPetEpitome::OnRep_noLearnedSkillBox);

	PtrMap.Add(TEXT("corporeity"), &UPetEpitome::OnRep_corporeity);
	PtrMap.Add(TEXT("strength"), &UPetEpitome::OnRep_strength);
	PtrMap.Add(TEXT("intellect"), &UPetEpitome::OnRep_intellect);
	PtrMap.Add(TEXT("discern"), &UPetEpitome::OnRep_discern);
	PtrMap.Add(TEXT("dexterity"), &UPetEpitome::OnRep_dexterity);
	PtrMap.Add(TEXT("HP"), &UPetEpitome::OnRep_HP);
	PtrMap.Add(TEXT("MP"), &UPetEpitome::OnRep_MP);
	PtrMap.Add(TEXT("HP_Max"), &UPetEpitome::OnRep_HP_Max);
	PtrMap.Add(TEXT("MP_Max"), &UPetEpitome::OnRep_MP_Max);
	PtrMap.Add(TEXT("damage"), &UPetEpitome::OnRep_damage);
	PtrMap.Add(TEXT("magic_damage"), &UPetEpitome::OnRep_magic_damage);
	PtrMap.Add(TEXT("armor"), &UPetEpitome::OnRep_armor);
	PtrMap.Add(TEXT("magic_armor"), &UPetEpitome::OnRep_magic_armor);
	PtrMap.Add(TEXT("criticalstrike"), &UPetEpitome::OnRep_criticalstrike);
	PtrMap.Add(TEXT("parry"), &UPetEpitome::OnRep_parry);
	PtrMap.Add(TEXT("speed"), &UPetEpitome::OnRep_speed);
	PtrMap.Add(TEXT("hitrate"), &UPetEpitome::OnRep_hitrate);
	PtrMap.Add(TEXT("dodgerate"), &UPetEpitome::OnRep_dodgerate);
	PtrMap.Add(TEXT("gangQiValue"), &UPetEpitome::OnRep_gangQiValue);
	PtrMap.Add(TEXT("gangQiValue_Max"), &UPetEpitome::OnRep_gangQiValue_Max);
	PtrMap.Add(TEXT("gangQi_damagePoint"), &UPetEpitome::OnRep_gangQi_damagePoint);
	PtrMap.Add(TEXT("gangQi_armorPoint"), &UPetEpitome::OnRep_gangQi_armorPoint);
	PtrMap.Add(TEXT("combatPower"), &UPetEpitome::OnRep_combatPower);
	PtrMap.Add(TEXT("petShenTongSKill"), &UPetEpitome::OnRep_petShenTongSKill);
}

UPetEpitome::~UPetEpitome()
{
	PtrMap.Empty();
}

FString UPetEpitome::GetName()
{
	if (name.IsEmpty())
	{
		return uname;
	}
	return name;
}

void UPetEpitome::UpdateData(FString& attrName, FString& value)
 {
	if (PtrMap.Contains(attrName))
	{
		(this->*(PtrMap[attrName]))(value);
	}
	else
	{
		CS3_Warning(TEXT("Cannot find pet attr(%s),update fail!!"), *attrName);
	}		
}

void UPetEpitome::GetPetShenTongSKillTimes(int32 SkillID, int32 & Times)
{
	Times = 0;
	if (petShenTongSKill.Contains(SkillID))
	{
		Times = petShenTongSKill[SkillID];
	}
}

void UPetEpitome::OnRep_ability(FString& newValue)
{
	ability = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_ability_Max(FString& newValue)
{
	ability_Max = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_step(FString& newValue)
{
	step = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_name(FString& newValue)
{
	name = newValue;
}

void UPetEpitome::OnRep_sleepTime(FString& newValue)
{
	sleepTime = newValue;
}

void UPetEpitome::OnRep_attrSkillBox(FString& newValue)
{
	attrSkillBox.Empty();
	newValue.RemoveFromStart(TEXT("["));
	newValue.RemoveFromEnd(TEXT("]"));
	TArray<FString> SkillIDs = UGolbalBPFunctionLibrary::SplitString(newValue, false, TEXT(","));
	for (auto IT:SkillIDs)
	{
		attrSkillBox.Add(FSTRING_TO_INT(IT));
	}
}

void UPetEpitome::OnRep_passiveSkillBox(FString& newValue)
{
	passiveSkillBox.Empty();
	newValue.RemoveFromStart(TEXT("["));
	newValue.RemoveFromEnd(TEXT("]"));
	TArray<FString> SkillIDs = UGolbalBPFunctionLibrary::SplitString(newValue, false, TEXT(","));
	for (auto IT : SkillIDs)
	{
		passiveSkillBox.Add(FSTRING_TO_INT(IT));
	}

}

void UPetEpitome::OnRep_noLearnedSkillBox(FString& newValue)
{
	noLearnedSkillBox.Empty();
	newValue.RemoveFromStart(TEXT("["));
	newValue.RemoveFromEnd(TEXT("]"));
	TArray<FString> SkillIDs = UGolbalBPFunctionLibrary::SplitString(newValue, false, TEXT(","));
	for (auto IT : SkillIDs)
	{
		noLearnedSkillBox.Add(FSTRING_TO_INT(IT));
	}

}

void UPetEpitome::OnRep_corporeity(FString& newValue)
{
	corporeity = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_strength(FString& newValue)
{
	strength = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_intellect(FString& newValue)
{
	intellect = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_discern(FString& newValue)
{
	discern = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_dexterity(FString& newValue)
{
	dexterity = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_HP(FString& newValue)
{
	HP = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_MP(FString& newValue)
{
	MP = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_HP_Max(FString& newValue)
{
	HP_Max = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_MP_Max(FString& newValue)
{
	MP_Max = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_damage(FString& newValue)
{
	damage = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_magic_damage(FString& newValue)
{
	magic_damage = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_armor(FString& newValue)
{
	armor = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_magic_armor(FString& newValue)
{
	magic_armor = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_criticalstrike(FString& newValue)
{
	criticalstrike = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_parry(FString& newValue)
{
	parry = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_speed(FString& newValue)
{
	speed = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_hitrate(FString& newValue)
{
	hitrate = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_dodgerate(FString& newValue)
{
	dodgerate = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_gangQiValue(FString& newValue)
{
	gangQiValue = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_gangQiValue_Max(FString& newValue)
{
	gangQiValue_Max = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_gangQi_damagePoint(FString& newValue)
{
	gangQi_damagePoint = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_gangQi_armorPoint(FString& newValue)
{
	gangQi_armorPoint = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_combatPower(FString& newValue)
{
	combatPower = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_ice_damage(FString & newValue)
{
	ice_damage = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_fire_damage(FString & newValue)
{
	fire_damage = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_thunder_damage(FString & newValue)
{
	thunder_damage = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_xuan_damage(FString & newValue)
{
	xuan_damage = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_ice_armor(FString & newValue)
{
	ice_armor = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_fire_armor(FString & newValue)
{
	fire_armor = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_thunder_armor(FString & newValue)
{
	thunder_armor = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_xuan_armor(FString & newValue)
{
	xuan_armor = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_damage_ignore(FString & newValue)
{
	damage_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_magic_damage_ignore(FString & newValue)
{
	magic_damage_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_armor_ignore(FString & newValue)
{
	armor_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_magic_armor_ignore(FString & newValue)
{
	magic_armor_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_criticalstrike_ignore(FString & newValue)
{
	criticalstrike_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_parry_ignore(FString & newValue)
{
	parry_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_hitrate_ignore(FString & newValue)
{
	hitrate_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_dodgerate_ignore(FString & newValue)
{
	dodgerate_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_ice_damage_ignore(FString & newValue)
{
	ice_damage_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_fire_damage_ignore(FString & newValue)
{
	fire_damage_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_thunder_damage_ignore(FString & newValue)
{
	thunder_damage_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_xuan_damage_ignore(FString & newValue)
{
	xuan_damage_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_ice_armor_ignore(FString & newValue)
{
	ice_armor_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_fire_armor_ignore(FString & newValue)
{
	fire_armor_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_thunder_armor_ignore(FString & newValue)
{
	thunder_armor_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_xuan_armor_ignore(FString & newValue)
{
	xuan_armor_ignore = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_depress_resist(FString & newValue)
{
	depress_resist = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_hitback_resist(FString & newValue)
{
	hitback_resist = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_control_resist(FString & newValue)
{
	control_resist = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_insane_resist(FString & newValue)
{
	insane_resist = FSTRING_TO_INT(newValue);
}

void UPetEpitome::OnRep_petShenTongSKill(FString& newValue)
{
	petShenTongSKill.Empty();
	petShenTongSKillList.Empty();
	newValue.RemoveFromStart(TEXT("["));
	newValue.RemoveFromEnd(TEXT("]"));
	TArray<FString> strList = UGolbalBPFunctionLibrary::SplitString(newValue, false, TEXT(","));
	TArray<int32>TempShenTongSKillList;
	for (auto i : strList)
	{
		i.RemoveFromStart(TEXT(" "));
		i.RemoveFromStart(TEXT("{"));
		i.RemoveFromEnd(TEXT("}"));
		TArray<FString> ShenTongStr = UGolbalBPFunctionLibrary::SplitString(i, false, TEXT(":"));
		petShenTongSKill.Add(FSTRING_TO_INT(ShenTongStr[0]), FSTRING_TO_INT(ShenTongStr[1]));
		TempShenTongSKillList.Add(FSTRING_TO_INT(ShenTongStr[0]));
	}
	for (int32 i = 0; i < TempShenTongSKillList.Num(); ++i)
	{
		petShenTongSKillList.Add(TempShenTongSKillList[TempShenTongSKillList.Num() - 1 - i]);
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdatePetShenTongSkillEvent.Broadcast(uid);
	}
}