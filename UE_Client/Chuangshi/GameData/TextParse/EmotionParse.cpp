

#include "EmotionParse.h"

UEmotionParse::UEmotionParse()
{

}

UEmotionParse::~UEmotionParse()
{

}

void UEmotionParse::FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance)
{
	Super::FormatText(OriginText, FormatInfo, LeaveText, DefaultParseInstance);
}

FString UEmotionParse::TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos)
{
	return Super::TransformText(OriginText, AttrInfos, LastAttrInfos);
}
