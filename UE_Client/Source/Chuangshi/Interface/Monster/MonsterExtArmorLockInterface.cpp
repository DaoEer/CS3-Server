#include "MonsterExtArmorLockInterface.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Actor/ServerCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtArmorLockInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtArmorLockInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtArmorLockInterface::UMonsterExtArmorLockInterface()
{
}


UMonsterExtArmorLockInterface::~UMonsterExtArmorLockInterface()
{
}

void UMonsterExtArmorLockInterface::EnterArmorLock_Implementation()
{
	if (IsValid(GetActor()))
	{
		AServerCharacter* character = Cast<AServerCharacter>(GetActor());
		if (IsValid(character))
		{
			character->GetMesh()->SetScalarParameterValueOnMaterials("Dis_Panner", 0.0f);
		}
	}
}

void UMonsterExtArmorLockInterface::ExitArmorLock_Implementation(const float OutTime)
{
	DelayTime = OutTime;
	CoverParameter = 0.0f;
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(CoverEventHandle, this, &UMonsterExtArmorLockInterface::MaterialTimer, 0.01f, true);
}

void UMonsterExtArmorLockInterface::MaterialTimer()
{
	if (IsValid(GetActor()))
	{
		AServerCharacter* character = Cast<AServerCharacter>(GetActor());
		if (IsValid(character))
		{
			if (CoverParameter<1)
			{
				CoverParameter += 0.01f / DelayTime;
				character->GetMesh()->SetScalarParameterValueOnMaterials("Dis_Panner", CoverParameter);
			}
			else
			{
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CoverEventHandle);
			}
		}
	}
}

void UMonsterExtArmorLockInterface::InitBlueCB()
{
	ArrBlueFunc.Add("EnterArmorLock");
	ArrBlueFunc.Add("ExitArmorLock");
	Supper::InitBlueCB();
}