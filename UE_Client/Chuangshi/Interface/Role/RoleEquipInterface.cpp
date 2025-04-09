// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleEquipInterface.h"
#include "KBEngine.h"
#include "RoleKitBagInterface.h"
#include "GameData/Item/Equip.h"
#include "GameData/Item/ItemFactory.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/EnumCsvDefine.h"
#include "Manager/CfgManager.h"
#include "Manager/TutorialManager.h"
#include "Manager/MessageManager.h"

CONTROL_COMPILE_OPTIMIZE_START
struct  FMath;

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleEquipInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnQueryTargetEquipInfo, &URoleEquipInterface::CLIENT_OnQueryTargetEquipInfo, const FVariant&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRequestIntensifySaveSlotInfo, &URoleEquipInterface::CLIENT_OnRequestIntensifySaveSlotInfo, const int32&, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleEquipInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleEquipInterface::URoleEquipInterface()
{

}

URoleEquipInterface::~URoleEquipInterface()
{

}



void URoleEquipInterface::CLIENT_onEquipWieldCb_Implementation(const FString& ItemUID)
{
	//穿戴装备时时，检查有没有需要关闭的新手指引
	if (UGolbalBPFunctionLibrary::TutorialManager())
	{
		UGolbalBPFunctionLibrary::TutorialManager()->OnRemoveItem(ItemUID);
	}
}

void URoleEquipInterface::CLIENT_onEquipUnWieldCb_Implementation(const FString& ItemUID)
{

}

void URoleEquipInterface::IntensifyEquip(const FString& EquipUID, const int32& DstLv, const int32& AttachItemID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::IntensifyEquip : GetEntity()!"));
		return;
	}
	if (CanIntensify(EquipUID,DstLv, AttachItemID))
	{
		KBEngine::FVariantArray Args;
		Args.Add(EquipUID);
		Args.Add(DstLv);
		Args.Add(AttachItemID);
		GetEntity()->CellCall(TEXT("doEquipIntensify"), Args);
	}
	
}

void URoleEquipInterface::GetIntensifyCost(const FString& EquipUID, const int32& IntensifyLv, int32& CostMoney, int32& WhiteBeadCount, int32& FiveBeadCount, int32& SuperBeadCount)
{
	CostMoney = 0;
	WhiteBeadCount = 0;
	FiveBeadCount = 0;
	SuperBeadCount = 0;
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifyCost : kitbatInst!"));
		return;
	}
	UItemBase* Item = kitbatInst->FindItemByUID(EquipUID);
	UEquip* Equip = Cast<UEquip>(Item);
	if (IsValid(Equip))
	{
		int32 EquipLv = Equip->Level;
		int32 CurrIntensifyLv = Equip->GetCurrIntensifyLv();
		int32 MaxIntensifyLv = Equip->GetMaxIntensifyLv();
		if (IntensifyLv <= MaxIntensifyLv)
		{
			const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_EQUIP_INTENSIFY_COST);
			TArray<FName> RowNames;
			RowNames = table->GetRowNames();
			for (FName RowName : RowNames)
			{
				const FIntensifyCost* Data = table->GetRow<FIntensifyCost>(RowName);
				if (Data)
				{
					FString Temp = Data->MinMaxLv;
					FString Left;
					FString Right;
					Temp.Split(TEXT("-"), &Left, &Right);
					int32 MinLv = FSTRING_TO_INT(Left);
					int32 MaxLv = FSTRING_TO_INT(Right);
					if ((EquipLv >= MinLv) && (EquipLv < MaxLv) && (IntensifyLv == Data->IntensifyLv))
					{
						CostMoney = Data->MoneyCost;
						WhiteBeadCount = Data->LowMaterialCost;
						FiveBeadCount = Data->MediumMaterialCost;
						SuperBeadCount = Data->HighMaterialCost;
						return;
					}
				}
			}
		}
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("EquipUID[%s], IntensifyLv[%d], CostMoney[%d], WhiteBeadCount[%d], FiveBeadCount[%d]. SuperBeadCount[%d]"), *EquipUID, IntensifyLv, CostMoney, WhiteBeadCount, FiveBeadCount, SuperBeadCount);
	}
}

void URoleEquipInterface::GetSumIntensifyCost(const FString& EquipUID, const int32& DstLv, int32& CostMoney, int32& WhiteBeadCount, int32& FiveBeadCount, int32& SuperBeadCount)
{
	CostMoney = 0;
	WhiteBeadCount = 0;
	FiveBeadCount = 0;
	SuperBeadCount = 0;
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetSumIntensifyCost : kitbatInst!"));
		return;
	}
	UItemBase* Item = kitbatInst->FindItemByUID(EquipUID);
	UEquip* Equip = Cast<UEquip>(Item);
	if (IsValid(Equip))
	{
		int32 CurrIntensifyLv = Equip->GetCurrIntensifyLv();
		int32 MaxIntensifyLv = Equip->GetMaxIntensifyLv();
		int32 MinLv = (DstLv > MaxIntensifyLv ? MaxIntensifyLv : DstLv);
		if (CurrIntensifyLv < MinLv)
		{
			for (int32 i = CurrIntensifyLv + 1; i <= MinLv; i++)
			{
				int32 TempCostMoney = 0;
				int32 TempWhiteBeadCount = 0;
				int32 TempFiveBeadCount = 0;
				int32 TempSuperBeadCount = 0;
				GetIntensifyCost(EquipUID, i, TempCostMoney, TempWhiteBeadCount, TempFiveBeadCount, TempSuperBeadCount);
				CostMoney += TempCostMoney;
				WhiteBeadCount += TempWhiteBeadCount;
				FiveBeadCount += TempFiveBeadCount;
				SuperBeadCount += TempSuperBeadCount;
			}
		}
	}
}

int32 URoleEquipInterface::GetTotalAmountByItemID(const int32& ItemID)
{
	int32 amount(0);
	const FCS3ItemData IData = UItemFactory::GetStaticDataByItemID(ItemID);
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifyCrystal : kitbatInst!"));
		return amount;
	}
	TArray<UItemBase*> itemList = kitbatInst->GetItemListByItemScript(IData.Script);
	for (auto item_ : itemList)
	{
		if (item_->Param1.Equals(IData.Param1))
		{
			amount += item_->Amount;
		}
	}
	return amount;
}

void URoleEquipInterface::GetIntensifyCrystal(int32& WhiteBeadCount, int32& FiveBeadCount, int32& SuperBeadCount)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifyCrystal : kitbatInst!"));
		return;
	}
	TArray<UItemBase*> itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemIntensifyCrystal"));
	for (auto item_ : itemList)
	{
		if (item_->Param1 == TEXT("1"))
		{
			WhiteBeadCount += item_->Amount;
		}
		else if (item_->Param1 == TEXT("2"))
		{
			FiveBeadCount += item_->Amount;
		}
		else if (item_->Param1 == TEXT("3"))
		{
			SuperBeadCount += item_->Amount;
		}
	}
}

void URoleEquipInterface::GetIntensifyDragon(int32& WhiteDragonCount, int32& FiveDragonCount, int32& SuperDragonCount)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifyDragon : kitbatInst!"));
		return;
	}
	TArray<UItemBase*> itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemIntensifyDragon"));
	for (auto item_ : itemList)
	{
		if (item_->Param1 == TEXT("1"))
		{
			WhiteDragonCount += item_->Amount;
		}
		else if (item_->Param1 == TEXT("2"))
		{
			FiveDragonCount += item_->Amount;
		}
		else if (item_->Param1 == TEXT("3"))
		{
			SuperDragonCount += item_->Amount;
		}
	}
}

void URoleEquipInterface::GetIntensifySpar(int32& WhiteSparCount, int32& FiveSparCount, int32& SuperSparCount)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifySpar : kitbatInst!"));
		return;
	}
	TArray<UItemBase*> itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemIntensifySpar"));
	for (auto item_ : itemList)
	{
		if (item_->Param1 == TEXT("1"))
		{
			WhiteSparCount += item_->Amount;
		}
		else if (item_->Param1 == TEXT("2"))
		{
			FiveSparCount += item_->Amount;
		}
		else if (item_->Param1 == TEXT("3"))
		{
			SuperSparCount += item_->Amount;
		}
	}
}

