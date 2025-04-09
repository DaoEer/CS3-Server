// Fill out your copyright notice in the Description page of Project Settings.


#include "EmoteManager.h"
#include"Chuangshi.h"
#include "CfgManager.h"
#include "JsonWriter.h"

UEmoteManager::UEmoteManager()
{
	
}

UEmoteManager::~UEmoteManager()
{
	DefaultEmotes.Empty();
	CustomTextEmotes.Empty();
}

UEmoteManager* UEmoteManager::GetInstance()
{
	cs3_checkNoReentry();

	return (UEmoteManager*)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_EmoteManager")));
}

void UEmoteManager::Init()
{
	InitDefaultEmoteData();
	//InitCustomTextEmoteData();
}

FString UEmoteManager::GetFormatEmoteStr(const FString& replaceString)
{
	FString ReturnStr = replaceString;

	//正则表达式：\[#[^\[\]\s]+\]
	FRegexPattern StrPattern(TEXT("\\[#[^\\[\\]\\s]+\\]"));
	FRegexMatcher StrMatcher(StrPattern, replaceString);
	while (StrMatcher.FindNext())
	{
		int32 MatchStart = StrMatcher.GetMatchBeginning();
		int32 MatchEnd = StrMatcher.GetMatchEnding();
		FString MatchStr = replaceString.Mid(MatchStart, MatchEnd - MatchStart);//[#123]

		TArray<FString> SplitArray1 = UGolbalBPFunctionLibrary::SplitString(MatchStr, false, "[#");
		if (SplitArray1.Num() > 1)
		{
			TArray<FString> SplitArray2 = UGolbalBPFunctionLibrary::SplitString(SplitArray1[1], false, "]");
			if (SplitArray2.Num() > 0)
			{
				FString EmoteNameStr = SplitArray2[0];
				//配置了表情才替换，没有配置表情原样输出
				bool IsSuccess;
				FString EmoteStr = GetEmoteStr(EmoteNameStr, IsSuccess);
				if (IsSuccess)
				{
					ReturnStr = ReturnStr.Replace(*MatchStr, *EmoteStr);
				}
			}
		}
	}
	return ReturnStr;
}

FString UEmoteManager::GetEmoteStr(const FString& EmoteName, bool& IsSuccess)
{
	const FEMOTE_DATA EmoteData = GetDefaultEmoteDataByName(EmoteName, IsSuccess);
	if (IsSuccess)
	{
		return TEXT("@I{p=") + EmoteData.Sign + TEXT("}");
	}
	else
	{
		return EmoteName;
	}
}

FEMOTE_DATA UEmoteManager::GetDefaultEmoteDataBySign(FString Sign, bool& IsSuccess)
{
	for (TPair<FString, FEMOTE_DATA>& Emote : DefaultEmotes)
	{
		if (Emote.Value.Sign.Equals(Sign))
		{
			IsSuccess = true;
			return Emote.Value;
		}
	}
	
	CS3_Warning(TEXT("FEMOTE_DATA is NULL"));
	IsSuccess = false;
	return FEMOTE_DATA();
}

struct FEMOTE_DATA UEmoteManager::GetDefaultEmoteDataByName(FString Name, bool& IsSuccess)
{
	for (TPair<FString, FEMOTE_DATA>& Emote : DefaultEmotes)
	{
		if (Emote.Value.Name.Equals(Name))
		{
			IsSuccess = true;
			return Emote.Value;
		}
	}

	CS3_Warning(TEXT("FEMOTE_DATA is NULL"));
	IsSuccess = false;
	return FEMOTE_DATA();
}

FTEXT_EMOTE_DATA UEmoteManager::GetTextEmoteDataBySign(FString Sign)
{
	FTEXT_EMOTE_DATA TextEmoteData;
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (CfgManager)
	{
		const UConfigTable* TextEmoteTableCfg = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CUSTOM_TEXT_EMOTES);
		if (!TextEmoteTableCfg)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UEmoteManager::GetTextEmoteDataBySign : TextEmoteTableCfg!"));
			return TextEmoteData;
		}
		TArray<FName> RowNames = TextEmoteTableCfg->GetRowNames();
		for (auto& RowName : RowNames)
		{
			FString RowNameStr = FNAME_TO_FSTRING(RowName);
			FTEXT_EMOTE_DATA* FEmoteData = (FTEXT_EMOTE_DATA*)TextEmoteTableCfg->GetRow<FTEXT_EMOTE_DATA>(RowNameStr);
			if (FEmoteData && (FEmoteData->Sign == Sign))
			{
				return *FEmoteData;
			}
		}
	}
	return TextEmoteData;
}

