#include "MovingPlatformRotatorInterface.h"
#include "Actor/Scene/MovingPlatformCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMovingPlatformRotatorInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMovingPlatformRotatorInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMovingPlatformRotatorInterface::UMovingPlatformRotatorInterface()
{
}

UMovingPlatformRotatorInterface::~UMovingPlatformRotatorInterface()
{
}

void UMovingPlatformRotatorInterface::notifyClientStartRotat_Implementation(FVector angle, float moveSpeed, int isContinuousMove)
{
	if (IsValid(GetActor()))
	{
		AMovingPlatformCharacter* MovingPlatformActor = Cast<AMovingPlatformCharacter>(GetActor());
		if (MovingPlatformActor)
		{
			MovingPlatformActor->OnNotifyClientStartRotat(angle, moveSpeed, isContinuousMove);
		}
	}
}

void UMovingPlatformRotatorInterface::InitBlueCB()
{
	ArrBlueFunc.Add("notifyClientStartRotat");
	Supper::InitBlueCB();
}
