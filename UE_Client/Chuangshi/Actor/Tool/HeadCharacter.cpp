#include "HeadCharacter.h"
#include "Component/AppearanceComponent.h"

#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
AHeadCharacter::AHeadCharacter()
{
	CharacterClassName = TEXT("HeadCharacter");
	PrimaryActorTick.bCanEverTick = true;
	CreateRoleMesh();
	InitBaseComponent();
}

void AHeadCharacter::BeginPlay()
{
	Super::BeginPlay();
}

void AHeadCharacter::OnCreateModelOver()
{
	Super::OnCreateModelOver();
}

void AHeadCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();
}

void AHeadCharacter::ChangeModel(FString ModelID)
{
	if (!ModelID.IsEmpty() && this->AppearanceComponent)
	{
		this->AppearanceComponent->CreateAppearance(ModelID);
	}
}

void AHeadCharacter::PlayAction_BP(FName ActionID)
{
	this->PlayAction(ActionID);
}

void AHeadCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

CONTROL_COMPILE_OPTIMIZE_END