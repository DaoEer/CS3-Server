// Fill out your copyright notice in the Description page of Project Settings.

#include "FlyBindCharacter.h"

AFlyBindCharacter::AFlyBindCharacter()
{
	CharacterClassName = TEXT("FlyBindCharacter");
}

void AFlyBindCharacter::initFlyBindActor(const FFLY_BIND_MESH_DATA* Config, int32 PlayerId)
{
	SplineAsset = Config->SplineAsset;
	LoopNumber = Config->FlyLoopNumber;
	FlySpeed = Config->FlySpeed;
	bIsAbsoluteLocation = Config->IsAbsoluteLocation;
	bIsAbsoluteRotation = Config->IsAbsoluteRotation;
	bIsAbsoluteScale = Config->IsAbsoluteScale;
	SkillType = Config->SkillType;
	AnimID = Config->AnimID;
	EffectID = Config->EffectID;
	PlayTime = Config->PlayTime;
	FlyModeBindSocket = Config->FlyModeBindSocket;
	PlayerID = PlayerId;
	FlyTransform = Config->FlyTransform;
	FlySplineTransform = Config->FlySplineTransform;
	OnInitFromConfig();
}
