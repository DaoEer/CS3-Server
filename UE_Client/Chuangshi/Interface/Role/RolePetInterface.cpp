// Fill out your copyright notice in the Description page of Project Settings.

#include "RolePetInterface.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Kismet/KismetMathLibrary.h"
#include "GameData/TexturePath.h"
#include "GameData/PetData.h"
#include "GameData/ConstData.h"
#include "Manager/ResourceManager.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Pet/OriginPetCharacter.h"
#include "Manager/MessageManager.h"
#include "Component/Role/RideCarrierComponent.h"
#include "Manager/SkillManager.h"   
#include "Actor/Pet/PetCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "RoleKitBagInterface.h"
#include "RoleLunHuiMiJinInterface.h"
#include "Manager/MessageManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "Blueprint/AIBlueprintHelperLibrary.h"


CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URolePetInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_addOriginPet, &URolePetInterface::CLIENT_addOriginPet, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(PetAddData, &URolePetInterface::PetAddData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnGetSealPetEggAttr, &URolePetInterface::OnGetSealPetEggAttr, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnGeneratePet, &URolePetInterface::OnGeneratePet, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnActivePetEnterFence, &URolePetInterface::CLIENT_OnActivePetEnterFence, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnExChangePetFromFence, &URolePetInterface::CLIENT_OnExChangePetFromFence, const FString&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_showOriginPetModel, &URolePetInterface::CLIENT_showOriginPetModel, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnAddOriginPetModel, &URolePetInterface::CLIENT_OnAddOriginPetModel, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRemoveOriginPetModel, &URolePetInterface::CLIENT_OnRemoveOriginPetModel, const int8&, const uint8&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnExChangeOriginPetModel, &URolePetInterface::CLIENT_OnExChangeOriginPetModel, const FVariant&, const int8&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(updateOriginPetEpitomeDatas, &URolePetInterface::updateOriginPetEpitomeDatas, FString&, FString&, FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnChangePetAI, &URolePetInterface::OnChangePetAI, FString)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnFinishChangePetAI, &URolePetInterface::OnFinishChangePetAI)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URolePetInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(carrierId, &URolePetInterface::Set_carrierId, FString)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URolePetInterface::URolePetInterface()
{

}

URolePetInterface::~URolePetInterface()
{

}

void URolePetInterface::OnOccypySpaceTypeChange(const LHMJ_SPACE_TYPE &_spaceType)
{
	spaceType = _spaceType;
}

void URolePetInterface::ActivePetEnterFence()
{
	if (!ActivityPetUID.IsEmpty())
	{
		KBEngine::FVariantArray args;
		CellCall(TEXT("CELL_activePetEnterFence"), args);
	}
	else
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(5510);
	}
}

void URolePetInterface::CLIENT_OnActivePetEnterFence(const FString& petUID)
{
	_CreateOriginPetByPetUID(petUID);

	PetRemoveData(petUID);
}

void URolePetInterface::CLIENT_addOriginPet(const FVariant& ORIGIN_PET_DATA_1)
{
	_CreateOriginPet(ORIGIN_PET_DATA_1);

}

void URolePetInterface::CLIENT_showOriginPetModel(const FVariant& _OriginPetDatas)
{
	ORIGIN_PET_CLIENT_SIMPLE_DATA_LIST datas(_OriginPetDatas);
	for (auto data : datas.dictDatas1)
	{
		int32 Index = data.index;
		if (ORIGIN_PET_SPAWN_POS.Num() < Index)return;
		UClass *petClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_OriginPetCharacter"));
		AOriginPetCharacter* PetCharacter = Cast<AOriginPetCharacter>(UGolbalBPFunctionLibrary::SpawnActor<AActor>(petClass, ORIGIN_PET_SPAWN_POS[Index]));
		if (IsValid(PetCharacter))
		{
			PetCharacter->InitOriginPet(data);
			OriginPetCharacters.Add(Index, PetCharacter);
		}
	}
}

void URolePetInterface::CLIENT_OnAddOriginPetModel(const FVariant& _OriginPetData)
{
	ORIGIN_PET_CLIENT_SIMPLE_DATA data(_OriginPetData);
	int32 Index = data.index;
	if (ORIGIN_PET_SPAWN_POS.Num() < Index)return;
	UClass *petClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_OriginPetCharacter"));
	AOriginPetCharacter* PetCharacter = Cast<AOriginPetCharacter>(UGolbalBPFunctionLibrary::SpawnActor<AActor>(petClass, ORIGIN_PET_SPAWN_POS[Index]));
	if (IsValid(PetCharacter))
	{
		PetCharacter->InitOriginPet(data);
		OriginPetCharacters.Add(Index, PetCharacter);
	}
}

void URolePetInterface::CLIENT_OnRemoveOriginPetModel(const int8& Index, const uint8& DirectDel)
{
	int32 petIndex(Index);
	if (OriginPetCharacters.Contains(petIndex))
	{
		auto pet = OriginPetCharacters[petIndex];
		OriginPetCharacters.Remove(petIndex);
		if (DirectDel)
		{
			pet->Destroy();
		}
		else
		{
			pet->MoveLeaveBeforeDestroy();
		}
		
		
	}
}

void URolePetInterface::CLIENT_OnExChangeOriginPetModel(const FVariant& _OriginPetData, const int8& Index)
{
	CLIENT_OnRemoveOriginPetModel(Index, 1);
	CLIENT_OnAddOriginPetModel(_OriginPetData);
}

void URolePetInterface::FreePetFromFence(const FString & UID)
{
	TWeakObjectPtr<URolePetInterface> DelayThisPtr(this);
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(2015,"", FBtnClick::CreateLambda([DelayThisPtr,UID](RT_BTN_TYPE BtnType)
	{
		if (DelayThisPtr.IsValid())
		{
			URolePetInterface* ThisPtr = DelayThisPtr.Get();
			if (IsValid(ThisPtr))
			{
				if (BtnType == RT_BTN_TYPE::RT_OK)
				{
					KBEngine::FVariantArray args;
					args.Add(UID);
					ThisPtr->CellCall(TEXT("CELL_freePetFromFence"), args);
				}
			}
		}
	}));
	
}

void URolePetInterface::CLIENT_OnFreePetFromFence_Implementation(const FString& UID)
{
	if (OriginPetDatas.Contains(UID))
	{
		OriginPetDatas.Remove(UID);

	}
}

void URolePetInterface::GetOriginPetEgg(TArray<FString>& UIds)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifyCrystal : kitbatInst!"));
		return;
	}
	TArray<UItemBase*> itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemOriginPetEgg"));
	TArray<int32> tempItemIDs;
	for (auto item : itemList)
	{
		if (!tempItemIDs.Contains(item->ItemID))//相同的物品ID不同的UID不重新输出
		{
			tempItemIDs.Add(item->ItemID);
			UIds.Add(item->UID);
		}
	}
}

