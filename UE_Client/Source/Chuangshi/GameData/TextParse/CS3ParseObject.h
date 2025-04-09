#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/TextParse/DefaultParse.h"
#include "CS3ParseObject.generated.h"

/**
* 文件名称：CS3ParseObject.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-09-18
*/

struct StructFormatInfo
{
	FString EscapeText = TEXT("");
	TMap<FString, FString> AttrInfos;
};

struct StructFormatTextInfo
{
	StructFormatInfo FormatInfo;
	FString TextInfo;
};

UCLASS(BlueprintType)
class CHUANGSHI_API UCS3ParseObject :public UCS3Object
{
	GENERATED_BODY()
public:
	UCS3ParseObject();
	~UCS3ParseObject();

	virtual void FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance);
	virtual FString TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos);
	virtual FString TransformExtraText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos);
public:
	FString EscapeText;
	TMap<FString, FString> KeyReplacementInfos;
	TArray<FString> SpecialKeys;
	TArray<FString> ExtraSpecialKeys;
};
