// Fill out your copyright notice in the Description page of Project Settings.


#include "Component/AppearanceComponent.h"
//c++标准库
#include "time.h"
//UE4
#include "Materials/MaterialInstanceDynamic.h"
#include "Engine/StreamableManager.h"
#include "Engine/SkeletalMesh.h"
#include "Components/MeshComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/BlendSpaceBase.h"
#include "UnrealString.h"
//CS3数据
#include "GameData/RoleCreateUIData.h"
#include "GameData/CharacterData.h"
#include "GameData/GameDefault.h"
#include "GameData/AppearanceStyle/BattlefieldAppearanceStyle.h"
#include "Util/CS3Debug.h"
#include "GameData/GameDeFine.h"
//CS3
#include "Util/ConvertUtil.h"
#include "Entity/Alias.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Interface/StateInterface.h"
#include "Components/StaticMeshComponent.h"
#include "Interface/GameObjectInterface.h"
#include "Actor/Pet/RiderCharacter.h"
#include "Actor/GameCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "Manager/ParticleManager.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Manager/VisibleManager.h"
#include "Manager/ResourceManager.h"
#include "Manager/CharacterRideManager.h"
#include "Manager/CfgManager.h"
#include "GameData/ModelPartData.h"
#include "Util/CS3DebugType.h"
#include "Manager/ActionManager.h"
#include "Entity/SpellBox/SpellBox.h"
#include "Actor/Player/ProxyCharacter.h"

DECLARE_CYCLE_STAT(TEXT("CreateAppearance"), STAT_CreateAppearance, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("CreateModel"), STAT_CreateModel, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("LoadAssetPath"), STAT_LoadAssetPath, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("CreateModelOver"), STAT_CreateModelOver, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("ChangeAnimAction"), STAT_ChangeAnimAction, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("FillActionAssertToLoad"), STAT_FillActionAssertToLoad, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("FillModelAssertToLoad"), STAT_FillModelAssertToLoad, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("RemoveAllParts"), STAT_RemoveAllParts, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("ApplayPartsModel"), STAT_ApplayPartsModel, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("ApplayModelByPartsMap"), STAT_ApplayModelByPartsMap, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("SetActorPart"), STAT_SetActorPart, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("AddActorPart"), STAT_AddActorPart, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("CopyModelFrom"), STAT_CopyModelFrom, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("CopyModelFromNormal"), STAT_CopyModelFromNormal, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("SetMaterialColor"), STAT_SetMaterialColor, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("UpdateWeaponLocation"), STAT_UpdateWeaponLocation, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("PlayerBornEffect"), STAT_PlayerBornEffect, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("CreateStaticMeshComponent"), STAT_CreateStaticMeshComponent, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("CreateSkeletalMeshComponent"), STAT_CreateSkeletalMeshComponent, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("SetMeshComponent"), STAT_SetMeshComponent, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("SetActionAnimAsset"), STAT_SetActionAnimAsset, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("CreateRideAppearance"), STAT_CreateRideAppearance, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("CreateRoleModel"), STAT_CreateRoleModel, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("CreateRiderAndPetForRideModel"), STAT_CreateRiderAndPetForRideModel, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("ChangePart"), STAT_ChangePart, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("OnChangeActorPartLoadCompleted"), STAT_OnChangeActorPartLoadCompleted, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("CreatePartMapByServer"), STAT_CreatePartMapByServer, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("GetPartDataMapByModelNumber"), STAT_GetPartDataMapByModelNumber, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("GetPartDataMapByModelInfo"), STAT_GetPartDataMapByModelInfo, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("GetRideModelAnimDataFromCfg"), STAT_GetRideModelAnimDataFromCfg, STATGROUP_UAppearanceComponent);
DECLARE_CYCLE_STAT(TEXT("GetRoleModelData"), STAT_GetRoleModelData, STATGROUP_UAppearanceComponent);

CONTROL_COMPILE_OPTIMIZE_START
UAppearanceComponent::UAppearanceComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
	if (IsValid(UUECS3GameInstance::Instance))
	{
		DefaultNumber = UUECS3GameInstance::Instance->GameDefault->DefaultModelNumber_M;
	}
	isInModelCreating = false;
}

void UAppearanceComponent::CreateModelOver()
{
	SCOPE_CYCLE_COUNTER(STAT_CreateModelOver);
	isInModelCreating = false;
	AGameCharacter* GameCharacter = Cast<AGameCharacter>(GetOwner());
	if (IsValid(GameCharacter))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.CreateModelOver(name=%s, bHasCacheModelNumber=%d, CacheModelNumber=%s)"), 
			*GameCharacter->GetName(), bHasCacheModelNumber ? 1 : 0, *CachaeCreateAppData.RoleModelId);

		GameCharacter->OnCreateModelOver();
		//刷新状态光效
		UpdateStateEffect();
		if (bHasCacheModelNumber)
		{
			bHasCacheModelNumber = false;
			//有缓存的模型，继续创建
			CreateAppearance(CachaeCreateAppData.RoleModelId);
		}
	}
}

void UAppearanceComponent::OnChangePartOver()
{
	AGameCharacter* GameCharacter = Cast<AGameCharacter>(GetOwner());
	if (IsValid(GameCharacter))
	{
		GameCharacter->OnChangePartOver();
	}
}

void UAppearanceComponent::CreateAppearance(FString InModelNumber)
{	
	SCOPE_CYCLE_COUNTER(STAT_CreateAppearance);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.CreateAppearance(ModelId=%s, isInModelCreating=%d)"),*InModelNumber, isInModelCreating?1:0);

	if (isInModelCreating)
	{
		bHasCacheModelNumber = true; //正在创建中，但是有新的模型需要创建
		CachaeCreateAppData.RoleModelId = InModelNumber;
		CachaeCreateAppData.RidePetModelId.Empty();				// 因为缓存没有clear，所以在这里处理。否则有可能会有骑乘的流程
		return;
	}

	isInModelCreating = true;
	CurCreateAppData.RoleModelId = InModelNumber;
	TMap<MODEL_PART_TYPE, FString> PartDataMap;
	CreatePartMapByServer(PartDataMap);
	if (PartDataMap.Num() == 0)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.PartDataMap is IsEmpty![ModelNumber=%s]"), *InModelNumber);
		return;
	}

	if (!CreateModel(CurCreateAppData.RoleModelId, PartDataMap))
	{
		isInModelCreating = false;
	}
}
bool UAppearanceComponent::CreateModel(FString InModelNumber, TMap<MODEL_PART_TYPE, FString> &InPartMap )
{
	SCOPE_CYCLE_COUNTER(STAT_CreateModel);
	TSharedPtr<FMODEL_DATA>  ModelData = MakeShareable(new FMODEL_DATA(*GetModelDataFromCfg(InModelNumber)));
	SetModelData(ModelData);
	
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.CreateAppearance(ModelId=%s, isInModelCreating=%d)"), *InModelNumber, isInModelCreating ? 1 : 0);
	TWeakObjectPtr<UAppearanceComponent> DelayThisPtr(this);
	LoadModelTotalAssetPath([DelayThisPtr, InPartMap]()
	{
		if (!DelayThisPtr.IsValid())
		{
			CS3_Warning(TEXT("AppCmpt.Error::CreateModel:LoadAssetPathCallBack *this is error!"));
			return;
		}
		UAppearanceComponent* ThisPtr = DelayThisPtr.Get();
		ThisPtr->ApplayModelByPartsMap(InPartMap);
	});
	return true;
}

void UAppearanceComponent::LoadModelTotalAssetPath(TFunction<void()>&& Callback)
{
	SCOPE_CYCLE_COUNTER(STAT_LoadAssetPath);
	TArray<FStringAssetReference> LoadArray;
	if (CurModelData->ActionConfigPath.ToSoftObjectPath().IsValid())
	{
		LoadArray.Push(CurModelData->ActionConfigPath.ToSoftObjectPath());
	}

	RESOURCE_LOAD_PRIORITY_TYPE LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_OTHER_ENTITY;
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (IsValid(PlayerCharacter))
	{
		ARiderCharacter* RiderCharacter = PlayerCharacter->GetRiderCharacter();
		if (IsValid(RiderCharacter) && RiderCharacter->GetCurModelData().IsValid()
			&& RiderCharacter->GetCurModelData()->ActionConfigPath.ToSoftObjectPath().IsValid())
		{
			LoadArray.Push(RiderCharacter->GetCurModelData()->ActionConfigPath.ToSoftObjectPath());
		}
		LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER;
	}

	if (LoadArray.Num() > 0)
	{
		FVector OwnerPosition = FVector::ZeroVector;
		AActor* OwnerActor = GetOwner();
		if (IsValid(OwnerActor))
		{
			OwnerPosition = OwnerActor->GetActorLocation();
			UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(OwnerActor, LoadArray,
				FStreamableDelegate::CreateLambda([Callback]()
			{
				Callback();
			}), LoadPriority, OwnerPosition);
		}
	}
	else
	{
		Callback();
	}
}

void UAppearanceComponent::CreateAppearanceByModelInfo(const FString& InModelNumber, const FAModelInfo& AModelInfo)
{
	CurCreateAppData.RoleModelId = InModelNumber;
	TMap<MODEL_PART_TYPE, FString> NewPartMap = GetPartDataMapByModelInfo(AModelInfo);
	CreateModel(InModelNumber, NewPartMap);
}

