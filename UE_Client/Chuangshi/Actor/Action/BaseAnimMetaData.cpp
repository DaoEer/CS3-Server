// Fill out your copyright notice in the Description page of Project Settings.

#include "BaseAnimMetaData.h"


void UBaseAnimMetaData::SetInterruptedType(ACTION_INTERRUPTED_ENUM InInterruptedType)
{
	InterruptedType = InInterruptedType;
}

ACTION_INTERRUPTED_ENUM UBaseAnimMetaData::GetInterruptedType()
{
	return InterruptedType;
}
