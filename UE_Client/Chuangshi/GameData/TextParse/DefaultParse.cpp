
#include "DefaultParse.h"
#include "GameData/ColorAliasData.h"
#include "Manager/CfgManager.h"
#include "UObject/ConstructorHelpers.h"
#include "Util/GolbalBPFunctionLibrary.h"

DefaultParse::DefaultParse()
	:ScopePattern(FRegexPattern((TEXT("\\{.*[^\\\\]\\}"))))
	//, SplitPattern(FRegexPattern((TEXT("\\w+\\s*=\\s*[^'].*?(?=;)|\\w+\\s*=\\s*'.*?'|\\w+\\s*=\\s*[^'].*|\\w+\\s*=\\s*'.*"))))
	, IntPattern(FRegexPattern((TEXT("^[\\+\\-]{0,1}\\d+$"))))
	, FloatPattern(FRegexPattern((TEXT("^([\\+\\-]{0,1}\\d*)(\\.\\d*)?$"))))
	, ColorPattern(FRegexPattern(TEXT("^\\(((?:\\s*?\\d+\\s*?,){2,3})\\s*?\\d+\\s*?\\)$|^\\s*?c\\d{1,3}\\s*$")))
{
	
}

DefaultParse::~DefaultParse()
{

}

struct StructSpecialFormatText DefaultParse::GetFormatText(FString Text)
{
	FString FormatText = "";
	FString UnformattedText = Text;
	struct StructSpecialFormatText ScopeFormatText = {FormatText,UnformattedText };
	FRegexMatcher ScopeMatcher(ScopePattern, Text);
	if (ScopeMatcher.FindNext())
	{
		int32 MatchStart = ScopeMatcher.GetMatchBeginning();
		int32 MatchEnd = ScopeMatcher.GetMatchEnding();
		if (MatchStart != 0)
		{
			return ScopeFormatText;
		}
		else
		{
			FormatText = Text.Mid(1, MatchEnd - MatchStart - 2).TrimStartAndEnd();//去掉两边的{}，并且去除空字符
			FormatText = FormatText.Replace(TEXT("\\}"), TEXT("}"));
			UnformattedText = Text.Mid(MatchEnd);
			ScopeFormatText.SpecialFormatText = FormatText;
			ScopeFormatText.UnformattedText = UnformattedText;
			return ScopeFormatText;
		}
	}
	else
	{
		return ScopeFormatText;
	}
	
}

struct StructSpecialFormatText DefaultParse::GetSpeicalFormatText(FString Text)
{
	int32 StartIndex = Text.Find("{");
	FString SpecialText = Text.Mid(StartIndex);
	return GetFormatText(SpecialText);
}

void DefaultParse::GetAttrInfos(FString AttrsText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& KeyReplacementInfos)
{
	TArray<FString> AttrInfoList = UGolbalBPFunctionLibrary::SplitString(AttrsText, false, TEXT(";"));
	for (auto AttrInfo:AttrInfoList)
	{
		FString AttrText, StrKey, StrValue;
		AttrInfo.Split(TEXT("="), &StrKey, &StrValue);
		StrKey = StrKey.TrimStartAndEnd();
		FString* ReplaceKeyPtr = KeyReplacementInfos.Find(StrKey);
		if (ReplaceKeyPtr != nullptr)
		{
			StrKey = *ReplaceKeyPtr;
		}
		StrValue = StrValue.TrimStartAndEnd();
		StrValue = StrValue.Replace(TEXT("\'"), TEXT(""));
		if (StrKey != "" && StrValue != "")
		{
			AttrInfos.Add(StrKey, StrValue);
		}

	}
	//FRegexMatcher SplitMatcher(SplitPattern, AttrsText);
	//while (SplitMatcher.FindNext())
	//{
	//	int32 MatchStart = SplitMatcher.GetMatchBeginning();
	//	int32 MatchEnd = SplitMatcher.GetMatchEnding();
	//	FString AttrText, StrKey, StrValue;
	//	AttrText = AttrsText.Mid(MatchStart, MatchEnd - MatchStart);
	//	AttrsText.Split(TEXT("="), &StrKey, &StrValue);
	//	StrKey = StrKey.TrimStartAndEnd();
	//	FString* ReplaceKeyPtr = KeyReplacementInfos.Find(StrKey);
	//	if (ReplaceKeyPtr != nullptr)
	//	{
	//		StrKey = *ReplaceKeyPtr;
	//	}
	//	StrValue = StrValue.TrimStartAndEnd();
	//	if (StrValue.StartsWith(TEXT("\'")))
	//	{
	//		StrValue = StrValue.Mid(1);
	//	}
	//	if (StrKey != "" && StrValue != "")
	//	{
	//		AttrInfos.Add(StrKey, StrValue);
	//	}
	//}
}

