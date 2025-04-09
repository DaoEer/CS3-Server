// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleWorkShopInterface.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "GameData/Item/ItemComposeEquipBP.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/CfgManager.h"
#include "GameData/EnumCsvDefine.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/CS3Debug.h"
#include "GameData/Item/ItemFactory.h"
#include "Manager/MessageManager.h"
#include "RoleLunHuiMiJinInterface.h"
#include "GameData/Item/CS3ItemData.h"
#include "CS3Base/UIManager.h"
#include "Manager/EventManager.h"

CONTROL_COMPILE_OPTIMIZE_START

void URoleWorkShopInterface::OnEnterScenes()
{
	// 绿装打造
	UCfgManager* cfgMgr = UGolbalBPFunctionLibrary::CfgManager();
	if (!IsValid(cfgMgr))return;
	GEquipComposeCost.Empty();
	const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_GEQUIP_COST_DATA);
	if (IsValid(table))
	{
		TArray<const FGreenEquipComposeCost*> AllConfig;
		table->GetAllRows(AllConfig);
		for (auto cost : AllConfig)
		{
			FGreenEquipComposeCost CCost;
			CCost.equipID = cost->equipID;
			CCost.labelName = cost->labelName;
			CCost.partEquipID = cost->partEquipID;
			CCost.needLevel = cost->needLevel;
			CCost.money = cost->money;
			CCost.bluePrint = cost->bluePrint;
			CCost.useTime = cost->useTime;
			CCost.mainMaterial = cost->mainMaterial;
			CCost.mainMaterialNum = cost->mainMaterialNum;
			CCost.material = cost->material;

			float rate = GetBuildConsumeRate(LHMJ_BUILD_TYPE::LHMJ_BUIILD_GONG_FANG);
			CCost.money = FMath::RoundToInt(CCost.money * rate);
			CCost.mainMaterialNum = FMath::RoundToInt(CCost.mainMaterialNum * rate);
			for (auto i = CCost.material.CreateConstIterator(); i; ++i)
			{
				CCost.material[i.Key()] = FMath::RoundToInt(i.Value() * rate);
			}

			GEquipComposeCost.Add(cost->equipID, CCost);
		}
	}
}

void URoleWorkShopInterface::CLIENT_onRequestComposeData_Implementation(const int32& ComposeType, const int32& EndTime, const int32& ItemID, const int32& UnlockNum, const int32& NPCID)
{
	if (ComposeType == int32(COMPOSE_TYPE::COMPOSE_TYPE_TRIPOD))
	{
		TripodComposeEndTime = UGolbalBPFunctionLibrary::FromServerTimeToClientTime(EndTime);
		_InitTripodConfig();
		URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
		if (IsValid(kitbatInst))
		{
			kitbatInst->tripodeCapacity = STORE_LOCKERS_CAPACITY;
			kitbatInst->canUnLockToolCapacity = STORE_LOCKERS_LOCK_CAPACITY;
			kitbatInst->unLockTripodGridNum = UnlockNum;
		}
	}
	else
	{
		ToolComposeType = COMPOSE_TYPE(ComposeType);
		ToolComposeEndTime = UGolbalBPFunctionLibrary::FromServerTimeToClientTime(EndTime);
		_InitToolConfig();
		URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
		if (IsValid(kitbatInst))
		{
			kitbatInst->toolCapacity = STORE_LOCKERS_CAPACITY;
			kitbatInst->canUnLockToolCapacity = STORE_LOCKERS_LOCK_CAPACITY;
			kitbatInst->unLockToolGridNum = UnlockNum;
		}
	}
}

void URoleWorkShopInterface::CLIENT_onRequestGEComposeData_Implementation(const int32 & ComposeType, const int32 & EndTime, const int32 & ItemID, const int32 & UnlockNum, const float & SuccessRate, const int32& NPCID)
{
	ToolComposeType = COMPOSE_TYPE(ComposeType);
	ToolComposeEndTime = UGolbalBPFunctionLibrary::FromServerTimeToClientTime(EndTime);
	_InitToolConfig();
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (IsValid(kitbatInst))
	{
		kitbatInst->toolCapacity = STORE_LOCKERS_CAPACITY;
		kitbatInst->canUnLockToolCapacity = STORE_LOCKERS_LOCK_CAPACITY;
		kitbatInst->unLockToolGridNum = UnlockNum;
	}
}

