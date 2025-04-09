
#include "HeadProxyCharacter.h"

#include "TimerManager.h"

#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/ResourceManager.h"
#include "Util/ConvertUtil.h"
#include "Manager/CfgManager.h"
#include "Component/AppearanceComponent.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/ParticleManager.h"
#include "GameData/VoiceData.h"
#include "GameData/EnumCsvDefine.h"
#include "LevelSequenceActor.h"
#include "GameFramework/WorldSettings.h"
#include "ContentStreaming.h"
#include "Manager/HeadManager.h"
#include "Kismet/GameplayStatics.h"

CONTROL_COMPILE_OPTIMIZE_START
AHeadProxyCharacter::AHeadProxyCharacter()
{
	CharacterClassName = TEXT("HeadProxyCharacter");
	PrimaryActorTick.bCanEverTick = true;
	CreateRoleMesh();
	InitBaseComponent();
}

void AHeadProxyCharacter::BeginPlay()
{
	Super::BeginPlay();
	SetForceMipStreaming(true);
}

void AHeadProxyCharacter::SetForceMipStreaming(bool IsForceMipStreaming)
{
	TInlineComponentArray<UMeshComponent*> PrimitiveComponents;
	this->GetComponents(PrimitiveComponents);
	for (int32 ComponentIndex = 0, NumComponents = PrimitiveComponents.Num(); ComponentIndex < NumComponents; ++ComponentIndex)
	{
		if (Cast<USkinnedMeshComponent>(PrimitiveComponents[ComponentIndex]) ||
			Cast<UStaticMeshComponent>(PrimitiveComponents[ComponentIndex]))
		{
			PrimitiveComponents[ComponentIndex]->bForceMipStreaming = IsForceMipStreaming;
			IStreamingManager::Get().NotifyPrimitiveUpdated(PrimitiveComponents[ComponentIndex]);
		}
	}
}

void AHeadProxyCharacter::OnCreateModelOver()
{
	Super::OnCreateModelOver();
}

void AHeadProxyCharacter::OnCreateApperanceOver()
{
	LoadISOver = true;
	if (BustActionID != "")
	{
		PlayAction(BustActionID);
		BustActionID = "";
	}
	if (BustBackActonID!= "")
	{
		PlayAction(BustBackActonID);
		BustBackActonID = "";
	}
}

void AHeadProxyCharacter::ChangeModelByHeadID(FString HeadID)
{
	ResetCharacterAction();
	bool IsSuccess;
	FHEAD_MODEL_DATA HeadModelData = UGolbalBPFunctionLibrary::HeadManager()->GetHalfHeadModleDataByHeadID(HeadID, IsSuccess);
	if (!IsSuccess)
		return;
	ChangeModel(HeadModelData);
	//SetForceMipStreaming(true);
	
}

void AHeadProxyCharacter::ChangeModelByHeadModelData(FHEAD_MODEL_DATA HeadModelData)
{
	ResetCharacterAction();
	ChangeModel(HeadModelData);
}

void AHeadProxyCharacter::ChangeModel(FHEAD_MODEL_DATA HeadModelData)
{
	LoadISOver = false;
	// “#”标识符 特殊处理仙道魔道旁白
	if (HeadModelData.ModelID == "#")
	{
		APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		if (Player->GetFinalCamp() == 1)//仙道
		{
			this->AppearanceComponent->CreateAppearance("SK_NPCM1043_NPC");
		}
		else if (Player->GetFinalCamp() == 2)//魔道
		{
			this->AppearanceComponent->CreateAppearance("SK_NPCM1049_Mon");
		}
	}
	else if (!HeadModelData.ModelID.IsEmpty() && IsValid(this))
	{
		this->AppearanceComponent->CreateAppearance(HeadModelData.ModelID);
	}
	StartHeadModelAction(HeadModelData);
}

float AHeadProxyCharacter::GetSequenceRate()
{
	AWorldSettings* WorldSettings = GetWorld()->GetWorldSettings();
	float Rate = 0.0f;
	if (WorldSettings)
	{
		Rate = WorldSettings->MatineeTimeDilation;
	}
	return Rate;
}

FString AHeadProxyCharacter::GetModelID()
{
	return GetAppearanceComponent()->GetModelId();
}

