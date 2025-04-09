
#include "PetProxyCharacter.h"

#include "Component/AppearanceComponent.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "ContentStreaming.h"

CONTROL_COMPILE_OPTIMIZE_START
APetProxyCharacter::APetProxyCharacter()
{
	CharacterClassName = TEXT("PetProxyCharacter");
	PrimaryActorTick.bCanEverTick = true;
	InitBaseComponent();
}

void APetProxyCharacter::BeginPlay()
{
	Super::BeginPlay();
}

void APetProxyCharacter::OnCreateModelOver()
{
	Super::OnCreateModelOver();
}

void APetProxyCharacter::OnCreateApperanceOver()
{
	
}

void APetProxyCharacter::PlayAction_BP(FName ActionID)
{
	FActionOverDelegate ActionOverDelegate;
	ActionOverDelegate.AddUObject(this, &APetProxyCharacter::PlayActionFinish);
	PlayAction(ActionID, 0.0f, ActionOverDelegate);
}

void APetProxyCharacter::PlayActionFinish(ACharacter* Character, FACTION_DATA InActionData)
{
	//动作播放完成，继续播放待机动作
	if (!InActionData.Id.IsEqual(TEXT("Idle_Free")))
	{
		PlayAction(TEXT("Idle_Free"));
	}
}

void APetProxyCharacter::ChangeModel(FString ModelID)
{
	if (!ModelID.IsEmpty() && IsValid(this))
	{
		this->AppearanceComponent->CreateAppearance(ModelID);
	}
}

FString APetProxyCharacter::GetModelID()
{
	return this->GetAppearanceComponent()->GetModelId();
}

void APetProxyCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}
CONTROL_COMPILE_OPTIMIZE_END
