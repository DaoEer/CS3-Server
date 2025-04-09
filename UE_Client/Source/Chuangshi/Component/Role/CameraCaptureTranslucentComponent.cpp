// Fill out your copyright notice in the Description page of Project Settings.

#include "CameraCaptureTranslucentComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Camera/CameraComponent.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Engine/TextureRenderTarget2D.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetMaterialLibrary.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Components/SceneComponent.h"


// Sets default values for this component's properties
UCameraCaptureTranslucentComponent::UCameraCaptureTranslucentComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	CaptureSource = SCS_SceneColorSceneDepth;
	bCaptureEveryFrame = true;
	PrimitiveRenderMode = ESceneCapturePrimitiveRenderMode::PRM_UseShowOnlyList;
	SetComponentTickEnabled(true);

	ShowFlags.SetAntiAliasing(false);
	ShowFlags.SetBSP(false);
	ShowFlags.SetDecals(false);
	ShowFlags.SetFog(false);
	ShowFlags.SetLandscape(false);
	ShowFlags.SetTranslucency(false);
	ShowFlags.SetAtmosphericFog(false);
	ShowFlags.SetTemporalAA(false);
	ShowFlags.SetBloom(false);
	ShowFlags.SetEyeAdaptation(false);
	ShowFlags.SetSkyLighting(false);
	ShowFlags.SetAmbientOcclusion(false);
	ShowFlags.SetDynamicShadows(false);
	ShowFlags.SetAmbientCubemap(false);
	ShowFlags.SetDistanceFieldAO(false);
	ShowFlags.SetLightFunctions(false);
	ShowFlags.SetLightShafts(false);
	ShowFlags.SetReflectionEnvironment(false);
	ShowFlags.SetScreenSpaceReflections(false);
	ShowFlags.SetTexturedLightProfiles(false);
	ShowFlags.SetVolumetricFog(false);
	ShowFlags.SetPostProcessing(false);
}


// Called when the game starts
void UCameraCaptureTranslucentComponent::BeginPlay()
{
	Init();
	Super::BeginPlay();

	// ...
}

void UCameraCaptureTranslucentComponent::Init()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player) || !Player->CameraComponent)
	{
		return;
	}
	// 渲染目标
	UTextureRenderTarget2D* RenderTarget_ = NewObject<UTextureRenderTarget2D>();
	const FVector2D ViewportSize = FVector2D(GEngine->GameViewport->Viewport->GetSizeXY());
	RenderTarget_->InitAutoFormat(ViewportSize.X, ViewportSize.Y);
	RenderTarget_->RenderTargetFormat = RTF_RGBA16f;
	RenderTarget_->UpdateResourceImmediate(true);

	TextureTarget = RenderTarget_;
	//  后处理材质
	UMaterial* Material = LoadObject<UMaterial>(NULL, TEXT("/Game/Materials/M_PostProcess_Translucent.M_PostProcess_Translucent"), NULL, LOAD_None, NULL);
	if (Material)
	{
		M_PTranslucentInst = UKismetMaterialLibrary::CreateDynamicMaterialInstance(GetWorld(), Material);
		M_PTranslucentInst->SetTextureParameterValue(TEXT("RenderTarget"), RenderTarget_);
		Player->CameraComponent->PostProcessSettings.WeightedBlendables.Array.Add(FWeightedBlendable(1.0f, M_PTranslucentInst));
	}
}

void UCameraCaptureTranslucentComponent::SetWarnTips(const uint8& BWarn)
{
	if (IsValid( M_PTranslucentInst))
	{
		if (BWarn)
		{
			// 有效 ！蓝色
			M_PTranslucentInst->SetVectorParameterValue(TEXT("WarnColor"), FLinearColor(0, 0.1, 0.8, 0));
		}
		else
		{
			// 无效！ 红色
			M_PTranslucentInst->SetVectorParameterValue(TEXT("WarnColor"), FLinearColor(0.6, 0, 0, 0));
		}
	}
}

void UCameraCaptureTranslucentComponent::AddTranslucentComponent(AActor* InActor)
{
	if (!IsValid(InActor))return;
	TInlineComponentArray<UMeshComponent*> PrimitiveComponents;
	InActor->GetComponents(PrimitiveComponents);
	for (auto component : PrimitiveComponents)
	{
		ShowOnlyComponent(component);
		APlayerController* PlayerController = UGameplayStatics::GetPlayerController(GetWorld(), 0);
		if (IsValid(PlayerController) && !PlayerController->HiddenPrimitiveComponents.Contains(component))
		{
			PlayerController->HiddenPrimitiveComponents.Add(component);
		}
	}
}

void UCameraCaptureTranslucentComponent::RemoveTranslucentComponent(AActor* InActor)
{
	ClearShowOnlyComponents();
	TInlineComponentArray<UMeshComponent*> PrimitiveComponents;
	InActor->GetComponents(PrimitiveComponents);
	for (auto component : PrimitiveComponents)
	{
		APlayerController* PlayerController = UGameplayStatics::GetPlayerController(GetWorld(), 0);
		if (PlayerController->HiddenPrimitiveComponents.Contains(component))
		{
			PlayerController->HiddenPrimitiveComponents.Remove(component);
		}
	}

	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!Player || !Player->CameraComponent)
	{
		return;
	}
	for (int32 i = 0; i < Player->CameraComponent->PostProcessSettings.WeightedBlendables.Array.Num(); i++)
	{
		if (Player->CameraComponent->PostProcessSettings.WeightedBlendables.Array[i].Object == M_PTranslucentInst)
		{
			Player->CameraComponent->PostProcessSettings.WeightedBlendables.Array.RemoveAt(i);
			M_PTranslucentInst = nullptr;
			break;
		}
	}
}


// Called every frame
void UCameraCaptureTranslucentComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	// ...
}

