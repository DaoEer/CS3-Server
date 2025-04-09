// Fill out your copyright notice in the Description page of Project Settings.


#include "CameraControl.h"
#include "Camera/CameraComponent.h"
#include "Component/SpringArmComponentEX.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Actor/Player/PlayerCharacter.h"
#include "TransActorCapture.h"
#include "../GolbalBPFunctionLibrary.h"

CONTROL_COMPILE_OPTIMIZE_START
// Sets default values
ACameraControl::ACameraControl()
{
	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	m_CameraComponent = nullptr;
	m_CameraComponent1 = nullptr;
	m_CurrCamera = nullptr;

	BlurMaterial = LoadObject<UMaterial>(NULL, TEXT("/Game/Materials/M_PostProcess_RadialBlur.M_PostProcess_RadialBlur"), NULL, LOAD_None, NULL);
	BlurOffsetMaterial = LoadObject<UMaterial>(NULL, TEXT("/Game/Materials/M_PostProcess_RadialOffset.M_PostProcess_RadialOffset"), NULL, LOAD_None, NULL);
	DistortMaterial = LoadObject<UMaterial>(NULL, TEXT("/Game/Materials/M_DistortScene.M_DistortScene"), NULL, LOAD_None, NULL);
	DistorSceneMaterial = LoadObject<UMaterialInstance>(NULL, TEXT("/Game/Materials/M_DistortScene_Inst.M_DistortScene_Inst"), NULL, LOAD_None, NULL);
	OutLineMaterial = LoadObject<UMaterial>(NULL, TEXT("/Game/Materials/M_PostProcess_Interactive.M_PostProcess_Interactive"), NULL, LOAD_None, NULL);
	ModelVagueMaterial = LoadObject<UMaterial>(NULL, TEXT("/Game/Materials/PP_CustomStencil_Fuzzy.PP_CustomStencil_Fuzzy"), NULL, LOAD_None, NULL);

	m_Blur.MID = UKismetMaterialLibrary::CreateDynamicMaterialInstance(GetWorld(), BlurMaterial);
	m_BlurOffsetX.MID = UKismetMaterialLibrary::CreateDynamicMaterialInstance(GetWorld(), BlurOffsetMaterial);
	m_BlurOffsetY.MID = m_BlurOffsetX.MID;
	m_Distort.MID = UKismetMaterialLibrary::CreateDynamicMaterialInstance(GetWorld(), DistortMaterial);
	m_DistorSceneData.MID = UKismetMaterialLibrary::CreateDynamicMaterialInstance(GetWorld(), DistorSceneMaterial);
	m_OutLines.MID = UKismetMaterialLibrary::CreateDynamicMaterialInstance(GetWorld(), OutLineMaterial);
	m_ModelVague.MID = UKismetMaterialLibrary::CreateDynamicMaterialInstance(GetWorld(), ModelVagueMaterial);
}

// Called when the game starts or when spawned
void ACameraControl::BeginPlay()
{
	Super::BeginPlay();

}

// Called every frame
void ACameraControl::Tick(float DeltaTime)
{
	if (!m_CurrCamera)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ACameraControl::Tick: m_CurrCamera!"));
		return;
	}
	Super::Tick(DeltaTime);

	_UpdateShake(DeltaTime);
	_UpdateApproach(DeltaTime);
	_UpdateRadialBlur(DeltaTime);
	_UpdataRadialOffsetX(DeltaTime);
	_UpdataRadialOffsetY(DeltaTime);
	_UpdateUp(DeltaTime);
	_UpdateLXDistort(DeltaTime);
	//_UpdateRotate(DeltaTime);
	_UpdateDistort(DeltaTime);
	_UpdatePerspectiveTarget(DeltaTime);
}

bool ACameraControl::ShouldTickIfViewportsOnly() const
{
	return true;
}

void ACameraControl::Init(UCameraComponent *Camera, UCameraComponent* Camera1)
{
	m_CameraComponent = Camera;
	m_CameraComponent1 = Camera1;
	m_CurrCamera = m_CameraComponent;
	m_CurrCamera->PostProcessSettings.WeightedBlendables.Array.Add(FWeightedBlendable(-1, m_Blur.MID));
	m_CurrCamera->PostProcessSettings.WeightedBlendables.Array.Add(FWeightedBlendable(-1, m_BlurOffsetX.MID));
	m_CurrCamera->PostProcessSettings.WeightedBlendables.Array.Add(FWeightedBlendable(-1, m_Distort.MID));
	m_CurrCamera->PostProcessSettings.WeightedBlendables.Array.Add(FWeightedBlendable(-1, m_DistorSceneData.MID));
	m_CurrCamera->PostProcessSettings.WeightedBlendables.Array.Add(FWeightedBlendable(-1, m_OutLines.MID));
	m_CurrCamera->PostProcessSettings.WeightedBlendables.Array.Add(FWeightedBlendable(-1, m_ModelVague.MID));
}

