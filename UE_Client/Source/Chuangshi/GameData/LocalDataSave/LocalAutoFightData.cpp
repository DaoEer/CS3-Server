// Fill out your copyright notice in the Description page of Project Settings.


#include "LocalAutoFightData.h"
#include "Util/CS3Debug.h"
#include "Manager/AutoFightMar.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Interface/Role/RoleAutoFightInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CfgManager.h"
#include "Manager/LocalDataSaveManager.h"


ULocalAutoFightData::ULocalAutoFightData()
{
	if (!IsValid(UUECS3GameInstance::Instance)) return;
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString PlayerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerId, TEXT("playerName"));
	FileName = "LocalAutoFightData_" + PlayerName;
	InitLocalData();
}

void ULocalAutoFightData::Serialize(FArchive& Ar)
{
	Super::Serialize(Ar);
	if (SettingData.IsAutoRoleAddHP || SettingData.IsAutoRoleAddMP)
	{
		UGolbalBPFunctionLibrary::AutoFightMar()->OnStartAutoAdd_HpMp();
	}
}

void ULocalAutoFightData::InitLocalData()
{
	SkillList = TMap<int32, int32>();
	ItemOfHPMPList = TMap<int32, int32>();
	SettingData = GetDefultAutoFightSettingData();
}

FAUTOFIGHTTTING_DATA ULocalAutoFightData::GetAutoFightSettingData()
{
	return SettingData;
}

const FString&  ULocalAutoFightData::GetFileName()
{
	return FileName;
}

void ULocalAutoFightData::SetAutoFightSettingData(FAUTOFIGHTTTING_DATA data)
{
	SetAddHPPercentage(data.RoleAddHPPercentage);
	SetAddMPPercentage(data.RoleAddMPPercentage);
	SetFightRange(data.FightRange);
	SettingData = data;

	if (SettingData.IsAutoRoleAddHP || SettingData.IsAutoRoleAddMP)
	{
		UGolbalBPFunctionLibrary::AutoFightMar()->OnStartAutoAdd_HpMp();
	}
	else
	{
		UGolbalBPFunctionLibrary::AutoFightMar()->OnStopAutoAdd_HpMp();
	}

	if (UAutoFightMar::GetInstanceByCS3GameInstance() && UAutoFightMar::GetInstanceByCS3GameInstance()->OnChangeAutoFightData.IsBound())
	{
		UAutoFightMar::GetInstanceByCS3GameInstance()->OnChangeAutoFightData.Broadcast(SettingData);
	}

	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalAutoFightDataFile();
}

FAUTOFIGHTTTING_DATA ULocalAutoFightData::GetDefultAutoFightSettingData()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UDataTable* DataTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_AUTOFIGHT_SETTING_DEFAULT)->GetBaseTable();

	if (DataTable)
	{
		for (auto data : DataTable->GetRowNames())
		{
			FAUTOFIGHTTTING_DATA* Data = (FAUTOFIGHTTTING_DATA*)DataTable->FindRowUnchecked(*data.ToString());
			return *Data;
		}
	}
	return FAUTOFIGHTTTING_DATA();
}

float ULocalAutoFightData::GetFightRange()
{
	return SettingData.FightRange;
}

bool ULocalAutoFightData::CanPickupByType(EAutomaticPickupType type)
{
	for (auto iter : SettingData.AutoPickupData)
	{
		if (iter.PickupType == type)
		{
			return iter.IsAuto;
		}
	}
	return false;
}

bool ULocalAutoFightData::IsCanAutoJoinTeam()
{
	return SettingData.IsAutoJoinTeam;
}

bool ULocalAutoFightData::CheckAutoFightSettingDataChanged(FAUTOFIGHTTTING_DATA data)
{
	if (data.IsAutoRoleAddHP != SettingData.IsAutoRoleAddHP)
	{
		return true;
	}
	if (!FMath::IsNearlyEqual(data.RoleAddHPPercentage, SettingData.RoleAddHPPercentage))
	{
		return true;
	}
	if (data.IsAutoRoleAddMP != SettingData.IsAutoRoleAddMP)
	{
		return true;
	}
	if (!FMath::IsNearlyEqual(data.RoleAddMPPercentage, SettingData.RoleAddMPPercentage))
	{
		return true;
	}
	if (!FMath::IsNearlyEqual(data.FightRange, SettingData.FightRange))
	{
		return true;
	}
	if (data.IsAutoJoinTeam != SettingData.IsAutoJoinTeam)
	{
		return true;
	}
	if (data.IsAutoRevive != SettingData.IsAutoRevive)
	{
		return true;
	}
	TArray<FAutomaticPickupData> TempAutoPickupData = data.AutoPickupData;
	for (auto iter : TempAutoPickupData)
	{
		if (iter.IsAuto != CanPickupByType(iter.PickupType))
		{
			return true;
		}
	}
	return false;
}

