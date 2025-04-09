// Fill out your copyright notice in the Description page of Project Settings.


#include "NPCInterface.h"
#include "Actor/NPC/NPCCharacter.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UNPCInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UNPCInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UNPCInterface::UNPCInterface()
{
}

UNPCInterface::~UNPCInterface()
{

}

void UNPCInterface::OnRep_modelNumber()
{
	Supper::OnRep_modelNumber();
}

void UNPCInterface::OnRep_modelScale()
{
	Supper::OnRep_modelScale();
}

void UNPCInterface::CLIENT_BubbleDialogue(const FString& voice)
{
	ANPCCharacter* Character = Cast<ANPCCharacter>(GetActor());
	if (IsValid(Character))
	{
		Character->BubbleDialogue(voice);
	}
}


void UNPCInterface::RPC_talkWith(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error: UNPCInterface::RPC_talkWith : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);
	entity->CellCall(TEXT("talkWith"), args);
}

void UNPCInterface::onCollisionBegin()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNPCInterface::onCollisionBegin : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("onCollisionBegin"), args);
}

void UNPCInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_BubbleDialogue");
	Supper::InitBlueCB();
}