void URoleEquipInterface::GetIntensifyFu(int32& HHFuCount, int32& ZYFuCount, int32& BDFuCount)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifyFu : kitbatInst!"));
		return;
	}
	TArray<UItemBase*> itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemIntensifySymbol"));
	for (auto item_ : itemList)
	{
		if (item_->Param1 == TEXT("1"))
		{
			HHFuCount += item_->Amount;
		}
		else if (item_->Param1 == TEXT("2"))
		{
			ZYFuCount += item_->Amount;
		}
		else if (item_->Param1 == TEXT("3"))
		{
			BDFuCount += item_->Amount;
		}
	}
}

void URoleEquipInterface::GetShuffleWStone(int32& WStoneCount)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetShuffleWStone : kitbatInst!"));
		return;
	}
	TArray<UItemBase*> itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemShuffle"));
	for (auto item_ : itemList)
	{
		if (item_->Param1 == TEXT("1"))
		{
			WStoneCount += item_->Amount;
		}
	}
}

void URoleEquipInterface::GetShuffleBloodFu(int32& BloodFuCount)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetShuffleBloodFu : kitbatInst!"));
		return;
	}
	TArray<UItemBase*> itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemIntensifySymbol"));
	for (auto item_ : itemList)
	{
		if (item_->Param1 == TEXT("4"))
		{
			BloodFuCount += item_->Amount;
		}
	}
}

void URoleEquipInterface::GetRecastCStone(int32& CStoneCount)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetRecastCStone : kitbatInst!"));
		return;
	}
	TArray<UItemBase*> itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemShuffle"));
	for (auto item_ : itemList)
	{
		if (item_->Param1 == TEXT("2"))
		{
			CStoneCount += item_->Amount;
		}
	}
}

void URoleEquipInterface::GetRecastCZFu(int32& CZFuCount)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetRecastCZFu : kitbatInst!"));
		return;
	}
	TArray<UItemBase*> itemList = kitbatInst->GetItemListByItemScript(TEXT("ItemIntensifySymbol"));
	for (auto item_ : itemList)
	{
		if (item_->Param1 == TEXT("5"))
		{
			CZFuCount += item_->Amount;
		}
	}
}

void URoleEquipInterface::EquipBackfire(const FString& EquipUID, const TArray<FString>& Indexs)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::EquipBackfire : GetEntity()!"));
		return;
	}
	if (CanBackFire(EquipUID,Indexs))
	{
		KBEngine::FVariantArray Args;
		KBEngine::FVariantArray Arr;
		for (auto index : Indexs)
		{
			Arr.Add(index);
		}
		Args.Add(EquipUID);
		Args.Add(FVariant(Arr));
		GetEntity()->CellCall(TEXT("doEquipBackfire"), Args);
	}
}

void URoleEquipInterface::GetBackFireCost(const FString& EquipUID, const TArray<FString>& SaveUIDs, int32& WhiteSparCount, int32& FiveSparCount, int32& SuperSparCount, int32& MoneyCost)
{
	MoneyCost = 0;
	WhiteSparCount = 0;
	FiveSparCount = 0;
	SuperSparCount = 0;
	UItemBase* Item = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0))->FindItemByUID(EquipUID);
	UEquip* Equip = Cast<UEquip>(Item);
	if (Equip)
	{
		int32 EquipLv = Equip->Level;
		const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_EQUIP_BACKFIRE_COST);
		if (IsValid(table))
		{
			TArray<FName> RowNames;
			RowNames = table->GetRowNames();
			for (FName RowName : RowNames)
			{
				const FBackFireCost* Data = table->GetRow<FBackFireCost>(RowName);
				if (Data)
				{
					FString Temp = Data->MinMaxLv;
					FString Left;
					FString Right;
					Temp.Split(TEXT("-"), &Left, &Right);
					int32 MinLv = FSTRING_TO_INT(Left);
					int32 MaxLv = FSTRING_TO_INT(Right);
					if ((EquipLv >= MinLv) && (EquipLv < MaxLv) && (SaveUIDs.Num() == Data->BackFireLockCount))
					{
						//MoneyCost = Data->MoneyCost;
						WhiteSparCount = Data->LowMaterialCost;
						FiveSparCount = Data->MediumMaterialCost;
						SuperSparCount = Data->HighMaterialCost;
					}
				}
			}
		}
		
		
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("EquipUID[%s], SaveUIDs.num[%d], CostMoney[%d], WhiteBeadCount[%d], FiveBeadCount[%d]. SuperBeadCount[%d]"), *EquipUID, SaveUIDs.Num(), MoneyCost, WhiteSparCount, FiveSparCount, SuperSparCount);
	}
}

bool URoleEquipInterface::RequestIntensifySaveSlotInfo()
{
	if (IntensifySaveSlotNum)
	{
		return false;
	}
	KBEngine::FVariantArray args;
	CellCall(TEXT("requestIntensifySaveSlotInfo"), args);
	return true;
}
void URoleEquipInterface::CLIENT_OnRequestIntensifySaveSlotInfo(const int32& SlotNum, const FVariant& EQUIP_INTENSIFY_SAVES_1)
{
	FEQUIP_INTENSIFY_SAVES* EquipInfo = new FEQUIP_INTENSIFY_SAVES(EQUIP_INTENSIFY_SAVES_1);
	IntensifySaveSlotNum = SlotNum;
	for (auto data : EquipInfo->datas1)
	{
		IntensifySaveItemMap.Add(data.index1, data.EquipID3);
		IntensifyUIDs.Add(data.index1, INT64_TO_FSTRING(data.EquipUID2));
		TArray<FIntensifyData> TIData;
		TArray<FString> splitArr = UGolbalBPFunctionLibrary::SplitString(data.intensifyDataStr4, false, TEXT("||"));
		for (auto attr : splitArr)
		{
			FIntensifyData IData;
			TArray<FString> ItList = UGolbalBPFunctionLibrary::SplitString(attr, false, TEXT("*"));
			if (ItList.Num() < 2)
			{
				CS3_Warning(TEXT("Intensify info save  err!UID(%s) is not match"), *attr);
				return;
			}
			IData.UID = ItList[0];

			TArray<FString> IsList = UGolbalBPFunctionLibrary::SplitString(ItList[1], false, TEXT("$"));
			if (IsList.Num() < 2)
			{
				CS3_Warning(TEXT("Intensify info save  err!StarLv(%s) is not match"), *attr);
				return;
			}
			IData.StarLevel = EIntensifyLevel(FSTRING_TO_INT(IsList[0]));

			TArray<FString> IpList = UGolbalBPFunctionLibrary::SplitString(IsList[1], false, TEXT(":"));
			if (IpList.IsValidIndex(0))
			{
				IData.MainPropertyStr = IpList[0];
			}
			if (IpList.IsValidIndex(1))
			{
				IData.AttachPropertyStr = IpList[1];
			}
			TIData.Add(IData);
		}
		IntensifySaveInfo.Add(INT64_TO_FSTRING(data.EquipUID2), TIData);
	}
	OnRequestIntensifySaveSlotInfo();
}

void URoleEquipInterface::OnRequestIntensifySaveSlotInfo_Implementation()
{
	
	
}

bool URoleEquipInterface::HasSaveItemIntensify(const FString& ItemUID)
{
	return IntensifySaveInfo.Contains(ItemUID);
}

TArray<FIntensifyData> URoleEquipInterface::GetSaveIntensifyInfoByIndex(const int32& Index)
{
	if (IntensifyUIDs.Contains(Index))
	{
		if (IntensifySaveInfo.Contains(IntensifyUIDs[Index]))
		{
			return IntensifySaveInfo[IntensifyUIDs[Index]];
		}
	}
	TArray<FIntensifyData> IData;
	return IData;
}

