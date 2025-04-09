#include "MonsterGhostEyeCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "../Player/PlayerCharacter.h"
#include "Manager/AtkStateMar.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "Component/SpringArmComponentEX.h"
#include "Components/CapsuleComponent.h"
#include "Component/Role/PosSyncComponent.h"

AMonsterGhostEyeCharacter::AMonsterGhostEyeCharacter()
{
	CharacterClassName = TEXT("MonsterExtChartletCharacter");
}

void AMonsterGhostEyeCharacter::BeginPlay()
{
	Super::BeginPlay();
}

void AMonsterGhostEyeCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();
}

void AMonsterGhostEyeCharacter::OnBindToEntity()
{
	Super::OnBindToEntity();
	SwitchControlToCharacter();
}

void AMonsterGhostEyeCharacter::OnUnBindActorCallBack()
{
	Super::OnUnBindActorCallBack();
	SwitchControlToPlayer();
}

void AMonsterGhostEyeCharacter::InitCharacterComponent()
{
	Super::InitCharacterComponent();
	InitCameraComponent();
	InitPosSyncComponent();
}

bool AMonsterGhostEyeCharacter::SwitchControlToCharacter()
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
	AtkStateMar->SwitchGhostEyeMode(true);
	FRotator CurControlRotator = PlayerController->GetControlRotation();
	//修改控制权
	if (PlayerController->GetPawn() != this)
	{
		PlayerController->Possess(this);
	}
	//绑定摄像机视角
	CameraComponent->Activate();
	PlayerController->SetViewTargetWithBlend(this);
	//设置初始的摄像机角度
	PlayerController->SetControlRotation(CurControlRotator);
	//激活移动组件
	SetCharacterMovementActive(true);
	PosSyncComp->setTickDoing(true);
	return true;
}

bool AMonsterGhostEyeCharacter::SwitchControlToPlayer()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return false;
	}
	//取消激活控制模式
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchGhostEyeMode(false);
	}
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return false;
	FRotator CurControlRotator = PlayerController->GetControlRotation();
	//控制权给玩家
	if (PlayerController->GetPawn() != PlayerActor)
	{
		PlayerController->Possess(PlayerActor);
	}
	//切换到玩家视角
	PlayerController->SetViewTargetWithBlend(PlayerActor);
	//设置初始的摄像机角度
	PlayerController->SetControlRotation(CurControlRotator);
	//停止移动组件
	SetCharacterMovementActive(false);
	PosSyncComp->setTickDoing(false);
	return true;
}

void AMonsterGhostEyeCharacter::SetCharacterMovementActive(bool bNewActive)
{
	GetCharacterMovement()->SetActive(bNewActive);
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerCharacter))
	{
		return;
	}
	PlayerCharacter->GetCharacterMovement()->SetActive(!bNewActive);

	if (bNewActive)
	{
// 		float Ratio = 2.0f;
// 		UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
// 		if (IsValid(ControllerModeMgr))
// 		{
// 			TArray<FString> OtherValue = ControllerModeMgr->GetOtherValue();
// 			Ratio = FSTRING_TO_FLOAT(OtherValue[0]);
// 		}
		SetMaxWalkSpeed(GetMoveSpeed() * 100.0f);
	}
}

void AMonsterGhostEyeCharacter::InitCameraComponent()
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

		CameraComponent = NewObject<UCS3CameraComponent>(this, TEXT("MonsterGhostEyeCamera"));
		CameraComponent->RegisterComponent();
		CameraComponent->AttachToComponent(SpringArmCompent, FAttachmentTransformRules::KeepRelativeTransform);
		CameraComponent->SetRelativeLocationAndRotation(FVector(60.0f, 0.0f, 0.0f), FRotator(0.0f, 0.0f, 0.0f));
		UGolbalBPFunctionLibrary::SetCameraFOV(CameraComponent, 90.0f);
	}
}

void AMonsterGhostEyeCharacter::InitPosSyncComponent()
{
	PosSyncComp = NewObject<UPosSyncComponent>(this, "TransFormControl", RF_NoFlags, nullptr, false, nullptr);
	PosSyncComp->RegisterComponent();
	PosSyncComp->Init(EntityId);
}