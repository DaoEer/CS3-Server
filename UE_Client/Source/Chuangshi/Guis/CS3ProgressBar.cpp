// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3ProgressBar.h"
#include "UnrealMathUtility.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/ResourceManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ResourceManager.h"



UCS3ProgressBar::UCS3ProgressBar(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{

}

void UCS3ProgressBar::SetProgressPercent(float InPercent)
{
	CurPercent = Percent;
	DstPercent = InPercent;
	TotalTime = FMath::Abs((DstPercent - CurPercent)/ Velocity);
	StartCdTime();
}

void UCS3ProgressBar::BeginDestroy()
{
	if (IsValid(this) && IsValid(UUECS3GameInstance::Instance))
	{
		if (IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearAllTimersForObject(this);
		}
		if (IsValid(UUECS3GameInstance::Instance->ResourceManager))
		{
			UUECS3GameInstance::Instance->ResourceManager->ReleaseHandlesByObject(this);
		}
	}
	Super::BeginDestroy();
}

void UCS3ProgressBar::StartCdTime()
{
	StopCdTime();
	ShowClipShader();
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(CdTimerHandle, this, &UCS3ProgressBar::ShowClipShader, IntervalTime, true);
}

void UCS3ProgressBar::StopCdTime()
{
	if (CdTimerHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CdTimerHandle);
	}
}

void UCS3ProgressBar::ShowClipShader()
{
	if (TotalTime > IntervalTime)
	{
		TotalTime = TotalTime - IntervalTime;
		if (DstPercent >= CurPercent)
		{
			CurPercent = CurPercent + (Velocity * IntervalTime);
		}
		else
		{
			CurPercent = CurPercent - (Velocity * IntervalTime);
		}
		Super::SetPercent(CurPercent);
	}
	else
	{
		SetPercent(DstPercent);///<防止有小数偏差，最后再设置一下
		StopCdTime();
	}
}