void AHeadProxyCharacter::ResetModelData()
{
	ResetCharacterAction();
	TInlineComponentArray<UMeshComponent*> PrimitiveComponents;
	this->GetComponents(PrimitiveComponents);
	for (int32 ComponentIndex = 0, NumComponents = PrimitiveComponents.Num(); ComponentIndex < NumComponents; ++ComponentIndex)
	{
		if (Cast<USkeletalMeshComponent>(PrimitiveComponents[ComponentIndex]))
		{
			USkeletalMeshComponent* SkeletalMeshCom = Cast<USkeletalMeshComponent>(PrimitiveComponents[ComponentIndex]);
			SkeletalMeshCom->SetSkeletalMesh(nullptr);
		}
		else if (Cast<UStaticMeshComponent>(PrimitiveComponents[ComponentIndex]))
		{
			UStaticMeshComponent* StaticSkeletalMeshCom = Cast<UStaticMeshComponent>(PrimitiveComponents[ComponentIndex]);
			StaticSkeletalMeshCom->SetStaticMesh(nullptr);
		}
	}
}

void AHeadProxyCharacter::TargetPlayAction(AGameCharacter* Target, bool IsPlayer,FString HeadModelID)
{
	bool IsSuccess;
	FHEAD_MODEL_DATA HeadModelData = UGolbalBPFunctionLibrary::HeadManager()->GetHalfHeadModleDataByHeadID(HeadModelID, IsSuccess);
	if (!IsSuccess)
		return;
	StartModelAction(HeadModelData, Target);
}

void AHeadProxyCharacter::TargetPlayActionByHeadModelData(AGameCharacter* Target, bool IsPlayer, FHEAD_MODEL_DATA HeadModelData)
{
	StartModelAction(HeadModelData, Target);
}

void AHeadProxyCharacter::PlayAction_BP(AGameCharacter* Target, FName ActionID)
{
	Target->PlayAction(ActionID);
}

void AHeadProxyCharacter::ResetCharacterAction()
{
	if (IsValid(CurCharacter))
	{
		CurCharacter->StopAction();
		CurCharacter->PlayAction(CurCharacterActionID);
	}
	if (IsValid(this))
	{
		this->StopAction();
	}
	CurCharacterActionID = TEXT("");
	ActionIndex = 0;
	HeadActionIndex = 0;
	EffectIndex = 0;

	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (EffectEventHandle.IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(EffectEventHandle);
		}
		if (ModelActionEventHandle.IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ModelActionEventHandle);
		}
		if (HeadModelActionEventHandle.IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(HeadModelActionEventHandle);
		}
	}
	for (int32 UID : EffectArray)
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(UID);
	}
	EffectArray.Reset();
	EffectArray.Empty();
}

void AHeadProxyCharacter::StartModelAction(FHEAD_MODEL_DATA HeadModelData, AGameCharacter* Target)
{
	if (CurCharacterActionID == TEXT(""))
	{
		if (IsValid(Target))
		{
			CurCharacter = Target;
			if (IsValid(Target->GetBaseAnimInstance()))
			{
				CurCharacterActionID = Target->GetBaseAnimInstance()->GetCurPlayActionData().Id;
			}
		}
		else
		{
			return;
		}
	}
	
	if (HeadModelData.ModelActionData.IsValidIndex(ActionIndex))
	{
		FHEAD_MODEL_ACTION_DATA ModelActionList = HeadModelData.ModelActionData[ActionIndex];
		if (ModelActionList.ModelActionTime <= 0)
		{
			Target->PlayAction(FSTRING_TO_FNAME(ModelActionList.ModelFrontActionID));
			Target->PlayAction(FSTRING_TO_FNAME(ModelActionList.ModelBackActionID));	
			if (HeadModelData.ModelActionData.Num() - 1 > ActionIndex)
			{
				ActionIndex += 1;
				StartModelAction(HeadModelData, Target);
			}
		}
		else
		{
			TWeakObjectPtr<AHeadProxyCharacter> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, ModelActionEventHandle, 
				FTimerDelegate::CreateLambda([DelayThisPtr, ModelActionList, HeadModelData, Target]()
			{
				Target->PlayAction(FSTRING_TO_FNAME(ModelActionList.ModelFrontActionID));
				Target->PlayAction(FSTRING_TO_FNAME(ModelActionList.ModelBackActionID));
				if (HeadModelData.ModelActionData.Num() - 1 > DelayThisPtr->ActionIndex)
				{
					DelayThisPtr->ActionIndex += 1;
					DelayThisPtr->StartModelAction(HeadModelData, Target);
				}
			}), ModelActionList.ModelActionTime, false);
		}	
	}
}