int32 ULocalAutoFightData::GetKeyByItemID(int32 ItemID)
{
	for (auto ItemData : ItemOfHPMPList)
	{
		if (ItemData.Value == ItemID)
		{
			return ItemData.Key;
		}
	}

	return -1;
}

void ULocalAutoFightData::SetFightRange(float NewFightRange)
{
	if (0.0f > NewFightRange)
	{
		return;
	}

	SettingData.FightRange = NewFightRange;
}

void ULocalAutoFightData::SetAddHPPercentage(float Percentage)
{
	if (Percentage < 0.0f || Percentage > 1.0f)
	{
		return;
	}

	SettingData.RoleAddHPPercentage = Percentage;
}

void ULocalAutoFightData::SetAddMPPercentage(float Percentage)
{
	if (Percentage < 0.0f || Percentage > 1.0f)
	{
		return;
	}

	SettingData.RoleAddMPPercentage = Percentage;
}

const TArray<EAutomaticPickupType> ULocalAutoFightData::GetCanPickUpList()
{
	TArray<EAutomaticPickupType> CanPickUpList{};
	for (FAutomaticPickupData& Data : SettingData.AutoPickupData)
	{
		if (Data.IsAuto)
		{
			CanPickUpList.Add(Data.PickupType);
		}
	}
	return CanPickUpList;
}

bool ULocalAutoFightData::AddSkillOnList(int32 SkillKey, int32 NewSkill)
{
	if (SkillList.Contains(SkillKey) && IsSkillInListByID(NewSkill))//当Key值和技能都在时
	{
		//判断Key值对应的技能是否为添加技能
		if (NewSkill == SkillList[SkillKey])
		{
			return false;
		}
		else
		{
			//将要添加的技能从原来的位置移除
			RemoveSkillOnListByValue(NewSkill);
			//将新值替换Key对应的值
			SkillList[SkillKey] = NewSkill;
		}
	}
	else
	if (SkillList.Contains(SkillKey) && !IsSkillInListByID(NewSkill))//仅当Key值存在时
	{
		//将新值替换Key对应的值
		SkillList[SkillKey] = NewSkill;
	}
	else
	if (!SkillList.Contains(SkillKey) && IsSkillInListByID(NewSkill))//仅当技能存在时
	{
		//将要添加的技能从原来的位置移除
		RemoveSkillOnListByValue(NewSkill);
		//将新技能添加到新位置
		SkillList.Add(SkillKey, NewSkill);
	}
	else//都不存在时
	{
		//将新技能添加到新位置
		SkillList.Add(SkillKey, NewSkill);
	}
	//添加技能成功回调
	if (UAutoFightMar::GetInstanceByCS3GameInstance())
	{
		UAutoFightMar::GetInstanceByCS3GameInstance()->OnAddSkillOnListOver(SkillKey, NewSkill);
	}

	//需要通知到服务器临时记录起来，创建一些怪物（替身、分身）等可能需要用到
	URoleAutoFightInterface* autoFightInterface = Cast<URoleAutoFightInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleAutoFightInterface"), 0));
	if (autoFightInterface != nullptr)
	{
		autoFightInterface->AddSkillOnList(SkillKey, NewSkill);
	}

	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalAutoFightDataFile();
	return true;
}

bool ULocalAutoFightData::RemoveSkillOnListByKey(int32 SkillKey)
{
	// 判断Key是否存在
	if (!SkillList.Contains(SkillKey)) return false;

	//移除
	SkillList.Remove(SkillKey);
	//移除技能成功回调
	if (UAutoFightMar::GetInstanceByCS3GameInstance())
	{
		UAutoFightMar::GetInstanceByCS3GameInstance()->OnRemoveSkillOnListByKey(SkillKey);
	}

	//需要通知到服务器临时记录起来，创建一些怪物（替身、分身）等可能需要用到
	URoleAutoFightInterface* autoFightInterface = Cast<URoleAutoFightInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleAutoFightInterface"), 0));
	if (autoFightInterface != nullptr)
	{
		autoFightInterface->RemoveSkillOnListByKey(SkillKey);
	}

	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalAutoFightDataFile();
	return true;
}

