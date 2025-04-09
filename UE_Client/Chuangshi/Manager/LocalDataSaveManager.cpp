// Fill out your copyright notice in the Description page of Project Settings.


#include "LocalDataSaveManager.h"
#include"Chuangshi.h"
#include "Util/CS3Debug.h"
CONTROL_COMPILE_OPTIMIZE_START

//一开始就需要加载的可以从这里调用,如果需要获得特殊的名字或者账号信息需要自己创建函数
void ULocalDataSaveManager::Init()
{
	LocalData = NewLocalDataFile<ULocalData>();

	LocalUserSettingData = NewLocalDataFile<ULocalUserSettingData>();
}

void ULocalDataSaveManager::OnPlayerEnterWorld()
{
	LocalKitbagData = NewLocalDataFile<ULocalKitbagData>();
	LocalAutoFightData = NewLocalDataFile<ULocalAutoFightData>();
	InitLocalChatSettingData();
	InitLocalStortcutKeyData();
	if (IsValid(LocalData))
	{
		LocalData->OnPlayerEnterWorld();
	}
}

void ULocalDataSaveManager::OnPlayerLeaveWorld()
{
	if (IsValid(LocalAutoFightData))
	{
		LocalAutoFightData = nullptr;
	}
	if (IsValid(LocalTongSettingData))
	{
		LocalTongSettingData = nullptr;
	}
	if (IsValid(LocalRelationData))
	{
		LocalRelationData = nullptr;
	}
	if (IsValid(LocalKitbagData))
	{
		LocalKitbagData = nullptr;
	}
	if (IsValid(LocalChatSettingData))
	{
		LocalChatSettingData = nullptr;
	}
	if (IsValid(LocalStortcutKeyData))
	{
		LocalStortcutKeyData = nullptr;
	}
	if (IsValid(LocalMessageData))
	{
		LocalMessageData = nullptr;
	}
}

bool ULocalDataSaveManager::SaveLocalChatSettingDataFile()
{
	return SaveLocalDataFile(LocalChatSettingData);
}

void ULocalDataSaveManager::InitLocalChatSettingData()
{
	if (!IsValid(LocalChatSettingData))
	{
		LocalChatSettingData = NewLocalDataFile<ULocalChatSettingData>();
	}
	if (!DoesLocalFileExist(LocalChatSettingData))
	{
		LocalChatSettingData->DefaultDataToFile();
	}
}

bool ULocalDataSaveManager::SaveLocalStortcutKeyDataFile()
{
	return SaveLocalDataFile(LocalStortcutKeyData);
}

void ULocalDataSaveManager::InitLocalStortcutKeyData()
{
	if (!IsValid(LocalStortcutKeyData))
	{
		LocalStortcutKeyData = NewLocalDataFile<ULocalStortcutKeyData>();
	}
}

ULocalDataSaveManager * ULocalDataSaveManager::GetInstance()
{
	cs3_checkNoReentry();
	return (ULocalDataSaveManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_LocalDataSaveManager")));
}

bool ULocalDataSaveManager::DeosLocalUserSettingDataExist()
{
	return DoesLocalFileExist(LocalUserSettingData);
}

bool ULocalDataSaveManager::SaveLocalDataFile()
{
	return SaveLocalDataFile(LocalData);
}

bool ULocalDataSaveManager::SaveLocalUserSettingDataFile()
{
	return SaveLocalDataFile(LocalUserSettingData);
}

bool ULocalDataSaveManager::NewLocalTongSettingDataFile()
{
	LocalTongSettingData = NewLocalDataFile<ULocalTongSettingData>();
	if (IsValid(LocalTongSettingData))return true;
	return false;
}

bool ULocalDataSaveManager::SaveLocalTongSettingDataFile()
{
	return SaveLocalDataFile(LocalTongSettingData);
}

bool ULocalDataSaveManager::NewLocalRelationDataFile()
{
	LocalRelationData = NewLocalDataFile<ULocalRelationData>();
	if (IsValid(LocalRelationData))return true;
	return false;
}

bool ULocalDataSaveManager::SaveLocalRelationDataFile()
{
	return SaveLocalDataFile(LocalRelationData);
}

bool ULocalDataSaveManager::SaveLocalItemDataFile()
{
	return SaveLocalDataFile(LocalKitbagData);
}

void ULocalDataSaveManager::InitLocalMessageDataFile()
{

	if (!IsValid(LocalChatSettingData))
	{
		LocalMessageData = NewLocalDataFile<ULocalMessageData>();
	}
	if (!DoesLocalFileExist(LocalMessageData))
	{
		LocalMessageData->InitLocalMessageData();
	}
}

bool ULocalDataSaveManager::SaveLocalMessageDataFile()
{
	return SaveLocalDataFile(LocalMessageData);
}

bool ULocalDataSaveManager::NewLocalAutoFightDataFile()
{
	LocalAutoFightData = NewLocalDataFile<ULocalAutoFightData>();
	if (IsValid(LocalAutoFightData))return true;
	return false;
}

bool ULocalDataSaveManager::SaveLocalAutoFightDataFile()
{
	return SaveLocalDataFile(LocalAutoFightData);
}
CONTROL_COMPILE_OPTIMIZE_END