void ACameraControl::CameraShake(float Intensity, float Rate, float Time,int32 Priority)
{
	if (!m_CurrCamera)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ACameraControl::CameraShake: m_CurrCamera!"));
		return;
	}
	
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("InShakeDeltaX =  %f"), m_Shake.ShakeDelta.X);
	if (m_Shake.Enable)
	{
		if (Priority>m_Shake.Priority)
		{
			m_Shake.Init(Intensity, Rate, Time, this);
		}else if (Priority == m_Shake.Priority)
		{
			m_Shake.Init(Intensity, Rate, Time, this);
		}
	}
	else
	{
		m_Shake.Init(Intensity, Rate, Time, this);
		m_Shake.Priority = Priority;
	}
}

void ACameraControl::StopCameraShake()
{
	m_Shake.Enable = false;
	USpringArmComponent* arm = Cast<USpringArmComponent>(m_CurrCamera->GetAttachParent());
	if (arm)
	{
		//清除偏移
		arm->SocketOffset.Set(arm->SocketOffset.X - m_Shake.ShakeDelta.X, arm->SocketOffset.Y - m_Shake.ShakeDelta.Y,
			arm->SocketOffset.Z - m_Shake.ShakeDelta.Z);
	}
	m_Shake.ShakeDelta = FVector(0.0f, 0.0f, 0.0f);
}

void ACameraControl::CameraApproach(float Dist, float ApproachT, float RemainT, float ApproachBackT)
{
	if (!m_CurrCamera)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ACameraControl::CameraApproach: m_CurrCamera!"));
		return;
	}
	USpringArmComponent* arm = Cast<USpringArmComponent>(m_CurrCamera->GetAttachParent());
	if (!arm)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ACameraControl::CameraApproach: arm!"));
		return;
	}
	m_Approach.Init(Dist, ApproachT, RemainT, ApproachBackT, arm->TargetArmLength);
}

void ACameraControl::StopCameraApproach()
{
	m_Approach.Enable = false;
	USpringArmComponent* arm = Cast<USpringArmComponent>(m_CurrCamera->GetAttachParent());
	if (arm)
	{
		UGolbalBPFunctionLibrary::SetCameraTargetArmLength(arm, arm->TargetArmLength - m_Approach.ArmLength);
	}
	m_Approach.ArmLength = 0.0f;
}

void ACameraControl::RadialBlur(float Intensity, float FadeInT, float RemainT, float FadeOutT)
{
	if (!m_CurrCamera)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ACameraControl::RadialBlur: m_CurrCamera!"));
		return;
	}
	m_Blur.Init(Intensity, FadeInT, RemainT, FadeOutT);
	if (m_CameraComponent && IsValid((m_Blur.MID)))
	{
		m_CameraComponent->AddOrUpdateBlendable(m_Blur.MID, 1);
	}
}

void ACameraControl::StopRadialBlur()
{
	m_Blur.Enable = false;
	m_Blur.MID->SetScalarParameterValue(FName(TEXT("BlurAmount")), 0);
	if (IsValid(m_CameraComponent))
	{
		m_CameraComponent->AddOrUpdateBlendable(m_Blur.MID, 0);
	}
}

void ACameraControl::RadialOffsetX(float Offset, float FadeInT, float RemainT, float FadeOutT)
{
	if (!m_CurrCamera)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ACameraControl::RadialOffsetX: m_CurrCamera!"));
		return;
	}
	m_BlurOffsetX.Init(Offset, FadeInT, RemainT, FadeOutT);
	if (m_CameraComponent && IsValid((m_BlurOffsetX.MID)))
	{
		m_CameraComponent->AddOrUpdateBlendable(m_BlurOffsetX.MID, 1);
	}	
}

void ACameraControl::StopRadialOffsetX()
{
	m_BlurOffsetX.Enable = false;
	m_BlurOffsetX.MID->SetScalarParameterValue(FName(TEXT("OffsetAmount")), 0.f);
	m_BlurOffsetX.MID->SetScalarParameterValue(FName(TEXT("OffsetX")), 0.f);
	m_CameraComponent->AddOrUpdateBlendable(m_BlurOffsetX.MID, 0);
}

void ACameraControl::RadialOffsetY(float Offset, float FadeInT, float RemainT, float FadeOutT)
{
	if (!m_CurrCamera)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ACameraControl::RadialOffsetY: m_CurrCamera!"));
		return;
	}
	m_BlurOffsetY.Init(Offset, FadeInT, RemainT, FadeOutT);
	if (m_CameraComponent && IsValid((m_BlurOffsetY.MID)))
	{
		m_CameraComponent->AddOrUpdateBlendable(m_BlurOffsetY.MID, 1);
	}
}

void ACameraControl::StopRadialOffsetY()
{
	m_BlurOffsetY.Enable = false;
	m_BlurOffsetY.MID->SetScalarParameterValue(FName(TEXT("OffsetAmount")), 0.f);
	m_BlurOffsetY.MID->SetScalarParameterValue(FName(TEXT("OffsetY")), 0.f);
	m_CameraComponent->AddOrUpdateBlendable(m_BlurOffsetY.MID, 0);
}

void ACameraControl::CameraUp(float Height, float FadeInT, float RemainT, float FadeOutT)
{
	if (!m_CurrCamera)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ACameraControl::CameraUp: m_CurrCamera!"));
		return;
	}
	m_Up.Init(Height, FadeInT, RemainT, FadeOutT);
}

