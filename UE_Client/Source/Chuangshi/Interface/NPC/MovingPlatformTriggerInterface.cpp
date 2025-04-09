

#include "MovingPlatformTriggerInterface.h"
#include "Actor/Scene/MovingPlatformCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMovingPlatformTriggerInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMovingPlatformTriggerInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMovingPlatformTriggerInterface::UMovingPlatformTriggerInterface()
{
}

UMovingPlatformTriggerInterface::~UMovingPlatformTriggerInterface()
{
}

void UMovingPlatformTriggerInterface::OnReadyToMoveBack_Implementation()
{
	if (IsValid(GetActor()))
	{
		AMovingPlatformCharacter* MovingPlatformActor = Cast<AMovingPlatformCharacter>(GetActor());
		if (MovingPlatformActor)
		{
			MovingPlatformActor->OnReadyToMoveBack();
		}
	}
}

void UMovingPlatformTriggerInterface::OnReadyToMove_Implementation()
{
	if (IsValid(GetActor()))
	{
		AMovingPlatformCharacter* MovingPlatformActor = Cast<AMovingPlatformCharacter>(GetActor());
		if (MovingPlatformActor)
		{
			MovingPlatformActor->OnReadyToMove();
		}
	}
}
void UMovingPlatformTriggerInterface::InitBlueCB()
{
	ArrBlueFunc.Add("OnReadyToMoveBack");
	ArrBlueFunc.Add("OnReadyToMove");
	Supper::InitBlueCB();
}
