#pragma once

#include "Blueprint/UserWidget.h"
#include "CS3Base/CS3UserWidget.h"
#include "BaseWindow.h"
#include "RootUIWidget.generated.h"

/*
* 文件名称：RootUIWidget.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-01-03
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URootUIWidget : public UCS3UserWidget
{
	GENERATED_BODY()
public:

	URootUIWidget(const FObjectInitializer& ObjectInitializer);

	virtual UCanvasPanel* NativeGetTutorialPanel() override;

	/**
	*界面添加到RootUI上
	*
	*@param Window 界面
	*@param Position 位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "URootUIWidget")
		UCanvasPanelSlot* AddToRootUI(UBaseWindow* Window, FVector2D Position);
	/**
	*刷新同层界面的深度
	*
	*@param PosZSegment 界面的层级
	*
	*@return 无
	*/
	void RefreshChildZOrder(int32 PosZSegment);

	void SetRootUIVisible(ESlateVisibility InVisibility);

public:
	UPROPERTY(meta = (BindWidget))
		UCanvasPanel* RootPanel;
	UPROPERTY(meta = (BindWidget))
		UCanvasPanel* BottomLevel;
	UPROPERTY(meta = (BindWidget))
		UCanvasPanel* CommonLevel;
	UPROPERTY(meta = (BindWidget))
		UCanvasPanel* AlwayTopLevel;
	UPROPERTY(meta = (BindWidget))
		UNamedSlot* Menu;
	UPROPERTY(meta = (BindWidget))
		UCanvasPanel* ChildLevelPanel;
	UPROPERTY(meta = (BindWidget))
		UCanvasPanel* SwitchPanel;
};