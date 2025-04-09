
#include "NpcAnimInstance.h"

UNpcAnimInstance::UNpcAnimInstance()
{
	bTickUpdate = false;
}

UNpcAnimInstance::~UNpcAnimInstance()
{
}

bool UNpcAnimInstance::IsInWater()
{
	return false;
}
