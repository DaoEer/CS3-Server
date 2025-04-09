// Fill out your copyright notice in the Description page of Project Settings.


#include "TongNagualCharacter.h"
#include "Component/AppearanceComponent.h"
#include "GameData/EnumCsvDefine.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CfgManager.h"
#include "LogMacros.h"

ATongNagualCharacter::ATongNagualCharacter()
{
	CurrModelID = TEXT("");

	CharacterClassName = TEXT("TongNagualCharacter");
	ModelDatas.Empty();
	InitBaseComponent();
}

void ATongNagualCharacter::ChangeModelByModelID(FString ModelID)
{
	CurrModelID = ModelID;
	this->AppearanceComponent->CreateAppearance(ModelID);
}

FTONG_NAGUAL_MODEL_DATA ATongNagualCharacter::GetModelDataByScriptID(FString ScriptID)
{
	FTONG_NAGUAL_MODEL_DATA TempModelData;
	if (ModelDatas.Contains(ScriptID))
	{
		TempModelData = ModelDatas[ScriptID];
	}
	else
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const UConfigTable* DataConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TONG_NAGUAL_MODEL_DATA);
		if (DataConfig != nullptr)
		{
			const FTONG_NAGUAL_MODEL_DATA* ModelData = DataConfig->GetRow<FTONG_NAGUAL_MODEL_DATA>(ScriptID);
			if (ModelData != nullptr)
			{
				TempModelData = *ModelData;
				ModelDatas.Add(ScriptID, TempModelData);
			}
		}
	}
	return TempModelData;
}

void ATongNagualCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

void ATongNagualCharacter::OnCreateApperanceOver()
{
	if (CurrModelID == GetAppearanceComponent()->GetModelId())
	{
		//如果创建的模型是需要当前需要的，则通知界面显示
		OnCreateApperanceOver_BP();
	}
	else
	{
		//如果创建的模型不是当前需要的，则再次请求创建
		ChangeModelByModelID(CurrModelID);
	}
}
