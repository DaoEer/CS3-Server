#include "HeadManager.h"

#include "Kismet/KismetRenderingLibrary.h"
#include "Kismet/KismetMaterialLibrary.h"
#if WITH_EDITOR
#include "FileHelpers.h"
#endif

#include "Chuangshi.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/CfgManager.h"
#include "Manager/ResourceManager.h"
#include "Actor/Player/HeadProxyCharacter.h"
#include "Kismet/GameplayStatics.h"
#include "Util/ConvertUtil.h"
#include "GameStatus.h"


CONTROL_COMPILE_OPTIMIZE_START
AHeadManager::AHeadManager()
{

}

AHeadManager::~AHeadManager()
{

}

AHeadManager* AHeadManager::GetInstance()
{
	cs3_checkNoReentry();
	return UGolbalBPFunctionLibrary::SpawnActor<AHeadManager>(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_HeadManager")));

//	return NewObject<AHeadManager>();
}

void AHeadManager::BeginPlay()
{
	Super::BeginPlay();
	InitHalfHeadTableData();
}

void AHeadManager::StartHalfHeadSetting()
{
#if WITH_EDITOR
	IsHeadSetting = true;
	IsChangeSetting = false;
	IsChangeTransSetting = false;
#endif
}

void AHeadManager::StopHalfHeadSetting()
{
#if WITH_EDITOR
	//如果不是正在配置，则不需要重新保存表
	if (!IsHeadSetting)
	{
		return;
	}
	IsHeadSetting = false;
	SaveHalfHeadTableData();
	DestroyHalfHeadCharacter();
#endif
}

void AHeadManager::UpdateHalfHeadTableData(const FString& HeadID, const FTransform& Transform, const float& FOVAngle)
{
#if WITH_EDITOR
	if (HalfHeadTranConfigTable == NULL || HeadID == TEXT(""))
	{
		return;
	}
	FHEAD_MODEL_TRANSFORM_DATA* RData = HalfHeadTranConfigTable->FindRow<FHEAD_MODEL_TRANSFORM_DATA>(FSTRING_TO_FNAME(HeadID),TEXT(""));
	if (RData)
	{
		for (TFieldIterator<UProperty> It(HalfHeadTranConfigTable->RowStruct); It; ++It)
		{
			UProperty* BaseProp = *It;
			//uint8* RData = HalfHeadTranConfigTable->GetRowMap()[RowName];
			FString PropertyName = BaseProp->GetDisplayNameText().ToString();
			if (PropertyName.Equals(TEXT("Transform")))
			{
				if (UStructProperty* StructProperty = Cast<UStructProperty>(BaseProp))
				{
					if (StructProperty != NULL && StructProperty->Struct == TBaseStructure<FTransform>::Get())
					{
						*StructProperty->ContainerPtrToValuePtr<FTransform>(RData) = Transform;
					}
				}
			}
			else if (PropertyName.Equals(TEXT("FOVAngle")))
			{
				if (UFloatProperty* FloatProp = Cast<UFloatProperty>(BaseProp))
				{
					FloatProp->SetPropertyValue_InContainer(RData, FOVAngle);
				}
			}
		}
	}
	else
	{
		FHEAD_MODEL_TRANSFORM_DATA HeadModelTranCreen;
		HeadModelTranCreen.FOVAngle = FOVAngle;
		HeadModelTranCreen.Transform = Transform;
		FString TableName = "DataTable'/Game/Miscs/ContentConfig/Audio/DT_HeadModelTransformCfg.DT_HeadModelTransformCfg'";
		UDataTable* Table = LoadObject<UDataTable>(NULL, *TableName);
		if (Table)
		{
			Table->AddRow(FSTRING_TO_FNAME(HeadID), HeadModelTranCreen);
		}
	}
	IsChangeTransSetting = true;
#endif
}

void AHeadManager::UpdateHalfHeadModelTableData(const FString& HeadID, const FString& ModelID, const TArray<FHEAD_MODEL_ACTION_DATA>& ModelActionData, const TArray<FHEAD_BUST_MODEL_ACTION_DATA>& HeadModelActionData, const TArray<FHEAD_MODEL_EFFECT_DATA>& ModelEffectData)
{
#if WITH_EDITOR
	if (HalfHeadConfigTable == NULL || HeadID == TEXT("") || ModelID == TEXT(""))
	{
		return;
	}
	FName RowName = FSTRING_TO_FNAME(HeadID);
	FHEAD_MODEL_DATA* RData = (FHEAD_MODEL_DATA*)HalfHeadConfigTable->GetRowMap()[RowName];

	// 修改本HeadID的数据
	if (RData)
	{
		for (TFieldIterator<UProperty> It(HalfHeadConfigTable->RowStruct); It; ++It)
		{
			UProperty *BaseProp = *It;
			FString PropertyName = BaseProp->GetDisplayNameText().ToString();

			if (PropertyName.Equals(TEXT("ModelID")))
			{
				if (UStrProperty* StrProperty = Cast<UStrProperty>(BaseProp))
				{
					StrProperty->SetPropertyValue_InContainer(RData, ModelID);
				}
			}
			else if (PropertyName.Equals(TEXT("Model Action Data")))
			{
				if (UArrayProperty* ArrayProperty = Cast<UArrayProperty>(BaseProp))
				{
					if (ArrayProperty != NULL)
					{
						*ArrayProperty->ContainerPtrToValuePtr<TArray<FHEAD_MODEL_ACTION_DATA>>(RData) = ModelActionData;
					}
				}
			}
			else if (PropertyName.Equals(TEXT("Head Model Action Data")))
			{
				if (UArrayProperty* ArrayProperty = Cast<UArrayProperty>(BaseProp))
				{
					if (ArrayProperty != NULL)
					{
						*ArrayProperty->ContainerPtrToValuePtr<TArray<FHEAD_BUST_MODEL_ACTION_DATA>>(RData) = HeadModelActionData;
					}
				}
			}
			else if (PropertyName.Equals(TEXT("Model Effect Data")))
			{
				if (UArrayProperty* ArrayProperty = Cast<UArrayProperty>(BaseProp))
				{
					if (ArrayProperty != NULL)
					{
						*ArrayProperty->ContainerPtrToValuePtr<TArray<FHEAD_MODEL_EFFECT_DATA>>(RData) = ModelEffectData;
					}
				}
			}
		}
	}
	IsChangeSetting = true;
#endif
}

void AHeadManager::SetCurrModelID(FString ModelID)
{
	if (ModelID == TEXT(""))
	{
		CurrModelID = CurrPlayerModelID;
	}
	else
	{
		CurrModelID = ModelID;
	}
}

void AHeadManager::DestroyHalfHeadCharacter()
{
#if WITH_EDITOR
	for (AGameCharacter* TempActor : HalfHeadCharacters)
	{
		TempActor->Destroy();
	}
	HalfHeadCharacters.Empty();
	HalfHeadMaterialIns.Empty();
#endif
}

bool AHeadManager::SaveHalfHeadTableData()
{
#if WITH_EDITOR
	if (!IsChangeSetting && !IsChangeTransSetting)
	{
		return true;
	}

	TArray<UPackage*> PackagesToSave;

	if (IsChangeSetting)
	{
		check(IsValid(HalfHeadConfigTable) && HalfHeadConfigTable->IsAsset());
		PackagesToSave.Add(HalfHeadConfigTable->GetOutermost());
		IsChangeSetting = false;
	}
	if (IsChangeTransSetting)
	{
		check(IsValid(HalfHeadTranConfigTable) && HalfHeadTranConfigTable->IsAsset());
		PackagesToSave.Add(HalfHeadTranConfigTable->GetOutermost());
		IsChangeTransSetting = false;
	}

	FEditorFileUtils::EPromptReturnCode ret = FEditorFileUtils::PromptForCheckoutAndSave(PackagesToSave, false, false);

	return ret == FEditorFileUtils::EPromptReturnCode::PR_Success;
#else
	return true;
#endif
}

FHEAD_MODEL_DATA AHeadManager::GetHalfHeadModleDataByHeadID(const FString& HeadID, bool& IsSuccess)
{
	IsSuccess = false;
	if (HalfHeadConfigTable)
	{
		for (auto it : HalfHeadConfigTable->GetRowMap())
		{
			FHEAD_MODEL_DATA* HeadData = (FHEAD_MODEL_DATA*)it.Value;
			if (HeadData->HeadID == HeadID)
			{
				IsSuccess = true;
				return *HeadData;
			}
		}
	}
	return FHEAD_MODEL_DATA();
}

FHEAD_MODEL_TRANSFORM_DATA AHeadManager::GetHalfHeadModelTransDataByModelID(const FString& ModelID, bool& IsSuccess)
{
	if (HalfHeadTranConfigTable)
	{
		FString ModelIndex;
		if (ModelID == TEXT(""))
		{
			if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GameStatus) &&
				UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == EGameStatus::InWorld)
			{
				//在游戏中，ModelID为空，位置信息根据玩家职业和性别获取不同数据
				int32 Camp = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("camp"));
				int32 Gender = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("gender"));
				int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("profession"));
				ModelIndex = INT_TO_FSTRING(Camp) + INT_TO_FSTRING(Gender) + INT_TO_FSTRING(Profession);
			}
			else
			{
				//不在游戏中，半身像编辑关卡
				ModelIndex = ModelID;
			}
			
		}
		else if (ModelID == TEXT("#"))
		{
			//根据阵营获取不同数据，仙道#1，魔道#2
			int32 Camp = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("camp"));
			switch (Camp)
			{
			case 1:
			{
				ModelIndex = TEXT("#1");
				break;
			}
			case 2:
			{
				ModelIndex = TEXT("#2");
				break;
			}
			default:
				//不在游戏中，半身像编辑关卡，Camp为0
				ModelIndex = TEXT("#1");
				break;
			}
		}
		else
		{
			ModelIndex = ModelID;
		}
		for (auto it : HalfHeadTranConfigTable->GetRowMap())
		{
			FHEAD_MODEL_TRANSFORM_DATA* ModelData = (FHEAD_MODEL_TRANSFORM_DATA*)it.Value;
			if (it.Key == FSTRING_TO_FNAME(ModelIndex))
			{
				IsSuccess = true;
				return *ModelData;
			}
		}
	}
	IsSuccess = false;
	//默认数据
	FHEAD_MODEL_TRANSFORM_DATA DefaultData;
	DefaultData.SocketName = "None";
	DefaultData.Transform = FTransform(FQuat(0.0, 0.0, 0.0, 0.0), FVector(0.0, 0.0, 0.0), FVector(1.0, 1.0, 1.0));
	DefaultData.FOVAngle = 0.0;
	return DefaultData;
}

void AHeadManager::InitHalfHeadTableData()
{
	auto CfgManager = UUECS3GameInstance::Instance->CfgManager;
	HalfHeadConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_DYNAMIC_HEAD_DATA)->GetBaseTable();
	HalfHeadTranConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_DYNAMIC_HEAD_TRAN_DATA)->GetBaseTable();
}

CONTROL_COMPILE_OPTIMIZE_END