// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleCtrlStateMgr.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/ConvertUtil.h"
#include "Manager/LocalDataSaveManager.h"
#include "GameData/LocalDataSave/LocalStortcutKeyData.h"
#include "Manager/CfgManager.h"

CONTROL_COMPILE_OPTIMIZE_START
URoleCtrlStateMgr::URoleCtrlStateMgr()
	:Super()
{
	CtrlStateList.Empty();
}

URoleCtrlStateMgr::~URoleCtrlStateMgr()
{
	for (int32 i = 0; i < CtrlStateList.Num(); ++i)
	{
		URoleCtrlBase* RoleCtrlState = CtrlStateList[i];
		CtrlStateList.Remove(RoleCtrlState);
	}
	CtrlStateList.Reset();
}

void URoleCtrlStateMgr::OnEnterState(EROLE_CTRL_STATE State, int32 Index/* = 0*/)
{
	for (auto NowState = CtrlStateList.CreateIterator(); NowState; ++NowState)
	{
		if (IsValid(*NowState))
		{
			if ((*NowState)->GetCtrlState() == State)
			{
				CS3_Warning(TEXT("URoleCtrlStateMgr::OnEnterState -> Already exist state~"));
					return;
			}
		}
	}
	// 创建新状态,并加入链表
	URoleCtrlBase* NewCtrlState = URoleCtrlBase::Create(this, State);
	if (Index > 0)
	{
		NewCtrlState->SetCtrlStateDataIndex(Index);
	}
	if (IsValid(NewCtrlState))
	{
		CtrlStateList.AddUnique(NewCtrlState);
	}
	else
	{
		CS3_Warning(TEXT("URoleCtrlStateMgr::OnEnterState -> Create State[%d] is fail~"), (int32)State);
	}
}

void URoleCtrlStateMgr::OnLeaveState(EROLE_CTRL_STATE State)
{
	//CS3_Warning(TEXT(" URoleCtrlStateMgr::OnLeaveState"));
	// 查找是否存在该状态
	for (int32 i = 0; i < CtrlStateList.Num(); ++i)
	{
		URoleCtrlBase* RoleCtrlState = CtrlStateList[i];
		//CS3_Warning(TEXT("URoleCtrlStateMgr::OnLeaveState -> For State[%s]"), *RoleCtrlState->ToString());
		if (IsValid(RoleCtrlState) && RoleCtrlState->GetCtrlState() == State)
		{
			RoleCtrlState->ConditionalBeginDestroy();
			CtrlStateList.Remove(RoleCtrlState);
		}
	}
}

void URoleCtrlStateMgr::ResetToCommomState()
{
	CtrlStateList.Empty();
	OnEnterState(EROLE_CTRL_STATE::RCS_COMMON);
}

bool URoleCtrlStateMgr::IsHaveState(EROLE_CTRL_STATE State)
{
	for (auto* NowState : CtrlStateList)
	{
		if (IsValid(NowState) && NowState->GetCtrlState() == State)
		{
			return true;
		}
	}
	return false;
}

void URoleCtrlStateMgr::UpdateStortcutKeyData(bool bGetPlayerData/*=false*/)
{
	if (IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()) && IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalStortcutKeyData))
	{
		ChangedKeys = UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalStortcutKeyData->ChangedKeys;
	}
}

TArray<FSHORTCUTKEY> URoleCtrlStateMgr::GetAllShortcutKeyData()
{
	if (AllKeys.Num() < 1)
	{
		InitShortcutKeyDataBySaveData();
	}
	return AllKeys;
}

void URoleCtrlStateMgr::SaveShortcutKeyDataByTypeToFile(SHORTCUTKEY_TYPE_ENUM Type, TArray<FSHORTCUTKEY> NewKeys, TArray<FSHORTCUTKEY>& OldKeys)
{
	TArray<FSHORTCUTKEY> temp;
	for (int i=0;i<AllKeys.Num();i++)
	{
		if (AllKeys[i].KeyType != Type)
		{
			temp.Add(AllKeys[i]);
		}
	}
	AllKeys.Reset();
	AllKeys.Append(temp);
	AllKeys.Append(NewKeys);
	
	//移除修改的快捷键
	for (int i = 0; i < TempChangedKeys.Num(); i++)
	{
		if (TempChangedKeys[i].KeyType == Type)
		{
			TempChangedKeys.RemoveAt(i);
		}
	}

	///<将改变了的数据保存在本地
	if (IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()) && IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalStortcutKeyData))
	{
		TArray<FSHORTCUTKEY> defaultShortcutKeyData = GetDefaultShortcutKeyDataByType(Type);
		TArray<FSHORTCUTKEY> ChangedShortcutKeyData;
		
		for (auto & defaultData : defaultShortcutKeyData)
		{		
			for (auto& newKeydata : NewKeys)
			{
				if (defaultData.ActName == newKeydata.ActName)
				{
					if (!newKeydata.Compara(defaultData))
					{
						ChangedShortcutKeyData.Add(newKeydata);
					}
					break;
				}
			}
		}
		UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalStortcutKeyData->SaveShortcutKeyDataByTypeToFile(Type, ChangedShortcutKeyData);
	}
}

