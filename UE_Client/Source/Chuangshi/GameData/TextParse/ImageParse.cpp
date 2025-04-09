

#include "ImageParse.h"

UImageParse::UImageParse()
{
	EscapeText = TEXT("@I");
	KeyReplacementInfos.Add(TEXT("m"), TEXT("href"));
	KeyReplacementInfos.Add(TEXT("p"), TEXT("src"));
	SpecialKeys.Add(TEXT("href"));
	SpecialKeys.Add(TEXT("src"));
}

UImageParse::~UImageParse()
{

}

void UImageParse::FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance)
{
	StructSpecialFormatText ScopeFormatText = DefaultParseInstance.GetFormatText(OriginText);
	FString SpecialFormatText = ScopeFormatText.SpecialFormatText;
	if (!SpecialFormatText.IsEmpty())
	{
		DefaultParseInstance.GetAttrInfos(SpecialFormatText, FormatInfo, KeyReplacementInfos);
	}
	LeaveText = ScopeFormatText.UnformattedText;
}

FString UImageParse::TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos)
{
	FString FinalText;
	FString *HyperLinkPtr;
	HyperLinkPtr = AttrInfos.Find(TEXT("href"));
	if (HyperLinkPtr != nullptr)
	{
		FinalText += TEXT("<a id=\"HyperlinkDecorator\" style=\"Hyperlink\"");
		FinalText += *HyperLinkPtr;
		FinalText += TEXT(">");
	}
	
	FinalText += TEXT("<img");
	FString *CurrentPtr, *LastPtr;
	for (auto SpecialKey : SpecialKeys)
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
		if ((!StrValue.IsEmpty()) && (!SpecialKey.Equals("href")))
		{
			FinalText += FString::Printf(TEXT(" %s=\"%s\""), *SpecialKey, *StrValue);
		}
	}
	FinalText += TEXT("/>");
	if (HyperLinkPtr != nullptr)
	{
		FinalText += TEXT("</>");
	}
	FinalText += TransformExtraText(OriginText, AttrInfos, LastAttrInfos);
	return FinalText;
}