void UAppearanceComponent::FillActionAssertToLoad(TArray<FStringAssetReference> &OutLoadArray, TMap<ACTION_POSE_ENUM, FACTION_DATA> &OutTemActionDatas)
{
	SCOPE_CYCLE_COUNTER(STAT_FillActionAssertToLoad);
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (CurModelData->AnimationPath.ToSoftObjectPath().IsValid())
	{
		//动画蓝图
		OutLoadArray.Add(CurModelData->AnimationPath.ToSoftObjectPath());
		//动画蓝图中的动作对象
		if (CurModelData->ActionConfigPath.ToSoftObjectPath().IsValid())
		{
			const UDataTable* TableData = CfgManager->GetTableByPath(CurModelData->ActionConfigPath)->GetBaseTable();
			for (auto object : TableData->GetRowMap())
			{
				FACTION_DATA* ActionData = (FACTION_DATA*)object.Value;
				ActionData->Id = object.Key;
				OutTemActionDatas.Add(ActionData->ActionPose, *ActionData);
				//Owner->ActionDatas.Add(ActionData->ActionPose, *ActionData);
				if (ActionData->AnimPath.ToSoftObjectPath().IsValid())
				{
					OutLoadArray.Add(ActionData->AnimPath.ToSoftObjectPath());
				}
			}
		}
	}
}

void UAppearanceComponent::FillModelAssertToLoad(TArray<FStringAssetReference> &AllLoadArray, 
	TMap<MODEL_PART_TYPE, FMODEL_PART_DATA> &PartArray, const TMap<MODEL_PART_TYPE, FString>& PartMap)
{
	SCOPE_CYCLE_COUNTER(STAT_FillModelAssertToLoad);
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	for (TPair<MODEL_PART_TYPE, FString> Part : PartMap)
	{
		if (!Part.Value.IsEmpty())
		{
			const FMODEL_PART_DATA* pPartData = GetPartDataFromCfg(Part.Value);
			if (pPartData)
			{
				AllLoadArray.Add(pPartData->ModelPartPath.ToSoftObjectPath());
				PartArray.Add(Part.Key, *pPartData);

				if (pPartData->PartAnimBpPath.ToSoftObjectPath().IsValid())
				{
					AllLoadArray.Add(pPartData->PartAnimBpPath.ToSoftObjectPath());
				}
			}
		}
	}
}

void UAppearanceComponent::RemoveAllParts()
{
	SCOPE_CYCLE_COUNTER(STAT_RemoveAllParts);
	for (auto RemovePart : CurPartMap)
	{
		if (!RemovePart.Value.IsEmpty())
		{
			CancelActorPart(RemovePart.Key);
		}
	}
}

void UAppearanceComponent::ApplayPartsModel(const TMap<MODEL_PART_TYPE, FMODEL_PART_DATA> &InPartDataArray)
{
	SCOPE_CYCLE_COUNTER(STAT_ApplayPartsModel);
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	int32 Length = (int32)MODEL_PART_TYPE::MODEL_PART_NUM;
	for (size_t i = 0; i < Length; i++)
	{
		MODEL_PART_TYPE PartType = (MODEL_PART_TYPE)i;
		//当没有这个部件时
		if (!InPartDataArray.Contains(PartType))
		{
			CancelActorPart((MODEL_PART_TYPE)PartType);
			continue;
		}
		
		//当部件与当前的无效
		FMODEL_PART_DATA ModelPartData = *InPartDataArray.Find(PartType);
		if (!CheckIsVaildPart(PartType, ModelPartData.RowName.ToString()))
		{
			CancelActorPart(PartType);
			continue;
		}
		//当部件资源无效
		UObject* PartMesh = ModelPartData.ModelPartPath.Get();
		if (!PartMesh)
		{
			CancelActorPart(PartType);
			continue;
		}

		AddActorPart(PartType, ModelPartData);
		if (Owner->IsControlled() || IsValid(Cast<ARiderCharacter>(Owner)))
		{
			UUECS3GameInstance::Instance->CharacterRideManager->CacheRideAsset(ModelPartData.ModelPartPath.ToString(), PartMesh);
		}
	}
}

void UAppearanceComponent::ApplayModelByPartsMap(TMap<MODEL_PART_TYPE, FString> InNewPartMap)
{
	SCOPE_CYCLE_COUNTER(STAT_ApplayModelByPartsMap);
	if (!(IsValid(GetOwner())))return;

	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	TArray<FStringAssetReference> AllLoadArray;    //所有需要加载的资源数组
	TMap<MODEL_PART_TYPE, FMODEL_PART_DATA> PartValidData;	 //通过NewPartMap过滤出的有效的部位数据
	FillModelAssertToLoad(AllLoadArray, PartValidData, InNewPartMap);	//填充模型数据，模型部位列表

	if (AllLoadArray.Num() == 0)
	{
		isInModelCreating = false;
		return;
	}

	TMap<ACTION_POSE_ENUM, FACTION_DATA> TemActionDatas;
	FillActionAssertToLoad(AllLoadArray, TemActionDatas);	//填充动作数据

	//加载所需资源(此为值写-1，是因为UGolbalBPFunctionLibrary::GetInterfaceByName逻辑里，大家把0当作了玩家的默认写法)
	int32 EntityId = Owner->GetSelfEntity() ? Owner->GetSelfEntity()->ID() : -1;
	FString ModelId = CurModelData.Get() ? CurModelData->RowName.ToString() : "Null";
	//检查资源文件是否存在
	//UUECS3GameInstance::Instance->ResourceManager->CheckMultipleAssetFileIsExist(LoadPartArray, EntityId, ModelId);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.StartLoadArray(Name=%s, ModelId=%s)"), *Owner->GetName(), *ModelId);

	CurPartMap = InNewPartMap;

	clock_t AssetTime = clock();
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.StartLoadTime [Name=%s, AssetTime=%d]"), *Owner->GetName(), AssetTime);

	RESOURCE_LOAD_PRIORITY_TYPE LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_OTHER_ENTITY;
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	bool bManageActiveHandle = false;
	if (PlayerCharacter)
	{
		LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER;
		if (PlayerCharacter->ActorIsPlayer())
		{
			bManageActiveHandle = true;
		}
	}

	FString LoadedLevel = GetWorld()->PersistentLevel->GetName();
	
	//开始加载
	TWeakObjectPtr<UAppearanceComponent> DelayThisPtr(this);
	UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(Owner, AllLoadArray,
		FStreamableDelegate::CreateLambda([DelayThisPtr, PartValidData, EntityId, ModelId, TemActionDatas, AssetTime, LoadedLevel]()
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("[AppCmpt.Load Assets Successful (EntityId=%d, ModelId=%s)"), EntityId, *ModelId);
		
		if (!DelayThisPtr.IsValid())
		{
			CS3_Warning(TEXT("AppCmpt.Error::ApplayModelByPartsMap:RequestAsyncLoad *this is error!"));
			return;
		}

		
		UAppearanceComponent* ThisPtr = DelayThisPtr.Get();
		AGameCharacter* Owner = Cast<AGameCharacter>(ThisPtr->GetOwner());

		///需增加这种判断，与判断IsValid(Owner)共同存在，因测试发现这个测进，但IsValid不会进入，再使用Owner就崩溃了
		if (!IsValid(Owner))
		{
			CS3_Warning(TEXT("AppCmpt.Error::ApplayModelByPartsMap:RequestAsyncLoad *Owner is error!"));
			return;
		}

		clock_t AssetTime1 = clock();
		ThisPtr->isInModelCreating = false;
		//判断加载完成后的entity还是不是加载前的entity
		if (EntityId > 0)
		{
			int32 CurEntityId = Owner->GetSelfEntity() ? Owner->GetSelfEntity()->ID() : 0;
			if (EntityId != CurEntityId)
			{
				CS3_Warning(TEXT("AppCmpt.Error::ApplayModelByPartsMap:RequestAsyncLoad[OldEntityId=%d,CurEntityId=%d]"), EntityId, CurEntityId);
				return;
			}
		}
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.EndLoadArray(Name=%s, ModelId=%s)"), *Owner->GetName(), *ModelId);
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.EndLoadTime [Name=%s, LeftTime=%d]"), *Owner->GetName(), (AssetTime1 - AssetTime));

		FString CurrentLevel = ThisPtr->GetWorld()->PersistentLevel->GetName();
		//当前地图和加载的时候的地图不是同一个，owner再去设置一些东西也没有意义了
		if (!CurrentLevel.Equals(LoadedLevel))
		{
			CS3_Warning(TEXT("AppCmpt.Error::ApplayModelByPartsMap:RequestAsyncLoad[CurrentLevel=%s, LoadLevel=%s]"), *CurrentLevel, *LoadedLevel);
			return;
		}

		//设置玩家的初始动作 
		Owner->SetInitAction();

		//bool IsSpellBox = Owner->GetClass()->IsChildOf(SpellBox::stat);

		// 动画模式(ps:游戏中角色模型是动画蓝图模型,剧情中模型是动画资源模式)
		if (IsValid(Owner->GetMesh()) && Owner->GetMesh()->GetAnimationMode() == EAnimationMode::AnimationBlueprint)
		{
			if (UClass* anim = ThisPtr->CurModelData->AnimationPath.Get())
			{
				Owner->ActionDatas = TemActionDatas;
				ThisPtr->UpdateActionAnimAssetList();
				Owner->GetMesh()->SetAnimInstanceClass(anim);
			}
			else
			{
				Owner->ActionDatas.Empty();
				Owner->GetMesh()->SetAnimInstanceClass(nullptr);
			}
			ThisPtr->PlayerBornEffect();
		}// TODO: 剧情中模型相关操作
		else
		{
			CS3_Warning(TEXT("AppCmpt.Error::ApplayModelByPartsMap:RequestAsyncLoad AnimationAsset Model[GameCharacter=%s]"), *Owner->GetName());
		}

		//资源加载完毕更换部件
		ThisPtr->ApplayPartsModel(PartValidData);

		//设置了主mesh后才能取到animinstance
		Owner->SetBaseAnimInstance(Cast<UBaseAnimInstance>(Owner->GetMesh()->GetAnimInstance()));
		
		if (Owner->IsControlled() || IsValid(Cast<ARiderCharacter>(Owner)))
		{
			UUECS3GameInstance::Instance->CharacterRideManager->CacheRideAsset(ThisPtr->CurModelData->AnimationPath.ToString(), Owner->GetBaseAnimInstance());
		}

		UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Owner);

		//资源加载完毕让旧的模型编号等于新的模型编号
		UGameObjectInterface* GameInterface = Cast<UGameObjectInterface>(
			UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("GameObjectInterface"), EntityId));
		if (GameInterface)
		{
			GameInterface->old_modelNumber = GameInterface->new_modelNumber;
			if (!GameInterface->bScaleTweenProcess)
			{
				GameInterface->OnRep_modelScale();
			}
		}

		// 禁用没用到的部件,提升性能 CST-9883
		{
			int32 length = (int32)MODEL_PART_TYPE::MODEL_PART_NUM;
			for (int32 i = 0; i < length; i++)
			{
				MODEL_PART_TYPE PartTypeKey = (MODEL_PART_TYPE)i;

				if (PartTypeKey == MODEL_PART_TYPE::MODEL_PART_BODYS || PartValidData.Contains(PartTypeKey)) continue; //排除主骨骼和用到的部件

				if (UMeshComponent* NotValidMeshComponent = Owner->GetPartMeshComponent(PartTypeKey))
				{
					NotValidMeshComponent->SetVisibility(false, true);
					NotValidMeshComponent->SetComponentTickEnabled(false);
					//NotValidMeshComponent->DetachFromComponent(FDetachmentTransformRules::KeepRelativeTransform);
				}
			}
		}
		
		ThisPtr->CreateModelOver();
	}), LoadPriority, GetOwner()->GetActorLocation(), bManageActiveHandle);

}