void URoleCtrlStateMgr::SaveShortcutKeyDataToFile(TArray<FSHORTCUTKEY> NewKeys)
{
	TArray<FSHORTCUTKEY> temp= AllKeys;
	for (auto data : NewKeys)
	{
		for (int i = 0; i < AllKeys.Num(); i++)
		{
			if (AllKeys[i].ActName == data.ActName)
			{
				temp.RemoveAt(i);
				break;
			}
		}
		//移除修改的快捷键
		for (int i = 0; i < TempChangedKeys.Num(); i++)
		{
			if (TempChangedKeys[i].ActName == data.ActName)
			{
				TempChangedKeys.RemoveAt(i);
				break;
			}
		}
	}
	
	AllKeys.Reset();
	AllKeys.Append(temp);	
	AllKeys.Append(NewKeys);
	///<将改变了的数据保存在本地
	if (IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()) && IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalStortcutKeyData))
	{
		TArray<FSHORTCUTKEY> ChangedShortcutKeyData;
		for (auto& newKeydata : NewKeys)
		{
			FSHORTCUTKEY defaultShortcutKeyData = GetDefaultShortcutKeyDataByActName(newKeydata.ActName);
			if (!newKeydata.Compara(defaultShortcutKeyData))
			{
				ChangedShortcutKeyData.Add(newKeydata);
			}
		}
		UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalStortcutKeyData->SaveShortcutKeyDataToFile(ChangedShortcutKeyData);
	}
}

void URoleCtrlStateMgr::CancelShortcutKeyData(SHORTCUTKEY_TYPE_ENUM Type)
{
	TArray<FSHORTCUTKEY> temp;
	for (int i = 0; i < TempChangedKeys.Num(); i++)
	{
		if (TempChangedKeys[i].KeyType != Type)
		{
			temp.Add(TempChangedKeys[i]);
		}
	}
	TempChangedKeys.Reset();
	if (temp.Num() > 0)
	{
		TempChangedKeys.Append(temp);
	}
}

TArray<FSHORTCUTKEY> URoleCtrlStateMgr::GetDefaultShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type)
{
	TArray<FSHORTCUTKEY> results;
	if (!IsValid(UUECS3GameInstance::Instance))return results;

	auto CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UDataTable* DataTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_DEFAULT_SHORTCUTKEY)->GetBaseTable();
	
	if (DataTable)
	{
		for (auto data : DataTable->GetRowNames())
		{
			FSHORTCUTKEY* Data = (FSHORTCUTKEY*)DataTable->FindRowUnchecked(*data.ToString());
			FSHORTCUTKEY KeyData;
			KeyData.KeyType = Data->KeyType;
			KeyData.ActName = Data->ActName;
			KeyData.MainKey = Data->MainKey;
			KeyData.CannotChangeKeys = Data->CannotChangeKeys;
			KeyData.CanChange = Data->CanChange;
			KeyData.CanGroup = Data->CanGroup;
			KeyData.CanDoubleClick = Data->CanDoubleClick;
			KeyData.CanSkipChecking = Data->CanSkipChecking;
			KeyData.Remarks = Data->Remarks;
			if (Data->KeyType == Type)
			{
				results.Add(KeyData);
			}
		}
	}
	return results;
}

FSHORTCUTKEY URoleCtrlStateMgr::GetDefaultShortcutKeyDataByActName(FName ActName)
{
	FSHORTCUTKEY results;
	if (!IsValid(UUECS3GameInstance::Instance))return results;

	auto CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UDataTable* DataTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_DEFAULT_SHORTCUTKEY)->GetBaseTable();

	if (DataTable)
	{
		for (auto data : DataTable->GetRowNames())
		{
			FSHORTCUTKEY* Data = (FSHORTCUTKEY*)DataTable->FindRowUnchecked(*data.ToString());
			FSHORTCUTKEY KeyData;
			KeyData.KeyType = Data->KeyType;
			KeyData.ActName = Data->ActName;
			KeyData.MainKey = Data->MainKey;
			KeyData.CannotChangeKeys = Data->CannotChangeKeys;
			KeyData.CanChange = Data->CanChange;
			KeyData.CanGroup = Data->CanGroup;
			KeyData.CanDoubleClick = Data->CanDoubleClick;
			KeyData.CanSkipChecking = Data->CanSkipChecking;
			KeyData.Remarks = Data->Remarks;
			if (Data->ActName == ActName)
			{
				results = KeyData;
				return results;
			}
		}
	}
	return results;
}