TArray<FIntensifyData> URoleEquipInterface::GetSaveIntensifyInfoByUID(const FString& ItemUID, int32& Index)
{
	if (IntensifySaveInfo.Contains(ItemUID))
	{
		for (auto IT = IntensifyUIDs.CreateConstIterator(); IT;++IT)
		{
			if (IT.Value() == ItemUID)
			{
				Index = IT.Key();
				break;
			}
		}
		return IntensifySaveInfo[ItemUID];
	}
	TArray<FIntensifyData> IData;
	Index = -1;
	return IData;
}

void URoleEquipInterface::OpenIntensifySaveSlot(const int32& MoneyCost)
{
	int64 money = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	int64 bindMoney = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
	if (money + bindMoney < MoneyCost)
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(5568);
		return;
	}

	if (bindMoney < MoneyCost)
	{
		//绑金不够的话，是否使用金钱代替
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1322, UGolbalBPFunctionLibrary::GetRichTextMoney((int64)(MoneyCost - bindMoney)), FBtnClick::CreateLambda([this](RT_BTN_TYPE RtType)
		{
			if (RtType == RT_BTN_TYPE::RT_OK)
			{
				KBEngine::FVariantArray args;
				CellCall(TEXT("openIntensifySaveSlot"), args);
			}
		}));
		return;
	}
	KBEngine::FVariantArray args;
	CellCall(TEXT("openIntensifySaveSlot"), args);
}

void URoleEquipInterface::OpenIntensifySaveSlotSuccess_Implementation()
{
	IntensifySaveSlotNum += 1;

}

void URoleEquipInterface::IntensifySaveEquip(const FString& Index, const FString& ItemUID)
{
	if (CanSaveIntensify(Index, ItemUID))
	{
		// 备份栏已满
		if (IntensifyUIDs.Num() == IntensifySaveSlotNum)
		{
			TWeakObjectPtr<URoleEquipInterface> DelayThisPtr(this);
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(1088, FBtnClick::CreateLambda([DelayThisPtr, Index, ItemUID](RT_BTN_TYPE TrType)
			{
				if (DelayThisPtr.IsValid())
				{
					URoleEquipInterface* ThisPtr = DelayThisPtr.Get();
					if (TrType == RT_BTN_TYPE::RT_OK)
					{
						ThisPtr->_OnIntensifySaveEquip(Index, ItemUID);
					}
				}
			}));
			return;
		}
		// 备份同一个装备
		for (auto It = IntensifyUIDs.CreateConstIterator(); It ; ++It)
		{
			if (It.Value().Equals(ItemUID))
			{
				TWeakObjectPtr<URoleEquipInterface> DelayThisPtr(this);
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(1077, FBtnClick::CreateLambda([DelayThisPtr, Index, ItemUID](RT_BTN_TYPE TrType)
				{
					if (DelayThisPtr.IsValid())
					{
						URoleEquipInterface* ThisPtr = DelayThisPtr.Get();
						if (TrType == RT_BTN_TYPE::RT_OK)
						{
							ThisPtr->_OnIntensifySaveEquip(Index, ItemUID);
						}
					}
				}));
				return;
			}
		}
		
		_OnIntensifySaveEquip(Index, ItemUID);
	}
}

void URoleEquipInterface::_OnIntensifySaveEquip(const FString & Index, const FString & ItemUID)
{
	KBEngine::FVariantArray args;
	args.Add(FSTRING_TO_INT(Index));
	args.Add(ItemUID);
	CellCall(TEXT("doEquipIntensifySave"), args);
}

void URoleEquipInterface::OnIntensifySaveSuccess_Implementation(const int32& Index, const FString& ItemUID)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::OnIntensifySaveSuccess_Implementation : kitbatInst!"));
		return;
	}
	UItemBase* Item = kitbatInst->FindItemByUID(ItemUID);
	if (IsValid(Item))
	{
		UEquip* equip = Cast<UEquip>(Item);
		IntensifySaveItemMap.Add(Index, Item->ItemID);
		IntensifyUIDs.Add(Index, ItemUID);
		IntensifySaveInfo.Add(ItemUID, equip->IntensifyArray);
	}
	
}

void URoleEquipInterface::GetIntensifySaveCost(const FString& ItemUID, int32& MoneyCost, int32& BDFuCost)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifySaveCost : kitbatInst!"));
		return;
	}
	UItemBase* Item = kitbatInst->FindItemByUID(ItemUID);
	if (!IsValid(Item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifySaveCost : Item!"));
		return;
	}

	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_EQUIP_RESTORE_COST);
	if (IsValid(table))
	{
		TArray<FIntensifyRestoreCost*> AllConfig;
		table->GetAllRows(AllConfig);
		for (auto config_ : AllConfig)
		{
			TArray<FString> lvList = UGolbalBPFunctionLibrary::SplitString(config_->MinMaxLv, false, TEXT("-"));
			if (lvList.Num() >= 2)
			{
				if (Item->Level >= FSTRING_TO_INT(lvList[0]) && Item->Level <= FSTRING_TO_INT(lvList[1]))
				{
					MoneyCost = config_->SaveMoneyCost;
					BDFuCost = config_->SaveBeidouFuCost;
					return;
				}
			}
		}
	}
}

void URoleEquipInterface::IntensifyRestoreEquip(const FString& ItemUID)
{
	if (CanRestoreIntensify(ItemUID))
	{
		KBEngine::FVariantArray args;
		args.Add(ItemUID);
		CellCall(TEXT("doEquipIntensifyRestore"), args);
	}
}

void URoleEquipInterface::OnIntensifyRestoreSuccess_Implementation(const FString& ItemUID)
{
	int32 index = -1;
	for (auto IT = IntensifyUIDs.CreateConstIterator(); IT; ++IT)
	{
		if (IT.Value() == ItemUID)
		{
			index = IT.Key();
			break;
		}
	}
	if (index != -1)
	{
		IntensifyUIDs.Remove(index);
		if (IntensifySaveItemMap.Contains(index))
		{
			IntensifySaveItemMap.Remove(index);
		}
	}
	if (IntensifySaveInfo.Contains(ItemUID))
	{
		IntensifySaveInfo.Remove(ItemUID);
	}
}

void URoleEquipInterface::GetIntensifyRestoreCost(const FString& ItemUID, int32& MoneyCost, int32& BDFuCost)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifyRestoreCost : kitbatInst!"));
		return;
	}
	UItemBase* Item = kitbatInst->FindItemByUID(ItemUID);
	if (!IsValid(Item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetIntensifyRestoreCost : Item!"));
		return;
	}

	const UConfigTable* table =(Cast<UCfgManager>(UGolbalBPFunctionLibrary::CfgManager()))->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_EQUIP_RESTORE_COST);
	if (IsValid(table))
	{
		TArray<FIntensifyRestoreCost*> AllConfig;
		table->GetAllRows(AllConfig);
		for (auto config_ : AllConfig)
		{
			TArray<FString> lvList = UGolbalBPFunctionLibrary::SplitString(config_->MinMaxLv, false, TEXT("-"));
			if (lvList.Num() >= 2)
			{
				if (Item->Level >= FSTRING_TO_INT(lvList[0]) && Item->Level <= FSTRING_TO_INT(lvList[1]))
				{
					MoneyCost = config_->RestoreMoneyCost;
					BDFuCost = config_->RestoreBeidouFuCost;
					return;
				}
			}
		}
	}
}

void URoleEquipInterface::ShuffleEquip(const FString& EquipUID, const TArray<int32>& LockProps, const bool& UseYBToStone, const bool& UseYBToFu)
{
	bool bYbToStone, bYbToFu;
	if (CanShuffle(EquipUID,LockProps,UseYBToStone,UseYBToFu,bYbToStone,bYbToFu))
	{
		KBEngine::FVariantArray args;
		args.Add(EquipUID);
		args.Add(UGolbalBPFunctionLibrary::ListToFVariant(LockProps));
		args.Add(int(bYbToStone));
		args.Add(int(bYbToFu));
		CellCall(TEXT("shuffleEquip"), args);
	}
}