void URoleWorkShopInterface::CLIENT_beginComposeTool_Implementation(const int32 & ComposeType, const int32& ItemID, const int32 & EndTime)
{
	if (ComposeType == int32(COMPOSE_TYPE::COMPOSE_TYPE_TRIPOD))
	{
		TripodComposeEndTime = UGolbalBPFunctionLibrary::FromServerTimeToClientTime(EndTime);
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
		{
			UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("StartRefine"));
		}
	}
	else
	{
		ToolComposeType = COMPOSE_TYPE(ComposeType);
		ToolComposeEndTime = UGolbalBPFunctionLibrary::FromServerTimeToClientTime(EndTime);
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
		{
			UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("StartCompose"));
		}
	}
}

void URoleWorkShopInterface::CLIENT_beginGEComposeTool_Implementation(const int32 & ComposeType, const int32& ItemID, const int32 & EndTime, const float & SuccessRate)
{
	ToolComposeType = COMPOSE_TYPE(ComposeType);
	ToolComposeEndTime = UGolbalBPFunctionLibrary::FromServerTimeToClientTime(EndTime);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("StartCompose"));
	}
}

void URoleWorkShopInterface::CLIENT_OnFinishCompose_Implementation(const int32 & ComposeType, const int32& ItemID, const int32& Result)
{
	if (ComposeType == int32(COMPOSE_TYPE::COMPOSE_TYPE_TRIPOD))
	{
		TripodComposeEndTime = 0;
	}
	else
	{
		ToolComposeEndTime = 0;
	}
	const FCS3ItemData itemdata = UItemFactory::GetStaticDataByItemID(ItemID);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
	{
		if (Result == 0)
		{
			if (ComposeType == int32(COMPOSE_TYPE::COMPOSE_TYPE_TRIPOD))
			{
				UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("RefineFail"));
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5409, itemdata.ItemName);
			}
			else
			{
				UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("ComposeFail"));
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5360, itemdata.ItemName);
			}
		}
		else
		{
			if (ComposeType == int32(COMPOSE_TYPE::COMPOSE_TYPE_TRIPOD))
			{
				UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("RefineSuccess"));
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5408, itemdata.ItemName);
			}
			else
			{
				UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("ComposeSuccess"));
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5359, itemdata.ItemName);
			}
		}
	}
}

int32 URoleWorkShopInterface::GetComposeToolNum(const int32 & ItemID)
{
	if (ToolComposeCost.Contains(ItemID))
	{
		int num(0);
		const FToolComposeCost cost = ToolComposeCost[ItemID];

		URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
		if (!IsValid(kitbatInst))return 0;
		int32 index(0);
		for (auto It = cost.material.CreateConstIterator(); It; ++It)
		{
			index += 1;
			int32 amount = It.Value();
			int32 MaterialNum = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, It.Key(), FIND_BINDTYPE_ENUM::INGOREBIND);
			if (index == 1)
			{
				num = MaterialNum / amount;
			}
			else
			{
				num = FMath::Min(num, MaterialNum / amount);
			}
			if (num == 0)
			{
				return num;
			}
		}
		int64 OwnMoney = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
		int32 OwnPsionic = GetEntity()->GetDefinedProperty(TEXT("psionic")).GetValue<int32>();
		num = FMath::Min(num, int(OwnMoney / cost.money));
		num = FMath::Min(num, int(OwnPsionic / cost.psionic));
		return num;

	}
	return 0;
}

void URoleWorkShopInterface::OnOccypySpaceTypeChange(const LHMJ_SPACE_TYPE &_spaceType)
{
	spaceType = _spaceType;
	if (ToolComposeCost.Num() > 0)
	{
		_InitToolConfig();
	}
	if (TripodComposeCost.Num()>0)
	{
		_InitTripodConfig();
	}
	
}

