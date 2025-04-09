// Fill out your copyright notice in the Description page of Project Settings.


#include "SpellBoxAdvancedInterface.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(USpellBoxAdvancedInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(USpellBoxAdvancedInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

USpellBoxAdvancedInterface::USpellBoxAdvancedInterface()
{
}

USpellBoxAdvancedInterface::~USpellBoxAdvancedInterface()
{
}
void USpellBoxAdvancedInterface::CELL_reqInterruptInteractive()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USpellBoxAdvancedInterface::CELL_reqInterruptInteractive : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("CELL_reqInterruptInteractive"), args);
	
}

void USpellBoxAdvancedInterface::CELL_reqStartInteractive()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USpellBoxAdvancedInterface::CELL_reqStartInteractive : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("CELL_reqStartInteractive"), args);
}