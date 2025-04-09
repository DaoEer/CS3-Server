// Fill out your copyright notice in the Description page of Project Settings.
#include "TrapInterface.h"
#include "Actor/Trap/TrapCharacter.h"
#include "Manager/ParticleManager.h"
#include "Manager/VisibleManager.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UTrapInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UTrapInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UTrapInterface::UTrapInterface()
{
}

UTrapInterface::~UTrapInterface()
{

}
void UTrapInterface::OnRep_modelNumber()
{
	Supper::OnRep_modelNumber();
}

void UTrapInterface::OnRep_modelScale()
{
	Supper::OnRep_modelScale();
}



void UTrapInterface::OnRep_triggerShape()
{

}

void UTrapInterface::OnRep_triggerRadius()
{

}

void UTrapInterface::OnEnterTrap(int32 entityID)
{
	if (nullptr == GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTrapInterface::OnEnterTrap:GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(entityID);
	GetEntity()->CellCall(TEXT("CELL_onEnter"), Args);
}

void UTrapInterface::OnLeaveTrap(int32 entityID)
{
	if (nullptr == GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTrapInterface::OnLeaveTrap:GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(entityID);
	GetEntity()->CellCall(TEXT("CELL_onLeave"), Args);
}

void UTrapInterface::CLIENT_PlayDeadEffect_Implementation(const FString& EffectID)
{
	PlayDeadEffect_Implementation(EffectID);
}

void UTrapInterface::PlayDeadEffect_Implementation(const FString& EffectID)
{
	if (EffectID.IsEmpty())return;
	ATrapCharacter* trap = Cast<ATrapCharacter>(GetActor());
	if (IsValid(trap))
	{
		UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(trap);
		UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, trap, trap);
	}
}

void UTrapInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_PlayDeadEffect");
	Supper::InitBlueCB();
}
