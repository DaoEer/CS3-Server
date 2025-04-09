// Fill out your copyright notice in the Description page of Project Settings.
#include "MoveScriptBase.h"


MoveScriptBase::MoveScriptBase(APawn* InPawn, float _AcceptanceRaius) {
	Owner = InPawn;
	AcceptanceRadius = _AcceptanceRaius;
	bIsMoveOver = false;
}

APawn* MoveScriptBase::GetOwner() {
	return Owner;
}

bool MoveScriptBase::IsMoveOver() {
	return bIsMoveOver;
}

void MoveScriptBase::OnMoveOver() {
	bIsMoveOver = true;
}

void MoveScriptBase::DoMove() {

}

void MoveScriptBase::MoveReachCheck() {

}