void URolePetInterface::GetPetFoodByType(const FString& UID, TArray<FString>& UIds)
{
	if (OriginPetDatas.Contains(UID))
	{
		URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
		if (!IsValid(kitbatInst))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifyCrystal : kitbatInst!"));
			return;
		}
		FString foodType = INT_TO_FSTRING(OriginPetDatas[UID]->foodType);
		TArray<UItemBase*> itemList;
		if (OriginPetDatas[UID]->wildness > 0)			// 还存在野性，只能驯养
		{
			itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemPetFood"));
		}
		else
		{
			itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemPetExpFood"));
		}
		FString petQuality(INT_TO_FSTRING(OriginPetDatas[UID]->quality));
		for (auto item_ : itemList)
		{
			//原兽品质及食材需求等级限制
			TArray<FString> petQualityArr = UGolbalBPFunctionLibrary::SplitString(item_->Param2);
			AServerCharacter* player = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			if (!petQualityArr.Contains(petQuality) || !item_->CheckLevel(player))
			{
				continue;
			}
			// 0 是通用食材
			if (item_->Param3.Equals(foodType) || item_->Param3.Equals("0"))
			{
				UIds.Add(item_->UID);
			}
		}
	}
}

void URolePetInterface::FeedPetItemFood(const FString & UID, const int32 & ItemID, const int32& Num)
{
	if (OriginPetDatas.Contains(UID))
	{
		KBEngine::FVariantArray args;
		args.Add(UID);
		args.Add(OriginPetDatas[UID]->quality);
		args.Add(ItemID);
		args.Add(Num);
		CellCall(TEXT("CELL_feedOriginPet"), args);
	}
	
}

void URolePetInterface::GenerateOriginPet(const int32 & ItemID)
{
	KBEngine::FVariantArray args;
	args.Add(ItemID);
	CellCall(TEXT("generateOriginPet"), args);
}

void URolePetInterface::CLIENT_OnFeedPetWildness_Implementation(const FString & UID, const int32 & CurWildness, const FString& CDEndTime)
{
	if (OriginPetDatas.Contains(UID))
	{
		auto petData = OriginPetDatas[UID];
		int32 oldWildness = petData->wildness;
		petData->wildness = CurWildness;
		petData->sleepTime = CDEndTime;
		OnFeedPetStartBP(UID, CDEndTime, petData->step);
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(2016, petData->GetName() + "|" + INT_TO_FSTRING(oldWildness-CurWildness) );
		//喂食成功动画提示
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
		{
			UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("FeedSuccess"));
		}

		for (auto it = OriginPetCharacters.CreateConstIterator(); it; ++it)
		{
			if (it.Value()->UID.Equals(UID))
			{
				it.Value()->PlayAction("Show_01");
				break;
			}
		}
	}
}

void URolePetInterface::CLIENT_OnFeedPetExp_Implementation(const FString & UID, const int32& Step, const int32 & CurExp, const FString& CDEndTime)
{
	if (OriginPetDatas.Contains(UID))
	{
		auto petData = OriginPetDatas[UID];
		petData->step = Step;
		petData->exp = CurExp;
		petData->sleepTime = CDEndTime;
		OnFeedPetStartBP(UID, CDEndTime, petData->step);
		//喂食成功动画提示
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
		{
			UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("FeedSuccess"));
		}

		for (auto it = OriginPetCharacters.CreateConstIterator(); it; ++it)
		{
			if (it.Value()->UID.Equals(UID))
			{
				it.Value()->PlayAction("Show_02");
				break;
			}
		}
	}
}

void URolePetInterface::CLIENT_clearPetCDTime()
{
	for (auto It = OriginPetDatas.CreateConstIterator(); It; ++It)
	{
		It.Value()->sleepTime = TEXT("0");
		OnFeedPetStartBP(It.Value()->uid, TEXT("0"),It.Value()->step);
	}
}

void URolePetInterface::EvolutionOriginPet(const FString & UID)
{
	KBEngine::FVariantArray args;
	args.Add(UID);
	CellCall(TEXT("CELL_evolutionOriginPet"), args);
}

void URolePetInterface::CLIENT_onEvolutionPet_Implementation(const FString & UID)
{
	if (OriginPetDatas.Contains(UID))
	{
		auto petData = OriginPetDatas[UID];
		petData->bEvolution = true;

		for (auto it = OriginPetCharacters.CreateConstIterator(); it; ++it)
		{
			auto pet = it.Value();
			if (IsValid(pet) && pet->UID.Equals(UID))
			{
				pet->ModelNumber = petData->ModelNumber;
				pet->CreateAppearance();
				FVector modelScale(petData->ModelScale, petData->ModelScale, petData->ModelScale);
				pet->SetActorScale3D(modelScale);
				break;
			}
		}
		//进化成功动画提示
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
		{
			UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("EvolutionSuccess"));
		}
	}
}

void URolePetInterface::PetOutsideFromFence(const FString & UID)
{
	if (OriginPetDatas.Contains(UID))
	{
		FDateTime cdtime_ = UGolbalBPFunctionLibrary::FromServerStrTimeToClientTime(OriginPetDatas[UID]->sleepTime);
		if (FDateTime::Now() < cdtime_)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(2019);
			return;
		}
		KBEngine::FVariantArray args;
		args.Add(UID);
		args.Add(OriginPetDatas[UID]->scriptID);
		CellCall(TEXT("CELL_PetOutsideFromFence"), args);
	}
	
}

void URolePetInterface::CLIENT_OnPetOutsideFromFence_Implementation(const FString & UID)
{
	if (OriginPetDatas.Contains(UID))
	{
		auto PetData = Cast<UPetEpitome>(OriginPetDatas.FindAndRemoveChecked(UID));
		PetData->sleepTime.Empty();
		Pets.Add(UID, PetData);
		int32 index = Pets.Num() - 1;
		OnAddPetBP(index, PetData, false);
	}
}

void URolePetInterface::CLIENT_OnExChangePetFromFence(const FString& EnterUID, const FString& LeaveUID)
{
	CLIENT_OnPetOutsideFromFence(LeaveUID);
	CLIENT_OnActivePetEnterFence(EnterUID);
}

UOriginPetEpitome* URolePetInterface::GetOriginPetByUId(const FString& UID)
{
	if (OriginPetDatas.Contains(UID))
	{
		return OriginPetDatas[UID];
	}
	return nullptr;
}

bool URolePetInterface::IsHunger(const FString& UID)
{
	//此功能未制作，提供接口
	return false;
}

void URolePetInterface::Set_carrierId(const FString & newVal, const FString & oldVal)
{
	//FString RideCarrierId = UGolbalBPFunctionLibrary::GetEntityPropertyValue(EntityID, TEXT("CarrierId"));

	AActor* _actor = GetActor();
	APlayerCharacter* player = Cast<APlayerCharacter>(_actor);
	if (!IsValid(player) || !player->IsInitialized())
	{
		return;
	}

	if (player->ActorIsPlayer())
	{
		if (newVal.IsEmpty())
		{
			OnPetRiderStateChangedBP(0);
		}
		else
		{
			OnPetRiderStateChangedBP(1);
		}
	}
	if (newVal == oldVal) return;

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("player(id:%d) Set_carrierId change(RideCarrierId:%s)"), EntityID, *newVal);
	if (newVal.IsEmpty() && !oldVal.IsEmpty())
	{
		player->RideCarrierComponent->DisRideOnPet();
	}
	else if (!newVal.IsEmpty())
	{
		player->RideCarrierComponent->RideOnPet(newVal);
	}
}