void URoleEquipInterface::OnShuffleEquip_Implementation(const FString& EquipUID, const FString& ShuffleProps)
{
	
}

void URoleEquipInterface::ReplaceShufflePro(const FString& EquipUID)
{
	KBEngine::FVariantArray args;
	args.Add(EquipUID);
	CellCall(TEXT("replaceShufflePro"), args);
}

void URoleEquipInterface::OnShuffleEquipSuccess_Implementation(const FString& EquipUID)
{

}

void URoleEquipInterface::GetShuffleCost(const FString& EquipUID, const int32 LockNum, int32& MoneyCost, int32& WashStone, int32& BloodFu, int32& YBrepStone, int32& YBrepFu)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetShuffleCost : kitbatInst!"));
		return;
	}
	UItemBase* Item = kitbatInst->FindItemByUID(EquipUID);
	if (!IsValid(Item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetShuffleCostt : Item!"));
		return;
	}

	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SHUFFLE_TYPE_DATA);
	if (IsValid(table))
	{
		TArray<FShuffleCost*> AllConfig;
		table->GetAllRows(AllConfig);
		for (auto config_ : AllConfig)
		{
			TArray<FString> lvList = UGolbalBPFunctionLibrary::SplitString(config_->MinMaxLv, false, TEXT("-"));
			if (lvList.Num() >= 2)
			{
				if (Item->Level >= FSTRING_TO_INT(lvList[0]) && Item->Level <= FSTRING_TO_INT(lvList[1]) && config_->LockProNum == LockNum)
				{
					MoneyCost = config_->MoneyCost;
					WashStone = config_->WashStone;
					BloodFu = config_->BloodFu;
					YBrepStone = config_->YBReplaceStone;
					YBrepFu = config_->YBReplaceFu;
					return;
				}
			}
		}
	}
}

void URoleEquipInterface::RecastEquip(const FString& EquipUID, const TArray<int32>& LockProps, const bool& UseYBToStone, const bool& UseYBToFu)
{
	bool bYbToStone, bYbToFu;
	if (CanRecast(EquipUID,LockProps,UseYBToStone,UseYBToFu,bYbToStone,bYbToFu))
	{
		KBEngine::FVariantArray args;
		args.Add(EquipUID);
		args.Add(UGolbalBPFunctionLibrary::ListToFVariant(LockProps));
		args.Add(int32(bYbToStone));
		args.Add(int32(bYbToFu));
		CellCall(TEXT("recastEquip"), args);
	}
}

void URoleEquipInterface::OnRecastEquipSuccess_Implementation(const FString& EquipUID)
{

}

void URoleEquipInterface::GetRecastCost(const FString& EquipUID, const int32 LockNum, int32& MoneyCost, int32& RecastStone, int32& RecastFu, int32& YBrepStone, int32& YBrepFu)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetRecastCost : kitbatInst!"));
		return;
	}
	UItemBase* Item = kitbatInst->FindItemByUID(EquipUID);
	if (!IsValid(Item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetRecastCost : Item!"));
		return;
	}

	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_RECAST_COST_DATA);
	if (IsValid(table))
	{
		TArray<FRecastCost*> AllConfig;
		table->GetAllRows(AllConfig);
		for (auto config_ : AllConfig)
		{
			TArray<FString> lvList = UGolbalBPFunctionLibrary::SplitString(config_->MinMaxLv, false, TEXT("-"));
			if (lvList.Num() >= 2)
			{
				if (Item->Level >= FSTRING_TO_INT(lvList[0]) && Item->Level <= FSTRING_TO_INT(lvList[1]) && config_->ProtectProNum == LockNum)
				{
					MoneyCost = config_->MoneyCost;
					RecastStone = config_->RecastStone;
					RecastFu = config_->RecastFu;
					YBrepStone = config_->YBReplaceStone;
					YBrepFu = config_->YBReplaceFu;
					return;
				}
			}
		}
	}
}

void URoleEquipInterface::BiographyEquip(const FString& SrcEquipUID, const FString& DstEquipUID, const bool& UseNewPro, const TArray<FString>& BiographyList)
{
	if (CanBiography(SrcEquipUID, DstEquipUID, UseNewPro, BiographyList))
	{
		KBEngine::FVariantArray args;
		KBEngine::FVariantArray arr;
		for (auto Fs : BiographyList)
		{
			arr.Add(Fs);
		}
		args.Add(SrcEquipUID);
		args.Add(DstEquipUID);
		args.Add(int32(UseNewPro));
		args.Add(arr);
		CellCall(TEXT("transferIntensifyEquip"), args);
	}
}

void URoleEquipInterface::OnBiographyEquipSuccess_Implementation()
{

}

void URoleEquipInterface::GetBiographyCost(const FString& DstEquipUID, const int32 LockNum, int32& MoneyCost, int32& WhiteSparCount, int32& FiveSparCount, int32& SuperSparCount)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetBiographyCost : kitbatInst!"));
		return;
	}
	UItemBase* Item = kitbatInst->FindItemByUID(DstEquipUID);
	if (!IsValid(Item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetBiographyCost : Item!"));
		return;
	}

	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BIOGRAPHY_COST_DATA);
	if (IsValid(table))
	{
		TArray<FTransferIntensifyCost*> AllConfig;
		table->GetAllRows(AllConfig);
		for (auto config_ : AllConfig)
		{
			TArray<FString> lvList = UGolbalBPFunctionLibrary::SplitString(config_->MinMaxLv, false, TEXT("-"));
			if (lvList.Num() >= 2)
			{
				if (Item->Level >= FSTRING_TO_INT(lvList[0]) && Item->Level <= FSTRING_TO_INT(lvList[1]) && config_->LockCount == LockNum)
				{
					MoneyCost = config_->MoneyCost;
					WhiteSparCount = config_->LowMaterialCost;
					FiveSparCount = config_->MediumMaterialCost;
					SuperSparCount = config_->HighMaterialCost;
					return;
				}
			}
		}
	}
}

void URoleEquipInterface::GetEquipPropMax(UEquip* Equip, const int32& PropertyID, int32& Max)
{
	Max = 0;
	int32 levelSec = int(Equip->Level / 10) * 10;
	TArray<int32> profress = Equip->GetReqClasses();
	bool BOnlyOnePrefress = profress.Num() == 1;
	int32 modelPartType = Equip->GetWieldOrder();
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_EQUIP_PROPERTY_DATA);
	if (IsValid(table))
	{
		TArray<FEquipPropertyInterval*> AllConfig;
		table->GetAllRows(AllConfig);
		for (auto propertyInt : AllConfig)
		{
			if (propertyInt->LevelSection == levelSec && propertyInt->ModelPart == modelPartType && PropertyID == propertyInt->PropertyID)
			{
				if (BOnlyOnePrefress)
				{
					if (propertyInt->Class == profress[0])
					{
						Max = propertyInt->Max;
						return;
					}
				}
				else
				{
					if (propertyInt->Class == 0)
					{
						Max = propertyInt->Max;
						return;
					}
				}
				
				
			}
		}
	}
}
	

void URoleEquipInterface::GetEquipShuffleShow(const FString& EquipUID, TArray<FEquipShuffleData>& ShuffleData)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::GetEquipShuffleShow : kitbatInst!"));
		return;
	}
	UItemBase* Item = kitbatInst->FindItemByUID(EquipUID);
	if (Item)
	{
		UEquip* equip = Cast<UEquip>(Item);
		TArray<FString> SStri = UGolbalBPFunctionLibrary::SplitString(equip->AttachPropertiesStr);
		for (auto S : SStri)
		{
			TArray<FString> T = UGolbalBPFunctionLibrary::SplitString(S, false, TEXT("#"));
			if (T.Num()>=2)
			{
				FEquipShuffleData ESData;
				ESData.PropertyID = FSTRING_TO_INT(T[0]);
				ESData.PropertyValue = FSTRING_TO_INT(T[1]);
				int32 Max;
				GetEquipPropMax(equip, ESData.PropertyID, Max);
				ESData.Max = Max;
				ShuffleData.Add(ESData);
			}
		}
	}
}

