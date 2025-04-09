// Fill out your copyright notice in the Description page of Project Settings.

#include "SpellBoxLingTianInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/LingTianPlantData.h"
#include "Manager/CfgManager.h"
#include "CS3Base/UIManager.h"
#include "Manager/EventManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "../Role/RoleLunHuiMiJinInterface.h"
#include "GameData/Item/ToolCost.h"
#include "Manager/EventManager.h"
#include "Component/AppearanceComponent.h"
#include "Manager/Delegate/SpaceContentDelegateObject.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(USpellBoxLingTianInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowLingTianPlantUI, &USpellBoxLingTianInterface::ShowLingTianPlantUI, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowGrowUpMsgUI, &USpellBoxLingTianInterface::ShowGrowUpMsgUI, const int32&, const FString&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(USpellBoxLingTianInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(seedNum, &USpellBoxLingTianInterface::Set_clientSeedNum, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(growthStage, &USpellBoxLingTianInterface::Set_clientGrowthStage, int32)
CS3_END_INTERFACE_PROPERTY_MAP()

CONTROL_COMPILE_OPTIMIZE_START

USpellBoxLingTianInterface::USpellBoxLingTianInterface()
{
	ModelIsCreate = false;
	InitLingTianSeedData();
}

USpellBoxLingTianInterface::~USpellBoxLingTianInterface()
{
}

void USpellBoxLingTianInterface::ShowLingTianPlantUI(const int32& entityID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("Field"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->ShowLingTianPlantUIEvent.Broadcast(EntityID);
	}
}

void USpellBoxLingTianInterface::ShowGrowUpMsgUI(const int32& entityID, const FString& endTimeStr)
{
	endStrTime = endTimeStr;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("FieldGrowUpMessage"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->ShowGrowUpMsgUIEvent.Broadcast(EntityID);
	}
}

void USpellBoxLingTianInterface::RPC_onClickPlant(int32 ItemID)
{
	KBEngine::FVariantArray Args;
	Args.Add(ItemID);
	if (this->GetEntity())
	{
		this->GetEntity()->CellCall(TEXT("onClickPlant"), Args);
	}
}

TArray<int32> USpellBoxLingTianInterface::GetSeedIDList()
{
	TArray<int32> IDList;
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->CfgManager))
	{
		return IDList;
	}
	int32 BuildLevel = 1;
	URoleLunHuiMiJinInterface* LHMJInterface = Cast<URoleLunHuiMiJinInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleLunHuiMiJinInterface")));
	if (IsValid(LHMJInterface))
	{
		BuildLevel = LHMJInterface->GetBuildLevel(LHMJ_BUILD_TYPE::LHMJ_BUIILD_LING_TIAN);
	}
	const UDataTable* TableData = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ITEMDATA)->GetBaseTable();
	for (auto It = seedData.CreateConstIterator(); It; ++It)
	{
		FLING_TIAN_PLANT_DATA* data = It.Value();
		if (data->needLevel <= BuildLevel)
		{
			IDList.Add(data->seedItemID);
		}
	}
	return IDList;
}

void USpellBoxLingTianInterface::Set_clientSeedNum(const int32& newVal, const int32& oldVal)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		seedNum = newVal;
		if (!UUECS3GameInstance::Instance->CustomTimerManager->IsTimerActive(DelayCreateHandle))
		{
			//TWeakObjectPtr<USpellBoxLingTianInterface> DelayThis(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayCreateHandle, this, &USpellBoxLingTianInterface::BeginCreateMesh, 0.2f, false);
		}
	}
}

void USpellBoxLingTianInterface::Set_clientGrowthStage(const int32& newVal, const int32& oldVal)
{
	
	if (IsValid(UUECS3GameInstance::Instance))
	{
		growthStage = newVal;
		if (!UUECS3GameInstance::Instance->CustomTimerManager->IsTimerActive(DelayCreateHandle))
		{
			//TWeakObjectPtr<USpellBoxLingTianInterface> DelayThis(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayCreateHandle, this, &USpellBoxLingTianInterface::BeginCreateMesh, 0.2f, false);
		}
	}
}

void USpellBoxLingTianInterface::GetLingTianSeedData(FString &seedIcon, FString &seedName)
{
	if (seedData.Contains(seedNum))
	{
		FLING_TIAN_PLANT_DATA* tempData = seedData[seedNum];
		seedIcon = tempData->seedIcon;
		seedName = tempData->seedName;
	}
}

FGROWTHSTAGEMODELNUMBER USpellBoxLingTianInterface::GetCurSeedGrowData()
{
	FLING_TIAN_PLANT_DATA* curSeedData = seedData[seedNum];
	int32 grow = FMath::Min(growthStage, curSeedData->posArr.Num());
	for (auto data : curSeedData->growthStageModelNumber)
	{
		if (data.growthStage == grow)
		{
			return data;
		}
	}
	return FGROWTHSTAGEMODELNUMBER();
}

void USpellBoxLingTianInterface::OnCreateModelFinish()
{
	ModelIsCreate = true;
}

