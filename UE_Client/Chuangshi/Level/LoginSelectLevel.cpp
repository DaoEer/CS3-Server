// Fill out your copyright notice in the Description page of Project Settings.

#include "LoginSelectLevel.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/MediaPlayerManager.h"
#include "Manager/LoginManager.h"
#include "Manager/LevelManager.h"

void ALoginSelectLevel::BeginPlay()
{
	Super::BeginPlay();
}

void ALoginSelectLevel::OnBeginPlayCGEvent()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LoginSelectLevel::OnBeginPlayCGEvent----------"));
	if (UGolbalBPFunctionLibrary::LoginManager()->OnBeginPlayCGDelegate.IsBound())
	{
		UGolbalBPFunctionLibrary::LoginManager()->OnBeginPlayCGDelegate.Broadcast();
	}
	if (IsValid(UGolbalBPFunctionLibrary::MediaPlayerManager()) && UGolbalBPFunctionLibrary::MediaPlayerManager()->OnMediaOpenedDelegate.IsBoundToObject(this))
	{
		UGolbalBPFunctionLibrary::MediaPlayerManager()->OnMediaOpenedDelegate.RemoveAll(this);
	}
}

void ALoginSelectLevel::PlayCG()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LoginSelectLevel::PlayCG----------"));
	if (IsValid(UGolbalBPFunctionLibrary::MediaPlayerManager()))
	{
		UGolbalBPFunctionLibrary::MediaPlayerManager()->PlayMedia(TEXT("1"));
		if (!UGolbalBPFunctionLibrary::MediaPlayerManager()->OnMediaEndReachedDelegate.IsBoundToObject(this))
		{
			UGolbalBPFunctionLibrary::MediaPlayerManager()->OnMediaEndReachedDelegate.AddUObject(this, &ALoginSelectLevel::PlayerCGFinished);
		}
		if (!UGolbalBPFunctionLibrary::MediaPlayerManager()->OnMediaOpenedDelegate.IsBoundToObject(this))
		{
			UGolbalBPFunctionLibrary::MediaPlayerManager()->OnMediaOpenedDelegate.AddUObject(this, &ALoginSelectLevel::OnBeginPlayCGEvent);
		}
	}
}

void ALoginSelectLevel::PlayerCGFinished()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LoginSelectLevel::PlayerCGFinished----------"));
	UGolbalBPFunctionLibrary::LevelManager()->TeleportSelectCampLevel();
	if (IsValid(UGolbalBPFunctionLibrary::MediaPlayerManager()) && UGolbalBPFunctionLibrary::MediaPlayerManager()->OnMediaEndReachedDelegate.IsBoundToObject(this))
	{
		UGolbalBPFunctionLibrary::MediaPlayerManager()->OnMediaEndReachedDelegate.RemoveAll(this);
	}
}