float URoleWorkShopInterface::GetBuildConsumeRate(const enum LHMJ_BUILD_TYPE & _buildType)
{
	if (spaceType == LHMJ_SPACE_TYPE::LHMJ_SPACE_TYPE_PRIVATE || spaceType == LHMJ_SPACE_TYPE::LHMJ_SPACE_TYPE_NONE)
	{
		return 1.0;
	}
	URoleLunHuiMiJinInterface* LHMJInterface = Cast<URoleLunHuiMiJinInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleLunHuiMiJinInterface")));
	if (IsValid(LHMJInterface))
	{
		int32 BuildLevel = LHMJInterface->GetBuildLevel(_buildType);
		UCfgManager* cfgMgr = UGolbalBPFunctionLibrary::CfgManager();
		if (!IsValid(cfgMgr))return 1.0;
		const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_LHMJ_COMPOSE_RATE_COST_DATA);
		if (IsValid(table))
		{
			TArray<const FForgeConsumeCfg*> AllConfig;
			table->GetAllRows(AllConfig);
			for (auto cost : AllConfig)
			{
				if (cost->level == BuildLevel)
				{
					if (spaceType == LHMJ_SPACE_TYPE::LHMJ_SPACE_TYPE_PUBLIC)
					{
						return cost->publicConsumeRate / 100.0;
					}
					else if (spaceType == LHMJ_SPACE_TYPE::LHMJ_SPACE_TYPE_HIGH_DF)
					{
						return cost->highConsumeRate / 100.0;
					}
				}
			}
		}
	}
	return 1.0;
}

void URoleWorkShopInterface::GetBuildSuccessRate(LHMJ_BUILD_TYPE BuildType, int32 ComposeType, int32& SuccessRate, int32& ConsumeRate)
{
	URoleLunHuiMiJinInterface* LHMJInterface = Cast<URoleLunHuiMiJinInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleLunHuiMiJinInterface")));
	if (IsValid(LHMJInterface))
	{
		int32 BuildLevel = LHMJInterface->GetBuildLevel(BuildType);
		LHMJ_SPACE_TYPE SpaceType = LHMJInterface->OccupySpaceType;
		UCfgManager* cfgMgr = UGolbalBPFunctionLibrary::CfgManager();
		if (!IsValid(cfgMgr)) return;
		const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_LHMJ_COMPOSE_RATE_COST_DATA);
		if (!IsValid(table)) return;
		const FForgeConsumeCfg* data = table->GetRow<FForgeConsumeCfg>(INT_TO_FSTRING(BuildLevel));
		if (data != nullptr)
		{
			if (data->level == BuildLevel)
			{
				switch (SpaceType)
				{
				case LHMJ_SPACE_TYPE::LHMJ_SPACE_TYPE_PRIVATE:
				{
					switch (ComposeType)
					{
					case 2:
					{
						SuccessRate = data->df_SumSuccessRate;
						break;
					}
					default:
						SuccessRate = 0;
						break;
					}
					ConsumeRate = 0;
					break;
				}
				case LHMJ_SPACE_TYPE::LHMJ_SPACE_TYPE_PUBLIC:
				{
					switch (ComposeType)
					{
					case 2:
					{
						SuccessRate = data->xf_SumSuccessRate;
						break;
					}
					default:
						SuccessRate = data->successRate;
						break;
					}
					ConsumeRate = data->publicConsumeRate;
					break;
				}
				case LHMJ_SPACE_TYPE::LHMJ_SPACE_TYPE_HIGH_DF:
				{
					switch (ComposeType)
					{
					case 2:
					{
						SuccessRate = data->gjdf_SumSuccessRate;
						break;
					}
					default:
						SuccessRate = data->successRate;
						break;
					}
					ConsumeRate = data->highConsumeRate;
					break;
				}
				default:
					SuccessRate = 0;
					ConsumeRate = 0;
					break;
				}
			}
		}
	}
}

