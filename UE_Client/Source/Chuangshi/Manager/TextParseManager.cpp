

#include "TextParseManager.h"
#include"Chuangshi.h"

CONTROL_COMPILE_OPTIMIZE_START

RegexManager::RegexManager()
	:SplitPattern(FRegexPattern(TEXT("@F|@B|@S|@I|@L|\\$by|\\$emote|@D")))
{
}

RegexManager::~RegexManager()
{
}

void UTextParseManger::AddFormatInfo(TArray<StructFormatTextInfo>& FormatTextInfos, FString EscapeText, FString OriginText)
{
	if (EscapeText.IsEmpty() && OriginText.IsEmpty())
	{
		return;
	}
	StructFormatTextInfo FormatTextInfo;
	FormatTextInfo.FormatInfo.EscapeText = EscapeText;
	if (EscapeText.Equals(""))
	{
		FormatTextInfo.TextInfo = OriginText;
		FormatTextInfos.Add(FormatTextInfo);
	}
	else
	{
		if (AllParses.Find(EscapeText) == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTextParseManger::AddFormatInfo : EscapeText!"));
			return;
		}
		UCS3ParseObject*  ParseObject = *(AllParses.Find(EscapeText));
		TMap<FString, FString> AttrInfos;
		FString LeaveText;
		ParseObject->FormatText(OriginText, AttrInfos, LeaveText, DefaultParseInstance);
		if (AttrInfos.Num() > 0)
		{
			FormatTextInfo.FormatInfo.AttrInfos = AttrInfos;
		}
		if (!LeaveText.IsEmpty())
		{
			FormatTextInfo.TextInfo = LeaveText;
		}
		if (EscapeText.Equals("@S") || EscapeText.Equals("$by"))
		{
			if (FormatTextInfos.Num() > 0)
			{
				FString LastEscapeText = FormatTextInfos.Last().FormatInfo.EscapeText;
				FormatTextInfos.Last().TextInfo += FormatTextInfo.TextInfo;
			}
			else
			{
				FormatTextInfos.Add(FormatTextInfo);
			}
		}
		else
		{
			FormatTextInfos.Add(FormatTextInfo);
		}
	}
	
}



UTextParseManger::UTextParseManger()
{
	
}

UTextParseManger::~UTextParseManger()
{
	//C_SAFE_DELETE(DefaultParseInstance);
	//C_SAFE_DELETE(RegexMgrInstance);
	//AllParses.Remove(TEXT("@F"));
	//AllParses.Remove(TEXT("@B"));
	//AllParses.Remove(TEXT("@S"));
	//AllParses.Remove(TEXT("@I"));
	//AllParses.Remove(TEXT("@L"));
	//AllParses.Remove(TEXT("$by"));
	//AllParses.Remove(TEXT("$emote"));
	//AllParses.Remove(TEXT("@D"));
}

UTextParseManger* UTextParseManger::GetInstance()
{
	cs3_checkNoReentry();

	UTextParseManger* Instance = NewObject<UTextParseManger>();
	Instance->Init();

	return Instance;
}

void UTextParseManger::Init()
{
	DefaultParseInstance = DefaultParse();
	RegexMgrInstance = RegexManager();
	AllParses.Add(TEXT("@F"), NewObject<UFontParse>());
	AllParses.Add(TEXT("@B"), NewObject<UNewLineParse>());
	AllParses.Add(TEXT("@S"), NewObject<USpaceParse>());
	AllParses.Add(TEXT("@I"), NewObject<UImageParse>());
	AllParses.Add(TEXT("@L"), NewObject<UHyperLinkParse>());
	AllParses.Add(TEXT("$by"), NewObject<UByHeadParse>());
	AllParses.Add(TEXT("$emote"), NewObject<UEmotionParse>());
	AllParses.Add(TEXT("@D"), NewObject<URestoreFormatParse>());
	KeyReplacements.Add(TEXT("&nbsp;"), TEXT(" "));
	KeyReplacements.Add(TEXT("&quot;"), TEXT("\""));
	KeyReplacements.Add(TEXT("&amp;"), TEXT("&"));
	KeyReplacements.Add(TEXT("&apos;"), TEXT("\'"));
	KeyReplacements.Add(TEXT("&lt;"), TEXT("<"));
	KeyReplacements.Add(TEXT("&gt;"), TEXT(">"));
}

void UTextParseManger::ParseText(FString OriginText, TArray<StructFormatTextInfo>& FormatTextInfos)
{
	FRegexMatcher SplitMatcher(RegexMgrInstance.SplitPattern, OriginText);
	int32 CurrentStart = 0;
	FString CurrentEscape = TEXT("");
	while (true)
	{
		if (SplitMatcher.FindNext())
		{
			int32 MatchStart = SplitMatcher.GetMatchBeginning();
			int32 MatchEnd = SplitMatcher.GetMatchEnding();
			FString EscapeText;
			EscapeText = OriginText.Mid(MatchStart, MatchEnd - MatchStart);
			FString IncludedText = OriginText.Mid(CurrentStart, MatchStart - CurrentStart);
			AddFormatInfo(FormatTextInfos, CurrentEscape, IncludedText);
			CurrentEscape = EscapeText;
			CurrentStart = MatchEnd;
		}
		else
		{
			FString IncludedText = OriginText.Mid(CurrentStart);
			AddFormatInfo(FormatTextInfos, CurrentEscape, IncludedText);
			break;
		}

	}
}

FString UTextParseManger::TransformText(FString OriginText)
{
	FString BeginText = OriginText;
	FString FinalText;
	TArray<StructFormatTextInfo> FormatTextInfos;
	TMap<FString, FString> LastAttrInfos;
	for (auto KeyReplacement:KeyReplacements)
	{
		BeginText = BeginText.Replace(*KeyReplacement.Key, *KeyReplacement.Value);
	}
	
	ParseText(BeginText, FormatTextInfos);
	for (auto FormatTextInfo:FormatTextInfos)
	{
		FString EscapeText = FormatTextInfo.FormatInfo.EscapeText;
		if (EscapeText.Equals(""))
		{
			FinalText += FormatTextInfo.TextInfo;
		}
		else
		{
			if (AllParses.Find(EscapeText) == nullptr)
			{
				CS3_Warning(TEXT("-->Null Pointer error:UTextParseManger::TransformText : EscapeText!"));
				FinalText += FormatTextInfo.TextInfo;
				continue;
			}
			UCS3ParseObject*  ParseObject = *(AllParses.Find(EscapeText));
			FinalText += ParseObject->TransformText(FormatTextInfo.TextInfo, FormatTextInfo.FormatInfo.AttrInfos, LastAttrInfos);
			LastAttrInfos.Append(FormatTextInfo.FormatInfo.AttrInfos);
		}
	}
	return FinalText;
}

CONTROL_COMPILE_OPTIMIZE_END