void URoleEquipInterface::OpenForgeEquip_Implementation(const int32& NPCID)
{

}

bool URoleEquipInterface::HasEnoughStone(int32 StoneNum)
{
	int32 lingshi = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("lingshi"));
	if (lingshi >= StoneNum)
	{
		return true;
	}
	StoneNum -= lingshi;
	int32 xianshi = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("xianshi"));
	return xianshi >= StoneNum;

}

void URoleEquipInterface::QueryEquipComposeDatas()
{
	KBEngine::FVariantArray args;
	CellCall(TEXT("CELL_requestEquipCompose"), args);
}

void URoleEquipInterface::CLIENT_onRequestEquipCompose_Implementation(const TArray<int32>& EquipBprint)
{
	EquipComposeInfo.Empty();
	UCfgManager* cfgMgr = UGolbalBPFunctionLibrary::CfgManager();
	if (cfgMgr)
	{
		const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_EQUIP_COMPOSE_DATA);
		if (IsValid(table))
		{
			for (int32 equipid : EquipBprint)
			{
				if (equipid == 0)continue;
				const FEquipComposeCost* cost = table->GetRow<FEquipComposeCost>(FSTRING_TO_FNAME(INT_TO_FSTRING(equipid)));
				if (cost)
				{
					EquipComposeInfo.Add(equipid, cost);
				}
			}
		}
	}
	//设置装备部位对应有哪些装备ID数据
	SetEquipBuildPartDatas();
}

void URoleEquipInterface::SetEquipBuildPartDatas()
{
	TArray<int32> EquipIDs;
	EquipPartDatas.Empty();
	EquipComposeInfo.GetKeys(EquipIDs);
	for (auto& EquipID : EquipIDs)
	{
		AddEquipBuildPartData(EquipID);
	}
}

void URoleEquipInterface::AddEquipBuildPartData(int32 EquipID)
{
	UItemBase* ItemBase = UItemFactory::GetItemByID(EquipID);
	MODEL_PART_TYPE PartType;
	if (GetEquipBuildPartType(EquipID, PartType))
	{
		if (EquipPartDatas.Contains(PartType))
		{
			EquipPartDatas[PartType].Add(EquipID);
		}
		else
		{
			TArray<int32> TempEquipIDs;
			TempEquipIDs.Add(EquipID);
			EquipPartDatas.Emplace(PartType, TempEquipIDs);
		}
	}
}

TArray<int32> URoleEquipInterface::GetEquipBuildIDList(MODEL_PART_TYPE PartType)
{
	TArray<int32> EquipIDList;
	if (EquipPartDatas.Contains(PartType))
	{
		return EquipPartDatas[PartType];
	}
	return EquipIDList;
}

bool URoleEquipInterface::GetEquipBuildPartType(int32 EquipID, MODEL_PART_TYPE& PartType)
{
	UItemBase* ItemBase = UItemFactory::GetItemByID(EquipID);
	if (IsValid(ItemBase) && ItemBase->IsEquip())
	{
		UEquip* Equip = Cast<UEquip>(ItemBase);
		if (IsValid(Equip))
		{
			PartType = Equip->GetModelPartType();
			//左手戒指右手戒指都显示戒指
			if (PartType == MODEL_PART_TYPE::MODEL_PART_LHAND_RING || PartType == MODEL_PART_TYPE::MODEL_PART_RHAND_RING)
			{
				PartType = MODEL_PART_TYPE::MODEL_PART_LHAND_RING;
			}
			//左手武器、右手武器、双手武器都显示武器
			else if (PartType == MODEL_PART_TYPE::MODEL_PART_LWEAPON || PartType == MODEL_PART_TYPE::MODEL_PART_RWEAPON || PartType == MODEL_PART_TYPE::MODEL_PART_BWEAPON)
			{
				PartType = MODEL_PART_TYPE::MODEL_PART_LWEAPON;
			}
			return true;
		}
	}
	return false;
}

void URoleEquipInterface::CLIENT_onStudyEquipCompose_Implementation(const int32& EquipID)
{
	UCfgManager* cfgMgr = UGolbalBPFunctionLibrary::CfgManager();
	if (cfgMgr)
	{
		const UConfigTable* table = cfgMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_EQUIP_COMPOSE_DATA);
		if (IsValid(table))
		{
			const FEquipComposeCost* cost = table->GetRow<FEquipComposeCost>(FSTRING_TO_FNAME(INT_TO_FSTRING( EquipID)));
			if (cost)
			{
				EquipComposeInfo.Add(EquipID, cost);
				//增加装备打造图纸部位类型对应的装备数据
				AddEquipBuildPartData(EquipID);
			}
		}
	}
}

void URoleEquipInterface::RequestEquipCompose(const int32& EquipID, bool bUseUnbind)
{
	if (EquipComposeInfo.Contains(EquipID))
	{
		KBEngine::FVariantArray args;
		args.Add(EquipID);
		args.Add(int32(bUseUnbind));
		CellCall(TEXT("CELL_composeEquip"), args);
	}
	
}

void URoleEquipInterface::CLIENT_onSuccessComposeEquip_Implementation(const int32& EquipID)
{

}

int32 URoleEquipInterface::GetComposeEquipNum(const int32& EquipID, const bool& UseUnBind)
{
	if (EquipComposeInfo.Contains(EquipID))
	{
		int32 num(0);
		const FEquipComposeCost* cost = EquipComposeInfo[EquipID];

		URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
		
		FIND_BINDTYPE_ENUM bindType = UseUnBind ? FIND_BINDTYPE_ENUM::NONE_BIND : FIND_BINDTYPE_ENUM::INGOREBIND;
		num = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, cost->srcEquip, bindType);
		int32 Material1 = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, cost->material_1, bindType);
		num = FMath::Min(num, Material1 / cost->mNum_1);
		int32 Material2 = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, cost->material_2, bindType);
		num = FMath::Min(num, Material2 / cost->mNum_2);
		int32 Material3 = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, cost->material_3, bindType);
		num = FMath::Min(num, Material3 / cost->mNum_3);
		int32 Material4 = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, cost->material_4, bindType);
		num = FMath::Min(num, Material4 / cost->mNum_4);
		return num;
	}
	return 0;
}

FEquipComposeCost URoleEquipInterface::GetComposeEquipData(const int32& EquipID)
{
	if (EquipComposeInfo.Contains(EquipID))
	{
		return *EquipComposeInfo[EquipID];
		
	}
	FEquipComposeCost Data;
	return  Data;
}

void URoleEquipInterface::QueryTargetEquipInfo(const int32& TargetID)
{
	KBEngine::FVariantArray args;
	args.Add(TargetID);
	CellCall(TEXT("CELL_queryTargetEquipInfo"), args);
}

void URoleEquipInterface::RemoteQueryTargetEquipInfo(const FString& TargetName)
{
	KBEngine::FVariantArray args;
	args.Add(TargetName);
	BaseCall(TEXT("BASE_remoteQueryTargetEquipInfo"), args);
}