int32 URoleWorkShopInterface::GetComposeGEquipNum(const int32 & ItemID)
{
	if (GEquipComposeCost.Contains(ItemID))
	{
		int num(0);
		const FGreenEquipComposeCost cost = GEquipComposeCost[ItemID];

		URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
		if (!IsValid(kitbatInst))return 0;

		TArray<UItemBase*> ItemArr = kitbatInst->GetItemsByItemID(cost.bluePrint);
		TMap<int32, int32> hasMMItemNums;				// 背包中含有的主材料数量
		for (auto item : ItemArr)
		{
			UItemComposeEquipBP* bPrintItem = Cast<UItemComposeEquipBP>(item);
			if (IsValid(bPrintItem) && cost.mainMaterial.Contains(bPrintItem->suitIndex))
			{
				int32 mmItemID= cost.mainMaterial[bPrintItem->suitIndex];				// 主材料ID
				int32 mmItemNum = cost.mainMaterialNum;									// 主材料数量
				if (hasMMItemNums.Contains(mmItemID))
				{
					if (hasMMItemNums[mmItemID] < mmItemNum)continue;
					hasMMItemNums[mmItemID] -= mmItemNum;
					num += 1;
				}
				else
				{
					int32 MaterialNum = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, mmItemID, FIND_BINDTYPE_ENUM::INGOREBIND);
					if (MaterialNum >= mmItemNum)
					{
						MaterialNum -= mmItemNum;
						num += 1;
					}
					hasMMItemNums.Add(mmItemID, MaterialNum);
				}	
			}	
		}
		if (num == 0)return num;

		for (auto It = cost.material.CreateConstIterator(); It; ++It)
		{
			int32 amount = It.Value();
			int32 MaterialNum = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, It.Key(), FIND_BINDTYPE_ENUM::INGOREBIND);
			num = FMath::Min(num, MaterialNum / amount);
			if (num == 0)
			{
				return num;
			}
		}
		int64 OwnMoney = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
		num = FMath::Min(num, int32(OwnMoney / cost.money));
		return num;

	}
	return 0;
}

int32 URoleWorkShopInterface::GetComposeTripodNum(const int32 & ItemID)
{
	if (TripodComposeCost.Contains(ItemID))
	{
		int num(0);
		const FTripodComposeCost cost = TripodComposeCost[ItemID];

		URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
		if (!IsValid(kitbatInst))return 0;
		int32 index(0);
		for (auto It = cost.material.CreateConstIterator(); It; ++It)
		{
			int32 amount = It.Value();
			index += 1;
			int32 MaterialNum = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, It.Key(), FIND_BINDTYPE_ENUM::INGOREBIND);
			if (index == 1)
			{
				num = MaterialNum / amount;
			}
			else
			{
				num = FMath::Min(num, MaterialNum / amount);
			}
			if (num == 0)
			{
				return num;
			}
		}
		int64 OwnMoney = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
		int32 OwnPsionic = GetEntity()->GetDefinedProperty(TEXT("psionic")).GetValue<int32>();
		num = FMath::Min(num, int32(OwnMoney / cost.money));
		num = FMath::Min(num, int32(OwnPsionic / cost.psionic));
		return num;

	}
	return 0;
}

void URoleWorkShopInterface::SortItemIDs(TArray<int32> InputItemIDArr, TArray<int32> & ItemIDArr)
{
	TArray<FCS3ItemData> itemArr;
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (IsValid(kitbatInst))
	{
		for (auto id : InputItemIDArr)
		{
			const FCS3ItemData itemdata = UItemFactory::GetStaticDataByItemID(id);
			itemArr.Add(itemdata);
		}
		itemArr.Sort([this](const FCS3ItemData& A, const FCS3ItemData& B)->bool
		{
			if (A.Quality > B.Quality )
			{
				return true;
			}
			if (A.ItemID >= B.ItemID)
			{
				return true;
			}
			return false;
		});
		for (auto item : itemArr)
		{
			ItemIDArr.Add(item.ItemID);
		}

	}
}

