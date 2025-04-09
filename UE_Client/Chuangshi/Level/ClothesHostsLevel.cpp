// Fill out your copyright notice in the Description page of Project Settings.


#include "ClothesHostsLevel.h"
#include "Manager/LevelManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/ModifyFaceManager.h"
#include "CS3Base/UIManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/LocalDataSaveManager.h"

void AClothesHostsLevel::BeginPlay()
{
	Super::BeginPlay();
	if (IsValid(InputComponent))
	{
		InputComponent->BindKey(EKeys::Escape, EInputEvent::IE_Pressed, this, &AClothesHostsLevel::HideSettleAccounts);
	}
	SetScreenPercentage();
}

void AClothesHostsLevel::CreateDynamicRes()
{
	ModifyFaceCharacter = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("ClothesCharacter"));
	//显示商城界面
	UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::Personalize, TEXT("AppearanceMall"));
}

void AClothesHostsLevel::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	ResetScreenPercentage();
	Super::EndPlay(EndPlayReason);
}

void AClothesHostsLevel::OnLoadLevelFinished()
{
	UGolbalBPFunctionLibrary::LevelManager()->OnEndTeleportChangeClothesLevel();
}

void AClothesHostsLevel::HideSettleAccounts()
{
	UGolbalBPFunctionLibrary::GUIManager()->OrderHideWindows();
}

void AClothesHostsLevel::SetScreenPercentage()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager) && IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData))
	{
		int32 ScreenPercentage = UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->VideoSettingData.ScreenPercentage;

		TArray<int> ScreenPercentages = { 75,85,100,150 };
		const FSYSTEM_DEFAULT_DATA* SystemData = UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->GetDefaultSystemData();
		if (SystemData)
		{
			ScreenPercentages = SystemData->RangeValueVideoData.ScreenPercentages;
		}

		//是否是完美画质
		if ((ScreenPercentages.Num() - 1) != ScreenPercentage)
		{
			//FString cmd = TEXT("r.ScreenPercentage 150");
			FString cmd = TEXT("r.ScreenPercentage ") + INT_TO_FSTRING(ScreenPercentages[ScreenPercentages.Num() - 1]);
			UKismetSystemLibrary::ExecuteConsoleCommand(UUECS3GameInstance::Instance->GetWorld(), cmd);
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("AClothesHostsLevel::SetScreenPercentage   r.ScreenPercentage  ==%s "), *cmd);
		}
	}
}

void AClothesHostsLevel::ResetScreenPercentage()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager) && IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData))
	{
		int32 ScreenPercentage = UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->VideoSettingData.ScreenPercentage;

		TArray<int> ScreenPercentages = { 75,85,100,150 };
		const FSYSTEM_DEFAULT_DATA* SystemData = UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->GetDefaultSystemData();
		if (SystemData)
		{
			ScreenPercentages = SystemData->RangeValueVideoData.ScreenPercentages;
		}

		UWorld* world = UUECS3GameInstance::Instance->GetWorld();
		FString cmd = "";

		if (ScreenPercentages.Num() > ScreenPercentage)
		{
			cmd = TEXT("r.ScreenPercentage ") + INT_TO_FSTRING(ScreenPercentages[ScreenPercentage]);
			UKismetSystemLibrary::ExecuteConsoleCommand(world, cmd);
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("AClothesHostsLevel::ResetScreenPercentage   r.ScreenPercentage  ==%s "), *cmd);
		}
	}
}