void ACameraControl::StopCameraUp()
{
	m_Up.Enable = false;
	USpringArmComponent* arm = Cast<USpringArmComponent>(m_CurrCamera->GetAttachParent());
	if (arm)
	{
		arm->SocketOffset = FVector::ZeroVector;
	}
	m_Up.Intensity = 0.0f;
	m_Up.Time = FVector::ZeroVector;
	m_Up.Passed = 0.0f;
}

void ACameraControl::DistortScene(float Intensity, FLinearColor FilterColor, FLinearColor MaskColor, float fDistortArea, float FadeInT, float RemainT, float FadeOutT)
{
	if (!m_CurrCamera)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ACameraControl::DistortScene: m_CurrCamera!"));
		return;
	}

	m_Distort.Init(Intensity, FilterColor, MaskColor, fDistortArea, FadeInT, RemainT, FadeOutT);
	if (m_CameraComponent && IsValid((m_Distort.MID)))
	{
		m_CameraComponent->AddOrUpdateBlendable(m_Distort.MID, 1);
	}
}

void ACameraControl::OnEndDistortScene()
{
	m_Distort.bIsEndEffect = true;
	m_Distort.Passed = 0.0f;
}

void ACameraControl::StopDistortScene()
{
	if (m_Distort.Enable)
	{
		FLinearColor linearColor = m_Distort.FilterColor;
		FLinearColor maskColor = m_Distort.MaskColor;

		m_Distort.Enable = false;
		m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortArea")), 0);
		m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortRange")), 0);
		linearColor.R = 1;
		linearColor.G = 1;
		linearColor.B = 1;
		linearColor.A = 0;
		m_Distort.MID->SetVectorParameterValue(FName(TEXT("FilterColor")), linearColor);
		m_Distort.MID->SetVectorParameterValue(FName(TEXT("FilterAlpha")), linearColor);
		OnDistortSceneFinished.Broadcast();
		m_CameraComponent->AddOrUpdateBlendable(m_Distort.MID, 0);
	}
}

void ACameraControl::LXDistortScene(float fDitortAngle, float fDistortMask, float fStartTimeDistort, float fRecoveryTimeDistort)
{
	if (!m_CurrCamera)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ACameraControl::LXDistortScene: m_CurrCamera!"));
		return;
	}
	m_DistorSceneData.Init(fDitortAngle, fDistortMask, fStartTimeDistort, fRecoveryTimeDistort);
	if (m_CameraComponent && IsValid((m_DistorSceneData.MID)))
	{
		m_CameraComponent->AddOrUpdateBlendable(m_DistorSceneData.MID, 1);
	}
}

void ACameraControl::OnEndLXDistortScene()
{
	m_DistorSceneData.Passed = 0.0f;
	m_DistorSceneData.bIsEndEffect = true;
}

void ACameraControl::StopLXDistortScene()
{
	if (m_DistorSceneData.isEable && IsValid(m_Distort.MID) && IsValid(m_CameraComponent))
	{
		m_DistorSceneData.isEable = false;
		m_DistorSceneData.MID->SetScalarParameterValue(FName(TEXT("Angle")), 0);
		m_DistorSceneData.MID->SetScalarParameterValue(FName(TEXT("Masks")), 0);
		m_CameraComponent->AddOrUpdateBlendable(m_DistorSceneData.MID, 0);
	}
}

// void ACameraControl::CameraRotate(float Time)
// {
// 	if (!m_CurrCamera)
// 	{
// 		UE_LOG(LogScript, Warning, TEXT("CameraControl::Tick : Camera is null, please init first!"));
// 		return;
// 	}
// 	m_Rotate.Init(Time);
// }

bool ACameraControl::BlurisEnable()
{
	return m_Blur.Enable;
}

void ACameraControl::ResetBlur()
{
	m_Blur.Enable = false;
	m_Blur.MID->SetScalarParameterValue(FName(TEXT("BlurAmount")), 0);
}

void ACameraControl::OpenOutLineCalculation()
{
	OutLineNums += 1;
	if (m_CameraComponent && IsValid((m_OutLines.MID)))
	{
		m_OutLines.MID->SetScalarParameterValue(FName(TEXT("OpenOutLine")), 1.0);
		m_CameraComponent->AddOrUpdateBlendable(m_OutLines.MID, 1);
	}
	
}

void ACameraControl::CloseOutLineCalculation()
{
	if (OutLineNums > 1)
	{
		OutLineNums -= 1;
	}
	else
	{
		OutLineNums = 0;
		m_OutLines.MID->SetScalarParameterValue(FName(TEXT("OpenOutLine")), 0.0);
		m_CameraComponent->AddOrUpdateBlendable(m_OutLines.MID, 0);
	}
}

void ACameraControl::OpenModelVagueCalculation()
{
	if (m_CameraComponent && IsValid((m_ModelVague.MID)))
	{
		m_CameraComponent->AddOrUpdateBlendable(m_ModelVague.MID, 1);
	}
}

void ACameraControl::CloseModelVagueCalculation()
{
	if (m_CameraComponent && IsValid((m_ModelVague.MID)))
	{
		m_CameraComponent->AddOrUpdateBlendable(m_ModelVague.MID, -1);
	}
}

void ACameraControl::ChangeOutLineColor(const FVector & Color)
{
	FVector NewColor = Color / 255;
	m_OutLines.MID->SetVectorParameterValue(FName(TEXT("CustomDepthStencilValueEqual2Color")), NewColor);
}

