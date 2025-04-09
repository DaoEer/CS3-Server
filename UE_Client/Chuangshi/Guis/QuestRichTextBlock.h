#pragma once
#include "CoreMinimal.h"
#include "Guis/CS3RichTextBlock.h"
#include "QuestRichTextBlock.generated.h"

/*
* 文件名称：QuestRichTextBlock.h
* 功能说明：富文本控件
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-08-30
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UQuestRichTextBlock : public UCS3RichTextBlock
{
	GENERATED_BODY()
public:
	UQuestRichTextBlock(const FObjectInitializer& ObjectInitializer);
	
private:


public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuestRichTextBlock")
	int32 QuestID = 0;//任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuestRichTextBlock")
	bool IsCompletedQuest = false;//是否完成
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuestRichTextBlock")
	FString QuestTaskClass = "";//任务目标类型
};