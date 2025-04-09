// Fill out your copyright notice in the Description page of Project Settings.

#include "RiderCharacter.h"
#include "../Player/PlayerCharacter.h"
#include "Component/CollisionComponent.h"
#include "Component/AppearanceComponent.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ModifyFaceManager.h"

ARiderCharacter::ARiderCharacter():GameCharacter(nullptr)
{
	CharacterClassName = TEXT("RiderCharacter");
	PrimaryActorTick.bCanEverTick = true;
	CreateRoleMesh();
	InitBaseComponent();
}

void ARiderCharacter::OnCreateModelOver()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GameCharacter);
	if (IsValid(PlayerCharacter))
	{
		//如果是跳伞，需要关闭模型LOD切换
		if (PlayerCharacter->IsJumpParachuteState())
		{
			Cast<USkeletalMeshComponent>(GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_COATS))->SetForcedLOD(1);
//			Cast<USkeletalMeshComponent>(GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_COATS))->SetTeleportRotationThreshold(0.f);
// 				TArray<USceneComponent*> ComponentList;
// 				GetMesh()->GetChildrenComponents(false, ComponentList);
// 				ComponentList.Insert(GetMesh(), 0);
// 				for (USceneComponent* Component : ComponentList)
// 				{
// 					USkeletalMeshComponent* SkeletalMeshCpt = Cast<USkeletalMeshComponent>(Component);
// 					if (IsValid(SkeletalMeshCpt))
// 					{
// 						SkeletalMeshCpt->SetForcedLOD(SkeletalMeshCpt->PredictedLODLevel + 1);
// 						// 				SkeletalMeshCpt->bPauseAnims = true;
// 						// 				SkeletalMeshCpt->SuspendClothingSimulation();
// 					}
// 				}
			USkeletalMeshComponent* mesh = Cast<USkeletalMeshComponent>(GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_COATS));
			
		}

		PlayerCharacter->OnCreateRiderModelOver();

		///动作切换成功时--执行对部件的影响
		if (IsValid(GetBaseAnimInstance()) && !GetBaseAnimInstance()->OnActionChangeFinish.IsBound())
		{
			GetBaseAnimInstance()->OnActionChangeFinish.AddUObject(this, &ARiderCharacter::OnNotifyActionChangeFinish);
		}

		///显示捏脸表现
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->ModifyFaceManager)
			&& !PlayerCharacter->IsChangeModelState())
		{
			UUECS3GameInstance::Instance->ModifyFaceManager->SetBoneRef(this);
			UUECS3GameInstance::Instance->ModifyFaceManager->SetActorFaceData(this,
				PlayerCharacter->ModifyFaceDatas, PlayerCharacter->FaceStyleDatas);
		}
	}
}

void ARiderCharacter::BeginPlay()
{
	CollisionComponent->InitCollision();
	Super::BeginPlay();
}

void ARiderCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<URoleAppearanceComponent>(TEXT("RoleAppearanceComponent"));
}

void ARiderCharacter::OnNotifyActionChangeFinish(FACTION_DATA ActionData)
{
	CheckPartHideByAction(ActionData);
}

void ARiderCharacter::SetInitAction()
{
	InitActionId = "Idle_Free";
}

void ARiderCharacter::ApplayModelByPartsMap(TMap<MODEL_PART_TYPE, FString>& NewPartMap)
{
	GetAppearanceComponent()->ApplayModelByPartsMap(NewPartMap);
}

void ARiderCharacter::ChangeActorPart(MODEL_PART_TYPE pos, FString PartID)
{
	ChangeModelPart(pos, PartID);
}

void ARiderCharacter::UseRideAnimData(TSoftClassPtr<UAnimInstance> AnimationPath, TSoftObjectPtr<UDataTable> ActionConfigPath)
{
	GetAppearanceComponent()->SetAnimData(AnimationPath, ActionConfigPath);
}

void ARiderCharacter::SetModelData(TSharedPtr<FMODEL_DATA> ModelData)
{
	GetAppearanceComponent()->SetModelData(ModelData);
}

void ARiderCharacter::SetPlayerCharacter(AGameCharacter* InPlayerCharacter)
{
	GameCharacter = InPlayerCharacter;
}