void AHeadProxyCharacter::StartHeadModelAction(FHEAD_MODEL_DATA HeadModelData)
{
	if (HeadModelData.HeadModelActionData.IsValidIndex(HeadActionIndex)) 
	{
		FHEAD_BUST_MODEL_ACTION_DATA HeadModelActionList = HeadModelData.HeadModelActionData[HeadActionIndex];
		if (HeadModelActionList.BustActionTime<=0)
		{
			if (LoadISOver)
			{
				this->PlayAction(FSTRING_TO_FNAME(HeadModelActionList.HeadModelFrontActionID));
				this->PlayAction(FSTRING_TO_FNAME(HeadModelActionList.HeadModelBackActionID));
			}
			else
			{
				BustActionID = FSTRING_TO_FNAME(HeadModelActionList.HeadModelFrontActionID);
				BustBackActonID = FSTRING_TO_FNAME(HeadModelActionList.HeadModelBackActionID);
			}
			if (HeadModelData.HeadModelActionData.Num() - 1 > HeadActionIndex)
			{
				HeadActionIndex += 1;
				StartHeadModelAction(HeadModelData);
			}
		}
		else
		{
			TWeakObjectPtr<AHeadProxyCharacter> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, HeadModelActionEventHandle, FTimerDelegate::CreateLambda([DelayThisPtr, HeadModelActionList, HeadModelData]()
			{
				if (DelayThisPtr->LoadISOver)
				{
					AHeadProxyCharacter* ThisPtr = DelayThisPtr.Get();
					DelayThisPtr->PlayAction(FSTRING_TO_FNAME(HeadModelActionList.HeadModelFrontActionID));
					DelayThisPtr->PlayAction(FSTRING_TO_FNAME(HeadModelActionList.HeadModelBackActionID));
				}
				else
				{
					DelayThisPtr->BustActionID = FSTRING_TO_FNAME(HeadModelActionList.HeadModelFrontActionID);
					DelayThisPtr->BustBackActonID = (FSTRING_TO_FNAME(HeadModelActionList.HeadModelBackActionID));
				}
				if (HeadModelData.HeadModelActionData.Num() - 1 > DelayThisPtr->HeadActionIndex)
				{
					DelayThisPtr->HeadActionIndex += 1;
					DelayThisPtr->StartHeadModelAction(HeadModelData);
				}
			}), HeadModelActionList.BustActionTime, false);
		}
	}
	else
	{
		PlayAction(TEXT("Idle_Free"));
	}
}

void AHeadProxyCharacter::PlayParticleModel(AGameCharacter* Target, TArray<FHEAD_MODEL_EFFECT_DATA> EffectData)
{
	AServerCharacter* Player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	PlayParticle(Target, Player, EffectData);
}

void AHeadProxyCharacter::PlayParticleModelTest(AGameCharacter* Target, TArray<FHEAD_MODEL_EFFECT_DATA> EffectData)
{
	ACharacter* ServerCharacter = UGameplayStatics::GetPlayerCharacter(UUECS3GameInstance::Instance->GetWorld(), 0);
	if (ServerCharacter)
	{
		PlayParticle(Target, ServerCharacter, EffectData);
	}
}

void AHeadProxyCharacter::PlayParticle(AGameCharacter* Target, ACharacter* Player, TArray<FHEAD_MODEL_EFFECT_DATA> EffectData)
{
	if (EffectData.Num() > 0)
	{
		if (EffectData[EffectIndex].EffectTime <= 0)
		{
			if (EffectData[EffectIndex].isPlayer)
			{
				//AServerCharacter* Player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
				int32 UID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectData[EffectIndex].EffectID, 0.0f, Player, Player);
				EffectArray.Add(UID);
			}
			else
			{
				int32 UID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectData[EffectIndex].EffectID, 0.0f, Target, Target);
				EffectArray.Add(UID);
			}
			if (EffectData.Num() - 1 > EffectIndex)
			{
				EffectIndex += 1;
				PlayParticleModel(Target, EffectData);
			}
		}
		else
		{
			TWeakObjectPtr<AHeadProxyCharacter> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, EffectEventHandle, FTimerDelegate::CreateLambda([DelayThisPtr, Target, Player, EffectData]()
			{
				if (EffectData[DelayThisPtr->EffectIndex].isPlayer)
				{
					//AServerCharacter* Player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
					int32 UID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectData[DelayThisPtr->EffectIndex].EffectID, 0.0f, Player, Player);
					DelayThisPtr->EffectArray.Add(UID);

				}
				else
				{
					int32 UID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectData[DelayThisPtr->EffectIndex].EffectID, 0.0f, Target, Target);
					DelayThisPtr->EffectArray.Add(UID);

				}
				if (EffectData.Num() - 1 > DelayThisPtr->EffectIndex)
				{
					DelayThisPtr->EffectIndex += 1;
					DelayThisPtr->PlayParticleModel(Target, EffectData);
				}
			}), EffectData[EffectIndex].EffectTime, false);
		}
	}
}

void AHeadProxyCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}
CONTROL_COMPILE_OPTIMIZE_END