void URolePetInterface::_CreateOriginPet(FORIGIN_PET_DATA data)
{
	UOriginPetEpitome* OriginPet = NewObject<UOriginPetEpitome>();
	OriginPet->uid = INT64_TO_FSTRING(data.uid1);
	OriginPet->scriptID = data.scriptID2;
	OriginPet->uname = data.uname4;
	OriginPet->exp = data.exp6;
	OriginPet->ability = data.ability9;
	OriginPet->ability_Max = data.ability_Max10;
	OriginPet->quality = data.quality12;
	OriginPet->step = data.step11;
	OriginPet->bEvolution = (data.bEvolution == 1);
	OriginPet->HP = data.HP27;
	OriginPet->MP = data.MP28;
	OriginPet->sleepTime = INT64_TO_FSTRING(data.sleepTime16);
	OriginPet->wildness = data.wildness17;
	OriginPet->corporeity = data.corporeity22;
	OriginPet->strength = data.strength23;
	OriginPet->intellect = data.intellect24;
	OriginPet->discern = data.discern25;
	OriginPet->dexterity = data.dexterity26;
	OriginPet->HP_Max = data.HP_Max29;
	OriginPet->MP_Max = data.MP_Max30;
	OriginPet->damage = data.damage31;
	OriginPet->magic_damage = data.magic_damage32;
	OriginPet->armor = data.armor33;
	OriginPet->magic_armor = data.magic_armor34;
	OriginPet->criticalstrike = data.criticalstrike35;
	OriginPet->parry = data.parry36;
	OriginPet->speed = data.speed37;
	OriginPet->hitrate = data.hitrate38;
	OriginPet->dodgerate = data.dodgerate39;
	OriginPet->gangQiValue = data.gangQiValue40;
	OriginPet->gangQiValue_Max = data.gangQiValue_Max41;
	OriginPet->gangQi_damagePoint = data.gangQi_damagePoint43;
	OriginPet->gangQi_armorPoint = data.gangQi_armorPoint44;
	OriginPet->gangQi_armorPoint = data.gangQi_armorPoint44;
	OriginPet->gangQi_armorPoint = data.gangQi_armorPoint44;
	OriginPet->gangQi_armorPoint = data.gangQi_armorPoint44;
	OriginPet->attrSkillBox = data.attrSkillBox13;
	OriginPet->passiveSkillBox = data.passiveSkillBox14;
	OriginPet->noLearnedSkillBox = data.noLearnedSkillBox15;
	OriginPet->combatPower = data.combatPower47;
	OriginPet->cure = data.cure48;

	OriginPet->ice_damage = data.ice_damage;
	OriginPet->fire_damage = data.fire_damage;
	OriginPet->thunder_damage = data.thunder_damage;
	OriginPet->xuan_damage = data.xuan_damage;
	OriginPet->ice_armor = data.ice_armor;
	OriginPet->fire_armor = data.fire_armor;
	OriginPet->thunder_armor = data.thunder_armor;
	OriginPet->xuan_armor = data.xuan_armor;

	OriginPet->damage_ignore = data.damage_ignore;
	OriginPet->magic_damage_ignore = data.magic_damage_ignore;
	OriginPet->armor_ignore = data.armor_ignore;
	OriginPet->magic_armor_ignore = data.magic_armor_ignore;
	OriginPet->criticalstrike_ignore = data.criticalstrike_ignore;
	OriginPet->parry_ignore = data.parry_ignore;
	OriginPet->hitrate_ignore = data.hitrate_ignore;
	OriginPet->dodgerate_ignore = data.dodgerate_ignore;

	OriginPet->ice_damage_ignore = data.ice_damage_ignore;
	OriginPet->fire_damage_ignore = data.fire_damage_ignore;
	OriginPet->thunder_damage_ignore = data.thunder_damage_ignore;
	OriginPet->xuan_damage_ignore = data.xuan_damage_ignore;
	OriginPet->ice_armor_ignore = data.ice_armor_ignore;
	OriginPet->fire_armor_ignore = data.fire_armor_ignore;
	OriginPet->thunder_armor_ignore = data.thunder_armor_ignore;
	OriginPet->xuan_armor = data.xuan_armor;

	OriginPet->depress_resist = data.depress_resist;
	OriginPet->hitback_resist = data.hitback_resist;
	OriginPet->control_resist = data.control_resist;
	OriginPet->insane_resist = data.insane_resist;

	// 客户端配置
	const UConfigTable* ConfigTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET);
	if (ConfigTable)
	{
		const FPET_DATA* petData = ConfigTable->GetRow<FPET_DATA>(data.scriptID2);
		if (petData != nullptr)
		{
			OriginPet->ModelNumber = petData->ModelNumber;
			OriginPet->ModelScale = petData->ModelScale;
			OriginPet->OriginModelNumber = petData->OriginModelNumber;
			OriginPet->OriginModelScale = petData->OriginModelScale;
			OriginPet->profession = int(petData->profession);
			OriginPet->race = petData->race;
			OriginPet->takeLevel = petData->takeLevel;
			OriginPet->combatType = petData->combatType;
			OriginPet->icon = petData->icon;
			OriginPet->foodType = petData->foodType;
		}
	}
	OriginPetDatas.Add(OriginPet->uid, OriginPet);
	OnAddOriginPetBP(OriginPetDatas.Num()-1, OriginPet->uid);
}