bool ULocalAutoFightData::RemoveSkillOnListByValue(int32 RemValue)
{
	//判断Key是否存在
	if (!IsSkillInListByID(RemValue)) return false;
	//移除技能成功回调
	if (UAutoFightMar::GetInstanceByCS3GameInstance())
	{
		UAutoFightMar::GetInstanceByCS3GameInstance()->OnRemoveSkillOnListByValue(RemValue);
	}

	int32 SkillKey = GetKeyBySkill(RemValue);
	//需要通知到服务器临时记录起来，创建一些怪物（替身、分身）等可能需要用到
	URoleAutoFightInterface* autoFightInterface = Cast<URoleAutoFightInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleAutoFightInterface"), 0));
	if (autoFightInterface != nullptr)
	{
		autoFightInterface->RemoveSkillOnListByKey(SkillKey);
	}

	//移除
	SkillList.Remove(SkillKey);
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalAutoFightDataFile();
	return true;
}

bool ULocalAutoFightData::ExchangeOnSkill(int32 KeyValue1, int32 KeyValue2)
{
	if (SkillList.Contains(KeyValue1) && SkillList.Contains(KeyValue2))//两个都存在直接交换
	{
		//交换数据
		int32 TemSkill = SkillList[KeyValue1];
		SkillList[KeyValue1] = SkillList[KeyValue2];
		SkillList[KeyValue2] = TemSkill;
		UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalAutoFightDataFile();
		
	}
	else if (SkillList.Contains(KeyValue1) && !SkillList.Contains(KeyValue2))//第一个存在，第二个不存在，则移动第一个到第二个
	{
		SkillList.Add(KeyValue2, SkillList[KeyValue1]);
		RemoveSkillOnListByKey(KeyValue1);
	}
	else
	{
		return false;
	}

	if (UAutoFightMar::GetInstanceByCS3GameInstance())
	{
		UAutoFightMar::GetInstanceByCS3GameInstance()->OnExchangeOnSkill(KeyValue1, KeyValue2);
	}
	
	return true;
}

bool ULocalAutoFightData::IsSkillInListByID(int32 SkillID)
{
	for (auto SkillValue : SkillList)
	{
		if (SkillID == SkillValue.Value)
		{
			return true;
		}
	}
	return false;
}

bool ULocalAutoFightData::IsSkillInListByKey(int32 SkillKey)
{
	return SkillList.Contains(SkillKey);
}

