

#include "SpaceParse.h"

USpaceParse::USpaceParse()
{
	EscapeText = TEXT("@S");
}

USpaceParse::~USpaceParse()
{

}

void USpaceParse::FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance)
{
	StructSpecialFormatText ScopeFormatText = DefaultParseInstance.GetFormatText(OriginText);
	if (ScopeFormatText.SpecialFormatText.IsEmpty())
	{
		LeaveText = TEXT(" ") + ScopeFormatText.UnformattedText;
	}
	else
	{
		int32 count = DefaultParseInstance.TransInt(ScopeFormatText.SpecialFormatText);
		count = FMath::Max(count, 1);
		for (int i=0;i<count;++i)
		{
			LeaveText += TEXT(" ");
		}
		LeaveText = LeaveText + ScopeFormatText.UnformattedText;
	}
}

FString USpaceParse::TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos)
{
	return TransformExtraText(OriginText, AttrInfos, LastAttrInfos);
}