TArray<FSHORTCUTKEY> URoleCtrlStateMgr::GetShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type)
{
	TArray<FSHORTCUTKEY> results;
	for (auto& data : AllKeys)
	{
		if (data.KeyType == Type)
		{
			results.Add(data);
		}
	}
	return results;
}

TArray<FSHORTCUTKEY> URoleCtrlStateMgr::GetChangedShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type)
{
	TArray<FSHORTCUTKEY> results;
	bool bHasSameData = false;
	for (auto& data : AllKeys)
	{
		bHasSameData = false;
		for (auto& temp: TempChangedKeys)
		{
			if (data.KeyType == Type && data.ActName== temp.ActName)
			{
				bHasSameData = true;			
				results.Add(temp);
				break;
			}
		}
		if (!bHasSameData)
		{
			results.Add(data);
		}
	}
	return results;
}

ESHORTCUT_EXISTING_TYPE URoleCtrlStateMgr::CheckShortcutKeyExisting(FGROUPKEY_DATA Keys, FName ActName,FSHORTCUTKEY& OldShortcutKey)
{
		//当前快捷键中是否存在
	for (auto& data : AllKeys)
	{
		if (data.CanSkipChecking)
		{
			continue;
		}
		if (CheckShortcutKeyExistingInTarray(Keys, data.MainKey))
		{
			if (ActName == data.ActName)
			{
				return ESHORTCUT_EXISTING_TYPE::SET_OLDKEYS;
			}
			OldShortcutKey = data;
			return ESHORTCUT_EXISTING_TYPE::SET_TRUE_IN_OLDKEYS;
		}
	}
	return ESHORTCUT_EXISTING_TYPE::SET_FALSE;
}

ESHORTCUT_EXISTING_TYPE URoleCtrlStateMgr::CheckShortcutKeyExistingInChanged(FGROUPKEY_DATA Keys, FName ActName, FSHORTCUTKEY& OldShortcutKey)
{
	//修改后没有保存的快捷键中是否存在
	for (auto& data : TempChangedKeys)
	{
		if (data.CanSkipChecking)
		{
			continue;
		}
		if (CheckShortcutKeyExistingInTarray(Keys, data.MainKey))
		{
			if (ActName == data.ActName)
			{
				return ESHORTCUT_EXISTING_TYPE::SET_CHANGEDKEYS;
			}
			OldShortcutKey = data;
			return ESHORTCUT_EXISTING_TYPE::SET_TRUE_IN_CHANGEDKEYS;
		}
	}
	return ESHORTCUT_EXISTING_TYPE::SET_FALSE;
}

bool URoleCtrlStateMgr::CheckChangedShortcutDataReseted(FSHORTCUTKEY OldShortcutKey, TArray<FKey>Keys)
{
	if (Keys.Num() < 1 )return false;
	///<将Keys转换成FGROUPKEY_DATA类型
	FGROUPKEY_DATA GroupKey = UGolbalBPFunctionLibrary::ConvertKeysToGroupKey(Keys);
	FSHORTCUTKEY ShortcutData;
	//添加新修改的数据
	FSHORTCUTKEY temp = OldShortcutKey;
	bool bIsMainKey = true;
	for (int i = 0; i < temp.MainKey.Num(); i++)
	{
		if (GroupKey.Key == temp.MainKey[i].Key)
		{
			for (auto InputKeyData : temp.MainKey[i].KeyDatas)
			{
				if (GroupKey.Alt == InputKeyData.Alt && GroupKey.Cmd == InputKeyData.Cmd && GroupKey.Ctrl == InputKeyData.Ctrl
					&& GroupKey.Shift == InputKeyData.Shift && GroupKey.DoubleClick == (InputKeyData.IE == EINPUT_EVENT::IE_DoubleClick))
				{
					bIsMainKey = temp.MainKey[i].BIsMainKey;
					break;
				}
			}
			break;
		}
	}
	for (auto& data : TempChangedKeys)
	{
		if (OldShortcutKey.ActName == data.ActName)
		{
			if (data.MainKey.Num() == 0)
			{
				return true;
			}
			bool hasMainKey = false;
			for (int i = 0; i < data.MainKey.Num(); i++)
			{
				if (data.MainKey[i].BIsMainKey == bIsMainKey)
				{
					if (data.MainKey[i].KeyDatas.Num()==0)
					{
						return true;
					}
					return false;
				}
			}
			return true;
		}
	}
	return false;
}