void ACameraControl::ChangeOutLineWidth(const float & Width)
{
	m_OutLines.MID->SetScalarParameterValue(FName(TEXT("LineThickness")), Width);
}

void ACameraControl::AddPerspectiveTarget(int32 targetID, float maxDist, float minDist, float maxHeigth)
{
	if (!TargetIDArr.Contains(targetID))
	{
		TargetIDArr.Add(targetID);
		MaxVisibleDistance = maxDist * 100;
		MinVisibleDistance = minDist * 100;
		MaxVisibleHeigth = maxHeigth * 100;
		OpenOutLineCalculation();
	}
}

void ACameraControl::RemovePerspectiveTarget(int32 targetID)
{
	if (TargetIDArr.Contains(targetID))
	{
		TargetIDArr.Remove(targetID);
		CloseOutLineCalculation();
	}
}

void ACameraControl::_UpdateShake(float DeltaTime)
{
	if (m_Shake.Enable)
	{
		float speed = 1 / m_Shake.Time;
		USpringArmComponent* arm = Cast<USpringArmComponent>(m_CurrCamera->GetAttachParent());

		if (m_Shake.Passed <= 1)
		{
			m_Shake.Passed += DeltaTime * speed;
			float radian = m_Shake.Rate * m_Shake.Time * m_Shake.Passed;
			FVector Offset(FMath::Sin(radian * 0.618f) , FMath::Cos(radian), FMath::Sin(radian));
			FVector CurOffset = Offset * (m_Shake.Intensity * (1 - m_Shake.Passed));

			//先尝试清除偏移
			arm->SocketOffset.Set(arm->SocketOffset.X - m_Shake.ShakeDelta.X, arm->SocketOffset.Y - m_Shake.ShakeDelta.Y, 
				arm->SocketOffset.Z - m_Shake.ShakeDelta.Z);

			//记录偏移
			m_Shake.ShakeDelta = CurOffset;

			//根据记录的偏移更改摄像机偏移
			arm->SocketOffset.Set(arm->SocketOffset.X + m_Shake.ShakeDelta.X, arm->SocketOffset.Y + m_Shake.ShakeDelta.Y,
				arm->SocketOffset.Z + m_Shake.ShakeDelta.Z);

				
		}
		else
		{
		
			m_Shake.Enable = false;
			
			//清除偏移
			arm->SocketOffset.Set(arm->SocketOffset.X - m_Shake.ShakeDelta.X, arm->SocketOffset.Y - m_Shake.ShakeDelta.Y,
				arm->SocketOffset.Z - m_Shake.ShakeDelta.Z);

			m_Shake.ShakeDelta = FVector(0.0f, 0.0f, 0.0f);
		}
	}
}
void ACameraControl::_UpdateApproach(float DeltaTime)
{
	if (m_Approach.Enable)
	{
		m_Approach.Passed += DeltaTime;
		USpringArmComponent* arm = Cast<USpringArmComponent>(m_CurrCamera->GetAttachParent());
		if (arm)
		{
			//GEngine->AddOnScreenDebugMessage(-1, 2.f, FColor::Blue, FString::Printf(TEXT("Character Position is %f"), arm->TargetArmLength));
			if (m_Approach.Passed < m_Approach.Time.X)
			{
				float preTargetArmLength = arm->TargetArmLength;
				UGolbalBPFunctionLibrary::SetCameraTargetArmLength(arm, arm->TargetArmLength +(-m_Approach.Intensity * DeltaTime / m_Approach.Time.X));
				m_Approach.ArmLength += (arm->TargetArmLength - preTargetArmLength);
			}
			else if (m_Approach.Passed < m_Approach.Time.X + m_Approach.Time.Y)
			{

			}
			else if (m_Approach.Passed < (m_Approach.Time.X + m_Approach.Time.Y + m_Approach.Time.Z))
			{
				float preTargetArmLength = arm->TargetArmLength;
				UGolbalBPFunctionLibrary::SetCameraTargetArmLength(arm, arm->TargetArmLength + (-m_Approach.ArmLength * DeltaTime / m_Approach.Time.Z));
				m_Approach.ArmLength += (arm->TargetArmLength - preTargetArmLength);
			}
			else
			{
				m_Approach.Enable = false;
				UGolbalBPFunctionLibrary::SetCameraTargetArmLength(arm, arm->TargetArmLength - m_Approach.ArmLength);
				m_Approach.ArmLength = 0.0f;
			}
		}
	}
}

void ACameraControl::_UpdateRadialBlur(float DeltaTime)
{
	if (m_Blur.Enable && IsValid(m_Blur.MID) && IsValid(m_CameraComponent))
	{
		if (m_Blur.Time.IsNearlyZero())
		{
			m_Blur.MID->SetScalarParameterValue(FName(TEXT("BlurAmount")), m_Blur.Intensity);
		}
		else
		{
			m_Blur.Passed += DeltaTime;
			if (m_Blur.Passed < m_Blur.Time.X)
			{
				m_Blur.MID->SetScalarParameterValue(FName(TEXT("BlurAmount")), m_Blur.Intensity * (m_Blur.Passed / m_Blur.Time.X));
			}
			else if (m_Blur.Passed < m_Blur.Time.X + m_Blur.Time.Y)
			{
				m_Blur.MID->SetScalarParameterValue(FName(TEXT("BlurAmount")), m_Blur.Intensity);
			}
			else if (m_Blur.Passed < m_Blur.Time.X + m_Blur.Time.Y + m_Blur.Time.Z)
			{
				m_Blur.MID->SetScalarParameterValue(FName(TEXT("BlurAmount")), m_Blur.Intensity * (1 - (m_Blur.Passed - m_Blur.Time.X - m_Blur.Time.Y) / m_Blur.Time.Z));
			}
			else
			{
				m_Blur.Enable = false;
				m_Blur.MID->SetScalarParameterValue(FName(TEXT("BlurAmount")), 0);
				m_CameraComponent->AddOrUpdateBlendable(m_Blur.MID, 0);
			}
		}
	}
}

