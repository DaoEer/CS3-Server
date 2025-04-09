

#include "NewLineParse.h"

UNewLineParse::UNewLineParse()
{
	EscapeText = TEXT("@B");
	SpecialKeys.Add(TEXT("newlineText"));
}

UNewLineParse::~UNewLineParse()
{

}

void UNewLineParse::FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance)
{
	StructSpecialFormatText ScopeFormatText = DefaultParseInstance.GetFormatText(OriginText);
	if (ScopeFormatText.SpecialFormatText.IsEmpty())
	{
		//FormatInfo.Add(TEXT("newlineText"), TEXT("\\n"));
		FormatInfo.Add(TEXT("newlineText"), TEXT("<br/>"));
	}
	else
	{
		int32 count = DefaultParseInstance.TransInt(ScopeFormatText.SpecialFormatText);
		count = FMath::Max(count, 1);
		FString NewlineFormatText;
		for (int32 i = 0; i < count; i++)
		{
			//NewlineFormatText += TEXT("\\n");
			NewlineFormatText += TEXT("<br/>");
		}
		FormatInfo.Add(TEXT("newlineText"), NewlineFormatText);
	}
	LeaveText = ScopeFormatText.UnformattedText;
}

FString UNewLineParse::TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos)
{
	FString FinalText;
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
		if (!StrValue.IsEmpty())
		{
			FinalText += FString::Printf(TEXT("%s"), *StrValue);
		}
	}
	FinalText += TransformExtraText(OriginText, AttrInfos, LastAttrInfos);
	return FinalText;
}

