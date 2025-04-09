

#include "CS3ParseObject.h"

UCS3ParseObject::UCS3ParseObject()
{
	EscapeText = TEXT("");
	ExtraSpecialKeys.Add(TEXT("fontPath"));
	ExtraSpecialKeys.Add(TEXT("fontType"));
	ExtraSpecialKeys.Add(TEXT("fontSize"));
	ExtraSpecialKeys.Add(TEXT("color"));
	ExtraSpecialKeys.Add(TEXT("shadowColor"));
	ExtraSpecialKeys.Add(TEXT("shadowOffset"));
}

UCS3ParseObject::~UCS3ParseObject()
{

}

void UCS3ParseObject::FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance)
{

}

FString UCS3ParseObject::TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos)
{
	return OriginText;
}

FString UCS3ParseObject::TransformExtraText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos)
{
	FString FinalText = TEXT("<text");
	FString *LastPtr;
	for (auto SpecialKey : ExtraSpecialKeys)
	{
		FString StrValue = TEXT("");
		LastPtr = LastAttrInfos.Find(SpecialKey);
		if (LastPtr != nullptr)
		{
			StrValue = *LastPtr;
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
