

#include "TextShieldMgr.h"
#include "GameData/ConstData.h"
#include"Chuangshi.h"
#include "GameData/GameDefault.h"
#include "Manager/CfgManager.h"

ShieldTextRegex::ShieldTextRegex()
{
	RegexSpecialKey.AddUnique(TEXT("\\"));
	RegexSpecialKey.AddUnique(TEXT("$"));
	RegexSpecialKey.AddUnique(TEXT("("));
	RegexSpecialKey.AddUnique(TEXT(")"));
	RegexSpecialKey.AddUnique(TEXT("*"));
	RegexSpecialKey.AddUnique(TEXT("+"));
	RegexSpecialKey.AddUnique(TEXT("."));
	RegexSpecialKey.AddUnique(TEXT("["));
	RegexSpecialKey.AddUnique(TEXT("]"));
	RegexSpecialKey.AddUnique(TEXT("?"));
	RegexSpecialKey.AddUnique(TEXT("^"));
	RegexSpecialKey.AddUnique(TEXT("{"));
	RegexSpecialKey.AddUnique(TEXT("}"));
	RegexSpecialKey.AddUnique(TEXT("|"));
}

ShieldTextRegex::~ShieldTextRegex()
{
	ShieldTextRegexList.Empty();
	RegexSpecialKey.Empty();
}

void ShieldTextRegex::InitRegexList()
{
	const UConfigTable* TextShieldTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TEXT_SHIELD_DATA);
	if (TextShieldTable)
	{
		TArray<FTEXT_SHIELD_DATA*> ShieldTextDatas;
		TextShieldTable->GetAllRows(ShieldTextDatas);
		TArray<FString> ShieldKeyWords;
		int32 Amount = 0;
		for (auto ShieldTextData : ShieldTextDatas)
		{
			FString ShileKeyWord = ShieldTextData->ShieldText.TrimStartAndEnd();
			ShileKeyWord = ReplaceRegexSpecialKey(ShileKeyWord);
			ShieldKeyWords.AddUnique(ShileKeyWord);
			Amount += 1;
			if (Amount % SHIELD_MAX_ROW_LENGTH == 0)
			{
				FString PatternStr = FString::Join(ShieldKeyWords, TEXT("|"));
				ShieldTextRegexList.Add(FRegexPattern(PatternStr));
				ShieldKeyWords.Empty();
			}
		}
		if (Amount % SHIELD_MAX_ROW_LENGTH != 0)
		{
			FString PatternStr = FString::Join(ShieldKeyWords, TEXT("|"));
			ShieldTextRegexList.Add(FRegexPattern(PatternStr));
		}
	}
}

FString ShieldTextRegex::ReplaceRegexSpecialKey(FString MsgText)
{
	FString NewMsgText(*MsgText);
	for (auto SpecialKey:RegexSpecialKey)
	{
		NewMsgText.ReplaceInline(*SpecialKey, *(TEXT("\\") + SpecialKey) );
	}
	return NewMsgText;
}

UTextShieldMgr::UTextShieldMgr()
{

}

UTextShieldMgr::~UTextShieldMgr()
{

}

UTextShieldMgr* UTextShieldMgr::GetInstance()
{
	cs3_checkNoReentry();
	UTextShieldMgr* Instance = NewObject<UTextShieldMgr>();
	Instance->InitInstance();
	return Instance;
}

void UTextShieldMgr::InitInstance()
{
	ShieldTextRegexIns = ShieldTextRegex();
	ShieldTextRegexIns.InitRegexList();
}

bool UTextShieldMgr::HasShieldText(FString MsgText)
{
	if (UUECS3GameInstance::Instance->GameDefault->bIsUseShieldText == false)
	{
		return false;
	}
	for (auto RePattern : ShieldTextRegexIns.ShieldTextRegexList)
	{
		FRegexMatcher ShieldMatcher(RePattern, MsgText);
		if (ShieldMatcher.FindNext())
		{
			return true;
		}
	}
	return false;
}

FString UTextShieldMgr::FilterMsgText(FString MsgText)
{
	FString NewMsgText = MsgText;
	if (UUECS3GameInstance::Instance->GameDefault->bIsUseShieldText == false)
	{
		return NewMsgText;
	}
	for (auto RePattern : ShieldTextRegexIns.ShieldTextRegexList)
	{
		FRegexMatcher ShieldMatcher(RePattern, MsgText);
		while(ShieldMatcher.FindNext())
		{
			int32 MatchStart = ShieldMatcher.GetMatchBeginning();
			int32 MatchEnd = ShieldMatcher.GetMatchEnding();
			NewMsgText = NewMsgText.Mid(0, MatchStart) + FString::ChrN( MatchEnd - MatchStart, TCHAR('*')) + NewMsgText.Mid(MatchEnd);
		}
		if (NewMsgText.Equals(FString::ChrN(MsgText.Len(), TCHAR('*'))))
		{
			break;
		}
	}
	return NewMsgText;
}