void USpellBoxLingTianInterface::InitLingTianSeedData()
{
	if (!IsValid(UUECS3GameInstance::Instance))
		return;
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (!IsValid(CfgManager))
		return;
	const UConfigTable* LingTianPlantTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_LING_TIAN_PLANT_DATA);
	if (!IsValid(LingTianPlantTable))
		return;
	TArray< FLING_TIAN_PLANT_DATA*>LingTianPlantData;
	LingTianPlantTable->GetAllRows(LingTianPlantData);
	for (auto i : LingTianPlantData)
	{
		seedData.Add(i->seedNum, i);
	}
}

void USpellBoxLingTianInterface::BeginCreateMesh()
{
	if (seedNum == 0)				// 被收获了
	{
		for (auto meshCom : CropMeshComponents)
		{
			meshCom->SetStaticMesh(nullptr);
		}
		return;
	}
	AServerCharacter* ltCharacter = Cast<AServerCharacter>(GetActor());
	if (!IsValid(ltCharacter))return;
	if (!ModelIsCreate)					// 农作物的创建 前提是 ，灵田的模型已经创建完成
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayCreateHandle, this, &USpellBoxLingTianInterface::BeginCreateMesh, 1.2f, false);
		return;
	}

	if (!seedData.Contains(seedNum))return;
	FLING_TIAN_PLANT_DATA* curSeedData = seedData[seedNum];
	CheckMeshComponent(curSeedData->posArr);
	

	CurCreateMeshIndex = -1;
	UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(ltCharacter->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
	TempMesh = DefaultStaticMeshCpt->GetStaticMesh();

	TWeakObjectPtr<USpellBoxLingTianInterface> DelayThis(this);
	TWeakObjectPtr<AServerCharacter> DelayCharacter(ltCharacter);
	ltCharacter->OnBroadCreateModelOver.BindLambda([DelayThis, DelayCharacter]()
	{
		if (DelayThis.IsValid() && DelayCharacter.IsValid())
		{
			auto thisPtr = DelayThis.Get();
			auto characterPtr = DelayCharacter.Get();
			if (!thisPtr->seedData.Contains(thisPtr->seedNum))return;
			thisPtr->CurCreateMeshIndex += 1;
			FLING_TIAN_PLANT_DATA* curSeedData = thisPtr->seedData[thisPtr->seedNum];

			UStaticMeshComponent* mComponent = Cast<UStaticMeshComponent>(characterPtr->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
			if (IsValid(mComponent))
			{
				UStaticMesh* sMesh = mComponent->GetStaticMesh();
				mComponent->SetStaticMesh(thisPtr->TempMesh);
				thisPtr->TempMesh = nullptr;

				for (auto meshCom : thisPtr->CropMeshComponents)
				{
					meshCom->SetStaticMesh(sMesh);
				}
				characterPtr->OnBroadCreateModelOver.Unbind();	

				/*
				if (thisPtr->CropMeshComponents.Num() - 1 >= thisPtr->CurCreateMeshIndex)
				{
					thisPtr->CropMeshComponents[thisPtr->CurCreateMeshIndex]->SetStaticMesh(sMesh);
				}
			}
			if (curSeedData->posArr.Num() - 1 <= thisPtr->CurCreateMeshIndex)
			{
				characterPtr->OnBroadCreateModelOver.Unbind();
				UStaticMeshComponent* mComponent = Cast<UStaticMeshComponent>(characterPtr->STMesh_DefaultStatic);
				if (IsValid(mComponent))
				{
					mComponent->SetStaticMesh(thisPtr->TempMesh);
					thisPtr->TempMesh = nullptr;
				}
				return;
			}


			thisPtr->CreateApperaance(thisPtr->GetCurSeedGrowData().modelNumber);
			return;*/

			}
		}
	});
	CreateApperaance(GetCurSeedGrowData().modelNumber);
}

void USpellBoxLingTianInterface::CheckMeshComponent(const TArray<FVector>& PosList)
{
	int32 cropNum = PosList.Num();
	int32 curNum = CropMeshComponents.Num();
	
	if (cropNum > curNum )
	{
		AServerCharacter* Owner = Cast<AServerCharacter>(GetActor());
		if (!IsValid(Owner))return;
		for (auto i = cropNum - curNum  ; i > 0; i--)
		{
			auto staticComponent = NewObject<UStaticMeshComponent>(Owner);
			staticComponent->RegisterComponent();
			staticComponent->AttachToComponent(Owner->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
			CropMeshComponents.Add(staticComponent);
		}
	}
	for (auto It = CropMeshComponents.CreateConstIterator(); It; ++It)
	{
		int32 index = It.GetIndex();
		auto mesh_ = CropMeshComponents[index]->GetStaticMesh();
		CropMeshComponents[index]->SetStaticMesh(nullptr);
		if (cropNum > index)
		{
			CropMeshComponents[index]->SetRelativeLocation(PosList[index]);
		}
	}
}

void USpellBoxLingTianInterface::CreateApperaance(const FString & ModelID)
{
	AServerCharacter* ltCharacter = Cast<AServerCharacter>(GetActor());
	if (!IsValid(ltCharacter))return;
	
	ltCharacter->GetAppearanceComponent()->CreateAppearance(ModelID);

}

CONTROL_COMPILE_OPTIMIZE_END