void URoleWorkShopInterface::ComposeTool(const int32 & ComposeType, const int32 & EquipID, bool bUseUnbind)
{
	if (ComposeType == int32(COMPOSE_TYPE::COMPOSE_TYPE_TRIPOD))
	{
		if (TripodComposeEndTime > FDateTime::Now())
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5357);
			return;
		}
	}
	else
	{
		if (ToolComposeEndTime > FDateTime::Now())
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5357);
			return;
		}
	}
	KBEngine::FVariantArray args;
	args.Add(uint8(ComposeType));
	args.Add(EquipID);
	args.Add(uint8(bUseUnbind));
	CellCall(TEXT("CELL_composeTool"), args);
}

void URoleWorkShopInterface::ComposeGreedEquip(const int32 & EquipID, bool bUseUnbind, const FString & BPrintUID)
{
	if (ToolComposeEndTime > FDateTime::Now())
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(5357);
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(EquipID);
	args.Add(uint8(bUseUnbind));
	args.Add(BPrintUID);
	CellCall(TEXT("CELL_composeGreedEquip"), args);
}

void URoleWorkShopInterface::MeltingGreedEquip(const FString & BPrintUID, const TArray<FString> EquipUIDArr)
{
	KBEngine::FVariantArray args;
	KBEngine::FVariantArray arr;
	for (FString it : EquipUIDArr)
	{
		arr.Add(FVariant(it));
	}
	args.Add(BPrintUID);
	args.Add(arr);
	CellCall(TEXT("CELL_meltingEquip"), args);
}

void URoleWorkShopInterface::CLIENT_onMeltingtEquip_Implementation(const FString & BPrintUID, const float & AddRate)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("MeltSuccess"));
	}
}

void URoleWorkShopInterface::RequestPrayTimes()
{
	KBEngine::FVariantArray args;
	CellCall(TEXT("CELL_requestPrayTimes"), args);
}

int32 URoleWorkShopInterface::GetReflashTime()
{
	FDateTime now_ = FDateTime::Now();
	return 15 * 60 - (now_.GetMinute() % 15 * 60 + now_.GetSecond());
}

void URoleWorkShopInterface::CLIENT_OnRequestPrayTimes_Implementation(const TArray<int32>& ProyTimeArr, const int32 & ProyNum)
{
	_ProyNum = ProyNum;
}

void URoleWorkShopInterface::BeginPrayComposeTimes()
{
	if (_ProyNum >= 10)
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(5361);
		return;
	}
	KBEngine::FVariantArray args;
	CellCall(TEXT("CELL_prayComposeTime"), args);
}

void URoleWorkShopInterface::CLIENT_OnPrayTime_Implementation(const int32 & ProyTime)
{
	_ProyNum += 1;
	ToolComposeEndTime -= FTimespan::FromSeconds(ProyTime * 60);
}

void URoleWorkShopInterface::CLIENT_OpenQuenchingEquip_Implementation(const int32& NPCID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("WorkShopQuenching"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OpenWorkShopQuenchingUIEvent.Broadcast(NPCID);
	}
}

void URoleWorkShopInterface::QuenchingEquip(const FString & EquipUID)
{
	KBEngine::FVariantArray args;
	args.Add(EquipUID);
	CellCall(TEXT("CELL_quenchingEquip"), args);
}

void URoleWorkShopInterface::CLIENT_OnQuenchingEquip_Implementation(const FString & EquipUID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowTextAnimationMessage(TEXT("QuenchingSuccess"));
	}
}

void URoleWorkShopInterface::RequestTakeToolItem(const int32 & Order)
{
	KBEngine::FVariantArray args;
	args.Add(Order);
	CellCall(TEXT("CELL_requestTakeToolItem"), args);
}

void URoleWorkShopInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_onRequestComposeData");
	ArrBlueFunc.Add("CLIENT_onRequestGEComposeData");
	ArrBlueFunc.Add("CLIENT_OnFinishCompose");
	ArrBlueFunc.Add("CLIENT_beginComposeTool");
	ArrBlueFunc.Add("CLIENT_beginGEComposeTool");
	ArrBlueFunc.Add("CLIENT_onMeltingtEquip");
	ArrBlueFunc.Add("CLIENT_OnRequestPrayTimes");
	ArrBlueFunc.Add("CLIENT_OnPrayTime");
	ArrBlueFunc.Add("CLIENT_OpenQuenchingEquip");
	ArrBlueFunc.Add("CLIENT_OnQuenchingEquip");

	Super::InitBlueCB();
}

