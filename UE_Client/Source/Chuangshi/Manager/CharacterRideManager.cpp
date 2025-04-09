// Fill out your copyright notice in the Description page of Project Settings.


#include "CharacterRideManager.h"
//UE4
#include "Kismet/KismetMathLibrary.h"
//CS3数据
#include "GameData/EffectEmitterData.h"
#include "GameData/PetData.h"
#include "Engine/DataTable.h"
#include "GameData/CharacterData.h"
#include "GameData/GameDeFine.h"
//CS3
#include "CfgManager.h"
#include "ResourceManager.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Manager/ParticleManager.h"
#include "Component/Role/RideCarrierComponent.h"
#include "Component/AppearanceComponent.h"
#include "Component/ActorTraceMoveComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Chuangshi.h"
CONTROL_COMPILE_OPTIMIZE_START

UCharacterRideManager::UCharacterRideManager()
{
	CacheRideAssetDatas.Empty();
}

UCharacterRideManager::~UCharacterRideManager()
{

}

UCharacterRideManager* UCharacterRideManager::GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<UCharacterRideManager>();
}

void UCharacterRideManager::LoadRideAsset(FString InPetId)
{
	TArray<FStringAssetReference> LoadAssetPath;

	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* PetConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET);
	APlayerCharacter* MyPlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PetConfigTable))
	{
		const UConfigTable* ModelConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_MODEL);
		const UConfigTable* PartConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PART_MODEL);

		//骑宠资源
		const FPET_DATA* PetData = (FPET_DATA*)PetConfigTable->GetRow(FSTRING_TO_FNAME(InPetId));
		const FMODEL_DATA* PetModelData = ModelConfigTable->GetRow<FMODEL_DATA>(PetData->vehicleModelNum);
		if (!PetModelData)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UCharacterRideManager::[PetId=%d,  vehicleModelNum=%s]"),
				*InPetId, *PetData->vehicleModelNum);
			return;
		}
		if (PetModelData->AnimationPath.ToSoftObjectPath().IsValid())
		{
			LoadAssetPath.Add(PetModelData->AnimationPath.ToSoftObjectPath());
		}

		if (PetModelData->ActionConfigPath.ToSoftObjectPath().IsValid())
		{
			const UDataTable* TableData = CfgManager->GetTableByPath(PetModelData->ActionConfigPath)->GetBaseTable();
			for (auto object : TableData->GetRowMap())
			{
				FACTION_DATA* ActionData = (FACTION_DATA*)object.Value;
				if (ActionData->AnimPath.ToSoftObjectPath().IsValid())
				{
					LoadAssetPath.Add(ActionData->AnimPath.ToSoftObjectPath());
				}
			}
		}
		
		for (FPartItem PratItem : PetModelData->PartArray)
		{
			const FMODEL_PART_DATA* ModelPartData = PartConfigTable->GetRow<FMODEL_PART_DATA>(PratItem.PartID);
			if (!ModelPartData)
			{
				CS3_Warning(TEXT("UCharacterRideManager::LoadRideAsset PartId=%s"), *PratItem.PartID);
				continue;
			}
			if (ModelPartData->ModelPartPath.ToSoftObjectPath().IsValid())
			{
				LoadAssetPath.Add(ModelPartData->ModelPartPath.ToSoftObjectPath());
			}
		}

		//骑士资源
		if (!IsValid(MyPlayerCharacter))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UCharacterRideManager::LoadRideAsset : MyPlayerCharacter!"));
			return;
		}
		FMODEL_DATA *RoleModelData =MyPlayerCharacter->GetCurModelData().Get();
		KBEngine::Entity* MyEntity = MyPlayerCharacter->GetSelfEntity();
		if (MyEntity == nullptr) 
		{
			CS3_Warning(TEXT("-->Null Pointer error:UCharacterRideManager::LoadRideAsset : MyEntity!"));
			return;
		}
		ROLE_PROFESSION_ENUM RoleProfession = (ROLE_PROFESSION_ENUM)((int32)MyEntity->GetDefinedProperty(TEXT("profession")));
		ROLE_GENDER_ENUM RoleGender = (ROLE_GENDER_ENUM)((int32)MyEntity->GetDefinedProperty(TEXT("gender")));
		
		FRIDER_MODEL_ANIM_DATA* RiderModelAnimData = nullptr;
		const UDataTable* RideAnimDataTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_RIDE_ANIM_DATA)->GetBaseTable();
		for (auto it : RideAnimDataTable->GetRowMap())
		{
			FRIDER_MODEL_ANIM_DATA* FindRiderModelAnimData = (FRIDER_MODEL_ANIM_DATA*)it.Value;
			if (FindRiderModelAnimData->RidePosture == PetData->RidePosture &&
				FindRiderModelAnimData->RiderProfession == RoleProfession &&
				FindRiderModelAnimData->RiderGender == RoleGender)
			{
				RiderModelAnimData = FindRiderModelAnimData;
				break;
			}
		}

		if (RiderModelAnimData)
		{
			if (RiderModelAnimData->AnimationPath.ToSoftObjectPath().IsValid())
			{
				LoadAssetPath.Add(RiderModelAnimData->AnimationPath.ToSoftObjectPath());
			}

			if (RiderModelAnimData->ActionConfigPath.ToSoftObjectPath().IsValid())
			{
				const UDataTable* TableData = CfgManager->GetTableByPath(RiderModelAnimData->ActionConfigPath)->GetBaseTable();
				for (auto object : TableData->GetRowMap())
				{
					FACTION_DATA* ActionData = (FACTION_DATA*)object.Value;
					if (ActionData->AnimPath.ToSoftObjectPath().IsValid())
					{
						LoadAssetPath.Add(ActionData->AnimPath.ToSoftObjectPath());
					}
				}
			}
		}

		for (FPartItem PratItem : RoleModelData->PartArray)
		{
			const FMODEL_PART_DATA* ModelPartData = PartConfigTable->GetRow<FMODEL_PART_DATA>(PratItem.PartID);
			if (ModelPartData->ModelPartPath.ToSoftObjectPath().IsValid())
			{
				LoadAssetPath.Add(ModelPartData->ModelPartPath.ToSoftObjectPath());
			}
		}
	}

	//光效资源
	const FEFFECT_EMITTER_DATA *EffectEmitterData = UUECS3GameInstance::Instance->ParticleManager->GetEffectData("100084");
	if (EffectEmitterData)
	{
		LoadAssetPath.Add(EffectEmitterData->ParticleData.ParticleSystemAsset.ToString());
		if (EffectEmitterData->SkeletalMesh.AnimAssetList.Num())
		{
			LoadAssetPath.Add(EffectEmitterData->SkeletalMesh.AnimAssetList[0].ToString());
		}
		LoadAssetPath.Add(EffectEmitterData->SkeletalMesh.SkeletalMeshAsset.ToString());
		LoadAssetPath.Add(EffectEmitterData->StaticMesh.StaticMeshAsset.ToString());
	}

	//开始加载
	UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, LoadAssetPath,
		FStreamableDelegate::CreateLambda([this, LoadAssetPath]()
	{
		for (FStringAssetReference AssetPath : LoadAssetPath)
		{
			CacheRideAsset(AssetPath.ToString(), AssetPath.ResolveObject());
		}
	}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER, MyPlayerCharacter->GetActorLocation());
}