void URoleEquipInterface::CLIENT_OnQueryTargetEquipInfo(const FVariant& equipFixedDict, const FVariant& roleFixedDict)
{
	FEQUIP_INFO_DICT * EQUIP_INFO_DICT_1 = new FEQUIP_INFO_DICT(equipFixedDict);
	FROLE_PROPERTY_INFO * ROLE_PROPERTY_INFO_1 = new FROLE_PROPERTY_INFO(roleFixedDict);
	TargetEquipArry.Empty();
	UItemFactory* ItemFactory = UUECS3GameInstance::Instance->ItemFactory;
	if (!IsValid(ItemFactory))return;
	for (auto EquipInfo : EQUIP_INFO_DICT_1->Datas1)
	{
		UItemBase* equip = ItemFactory->GetItemByID(EquipInfo.itemID1);
		if(!IsValid(equip))continue;
		equip->SetDynamicProperty(EquipInfo.combatPower2, EquipInfo.attackPropertiesStr4, EquipInfo.attachPropertiesStr5, EquipInfo.intensifyDataStr6, EquipInfo.hardiness3);
		TargetEquipArry.Add(equip);
	}
	TargetPropertyInfo.Name = ROLE_PROPERTY_INFO_1->name;
	TargetPropertyInfo.camp = ROLE_PROPERTY_INFO_1->camp1;
	TargetPropertyInfo.gender = ROLE_PROPERTY_INFO_1->gender2;
	TargetPropertyInfo.profession = ROLE_PROPERTY_INFO_1->profession3;
	TargetPropertyInfo.level = ROLE_PROPERTY_INFO_1->level4;
	TargetPropertyInfo.xiuwei = ROLE_PROPERTY_INFO_1->xiuwei5;
	TargetPropertyInfo.jingjieLevel = ROLE_PROPERTY_INFO_1->jingjieLevel6;
	TargetPropertyInfo.killingValue = ROLE_PROPERTY_INFO_1->killingValue7;
	TargetPropertyInfo.potential = ROLE_PROPERTY_INFO_1->potential8;
	TargetPropertyInfo.combatPower = ROLE_PROPERTY_INFO_1->combatPower9;
	TargetPropertyInfo.strength = ROLE_PROPERTY_INFO_1->strength10;
	TargetPropertyInfo.dexterity = ROLE_PROPERTY_INFO_1->dexterity11;
	TargetPropertyInfo.intellect = ROLE_PROPERTY_INFO_1->intellect12;
	TargetPropertyInfo.corporeity = ROLE_PROPERTY_INFO_1->corporeity13;
	TargetPropertyInfo.discern = ROLE_PROPERTY_INFO_1->discern14;
	TargetPropertyInfo.speed = ROLE_PROPERTY_INFO_1->speed15;
	TargetPropertyInfo.HP = ROLE_PROPERTY_INFO_1->HP16;
	TargetPropertyInfo.HP_Max = ROLE_PROPERTY_INFO_1->HP_Max17;
	TargetPropertyInfo.MP = ROLE_PROPERTY_INFO_1->MP18;
	TargetPropertyInfo.MP_Max = ROLE_PROPERTY_INFO_1->MP_Max19;
	TargetPropertyInfo.gangQiValue = ROLE_PROPERTY_INFO_1->gangQiValue20;
	TargetPropertyInfo.gangQiValue_Max = ROLE_PROPERTY_INFO_1->gangQiValue_Max21;
	TargetPropertyInfo.damage = ROLE_PROPERTY_INFO_1->damage22;
	TargetPropertyInfo.magic_damage = ROLE_PROPERTY_INFO_1->magic_damage23;
	TargetPropertyInfo.armor = ROLE_PROPERTY_INFO_1->armor24;
	TargetPropertyInfo.magic_armor = ROLE_PROPERTY_INFO_1->magic_armor25;
	TargetPropertyInfo.gangQi_damagePoint = ROLE_PROPERTY_INFO_1->gangQi_damagePoint26;
	TargetPropertyInfo.gangQi_armorPoint = ROLE_PROPERTY_INFO_1->gangQi_armorPoint27;
	TargetPropertyInfo.criticalstrike = ROLE_PROPERTY_INFO_1->criticalstrike28;
	TargetPropertyInfo.parry = ROLE_PROPERTY_INFO_1->parry29;
	TargetPropertyInfo.hitrate = ROLE_PROPERTY_INFO_1->hitrate30;
	TargetPropertyInfo.dodgerate = ROLE_PROPERTY_INFO_1->dodgerate31;
	TargetPropertyInfo.healingrate = ROLE_PROPERTY_INFO_1->healingrate32;
	TargetPropertyInfo.cure = ROLE_PROPERTY_INFO_1->cure33;
	TargetPropertyInfo.ice_damage = ROLE_PROPERTY_INFO_1->ice_damage34;
	TargetPropertyInfo.fire_damage = ROLE_PROPERTY_INFO_1->fire_damage35;
	TargetPropertyInfo.thunder_damage = ROLE_PROPERTY_INFO_1->thunder_damage36;
	TargetPropertyInfo.xuan_damage = ROLE_PROPERTY_INFO_1->xuan_damage37;
	TargetPropertyInfo.ice_armor = ROLE_PROPERTY_INFO_1->ice_armor38;
	TargetPropertyInfo.fire_armor = ROLE_PROPERTY_INFO_1->fire_armor39;
	TargetPropertyInfo.thunder_armor = ROLE_PROPERTY_INFO_1->thunder_armor40;
	TargetPropertyInfo.xuan_armor = ROLE_PROPERTY_INFO_1->xuan_armor41;
	TargetPropertyInfo.damage_ignore = ROLE_PROPERTY_INFO_1->damage_ignore42;
	TargetPropertyInfo.magic_damage_ignore = ROLE_PROPERTY_INFO_1->magic_damage_ignore43;
	TargetPropertyInfo.armor_ignore = ROLE_PROPERTY_INFO_1->armor_ignore44;
	TargetPropertyInfo.magic_armor_ignore = ROLE_PROPERTY_INFO_1->magic_armor_ignore45;
	TargetPropertyInfo.criticalstrike_ignore = ROLE_PROPERTY_INFO_1->criticalstrike_ignore46;
	TargetPropertyInfo.parry_ignore = ROLE_PROPERTY_INFO_1->parry_ignore47;
	TargetPropertyInfo.hitrate_ignore = ROLE_PROPERTY_INFO_1->hitrate_ignore48;
	TargetPropertyInfo.dodgerate_ignore = ROLE_PROPERTY_INFO_1->dodgerate_ignore49;
	TargetPropertyInfo.ice_damage_ignore = ROLE_PROPERTY_INFO_1->ice_damage_ignore50;
	TargetPropertyInfo.fire_damage_ignore = ROLE_PROPERTY_INFO_1->fire_damage_ignore51;
	TargetPropertyInfo.thunder_damage_ignore = ROLE_PROPERTY_INFO_1->thunder_damage_ignore52;
	TargetPropertyInfo.xuan_damage_ignore = ROLE_PROPERTY_INFO_1->xuan_damage_ignore53;
	TargetPropertyInfo.ice_armor_ignore = ROLE_PROPERTY_INFO_1->ice_armor_ignore54;
	TargetPropertyInfo.fire_armor_ignore = ROLE_PROPERTY_INFO_1->fire_armor_ignore55;
	TargetPropertyInfo.thunder_armor_ignore = ROLE_PROPERTY_INFO_1->thunder_armor_ignore56;
	TargetPropertyInfo.xuan_armor_ignore = ROLE_PROPERTY_INFO_1->xuan_armor_ignore57;
	TargetPropertyInfo.depress_resist = ROLE_PROPERTY_INFO_1->depress_resist58;
	TargetPropertyInfo.hitback_resist = ROLE_PROPERTY_INFO_1->hitback_resist59;
	TargetPropertyInfo.control_resist = ROLE_PROPERTY_INFO_1->control_resist60;
	TargetPropertyInfo.insane_resist = ROLE_PROPERTY_INFO_1->insane_resist61;
	TargetPropertyInfo.feats = ROLE_PROPERTY_INFO_1->feats62;
	OnQueryTargetEquipInfoCB();
}

void URoleEquipInterface::InitBlueCB()
{
	ArrBlueFunc.Add("OnIntensifySuccess");
	ArrBlueFunc.Add("OnBackfireSuccess");
	ArrBlueFunc.Add("OnIntensifySaveSuccess");
	ArrBlueFunc.Add("OnIntensifyRestoreSuccess");
	ArrBlueFunc.Add("OnRequestIntensifySaveSlotInfo");
	ArrBlueFunc.Add("OpenIntensifySaveSlotSuccess");
	ArrBlueFunc.Add("OnShuffleEquip");
	ArrBlueFunc.Add("OnShuffleEquipSuccess");
	ArrBlueFunc.Add("OnRecastEquipSuccess");
	ArrBlueFunc.Add("OnBiographyEquipSuccess");
	ArrBlueFunc.Add("OpenForgeEquip");
	ArrBlueFunc.Add("CLIENT_onEquipWieldCb");
	ArrBlueFunc.Add("CLIENT_onEquipUnWieldCb");
	ArrBlueFunc.Add("CLIENT_onRequestEquipCompose");
	ArrBlueFunc.Add("CLIENT_onSuccessComposeEquip");
	ArrBlueFunc.Add("CLIENT_onStudyEquipCompose");
	Supper::InitBlueCB();
}