bool UAppearanceComponent::CheckIsVaildPart(MODEL_PART_TYPE PartType, const FString& PartID)
{
	return CurPartMap.Contains(PartType) && CurPartMap[PartType] == PartID;
}

void UAppearanceComponent::SetActorPart(MODEL_PART_TYPE partPos, UObject* partMesh)
{
	SCOPE_CYCLE_COUNTER(STAT_SetActorPart);

	AGameCharacter* GameCharacter = Cast<AGameCharacter>(GetOwner());
	UMeshComponent* MeshComponent = GameCharacter->GetPartMeshComponent(partPos);
	if (!IsValid(MeshComponent))
	{
		//CS3_Warning(TEXT("AppCmpt.Error::SetActorPart MeshComponent is not valid!"));
		return;
	}

	if (partPos == MODEL_PART_TYPE::MODEL_PART_BODYS)
	{	
		USkeletalMeshComponent* SkeletalMeshCom = Cast<USkeletalMeshComponent>(MeshComponent);
		if (CurModelData && CurModelData->IsRenderCustomDepth)
		{
			SkeletalMeshCom->SetRenderCustomDepth(CurModelData->IsRenderCustomDepth);
		}
		SkeletalMeshCom->SetSkeletalMesh(nullptr);//注：同模型变身，也需播放初始动作
		SkeletalMeshCom->SetSkeletalMesh(Cast<USkeletalMesh>(partMesh));

		//恢复材质CST-1717,受击时变身后异常，受击材质混合到了变身后表现了
		USkeletalMesh* SkeletalMesh = Cast<USkeletalMesh>(partMesh);
		if (IsValid(SkeletalMesh))
		{
			TArray<FSkeletalMaterial> Materials = SkeletalMesh->Materials;
			for (int i = 0; i < Materials.Num(); i++)
			{
				MeshComponent->SetMaterial(i, Materials[i].MaterialInterface);
			}

			GameCharacter->setIsHitMaterialCreated(false);
		}
	}
	else if (partPos == MODEL_PART_TYPE::MODEL_PART_LWEAPON) 
	{
		FName SockeName = GameCharacter->GetWeaponSockName(true);
		SetMeshComponent(MeshComponent, TEXT("LHweapon"), SockeName, partMesh);
	}
	else if (partPos == MODEL_PART_TYPE::MODEL_PART_RWEAPON)
	{
		FName SockeName = GameCharacter->GetWeaponSockName(false);
		SetMeshComponent(MeshComponent, TEXT("RHweapon"), SockeName, partMesh);
	}
	else if (partPos == MODEL_PART_TYPE::MODEL_PART_S_LWEAPON)
	{
		FName SockeName = GameCharacter->GetWeaponSockName(true);
		SetMeshComponent(MeshComponent, TEXT("LHweapon"), SockeName, partMesh);
	}
	else if (partPos == MODEL_PART_TYPE::MODEL_PART_S_RWEAPON)
	{
		FName SockeName = GameCharacter->GetWeaponSockName(false);
		SetMeshComponent(MeshComponent, TEXT("RHweapon"), SockeName, partMesh);
	}
	else if (partPos == MODEL_PART_TYPE::MODEL_PART_STATIC)
	{
		SetMeshComponent(MeshComponent, TEXT("Default"), NAME_None, partMesh);
	}
	else if (partPos == MODEL_PART_TYPE::MODEL_PART_FABAO)
	{
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
		if (IsValid(PlayerCharacter))
		{
			FString FaBaoModelId = "";
			if (CurPartMap.Contains(MODEL_PART_TYPE::MODEL_PART_FABAO))
			{
				FaBaoModelId = *CurPartMap.Find(MODEL_PART_TYPE::MODEL_PART_FABAO);
			}
			PlayerCharacter->UpdateFaBao(FaBaoModelId);
		}
	}
	else if (partPos == MODEL_PART_TYPE::MODEL_PART_BODYS_LIGHT)
	{
		/*APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
		if (IsValid(PlayerCharacter))
		{
			PlayerCharacter->ChangeBodyLightEffect();
		}*/
	}
	else
	{
		APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
		if (IsValid(PlayerCharacter) && PlayerCharacter->GetSelfEntity())
		{
			CS3_Warning(TEXT("RoleChangePart.[5](EntityID=%d, PartType=%d,  Mesh=%d)"),
				PlayerCharacter->GetSelfEntity()->ID(), int32(partPos), PlayerCharacter->GetMesh() ? 1 : 0);
		}

		USkeletalMeshComponent* SkeletalMeshCom = Cast<USkeletalMeshComponent>(MeshComponent);
		SkeletalMeshCom->SetSkeletalMesh(Cast<USkeletalMesh>(partMesh));
		//性能优化,使用到的组件才开启Tick和渲染   CST-9883
		SkeletalMeshCom->SetComponentTickEnabled(true);
		SkeletalMeshCom->SetVisibility(true, true);

		if (partPos == MODEL_PART_TYPE::MODEL_PART_HEAD_ADORN)
		{
			MeshComponent->AttachToComponent(GameCharacter->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, "Socket_Toushi");
		}
		else if (partPos == MODEL_PART_TYPE::MODEL_PART_FACE_ADORN)
		{
			MeshComponent->AttachToComponent(GameCharacter->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, "Socket_MianShi");
		}
		else if (partPos == MODEL_PART_TYPE::MODEL_PART_BACK_ADORN)
		{
			MeshComponent->AttachToComponent(GameCharacter->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, "Socket_Beishi");
		}
		else if (partPos == MODEL_PART_TYPE::MODEL_PART_WAIST_ADORN)
		{
			MeshComponent->AttachToComponent(GameCharacter->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, "Socket_Yaoshi");
		}
		else
		{
			bool IsAttachedToMesh = SkeletalMeshCom->IsAttachedTo(GameCharacter->GetMesh());
			//if (!IsAttachedToMesh)
			{
				SkeletalMeshCom->AttachToComponent(GameCharacter->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
				SkeletalMeshCom->SetVisibility(true, true);
				SkeletalMeshCom->SetComponentTickEnabled(true);
			}
		}
	}
}

void UAppearanceComponent::AddActorPart(MODEL_PART_TYPE PartType, FMODEL_PART_DATA PartData)
{
	SCOPE_CYCLE_COUNTER(STAT_AddActorPart);
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	if (!IsValid(Owner))
	{
		CS3_Warning(TEXT("AppCmpt.Error::AddActorPart Owner is not valid!"));
		return;
	}
	UMeshComponent* MeshComponent = Owner->GetPartMeshComponent(PartType);

	///子部件可以设置偏移、旋转、缩放【法宝是个例外它没子组件，后面需要优化】
	SetPartCptTransform(PartType, MeshComponent, PartData.PartTransform);

	///设置资源
	UObject* PartMesh = PartData.ModelPartPath.Get();
	SetActorPart(PartType, PartMesh);

	///设置部件动画蓝图表现[目前用于头发表现功能]
	if (PartData.PartAnimBpPath.ToSoftObjectPath().IsValid())
	{
		USkeletalMeshComponent* ParSkeletalMeshCom = Cast<USkeletalMeshComponent>(MeshComponent);
		if (IsValid(ParSkeletalMeshCom))
		{
			ParSkeletalMeshCom->SetAnimationMode(EAnimationMode::AnimationBlueprint);
			UClass* PartAnimBpClass = PartData.PartAnimBpPath.Get();
			ParSkeletalMeshCom->SetAnimInstanceClass(PartAnimBpClass);
		}
	}
	for (FString effectID: PartData.EffectIdArray)
	{
		if (!effectID.IsEmpty())
		{
			int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(effectID, 0.0f, Owner, Owner);
			ModelEffectUID.Add(EffectUID);
		}
	}
	// 模型变色
	if (!PartData.ColorScheme.IsEmpty() && IsValid(MeshComponent))
	{
		ChangeModelPartMaterial(MeshComponent, PartData.ColorScheme);
		
	}
}

void UAppearanceComponent::ChangeModelPartMaterial(UMeshComponent * MeshComp, const FString & ColorScheme)
{
	const FMODEL_COLOR_SCHEME_DATA* ModelColorSchemeData = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
		CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_MODEL_SCHEME)->GetRow<FMODEL_COLOR_SCHEME_DATA>(FSTRING_TO_FNAME(ColorScheme));
	if (ModelColorSchemeData)
	{
		TArray<FStringAssetReference> LoadList;
		for (auto It = ModelColorSchemeData->RepMaterialMap.CreateConstIterator(); It; ++It)
		{
			LoadList.Add(It.Value().ToSoftObjectPath());
		}
		if (LoadList.Num() > 0)
		{
			TWeakObjectPtr<UMeshComponent> WeakMeshComp(MeshComp);
			UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, LoadList,
				FStreamableDelegate::CreateLambda([WeakMeshComp, ModelColorSchemeData]()
			{
				UMeshComponent* MeshComp = WeakMeshComp.Get();
				if (!IsValid(MeshComp))return;
				for (auto Its = ModelColorSchemeData->RepMaterialMap.CreateConstIterator(); Its; ++Its)
				{
					if (!Its.Value().Get())continue;
					UMaterialInstanceDynamic* MID = UMaterialInstanceDynamic::Create(Its.Value().Get(), MeshComp);
					MeshComp->SetMaterial(Its.Key(), MID);
				}
			}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_EFFECT);
		}
	}
}