bool ULocalAutoFightData::AddItemOnList(int32 ItemKey, int32 NewID)
{
	if (ItemKey < 0 || ItemKey > 1)
	{
		CS3_Warning(TEXT("ULocalAutoFightData::AddItemOnList ItemKey Is Out Of Bounds!"));
		return false;
	}

	//获取玩家的背包
	URoleKitBagInterface* KitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));

	//获取物品数据
	TArray<UItemBase*> ItemDatas = KitBagInterface->GetItemsByItemID(NewID);

	UItemBase* ItemData = nullptr;

	if (ItemDatas.Num() > 0)
	{
		ItemData = ItemDatas[0];
	}
	else
	{
		CS3_Warning(TEXT("ULocalAutoFightData::AddItemOnList Don't Find This Item!"));
		return false;
	}

	//判断物品类型
	if (IsValid(ItemData))
	{
		if (0 == ItemKey)
		{
			if (20002 != ItemData->ItemType &&
				20004 != ItemData->ItemType)
			{
				CS3_Warning(TEXT("ULocalAutoFightData::AddItemOnList NewItem Type Error!"));
				return false;
			}
		}

		if (1 == ItemKey)
		{
			if (20003 != ItemData->ItemType &&
				20005 != ItemData->ItemType)
			{
				CS3_Warning(TEXT("ULocalAutoFightData::AddItemOnList NewItem Type Error!"));
				return false;
			}
		}

	}

	//判断物品KEY和Value是否已经存在
	if (ItemOfHPMPList.Contains(ItemKey) && IsItemInListByID(NewID))
	{
		//当要加的物品和起位置都是对的则不进行任何操作
		if (NewID == ItemOfHPMPList[ItemKey])
		{
			CS3_Warning(TEXT("ULocalAutoFightData::AddItemOnList ItemKey And NewItem Is Existence!"));
			return false;
		}
		else//位置和物品不对应，就将物品从原来的位置移除，再加到新的位置
		{
			//把物品从本来的位置移除
			ItemOfHPMPList.Remove(*ItemOfHPMPList.FindKey(NewID));
			//新物品替换旧物品
			ItemOfHPMPList[ItemKey] = NewID;
		}

	}
	else if (ItemOfHPMPList.Contains(ItemKey) && !IsItemInListByID(NewID))
	{
		//新物品替换旧物品
		ItemOfHPMPList[ItemKey] = NewID;
	}
	else if (!ItemOfHPMPList.Contains(ItemKey) && IsItemInListByID(NewID))
	{
		//把物品从本来的位置移除
		ItemOfHPMPList.Remove(*ItemOfHPMPList.FindKey(NewID));
		//添加到新的物品
		ItemOfHPMPList.Add(ItemKey, NewID);
	}
	else if (!ItemOfHPMPList.Contains(ItemKey) && !IsItemInListByID(NewID))
	{
		//添加到新的物品
		ItemOfHPMPList.Add(ItemKey, NewID);
	}

	if (UAutoFightMar::GetInstanceByCS3GameInstance())
	{
		UAutoFightMar::GetInstanceByCS3GameInstance()->OnAddItemOnListOver(ItemKey, NewID);
	}
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalAutoFightDataFile();
	return true;
}

bool ULocalAutoFightData::RemoveItemOnListByKey(int32 ItemKey)
{
	//判断参数是否存在
	if (!IsItemInListByKey(ItemKey))
	{
		CS3_Warning(TEXT("ULocalAutoFightData::RemoveItemOnListByKey ItemKey Is Not Valid !"));
		return false;
	}

	ItemOfHPMPList.Remove(ItemKey);

	if (UAutoFightMar::GetInstanceByCS3GameInstance())
	{
		UAutoFightMar::GetInstanceByCS3GameInstance()->OnRemoveItemOnListByKey(ItemKey);
	}
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalAutoFightDataFile();
	return true;
}

bool ULocalAutoFightData::RemoveItemOnListByValue(int32 RemValue)
{
	//判断参数是否存在
	if (IsItemInListByID(RemValue))
	{
		CS3_Warning(TEXT("ULocalAutoFightData::RemoveItemOnListByValue RemValue Is Not Valid !"));
		return false;
	}
	if (UAutoFightMar::GetInstanceByCS3GameInstance())
	{
		UAutoFightMar::GetInstanceByCS3GameInstance()->OnRemoveItemOnListByValue(RemValue);
	}
	ItemOfHPMPList.Remove(GetKeyByItemID(RemValue));
	
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalAutoFightDataFile();
	return true;
}

int32 ULocalAutoFightData::GetItemIDByKey(int32 KeyValue)
{
	if (ItemOfHPMPList.Contains(KeyValue))
	{
		return *ItemOfHPMPList.Find(KeyValue);
	}
	else
	{
		return -1;
	}
}

bool ULocalAutoFightData::IsItemInListByID(int32 ItemID)
{
	for (auto ItemValue : ItemOfHPMPList)
	{
		if (ItemID == ItemValue.Value)
		{
			return true;
		}
	}

	return false;
}

bool ULocalAutoFightData::IsItemInListByKey(int32 ItemlKey)
{
	return ItemOfHPMPList.Contains(ItemlKey);
}

const TMap<int32, int32>& ULocalAutoFightData::GetItemList()
{
	return ItemOfHPMPList;
}

const TMap<int32, int32>& ULocalAutoFightData::GetSkillList()
{
	return SkillList;
}

const int32 ULocalAutoFightData::GetSkillByKey(int32 KeyValue)
{
	if (SkillList.Contains(KeyValue))
	{
		return *SkillList.Find(KeyValue);
	}
	else
	{
		return -1;
	}
}

const int32 ULocalAutoFightData::GetKeyBySkill(int32 SkillValue)
{
	for (auto skillData : SkillList)
	{
		if (skillData.Value == SkillValue)
		{
			return skillData.Key;
		}
	}

	return -1;
}