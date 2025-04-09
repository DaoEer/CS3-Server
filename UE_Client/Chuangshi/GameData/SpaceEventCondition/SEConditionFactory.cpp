// Fill out your copyright notice in the Description page of Project Settings.


#include "SEConditionFactory.h"
#include "GameData/SpaceEventCondition/SECondition3.h"
#include "GameData/SpaceEventCondition/SECondition18.h"

USEConditionBase* USEConditionFactory::CreateConditionByClass(FString ScriptName)
{
	if (ScriptName == "SECondition3")
	{
		return NewObject<USECondition3>();
	}
	if (ScriptName == "SECondition18")
	{
		return NewObject<USECondition18>();
	}
	else
	{
		return NewObject<USEConditionBase>();
	}
};