void UAppearanceComponent::CancelActorPart(MODEL_PART_TYPE PartType)
{
	SetActorPart(PartType, nullptr);
}

void UAppearanceComponent::ChangeAnimAction(TSoftClassPtr<UAnimInstance> InAnimationPath, 
	TSoftObjectPtr<UDataTable> InActionConfigPath,
	FChangeAnimComplete ChangeAnimComplete /*= nullptr*/)
{
	SCOPE_CYCLE_COUNTER(STAT_ChangeAnimAction);
	TArray<FStringAssetReference> LoadPartArray;
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	TArray<FACTION_DATA> ChangeActionDatas;

	//动画蓝图
	if (InAnimationPath.ToSoftObjectPath().IsValid())
	{
		LoadPartArray.Add(InAnimationPath.ToSoftObjectPath());
	}

	//动作表
	if (InActionConfigPath.ToSoftObjectPath().IsValid())
	{
		const UDataTable* TableData = CfgManager->GetTableByPath(InActionConfigPath)->GetBaseTable();
		for (auto object : TableData->GetRowMap())
		{
			FACTION_DATA* ActionData = (FACTION_DATA*)object.Value;
			ActionData->Id = object.Key;
			ChangeActionDatas.Add(*ActionData);
			//Owner->ActionDatas.Add(ActionData->ActionPose, *ActionData);
			if (ActionData->AnimPath.ToSoftObjectPath().IsValid())
			{
				LoadPartArray.Add(ActionData->AnimPath.ToSoftObjectPath());
			}
		}
	}
	else
	{
		Owner->ActionDatas.Empty();//给无效的动作表时，策划要求表现为十子架便于查错！
		if (Owner->GetBaseAnimInstance())
		{
			Owner->GetBaseAnimInstance()->StopFrontAction();
		}
	}

	if (LoadPartArray.Num() <= 0)
	{
		return;
	}
	RESOURCE_LOAD_PRIORITY_TYPE LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_OTHER_ENTITY;
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	if (PlayerCharacter)
	{
		LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER;
	}
	FVector OwnerPosition = FVector::ZeroVector;
	AActor* OwnerActor = GetOwner();
	if (IsValid(OwnerActor))
	{
		OwnerPosition = OwnerActor->GetActorLocation();
		TWeakObjectPtr<UAppearanceComponent> DelayThisPtr(this);
		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(OwnerActor, LoadPartArray,
			FStreamableDelegate::CreateLambda([DelayThisPtr, ChangeAnimComplete, InAnimationPath, ChangeActionDatas]()
				{
					if (!DelayThisPtr.IsValid())
					{
						CS3_Warning(TEXT("AppCmpt.Error::ChangeAnimAction RequestAsyncLoad [ *this is error!]"));
						return;
					}
					UAppearanceComponent* ThisPtr = DelayThisPtr.Get();
					AGameCharacter* Owner = Cast<AGameCharacter>(ThisPtr->GetOwner());
					if (!IsValid(Owner))
					{
						return;
					}

					//换动画蓝图
					if (InAnimationPath.ToSoftObjectPath().IsValid())
					{
						if (UClass* AnimClass = InAnimationPath.Get())
						{
							Owner->GetMesh()->SetAnimInstanceClass(AnimClass);
							Owner->SetBaseAnimInstance(Cast<UBaseAnimInstance>(Owner->GetMesh()->GetAnimInstance()));
						}
					}

					//换动作表
					if (IsValid(Owner->GetBaseAnimInstance()))
					{
						//清除当前动作表中所有动作（除了当前正在播的动作）
						FACTION_DATA CurActionData = Owner->GetBaseAnimInstance()->GetCurPlayActionData();
						for (TMap<ACTION_POSE_ENUM, FACTION_DATA>::TIterator It = Owner->ActionDatas.CreateIterator(); It; ++It)
						{
							if (It->Key != CurActionData.ActionPose)
							{
								Owner->ActionDatas.Remove(It->Key);
								//CS3_Display(CS3DebugType::CL_Undefined, TEXT("YYYYY=(%d)"), (int32)It.Key);
							}
						}

						//重新存储当前动作表中所有动作（除了当前正在播的动作）
						FACTION_DATA ChangeCurActionData = FACTION_DATA();
						for (FACTION_DATA ChangeActionData : ChangeActionDatas)
						{
							if (ChangeActionData.ActionPose != CurActionData.ActionPose)
							{
								Owner->ActionDatas.Add(ChangeActionData.ActionPose, ChangeActionData);
							}
							else
							{
								ChangeCurActionData = ChangeActionData;
							}
						}
						ThisPtr->UpdateActionAnimAssetList();

						//当其他动作更新完后，再更新当前正在播放的动作(解决所有动作一次更新会使玩家会变十字架的问题)
						if (ChangeCurActionData.Id.IsNone())
						{
							Owner->ActionDatas.Remove(CurActionData.ActionPose);
						}
						else
						{
							ThisPtr->SetActionAnimAsset(ChangeCurActionData);
							Owner->ActionDatas.Emplace(ChangeCurActionData.ActionPose, ChangeCurActionData);
						}

						Owner->GetBaseAnimInstance()->RefreshData();
						ChangeAnimComplete.ExecuteIfBound();
					}
						
				}), LoadPriority, OwnerPosition);
	}
}

void UAppearanceComponent::CopyCharacterFromClientAppearance(ACharacter* CopyCharacter)
{
	SCOPE_CYCLE_COUNTER(STAT_CopyModelFrom);
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(CopyCharacter);
	AGameCharacter* ApperanceCharacter = PlayerCharacter;

	if (IsValid(PlayerCharacter) && PlayerCharacter->GetRiderCharacter())
	{
		ApperanceCharacter = PlayerCharacter->GetRiderCharacter();
	}

	if (IsValid(ApperanceCharacter))
	{
		TSharedPtr<FMODEL_DATA> ModelData = ApperanceCharacter->GetCurModelData();
		if (ModelData.IsValid())
		{
			CurCreateAppData.RoleModelId = ApperanceCharacter->GetCurModelData()->RowName.ToString();
			TMap<MODEL_PART_TYPE, FString> NewPartMap = ApperanceCharacter->GetAppearanceComponent()->GetPartMap();
			CreateModel(CurCreateAppData.RoleModelId, NewPartMap);
		}
	}
}

void UAppearanceComponent::CopyCharacterFromServerAppearance(ACharacter* CopyCharacter)
{
	SCOPE_CYCLE_COUNTER(STAT_CopyModelFromNormal);
	AGameCharacter* OwnerCharacter = Cast<AGameCharacter>(GetOwner());
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(CopyCharacter);
	if (!IsValid(OwnerCharacter) || !IsValid(PlayerCharacter) || !PlayerCharacter->GetSelfEntity())
	{
		CS3_Warning(TEXT("AppCmpt.Error::CopyModelFromNormal [ *this is error!]"));
		return;
	}
	int32 Profession = (int32)PlayerCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("profession"));
	int32 Gender = (int32)PlayerCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("gender"));
	int32 Camp = (int32)PlayerCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("camp"));
	OwnerCharacter->ProfessionID = PlayerCharacter->ProfessionID;

	int32 RowIndex = Profession;
	if (Camp == 2)//阵营1仙 2魔
	{
		RowIndex += 8;
	}
	if (Gender == 2)//性别1男 2女
	{
		RowIndex += 4;
	}
	const FRoleCreateUIData* RoleCreateUIData = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
		CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_CREATE)->GetRow<FRoleCreateUIData>(FSTRING_TO_FNAME(INT_TO_FSTRING(RowIndex)));

	FString CopyModelId = "";
	if (RoleCreateUIData)
	{
		CopyModelId = RoleCreateUIData->RoleModelName.ToString();
	}

	GameObject *PlayerGameObject = (GameObject*)PlayerCharacter->GetSelfEntity();
	CreateAppearanceByModelInfo(CopyModelId, PlayerGameObject->GetModelInfo());
}

