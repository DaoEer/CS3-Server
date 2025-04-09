// Fill out your copyright notice in the Description page of Project Settings.
#include "MAI_Dec_IsStateShow.h"

#include "Actor/Monster/MonsterCharacter.h"
#include "Entity/Monster/CMonster.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/StateInterface.h"
#include "GameData/GameDeFine.h"



bool UMAI_Dec_IsStateShow::CalculateRawConditionValue(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) const
{
	return EntityIsState(OwnerComp, ENTITY_STATE::EntityStateShow);
}