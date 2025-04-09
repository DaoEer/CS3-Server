

#include "FontParse.h"

UFontParse::UFontParse()
{
	EscapeText = TEXT("@F");
	KeyReplacementInfos.Add(TEXT("n"), TEXT("fontPath"));
	KeyReplacementInfos.Add(TEXT("ft"), TEXT("fontType"));
	KeyReplacementInfos.Add(TEXT("fs"), TEXT("fontSize"));
	KeyReplacementInfos.Add(TEXT("fc"), TEXT("color"));
	KeyReplacementInfos.Add(TEXT("sc"), TEXT("shadowColor"));
	KeyReplacementInfos.Add(TEXT("so"), TEXT("shadowOffset"));
	SpecialKeys.Add(TEXT("fontPath"));
	SpecialKeys.Add(TEXT("fontType"));
	SpecialKeys.Add(TEXT("fontSize"));
	SpecialKeys.Add(TEXT("color"));
	SpecialKeys.Add(TEXT("shadowColor"));
	SpecialKeys.Add(TEXT("shadowOffset"));
}

UFontParse::~UFontParse()
{

}

void UFontParse::FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance)
{
	StructSpecialFormatText ScopeFormatText = DefaultParseInstance.GetFormatText(OriginText);
	FString SpecialFormatText = ScopeFormatText.SpecialFormatText;
	if(!SpecialFormatText.IsEmpty())
	{
		DefaultParseInstance.GetAttrInfos(SpecialFormatText, FormatInfo, KeyReplacementInfos);
		FString* ColorPtr = FormatInfo.Find(TEXT("color"));
		if (ColorPtr != nullptr)
		{
			FString ColorValue = *ColorPtr;
			ColorValue = DefaultParseInstance.TransColor(ColorValue);
			FormatInfo[TEXT("color")] = ColorValue;
		}
		FString* ShadowColorPtr = FormatInfo.Find(TEXT("shadowColor"));
		if (ShadowColorPtr != nullptr)
		{
			FString ShadowColorValue = *ShadowColorPtr;
			ShadowColorValue = DefaultParseInstance.TransColor(ShadowColorValue);
			FormatInfo[TEXT("shadowColor")] = ShadowColorValue;
		}
	}
	LeaveText = ScopeFormatText.UnformattedText;
}

FString UFontParse::TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos)
{
	FString FinalText = TEXT("<text");
	FString *CurrentPtr, *LastPtr;
	for (auto SpecialKey:SpecialKeys)
	{
		FString StrValue = TEXT("");
		CurrentPtr = AttrInfos.Find(SpecialKey);
		LastPtr = LastAttrInfos.Find(SpecialKey);
		if (CurrentPtr != nullptr)
		{
			StrValue = *CurrentPtr;
		}
		else
		{
			if (LastPtr != nullptr)
			{
				StrValue = *LastPtr;
			}
		}
		if (!StrValue.IsEmpty())
		{
			FinalText += FString::Printf(TEXT(" %s=\"%s\""), *SpecialKey, *StrValue);
		}
	}
	FinalText += TEXT(">");
	FinalText += OriginText;
	FinalText += TEXT("</text>");
	return FinalText;
}