void URoleEquipInterface::onLeaveWorld()
{
	IntensifySaveSlotNum = 0;
	IntensifySaveItemMap.Empty();
	IntensifySaveInfo.Empty();
	IntensifyUIDs.Empty();
	EquipComposeInfo.Empty();
	EquipPartDatas.Empty();
	Super::onLeaveWorld();
}


bool URoleEquipInterface::CanIntensify(const FString& EquipUID, const int32& dstLv, const int32& AttachItemID)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::CanIntensify : kitbatInst!"));
		return false;
	}
	UItemBase* Item = kitbatInst->FindItemByUID(EquipUID);
	UEquip* Equip = Cast<UEquip>(Item);
	if (IsValid(Equip))
	{
		//强化到最高级，不能再继续强化
		if (Equip->GetMaxIntensifyLv() == Equip->GetCurrIntensifyLv())
		{
			return false;
		}
		int32 CostMoney = 0;
		int32 WhiteXuanJingCount(0), FiveXuanJingCount(0), SuperXuanJingCount(0);
		int32 OwnXuanJingCount(0), OwnFiveXuanJingCount(0), OwnSuperXuanJingCount(0);
		GetSumIntensifyCost(EquipUID, dstLv, CostMoney, WhiteXuanJingCount, FiveXuanJingCount, SuperXuanJingCount);
		GetIntensifyCrystal(OwnXuanJingCount, OwnFiveXuanJingCount, OwnSuperXuanJingCount);
		if (!((OwnXuanJingCount >= WhiteXuanJingCount) && (OwnFiveXuanJingCount >= FiveXuanJingCount) && (OwnSuperXuanJingCount >= SuperXuanJingCount)))
		{
			UGolbalBPFunctionLibrary::StatusMessage(1046, TEXT(""));
			return false;
		}

		if (nullptr != GetEntity())
		{
			//金钱不足
			int64 money = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
			int64 bindMoney = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
			if (money + bindMoney < CostMoney)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(1066);
				return false;
			}

			if (bindMoney < CostMoney)
			{
				//绑金不够的话，是否使用金钱代替
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(1322, UGolbalBPFunctionLibrary::GetRichTextMoney((int64)(CostMoney - bindMoney)), FBtnClick::CreateLambda([this, EquipUID, dstLv, AttachItemID](RT_BTN_TYPE RtType)
				{
					if (RtType == RT_BTN_TYPE::RT_OK)
					{
						KBEngine::FVariantArray Args;
						Args.Add(EquipUID);
						Args.Add(dstLv);
						Args.Add(AttachItemID);
						GetEntity()->CellCall(TEXT("doEquipIntensify"), Args);
					}
				}));
				return false;
			}
			return true;
		}
	}
	return false;
}

bool URoleEquipInterface::CanBackFire(const FString& EquipUID, const TArray<FString>& SaveUIDs)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst) || nullptr == GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::CanBackFire : kitbatInst!"));
		return false;
	}

	int32 OwnWhiteSparCount(0), OwnFiveSparCount(0), OwnSuperSparCount(0);
	int32 WhiteSparCount(0), FiveSparCount(0), SuperSparCount(0), MoneyCost(0);
	GetBackFireCost(EquipUID, SaveUIDs, WhiteSparCount, FiveSparCount, SuperSparCount, MoneyCost);
	
	GetIntensifyFu(OwnWhiteSparCount, OwnFiveSparCount, OwnSuperSparCount);
	if (OwnWhiteSparCount < WhiteSparCount || OwnFiveSparCount < FiveSparCount || OwnSuperSparCount < SuperSparCount)
	{
		UGolbalBPFunctionLibrary::StatusMessage(1048, TEXT(""));
		return false;
	}

	int64 money = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	int64 bindMoney = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
	if (money + bindMoney < MoneyCost)
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1034);
		return false;
	}

	if (bindMoney < MoneyCost)
	{
		//绑金不够的话，是否使用金钱代替
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1322, UGolbalBPFunctionLibrary::GetRichTextMoney((int64)(MoneyCost - bindMoney)), FBtnClick::CreateLambda([this, EquipUID, SaveUIDs](RT_BTN_TYPE RtType)
		{
			if (RtType == RT_BTN_TYPE::RT_OK)
			{
				KBEngine::FVariantArray Args;
				KBEngine::FVariantArray Arr;
				for (auto index : SaveUIDs)
				{
					Arr.Add(index);
				}
				Args.Add(EquipUID);
				Args.Add(FVariant(Arr));
				GetEntity()->CellCall(TEXT("doEquipBackfire"), Args);
			}
		}));
		return false;
	}
	return true;
}

bool URoleEquipInterface::CanSaveIntensify(const FString& Index, const FString& EquipUID)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst) || nullptr == GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::CanSaveIntensify : kitbatInst!"));
		return false;
	}

	int32 OwnBDFuCost(0);
	int32 temp1(0), temp2(0), BDFuCost(0), MoneyCost(0);
	GetIntensifySaveCost(EquipUID, MoneyCost, BDFuCost);

	GetIntensifyFu(temp1, temp2, OwnBDFuCost);
	if (OwnBDFuCost < BDFuCost)
	{
		UGolbalBPFunctionLibrary::StatusMessage(1050, TEXT(""));
		return false;
	}

	int64 money = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	int64 bindMoney = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
	if (money + bindMoney < MoneyCost)
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1038);
		return false;
	}

	if (bindMoney < MoneyCost)
	{
		//绑金不够的话，是否使用金钱代替
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1322, UGolbalBPFunctionLibrary::GetRichTextMoney((int64)(MoneyCost - bindMoney)), FBtnClick::CreateLambda([this, Index, EquipUID](RT_BTN_TYPE RtType)
		{
			if (RtType == RT_BTN_TYPE::RT_OK)
			{
				_OnIntensifySaveEquip(Index, EquipUID);
			}
		}));
		return false;
	}
	
	return true;
}

bool URoleEquipInterface::CanRestoreIntensify(const FString& EquipUID)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst) || nullptr == GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::CanRestoreIntensify : kitbatInst!"));
		return false;
	}

	int32 OwnBDFuCost(0);
	int32 temp1(0), temp2(0), BDFuCost(0), MoneyCost(0);
	GetIntensifyRestoreCost(EquipUID, MoneyCost, BDFuCost);

	GetIntensifyFu(temp1, temp2, OwnBDFuCost);
	if (OwnBDFuCost < BDFuCost)
	{
		UGolbalBPFunctionLibrary::StatusMessage(1079, TEXT(""));
		return false;
	}

	int64 money = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	int64 bindMoney = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
	if (money + bindMoney < MoneyCost)
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1042);
		return false;
	}
	
	if (bindMoney < MoneyCost)
	{
		//绑金不够的话，是否使用金钱代替
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1322, UGolbalBPFunctionLibrary::GetRichTextMoney((int64)(MoneyCost - bindMoney)), FBtnClick::CreateLambda([this, EquipUID](RT_BTN_TYPE RtType)
		{
			if (RtType == RT_BTN_TYPE::RT_OK)
			{
				KBEngine::FVariantArray args;
				args.Add(EquipUID);
				CellCall(TEXT("doEquipIntensifyRestore"), args);
			}
		}));
		return false;
	}
	return true;
}