void ACameraControl::_UpdataRadialOffsetX(float DeltaTime)
{
	if (m_BlurOffsetX.Enable && IsValid(m_BlurOffsetX.MID) && IsValid(m_CameraComponent))
	{
		m_BlurOffsetX.Passed += DeltaTime;
		m_BlurOffsetX.MID->SetScalarParameterValue(FName(TEXT("OffsetAmount")), 0.2f);
		if (m_BlurOffsetX.Passed < m_BlurOffsetX.Time.X)
		{
			m_BlurOffsetX.MID->SetScalarParameterValue(FName(TEXT("OffsetX")), m_BlurOffsetX.Intensity);
		}
		else if (m_BlurOffsetX.Passed < m_BlurOffsetX.Time.X + m_BlurOffsetX.Time.Y)
		{
			m_BlurOffsetX.MID->SetScalarParameterValue(FName(TEXT("OffsetX")), m_BlurOffsetX.Intensity);
		}
		else if (m_BlurOffsetX.Passed < m_BlurOffsetX.Time.X + m_BlurOffsetX.Time.Y + m_BlurOffsetX.Time.Z)
		{
			m_BlurOffsetX.MID->SetScalarParameterValue(FName(TEXT("OffsetX")), m_BlurOffsetX.Intensity);
		}
		else
		{
			m_BlurOffsetX.Enable = false;
			m_BlurOffsetX.MID->SetScalarParameterValue(FName(TEXT("OffsetAmount")), 0.f);
			m_BlurOffsetX.MID->SetScalarParameterValue(FName(TEXT("OffsetX")), 0.f);
			m_CameraComponent->AddOrUpdateBlendable(m_BlurOffsetX.MID, 0);
		}
	}
}

void ACameraControl::_UpdataRadialOffsetY(float DeltaTime)
{
	if (m_BlurOffsetY.Enable && IsValid(m_BlurOffsetY.MID) && IsValid(m_CameraComponent))
	{
		m_BlurOffsetY.Passed += DeltaTime;
		m_BlurOffsetY.MID->SetScalarParameterValue(FName(TEXT("OffsetAmount")), 0.2f);
		if (m_BlurOffsetY.Passed < m_BlurOffsetY.Time.X)
		{
			m_BlurOffsetY.MID->SetScalarParameterValue(FName(TEXT("OffsetY")),m_BlurOffsetY.Intensity * (m_BlurOffsetY.Passed / m_BlurOffsetY.Time.X));
		}
		else if (m_BlurOffsetY.Passed < m_BlurOffsetY.Time.X + m_BlurOffsetY.Time.Y)
		{
			m_BlurOffsetY.MID->SetScalarParameterValue(FName(TEXT("OffsetY")),m_BlurOffsetY.Intensity);
		}
		else if (m_BlurOffsetY.Passed < m_BlurOffsetY.Time.X + m_BlurOffsetY.Time.Y + m_BlurOffsetY.Time.Z)
		{
			
			m_BlurOffsetY.MID->SetScalarParameterValue(FName(TEXT("OffsetY")),
				m_BlurOffsetY.Intensity * (1 - (m_BlurOffsetY.Passed - m_BlurOffsetY.Time.X - m_BlurOffsetY.Time.Y) / m_BlurOffsetY.Time.Z));
		}
		else
		{
			m_BlurOffsetY.Enable = false;
			m_BlurOffsetY.MID->SetScalarParameterValue(FName(TEXT("OffsetAmount")), 0.f);
			m_BlurOffsetY.MID->SetScalarParameterValue(FName(TEXT("OffsetY")), 0.f);
			m_CameraComponent->AddOrUpdateBlendable(m_BlurOffsetY.MID, 0);
		}
	}
}

void ACameraControl::_UpdateUp(float DeltaTime)
{
	if (m_Up.Enable)
	{
		m_Up.Passed += DeltaTime;
		USpringArmComponent* arm = Cast<USpringArmComponent>(m_CurrCamera->GetAttachParent());

		if (m_Up.Passed < m_Up.Time.X)
		{
			arm->SocketOffset =  FVector(0, 0, m_Up.Intensity * (m_Up.Passed / m_Up.Time.X));

		}
		else if (m_Up.Passed < m_Up.Time.X + m_Up.Time.Y)
		{
			arm->SocketOffset =  FVector(0, 0, m_Up.Intensity);

		}
		else if (m_Up.Passed < m_Up.Time.X + m_Up.Time.Y + m_Up.Time.Z)
		{
			arm->SocketOffset =  FVector(0, 0, m_Up.Intensity * (1 - (m_Up.Passed - m_Up.Time.X - m_Up.Time.Y) / m_Up.Time.Z));
		}
		else
		{
			m_Up.Enable = false;
			arm->SocketOffset = FVector::ZeroVector;
			m_Up.Intensity = 0.0f;
			m_Up.Time = FVector::ZeroVector;
			m_Up.Passed = 0.0f;
		}
	}
}

