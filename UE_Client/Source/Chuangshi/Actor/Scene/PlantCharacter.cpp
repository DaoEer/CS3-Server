// Fill out your copyright notice in the Description page of Project Settings.


#include "PlantCharacter.h"
#include "GameData/ConstData.h"

CONTROL_COMPILE_OPTIMIZE_START

APlantCharacter::APlantCharacter()
{
	
}



void APlantCharacter::BeginPlay()
{
	Supper::BeginPlay();
	
}

void APlantCharacter::InitPlantData(const LINGTIAN_DATA PlantData_)
{
	seedNum = PlantData_.seedNum;
	growthStage = PlantData_.growthStage;
	growTime = PlantData_.growTime;

	OnBroadCreateModelOver.Unbind();
	CheckGrowthStage();
}

void APlantCharacter::CreateAppearance()
{
	UAppearanceComponent* apperanceCom = GetAppearanceComponent();
	if (IsValid(apperanceCom))
	{
		apperanceCom->CreateAppearance(LHMJ_LING_TIAN_MODEL);
	}
}

const FLING_TIAN_PLANT_DATA* APlantCharacter::GetCurLingTianData()
{
	if (!IsValid(UUECS3GameInstance::Instance))
		return nullptr;
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (!IsValid(CfgManager))
		return nullptr;
	const UConfigTable* LingTianPlantTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_LING_TIAN_PLANT_DATA);
	if (!IsValid(LingTianPlantTable))
		return nullptr;
	TArray< FLING_TIAN_PLANT_DATA*>LingTianPlantData;
	LingTianPlantTable->GetAllRows(LingTianPlantData);
	for (auto i : LingTianPlantData)
	{
		if (i->seedNum == seedNum)return i;
	}
	return nullptr;
}

FGROWTHSTAGEMODELNUMBER APlantCharacter::GetCurSeedGrowData(const FLING_TIAN_PLANT_DATA* curSeedData)
{
	int32 grow = FMath::Min(int32(growthStage), curSeedData->posArr.Num());
	for (auto data : curSeedData->growthStageModelNumber)
	{
		if (data.growthStage == grow)
		{
			return data;
		}
	}
	return FGROWTHSTAGEMODELNUMBER();
}

void APlantCharacter::OnCreateApperanceOver()
{
	
}

void APlantCharacter::CheckGrowthStage()
{
	FDateTime beginGrow_ = UGolbalBPFunctionLibrary::FromServerTimeToClientTime(growTime);
	FDateTime now_ = FDateTime::Now();
	const FLING_TIAN_PLANT_DATA* CurLTData = GetCurLingTianData();
	if (CurLTData)
	{
		if (growthStage >= CurLTData->growthStageModelNumber.Num())
		{
			BeginCreateMesh();
			return;
		}
		int32 time = CurLTData->growthStageModelNumber[growthStage].growthTime * 60;
		while (now_ - beginGrow_ >= time * ETimespan::TicksPerSecond)
		{
			growTime += time;
			beginGrow_ += time * ETimespan::TicksPerSecond;
			growthStage += 1;
			if (growthStage >= CurLTData->growthStageModelNumber.Num())
			{
				BeginCreateMesh();
				return;
			}
			time = CurLTData->growthStageModelNumber[growthStage].growthTime * 60;

		}

		BeginCreateMesh();
		float delayTime = time - (now_ - beginGrow_).GetSeconds();
		UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(DelayGrowHandle, this, &APlantCharacter::CheckGrowthStage, delayTime, false);
	}
}

void APlantCharacter::AddGrowthStage()
{

}

void APlantCharacter::BeginCreateMesh()
{
	const FLING_TIAN_PLANT_DATA* curSeedData = GetCurLingTianData();
	if (!curSeedData)
	{
		for (auto meshCom : CropMeshComponents)
		{
			meshCom->SetStaticMesh(nullptr);
		}
		return;
	}
	CheckMeshComponent(curSeedData->posArr);

	CurCreateMeshIndex = -1;
	UStaticMeshComponent* mComponent = Cast<UStaticMeshComponent>(STMesh_DefaultStatic);
	if (IsValid(mComponent))
	{
		TempMesh = mComponent->GetStaticMesh();
	}

	TWeakObjectPtr<APlantCharacter> DelayThis(this);
	OnBroadCreateModelOver.BindLambda([DelayThis, curSeedData]()
	{
		if (DelayThis.IsValid())
		{
			auto thisPtr = DelayThis.Get();
			thisPtr->CurCreateMeshIndex += 1;

			UStaticMeshComponent* mComponent = Cast<UStaticMeshComponent>(thisPtr->STMesh_DefaultStatic);
			if (!IsValid(mComponent))return;
			UStaticMesh* sMesh = mComponent->GetStaticMesh();
			mComponent->SetStaticMesh(nullptr);

			for (auto meshCom : thisPtr->CropMeshComponents)
			{
				meshCom->SetStaticMesh(sMesh);
			}
			thisPtr->OnBroadCreateModelOver.Unbind();
			mComponent->SetStaticMesh(thisPtr->TempMesh);
			thisPtr->TempMesh = nullptr;
			/*
			if (thisPtr->CropMeshComponents.Num() - 1 >= thisPtr->CurCreateMeshIndex)
			{
				thisPtr->CropMeshComponents[thisPtr->CurCreateMeshIndex]->SetStaticMesh(sMesh);
			}

			if (curSeedData->posArr.Num() - 1 <= thisPtr->CurCreateMeshIndex)
			{
				thisPtr->OnBroadCreateModelOver.Unbind();
				mComponent->SetStaticMesh(thisPtr->TempMesh);
				thisPtr->TempMesh = nullptr;
				return;
			}
			

			thisPtr->GetAppearanceComponent()->CreateAppearance(thisPtr->GetCurSeedGrowData(curSeedData).modelNumber);
			return;
			*/
		}
	});
	GetAppearanceComponent()->CreateAppearance(GetCurSeedGrowData(curSeedData).modelNumber);
}

void APlantCharacter::CheckMeshComponent(const TArray<FVector>& PosList)
{
	int32 cropNum = PosList.Num();
	int32 curNum = CropMeshComponents.Num();


	if (cropNum > curNum)
	{
		for (auto i = cropNum - curNum; i > 0; i--)
		{
			auto staticComponent = NewObject<UStaticMeshComponent>(this);
			staticComponent->RegisterComponent();
			staticComponent->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
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
			CropMeshComponents[index]->SetRelativeScale3D(FVector(1.8, 1.8, 1.8));
		}
	}
}

CONTROL_COMPILE_OPTIMIZE_END