void URolePetInterface::_CreateOriginPetByPetUID(const FString& UID)
{
	if (Pets.Contains(UID))
	{
		UPetEpitome* pet = Pets[UID];
		UOriginPetEpitome* OriginPet = NewObject<UOriginPetEpitome>();
		OriginPet->uid = pet->uid;
		OriginPet->scriptID = pet->scriptID;
		OriginPet->uname = pet->uname;
		OriginPet->exp = pet->exp;
		OriginPet->ability = pet->ability;
		OriginPet->ability_Max = pet->ability_Max;
		OriginPet->quality = pet->quality;
		OriginPet->step = pet->step;
		OriginPet->bEvolution = 1;
		OriginPet->HP = pet->HP;
		OriginPet->MP = pet->MP;
		OriginPet->sleepTime = pet->sleepTime;
		OriginPet->wildness = 0;
		OriginPet->corporeity = pet->corporeity;
		OriginPet->strength = pet->strength;
		OriginPet->intellect = pet->intellect;
		OriginPet->discern = pet->discern;
		OriginPet->dexterity = pet->dexterity;
		OriginPet->HP_Max = pet->HP_Max;
		OriginPet->MP_Max = pet->MP_Max;
		OriginPet->damage = pet->damage;
		OriginPet->magic_damage = pet->magic_damage;
		OriginPet->armor = pet->armor;
		OriginPet->magic_armor = pet->magic_armor;
		OriginPet->criticalstrike = pet->criticalstrike;
		OriginPet->parry = pet->parry;
		OriginPet->speed = pet->speed;
		OriginPet->hitrate = pet->hitrate;
		OriginPet->dodgerate = pet->dodgerate;
		OriginPet->gangQiValue = pet->gangQiValue;
		OriginPet->gangQiValue_Max = pet->gangQiValue_Max;
		OriginPet->gangQi_damagePoint = pet->gangQi_damagePoint;
		OriginPet->gangQi_armorPoint = pet->gangQi_armorPoint;
		OriginPet->gangQi_armorPoint = pet->gangQi_armorPoint;
		OriginPet->gangQi_armorPoint = pet->gangQi_armorPoint;
		OriginPet->gangQi_armorPoint = pet->gangQi_armorPoint;
		OriginPet->attrSkillBox = pet->attrSkillBox;
		OriginPet->passiveSkillBox = pet->passiveSkillBox;
		OriginPet->noLearnedSkillBox = pet->noLearnedSkillBox;
		OriginPet->combatPower = pet->combatPower;
		OriginPet->cure = pet->cure;
		// 客户端配置
		const UConfigTable* ConfigTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET);
		if (ConfigTable)
		{
			const FPET_DATA* petData = ConfigTable->GetRow<FPET_DATA>(pet->scriptID);
			if (petData != nullptr)
			{
				OriginPet->ModelNumber = petData->ModelNumber;
				OriginPet->ModelScale = petData->ModelScale;
				OriginPet->OriginModelNumber = petData->OriginModelNumber;
				OriginPet->OriginModelScale = petData->OriginModelScale;
				OriginPet->profession = int(petData->profession);
				OriginPet->race = petData->race;
				OriginPet->takeLevel = petData->takeLevel;
				OriginPet->combatType = petData->combatType;
				OriginPet->icon = petData->icon;
				OriginPet->foodType = petData->foodType;
			}
		}
		OriginPetDatas.Add(OriginPet->uid, OriginPet);
		OnAddOriginPetBP(OriginPetDatas.Num() - 1, OriginPet->uid);
	}
}

void URolePetInterface::OnRep_petCageMax()
{
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	OnPetCageMaxChangedBP( UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, TEXT("petCageMax")) );
}

void URolePetInterface::PetAddData(const FVariant& var)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("Add Pet->%s"),*JsonStr);
	UPetEpitome* Pet = AnalyzePetJsonStr(var);

	Pets.Add(Pet->uid, Pet);
	int32 index = Pets.Num()-1;
	OnAddPetBP(index, Pet, false);
}

void URolePetInterface::PetRemoveData(const FString& UID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Remove Pet--------------------------------------->>>%s"), *UID);
	
	if (Pets.Contains(UID))
	{
		Pets.Remove(UID);
		OnRemovePetBP(UID);
	}
}

void URolePetInterface::CLIENT_OnSetActivePetExp_Implementation(const int32& CurExp)
{
	if (Pets.Contains(ActivityPetUID))
	{
		Pets[ActivityPetUID]->exp = CurExp;
	}
}

void URolePetInterface::OnGeneratePet(const FVariant& var)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("Generate Pet->%s"), *JsonStr);
	UPetEpitome* Pet = AnalyzePetJsonStr(var);

	Pets.Add(Pet->uid, Pet);
	int32 index = Pets.Num() - 1;
	OnAddPetBP(index, Pet, true);
	UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("PetHatchSuccess"));

}

void URolePetInterface::OnGetSealPetEggAttr(const FVariant& Variantdata)
{
	FClientSealPetData Pet = VarToClientSealPetData( Variantdata);
	OnGetSealPetEggAttrTo(Pet);
}
void URolePetInterface::OnGetSealPetEggAttrTo_Implementation(const FClientSealPetData& Pet)
{

}
FClientSealPetData URolePetInterface::VarToClientSealPetData(const FVariant& Variantdata)
{
	PET_PERSISTENT_DATA data = PET_PERSISTENT_DATA(Variantdata);
	FClientSealPetData SealPet;
	SealPet.scriptID = data.scriptID;
	SealPet.ability= data.ability;
	SealPet.ability_Max = data.ability_Max;
	SealPet.quality = data.quality;
	SealPet.step = data.step;
	SealPet.exp = data.exp;
	SealPet.name = data.name;
	SealPet.HP = data.HP;
	SealPet.MP = data.MP;

	for (auto skill : data.attrSkillBox)
	{
		SealPet.attrSkillBox.Add(skill);
	}
	for (auto skill : data.passiveSkillBox)
	{
		SealPet.passiveSkillBox.Add(skill);
	}
	for (auto skill : data.noLearnedSkillBox)
	{
		SealPet.noLearnedSkillBox.Add(skill);
	}
	SealPet.corporeity = data.corporeity;
	SealPet.strength = data.strength;
	SealPet.intellect = data.intellect;
	SealPet.discern = data.discern;
	SealPet.dexterity = data.dexterity;
	SealPet.HP_Max = data.HP_Max;
	SealPet.MP_Max = data.MP_Max;
	SealPet.damage = data.damage;
	SealPet.magic_damage = data.magic_damage;
	SealPet.armor = data.armor;
	SealPet.magic_armor = data.magic_armor;
	SealPet.criticalstrike = data.criticalstrike;
	SealPet.parry = data.parry;
	SealPet.speed = data.speed;
	SealPet.hitrate = data.hitrate;
	SealPet.dodgerate = data.dodgerate;
	SealPet.gangQiValue = data.gangQiValue;
	SealPet.gangQiValue_Max = data.gangQiValue_Max;
	SealPet.gangQi_damagePoint = data.gangQi_damagePoint;
	SealPet.gangQi_armorPoint = data.gangQi_armorPoint;
	SealPet.cure = data.cure;
	SealPet.ice_damage = data.ice_damage;
	SealPet.fire_damage = data.fire_damage;
	SealPet.thunder_damage = data.thunder_damage;
	SealPet.xuan_damage = data.xuan_damage;
	SealPet.ice_armor = data.ice_armor;
	SealPet.fire_armor = data.fire_armor;
	SealPet.thunder_armor = data.thunder_armor;
	SealPet.xuan_armor = data.xuan_armor;

	SealPet.damage_ignore = data.damage_ignore;
	SealPet.magic_damage_ignore = data.magic_damage_ignore;
	SealPet.armor_ignore = data.armor_ignore;
	SealPet.magic_armor_ignore = data.magic_armor_ignore;
	SealPet.criticalstrike_ignore = data.criticalstrike_ignore;
	SealPet.parry_ignore = data.parry_ignore;
	SealPet.hitrate_ignore = data.hitrate_ignore;
	SealPet.dodgerate_ignore = data.dodgerate_ignore;

	SealPet.ice_damage_ignore = data.ice_damage_ignore;
	SealPet.fire_damage_ignore = data.fire_damage_ignore;
	SealPet.thunder_damage_ignore = data.thunder_damage_ignore;
	SealPet.xuan_damage_ignore = data.xuan_damage_ignore;
	SealPet.ice_armor_ignore = data.ice_armor_ignore;
	SealPet.fire_armor_ignore = data.fire_armor_ignore;
	SealPet.thunder_armor_ignore = data.thunder_armor_ignore;
	SealPet.xuan_armor = data.xuan_armor;

	SealPet.depress_resist = data.depress_resist;
	SealPet.hitback_resist = data.hitback_resist;
	SealPet.control_resist = data.control_resist;
	SealPet.insane_resist = data.insane_resist;
	return SealPet;
}