TArray<FString> URoleWorkShopInterface::GetCategoryNameList(COMPOSE_TYPE ComposeType)
{
	FName Row = FSTRING_TO_FNAME(INT_TO_FSTRING(int32(ComposeType)));
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_WORKSHOP_CATEGORY_DATA);
	FWorkShopComposeCategory* data = const_cast<FWorkShopComposeCategory*>(table->GetRow<FWorkShopComposeCategory>(Row));
	if (data == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleWorkShopInterface::GetCategoryNameList : data!"));
		TArray<FString> Names = {};
		return Names;
	}
	return data->CategoryNames;
}

TArray<int32> URoleWorkShopInterface::GetToolIDList(FString LabelName)
{
	TArray<int32> IDList;
	int32 BuildLevel = 1;
	URoleLunHuiMiJinInterface* LHMJInterface = Cast<URoleLunHuiMiJinInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleLunHuiMiJinInterface")));
	if (IsValid(LHMJInterface))
	{
		BuildLevel = LHMJInterface->GetBuildLevel(LHMJ_BUILD_TYPE::LHMJ_BUIILD_GONG_FANG);
	}
	for (TPair<int32, FToolComposeCost>& MapData : ToolComposeCost)
	{
		if (MapData.Value.labelName.Equals(LabelName) && MapData.Value.needLevel <= BuildLevel)
		{
			IDList.Add(MapData.Value.equipID);
		}
	}
	return IDList;
}

TArray<int32> URoleWorkShopInterface::GetEquipIDList(FString LabelName)
{
	TArray<int32> IDList;
	int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("profession"));
	int32 BuildLevel = 1;
	URoleLunHuiMiJinInterface* LHMJInterface = Cast<URoleLunHuiMiJinInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleLunHuiMiJinInterface")));
	if (IsValid(LHMJInterface))
	{
		BuildLevel = LHMJInterface->GetBuildLevel(LHMJ_BUILD_TYPE::LHMJ_BUIILD_GONG_FANG);
	}
	for (TPair<int32, FGreenEquipComposeCost>& MapData : GEquipComposeCost)
	{
		FCS3ItemData ItemData = UItemFactory::GetStaticDataByItemID(MapData.Value.equipID);
		TArray<FString> ReqClasses = UGolbalBPFunctionLibrary::SplitString(ItemData.ReqClasses, false, TEXT("|"));
		//需要筛出同职业的
		if (MapData.Value.labelName.Equals(LabelName) && MapData.Value.needLevel <= BuildLevel && ReqClasses.Contains(INT_TO_FSTRING(Profession)))
		{
			IDList.Add(MapData.Value.equipID);
		}
	}
	return IDList;
}

TArray<int32> URoleWorkShopInterface::GetTripodIDList(FString LabelName)
{
	TArray<int32> IDList;
	int32 BuildLevel = 1;
	URoleLunHuiMiJinInterface* LHMJInterface = Cast<URoleLunHuiMiJinInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleLunHuiMiJinInterface")));
	if (IsValid(LHMJInterface))
	{
		BuildLevel = LHMJInterface->GetBuildLevel(LHMJ_BUILD_TYPE::LHMJ_BUIILD_QIAN_KU_DING);
	}
	for (TPair<int32, FTripodComposeCost>& MapData : TripodComposeCost)
	{
		if (MapData.Value.labelName.Equals(LabelName) && MapData.Value.needLevel <= BuildLevel)
		{
			IDList.Add(MapData.Value.equipID);
		}
	}
	return IDList;
}