void ACameraControl::_UpdateDistort(float DeltaTime)
{
	if (m_Distort.Enable&&IsValid(m_Distort.MID)&&IsValid(m_CameraComponent))
	{
		FLinearColor linearColor = m_Distort.FilterColor;
		FLinearColor maskColor = m_Distort.MaskColor;
		m_Distort.Passed += DeltaTime;
		if (!m_Distort.bIsEndEffect)
		{
			if (m_Distort.Passed < m_Distort.Time.X)
			{
				m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortArea")), m_Distort.DistortArea * (m_Distort.Passed / m_Distort.Time.X));
				m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortRange")), m_Distort.Intensity * (m_Distort.Passed / m_Distort.Time.X));
				m_Distort.MID->SetVectorParameterValue(FName(TEXT("FilterColor")), GetDistortColor(m_Distort.FilterColor));
				m_Distort.MID->SetVectorParameterValue(FName(TEXT("MaskColor")), GetDistortColor(m_Distort.MaskColor));
			}
			else if (m_Distort.Time.Y > 0)
			{
				if (m_Distort.Passed < m_Distort.Time.X + m_Distort.Time.Y)
				{
					m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortArea")), m_Distort.DistortArea);
					m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortRange")), m_Distort.Intensity);
					m_Distort.MID->SetVectorParameterValue(FName(TEXT("FilterColor")), linearColor);
					m_Distort.MID->SetVectorParameterValue(FName(TEXT("MaskColor")), maskColor);
				}
				else if (m_Distort.Passed < m_Distort.Time.X + m_Distort.Time.Y + m_Distort.Time.Z)
				{
					m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortArea")), m_Distort.DistortArea * (1 - (m_Distort.Passed - m_Distort.Time.X - m_Distort.Time.Y) / m_Distort.Time.Z));
					m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortRange")), m_Distort.Intensity * (1 - (m_Distort.Passed - m_Distort.Time.X - m_Distort.Time.Y) / m_Distort.Time.Z));
					m_Distort.MID->SetVectorParameterValue(FName(TEXT("FilterColor")), GetDistortColor(m_Distort.FilterColor));
					m_Distort.MID->SetVectorParameterValue(FName(TEXT("MaskColor")), GetDistortColor(m_Distort.MaskColor));
				}
				else
				{
					m_Distort.Enable = false;
					m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortArea")), 0);
					m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortRange")), 0);
					linearColor.R = 1;
					linearColor.G = 1;
					linearColor.B = 1;
					linearColor.A = 0;
					m_Distort.MID->SetVectorParameterValue(FName(TEXT("FilterColor")), linearColor);
					m_Distort.MID->SetVectorParameterValue(FName(TEXT("MaskColor")), maskColor);
					OnDistortSceneFinished.Broadcast();
					m_CameraComponent->AddOrUpdateBlendable(m_Distort.MID, 0);
				}

			}
			else
			{
				if (m_Distort.Time.X < m_Distort.Passed || FMath::IsNearlyEqual(m_Distort.Time.X, m_Distort.Passed))
				{
					m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortArea")), m_Distort.DistortArea);
					m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortRange")), m_Distort.Intensity);
					m_Distort.MID->SetVectorParameterValue(FName(TEXT("FilterColor")), linearColor);
					m_Distort.MID->SetVectorParameterValue(FName(TEXT("MaskColor")), maskColor);
				}
			}						
		}
		else
		{
			if (m_Distort.Passed < m_Distort.Time.Z)
			{
				m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortArea")), m_Distort.DistortArea * (1 - m_Distort.Passed / m_Distort.Time.Z));
				m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortRange")), m_Distort.Intensity * (1 - m_Distort.Passed  / m_Distort.Time.Z));
				m_Distort.MID->SetVectorParameterValue(FName(TEXT("FilterColor")), GetDistortColor(m_Distort.FilterColor));
				m_Distort.MID->SetVectorParameterValue(FName(TEXT("MaskColor")), GetDistortColor(m_Distort.MaskColor));
			}
			else
			{
				m_Distort.Enable = false;
				m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortArea")), 0);
				m_Distort.MID->SetScalarParameterValue(FName(TEXT("DistortRange")), 0);
				linearColor.R = 1;
				linearColor.G = 1;
				linearColor.B = 1;
				linearColor.A = 0;
				m_Distort.MID->SetVectorParameterValue(FName(TEXT("FilterColor")), linearColor);
				m_Distort.MID->SetVectorParameterValue(FName(TEXT("FilterAlpha")), linearColor);
				OnDistortSceneFinished.Broadcast();
				m_CameraComponent->AddOrUpdateBlendable(m_Distort.MID, 0);
			}
		}
	}
}

