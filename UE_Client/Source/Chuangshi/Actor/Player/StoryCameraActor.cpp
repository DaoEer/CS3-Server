// Fill out your copyright notice in the Description page of Project Settings.


#include "StoryCameraActor.h"
#include "Kismet/KismetRenderingLibrary.h"
#include "Kismet/KismetMaterialLibrary.h"
#include "Materials/MaterialInstanceDynamic.h"

// Sets default values
AStoryCameraActor::AStoryCameraActor()
{
	SceneComponent = CreateDefaultSubobject<USceneComponent>(TEXT("SceneComponent"));
	// Make the scene component the root component
	RootComponent = SceneComponent;


 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	//初始化场景捕捉组件
	SceneCapture = CreateDefaultSubobject<USceneCaptureComponent2D>(TEXT("SceneCapture"));
	SceneCapture->CaptureSource = ESceneCaptureSource::SCS_SceneDepth;
	SceneCapture->PrimitiveRenderMode = ESceneCapturePrimitiveRenderMode::PRM_UseShowOnlyList;
	SceneCapture->ShowFlags.SetDynamicShadows(false);

	SceneCapture->SetupAttachment(SceneComponent);
}

// Called when the game starts or when spawned
void AStoryCameraActor::BeginPlay()
{
	Super::BeginPlay();
	
}

bool AStoryCameraActor::ShouldTickIfViewportsOnly() const
{
	return true;
}

void AStoryCameraActor::OutLineEffectToCamera()
{
	if (OpenOutLine)
	{
		if (StoryCameraComponent->IsValidLowLevel()&& SceneCapture->IsValidLowLevel())
		{
			///设置捕获组件参数值
			SceneCapture->TextureTarget = UKismetRenderingLibrary::CreateRenderTarget2D(this, DepthTexSize, DepthTexSize);
			SceneCapture->PrimitiveRenderMode = ESceneCapturePrimitiveRenderMode::PRM_UseShowOnlyList;
			SceneCapture->ShowOnlyActors = ActorRef;
			SceneCapture->FOVAngle = StoryCameraComponent->FieldOfView;
			SceneCapture->SetCaptureSortPriority(10);
			SceneCapture->CaptureSource = ESceneCaptureSource::SCS_DeviceDepth;
			SceneCapture->SetVisibility(true);
			///设置Post材质属性
			if (PostMaterial.ToSoftObjectPath().IsValid())
			{
				if (StoryCameraComponent->PostProcessSettings.WeightedBlendables.Array.Num() == 0)
				{
					StreamManager.LoadSynchronous(PostMaterial);
					UMaterialInstanceDynamic* DynamicMaterial = UKismetMaterialLibrary::CreateDynamicMaterialInstance(this, PostMaterial.Get(), TEXT("OutlinePP"));
					SetDynamicMaterial(DynamicMaterial);
					FWeightedBlendable Element(1.0f, DynamicMaterial);
					StoryCameraComponent->PostProcessSettings.WeightedBlendables.Array.Add(Element);
				}
				else
				{
					UMaterialInstanceDynamic* DynamicMaterial = Cast<UMaterialInstanceDynamic>(StoryCameraComponent->PostProcessSettings.WeightedBlendables.Array[0].Object);
					SetDynamicMaterial(DynamicMaterial);
				}
			}
		}
	}
}

// Called every frame
void AStoryCameraActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	OutLineEffectToCamera();
}
	
void AStoryCameraActor::SetDynamicMaterial(UMaterialInstanceDynamic* material)
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
