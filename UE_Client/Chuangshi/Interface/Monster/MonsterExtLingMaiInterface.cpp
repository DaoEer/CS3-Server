	// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtLingMaiInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/BaseWindow.h"
#include "CS3Base/UIManager.h"
#include "Manager/EventManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtLingMaiInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtLingMaiInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtLingMaiInterface::UMonsterExtLingMaiInterface()
{
	
}

UMonsterExtLingMaiInterface::~UMonsterExtLingMaiInterface()
{
	
}

void UMonsterExtLingMaiInterface::onEnterWorld()
{
	Supper::onEnterWorld();
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("LingMaiBattleFieldBossHPBar"));
	}
}

void UMonsterExtLingMaiInterface::onLeaveWorld()
{
	Supper::onLeaveWorld();
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UBaseWindow* LMBattleBossHPBar = UUECS3GameInstance::Instance->GUIManager->GetWindow("LingMaiBattleFieldBossHPBar");
		if(IsValid(LMBattleBossHPBar))
		{
			LMBattleBossHPBar->Hide();
		}	
	}
	
}

void UMonsterExtLingMaiInterface::OnRep_xianDamage()
{
	xianDamage = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("xianDamage"));
	int32 HP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("HP_Max"));
	float DamagePercent = float(xianDamage) / float(HP_Max);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnLingMaiBossDamageChanged.Broadcast(1, DamagePercent);
	}
	LingMaiBossHPChanged();
}

void UMonsterExtLingMaiInterface::OnRep_moDamage()
{
	moDamage = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("moDamage"));
	int32 HP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("HP_Max"));
	float DamagePercent = float(moDamage) / float(HP_Max);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnLingMaiBossDamageChanged.Broadcast(2, DamagePercent);
	}
	LingMaiBossHPChanged();
}
void UMonsterExtLingMaiInterface::LingMaiBossHPChanged()
{
	int32 HP = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("HP"));
	int32 HP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("HP_Max"));
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnLingMaiBossHPChanged.Broadcast(HP, HP_Max);
	}
}
void UMonsterExtLingMaiInterface::InitBlueCB()
{
	UMonsterInterface::InitBlueCB();
}




