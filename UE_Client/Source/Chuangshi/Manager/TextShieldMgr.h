#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/TextShield/TextShieldData.h"
#include "Internationalization/Regex.h"
#include "TextShieldMgr.generated.h"

/*
* 文件名称：TextShieldMgr.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2018-01-11
*/

class ShieldTextRegex
{
public:
	ShieldTextRegex();
	~ShieldTextRegex();
	void InitRegexList();
	FString ReplaceRegexSpecialKey(FString MsgText);
public:
	TArray<FString> RegexSpecialKey;
	TArray<FRegexPattern> ShieldTextRegexList;
};

UCLASS(BlueprintType)
class CHUANGSHI_API UTextShieldMgr : public UCS3Object
{
	GENERATED_BODY()
public:
	UTextShieldMgr();
	~UTextShieldMgr();
	static UTextShieldMgr* GetInstance();
	void InitInstance();

	//判断是否包含需要屏蔽的关键字
	UFUNCTION(BlueprintCallable, Category = "TextShieldManager")
	bool HasShieldText(FString MsgText);

	//过滤屏蔽的关键字并替换成*
	UFUNCTION(BlueprintCallable, Category = "TextShieldManager")
	FString FilterMsgText(FString MsgText);

private:
	ShieldTextRegex ShieldTextRegexIns;
};