void UAppearanceComponent::SetMaterialColor(FLinearColor &LinearColor)
{
	SCOPE_CYCLE_COUNTER(STAT_SetMaterialColor);
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	if (IsValid(Owner))
	{
		TArray<class UMaterialInterface*> MaterialsList;
		MaterialsList = Owner->GetMesh()->GetMaterials();
		for (int i = 0; i < MaterialsList.Num(); i++)
		{
			if (IsValid(MaterialsList[i]))
			{
				UMaterialInstanceDynamic* MaterialInstanceDynamic = Owner->GetMesh()->UPrimitiveComponent::CreateDynamicMaterialInstance(i, MaterialsList[i]);
				MaterialInstanceDynamic->SetVectorParameterValue(TEXT("EdgeEmissiveColor"), LinearColor);
			}
		}

		UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
		TArray<class UMaterialInterface*> ST_MaterialsList = DefaultStaticMeshCpt->GetMaterials();
		for (int i = 0; i < ST_MaterialsList.Num(); i++)
		{
			if (IsValid(ST_MaterialsList[i]))
			{
				UMaterialInstanceDynamic* StaticMeshMaterialInstanceDynamic = DefaultStaticMeshCpt->UPrimitiveComponent::CreateDynamicMaterialInstance(i, ST_MaterialsList[i]);
				StaticMeshMaterialInstanceDynamic->SetVectorParameterValue(TEXT("EdgeEmissiveColor"), LinearColor);
			}
		}
	}
}

void UAppearanceComponent::SetPartCptTransform(MODEL_PART_TYPE PartType, UMeshComponent* MeshComponent, const FPART_TRANSFORM& Transfrom)
{
	if (PartType == MODEL_PART_TYPE::MODEL_PART_FABAO)
	{
		return;
	}

	if (IsValid(MeshComponent))
	{
		//背饰需要检测偏移量优先级（玩家调整过的偏移量 > 部件表默认的偏移量）
		FPART_TRANSFORM CptTransfrom = Transfrom;
		if (PartType == MODEL_PART_TYPE::MODEL_PART_BACK_ADORN)
		{
			APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
			if (IsValid(PlayerCharacter))
			{
				FPART_TRANSFORM BackAdronTransfrom;
				PlayerCharacter->GetBackAdornTransfrom(BackAdronTransfrom);
				if (!BackAdronTransfrom.RelativeLocation.IsZero())
				{
					CptTransfrom.RelativeLocation = BackAdronTransfrom.RelativeLocation;
				}
				if (!BackAdronTransfrom.RelativeRotation.IsZero())
				{
					CptTransfrom.RelativeRotation = BackAdronTransfrom.RelativeRotation;
				}
			}
		}

		bool IsZeroLocation = CptTransfrom.RelativeLocation.IsZero();
		if (!IsZeroLocation)
		{
			MeshComponent->SetRelativeLocation(CptTransfrom.RelativeLocation);
		}
		bool IsZeroRotation = CptTransfrom.RelativeRotation.IsZero();
		if (!IsZeroRotation)
		{
			MeshComponent->SetRelativeRotation(CptTransfrom.RelativeRotation);
		}
		MeshComponent->SetRelativeScale3D(CptTransfrom.RelativeScale3D);
	}
}

void UAppearanceComponent::UpdatePartMap(MODEL_PART_TYPE ModelPartType, FString PartId)
{
	CurPartMap.Add(ModelPartType, PartId);
}

void UAppearanceComponent::ResetWeapon(bool IsFightShow, int32 InProfession)
{
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	UMeshComponent* LeftMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_LWEAPON);
	UMeshComponent* RightMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_RWEAPON);
	UMeshComponent* SLeftMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON);
	UMeshComponent* SRightMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON);
	ClearWeapon();
	//ROLE_PROFESSION_ENUM Profession = (ROLE_PROFESSION_ENUM)InProfession;
	if (CurPartMap.Contains(MODEL_PART_TYPE::MODEL_PART_LWEAPON))
	{
		FString PartId = CurPartMap[MODEL_PART_TYPE::MODEL_PART_LWEAPON];
		const FMODEL_PART_DATA* pPartData = GetPartDataFromCfg(PartId);
		if (pPartData)
		{
			AddActorPart(MODEL_PART_TYPE::MODEL_PART_LWEAPON, *pPartData);
		}
	}
	if (CurPartMap.Contains(MODEL_PART_TYPE::MODEL_PART_RWEAPON))
	{
		FString PartId = CurPartMap[MODEL_PART_TYPE::MODEL_PART_RWEAPON];
		const FMODEL_PART_DATA* pPartData = GetPartDataFromCfg(PartId);
		if (pPartData)
		{
			AddActorPart(MODEL_PART_TYPE::MODEL_PART_RWEAPON, *pPartData);
		}
	}
	if (CurPartMap.Contains(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON))
	{
		FString PartId = CurPartMap[MODEL_PART_TYPE::MODEL_PART_S_LWEAPON];
		const FMODEL_PART_DATA* pPartData = GetPartDataFromCfg(PartId);
		if (pPartData)
		{
			AddActorPart(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON, *pPartData);
		}
	}
	if (CurPartMap.Contains(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON))
	{
		FString PartId = CurPartMap[MODEL_PART_TYPE::MODEL_PART_S_RWEAPON];
		const FMODEL_PART_DATA* pPartData = GetPartDataFromCfg(PartId);
		if (pPartData)
		{
			AddActorPart(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON, *pPartData);
		}
	}
}

void UAppearanceComponent::ClearWeapon()
{
	CancelActorPart(MODEL_PART_TYPE::MODEL_PART_LWEAPON);
	CancelActorPart(MODEL_PART_TYPE::MODEL_PART_RWEAPON);
	CancelActorPart(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON);
	CancelActorPart(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON);
	CancelActorPart(MODEL_PART_TYPE::MODEL_PART_BWEAPON);
}

void UAppearanceComponent::UpdateWeaponLocation(bool IsFightShow, int32 InProfession)
{
	SCOPE_CYCLE_COUNTER(STAT_UpdateWeaponLocation);
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	UMeshComponent* LeftMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_LWEAPON);
	UMeshComponent* RightMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_RWEAPON);
	UMeshComponent* SLeftMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON);
	UMeshComponent* SRightMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON);

	ROLE_PROFESSION_ENUM Profession = (ROLE_PROFESSION_ENUM)InProfession;
	if (Profession == ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_ZHAN_SHI)
	{
	}
	else if (Profession == ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_JIAN_KE)
	{
	}
	else if (Profession == ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_SHE_SHOU)
	{
		const FAttachmentTransformRules AttachmentRules = FAttachmentTransformRules::KeepRelativeTransform;
		if (IsFightShow)
		{
			LeftMeshComponent->AttachToComponent(Owner->GetMesh(), AttachmentRules, "Socket_Weapon_L");
			RightMeshComponent->AttachToComponent(Owner->GetMesh(), AttachmentRules, "Socket_Weapon_R");

			if (CurPartMap.Contains(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON))
			{
				FString PartId = CurPartMap[MODEL_PART_TYPE::MODEL_PART_S_LWEAPON];
				const FMODEL_PART_DATA* pPartData = GetPartDataFromCfg(PartId);
				if (pPartData)
				{
					AddActorPart(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON, *pPartData);
					SLeftMeshComponent->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
					SLeftMeshComponent->SetCollisionResponseToAllChannels(ECR_Ignore);
				}
			}
			if (CurPartMap.Contains(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON))
			{
				FString PartId = CurPartMap[MODEL_PART_TYPE::MODEL_PART_S_RWEAPON];
				const FMODEL_PART_DATA* pPartData = GetPartDataFromCfg(PartId);
				if (pPartData)
				{
					AddActorPart(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON, *pPartData);
					SRightMeshComponent->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
					SRightMeshComponent->SetCollisionResponseToAllChannels(ECR_Ignore);
				}
			}
		}
		else
		{
			LeftMeshComponent->AttachToComponent(Owner->GetMesh(), AttachmentRules, "Socket_Weapon_Whip_Spine_L");
			RightMeshComponent->AttachToComponent(Owner->GetMesh(), AttachmentRules, "Socket_Weapon_Whip_Spine_R");
			
			CancelActorPart(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON);
			CancelActorPart(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON);
		}
	}
	else if (Profession == ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_FA_SHI)
	{
	}
	else
	{
	}
}

void UAppearanceComponent::UpdateWeaponRightToLeft(bool IsRightToLeft, int32 InProfession)
{
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	UMeshComponent* LeftMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_LWEAPON);
	UMeshComponent* RightMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_RWEAPON);
	UMeshComponent* SLeftMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON);
	UMeshComponent* SRightMeshComponent = Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON);

	ROLE_PROFESSION_ENUM Profession = (ROLE_PROFESSION_ENUM)InProfession;
	if (Profession == ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_JIAN_KE)
	{
		const FAttachmentTransformRules AttachmentRules = FAttachmentTransformRules::KeepRelativeTransform;
		if (IsRightToLeft)
		{
			RightMeshComponent->AttachToComponent(Owner->GetMesh(), AttachmentRules, "Socket_Weapon_L_RightOnLeft");
			LeftMeshComponent->AttachToComponent(Owner->GetMesh(), AttachmentRules, "Socket_Weapon_L");
		}
		else
		{
			RightMeshComponent->AttachToComponent(Owner->GetMesh(), AttachmentRules, "Socket_Weapon_R");
			LeftMeshComponent->AttachToComponent(Owner->GetMesh(), AttachmentRules, "Socket_Weapon_L");
		}
		
	}
}

