// Fill out your copyright notice in the Description page of Project Settings.


#include "EventManager.h"
#include"Chuangshi.h"
#include "Util/GlobalFunctions.h"
#include "GameDevelop/CS3GameInstance.h"


UGEventManager::UGEventManager()
{

}

UGEventManager::~UGEventManager()
{

}

UGEventManager* UGEventManager::GetInstance()
{
	cs3_checkNoReentry();

	return (UGEventManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_GEventManager")));
}