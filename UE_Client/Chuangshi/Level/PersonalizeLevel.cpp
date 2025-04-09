// Fill out your copyright notice in the Description page of Project Settings.

#include "PersonalizeLevel.h"
#include "Manager/LevelManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/ModifyFaceManager.h"
#include "CS3Base/UIManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/LocalDataSaveManager.h"

void APersonalizeLevel::BeginPlay()
{
	if (IsValid(InputComponent))
	{
		InputComponent->BindKey(EKeys::LeftMouseButton, EInputEvent::IE_Pressed, this, &APersonalizeLevel::SetModifyCurrBone);
	}
	Super::BeginPlay();
	SetScreenPercentage();
}

void APersonalizeLevel::CreateDynamicRes()
{
	ModifyFaceCharacter = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("ModifyFaceCharacter"));
	if(ModifyFaceCharacter)
	AccountActors.Add(ModifyFaceCharacter);
	//显示捏脸界面
	UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::Personalize, TEXT("PinchFace"));
}

void APersonalizeLevel::OnLoadLevelFinished()
{
	UGolbalBPFunctionLibrary::LevelManager()->OnEndTeleportPersonalizeLevel();
		
}

void APersonalizeLevel::SetModifyCurrBone()
{
	UGolbalBPFunctionLibrary::ModifyFaceManager()->SetCurrentBone();
}

void APersonalizeLevel::SetScreenPercentage()
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
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("APersonalizeLevel::SetScreenPercentage   r.ScreenPercentage  ==%s "), *cmd);
		}
	}
}

void APersonalizeLevel::ResetScreenPercentage()
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
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("APersonalizeLevel::ResetScreenPercentage   r.ScreenPercentage  ==%s "), *cmd);
		}
	}
}

void APersonalizeLevel::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
	{
		UBaseWindow* PinchFaceWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("PinchFace"));
		if (PinchFaceWidget)
		{
			PinchFaceWidget->Destroy();
		}
	}
	ResetScreenPercentage();
	Super::EndPlay(EndPlayReason);
	
}