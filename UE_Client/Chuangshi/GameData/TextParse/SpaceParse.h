#pragma once
#include "CoreMinimal.h"
#include "GameData/TextParse/CS3ParseObject.h"
#include "SpaceParse.generated.h"

/**
* 文件名称：SpaceParse.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-09-18
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USpaceParse :public UCS3ParseObject
{
	GENERATED_BODY()
public:
	USpaceParse();
	~USpaceParse();

	virtual void FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance) override;
	virtual FString TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos) override;

};