UPetEpitome* URolePetInterface::AnalyzePetJsonStr(const FVariant& Variantdata)
{
	PET_PERSISTENT_DATA data = PET_PERSISTENT_DATA(Variantdata);
	UPetEpitome* Pet = NewObject<UPetEpitome>();
	char charUid[21];
	sprintf_s(charUid, "%llu", data.uid);
	Pet->uid = charUid;
	Pet->scriptID = data.scriptID;
	Pet->ability = data.ability;	
	Pet->ability_Max = data.ability_Max;
	Pet->quality = data.quality;
	Pet->step = data.step;
	Pet->exp = data.exp;
	Pet->name = data.name;
	Pet->HP = data.HP;
	Pet->MP = data.MP;
	char charSleepTime[21];
	sprintf_s(charSleepTime, "%llu", data.sleepTime);
	Pet->sleepTime = charSleepTime;

	for (auto skill : data.attrSkillBox)
	{
		Pet->attrSkillBox.Add(skill);
	}
	for (auto skill : data.passiveSkillBox)
	{
		Pet->passiveSkillBox.Add(skill);
	}
	for (auto skill : data.noLearnedSkillBox)
	{
		Pet->noLearnedSkillBox.Add(skill);
	}
	Pet->corporeity = data.corporeity;
	Pet->strength = data.strength;
	Pet->intellect = data.intellect;
	Pet->discern = data.discern;
	Pet->dexterity = data.dexterity;
	Pet->HP_Max = data.HP_Max;
	Pet->MP_Max = data.MP_Max;
	Pet->damage = data.damage;
	Pet->magic_damage = data.magic_damage;
	Pet->armor = data.armor;
	Pet->magic_armor = data.magic_armor;
	Pet->criticalstrike = data.criticalstrike;
	Pet->parry = data.parry;
	Pet->speed = data.speed;
	Pet->hitrate = data.hitrate;
	Pet->dodgerate = data.dodgerate;
	Pet->gangQiValue = data.gangQiValue;
	Pet->gangQiValue_Max = data.gangQiValue_Max;
	Pet->gangQi_damagePoint = data.gangQi_damagePoint;
	Pet->gangQi_armorPoint = data.gangQi_armorPoint;
	Pet->combatPower = data.combatPower;
	Pet->ice_damage = data.ice_damage;
	Pet->fire_damage = data.fire_damage;
	Pet->thunder_damage = data.thunder_damage;
	Pet->xuan_damage = data.xuan_damage;
	Pet->ice_armor = data.ice_armor;
	Pet->fire_armor = data.fire_armor;
	Pet->thunder_armor = data.thunder_armor;
	Pet->xuan_armor = data.xuan_armor;

	Pet->damage_ignore = data.damage_ignore;
	Pet->magic_damage_ignore = data.magic_damage_ignore;
	Pet->armor_ignore = data.armor_ignore;
	Pet->magic_armor_ignore = data.magic_armor_ignore;
	Pet->criticalstrike_ignore = data.criticalstrike_ignore;
	Pet->parry_ignore = data.parry_ignore;
	Pet->hitrate_ignore = data.hitrate_ignore;
	Pet->dodgerate_ignore = data.dodgerate_ignore;

	Pet->ice_damage_ignore = data.ice_damage_ignore;
	Pet->fire_damage_ignore = data.fire_damage_ignore;
	Pet->thunder_damage_ignore = data.thunder_damage_ignore;
	Pet->xuan_damage_ignore = data.xuan_damage_ignore;
	Pet->ice_armor_ignore = data.ice_armor_ignore;
	Pet->fire_armor_ignore = data.fire_armor_ignore;
	Pet->thunder_armor_ignore = data.thunder_armor_ignore;
	Pet->xuan_armor = data.xuan_armor;

	Pet->depress_resist = data.depress_resist;
	Pet->hitback_resist = data.hitback_resist;
	Pet->control_resist = data.control_resist;
	Pet->insane_resist = data.insane_resist;

	TArray<int32>TempShenTongSKillList;
	for (auto i : data.petShenTongSKill)
	{
		Pet->petShenTongSKill.Add(i.key1, i.value2);
		TempShenTongSKillList.Add(i.key1);
	}
	for (int32 i = 0; i < TempShenTongSKillList.Num(); ++i)
	{
		Pet->petShenTongSKillList.Add(TempShenTongSKillList[TempShenTongSKillList.Num() - 1 - i]);
	}
	const UConfigTable* ConfigTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET);
	if (ConfigTable)
	{
		const FPET_DATA* petData = ConfigTable->GetRow<FPET_DATA>(Pet->scriptID);
		if (petData != nullptr)
		{
			Pet->uname = petData->Uname;
			Pet->profession = (int32)petData->profession;
			Pet->race = petData->race;
			Pet->takeLevel = petData->takeLevel;
			Pet->combatType = petData->combatType;
			Pet->icon = petData->icon;
			Pet->RidePosture = petData->RidePosture;
			FString Skills;
			if (Pet->quality == 1)
				Skills = petData->Skills_1;
			else if (Pet->quality == 2)
				Skills = petData->Skills_2;
			else if (Pet->quality == 3)
				Skills = petData->Skills_3;
			else if (Pet->quality == 4)
				Skills = petData->Skills_4;
			else if (Pet->quality == 5)
				Skills = petData->Skills_5;
			TArray<FString> SkillList = UGolbalBPFunctionLibrary::SplitString(Skills);
			for (auto IT : SkillList)
			{
				TArray<FString> SkillIDs = UGolbalBPFunctionLibrary::SplitString(IT, false, TEXT(":"));
				if (SkillIDs.Num() == 2)
				{
					Pet->skills.Add(FSTRING_TO_INT(SkillIDs[0]), FSTRING_TO_INT(SkillIDs[1]));
				}
				else
				{
					CS3_Warning(TEXT("Pet(script:%s,quality:%d) ConfigTable skill is error!!"), *Pet->scriptID, Pet->quality);
				}
			}
		}
		else
		{
			CS3_Warning(TEXT("Pet(%s) can find the config from PetTable!"), *Pet->scriptID);
		}
	}
	return Pet;
}

void URolePetInterface::updatePetEpitomeDatas(FString& UID, FString& attrName, FString& value)
{
	if (Pets.Contains(UID))
	{
		Pets[UID]->UpdateData(attrName, value);
		OnUpdatePetDatasBP(UID, attrName, value);
	}
}

void URolePetInterface::updateOriginPetEpitomeDatas(FString & UID, FString & attrName, FString & value)
{
	if (OriginPetDatas.Contains(UID))
	{
		OriginPetDatas[UID]->UpdateData(attrName, value);
		OnUpdatePetDatasBP(UID, attrName, value);
	}
}

