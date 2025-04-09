// Fill out your copyright notice in the Description page of Project Settings.

#include "MonsterExtChartletCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/ParticleManager.h"
#include "Actor/Particle/DecalEffectEmitter.h"
#include "Util/CustomEffect/DecalEffect.h"
#include "Util/CS3Debug.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3GameInstance.h"


CONTROL_COMPILE_OPTIMIZE_START
AMonsterExtChartletCharacter::AMonsterExtChartletCharacter()
{
	CharacterClassName = TEXT("MonsterExtChartletCharacter");
}

void AMonsterExtChartletCharacter::BeginPlay()
{
	Super::BeginPlay();

}

void AMonsterExtChartletCharacter::OnCreateApperanceOver()
{
	onDisplayChartlet();
}

void AMonsterExtChartletCharacter::onDisplayChartlet()
{
	if (!this->GetSelfEntity())
	{
		return;
	}
	FString effectID = UGolbalBPFunctionLibrary::GetFStringPropertyValue(this->GetSelfEntity()->ID(), TEXT("effectID"));
	TWeakObjectPtr<AMonsterExtChartletCharacter> DelayThisPtr(this);
	UUECS3GameInstance::Instance->ParticleManager->PlayParticle(effectID, 0.0f, this, this, FEffectCreate::CreateLambda([DelayThisPtr](int32 UID)
	{
		AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
		if (DelayThisPtr.IsValid() && Effect)
		{
			AMonsterExtChartletCharacter* ThisPtr = DelayThisPtr.Get();
			ThisPtr->DecalEffectEmitter = Cast<ADecalEffectEmitter>(Effect);
			if (ThisPtr->DecalEffectEmitter->GetDecalArr().Num() < 0)
			{
				return;
			}

			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(ThisPtr, ThisPtr->ChartletTimeHandle, 
					FTimerDelegate::CreateLambda([DelayThisPtr]()
				{
					if (DelayThisPtr.IsValid())
					{
						AMonsterExtChartletCharacter* ThisPtr = DelayThisPtr.Get();
						if (ThisPtr->DecalEffectEmitter->GetDecalArr().Num() > 0)
						{
							for (auto Decal : ThisPtr->DecalEffectEmitter->GetDecalArr())
							{
								if (IsValid(Decal))
								{
									ADecalEffect* decaleffect = Cast<ADecalEffect>(Decal);
									TArray<FLinearColor> VectorColor = decaleffect->GetVectorParameter();
									if (VectorColor[0].A < 1)
									{
										decaleffect->SetVectorParameter(VectorColor[0].A += 0.1f);
										CS3_Display(CS3DebugType::CL_Undefined, TEXT("--------VectorColor aphal = %f"), VectorColor[0].A);
									}
									else
									{
										if (IsValid(UUECS3GameInstance::Instance))
										{
											UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->ChartletTimeHandle);
											CS3_Display(CS3DebugType::CL_Undefined, TEXT("--------VectorColor aphal is over = %f"), VectorColor[0].A);
										}
									}
								}
							}
						}
						else
						{
							if (IsValid(UUECS3GameInstance::Instance))
							{
								UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->ChartletTimeHandle);
							}
						}
					}
				}), 0.1f, true);
			}
		}
	}));
}	

void AMonsterExtChartletCharacter::onDisappearChartlet(const int32& type)
{
	if (type == 1)
	{
		TWeakObjectPtr<AMonsterExtChartletCharacter> DelayThisPtr(this);
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, ChartletTimeHandle, 
				FTimerDelegate::CreateLambda([DelayThisPtr]()
			{
				if (DelayThisPtr.IsValid())
				{
					AMonsterExtChartletCharacter* ThisPtr = DelayThisPtr.Get();
					if (ThisPtr->DecalEffectEmitter->GetDecalArr().Num() > 0)
					{
						for (auto Decal : ThisPtr->DecalEffectEmitter->GetDecalArr())
						{
							if (IsValid(Decal))
							{
								ADecalEffect* decaleffect = Cast<ADecalEffect>(Decal);
								TArray<FLinearColor> VectorColor = decaleffect->GetVectorParameter();
								if (VectorColor[0].A > 0)
								{
									decaleffect->SetVectorParameter(VectorColor[0].A -= 0.1f);
									CS3_Display(CS3DebugType::CL_Undefined, TEXT("--------VectorColor aphal = %f"), VectorColor[0].A);
								}
								else
								{
									if (IsValid(UUECS3GameInstance::Instance))
									{
										UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->ChartletTimeHandle);
										CS3_Display(CS3DebugType::CL_Undefined, TEXT("--------VectorColor aphal is over = %f"), VectorColor[0].A);
									}
									
								}
							}
						}
					}
					else
					{
						if (IsValid(UUECS3GameInstance::Instance))
						{
							UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->ChartletTimeHandle);
						}
					}
				}
			}), 0.1f, true);
		}
	}
	else if (type == 2)
	{

	}
}

CONTROL_COMPILE_OPTIMIZE_END
