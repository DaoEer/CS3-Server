#include "LocalStortcutKeyData.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/LocalDataSaveManager.h"

ULocalStortcutKeyData::ULocalStortcutKeyData()
{
	if (!IsValid(UUECS3GameInstance::Instance)) return;
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString PlayerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerId, TEXT("playerName"));
	FileName = "LocalShortcutKeyData_" + PlayerName;
}

const FString & ULocalStortcutKeyData::GetFileName()
{
	return FileName;
}

void ULocalStortcutKeyData::SaveShortcutKeyDataByTypeToFile(SHORTCUTKEY_TYPE_ENUM Type, TArray<FSHORTCUTKEY> NewKeys)
{
	TArray<FSHORTCUTKEY> temp;
	for (int i = 0; i < ChangedKeys.Num(); i++)
	{
		if (ChangedKeys[i].KeyType != Type)
		{
			temp.Add(ChangedKeys[i]);
		}
		else
		{
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("SaveShortcutKeyDataToFile-->ChangedKeys[i]ActName=%s"), *FNAME_TO_FSTRING(ChangedKeys[i].ActName));
		}
	}
	ChangedKeys.Reset();
	ChangedKeys.Append(temp);
	ChangedKeys.Append(NewKeys);
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalStortcutKeyDataFile();
}

void ULocalStortcutKeyData::SaveShortcutKeyDataToFile(TArray<FSHORTCUTKEY> NewKeys)
{
	TArray<FSHORTCUTKEY> temp = ChangedKeys;
	for (auto data : NewKeys)
	{
		for (int i = 0; i < temp.Num(); i++)
		{
			if (ChangedKeys[i].ActName == data.ActName)
			{
				temp.RemoveAt(i);
				break;
			}
		}
	}
	ChangedKeys.Reset();
	ChangedKeys.Append(temp);
	ChangedKeys.Append(NewKeys);
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalStortcutKeyDataFile();
}