void ACameraControl::_UpdateLXDistort(float DeltaTime)
{
	if (m_DistorSceneData.isEable)
	{
		if (IsValid(m_Distort.MID) && IsValid(m_CameraComponent))
		{
			m_DistorSceneData.Passed += DeltaTime;
			float currentAngle;
			float currentMasks;
			m_DistorSceneData.MID->GetScalarParameterValue(FName(TEXT("Angle")), currentAngle);
			m_DistorSceneData.MID->GetScalarParameterValue(FName(TEXT("Masks")), currentMasks);
			if (!m_DistorSceneData.bIsEndEffect)
			{
				if (currentAngle <= m_DistorSceneData.DitortAngle)
				{
					m_DistorSceneData.MID->SetScalarParameterValue(FName(TEXT("Angle")), currentAngle + ((m_DistorSceneData.DitortAngle / m_DistorSceneData.StartTimeDistort)*DeltaTime));
				}
				if (currentMasks <= m_DistorSceneData.DistortMask)
				{
					m_DistorSceneData.MID->SetScalarParameterValue(FName(TEXT("Masks")), currentMasks + ((m_DistorSceneData.DistortMask / m_DistorSceneData.StartTimeDistort)*DeltaTime));
				}
			}
			else
			{
				if (currentAngle > 0.0f)
				{
					m_DistorSceneData.MID->SetScalarParameterValue(FName(TEXT("Angle")), currentAngle - ((m_DistorSceneData.DitortAngle / m_DistorSceneData.RecoveryTimeDistort)*DeltaTime));

				}
				if (currentAngle < 0.0f)
				{
					m_DistorSceneData.MID->SetScalarParameterValue(FName(TEXT("Angle")), 0);
				}
				if (currentMasks > 0.0f)
				{
					m_DistorSceneData.MID->SetScalarParameterValue(FName(TEXT("Masks")), currentMasks - ((m_DistorSceneData.DistortMask / m_DistorSceneData.RecoveryTimeDistort)*DeltaTime));
				}
				if (currentMasks < 0.0f)
				{
					m_DistorSceneData.MID->SetScalarParameterValue(FName(TEXT("Masks")), 0);
					m_CameraComponent->AddOrUpdateBlendable(m_DistorSceneData.MID, 0);
				}
			}
		}
	}
} 

FLinearColor ACameraControl::GetDistortColor(FLinearColor FilterColor)
{
	FLinearColor linearColor = FilterColor;
	if (!m_Distort.bIsEndEffect)
	{
		if (m_Distort.Passed < m_Distort.Time.X)
		{
			if (FilterColor.R > 1)
			{
				linearColor.R = 1 + (FilterColor.R - 1)*(m_Distort.Passed / m_Distort.Time.X);
			}
			else
			{
				linearColor.R = 1 - (1 - FilterColor.R)*(m_Distort.Passed / m_Distort.Time.X);
			}

			if (FilterColor.G > 1)
			{
				linearColor.G = 1 + (FilterColor.G - 1)*(m_Distort.Passed / m_Distort.Time.X);
			}
			else
			{
				linearColor.G = 1 - (1 - FilterColor.G)*(m_Distort.Passed / m_Distort.Time.X);
			}

			if (FilterColor.B > 1)
			{
				linearColor.B = 1 + (FilterColor.B - 1)*(m_Distort.Passed / m_Distort.Time.X);
			}
			else
			{
				linearColor.B = 1 - (1 - FilterColor.B)*(m_Distort.Passed / m_Distort.Time.X);
			}
			if (FilterColor.A > 0)
			{
				linearColor.A = FilterColor.A*(m_Distort.Passed / m_Distort.Time.X);
			}
		}
		else if (m_Distort.Time.Y > 0)
		{
			if (m_Distort.Passed < m_Distort.Time.X + m_Distort.Time.Y + m_Distort.Time.Z)
			{
				if (FilterColor.R > 1)
				{
					linearColor.R = FilterColor.R - (FilterColor.R - 1)*((m_Distort.Passed - m_Distort.Time.X - m_Distort.Time.Y) / m_Distort.Time.Z);
				}
				else
				{
					linearColor.R = FilterColor.R + (1 - FilterColor.R)*((m_Distort.Passed - m_Distort.Time.X - m_Distort.Time.Y) / m_Distort.Time.Z);
				}
				if (FilterColor.G > 1)
				{
					linearColor.G = FilterColor.G - (FilterColor.G - 1)*((m_Distort.Passed - m_Distort.Time.X - m_Distort.Time.Y) / m_Distort.Time.Z);
				}
				else
				{
					linearColor.G = FilterColor.G + (1 - FilterColor.G)*((m_Distort.Passed - m_Distort.Time.X - m_Distort.Time.Y) / m_Distort.Time.Z);
				}

				if (FilterColor.B > 1)
				{
					linearColor.B = FilterColor.B - (FilterColor.B - 1)*((m_Distort.Passed - m_Distort.Time.X - m_Distort.Time.Y) / m_Distort.Time.Z);
				}
				else
				{
					linearColor.B = FilterColor.B + (1 - FilterColor.B)*((m_Distort.Passed - m_Distort.Time.X - m_Distort.Time.Y) / m_Distort.Time.Z);
				}
				if (FilterColor.A > 0)
				{
					linearColor.A = FilterColor.A - FilterColor.A *((m_Distort.Passed - m_Distort.Time.X - m_Distort.Time.Y) / m_Distort.Time.Z);
				}

			}
		}
	}
	else
	{
		if (m_Distort.Passed < m_Distort.Time.Z)
		{
			if (FilterColor.R > 1)
			{
				linearColor.R = FilterColor.R - (FilterColor.R - 1)*(m_Distort.Passed / m_Distort.Time.Z);
			}
			else
			{
				linearColor.R = FilterColor.R + (1 - FilterColor.R)*(m_Distort.Passed / m_Distort.Time.Z);
			}
			if (FilterColor.G > 1)
			{
				linearColor.G = FilterColor.G - (FilterColor.G - 1)*(m_Distort.Passed / m_Distort.Time.Z);
			}
			else
			{
				linearColor.G = FilterColor.G + (1 - FilterColor.G)*(m_Distort.Passed / m_Distort.Time.Z);
			}

			if (FilterColor.B > 1)
			{
				linearColor.B = FilterColor.B - (FilterColor.B - 1)*(m_Distort.Passed / m_Distort.Time.Z);
			}
			else
			{
				linearColor.B = FilterColor.B + (1 - FilterColor.B)*(m_Distort.Passed / m_Distort.Time.Z);
			}
			if (FilterColor.A > 0)
			{
				linearColor.A = FilterColor.A - FilterColor.A*(m_Distort.Passed / m_Distort.Time.Z);
			}
		}
	}
	return linearColor;
}

