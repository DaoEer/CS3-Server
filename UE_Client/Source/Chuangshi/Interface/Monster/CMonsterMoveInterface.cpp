// Fill out your copyright notice in the Description page of Project Settings.


#include "CMonsterMoveInterface.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Component/Monster/CMonsterPosSyncComponent.h"



bool UCMonsterMoveInterface::CanMoveCheck(EMoveScriptType Type)
{
	if (!IsValid(GetActor()))
	{
		return false;
	}
	return true;
}

void UCMonsterMoveInterface::RandomMove(float range) {
	if (IsValid(GetActor())) {
		AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(GetActor());
		if (IsValid(MonsterCharacter)) {
			UCMonsterPosSyncComponent* CMonsterPosSyncComponent = Cast<UCMonsterPosSyncComponent>(MonsterCharacter->GetFilterComponent());
			if (CMonsterPosSyncComponent) {
				CMonsterPosSyncComponent->StartRandomWalk(MonsterCharacter->GetActorLocation(), range);
			}
		}
	}
}

void UCMonsterMoveInterface::ChaseActor(int32 targetID) {
	AActor* Actor = UGolbalBPFunctionLibrary::GetActorByID(targetID);
	if (!IsValid(Actor) || !IsValid(GetActor())) {
		return;
	}
	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(MonsterCharacter)) {
		UCMonsterPosSyncComponent* CMonsterPosSyncComponent = Cast<UCMonsterPosSyncComponent>(MonsterCharacter->GetFilterComponent());
		if (CMonsterPosSyncComponent) {
			CMonsterPosSyncComponent->ChaseActor(Actor);
		}
	}
}

void UCMonsterMoveInterface::StopMove()
{

}


EMoveScriptType UCMonsterMoveInterface::GetMoveScriptType() {
	return MoveScriptType;
}
