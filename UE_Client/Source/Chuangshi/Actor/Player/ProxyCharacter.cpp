// Fill out your copyright notice in the Description page of Project Settings.


#include "ProxyCharacter.h"
#include "Util/ConvertUtil.h"
#include "Component/AppearanceComponent.h"


AProxyCharacter::AProxyCharacter()
{
	CharacterClassName = TEXT("ProxyCharacter");
	PrimaryActorTick.bCanEverTick = true;
	CreateRoleMesh();
	InitBaseComponent();
}

void AProxyCharacter::BeginPlay()
{
	Super::BeginPlay();
}

void AProxyCharacter::OnCreateModelOver()
{
	Super::OnCreateModelOver();
}

void AProxyCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();
	//加载完成后检测部件隐显
	if(IsValid(GetBaseAnimInstance()))
	{
		CheckPartHideByAction(GetBaseAnimInstance()->GetCurPlayActionData());
	}

}

void AProxyCharacter::CreateModelAppearance(ACharacter * CopyCharacter, bool IsClientAppearance)
{
	bIsChangeAppearanceling = true;
	if (IsClientAppearance)
	{
		GetAppearanceComponent()->CopyCharacterFromClientAppearance(CopyCharacter);
	}
	else
	{
		GetAppearanceComponent()->CopyCharacterFromServerAppearance(CopyCharacter);
	}
}

void AProxyCharacter::PlayAction_BP(FString InActionID)
{
	PlayAction(FSTRING_TO_FNAME(InActionID));
}

void AProxyCharacter::HeadModelPlayAction_BP(TArray<FHEAD_BUST_MODEL_ACTION_DATA> HeadModelData)
{
	if (HeadModelData.Num()>0)
	{
		if (HeadModelData[ModelAcitonIndex].BustActionTime <= 0)
		{
			PlayAction(FSTRING_TO_FNAME(HeadModelData[ModelAcitonIndex].HeadModelFrontActionID));
			PlayAction(FSTRING_TO_FNAME(HeadModelData[ModelAcitonIndex].HeadModelBackActionID));
			if (HeadModelData.Num() - 1 > ModelAcitonIndex)
			{
				ModelAcitonIndex += 1;
				HeadModelPlayAction_BP(HeadModelData);
			}
		}
		else
		{
			TWeakObjectPtr<AProxyCharacter> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, ModelActionEventHandle, FTimerDelegate::CreateLambda([DelayThisPtr, HeadModelData]()
			{
				DelayThisPtr->PlayAction(FSTRING_TO_FNAME(HeadModelData[DelayThisPtr->ModelAcitonIndex].HeadModelFrontActionID));
				DelayThisPtr->PlayAction(FSTRING_TO_FNAME(HeadModelData[DelayThisPtr->ModelAcitonIndex].HeadModelBackActionID));
				if (HeadModelData.Num() - 1 > DelayThisPtr->ModelAcitonIndex)
				{
					DelayThisPtr->ModelAcitonIndex += 1;
					DelayThisPtr->HeadModelPlayAction_BP(HeadModelData);
				}
			}), HeadModelData[ModelAcitonIndex].BustActionTime, false);
		}
	}
	else
	{
		PlayAction(TEXT("Idle_Free"));
	}
}

void AProxyCharacter::RestActionData()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (ModelActionEventHandle.IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ModelActionEventHandle);
		}
	}
	ModelAcitonIndex = 0;
}

void AProxyCharacter::UpdateModelApperance(int32 Camp, int32 Profession, TArray<UItemBase*> EquipArray, int32 Gender = 1)
{
	///阵营 1：仙  2：魔   
	///性别 1：男  2：女
	///门派 1：战士 2：剑客 3：链刃 4：法师
	FString ModelID;
	if (Camp == 1)
	{
		if (Gender == 1)
		{
			if (Profession ==1)
			{
				ModelID = "SK_InitPC_M_01KunLun";
				
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_M_01KunLun");
			}
			else if (Profession == 2)
			{
				ModelID = "SK_InitPC_M_02YuXu";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_M_02YuXu");
			}
			else if (Profession == 3)
			{
				ModelID = "SK_InitPC_M_03PengLai";
	//			UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_M_03PengLai");
			}
			else if (Profession == 4)
			{
				ModelID = "SK_InitPC_M_04TaiQing";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_M_04TaiQing");
			}
		}
		else if (Gender == 2)
		{
			if (Profession == 1)
			{
				ModelID = "SK_InitPC_F_01KunLun";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_F_01KunLun");
			}
			else if (Profession == 2)
			{
				ModelID = "SK_InitPC_F_02YuXu";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_F_02YuXu");
			}
			else if (Profession == 3)
			{
				ModelID = "SK_InitPC_F_03PengLai";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_F_03PengLai");
			}
			else if (Profession == 4)
			{
				ModelID = "SK_InitPC_F_04TaiQing";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_F_04TaiQing");
			}
		}

	}
	else if (Camp == 2)
	{
		if (Gender == 1)
		{
			if (Profession == 1)
			{
				ModelID = "SK_InitPC_M_05XiuLuo";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_M_05XiuLuo");
			}
			else if (Profession == 2)
			{
				ModelID = "SK_InitPC_M_06XiaoYao";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_M_06XiaoYao");
			}
			else if (Profession == 3)
			{
				ModelID = "SK_InitPC_M_07PiaoMiao";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_M_07PiaoMiao");
			}
			else if (Profession == 4)
			{
				ModelID = "SK_InitPC_M_08MoHe";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_M_08MoHe");
			}
		}
		else if (Gender == 2)
		{
			if (Profession == 1)
			{
				ModelID = "SK_InitPC_F_05XiuLuo";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_F_05XiuLuo");
			}
			else if (Profession == 2)
			{
				ModelID = "SK_InitPC_F_06XiaoYao";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_F_06XiaoYao");
			}
			else if (Profession == 3)
			{
				ModelID = "SK_InitPC_F_07PiaoMiao";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_F_07PiaoMiao");
			}
			else if (Profession == 4)
			{
				ModelID = "SK_InitPC_F_08MoHe";
//				UGolbalBPFunctionLibrary::CS3SetModelPart(this, "SK_InitPC_F_08MoHe");
			}
		}
	}
	GetAppearanceComponent()->CreateAppearance(ModelID);
}

FString AProxyCharacter::GetModelID()
{
	return GetAppearanceComponent()->GetModelId();
}

void AProxyCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<URoleAppearanceComponent>(TEXT("RoleAppearanceComponent"));
}