void UAppearanceComponent::UpdateWeapontYXFXZ(YXFXZ_COPY_WEAPON_ENUM Type)
{
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	if (!IsValid(Owner))
	{
		return;
	}
	FName SockeName = "";
	FString PartId = "";
	switch (Type)
	{
	case YXFXZ_COPY_WEAPON_ENUM::YXFXZ_COPY_WEAPON_NULL:
		break;
	case YXFXZ_COPY_WEAPON_ENUM::YXFXZ_COPY_WEAPON_BISHOU:
		SockeName = "Socket_Weapon_Dagger";
		PartId = "SM_ZW0124";
		break;
	case YXFXZ_COPY_WEAPON_ENUM::YXFXZ_COPY_WEAPON_DAO:
		SockeName = "Socket_Weapon_Dagger";
		PartId = "SM_ZW0156";
		break;
	case YXFXZ_COPY_WEAPON_ENUM::YXFXZ_COPY_WEAPON_QIANG:
		SockeName = "Socket_Weapon_Long";
		PartId = "SM_ZW0157";
		break;
	case YXFXZ_COPY_WEAPON_ENUM::YXFXZ_COPY_WEAPON_GONG:
		SockeName = "Socket_Weapon_Bow";
		PartId = "SM_ZW0158";
		break;
	case YXFXZ_COPY_WEAPON_ENUM::YXFXZ_COPY_WEAPON_JIAN:
		SockeName = "Socket_Weapon_Arrow";
		PartId = "SM_ZW0159";
		break;
	default:
		break;
	}

	const FMODEL_PART_DATA* pPartData = GetPartDataFromCfg(PartId);
	if (pPartData)
	{
		RESOURCE_LOAD_PRIORITY_TYPE LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER;
		UMeshComponent* MeshComponent = Cast<UStaticMeshComponent>(Owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_RWEAPON));;

		TWeakObjectPtr<UAppearanceComponent> DelayThisPtr(this);
		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(Owner,
			pPartData->ModelPartPath.ToSoftObjectPath(),
			FStreamableDelegate::CreateLambda([DelayThisPtr, pPartData, SockeName, MeshComponent]()
				{
					if (!DelayThisPtr.IsValid())
					{
						return;
					}
					UAppearanceComponent* ThisPtr = DelayThisPtr.Get();
					UObject* PartMesh = pPartData->ModelPartPath.Get();
					ThisPtr->SetMeshComponent(MeshComponent, TEXT("RHweapon"), SockeName, PartMesh);
				}), LoadPriority);
	}
}

void UAppearanceComponent::UpdateWeapontYCJMD(YCJMD_COPY_WEAPON_ENUM Type, const FString& SockeName, const FString& PartId)
{
	AGameCharacter* GameCharacter = Cast<AGameCharacter>(GetOwner());
	if (!IsValid(GameCharacter))
	{
		return;
	}
	MODEL_PART_TYPE PartType = MODEL_PART_TYPE::MODEL_PART_RWEAPON;
	FName WeapCptName = "";
	switch (Type)
	{
	case YCJMD_COPY_WEAPON_ENUM::YCJMD_COPY_WEAPON_NULL:
		ResetWeapon(false, 1);
		break;
	case YCJMD_COPY_WEAPON_ENUM::YCJMD_COPY_WEAPON_SHOU_NU:
		WeapCptName = "Weapon_SHOU_NU";
		break;
	case YCJMD_COPY_WEAPON_ENUM::YCJMD_COPY_WEAPON_SHI_ZI_NU:
		WeapCptName = "Weapon_SHI_ZI_NU";
		break;
	default:
		break;
	}

	const FMODEL_PART_DATA* PartData = GetPartDataFromCfg(PartId);
	if (PartData)
	{
		RESOURCE_LOAD_PRIORITY_TYPE LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER;
		UMeshComponent* MeshComponent = GameCharacter->GetPartMeshComponent(PartType);

		TWeakObjectPtr<UAppearanceComponent> DelayThisPtr(this);
		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(GameCharacter,
			PartData->ModelPartPath.ToSoftObjectPath(),
			FStreamableDelegate::CreateLambda([DelayThisPtr, PartData, PartType, SockeName, WeapCptName, MeshComponent]()
				{
					if (!DelayThisPtr.IsValid())
					{
						return;
					}
					UAppearanceComponent* ThisPtr = DelayThisPtr.Get();
					ThisPtr->ClearWeapon();

					///设置偏移、旋转、缩放
					ThisPtr->SetPartCptTransform(PartType, MeshComponent, PartData->PartTransform);

					///设置资源
					UObject* PartMesh = PartData->ModelPartPath.Get();
					ThisPtr->SetMeshComponent(MeshComponent, WeapCptName, FSTRING_TO_FNAME(SockeName), PartMesh);
				}), LoadPriority);
	}
}

TSharedPtr<FMODEL_DATA> UAppearanceComponent::GetModelData()
{
	return CurModelData;
}

void UAppearanceComponent::SetModelData(TSharedPtr<FMODEL_DATA> ModelData)
{ 
	CurModelData = ModelData;
}

TMap<MODEL_PART_TYPE, FString>& UAppearanceComponent::GetPartMap()
{
	return CurPartMap;
}

FString UAppearanceComponent::GetModelId()
{
	return CurCreateAppData.RoleModelId;
}

void UAppearanceComponent::SetAnimData(TSoftClassPtr<UAnimInstance> AnimationPath, TSoftObjectPtr<UDataTable> ActionConfigPath)
{
	CurModelData->AnimationPath = AnimationPath;
	CurModelData->ActionConfigPath = ActionConfigPath;
}

void UAppearanceComponent::PlayerBornEffect()
{
	SCOPE_CYCLE_COUNTER(STAT_PlayerBornEffect);
	if (!IsValid(GetOwner())) return;
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());

	if (CurModelData.Get())
	{
		if (ModelEffectUID.Num() > 0)
		{
			for (auto UID : ModelEffectUID)
			{
				UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(UID);
			}
			ModelEffectUID.Empty();
		}

		for (FString effectID : CurModelData->EffectIdArray)
		{
			if (!effectID.IsEmpty())
			{
				int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(effectID, 0.0f, Owner, Owner);
				ModelEffectUID.Add(EffectUID);
			}
		}
	}
}

void UAppearanceComponent::AttachStaticMeshComponent(UStaticMeshComponent* staticMeshComponent, FName sockName, UObject* mesh)
{
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	staticMeshComponent->SetStaticMesh(Cast<UStaticMesh>(mesh));
	staticMeshComponent->AttachToComponent(Owner->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, sockName);
}

void UAppearanceComponent::AttachSkeletalMeshComponent(USkeletalMeshComponent* skeletalMeshComponent, FName sockName, UObject* mesh)
{
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	skeletalMeshComponent->RemoveAllClothingActors();
	skeletalMeshComponent->SetSkeletalMesh(Cast<USkeletalMesh>(mesh));
	skeletalMeshComponent->AttachToComponent(Owner->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, sockName);
}

UStaticMeshComponent* UAppearanceComponent::CreateStaticMeshComponent( FName ComponentName)
{
	SCOPE_CYCLE_COUNTER(STAT_CreateStaticMeshComponent);
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	FName NewCptName = FName(*FString::Printf(TEXT("%s_%s"), *ComponentName.ToString(), TEXT("Static")));
	UStaticMeshComponent* newStaticMeshComponent = NewObject<UStaticMeshComponent>(Owner, NewCptName);
	newStaticMeshComponent->bReceivesDecals = false;
	newStaticMeshComponent->RegisterComponent();
	return newStaticMeshComponent;
}

USkeletalMeshComponent* UAppearanceComponent::CreateSkeletalMeshComponent( FName ComponentName)
{
	SCOPE_CYCLE_COUNTER(STAT_CreateSkeletalMeshComponent);
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	FName NewCptName = FName(*FString::Printf(TEXT("%s_%s"), *ComponentName.ToString(), TEXT("Skeletal")));
	USkeletalMeshComponent* newSkeletalMeshComponent = NewObject<USkeletalMeshComponent>(Owner, NewCptName);
	newSkeletalMeshComponent->bReceivesDecals = false;
	newSkeletalMeshComponent->RegisterComponent();
	return newSkeletalMeshComponent;
}

//UMeshComponent* MeshCpt, FName CptName, FName SockName, UObject* MeshObject
void UAppearanceComponent::SetMeshComponent(UMeshComponent* MeshCpt, FName CptName, 
	FName SockName, UObject* MeshObject)
{
	SCOPE_CYCLE_COUNTER(STAT_SetMeshComponent);
	if (!IsValid(MeshCpt))
	{
		CS3_Warning(TEXT("AppCmpt.Error::SetMeshComponent [ *MeshCpt is error!]"));
		return;
	}

	UClass* MeshCptClass = MeshCpt->GetClass();
	if (MeshCptClass == UStaticMeshComponent::StaticClass())
	{
		if (IsValid(MeshObject))
		{
			UClass* MeshClass = MeshObject->GetClass();
			if (MeshClass != UStaticMesh::StaticClass())
			{
				MeshCpt->DestroyComponent(true);
				MeshCpt = CreateStaticMeshComponent(CptName);
			}
		}
		AttachStaticMeshComponent(Cast<UStaticMeshComponent>(MeshCpt), SockName, MeshObject);
	}
	else if (MeshCptClass == USkeletalMeshComponent::StaticClass())
	{
		if (IsValid(MeshObject))
		{
			UClass* MeshClass = MeshObject->GetClass();
			if (MeshClass != USkeletalMesh::StaticClass())
			{
				MeshCpt->DestroyComponent(true);
				MeshCpt = CreateSkeletalMeshComponent(CptName);
			}
		}
		AttachSkeletalMeshComponent(Cast<USkeletalMeshComponent>(MeshCpt), SockName, MeshObject);
	}

	if (CurModelData && CurModelData->IsRenderCustomDepth)
	{
		//设置个部位的自定义深度
		MeshCpt->SetRenderCustomDepth(CurModelData->IsRenderCustomDepth);
	}

	// 性能优化,使用到的组件才开启Tick和渲染   CST-9883
	{
		MeshCpt->SetComponentTickEnabled(true);
		MeshCpt->SetVisibility(true, true);
	}
}