UPetEpitome* URolePetInterface::GetPetByUID(const FString & UID)
{
	
	if (Pets.Contains(UID))
	{
		return Pets[UID];
	}
	return nullptr;
}

UTexture2D* URolePetInterface::GetIconByPetUID(const FString& UID)
{
	UPetEpitome* Pet = GetPetByUID(UID); 
	if (IsValid(Pet))
	{
		FString icon = Pet->icon;
		const UConfigTable* TextureTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET_HEAD_ICON_DATA);
		const FCS3TexturePath* textuerstruct = TextureTable->GetRow<FCS3TexturePath>(icon);
		if (textuerstruct)
		{
			if (IsValid(textuerstruct->TexturePath.Get()))
			{
				return textuerstruct->TexturePath.Get();
			}
			if (textuerstruct->TexturePath.ToSoftObjectPath().IsValid())
			{
				UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(textuerstruct->TexturePath.ToSoftObjectPath());
				return textuerstruct->TexturePath.Get();
			}
		} 
	}
	return nullptr;
}

UTexture2D* URolePetInterface::GetPetIconTexture(const FString& Icon)
{
	if (!Icon.IsEmpty())
	{
		const UConfigTable* TextureTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET_HEAD_ICON_DATA);
		const FCS3TexturePath* textuerstruct = TextureTable->GetRow<FCS3TexturePath>(Icon);
		if (textuerstruct)
		{
			if (IsValid(textuerstruct->TexturePath.Get()))
			{
				return textuerstruct->TexturePath.Get();
			}
			if (textuerstruct->TexturePath.ToSoftObjectPath().IsValid())
			{
				UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(textuerstruct->TexturePath.ToSoftObjectPath());
				return textuerstruct->TexturePath.Get();
			}
		}
	}
	return nullptr;
}

void URolePetInterface::onConjurePetResult(const FString& UID, const int32& PetEntityID)
{
	if (Pets.Contains(UID))
	{
		TArray<int32> skillBox = Pets[UID]->attrSkillBox;
		UUECS3GameInstance::Instance->SkillManager->InitActPetSkills(skillBox);
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		ActivityPetUID = UID;
		petEntityID = PetEntityID;
		PlayerCharacter->PetEntityId = PetEntityID;
		OnConjurePetResultBP(UID, PetEntityID);
	}
}

void URolePetInterface::onWithdrawPetResult()
{
	ActivityPetUID.Empty();
	petEntityID = 0;
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	PlayerCharacter->PetEntityId = 0;
	UUECS3GameInstance::Instance->SkillManager->RemoveActPetSkills();
	OnWithdrawPetResultBP();
}

PET_PROFESSION_ENUM URolePetInterface::GetPetProfessionByVehicleModelNum(const FString& VehicleModelNum)
{
	PET_PROFESSION_ENUM profession = PET_PROFESSION_ENUM::PET_PROFESSION_NULL;
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UDataTable* TableData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET)->GetBaseTable();
	for (auto it : TableData->GetRowMap())
	{
		FPET_DATA* PetData = (FPET_DATA*)it.Value;
		if (PetData->vehicleModelNum == VehicleModelNum)
		{
			profession = PetData->profession;
			break;
		}
	}
	return profession;
}

PET_PROFESSION_ENUM URolePetInterface::GetPetProfessionByScriptID(const FString& ScriptID)
{
	PET_PROFESSION_ENUM profession = PET_PROFESSION_ENUM::PET_PROFESSION_NULL;
	const UConfigTable* ConfigTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET);
	if (ConfigTable)
	{
		const FPET_DATA* petData = ConfigTable->GetRow<FPET_DATA>(ScriptID);
		if (petData != nullptr)
		{
			profession = petData->profession;
		}
	}
	return profession;
}

FString URolePetInterface::GetPetModelByScriptID(const FString& ScriptID)
{
	const UConfigTable* ConfigTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET);
	if (ConfigTable)
	{
		const FPET_DATA* petData = ConfigTable->GetRow<FPET_DATA>(ScriptID);
		if (petData != nullptr)
		{
			return petData->ModelNumber;
		}
	}
	return TEXT("");
}

FPET_MODEL_DATA URolePetInterface::GetPetModelTransformByModelID(const FString& ModelID)
{
	const UConfigTable* ConfigTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PET_MODEL_TRANSFORM);
	if (ConfigTable)
	{
		const FPET_MODEL_DATA* ModelData = ConfigTable->GetRow<FPET_MODEL_DATA>(ModelID);
		if (ModelData != nullptr)
		{
			return *ModelData;
		}
	}
	FPET_MODEL_DATA Data;
	return Data;
}

bool URolePetInterface::CheckIsOwn(FString ScriptID)
{
	for (TPair<FString, UPetEpitome*>& Pet : Pets)
	{
		if (Pet.Value->scriptID == ScriptID)
		{
			return true;
		}
	}
	return false;
}

void URolePetInterface::SortPetUId(const FString& ActivePetUId, const TArray<FString>& UIds)
{
	TArray<FString>& SrcUIds = const_cast<TArray<FString>&>(UIds);
	bool HasActivePet = false;
	TArray<FString> List = UIds;
	for (FString UId : List)
	{
		if (UId == ActivePetUId)
		{
			HasActivePet = true;
			SrcUIds.Remove(UId);
		}
		if (!GetPetByUID(UId))
		{
			SrcUIds.Remove(UId);
		}
	}
	SrcUIds.Sort([=](const FString& UId1, const FString& UId2) {
		UPetEpitome* Pet1 = GetPetByUID(UId1);
		UPetEpitome* Pet2 = GetPetByUID(UId2);
		if (Pet1->quality > Pet2->quality)
		{
			return true;
		}
		else if (Pet1->takeLevel > Pet2->takeLevel)
		{
			return true;
		}
		return Pet1->ability > Pet2->ability;
	});
	if (HasActivePet)
	{
		SrcUIds.Insert(ActivePetUId, 0);
	}
}

void URolePetInterface::OnPetReNameFail(const FString & UID, const int32 MessageID)
{
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(MessageID);
	FString PetName = GetPetByUID(UID)->GetName();
	OnPetReNameFailBP(UID, PetName);
}

void URolePetInterface::RequestPetAIChangeStateFC(const int32 State)
{
	//请求切换幻兽AI模式（客户端）
	KBEngine::Entity* PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetSelfEntity();
	if (PlayerEntity != nullptr)
	{
		int32 PetEntityId = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerEntity->ID(), TEXT("activePetID"));
		if (PetEntityId)
		{
			KBEngine::Entity* petEntity = UGolbalBPFunctionLibrary::FindEntity(PetEntityId);
			if (petEntity && petEntity->Actor())
			{
				APetCharacter* pet = Cast<APetCharacter>(petEntity->Actor());
				UBlackboardComponent* myBlackBoard = UAIBlueprintHelperLibrary::GetBlackboard(pet);
				if (IsValid(myBlackBoard))
				{
					myBlackBoard->SetValueAsEnum(FName(TEXT("AttackType")), State);
					VehiclePetSetAttackState(State);
				}
			}
		}
	}
	/*	//请求切换幻兽AI模式（服务器）
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RequestPetAIChangeStateFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(State);
	this->GetEntity()->CellCall(TEXT("CELL_petAIChangeState"), args);
	*/
}

