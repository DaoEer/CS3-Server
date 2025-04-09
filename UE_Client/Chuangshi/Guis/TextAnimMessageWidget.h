#pragma once

#include "Blueprint/UserWidget.h"
#include "Image.h"
#include "CS3Base/CS3UserWidget.h"
#include "GameData/MessageData.h"
#include "CS3Base/BaseWindow.h"
#include "TextAnimMessageWidget.generated.h"



/*
* 文件名称：TextAnimMessageWidget.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2020-03-24
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UTextAnimMessageWidget : public UBaseWindow
{
	GENERATED_BODY()
public:

	UTextAnimMessageWidget(const FObjectInitializer& ObjectInitializer);
	//设置信息
	void SetInfo(FTextAnimationMessage TextData);
	//动画
	void PlayAnimation();
	//重置
	void ResetAnimation();

public:
	UPROPERTY(meta = (BindWidget))
		UImage* TextAnimImage;

public:
	float PlayTime;
	float AnimPhase;
	FTimerHandle AnimEventHandle;
};