void UAppearanceComponent::UpdateActionAnimAssetList()
{
	SCOPE_CYCLE_COUNTER(STAT_SetActionAnimAsset);
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	if (IsValid(Owner))
	{
		for (auto& Kvp : Owner->ActionDatas)
		{
			FACTION_DATA& ActionData = Kvp.Value;
			SetActionAnimAsset(ActionData);
		}
	}
}

void UAppearanceComponent::SetActionAnimAsset(FACTION_DATA& ActionData)
{
	AGameCharacter* Owner = Cast<AGameCharacter>(GetOwner());
	UActionManager *ActionManager = UUECS3GameInstance::Instance->ActionManager;
	if (IsValid(Owner) && IsValid(ActionManager))
	{
		ActionData.GroundType = ActionManager->GetActionGround(ActionData);
		if (ActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_BLEND_SPACE || 
			ActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_OFFSET_BLEND_SAPCE)
		{
			ActionData.CurBlendSpaceBase = (UBlendSpaceBase*)ActionData.AnimPath.Get();
			ActionData.ActionName = ActionData.CurBlendSpaceBase ? ActionData.CurBlendSpaceBase->GetName() : "";
		}
		else
		{
			ActionData.CurAnimSquenceBase = (UAnimSequenceBase*)ActionData.AnimPath.Get();
			ActionData.ActionName = ActionData.CurAnimSquenceBase ? ActionData.CurAnimSquenceBase->GetName() : "";
		}
		//储存随机动作
		if (ActionData.ActionType == ACTION_TYPE_ENUM::ACTION_TYPE_RANDOM && ActionData.CurAnimSquenceBase)
		{
			Owner->RandomActionDatas.Add(ActionData);
		}

		if (Owner->IsControlled() || IsValid(Cast<ARiderCharacter>(Owner)))
		{
			UUECS3GameInstance::Instance->CharacterRideManager->CacheRideAsset(ActionData.AnimPath.ToString(), ActionData.AnimPath.Get());
		}
	}
}

void UAppearanceComponent::CreatePartMapByServer(TMap<MODEL_PART_TYPE, FString>& InPartDataMap)
{
	SCOPE_CYCLE_COUNTER(STAT_CreatePartMapByServer);
	if (!CurCreateAppData.RoleModelId.IsEmpty())
	{
		InPartDataMap = GetPartDataMapByModelNumber(CurCreateAppData.RoleModelId);
	}

	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(GetOwner());
	if (IsValid(ServerCharacter))
	{
		TMap<MODEL_PART_TYPE, FString> ServerPartDataMap;
		ServerCharacter->CreatePartMapByServer(ServerPartDataMap);
		if (ServerPartDataMap.Num() > 0)
		{
			InPartDataMap.Append(ServerPartDataMap);
		}
	}
}

TMap<MODEL_PART_TYPE, FString> UAppearanceComponent::GetPartDataMapByModelNumber(FString InModelNumber)
{
	SCOPE_CYCLE_COUNTER(STAT_GetPartDataMapByModelNumber);
	const FMODEL_DATA* ModelData = GetModelDataFromCfg(InModelNumber);
	if (ModelData == nullptr)
	{
		ModelData = GetModelDataFromCfg(DefaultNumber);
	}
	TMap<MODEL_PART_TYPE, FString> OutPartMap;
	for (FPartItem PratItem : ModelData->PartArray)
	{
		OutPartMap.Add(PratItem.posType, PratItem.PartID);
	}
	return OutPartMap;
}

TMap<MODEL_PART_TYPE, FString> UAppearanceComponent::GetPartDataMapByModelInfo(const FAModelInfo& AModelInfo)
{
	SCOPE_CYCLE_COUNTER(STAT_GetPartDataMapByModelInfo);
	TMap<MODEL_PART_TYPE, FString> InPartDataMap;
	TArray<FString> WeaponModels = UGolbalBPFunctionLibrary::SplitString(AModelInfo.WeaponModel);
	TArray<FString> SkeletalWeaponModels = UGolbalBPFunctionLibrary::SplitString(AModelInfo.SkeletalWeaponModel);
	FString LWeaponModel = WeaponModels.Num() > 0 ? WeaponModels[0] : "";
	FString RWeaponModel = WeaponModels.Num() > 1 ? WeaponModels[1] : "";
	FString LSkeletalweaponModel = SkeletalWeaponModels.Num() > 0 ? SkeletalWeaponModels[0] : "";
	FString RSkeletalweaponModel = SkeletalWeaponModels.Num() > 1 ? SkeletalWeaponModels[1] : "";

	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_BODYS, AModelInfo.BodyModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_HEADS, AModelInfo.HeadModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_SUITS, AModelInfo.SuitsModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_HAIRS, AModelInfo.HairModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_ADORN, AModelInfo.AdornModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_HEAD_ADORN, AModelInfo.HeadAdornModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_FACE_ADORN, AModelInfo.FaceAdornModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_BACK_ADORN, AModelInfo.BackAdornModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_WAIST_ADORN, AModelInfo.WaistAdornModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_HAT, AModelInfo.HatModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_COATS, AModelInfo.CoatModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_WRIST, AModelInfo.WristModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_GLOVES, AModelInfo.GlovesModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_WAIST, AModelInfo.WaistModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_PANTS, AModelInfo.PantsModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_SHOES, AModelInfo.ShoesModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_NECKLACE, AModelInfo.NecklaceModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_LHAND_RING, AModelInfo.LringModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_RHAND_RING, AModelInfo.RringModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_LWEAPON, LWeaponModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_RWEAPON, RWeaponModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_CLOAK, AModelInfo.CloakModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_FABAO, AModelInfo.FaBaoModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON, LSkeletalweaponModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON, RSkeletalweaponModel);
	InPartDataMap.Add(MODEL_PART_TYPE::MODEL_PART_BODYS_LIGHT, AModelInfo.bodyLightEffect);
	return InPartDataMap;
}

const FMODEL_PART_DATA* UAppearanceComponent::GetPartDataFromCfg(FString PartID)
{
	if (!IsValid(UUECS3GameInstance::Instance))
	{
		return nullptr;
	}
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	auto PartTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PART_MODEL);
	auto PartValue = PartTable->GetRow<FMODEL_PART_DATA>(PartID);
	return PartValue;

}

const FMODEL_DATA* UAppearanceComponent::GetModelDataFromCfg(FString InModelNumber)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	auto ModelTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_MODEL);
	const FMODEL_DATA* OutModelData = ModelTable->GetRow<FMODEL_DATA>(InModelNumber);
	if (OutModelData == nullptr)
	{
		OutModelData = ModelTable->GetRow<FMODEL_DATA>(DefaultNumber);
	}
	return OutModelData;
}

void UAppearanceComponent::UpdateStateEffect()
{
	AServerCharacter* GameCharacter = Cast<AServerCharacter>(GetOwner());
	//模型创建完毕刷新状态光效
	if (GameCharacter && GameCharacter->GetSelfEntity())
	{
		if (GameCharacter->GetSelfEntity()->ClassName() == "Role")
		{
			UStateInterface* roleStateInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.StateInterface : nullptr;
			if (roleStateInterface)
			{
				roleStateInterface->OnRep_effectState();
			}
		}
		else
		{
			UStateInterface* stateInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.StateInterface : nullptr;
			if (stateInterface)
			{
				stateInterface->OnRep_effectState();
			}
		}
	}
}

/*-------------------人物外观组件-------------------------------------*/

URoleAppearanceComponent::URoleAppearanceComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
	isInModelCreating = false;
	if (IsValid(UUECS3GameInstance::Instance))
	{
		DefaultNumber = UUECS3GameInstance::Instance->GameDefault->DefaultModelNumber_N;
	}
}

void URoleAppearanceComponent::CreateRideAppearance(FCREATE_APPEARANCE_DATA CreateAppData)
{
	SCOPE_CYCLE_COUNTER(STAT_CreateRideAppearance);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.CreateRideAppearance(ModelId=%s, isInModelCreating=%d)"), 
		*CreateAppData.RoleModelId, isInModelCreating ? 1 : 0);

	if (isInModelCreating)
	{
		bHasCacheModelNumber = true; //正在创建中，但是有新的模型需要创建
		CachaeCreateAppData = CreateAppData;
		return;
	}
	isInModelCreating = true;
	CurCreateAppData = CreateAppData;

	if (CurCreateAppData.RidePetModelId.IsEmpty())
	{//正常模式	
		CreateRoleModel(CurCreateAppData.RoleModelId);
	}
	else
	{//骑乘模式
		CreateRiderAndPetForRideModel();
	}
}

