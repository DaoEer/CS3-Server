
#include "MoveTrapInterface.h"
#include "Actor/Trap/TrapCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMoveTrapInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMoveTrapInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMoveTrapInterface::UMoveTrapInterface()
{
}

UMoveTrapInterface::~UMoveTrapInterface()
{

}

void UMoveTrapInterface::CLIENT_ChangeProgressBar_Implementation(float value)
{
	if (IsValid(GetActor()))
	{
		ATrapCharacter* trapActor = Cast<ATrapCharacter>(GetActor());
		if (trapActor)
		{
			trapActor->ChangeProgressBar(value);
		}
	}
}
void UMoveTrapInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_ChangeProgressBar");
	Supper::InitBlueCB();
}