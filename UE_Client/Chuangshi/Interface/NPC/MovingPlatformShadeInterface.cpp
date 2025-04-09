
#include "MovingPlatformShadeInterface.h"
#include "Actor/Scene/MovingPlatformCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ParticleManager.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(UMovingPlatformShadeInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMovingPlatformShadeInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

void UMovingPlatformShadeInterface::OnRep_shadeTime()
{
	FString endTime = UGolbalBPFunctionLibrary::GetFStringPropertyValue(EntityID, TEXT("shadeTime"));
	AMovingPlatformCharacter* platform = Cast<AMovingPlatformCharacter>(GetActor());
	if (!endTime.IsEmpty())
	{
		if (IsValid(platform))
		{
			TArray<FString> Times = UGolbalBPFunctionLibrary::SplitString(endTime);
			if (Times.Num() >= 2 && Times[0] == "1")
			{
				platform->starShade(Times[1]);
				if (Times.IsValidIndex(2))
				{
					UUECS3GameInstance::Instance->ParticleManager->PlayParticle(Times[2], 0.0f, platform, platform);
				}
			}
			if (Times.Num() >= 2 && Times[0] == "2")
			{
				platform->starDisPlay(Times[1]);
			}
		}
	}
	
}
