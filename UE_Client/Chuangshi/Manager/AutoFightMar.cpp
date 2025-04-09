// Fill out your copyright notice in the Description page of Project Settings.


#include "AutoFightMar.h"
#include"Chuangshi.h"

UAutoFightMar* UAutoFightMar::NewInstance()
{
	cs3_checkNoReentry();
	UAutoFightMar* autoFightMar = (UAutoFightMar*)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_AutoFightMar")));
	return autoFightMar;
}

UAutoFightMar* UAutoFightMar::GetInstanceByCS3GameInstance()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->AutoFightMar : nullptr;
}