void URolePetInterface::RequestPetAIChangeCommandFC(const int32 State)
{
	//请求切换幻兽AI命令（客户端）
	KBEngine::Entity* PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetSelfEntity();
	if (PlayerEntity != nullptr)
	{
		int32 PetEntityId = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerEntity->ID(), TEXT("activePetID"));
		if (PetEntityId)
		{
			KBEngine::Entity* petEntity = UGolbalBPFunctionLibrary::FindEntity(PetEntityId);
			if (petEntity && petEntity->Actor())
			{
				APetCharacter* pet = Cast<APetCharacter>(petEntity->Actor()); 
				UBlackboardComponent* myBlackBoard = UAIBlueprintHelperLibrary::GetBlackboard(pet);
				if (IsValid(myBlackBoard))
				{
					myBlackBoard->SetValueAsEnum(FName(TEXT("CurCommand")), State);
					myBlackBoard->SetValueAsObject(FName(TEXT("Target")), nullptr);
				}
			}
		}
	}
	/*	请求切换幻兽AI命令（服务器）
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RequestPetAIChangeCommandFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(State);
	this->GetEntity()->CellCall(TEXT("CELL_petAIChangeCommand"), args);
	*/
}

void URolePetInterface::RequestPetAIAttackTargetFC(const int32 SkillID, const int32 TargetID)
{
	//请求幻兽攻击命令（客户端）
	AServerCharacter* playerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(playerCharacter))return;
	KBEngine::Entity* PlayerEntity = playerCharacter->GetSelfEntity();
	if (PlayerEntity != nullptr)
	{
		int32 PetEntityId = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerEntity->ID(), TEXT("activePetID"));
		if (PetEntityId)
		{
			KBEngine::Entity* petEntity = UGolbalBPFunctionLibrary::FindEntity(PetEntityId);
			KBEngine::Entity* TargetEntity = UGolbalBPFunctionLibrary::FindEntity(TargetID);
			if (petEntity && TargetEntity && IsValid(TargetEntity->Actor()))
			{
				APetCharacter* pet = Cast<APetCharacter>(petEntity->Actor());
				AServerCharacter* target = Cast<AServerCharacter>(TargetEntity->Actor());
				if (playerCharacter->QueryRelation(target) != COMBAT_RELATION::COMBAT_RELATION_ENEMY)
				{
					UUECS3GameInstance::Instance->MessageManager->ShowMessage(1999);
					return;
				}
				if ((playerCharacter->GetActorLocation() - target->GetActorLocation()).Size() > 20 * 100)
				{
					UUECS3GameInstance::Instance->MessageManager->ShowMessage(2000);
					return;
				}

				UBlackboardComponent* myBlackBoard = UAIBlueprintHelperLibrary::GetBlackboard(pet);
				if (IsValid(myBlackBoard))
				{
					myBlackBoard->SetValueAsEnum(FName(TEXT("CurCommand")), 3);
					myBlackBoard->SetValueAsObject(FName(TEXT("Target")), target);
					myBlackBoard->SetValueAsInt(FName(TEXT("SkillId")), SkillID);
					VehiclePetStopAICommand();
				}
			}
		}
	}
	/*	请求幻兽攻击命令（服务器）
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RequestPetAIAttackTargetFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(SkillID);
	args.Add(TargetID);
	this->GetEntity()->CellCall(TEXT("CELL_petAIAttackTarget"), args);
	*/
}

void URolePetInterface::RequestOnComposePetBygold(const uint8 IsCompose, const FString MainPetUId, const FString VicePetUId)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RequestOnComposePetBygold : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(IsCompose);
	args.Add(MainPetUId);
	args.Add(VicePetUId);
	this->GetEntity()->CellCall(TEXT("onComposePetBygold"), args);
}

void URolePetInterface::RequestUpgradePetSkill(const FString UId, const int32 SkillId)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RequestUpgradePetSkill : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UId);
	args.Add(SkillId);
	this->GetEntity()->CellCall(TEXT("upgradePetSkill"), args);
}

void URolePetInterface::RequestUpgradePetPassiveSkill(const FString UId, const int32 SkillId, const int32 SkillBookId, const int32 ItemId)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RequestUpgradePetPassiveSkill : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UId);
	args.Add(SkillId);
	this->GetEntity()->CellCall(TEXT("upgradePetPassiveSkill"), args);
}

void URolePetInterface::RequestReplacePetSkill(const FString UId, const int32 SkillId, const int32 SkillBookId, const int32 ItemId)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RequestReplacePetSkill : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UId);
	args.Add(SkillId);
	args.Add(SkillBookId);
	this->GetEntity()->CellCall(TEXT("replacePetSkill"), args);
}

void URolePetInterface::RequestReplacePetPassiveSkill(const FString UId, const int32 SkillId, const int32 SkillBookId)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RequestReplacePetPassiveSkill : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UId);
	args.Add(SkillId);
	args.Add(SkillBookId);
	this->GetEntity()->CellCall(TEXT("replacePetPassiveSkill"), args);
}

void URolePetInterface::RequestTransformPetFC()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePetInterface::RequestTransformPetFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("transformPet"), args);
}

void URolePetInterface::OnIsmountSuccess(bool IsMount)
{
}

FString URolePetInterface::GetPetRangeAbility(const FString& UId1, const FString& UId2)
{
	FString RangeAbility = TEXT("0");
	UPetEpitome* MainPet = GetPetByUID(UId1);
	UPetEpitome* VicePet = GetPetByUID(UId2);
	if (IsValid(MainPet) && IsValid(VicePet))
	{
		float MinAbility, MaxAbility;
		if (MainPet->ability >= VicePet->ability)
		{
			MaxAbility = UKismetMathLibrary::FMin(MainPet->ability * 1.1, MainPet->ability_Max);
			MinAbility = MainPet->ability * 0.95;
		} 
		else
		{
			MaxAbility = UKismetMathLibrary::FMin(VicePet->ability * 1.1, VicePet->ability_Max);
			MinAbility = VicePet->ability * 0.95;
		}
		RangeAbility = INT_TO_FSTRING(UKismetMathLibrary::FFloor(MinAbility)) + TEXT("-") + INT_TO_FSTRING(UKismetMathLibrary::FFloor(MaxAbility));
	}
	return RangeAbility;
}

void URolePetInterface::OnChangePetAI(FString AIIndex)
{
	if (petEntityID == 0)return;
	APetCharacter* pet = Cast<APetCharacter>(UGolbalBPFunctionLibrary::GetActorByID(petEntityID));
	if (!IsValid(pet))return;
	// 配合变身使用
	pet->OnBroadCreateModelOver.BindUObject(pet, &APetCharacter::OnChangePetAI, AIIndex);
	//pet->OnChangePetAI(AIIndex);
}

