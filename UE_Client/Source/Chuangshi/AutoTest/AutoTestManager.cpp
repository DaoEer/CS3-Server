// Fill out your copyright notice in the Description page of Project Settings.


#include "AutoTestManager.h"
#include "Chuangshi.h"
#include "AutoTest/FMO/FMOProfile.h"

UAutoTestManager::UAutoTestManager()
{

}

UAutoTestManager* UAutoTestManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UAutoTestManager>();
}

void UAutoTestManager::StartFMO()
{
	Profile = NewObject<UFMOProfile>(this);
	//UFMOProfile* NewProfile = Cast<UFMOProfile>(Profile);
	Profile->StartRecord();
	bIsStartFMO = true;
}

void UAutoTestManager::StopFMO()
{
	UFMOProfile* NewProfile = Cast<UFMOProfile>(Profile);
	if (IsValid(NewProfile))
	{
		if (NewProfile->GetCurrTask())
		{
			NewProfile->GetCurrTask()->bCanEverTick = false;
		}
		NewProfile->bCanEverTick = false;
		NewProfile->Tasks.Empty();
	}
	bIsStartFMO = false;
}

void UAutoTestManager::PrintFMO()
{
	UFMOProfile* NewProfile = Cast<UFMOProfile>(Profile);
	if (IsValid(NewProfile))
	{
		NewProfile->EndRecord();
	}
}
