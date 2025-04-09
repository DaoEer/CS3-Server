// Fill out your copyright notice in the Description page of Project Settings.

#include "SpellBoxSpecialInterface.h"
#include "Actor/Particle/EffectEmitter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(USpellBoxSpecialInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(USpellBoxSpecialInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

USpellBoxSpecialInterface::USpellBoxSpecialInterface()
{
}

USpellBoxSpecialInterface::~USpellBoxSpecialInterface()
{
}

void USpellBoxSpecialInterface::InitBlueCB()
{
	Supper::InitBlueCB();
}
