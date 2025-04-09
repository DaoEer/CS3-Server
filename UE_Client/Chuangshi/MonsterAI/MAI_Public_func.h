// Fill out your copyright notice in the Description page of Project Settings.
#pragma once
#include "CoreMinimal.h"
#include "KBEngine.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/CS3Entity.h"
#include "Interface/CombatInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Entity/Role/CS3PlayRole.h"


KBEngine::Entity* GetEntity(int32 eid)
{
	KBEngine::Entity* e = UGolbalBPFunctionLibrary::FindEntity(eid);
	if (e != nullptr)
	{
		return e;
	}
	return nullptr;
}

CS3Entity* GetCS3Entity(int32 eid)
{
	KBEngine::Entity* e = UGolbalBPFunctionLibrary::FindEntity(eid);
	if (e != nullptr)
	{
		return static_cast<CS3Entity*>(e);
	}
	return nullptr;
}

int GetPlayerActorID()
{
	return UGolbalBPFunctionLibrary::GetPlayerID();
}

CS3PlayRole* GetPlayerEntity()
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		return nullptr;
	}
	KBEngine::Entity* playr = UUECS3GameInstance::pKBEApp->Player();
	if (playr == nullptr)
	{
		return nullptr;
	}
	return static_cast<CS3PlayRole*>(playr);
}

APlayerCharacter* GetPlayerActor()
{
	CS3PlayRole* player = GetPlayerEntity();
	if (player == nullptr)
	{
		return nullptr;
	}
	else {
		return Cast< APlayerCharacter >( player->Actor() );
	}
}