void URolePetInterface::OnFinishChangePetAI()
{
	if (petEntityID == 0)return;
	APetCharacter* pet = Cast<APetCharacter>(UGolbalBPFunctionLibrary::GetActorByID(petEntityID));
	if (!IsValid(pet))return;
	pet->OnFinishChangePetAI();
}

void URolePetInterface::onLeaveWorld()
{
	Pets.Empty();
	Supper::onLeaveWorld();
}


void URolePetInterface::OnLeaveScenes()
{
	OriginPetCharacters.Empty();
	VehiclePetStopAICommand();
}

void URolePetInterface::RPC_CELL_conjurePet(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_conjurePet no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("conjurePet"), args);
}

void URolePetInterface::RPC_CELL_withdrawPet()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_withdrawPet no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("withdrawPet"), args);
}

void URolePetInterface::RPC_CELL_freePet(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_freePet no this Entity!"));
		return;
	}
	TWeakObjectPtr<URolePetInterface> DelayThisPtr(this);
	UPetEpitome* Pet = GetPetByUID(STRING_1);
	if (!IsValid(Pet))
	{
		return;
	}
	int32 MessageID;
	FString MessageArgs;
	if (Pet->petShenTongSKillList.Num() > 0)
	{
		MessageID = 5476;
		MessageArgs = Pet->GetName();
	}
	else
	{
		MessageID = 1953;
		MessageArgs = TEXT("");
	}
	UUECS3GameInstance::Instance->MessageManager->ShowMessage(MessageID, MessageArgs, FBtnClick::CreateLambda([DelayThisPtr, STRING_1](RT_BTN_TYPE BtnType)
	{
		if (DelayThisPtr.IsValid())
		{
			URolePetInterface* ThisPtr = DelayThisPtr.Get();
			if (IsValid(ThisPtr))
			{
				if (BtnType == RT_BTN_TYPE::RT_OK)
				{
					KBEngine::FVariantArray args;
					args.Add(STRING_1);

					ThisPtr->CellCall(TEXT("freePet"), args);
				}
			}
		}
	}));

}

void URolePetInterface::RPC_CELL_addPetStep(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_addPetStep no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("addPetStep"), args);
}

void URolePetInterface::RPC_CELL_activateCage()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_activateCage no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("activateCage"), args);
}

void URolePetInterface::RPC_CELL_sealPet(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_sealPet no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("sealPet"), args);
}

void URolePetInterface::RPC_CELL_GetSealPetEggAttr(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_GetSealPetEggAttr no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("GetSealPetEggAttr"), args);
}

void URolePetInterface::RPC_CELL_composePet(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_composePet no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("composePet"), args);
}

void URolePetInterface::RPC_BASE_reName(const FString& STRING_1, const FString& UNICODE_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_BASE_reName no this Entity!"));
		return;
	}
	
	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(UNICODE_1);

	entity->BaseCall(TEXT("reName"), args);
}

void URolePetInterface::RPC_CELL_requestAttackTarget(int32 skillID, int32 targetID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_requestAttackTarget no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(skillID);
	args.Add(targetID);

	entity->CellCall(TEXT("CELL_requestAttackTarget"), args);
}

void URolePetInterface::RequestSetPetDistaceFC(const float Distance)
{
	KBEngine::Entity* PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetSelfEntity();
	if (PlayerEntity != nullptr)
	{
		int32 PetEntityId = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerEntity->ID(), TEXT("activePetID"));
		if (PetEntityId)
		{
			KBEngine::Entity* petEntity = UGolbalBPFunctionLibrary::FindEntity(PetEntityId);
			if (petEntity && petEntity->Actor())
			{
				APetCharacter* pet = Cast<APetCharacter>(petEntity->Actor());
				if (IsValid(pet))
				{
					UBlackboardComponent* myBlackBoard = UAIBlueprintHelperLibrary::GetBlackboard(pet);
					if (IsValid(myBlackBoard))
					{
						//myBlackBoard->SetValueAsFloat(FName(TEXT("AttackDistance")), Distance);
					}
				}
			}
		}
	}
}

void URolePetInterface::CLIENT_OnPetExtraHPChanged_Implementation(const int32 curHP, const int32 oldHP)
{
}

void URolePetInterface::CLIENT_OnPetExtraMPChanged_Implementation(const int32 curMP, const int32 oldMP)
{
}

void URolePetInterface::RPC_CELL_onActiveHPSlot(const bool& IsActiveHP, const int32& percentHP)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_onActiveHPSlot no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(int32(IsActiveHP));
	args.Add(percentHP);
	entity->CellCall(TEXT("CELL_onActiveHPSlot"), args);
}

void URolePetInterface::RPC_CELL_onActiveMPSlot(const bool& IsActiveMP, const int32& percentMP)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URolePetInterface::RPC_CELL_onActiveMPSlot no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(int32(IsActiveMP));
	args.Add(percentMP);
	entity->CellCall(TEXT("CELL_onActiveMPSlot"), args);
}



void URolePetInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_openOriginPetUI");
	ArrBlueFunc.Add("CLIENT_addOriginPet");
	ArrBlueFunc.Add("CLIENT_OnFeedPetWildness");
	ArrBlueFunc.Add("CLIENT_OnFeedPetExp");
	ArrBlueFunc.Add("CLIENT_OnFreePetFromFence");
	ArrBlueFunc.Add("CLIENT_onEvolutionPet");
	ArrBlueFunc.Add("CLIENT_OnPetOutsideFromFence");
	ArrBlueFunc.Add("CLIENT_OnSetActivePetExp");
	ArrBlueFunc.Add("PetAddData");
	ArrBlueFunc.Add("PetRemoveData");
	ArrBlueFunc.Add("OnGeneratePet");
	ArrBlueFunc.Add("onConjurePetResult");
	ArrBlueFunc.Add("onWithdrawPetResult");
	ArrBlueFunc.Add("updatePetEpitomeDatas");
	ArrBlueFunc.Add("OnPetReNameFail");
	ArrBlueFunc.Add("petOnSetAttackState");
	ArrBlueFunc.Add("OnSealSuccess");
	ArrBlueFunc.Add("OnComposePet");
	ArrBlueFunc.Add("OnPetComposeFailed");
	ArrBlueFunc.Add("OnReplacePetSkill");
	ArrBlueFunc.Add("OnUpgradePetSkill");
	ArrBlueFunc.Add("OnIsmountSuccess");
	ArrBlueFunc.Add("OnReplacePetPassiveSkill");
	ArrBlueFunc.Add("OnUpgradePetPassiveSkill");
	ArrBlueFunc.Add("OnGetSealPetEggAttr");
	ArrBlueFunc.Add("OnAIStopCommand");
	ArrBlueFunc.Add("CLIENT_OnPetExtraHPChanged");
	ArrBlueFunc.Add("CLIENT_OnPetExtraMPChanged");
	ArrBlueFunc.Add("CLIENT_clearPetCDTime");
	ArrBlueFunc.Add("CLIENT_ShowSelfOriginPet");
	Supper::InitBlueCB();
}

CONTROL_COMPILE_OPTIMIZE_END