bool URoleEquipInterface::CanShuffle(const FString& EquipUID, const TArray<int32>& LockProps, const bool& UseYBToStone, const bool& UseYBToFu, bool& BYbToStone, bool& BYbToFu)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst) || nullptr == GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::CanShuffle : kitbatInst!"));
		return false;
	}

	UItemBase* itemB = kitbatInst->FindItemByUID(EquipUID);
	if (!IsValid(itemB))
	{
		UGolbalBPFunctionLibrary::StatusMessage(593, TEXT(""));
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::CanShuffle : itemB!"));
		return false;
	}
	if (itemB->Level < EQUIP_SHUFFLE_MIX_LEVEL)
	{
		UGolbalBPFunctionLibrary::StatusMessage(1053, TEXT(""));
		return false;
	}
	if (itemB->IsWhite())
	{
		UGolbalBPFunctionLibrary::StatusMessage(1052, TEXT(""));
		return false;
	}
	int32 OwnBloodFu(0), OwnWStong(0);
	int32 BloodFu(0), WastStone(0), MoneyCost(0), YBRepStone(0), YBRepFu(0);
	GetShuffleCost(EquipUID, LockProps.Num(), MoneyCost, WastStone, BloodFu, YBRepStone, YBRepFu);
	
	GetShuffleWStone(OwnWStong);
	if (OwnWStong < WastStone)
	{
		BYbToStone = UseYBToStone;
		if (!UseYBToStone || !HasEnoughStone(YBRepStone))
		{
			UGolbalBPFunctionLibrary::StatusMessage(1064, TEXT(""));
			return false;
		}
		else
		{
			YBRepFu += YBRepStone;
		}
		
	}
	else
	{
		BYbToStone = false;					// 如果消耗足够，则为false
	}
	GetShuffleBloodFu(OwnBloodFu);
	if (OwnBloodFu < BloodFu)
	{
		BYbToStone = UseYBToFu;
		if (!UseYBToStone || !HasEnoughStone(YBRepFu))
		{
			UGolbalBPFunctionLibrary::StatusMessage(1063, TEXT(""));
			return false;
		}
	}
	else
	{
		BYbToFu = false;
	}

	int64 money = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	int64 bindMoney = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
	if (money + bindMoney < MoneyCost)
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1096);
		return false;
	}

	if (bindMoney < MoneyCost)
	{
		//绑金不够的话，是否使用金钱代替
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1322, UGolbalBPFunctionLibrary::GetRichTextMoney((int64)(MoneyCost - bindMoney)), FBtnClick::CreateLambda([this, EquipUID, LockProps, BYbToStone, BYbToFu](RT_BTN_TYPE RtType)
		{
			if (RtType == RT_BTN_TYPE::RT_OK)
			{
				KBEngine::FVariantArray args;
				args.Add(EquipUID);
				args.Add(UGolbalBPFunctionLibrary::ListToFVariant(LockProps));
				args.Add(int(BYbToStone));
				args.Add(int(BYbToFu));
				CellCall(TEXT("shuffleEquip"), args);
			}
		}));
		return false;
	}
	return true;
}

bool URoleEquipInterface::CanRecast(const FString& EquipUID, const TArray<int32>& LockProps, const bool& UseYBToStone, const bool& UseYBToFu, bool& BYbToStone, bool& BYbToFu)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst) || nullptr == GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::CanRecast : kitbatInst!"));
		return false;
	}

	UItemBase* itemB = kitbatInst->FindItemByUID(EquipUID);
	if (!IsValid(itemB))
	{
		UGolbalBPFunctionLibrary::StatusMessage(593, TEXT(""));
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::CanRecast : itemB!"));
		return false;
	}
	if (itemB->Level < EQUIP_RECAST_MIX_LEVEL)
	{
		UGolbalBPFunctionLibrary::StatusMessage(1055, TEXT(""));
		return false;
	}
	if (itemB->IsWhite())
	{
		UGolbalBPFunctionLibrary::StatusMessage(1054, TEXT(""));
		return false;
	}
	int32 OwnBloodFu(0), OwnWStong(0);
	int32 BloodFu(0), WastStone(0), MoneyCost(0), YBReplaceStone(0), YBReplaceFu(0);
	GetRecastCost(EquipUID, LockProps.Num(), MoneyCost, WastStone, BloodFu, YBReplaceStone, YBReplaceFu);

	GetRecastCStone(OwnWStong);
	if (OwnWStong < WastStone)
	{
		BYbToStone = UseYBToStone;
		if (!UseYBToStone || !HasEnoughStone(YBReplaceStone))
		{
			UGolbalBPFunctionLibrary::StatusMessage(1069, TEXT(""));
			return false;
		}
		else
		{
			YBReplaceFu += YBReplaceStone;
		}
	}
	else
	{
		BYbToStone = false;
	}

	GetRecastCZFu(OwnBloodFu);
	if (OwnBloodFu < BloodFu)
	{
		BYbToFu = UseYBToFu;
		if (!UseYBToFu || !HasEnoughStone(YBReplaceFu))
		{
			UGolbalBPFunctionLibrary::StatusMessage(1070, TEXT(""));
			return false;
		}
	}
	else
	{
		BYbToFu = false;
	}

	int64 money = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	int64 bindMoney = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
	if (money + bindMoney < MoneyCost)
	{
		UGolbalBPFunctionLibrary::StatusMessage(1097, TEXT(""));
		return false;
	}

	if (bindMoney < MoneyCost)
	{
		//绑金不够的话，是否使用金钱代替
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1322, UGolbalBPFunctionLibrary::GetRichTextMoney((int64)(MoneyCost - bindMoney)), FBtnClick::CreateLambda([this, EquipUID, LockProps, BYbToStone, BYbToFu](RT_BTN_TYPE RtType)
		{
			if (RtType == RT_BTN_TYPE::RT_OK)
			{
				KBEngine::FVariantArray args;
				args.Add(EquipUID);
				args.Add(UGolbalBPFunctionLibrary::ListToFVariant(LockProps));
				args.Add(int32(BYbToStone));
				args.Add(int32(BYbToFu));
				CellCall(TEXT("recastEquip"), args);
			}
		}));
		return false;
	}

	return true;
}

bool URoleEquipInterface::CanBiography(const FString& SrcEquipUID, const FString& DstEquipUID, const bool& UseNewPro, const TArray<FString>& BiographyList)
{
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst) || nullptr == GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleEquipInterface::CanBiography : kitbatInst!"));
		return false;
	}

	int32 OwnWhiteSparCount(0), OwnFiveSparCount(0), OwnSuperSparCount(0);
	int32 WhiteSparCount(0), FiveSparCount(0), SuperSparCount(0), MoneyCost(0);
	GetBiographyCost(DstEquipUID, BiographyList.Num(), MoneyCost, WhiteSparCount, FiveSparCount, SuperSparCount);

	GetIntensifyFu(OwnWhiteSparCount, OwnFiveSparCount, OwnSuperSparCount);
	if (OwnWhiteSparCount < WhiteSparCount || OwnFiveSparCount < FiveSparCount || OwnSuperSparCount < SuperSparCount)
	{
		UGolbalBPFunctionLibrary::StatusMessage(1074, TEXT(""));
		return false;
	}

	int64 money = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	int64 bindMoney = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
	if (money + bindMoney < MoneyCost)
	{
		UGolbalBPFunctionLibrary::StatusMessage(1094, TEXT(""));
		return false;
	}

	if (bindMoney < MoneyCost)
	{
		//绑金不够的话，是否使用金钱代替
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1322, UGolbalBPFunctionLibrary::GetRichTextMoney((int64)(MoneyCost-bindMoney)), FBtnClick::CreateLambda([this, SrcEquipUID, DstEquipUID, UseNewPro, BiographyList](RT_BTN_TYPE RtType)
		{
			if (RtType == RT_BTN_TYPE::RT_OK)
			{
				KBEngine::FVariantArray args;
				KBEngine::FVariantArray arr;
				for (auto Fs : BiographyList)
				{
					arr.Add(Fs);
				}
				args.Add(SrcEquipUID);
				args.Add(DstEquipUID);
				args.Add(int32(UseNewPro));
				args.Add(arr);
				CellCall(TEXT("transferIntensifyEquip"), args);
			}
		}));
		return false;
	}

	return true;
}
CONTROL_COMPILE_OPTIMIZE_END
