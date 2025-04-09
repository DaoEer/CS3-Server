// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Blueprint/UserWidget.h"
#include "Components/CanvasPanel.h"
#include "Components/PanelSlot.h"
#include "GameData/CursorData.h"
#include "CS3UserWidget.generated.h"

/*
* 文件名称：CS3UserWidget.h
* 功能说明：
* 文件作者：huting
* 目前维护：zhangdan
* 创建时间：2017-11-16
*/

/**
 * 
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UCS3UserWidget : public UUserWidget
{
	GENERATED_BODY()
public:

	virtual FReply NativeOnMouseButtonDown(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent) override;
	virtual FReply NativeOnMouseButtonDoubleClick(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent) override;
	virtual FReply NativeOnMouseButtonUp(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent) override;
	virtual void NativeOnMouseEnter(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent) override;
	virtual void NativeOnMouseLeave(const FPointerEvent& InMouseEvent) override;
	virtual void NativeOnDragDetected(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent, UDragDropOperation*& OutOperation) override;
	virtual bool NativeOnDrop(const FGeometry& InGeometry, const FDragDropEvent& InDragDropEvent, UDragDropOperation* InOperation) override;

	virtual void BeginDestroy() override;
	virtual UCanvasPanel* NativeGetTutorialPanel();

	//鼠标点击持有
	UFUNCTION(BlueprintCallable, Category = "Click Drag and Drop")
		void DetectClickDragIfPressed(const FPointerEvent& MouseEvent);
	/**
	*鼠标点击持有的表现
	*
	*@param Widget 跟随鼠标显示的控件
	*@param MouseCaptureData 鼠标持有数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, BlueprintCosmetic, Category = "Click Drag and Drop")
		void OnClickDrag(UUserWidget*& Widget, FDragDropOperationData& MouseCaptureData);
	/**
	*鼠标持有状态下放下鼠标
	*
	*@param MouseCaptureData 鼠标持有数据
	*
	*@return 鼠标事件是否吞噬，为true表示吞噬，即鼠标事件结束，默认为false
	*/
	UFUNCTION(BlueprintImplementableEvent, BlueprintCosmetic, Category = "Click Drag and Drop")
		bool OnClickDrop(const FDragDropOperationData& MouseCaptureData);
	/**
	*在控件蓝图上添加一个子控件蓝图
	*
	*@param ChildWidget 子控件蓝图
	*
	*@return 子控件的面板槽
	*/
	UPanelSlot* AddChild(UUserWidget* ChildWidget);

	/**
	*修改动态创建的蓝图控件名字，便于查找获得控件实例
	*
	*@param NewName 新名字
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3UserWidget")
		void SetWidgetName(const FString& NewName);
	/*
	* remove控件，并且设置Name为None
	* 动态创建并且调用SetWidgetName方法设置了Name的控件，remove时必须调用这个remove方法，不能用RemoveFromParent
	* 因为RemoveFromParent后，并没有马上回收，Name值还被占用着，导致设置同Name值会崩溃
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3UserWidget")
		void RemoveFromParentAndRenameNone();

	/**
	*是否能响应拆分鼠标
	*
	*@return 是否能响应修理鼠标
	*/
	UFUNCTION(BlueprintImplementableEvent, BlueprintCosmetic, Category = "Mouse")
		bool CanRespondSplit();

	/**
	*是否能响应修理鼠标
	*
	*@return 是否能响应修理鼠标
	*/
	UFUNCTION(BlueprintImplementableEvent, BlueprintCosmetic, Category = "Mouse")
		bool CanRespondRepair();

	/**
	*获取新手指引面板，用于在界面上弹出指引UI
	*
	*@return 新手指引面板
	*/
	UFUNCTION(BlueprintImplementableEvent, BlueprintCosmetic, Category = "Tutorial")
		UCanvasPanel* GetTutorialPanel();

	/**
	*检查完成指引，被点击时调用
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3UserWidget")
		void CheckFinishTutorial();
	
private:
	/**
	*取消鼠标操作
	*
	*@return 无
	*/
	void CancelMouseEvent();
};