void URoleAppearanceComponent::ChangePart(MODEL_PART_TYPE PartType, FString PartID)
{
	SCOPE_CYCLE_COUNTER(STAT_ChangePart);
	//判断是否载具模式下（是:else  否：if）
	if (CurCreateAppData.RidePetModelId.IsEmpty())
	{
		if (CurPartMap.Contains(PartType))
		{
			if (CurPartMap[PartType] == PartID)
			{
				return;
			}
			CurPartMap[PartType] = PartID;
		}
		else
		{
			CurPartMap.Add(PartType, PartID);
		}

		if (PartID.IsEmpty())
		{
			CancelActorPart(PartType);
			OnChangePartOver();
		}
		else
		{
			const FMODEL_PART_DATA* pPartData = GetPartDataFromCfg(PartID);
			if (pPartData)
			{
				RESOURCE_LOAD_PRIORITY_TYPE LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_OTHER_ENTITY;
				AActor* OwnerActor = GetOwner();
				AGameCharacter* PlayerCharacter = Cast<AGameCharacter>(OwnerActor);
				if (IsValid(PlayerCharacter))
				{
					TArray<FStringAssetReference> LoadArray;
					LoadArray.Push(pPartData->ModelPartPath.ToSoftObjectPath());
					if (pPartData->PartAnimBpPath.ToSoftObjectPath().IsValid())
					{
						LoadArray.Push(pPartData->PartAnimBpPath.ToSoftObjectPath());
					}

					LoadPriority = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER;
					FVector OwnerPosition = GetOwner()->GetActorLocation();
					TWeakObjectPtr<URoleAppearanceComponent> DelayThisPtr(this);
					UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(PlayerCharacter, LoadArray,
						FStreamableDelegate::CreateLambda([DelayThisPtr, PartType, pPartData]()
							{
								if (!DelayThisPtr.IsValid())
								{
									CS3_Warning(TEXT("UAppearanceComponent::CreateModel:LoadAssetPathCallBack *this is error!"));
									return;
								}
								URoleAppearanceComponent* ThisPtr = DelayThisPtr.Get();
								ThisPtr->OnChangeActorPartLoadCompleted(PartType, pPartData);
							}), LoadPriority, OwnerPosition);
				}
			}
		}
	}
	else
	{
		APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetOwner());
		if (IsValid(PlayerActor) && IsValid(PlayerActor->GetRiderCharacter()))
		{
			PlayerActor->GetRiderCharacter()->ChangeActorPart(PartType, PartID);
		}
	}
}

void URoleAppearanceComponent::CreateModelOver()
{
	isInModelCreating = false;
	AGameCharacter* GameCharacter = Cast<AGameCharacter>(GetOwner());
	if (IsValid(GameCharacter))
	{
		GameCharacter->OnCreateModelOver();
		//刷新状态光效
		UpdateStateEffect();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.CreateModelOver.Role(Name=%s, bHasCacheModelNumber=%d, CacheRoleModelNumber=%s)"), 
			*GameCharacter->GetName(), bHasCacheModelNumber ? 1 : 0, *CachaeCreateAppData.RoleModelId);

		if (bHasCacheModelNumber)
		{
			bHasCacheModelNumber = false;
			//有缓存的角色模型，继续创建(骑乘模式不做支持)
			CreateRideAppearance(CachaeCreateAppData);			
		}
	}
}

bool URoleAppearanceComponent::CreateRoleModel(FString RoleModelId)
{
	SCOPE_CYCLE_COUNTER(STAT_CreateRoleModel);
	TSharedPtr<FMODEL_DATA> ModelData = GetRoleModelData(CurCreateAppData.RoleModelId);
	SetModelData(ModelData);

	TMap<MODEL_PART_TYPE, FString> PartDataMap;
	CreatePartMapByServer(PartDataMap);
	if (PartDataMap.Num() == 0)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.Error::CreateRoleModel is IsEmpty![ModelNumber=%s]"), *CurCreateAppData.RoleModelId);
		return false;
	}

	TWeakObjectPtr<URoleAppearanceComponent> DelayThisPtr(this);
	LoadModelTotalAssetPath([DelayThisPtr, PartDataMap]()
	{
		if (!DelayThisPtr.IsValid())
		{
			CS3_Warning(TEXT("AppCmpt.Error::CreateRoleModel:LoadAssetPathCallBack *this is error!"));
			return;
		}
		URoleAppearanceComponent* ThisPtr = DelayThisPtr.Get();
		ThisPtr->ApplayModelByPartsMap(PartDataMap);
	});
	return true;
}

bool URoleAppearanceComponent::CreateRiderAndPetForRideModel()
{
	SCOPE_CYCLE_COUNTER(STAT_CreateRiderAndPetForRideModel);
	if (CurCreateAppData.RoleProfession == (int32)ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_NULL || 
		CurCreateAppData.RidePosture == RIDE_POSTURE_ENUM::RIDE_POSTURE_NULL)
	{
		return false;
	}

	//骑宠模型数据(主体)
	TSharedPtr<FMODEL_DATA> ModelData = MakeShareable(new FMODEL_DATA(*GetModelDataFromCfg(CurCreateAppData.RidePetModelId)));
	if (ModelData.Get()==NULL)
	{
		return false;
	}

	//人物模型数据(附体)
	TSharedPtr<FMODEL_DATA> RoleModelData = GetRoleModelData(CurCreateAppData.RoleModelId);
	if (RoleModelData.Get() == NULL)
	{
		return false;
	}

	//获取骑士的姿势数据[配置表：DT_RiderModelAnimCfg---180]
	FRIDER_MODEL_ANIM_DATA* RiderModelAnimData = GetRideModelAnimDataFromCfg(CurCreateAppData.RidePosture,
		(ROLE_PROFESSION_ENUM)CurCreateAppData.RoleProfession, (ROLE_GENDER_ENUM)CurCreateAppData.RoleGender);
	if (RiderModelAnimData == nullptr)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.Error::CreateRiderPet[RiderModelAnimData=nullptr]"));
		return false;
	}

	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwner());
	ARiderCharacter* RiderCharacter = PlayerCharacter->GetRiderCharacter();
	RiderCharacter->SetPlayerCharacter(PlayerCharacter);

	//骑宠
	SetModelData(ModelData);
	
	//设置骑士人物的姿势：动画蓝图、动作表
	RiderCharacter->SetModelData(RoleModelData);
	RiderCharacter->UseRideAnimData(RiderModelAnimData->AnimationPath, RiderModelAnimData->ActionConfigPath);

	TWeakObjectPtr<URoleAppearanceComponent> DelayThisPtr(this);
	LoadModelTotalAssetPath([DelayThisPtr, RiderCharacter]()
	{
		if (!DelayThisPtr.IsValid())
		{
			CS3_Warning(TEXT("AppCmpt.Error::CreateRiderPet:LoadAssetPathCallBack *this is error!"));
			return;
		}
		URoleAppearanceComponent* ThisPtr = DelayThisPtr.Get();

		TMap<MODEL_PART_TYPE, FString> PetPartDataMap = ThisPtr->GetPartDataMapByModelNumber(ThisPtr->CurCreateAppData.RidePetModelId);
		ThisPtr->ApplayModelByPartsMap(PetPartDataMap);

		TMap<MODEL_PART_TYPE, FString> RiderPartDataMap;
		ThisPtr->CreatePartMapByServer(RiderPartDataMap);
		RiderCharacter->ApplayModelByPartsMap(RiderPartDataMap);
	});
	return true;
}

void URoleAppearanceComponent::OnChangeActorPartLoadCompleted(MODEL_PART_TYPE PartType, const FMODEL_PART_DATA* pPartData)
{
	SCOPE_CYCLE_COUNTER(STAT_OnChangeActorPartLoadCompleted);
	if (CheckIsVaildPart(PartType, pPartData->RowName.ToString()))
	{
		UObject* mesh = pPartData->ModelPartPath.Get();
		if (IsValid(mesh))
		{
			AddActorPart(PartType, *pPartData);
		}
		else
		{
			CancelActorPart(PartType);
		}
		OnChangePartOver();
	}
}

FRIDER_MODEL_ANIM_DATA* URoleAppearanceComponent::GetRideModelAnimDataFromCfg(
	RIDE_POSTURE_ENUM InPetProfession,ROLE_PROFESSION_ENUM InRoleProfession, 
	ROLE_GENDER_ENUM InRoleGender)
{
	SCOPE_CYCLE_COUNTER(STAT_GetRideModelAnimDataFromCfg);
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UDataTable* TableData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_RIDE_ANIM_DATA)->GetBaseTable();
	for (auto it : TableData->GetRowMap())
	{
		FRIDER_MODEL_ANIM_DATA* RiderModelAnimData = (FRIDER_MODEL_ANIM_DATA*)it.Value;
		if (RiderModelAnimData->RidePosture == InPetProfession &&
			RiderModelAnimData->RiderProfession == InRoleProfession &&
			RiderModelAnimData->RiderGender == InRoleGender)
		{
			return RiderModelAnimData;
		}
	}
	return nullptr;
}

TSharedPtr<FMODEL_DATA>  URoleAppearanceComponent::GetRoleModelData(FString InRoleModelNumber)
{
	SCOPE_CYCLE_COUNTER(STAT_GetRoleModelData);
	TSharedPtr<FMODEL_DATA> RoleModelData;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.MODEL_DATA.GetRoleModelData(ModelId=%s)"), *InRoleModelNumber);
	if (InRoleModelNumber.IsEmpty())
	{
		const FMODEL_DATA* ModelData = GetModelDataByRoleCreateUiCfg();
		if (!ModelData)
		{
			RoleModelData = MakeShareable(new FMODEL_DATA());
		}
		else
		{
			RoleModelData = MakeShareable(new FMODEL_DATA(*ModelData));
		}
	}
	else
	{
		RoleModelData = MakeShareable(new FMODEL_DATA(*GetModelDataFromCfg(InRoleModelNumber)));
	}
	return RoleModelData;
}

const FMODEL_DATA* URoleAppearanceComponent::GetModelDataByRoleCreateUiCfg()
{
	int32 RowIndex = CurCreateAppData.RoleProfession;
	if (CurCreateAppData.RoleGender == 2)//女性
	{
		RowIndex += 4;
	}
	if (CurCreateAppData.RoleCamp == 2)//阵营为魔
	{
		RowIndex += 8;
	}
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	auto RoleTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_CREATE);
	const FRoleCreateUIData* RoleDefaultData = RoleTable->GetRow<FRoleCreateUIData>(FString::FromInt(RowIndex));
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AppCmpt.MODEL_DATA.GetModelDataByRoleCreateUiCfg(ModelId=%d)"), RowIndex);
	if (RoleDefaultData != nullptr)
	{
		const FMODEL_DATA* pModelData = GetModelDataFromCfg(RoleDefaultData->RoleGameModelName.ToString());
		return pModelData;
	}
	return nullptr;
}

CONTROL_COMPILE_OPTIMIZE_END
