

#include "RestoreFormatParse.h"

URestoreFormatParse::URestoreFormatParse()
{
	EscapeText = TEXT("@D");
}

URestoreFormatParse::~URestoreFormatParse()
{

}

void URestoreFormatParse::FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance)
{
	StructSpecialFormatText ScopeFormatText = DefaultParseInstance.GetFormatText(OriginText);
	LeaveText = ScopeFormatText.UnformattedText;
}

FString URestoreFormatParse::TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos)
{
	LastAttrInfos.Empty();
	return Super::TransformExtraText(OriginText,AttrInfos,LastAttrInfos);
}