bool URoleWorkShopInterface::CheckComposeState(COMPOSE_TYPE ComposeType, float& RemainTime)
{
	FDateTime EndTime;
	switch (ComposeType)
	{
	case COMPOSE_TYPE::COMPOSE_TYPE_TOOL:
	{
		EndTime = ToolComposeEndTime;
		break;
	}
	case COMPOSE_TYPE::COMPOSE_TYPE_GEQUIP:
	{
		EndTime = ToolComposeEndTime;
		break;
	}
	case COMPOSE_TYPE::COMPOSE_TYPE_TRIPOD:
	{
		EndTime = TripodComposeEndTime;
		break;
	}
	}
	FTimespan DTime = EndTime - FDateTime::Now();
	RemainTime = DTime.GetTotalSeconds();
	return RemainTime > 0;
}

float URoleWorkShopInterface::GetComposeTotalTime(COMPOSE_TYPE ComposeType, int32 ComposeItemID)
{
	switch (ComposeType)
	{
	case COMPOSE_TYPE::COMPOSE_TYPE_TOOL:
	{
		for (TPair<int32, FToolComposeCost>& MapData : ToolComposeCost)
		{
			if (MapData.Key == ComposeItemID)
			{
				return MapData.Value.useTime;
			}
		}
		break;
	}
	case COMPOSE_TYPE::COMPOSE_TYPE_GEQUIP:
	{
		for (TPair<int32, FGreenEquipComposeCost>& MapData : GEquipComposeCost)
		{
			if (MapData.Key == ComposeItemID)
			{
				return MapData.Value.useTime;
			}
		}
		break;
	}
	case COMPOSE_TYPE::COMPOSE_TYPE_TRIPOD:
	{
		for (TPair<int32, FTripodComposeCost>& MapData : TripodComposeCost)
		{
			if (MapData.Key == ComposeItemID)
			{
				return MapData.Value.useTime;
			}
		}
		break;
	}
	}
	return 0;
}

float URoleWorkShopInterface::GetMeltingEquipSuccessRate(FString BlueprintUID, TArray<FString> EquipUIDs)
{
	URoleKitBagInterface* kitbaginterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbaginterface)) return 0.0f;

	float AddSuccessRate = 0.0f;
	UItemComposeEquipBP* LocalBlueprintData = Cast<UItemComposeEquipBP>(kitbaginterface->FindItemByUID(BlueprintUID));
	if (!IsValid(LocalBlueprintData))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleWorkShopInterface::GetMeltingEquipSuccessRate : UItemComposeEquipBP!"));
		return 0.0f;
	}
	int32 ComposeEquipID = LocalBlueprintData->GetComposeEquipID();
	UItemFactory* ItemFactory = UUECS3GameInstance::Instance->ItemFactory;
	if (!IsValid(ItemFactory))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleWorkShopInterface::GetMeltingEquipSuccessRate : ItemFactory!"));
		return 0.0f;
	}
	UEquip* StaticEquip = Cast<UEquip>(ItemFactory->GetItemByID(ComposeEquipID));
	if (!IsValid(StaticEquip))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleWorkShopInterface::GetMeltingEquipSuccessRate : StaticEquip!"));
		return 0.0f;
	}
	for (auto EquipID : EquipUIDs)
	{
		UItemBase* EquipItemBase = kitbaginterface->FindItemByUID(EquipID);
		for (auto Data : MeltingEquipCfg)
		{
			if (StaticEquip->Level == Data.level && StaticEquip->Quality == Data.quality
				&& EquipItemBase->Level == Data.meltingLevel && EquipItemBase->Quality == Data.meltingQuality)
			{
				AddSuccessRate = AddSuccessRate + (Data.successRate / 100.0f);
				break;
			}
		}
	}
	//总共最多增加15%的成功率（此次熔炼能增加的最大成功率 = 15 - 以前熔炼增加的成功率）
	return FMath::Min(AddSuccessRate, (15.0f - LocalBlueprintData->addRate));
}

