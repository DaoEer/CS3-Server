
// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3LightComponent.h"
#include "Components/DirectionalLightComponent.h"
#include "Actor/ServerCharacter.h"
#include "GameData/PlayerLightData.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/LevelManager.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/CfgManager.h"

#if WITH_EDITOR
#include "LevelEditor.h"
#include "LevelEditorViewport.h"
#include "SLevelViewport.h"
#endif

#include "Kismet/KismetSystemLibrary.h"
#include "ModuleManager.h"
#include "Engine/EngineTypes.h"
#include "Actor/Player/PlayerCharacter.h"

using namespace EWorldType;

CONTROL_COMPILE_OPTIMIZE_START

// Sets default values for this component's properties
UCS3LightComponent::UCS3LightComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;
	if (!IsValid(GetWorld()))
		return;
#if WITH_EDITOR
	if (GetWorld()->WorldType == EWorldType::Editor)
	{
		// Get the Level editor module and request the Active Viewport.
		FLevelEditorModule& LevelEditorModule = FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor");

		ActiveLevelViewport = (SLevelViewport*)(LevelEditorModule.GetFirstActiveViewport().Get());
	}
#endif // WITH_EDITOR
}

// Called when the game starts
void UCS3LightComponent::BeginPlay()
{
	Super::BeginPlay();
	AServerCharacter* ServerPlayer = Cast<AServerCharacter>(GetOwner());
	if (!IsValid(SceneLight))
	{
		LightTag = false;
		CreateLight();
	}
}


void UCS3LightComponent::CreateLight()
{
	SceneLight = NewObject<UDirectionalLightComponent>(this, TEXT("SceneLight"));
	SceneLight->CastShadows = 0;
	SceneLight->LightingChannels.bChannel0 = false;
	//SceneLight->LightingChannels.bChannel3 = true;
	SceneLight->Intensity = 3.0f;
 	SceneLight->RegisterComponent();
	SceneLight->bAffectTranslucentLighting = false;
	SceneLight->CastTranslucentShadows = false;
	SceneLight->SetVisibility(false);
}

void UCS3LightComponent::InitLightData()
{
	auto PlayerLightData = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PLAYER_LIGHT_DATA);
	FString lightname = UGolbalBPFunctionLibrary::LevelManager()->GetCurrLevelName().ToString();
	const FPLAYER_LIGHT_DATA* lightdata = PlayerLightData->GetRow<FPLAYER_LIGHT_DATA>(lightname);
	if (lightdata != nullptr)
	{
		SceneLight->Intensity = lightdata->LightIntensity;
		SceneLight->SetLightColor(lightdata->LightColor);
		SceneLight->SetAffectTranslucentLighting(false);
		SceneLight->SetVisibility(true);
	}
}

// Called every frame
void UCS3LightComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (!IsValid(GetWorld()))
		return;

#if WITH_EDITOR
	if (ActiveLevelViewport != nullptr)
	{
		UCameraComponent* Pilot = ActiveLevelViewport->GetLevelViewportClient().GetCameraComponentForView();
		if (ActiveLevelViewport->GetLevelViewportClient().IsLockedToMatinee())
		{
			if (Pilot->GetOwner() == GetOwner())
			{
				SceneLight->SetVisibility(true);
			}
			else
			{
				SceneLight->SetVisibility(false);
			}
		}
	}
#endif // WITH_EDITOR
 

	if (LightTag && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()))
	{
		AActor* viewTarget = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetViewTarget();
		if (IsValid(viewTarget) && IsValid(SceneLight) && viewTarget == GetOwner() && !SceneLight->IsVisible())
		{
			SceneLight->SetVisibility(true);
		}
	}

}

CONTROL_COMPILE_OPTIMIZE_END