void ACameraControl::_UpdatePerspectiveTarget(float DeltaTime)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!Player)
	{
		return;
	}
	TArray<int32> PopIDArr;
	for (int32 TargetID : TargetIDArr)
	{
		AServerCharacter* _character = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
		if (IsValid(_character))
		{
			float Dist = FVector::Dist2D(Player->GetActorLocation(), _character->GetActorLocation());
			float Heigth = abs(Player->GetActorLocation().Z - _character->GetActorLocation().Z);
			if (Dist <= MaxVisibleDistance && Dist >= MinVisibleDistance && Heigth <= MaxVisibleHeigth)
			{
				_character->SetCustomDepthStncilValue(CUSTOM_DEPTH_STENCIL::CUSTOM_DEPTH_STENCIL_OUTLINE_COVER);
				
			}
			else
			{
				_character->SetCustomDepthStncilValue(CUSTOM_DEPTH_STENCIL::CUSTOM_DEPTH_STENCIL_NORMAL);
			}
		}
		else
		{
			PopIDArr.Add(TargetID);
		}
	}
	for (int32 id : PopIDArr)
	{
		RemovePerspectiveTarget(id);
	}

}

// void ACameraControl::_UpdateRotate(float DeltaTime)
// {
// 	if (m_Rotate.Enable)
// 	{
// 		m_Rotate.Passed += DeltaTime;
// 		USpringArmComponent* arm = Cast<USpringArmComponent>(m_CurrCamera->GetAttachParent());
// 		if (arm)
// 		{
// 			if (m_Rotate.Passed < m_Rotate.Time)
// 			{
// 
// 			}
// 
// 		}
// 	}
// }



void UCS3CameraShake::UpdateAndApplyCameraShake(float DeltaTime, float Alpha, FMinimalViewInfo& InOutPOV)
{
	Super::UpdateAndApplyCameraShake(DeltaTime, Alpha, InOutPOV);
}

void UCS3CameraShake::PlayShake(APlayerCameraManager * Camera, float Scale, ECameraAnimPlaySpace::Type InPlaySpace, FRotator UserPlaySpaceRot)
{
	Super::PlayShake(Camera, Scale, InPlaySpace, UserPlaySpaceRot);
}

void UCS3CameraShake::UpdateShakeData(int8 ShakeType, float Amplitude, float Frequency, uint8 InitialOffset, uint8 Waveform)
{
	if (ShakeType ==0 )
	{
		FFOscillator FOscillation;
		FOscillation.Amplitude = Amplitude;
		FOscillation.Frequency = Frequency;
		FOscillation.InitialOffset = (TEnumAsByte<enum EInitialOscillatorOffset>)InitialOffset;
		FOscillation.Waveform = (EOscillatorWaveform)Waveform;
		RotOscillation.Pitch = FOscillation;
		RotOscillation.Roll = FOscillation; 
		RotOscillation.Yaw = FOscillation;
	}
	else if (ShakeType == 1)
	{
		FFOscillator FOscillation;
		FOscillation.Amplitude = Amplitude;
		FOscillation.Frequency = Frequency;
		FOscillation.InitialOffset = (TEnumAsByte<enum EInitialOscillatorOffset>)InitialOffset;
		FOscillation.Waveform = (EOscillatorWaveform)Waveform;
		LocOscillation.X = FOscillation;
		LocOscillation.Y = FOscillation;
		LocOscillation.Z = FOscillation;
	}
	else if (ShakeType == 2)
	{
		FOVOscillation.Amplitude = Amplitude;
		FOVOscillation.Frequency = Frequency;
		FOVOscillation.InitialOffset = (TEnumAsByte<enum EInitialOscillatorOffset>)InitialOffset;
		FOVOscillation.Waveform = (EOscillatorWaveform)Waveform;
	}
}

CONTROL_COMPILE_OPTIMIZE_END


