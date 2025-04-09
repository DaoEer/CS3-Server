// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3CineCameraActor.h"
#include "CineCameraComponent.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Kismet/KismetRenderingLibrary.h"
#include "Kismet/KismetMaterialLibrary.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

ACS3CineCameraActor::ACS3CineCameraActor(const FObjectInitializer& ObjectInitializer)
	:Super(ObjectInitializer)
{

	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	//初始化场景捕捉组件
	SceneCapture = CreateDefaultSubobject<USceneCaptureComponent2D>(TEXT("SceneCapture"));
	SceneCapture->CaptureSource = ESceneCaptureSource::SCS_SceneDepth;
	SceneCapture->PrimitiveRenderMode = ESceneCapturePrimitiveRenderMode::PRM_UseShowOnlyList;
	SceneCapture->ShowFlags.SetDynamicShadows(false);

	SceneCapture->SetupAttachment(GetCineCameraComponent());
#if WITH_EDITOR
	GetCineCameraComponent()->FilmbackSettings.SensorWidth = 36;
	GetCineCameraComponent()->FilmbackSettings.SensorHeight = 20.25;
	GetCineCameraComponent()->bConstrainAspectRatio = true;
#else
	GetCineCameraComponent()->bConstrainAspectRatio = false;
#endif	
}

void ACS3CineCameraActor::BeginPlay()
{
	Super::BeginPlay();
	///<避免在蓝图中修改了bConstrainAspectRatio 导致在非编辑器模式下bConstrainAspectRatio的值不对
#if WITH_EDITOR
#else
	GetCineCameraComponent()->bConstrainAspectRatio = false;
#endif	

}

void ACS3CineCameraActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	OutLineEffectToCamera();
	UpdateCineCameraFocusMethod();
}

void ACS3CineCameraActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{	
	Super::EndPlay(EndPlayReason);
}

void ACS3CineCameraActor::OutLineEffectToCamera()
{
	if (OpenOutLine)
	{
		class UCineCameraComponent* StoryCameraComponent = GetCineCameraComponent();
		if (StoryCameraComponent->IsValidLowLevel() && SceneCapture->IsValidLowLevel())
		{
			if (!IsValid(SceneCapture->TextureTarget))
			{
				SceneCapture->TextureTarget = UKismetRenderingLibrary::CreateRenderTarget2D(this, DepthTexSize, DepthTexSize);
			}
			///设置捕获组件参数值

			SceneCapture->PrimitiveRenderMode = ESceneCapturePrimitiveRenderMode::PRM_UseShowOnlyList;
			TArray<AActor*> actorref;
			actorref.Add(ActorRef);
			SceneCapture->ShowOnlyActors = actorref;
			SceneCapture->FOVAngle = StoryCameraComponent->FieldOfView;
			SceneCapture->SetCaptureSortPriority(10);
			SceneCapture->CaptureSource = ESceneCaptureSource::SCS_DeviceDepth;
			SceneCapture->SetVisibility(true);
			///设置Post材质属性
			if (PostMaterial && IsValid(DynamicMaterial))
			{
				SetDynamicMaterial(DynamicMaterial);
			}
		}
	}
}
	
void ACS3CineCameraActor::UpdateCineCameraFocusMethod()
{
	UCineCameraComponent* StoryCameraComponent = GetCineCameraComponent();
	if (bIsChangeFocusMethod && IsValid(StoryCameraComponent) && StoryCameraComponent->FocusSettings.FocusMethod != FocusMethod)
	{
		StoryCameraComponent->FocusSettings.FocusMethod = FocusMethod;
	}
}

void ACS3CineCameraActor::UpdateCineCameraFocusSettings(float ManualFocusDistance,float FocalLength, float Aperture)
{
	UCineCameraComponent* StoryCameraComponent = GetCineCameraComponent();
	if (IsValid(StoryCameraComponent))
	{
		StoryCameraComponent->FocusSettings.FocusMethod = ECameraFocusMethod::Manual;
		StoryCameraComponent->FocusSettings.ManualFocusDistance = ManualFocusDistance;
		StoryCameraComponent->CurrentFocalLength = FocalLength;
		StoryCameraComponent->CurrentAperture	= Aperture;
	}
}

void ACS3CineCameraActor::SetMaterialInstanceDynamic()
{
	if(PostMaterial == nullptr) return;
	
	class UCineCameraComponent* StoryCameraComponent = GetCineCameraComponent();
	DynamicMaterial = UKismetMaterialLibrary::CreateDynamicMaterialInstance(this, PostMaterial, TEXT("OutlinePP"));
	FWeightedBlendable Element(1.0f, DynamicMaterial);
	StoryCameraComponent->PostProcessSettings.WeightedBlendables.Array.Add(Element);
	SetDynamicMaterial(DynamicMaterial);
}

void ACS3CineCameraActor::SetDynamicMaterial(UMaterialInstanceDynamic* material)
{
	if (IsValid(material))
	{
		material->SetTextureParameterValue(TEXT("SampleDepth"), SceneCapture->TextureTarget);
		material->SetScalarParameterValue(TEXT("SampleDepthSize"), DepthTexSize);
		material->SetVectorParameterValue(TEXT("OutlineColor"), OutLineColor);
		material->SetScalarParameterValue(TEXT("OutlineWidth"), OutlineWidth);
		material->SetVectorParameterValue(TEXT("InlineColor"), InLineColor);
	}
}

void ACS3CineCameraActor::SetActorRefData(AActor* actor)
{
	//ActorRef.Add(actor);
}

CONTROL_COMPILE_OPTIMIZE_END 