void URoleWorkShopInterface::_InitToolConfig()
{
	/// 工具打造消耗
	ToolComposeCost.Empty();
	UCfgManager* cfgMgr = UGolbalBPFunctionLibrary::CfgManager();
	if (!IsValid(cfgMgr))return;

	const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TOOL_COST_DATA);
	if (IsValid(table))
	{
		TArray<const FToolComposeCost*> AllConfig;
		table->GetAllRows(AllConfig);
		for (auto cost : AllConfig)
		{
			FToolComposeCost CCost;
			CCost.equipID = cost->equipID;
			CCost.labelName = cost->labelName;
			CCost.needLevel = cost-> needLevel;
			CCost.money = cost->money;
			CCost.psionic = cost->psionic;
			CCost.useTime = cost->useTime;
			CCost.material = cost->material;

			float rate = GetBuildConsumeRate(LHMJ_BUILD_TYPE::LHMJ_BUIILD_GONG_FANG);
			CCost.money = FMath::RoundToInt(CCost.money * rate);
			CCost.psionic = FMath::RoundToInt(CCost.psionic * rate);
			for (auto i = CCost.material.CreateConstIterator(); i ; ++i)
			{
				CCost.material[i.Key()] = FMath::RoundToInt(i.Value() * rate);
			}
			ToolComposeCost.Add(cost->equipID, CCost);
		}
	}
	// 绿装打造
	GEquipComposeCost.Empty();
	table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_GEQUIP_COST_DATA);
	if (IsValid(table))
	{
		TArray<const FGreenEquipComposeCost*> AllConfig;
		table->GetAllRows(AllConfig);
		for (auto cost : AllConfig)
		{
			FGreenEquipComposeCost CCost;
			CCost.equipID = cost->equipID;
			CCost.labelName = cost->labelName;
			CCost.partEquipID = cost->partEquipID;
			CCost.needLevel = cost->needLevel;
			CCost.money = cost->money;
			CCost.bluePrint = cost->bluePrint;
			CCost.useTime = cost->useTime;
			CCost.mainMaterial = cost->mainMaterial;
			CCost.mainMaterialNum = cost->mainMaterialNum;
			CCost.material = cost->material;

			float rate = GetBuildConsumeRate(LHMJ_BUILD_TYPE::LHMJ_BUIILD_GONG_FANG);
			CCost.money = FMath::RoundToInt(CCost.money * rate);
			CCost.mainMaterialNum = FMath::RoundToInt(CCost.mainMaterialNum * rate);
			for (auto i = CCost.material.CreateConstIterator(); i; ++i)
			{
				CCost.material[i.Key()] = FMath::RoundToInt(i.Value() * rate);
			}
			GEquipComposeCost.Add(cost->equipID, CCost);
		}
	}

	// 熔炼装备
	if (MeltingEquipCfg.Num() <= 0)
	{
		table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MELTHING_EQUIP_DATA);
		if (IsValid(table))
		{
			TArray<const FMeltingEquipCost*> AllConfig;
			table->GetAllRows(AllConfig);
			for (auto cost : AllConfig)
			{
				MeltingEquipCfg.Add(*cost);
			}
		}
	}
}

void URoleWorkShopInterface::_InitTripodConfig()
{
	// 消耗
	if (TripodComposeCost.Num() <= 0)
	{
		UCfgManager* cfgMgr = UGolbalBPFunctionLibrary::CfgManager();
		if (cfgMgr)
		{
			const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TRIPOD_COST_DATA);
			if (IsValid(table))
			{
				TArray<const FTripodComposeCost*> AllConfig;
				table->GetAllRows(AllConfig);
				for (auto cost : AllConfig)
				{
					FTripodComposeCost CCost;
					CCost.equipID = cost->equipID;
					CCost.labelName = cost->labelName;
					CCost.needLevel = cost->needLevel;
					CCost.money = cost->money;
					CCost.psionic = cost->psionic;
					CCost.useTime = cost->useTime;
					CCost.material = cost->material;

					float rate = GetBuildConsumeRate(LHMJ_BUILD_TYPE::LHMJ_BUIILD_QIAN_KU_DING);
					CCost.money = FMath::RoundToInt(CCost.money * rate);
					CCost.psionic = FMath::RoundToInt(CCost.psionic * rate);
					for (auto i = CCost.material.CreateConstIterator(); i; ++i)
					{
						CCost.material[i.Key()] = FMath::RoundToInt(i.Value() * rate);
					}
					TripodComposeCost.Add(cost->equipID, CCost);
				}
			}
		}
	}
}

CONTROL_COMPILE_OPTIMIZE_END