void URoleCtrlStateMgr::GetShortcutDataByActName(SHORTCUTKEY_TYPE_ENUM KeyType,FName ActName, FSHORTCUTKEY& ShortcutData, bool bIsChangedKeys/*=false*/)
{
	if (!bIsChangedKeys)
	{
		for (auto& data : AllKeys)
		{
			if (ActName == data.ActName&&KeyType==data.KeyType)
			{
				ShortcutData = data;
				return;
			}
		}
	}
	else
	{
		for (auto& data : TempChangedKeys)
		{
			if (ActName == data.ActName && KeyType == data.KeyType)
			{
				ShortcutData = data;
				return;
			}
		}
	}
}

void URoleCtrlStateMgr::AddShortcutDataToChangedKeys(FSHORTCUTKEY ShortcutData)
{
	for (int i = 0; i < TempChangedKeys.Num(); i++)
	{
		if (TempChangedKeys[i].Compara(ShortcutData))
		{
			return;
		}
	}
	TempChangedKeys.Add(ShortcutData);
}

void URoleCtrlStateMgr::RemoveShortcutDataFromChangedKeys(FSHORTCUTKEY ShortcutData)
{
	for (int i = 0; i < TempChangedKeys.Num(); i++)
	{
		if (TempChangedKeys[i].Compara(ShortcutData))
		{
			TempChangedKeys.RemoveAt(i);
		}
	}
}

bool URoleCtrlStateMgr::ChangedShortcutKeysIsEmpty()
{
	return TempChangedKeys.Num() > 0 ? false : true;
}

void URoleCtrlStateMgr::InitShortcutKeyDataBySaveData()
{
	AllKeys.Reset();
	const UDataTable* shortcutKeysTable = GetShortcutKeyDataConfig();
	if (shortcutKeysTable)
	{
		for (auto data : shortcutKeysTable->GetRowNames())
		{
			FSHORTCUTKEY* Data = (FSHORTCUTKEY*)shortcutKeysTable->FindRowUnchecked(*data.ToString());
			FSHORTCUTKEY KeyData;
			KeyData.KeyType = Data->KeyType;
			KeyData.ActName = Data->ActName;
			KeyData.MainKey = Data->MainKey;
			KeyData.CannotChangeKeys = Data->CannotChangeKeys;
			KeyData.CanChange = Data->CanChange;
			KeyData.CanGroup = Data->CanGroup;
			KeyData.CanDoubleClick = Data->CanDoubleClick;
			KeyData.CanSkipChecking = Data->CanSkipChecking;
			KeyData.Remarks = Data->Remarks;
			AllKeys.Add(KeyData);
		}
	}

	if (IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()) && IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalStortcutKeyData))
	{
		if (ChangedKeys.Num() > 0)
		{
			for (auto& data : ChangedKeys)
			{
				for (int i=0;i<AllKeys.Num();i++)
				{
					if (data.KeyType == AllKeys[i].KeyType && data.ActName == AllKeys[i].ActName && data.CanChange == AllKeys[i].CanChange)
					{
						AllKeys[i] = data;
						break;
					}
				}
			}
		}
	}
}

bool URoleCtrlStateMgr::CheckKeyCanChangeGroupKey(FSHORTCUTKEY ShortcutKey, FGROUPKEY_DATA Keys)
{
	if (ShortcutKey.CannotChangeKeys.Contains(Keys.Key))
	{
		return false;
	}
	return true;
}

