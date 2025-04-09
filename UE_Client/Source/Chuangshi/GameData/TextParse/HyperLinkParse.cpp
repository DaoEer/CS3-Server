

#include "HyperLinkParse.h"

/**
* 文件名称：HyperLinkParse.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-09-18
*/

UHyperLinkParse::UHyperLinkParse()
{
	EscapeText = TEXT("@L");
	KeyReplacementInfos.Add(TEXT("n"), TEXT("fontPath"));
	KeyReplacementInfos.Add(TEXT("fs"), TEXT("fontSize"));
	KeyReplacementInfos.Add(TEXT("sc"), TEXT("shadowColor"));
	KeyReplacementInfos.Add(TEXT("so"), TEXT("shadowOffset"));
	KeyReplacementInfos.Add(TEXT("t"), TEXT("text"));
	KeyReplacementInfos.Add(TEXT("m"), TEXT("href"));
	KeyReplacementInfos.Add(TEXT("cfc"), TEXT("color"));
	KeyReplacementInfos.Add(TEXT("bs"), TEXT("bstyle"));
	SpecialKeys.Add(TEXT("fontPath"));
	SpecialKeys.Add(TEXT("fontSize"));
	SpecialKeys.Add(TEXT("shadowColor"));
	SpecialKeys.Add(TEXT("shadowOffset"));
	SpecialKeys.Add(TEXT("text"));
	SpecialKeys.Add(TEXT("href"));
	SpecialKeys.Add(TEXT("color"));
	SpecialKeys.Add(TEXT("bstyle"));
}

UHyperLinkParse::~UHyperLinkParse()
{

}

void UHyperLinkParse::FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance)
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

FString UHyperLinkParse::TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos)
{
	FString *HyperLinkPtr;
	FString HyperLinkText;
	HyperLinkPtr = AttrInfos.Find(TEXT("text"));
	if (HyperLinkPtr != nullptr)
	{
		HyperLinkText = *HyperLinkPtr;
	}
	FString FinalText = TEXT("<a id=\"HyperlinkDecorator\" style=\"Hyperlink\"");
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
		if ((!StrValue.IsEmpty()) && (!SpecialKey.Equals("text")))
		{
			FinalText += FString::Printf(TEXT(" %s=\"%s\""), *SpecialKey, *StrValue);
		}
	}
	FinalText += TEXT(">");
	FinalText += HyperLinkText;
	FinalText += TEXT("</>");
	FinalText += TransformExtraText(OriginText, AttrInfos, LastAttrInfos);
	return FinalText;
}
