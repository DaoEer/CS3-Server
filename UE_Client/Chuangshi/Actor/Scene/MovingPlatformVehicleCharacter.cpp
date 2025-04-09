#include "MovingPlatformVehicleCharacter.h"
#include "Component/Role/PosSyncComponent.h"
#include "Component/SpringArmComponentEX.h"
#include "Component/CS3CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/AtkStateMar.h"
#include "../ServerCharacter.h"
#include "GameData/CharacterData.h"
#include "Component/AppearanceComponent.h"


AMovingPlatformVehicleCharacter::AMovingPlatformVehicleCharacter()
{
	CharacterClassName = TEXT("MovingPlatformVehicleCharacter");
}

void AMovingPlatformVehicleCharacter::BeginPlay()
{
	Super::BeginPlay();
}

void AMovingPlatformVehicleCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();
}

void AMovingPlatformVehicleCharacter::OnBindToEntity()
{
	Super::OnBindToEntity();
}

void AMovingPlatformVehicleCharacter::OnUnBindActorCallBack()
{
	Super::OnUnBindActorCallBack();
	SwitchControl(false);//正常Entity那边会通知
}

void AMovingPlatformVehicleCharacter::InitCharacterComponent()
{
	Super::InitCharacterComponent();
	InitCameraComponent();
	InitPosSyncComponent();
}

float AMovingPlatformVehicleCharacter::GetMoveSpeed()
{
	if (bIsClient)
	{
		return ClientMoveSpeed;
	}
	return UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, (TEXT("moveSpeed")));
}

bool AMovingPlatformVehicleCharacter::IsActiveMoveing()
{
	KBEngine::Entity* Entity = this->GetSelfEntity();
	if (Entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AMovingPlatformVehicleCharacter::IsActiveMoveing : Entity!"));
		return false;
	}
	if (Entity->IsControlled())
	{
		FVector CharacterVelocity = GetVelocity();
		CharacterVelocity.Z = 0;
		return CharacterVelocity.Size() > 0.0f ? true : false;
	}
	else
	{
		return GetFilterSpeed() > 0.0f ? true : false;
	}
}

bool AMovingPlatformVehicleCharacter::SwitchControl(bool InIsControl)
{
	if (bIsControl == InIsControl) return false;
	bIsControl = InIsControl;
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return false;
	}

	FRotator CurControlRotator = PlayerController->GetControlRotation();
	AServerCharacter* ControllerCharacter = this;
	if ( !InIsControl)
	{
		ControllerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	}
	if (!IsValid(ControllerCharacter)) return false;
	//修改控制权
	if (PlayerController->GetPawn() != ControllerCharacter)
	{
		PlayerController->Possess(ControllerCharacter);
	}
	//绑定摄像机视角
	CameraComponent->SetActive(InIsControl);
	PlayerController->SetViewTargetWithBlend(ControllerCharacter);
	//设置初始的摄像机角度
	PlayerController->SetControlRotation(CurControlRotator);
	//激活移动组件
	SetMovementActive(InIsControl);
	PosSyncComp->setTickDoing(InIsControl);
	return true;
}

bool AMovingPlatformVehicleCharacter::SwitchMoveVehicleMode(bool IsActive)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return false;
	}
	//修改控制模式和操作模式
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if (!IsValid(AtkStateMar))
	{
		return false;
	}
	AtkStateMar->SwitchMoveVehicle(IsActive);
	return true;
}

void AMovingPlatformVehicleCharacter::CreateVehicleAppearance(FString CarrierModelId)
{
	if (IsValid(GetAppearanceComponent()))
	{
		GetAppearanceComponent()->CreateAppearance(CarrierModelId);
	}
}

void AMovingPlatformVehicleCharacter::SwitchCamera(bool IsActive)
{
	//绑定摄像机视角
	AServerCharacter* ControllerCharacter = this;
	if (!IsActive)
	{
		ControllerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController)) return;
	CameraComponent->SetActive(IsActive);
	PlayerController->SetViewTargetWithBlend(ControllerCharacter);
}

void AMovingPlatformVehicleCharacter::SetMovementActive(bool bNewActive)
{
	GetCharacterMovement()->SetActive(bNewActive);
	if (bNewActive)
	{
		float moveSpeed = UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, TEXT("moveSpeed"));
		if (moveSpeed > 0.0f)
		{
			SetMaxWalkSpeed(moveSpeed * 100.0f);
		}
	}
}

void AMovingPlatformVehicleCharacter::InitCameraComponent()
{
	UCapsuleComponent* CharacterCapsuleComponent = GetCapsuleComponent();
	if (!IsValid(CharacterCapsuleComponent))
	{
		return;
	}

	{
		SpringArmCompent = NewObject<USpringArmComponentEX>(this, TEXT("SpringArmCompent"));
		SpringArmCompent->RegisterComponent();
		SpringArmCompent->AttachToComponent(CharacterCapsuleComponent, FAttachmentTransformRules::KeepRelativeTransform);
		UGolbalBPFunctionLibrary::SetCameraTargetArmLength(SpringArmCompent, 1500.0f);
		UGolbalBPFunctionLibrary::SetCameraSocketOffset(SpringArmCompent, FVector(-300.0f, 0.0f, 0.0f));
		SpringArmCompent->bUsePawnControlRotation = true;
		SpringArmCompent->SetRelativeLocation(FVector(0.0f, 0.0f, 65.0f));

		CameraComponent = NewObject<UCS3CameraComponent>(this, TEXT("MovingPlatformVehicleCamera"));
		CameraComponent->RegisterComponent();
		CameraComponent->AttachToComponent(SpringArmCompent, FAttachmentTransformRules::KeepRelativeTransform);
		CameraComponent->SetRelativeLocationAndRotation(FVector(60.0f, 0.0f, 0.0f), FRotator(0.0f, 0.0f, 0.0f));
		UGolbalBPFunctionLibrary::SetCameraFOV(CameraComponent, 90.0f);
		InitLightComponent();
	}
}

void AMovingPlatformVehicleCharacter::InitPosSyncComponent()
{
	PosSyncComp = NewObject<UPosSyncComponent>(this, "TransFormControl", RF_NoFlags, nullptr, false, nullptr);
	PosSyncComp->RegisterComponent();
	PosSyncComp->Init(EntityId);
	PosSyncComp->setTickDoing(false);
}

void AMovingPlatformVehicleCharacter::InitLightComponent()
{
	CS3LightComponent = NewObject<UCS3LightComponent>(this, TEXT("CS3LightComponent"));
	CS3LightComponent->RegisterComponent();
	CS3LightComponent->CreateLight();
	CS3LightComponent->SceneLight->AttachToComponent(SpringArmCompent, FAttachmentTransformRules::KeepRelativeTransform);
	CS3LightComponent->InitLightData();
	CS3LightComponent->SetComponentTickEnabled(false);
}