FString URoleCtrlStateMgr::GetKeyNameByActName(FName ActName, FGROUPKEY_DATA& KeyValue)
{
	for (int i = 0; i < AllKeys.Num(); i++)
	{
		if (! AllKeys[i].ActName.Compare(ActName))
		{
			FString KeyString = "";
			bool BIsDoubleClick = false;
			for (int j = 0; j < AllKeys[i].MainKey.Num(); j++)
			{
				if (AllKeys[i].MainKey[j].Key.IsValid())
				{
					KeyValue.Key = AllKeys[i].MainKey[j].Key;
					KeyValue.Alt = false;
					KeyValue.Shift = false;
					KeyValue.Cmd = false;
					KeyValue.Ctrl = false;
					KeyValue.DoubleClick = false;
					for (auto & keydata : AllKeys[i].MainKey[j].KeyDatas)
					{						
						if (keydata.IE == EINPUT_EVENT::IE_DoubleClick)
						{
							BIsDoubleClick = true;
							KeyValue.DoubleClick = true;
						}
						if (keydata.Type == EINPUT_TYPE::IT_Action)
						{
							if (keydata.Ctrl)
							{
								KeyString = KeyString + TEXT("Ctrl+");
								KeyValue.Ctrl = true;
							}
							if (keydata.Shift)
							{
								KeyString = KeyString + TEXT("Shift+");
								KeyValue.Shift = true;
							}
							if (keydata.Alt)
							{
								KeyString = KeyString + TEXT("Alt+");
								KeyValue.Alt = true;
							}
							if (keydata.Cmd)
							{
								KeyString = KeyString + TEXT("Cmd+");
								KeyValue.Cmd = true;
							}
							break;
						}
					}
					if (BIsDoubleClick)
					{
						KeyString = KeyString + TEXT("双击") + FNAME_TO_FSTRING(AllKeys[i].MainKey[j].Key.GetDisplayName());
					}
					else
					{
						KeyString = KeyString + FNAME_TO_FSTRING(AllKeys[i].MainKey[j].Key.GetDisplayName());
					}

					return KeyString;
				}
			}
		}
	}
	return TEXT("");
}

TArray<FSHORTCUTKEY> URoleCtrlStateMgr::GetShortcutDataByGroupKey(FKey Key)
{
	TArray<FSHORTCUTKEY> ShortcutDatas;
	bool bAlt = false;
	bool bCmd = false;
	bool bShift = false;
	bool bCtrl = false;
	if (Key == EKeys::LeftAlt || Key == EKeys::RightAlt)
	{
		bAlt = true;
	}
	else if (Key == EKeys::LeftCommand || Key == EKeys::RightCommand)
	{
		bCmd = true;
	}
	else if (Key == EKeys::LeftShift || Key == EKeys::RightShift)
	{
		bShift = true;
	}
	else if (Key == EKeys::LeftControl || Key == EKeys::RightControl)
	{
		bCtrl = true;
	}
	bool bbreak = false;
	for (auto& TempKey : AllKeys)
	{
		bbreak = false;
		for (auto& TempMainKey : TempKey.MainKey)
		{
			for (auto& TempKeyDatas : TempMainKey.KeyDatas)
			{
				if (TempKeyDatas.Type == EINPUT_TYPE::IT_Action&& TempKeyDatas.Alt == bAlt && TempKeyDatas.Cmd == bCmd &&
					TempKeyDatas.Shift == bShift && TempKeyDatas.Ctrl == bCtrl)
				{
					ShortcutDatas.Add(TempKey);
					bbreak = true;
					break;
				}
			}
			if (bbreak)
				break;
		}
	}

	return ShortcutDatas;
}

void URoleCtrlStateMgr::BeginPlay()
{
	Super::BeginPlay();

	// 默认为普通状态
	ResetToCommomState();
}

void URoleCtrlStateMgr::BeginDestroy()
{
	Super::BeginDestroy();
}

bool URoleCtrlStateMgr::CheckShortcutKeyExistingInTarray(FGROUPKEY_DATA GroupKey, TArray<FInputKeyEvent>InputKeyEventDatas)
{
	bool bIsGroupKey = (GroupKey.Shift || GroupKey.Ctrl || GroupKey.Alt || GroupKey.Cmd || GroupKey.DoubleClick) ? true : false;
	for (auto& data : InputKeyEventDatas)
	{
		bool bIsDoubleClick = false;
		if (GroupKey.Key == data.Key)
		{
			for (auto& keydata : data.KeyDatas)
			{
				bIsDoubleClick = false;
				if (keydata.IE == EINPUT_EVENT::IE_DoubleClick)
				{
					bIsDoubleClick = true;
				}
				if (keydata.Type == EINPUT_TYPE::IT_Action)
				{
					if (keydata.Shift == GroupKey.Shift && keydata.Ctrl == GroupKey.Ctrl &&
						keydata.Alt == GroupKey.Alt && keydata.Cmd == GroupKey.Cmd && GroupKey.DoubleClick == bIsDoubleClick)
					{
						return true;
					}
					else
					{
						return false;
					}
				}
				else if (keydata.Type == EINPUT_TYPE::IT_Axis && bIsGroupKey)
				{
					return false;
				}
			}			
			return true;
		}
	}
	return false;
}


const UDataTable* URoleCtrlStateMgr::GetShortcutKeyDataConfig()
{
	auto CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UDataTable* DataTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_DEFAULT_SHORTCUTKEY)->GetBaseTable();
	return DataTable;
}

CONTROL_COMPILE_OPTIMIZE_END
