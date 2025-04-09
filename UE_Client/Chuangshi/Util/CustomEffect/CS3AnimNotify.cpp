// Fill out your copyright notice in the Description page of Project Settings.

#include "CS3AnimNotify.h"
#include "../CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

UCS3AnimNotify::UCS3AnimNotify()
{

}


CONTROL_COMPILE_OPTIMIZE_END

void UCS3AnimNotify::StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{ 
	Received_StopNotifyEffect(MeshComp, Animation);
}
