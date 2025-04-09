#pragma once
#include "CS3Base/BaseWindow.h"
#include "ChatChildWindow.generated.h"

/*
* 文件名称：ChatChildWindow.h
* 功能说明：聊天子窗口
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-03-28
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UChatChildWindow : public UBaseWindow
{
	GENERATED_BODY()
public:
	UChatChildWindow(const FObjectInitializer& ObjectInitializer);
	~UChatChildWindow();
public:
	virtual FReply NativeOnMouseButtonDown(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent) override;
};