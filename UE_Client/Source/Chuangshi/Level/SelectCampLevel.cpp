// Fill out your copyright notice in the Description page of Project Settings.


#include "SelectCampLevel.h"
#include "Kismet/KismetMathLibrary.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/LoaderManager.h"
#include "CS3Base/UIManager.h"
#include "Camera/CameraActor.h"
#include "Manager/LevelManager.h"

void ASelectCampLevel::BeginPlay()
{
	Super::BeginPlay();
}

void ASelectCampLevel::CreateDynamicRes()
{
	//创建并显示阵营选择关卡界面
	UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::SelectCamp, TEXT("SelectCamp")); 
}

void ASelectCampLevel::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
	{
		UBaseWindow* SelectCampWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("SelectCamp"));
		if (SelectCampWidget)
		{
			SelectCampWidget->Destroy();
		}
	}
	Super::EndPlay(EndPlayReason);
}

void ASelectCampLevel::OnLoadLevelFinished()
{
	UGolbalBPFunctionLibrary::LevelManager()->OnEndTeleportSelectCampLevel();
}

