// Fill out your copyright notice in the Description page of Project Settings.


#include "GMTestInterface.h"
#include "KBEngine.h"
#include "Actor/ServerCharacter.h"
#include "Actor/Pet/RiderCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "GameDevelop/CS3GameInstance.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UGMTestInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(GMTestOpenEffect, &UGMTestInterface::GMTestOpenEffect, const FString&, const uint8&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UGMTestInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UGMTestInterface::UGMTestInterface()
{
	
}

UGMTestInterface::~UGMTestInterface()
{
	
}

void UGMTestInterface::GMTestOpenEffect(const FString& effectType, const uint8& isOpen)
{
	if (effectType == TEXT("Fire"))
	{
		if (IsValid(UUECS3GameInstance::Instance) && UUECS3GameInstance::Instance->pKBEApp)
		{
			TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
			for (auto& elem : EntitiesMap)
			{
				KBEngine::Entity*  e = elem.Value;
				if (e->ClassName() == TEXT("VehiclePet"))
				{
					AActor* actorPtr = e->Actor();
					if (IsValid(actorPtr))
					{
						AServerCharacter* charPtr = Cast< AServerCharacter >(actorPtr);
						if (isOpen == 0)
							charPtr->GetMesh()->SetScalarParameterValueOnMaterials( "Fire_Enable",0.f );
						else
							charPtr->GetMesh()->SetScalarParameterValueOnMaterials("Fire_Enable", 1.f);
					}
				}
				else if (e->ClassName() == TEXT("Role"))
				{
					if(APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(e->Actor()))
					{
						if(PlayerCharacter->GetRiderCharacter())
						{
							if (isOpen == 0)
								PlayerCharacter->GetMesh()->SetScalarParameterValueOnMaterials( "Fire_Enable",0.f );
							else
								PlayerCharacter->GetMesh()->SetScalarParameterValueOnMaterials("Fire_Enable", 1.f);
						}
					}
				}
			}
		}
	}else if (effectType == TEXT("SelfLight"))
	{
		if (IsValid(UUECS3GameInstance::Instance) && UUECS3GameInstance::Instance->pKBEApp)
		{
			TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
			for (auto& elem : EntitiesMap)
			{
				KBEngine::Entity* e = elem.Value;
				AActor* actorPtr = e->Actor();
				if (IsValid(actorPtr))
				{
					AServerCharacter* charPtr = Cast< AServerCharacter >(actorPtr);
					if (isOpen == 0)
						charPtr->GetMesh()->SetScalarParameterValueOnMaterials("Hair_EnableEmissive", 0.f);
					else
						charPtr->GetMesh()->SetScalarParameterValueOnMaterials("Hair_EnableEmissive", 1.f);
				}
			}
		}
	}
}
	