void UEmoteManager::RestoreEmoteData(FString Sign)
{
	FTEXT_EMOTE_DATA CustomEmote;
	FEMOTE_DATA DefaultEmote;
	if (CustomTextEmotes.Contains(Sign))
	{
		CustomEmote = CustomTextEmotes[Sign];
		if (DefaultEmotes.Contains(Sign))
		{
			DefaultEmote = DefaultEmotes[Sign];
			CustomEmote.Name = DefaultEmote.Name;
			CustomEmote.HasTargetDes = DefaultEmote.HasTargetDes;
			CustomEmote.NoTargetDes = DefaultEmote.NoTargetDes;
			UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
			if (CfgManager)
			{
				const UConfigTable* EmoteTableCfg = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CUSTOM_TEXT_EMOTES);
				const UDataTable* BaseTable = EmoteTableCfg->GetBaseTable();
				TArray<FName> RowNames = EmoteTableCfg->GetRowNames();
				FTEXT_EMOTE_DATA* RowData = BaseTable->FindRow<FTEXT_EMOTE_DATA>(FSTRING_TO_FNAME(Sign), TEXT("DataTable FindRow Error!"));
				if (RowData == nullptr)
				{
					CS3_Warning(TEXT("-->Null Pointer error:UEmoteManager::RestoreEmoteData : RowData!"));
					return;
				}
				FString outStr;
				TSharedRef<TJsonWriter<TCHAR>> JsonWriter = TJsonWriterFactory<TCHAR>::Create(&outStr);
//				JsonWriter.WriteValue(TEXT("Name"), DefaultEmote.Name);

//				BaseTable->WriteRowAsJSON(JsonWriter, RowData, );
				OnRestoreTextEmoteDataBP(Sign);
			}

		}
	}
}

void UEmoteManager::ChangeTextEmoteData(const FString &Sign, const FString &Name, const FString &NoTargetDes, const FString &HasTargetDes)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (CfgManager)
	{
		const UConfigTable* EmoteTableCfg = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_DEFAULT_EMOTES);
		if (!EmoteTableCfg)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UEmoteManager::ChangeTextEmoteData : EmoteTableCfg!"));
			return;
		}
		//已在自定义数据中
		if (CustomTextEmotes.Contains(Sign))
		{
			FTEXT_EMOTE_DATA CustomEmote = CustomTextEmotes[Sign];
			CustomEmote.Name = Name;
			CustomEmote.NoTargetDes = NoTargetDes;
			CustomEmote.HasTargetDes = HasTargetDes;
			const UDataTable* BaseTable = EmoteTableCfg->GetBaseTable();
			FTEXT_EMOTE_DATA* RowData = BaseTable->FindRow<FTEXT_EMOTE_DATA>(FSTRING_TO_FNAME(Sign), TEXT("DataTable FindRow Error!"));
			if (RowData == nullptr)
			{
				CS3_Warning(TEXT("-->Null Pointer error:UEmoteManager::ChangeTextEmoteData : RowData!"));
				return;
			}
			//RowData
		}
	}
}


void UEmoteManager::InitDefaultEmoteData()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (CfgManager)
	{
		const UConfigTable* EmoteTableCfg = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_DEFAULT_EMOTES);
		if (!EmoteTableCfg)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UEmoteManager::InitDefaultEmoteData : EmoteTableCfg!"));
			return;
		}
		TArray<FName> EmoteRowNames = EmoteTableCfg->GetRowNames();
		for (auto& RowName : EmoteRowNames)
		{
			FString RowNameStr = FNAME_TO_FSTRING(RowName);
			FEMOTE_DATA* EmoteData = (FEMOTE_DATA*)EmoteTableCfg->GetRow<FEMOTE_DATA>(RowNameStr);
			if (!DefaultEmotes.Contains(RowNameStr))
			{
				DefaultEmotes.Add(RowNameStr, (*EmoteData));
			}
		}
	}
}

void UEmoteManager::InitCustomTextEmoteData()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (CfgManager)
	{
		const UConfigTable* TextEmoteTableCfg = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CUSTOM_TEXT_EMOTES);
			if (!TextEmoteTableCfg)
			{
				CS3_Warning(TEXT("-->Null Pointer error:UEmoteManager::InitCustomTextEmoteData : TextEmoteTableCfg!"));
				return;
			}
		TArray<FName> RowNames = TextEmoteTableCfg->GetRowNames();
		for (auto& RowName : RowNames)
		{
			FString RowNameStr = FNAME_TO_FSTRING(RowName);
			FTEXT_EMOTE_DATA* EmoteData = (FTEXT_EMOTE_DATA*)TextEmoteTableCfg->GetRow<FTEXT_EMOTE_DATA>(RowNameStr);
			if (!CustomTextEmotes.Contains(RowNameStr))
			{
				CustomTextEmotes.Add(RowNameStr, (*EmoteData));
			}
		}
	}
}


bool UEmoteManager::CreateNewTextEmoteData(const FString &Sign, const FString &Name, const FString &NoTargetDes, const FString &HasTargetDes)
{
	if (DefaultEmotes.Contains(Sign))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Emote Config Already Has Emote Sign %s"), *Sign);
		return false;
	}
	OnCreateTextEmoteDataBP(Sign);
	return true;
}


void UEmoteManager::RemoveTextEmoteData(FString Sign)
{
	if (DefaultEmotes.Contains(Sign))
	{
		DefaultEmotes.Remove(Sign);
		OnRemoveTextEmoteDataBP(Sign);
	}
}


