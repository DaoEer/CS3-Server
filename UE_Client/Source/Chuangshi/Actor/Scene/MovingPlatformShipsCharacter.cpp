// Fill out your copyright notice in the Description page of Project Settings.


#include "MovingPlatformShipsCharacter.h"
#include "Component/SpringArmComponentEX.h"
#include "Util/GolbalBPFunctionLibrary.h"

AMovingPlatformShipsCharacter::AMovingPlatformShipsCharacter()
{


}

void AMovingPlatformShipsCharacter::BeginPlay()
{
	//初始化摄像机组件
	SpringArmCompent = NewObject<USpringArmComponentEX>(this, TEXT("SpringArmCompent"));
	SpringArmCompent->RegisterComponent();
	SpringArmCompent->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
	UGolbalBPFunctionLibrary::SetCameraTargetArmLength(SpringArmCompent, 1500.0f);
	UGolbalBPFunctionLibrary::SetCameraSocketOffset(SpringArmCompent, FVector(-300.0f, 0.0f, 0.0f));
	SpringArmCompent->bUsePawnControlRotation = true;
	SpringArmCompent->SetRelativeLocation(FVector(0.0f, 0.0f, 65.0f));

	CameraComponent = NewObject<UCS3CameraComponent>(this, TEXT("FirstPersonCamera"));
	CameraComponent->RegisterComponent();
	CameraComponent->AttachToComponent(SpringArmCompent, FAttachmentTransformRules::KeepRelativeTransform);
	CameraComponent->SetRelativeLocationAndRotation(FVector(60.0f, 0.0f, 0.0f), FRotator(0.0f, 0.0f, 0.0f));
	UGolbalBPFunctionLibrary::SetCameraFOV(CameraComponent, 90.0f);
}
