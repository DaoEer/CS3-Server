// Fill out your copyright notice in the Description page of Project Settings.

#include "PetCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/VehiclePet/PetPosSyncComponent.h"
#include "Component/DumbfilterActorComponent.h"
#include "Interface/VehiclePet/VehiclePetInterface.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Component/FightComponent.h"
#include "Component/AvatarFilterActorComponent.h"
#include "Component/AppearanceComponent.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"
#include "GameData/PetData.h"
#include "Manager/SkillManager.h"

void APetCharacter::InitFilterActorComponent()
{
	AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	bool IsStartActiveFilter(false);
	if (GetSelfEntity() != nullptr && IsValid(PlayerCharacter) && UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerCharacter->EntityId, TEXT("activePetID")) == EntityId)
	{
		SetFilterComponent(NewObject<UDumbFilterActorComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr));
		IsStartActiveFilter = false;
	}
	else
	{
		SetFilterComponent(NewObject<UAvatarFilterActorComponent>(this, "root", RF_NoFlags, nullptr, false, nullptr));
		IsStartActiveFilter = true;
	}
	GetFilterComponent()->RegisterComponent();
	GetFilterComponent()->InitFilter(IsStartActiveFilter);
}

APetCharacter::APetCharacter()
{
	CharacterClassName = TEXT("PetCharacter");
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = true;

	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	InitBaseComponent();
}
 
void APetCharacter::BeginPlay()
{
	Super::BeginPlay();
}

bool APetCharacter::IsActiveMoveing()
{
	if (GetSelfEntity() != nullptr)
	{
		if (IsMoveing())
		{
			return true;
		}
		return false;
	}
	return false;
}

bool APetCharacter::IsMoveing()
{
	if (PetIsPlayer())
	{
		return !GetCharacterMovement()->Velocity.IsZero();
	}
	else
	{
		return GetFilterSpeed() > 0.0f ? true : false;
	}
	
}

void APetCharacter::RunDefaultAITree()
{
	if (!IsValid(DefaultBTree))
	{
		DefaultBTree = Cast<UBehaviorTree>(LoadObject<UObject>(NULL, *(FString("BehaviorTree'/Game/BluePrints/Behavior/BT_VehiclePet.BT_VehiclePet'"))));
	}
	if (!IsValid(DefaultBTree))return;
	AAIController* controller = Cast<AAIController>(GetController());
	if (!IsValid(controller))return;
	controller->RunBehaviorTree(DefaultBTree);
}

void APetCharacter::OnChangePetAI(FString AIIndex)
{
	OnBroadCreateModelOver.Unbind();
	const UConfigTable* ConfigTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET_ST_AI_DATA);
	if (ConfigTable)
	{
		const FPET_ST_AI_DATA* STAIData = ConfigTable->GetRow<FPET_ST_AI_DATA>(AIIndex);
		if (STAIData)
		{
			UBehaviorTree* tempBT = Cast<UBehaviorTree>(UGolbalBPFunctionLibrary::LoadObjectByAssetPath(STAIData->PetAITree));
			if (IsValid(tempBT))
			{
				UBlackboardComponent* lastBlackBoard = UAIBlueprintHelperLibrary::GetBlackboard(this);
				uint8 attackType(0);
				uint8 commondType(0);
				if (IsValid(lastBlackBoard))
				{
					attackType = lastBlackBoard->GetValueAsEnum(FName(TEXT("AttackType")));
					commondType = lastBlackBoard->GetValueAsEnum(FName(TEXT("CurCommand")));
				}

				AAIController* controller = Cast<AAIController>(GetController());
				if (!IsValid(controller))return;
				controller->RunBehaviorTree(tempBT);

				UBlackboardComponent* myBlackBoard = UAIBlueprintHelperLibrary::GetBlackboard(this);
				if (IsValid(myBlackBoard))
				{
					AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
					myBlackBoard->SetValueAsObject(FName(TEXT("OwnerPlayer")), PlayerCharacter);
					myBlackBoard->SetValueAsEnum(FName(TEXT("AttackType")), attackType);					// 用于恢复之前的状态
					myBlackBoard->SetValueAsEnum(FName(TEXT("CurCommand")), commondType);

					myBlackBoard->SetValueAsInt(FName(TEXT("Param1")), STAIData->Param1);
					myBlackBoard->SetValueAsInt(FName(TEXT("Param2")), STAIData->Param2);
					myBlackBoard->SetValueAsString(FName(TEXT("Param3")), STAIData->Param3);
					myBlackBoard->SetValueAsString(FName(TEXT("Param4")), STAIData->Param4);
					STSkillArr = STAIData->SkillArr;
					UUECS3GameInstance::Instance->SkillManager->InitActPetSkills(STSkillArr);
				}
			}
		}
	}
}

void APetCharacter::OnFinishChangePetAI()
{
	RunDefaultAITree();
}

void APetCharacter::InitBaseComponent()
{
	FightComponent = CreateDefaultSubobject<UFightComponent>(TEXT("FightComponent"));
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

void APetCharacter::InitCharacterComponent()
{
	Super::InitCharacterComponent();
	
	//如果宠物是玩家的宠物，就往服务器同步位置
	if (PetIsPlayer())
	{
		UVehiclePetInterface* VehiclePetInterface = Cast<UVehiclePetInterface>(GetEntityInterface_Cache().GameObjectInterface);
		if (VehiclePetInterface)
		{
			VehiclePetInterface->RPC_onSetPetControlledBy();
		}
		InitPosSyncComponent();

		UCharacterMovementComponent* movementComponent = GetCharacterMovement();
		if (IsValid(movementComponent))
		{
			movementComponent->SetAutoActivate(true);
			movementComponent->SetActive(true);
			SetMaxWalkSpeed(GetMoveSpeed() * 100.0f);
			movementComponent->bOrientRotationToMovement = true;
			movementComponent->bConstrainToPlane = true;
			movementComponent->bSnapToPlaneAtStart = true;
		}
		
		SpawnDefaultController();
		RunDefaultAITree();
		UBlackboardComponent* myBlackBoard = UAIBlueprintHelperLibrary::GetBlackboard(this);
		if (IsValid(myBlackBoard))
		{
			AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
			myBlackBoard->SetValueAsObject(FName(TEXT("OwnerPlayer")), PlayerCharacter);
			myBlackBoard->SetValueAsEnum(FName(TEXT("AttackType")), 1);
		}
	}
}

void APetCharacter::InitPosSyncComponent()
{
	PetPosSyncComponent = NewObject<UPetPosSyncComponent>(this, "TransFormControl", RF_NoFlags, nullptr, false, nullptr);
	PetPosSyncComponent->RegisterComponent();
	PetPosSyncComponent->SetActive(true);
}

float APetCharacter::GetMoveSpeed()
{ 
	return UGolbalBPFunctionLibrary::GetFloatPropertyValue(EntityId, TEXT("moveSpeed"));
}	