void UCharacterRideManager::CacheRideAsset(FString AssetPath, UObject* AssetObject)
{
	if (!AssetPath.IsEmpty() && AssetObject && !CacheRideAssetDatas.Contains(AssetPath))
	{
		CacheRideAssetDatas.Add(AssetPath, AssetObject);
	}
}

void UCharacterRideManager::ClearCacheData()
{
	TArray<FStringAssetReference> LoadPartArray;
	for (auto data : CacheRideAssetDatas)
	{
		if (!data.Value)
		{
			LoadPartArray.Add((FStringAssetReference)data.Key);
		}
	}
	for (size_t i = 0; i < LoadPartArray.Num(); i++)
	{
		FStringAssetReference KeyString = LoadPartArray[i];
		CacheRideAssetDatas.Remove(KeyString.ToString());
	}

	FVector PlayerPosition = FVector::ZeroVector;
	RESOURCE_LOAD_PRIORITY_TYPE LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_OTHER_ENTITY;
	APlayerCharacter* MyPlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (MyPlayerCharacter)
	{
		PlayerPosition = MyPlayerCharacter->GetActorLocation();
		LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER;
	}
	//开始加载
	UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, LoadPartArray,
		FStreamableDelegate::CreateLambda([this, LoadPartArray]()
	{
		for (int32 i = 0; i < LoadPartArray.Num(); i++)
		{
			FStringAssetReference AssetReference = LoadPartArray[i];
			UObject* NewObject = AssetReference.ResolveObject();
			CacheRideAssetDatas.Add(AssetReference.ToString(), NewObject);
		}
	}), LoadPriority, PlayerPosition);
}

CONTROL_COMPILE_OPTIMIZE_END