int DefaultParse::TransInt(FString StrInt)
{
	return FCString::Atoi(*StrInt);
}

float DefaultParse::TransFloat(FString StrFloat)
{
	return FCString::Atof(*StrFloat);
}

FString DefaultParse::TransColor(FString StrColor)
{
	FRegexMatcher ColorMatcher(ColorPattern, StrColor);
	if (!ColorMatcher.FindNext())
	{
		return "";
	}
	else
	{
#if WITH_EDITOR // 在CST-7688需求中,需要在游戏未启动得时候使用富文本控件
		UDataTable* DT_ColorAliasCfg = LoadObject<UDataTable>(NULL, TEXT("/Game/Miscs/ContentConfig/UI/DT_ColorAliasCfg.DT_ColorAliasCfg"), NULL, LOAD_None, NULL);
		const FCOLOR_ALIAS_DATA* ColorAliasData;
		if (DT_ColorAliasCfg == nullptr)
		{
			ColorAliasData = nullptr;
		}
		else
		{
			ColorAliasData = (FCOLOR_ALIAS_DATA*)DT_ColorAliasCfg->FindRowUnchecked(FName(*StrColor.TrimStartAndEnd()));
		}
#else
		const UConfigTable* ColorAliasTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_COLOR_ALIAS);
		const FCOLOR_ALIAS_DATA* ColorAliasData = ColorAliasTable->GetRow<FCOLOR_ALIAS_DATA>(StrColor.TrimStartAndEnd());
#endif
		
		if (ColorAliasData != nullptr)
		{
			FColor Color = ColorAliasData->Color;
			return TEXT("#") + Color.ToHex();
		}
		else
		{
			int32 MatchStart = ColorMatcher.GetMatchBeginning();
			int32 MatchEnd = ColorMatcher.GetMatchEnding();
			FString ColorText;
			ColorText = StrColor.Mid(MatchStart, MatchEnd - MatchStart);
			ColorText = ColorText.Replace(TEXT("("), TEXT(""));
			ColorText = ColorText.Replace(TEXT(")"), TEXT(""));
			TArray<FString> TransColorList = UGolbalBPFunctionLibrary::SplitString(ColorText, false, TEXT(","));
			if (TransColorList.Num() == 3)
			{
				int R, G, B;
				R = FMath::Min(FCString::Atoi(*TransColorList[0]), 255);
				G = FMath::Min(FCString::Atoi(*TransColorList[1]), 255);
				B = FMath::Min(FCString::Atoi(*TransColorList[2]), 255);
				FColor Color(R, G, B);
				return TEXT("#") + Color.ToHex();
			}
			else if (TransColorList.Num() == 4)
			{
				int R, G, B, A;
				R = FMath::Min(FCString::Atoi(*TransColorList[0]), 255);
				G = FMath::Min(FCString::Atoi(*TransColorList[1]), 255);
				B = FMath::Min(FCString::Atoi(*TransColorList[2]), 255);
				A = FMath::Min(FCString::Atoi(*TransColorList[3]), 255);
				FColor Color(R, G, B, A);
				return TEXT("#") + Color.ToHex();
			}
		}
	}
	return "";
}