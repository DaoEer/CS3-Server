#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/TextParse/CS3ParseObject.h"
#include "GameData/TextParse/DefaultParse.h"
#include "GameData/TextParse/ByHeadParse.h"
#include "GameData/TextParse/EmotionParse.h"
#include "GameData/TextParse/FontParse.h"
#include "GameData/TextParse/HyperLinkParse.h"
#include "GameData/TextParse/ImageParse.h"
#include "GameData/TextParse/NewLineParse.h"
#include "GameData/TextParse/SpaceParse.h"
#include "GameData/TextParse/RestoreFormatParse.h"
#include "Internationalization/Regex.h"
#include "TextParseManager.generated.h"

/*
* 文件名称：TextParseManager.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-07-18
*/

class RegexManager
{
public:
	RegexManager();
	~RegexManager();
public:
	FRegexPattern SplitPattern;
};



UCLASS(BlueprintType)
class CHUANGSHI_API UTextParseManger : public UCS3Object
{
	GENERATED_BODY()
public:
	UTextParseManger();
	~UTextParseManger();
	static UTextParseManger* GetInstance();
	void Init();
	void ParseText(FString OriginText, TArray<StructFormatTextInfo>& FormatTextInfos);
	UFUNCTION(BlueprintPure, Category = "TextParseManger")
	FString TransformText(FString OriginText);

private:
	void AddFormatInfo(TArray<StructFormatTextInfo>& FormatTextInfos, FString EscapeText, FString OriginText);

private:
	//static UTextParseManger* Instance;
	DefaultParse DefaultParseInstance;
	RegexManager RegexMgrInstance;
	UPROPERTY()
	TMap<FString, UCS3ParseObject*> AllParses;
	TMap<FString, FString> KeyReplacements;

};

