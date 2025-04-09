// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3UserWidget.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ResourceManager.h"
#include "Manager/CustomCursorManager.h"
#include "Manager/EventManager.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/TutorialManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "CS3Base/UIManager.h"
CONTROL_COMPILE_OPTIMIZE_START

FReply UCS3UserWidget::NativeOnMouseButtonDown(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
	//如果是特殊鼠标状态
	if (UGolbalBPFunctionLibrary::CustomCursorManager() && UGolbalBPFunctionLibrary::CustomCursorManager()->IsEspecialCursorState())
	{
		//右键
		if (InMouseEvent.IsMouseButtonDown(EKeys::RightMouseButton))
		{
			//右键恢复鼠标
			UGolbalBPFunctionLibrary::CustomCursorManager()->ResetCursor();
			return FReply::Handled();
		}
		//左键
		else if (InMouseEvent.IsMouseButtonDown(EKeys::LeftMouseButton))
		{
			//鼠标持有状态下
			if (UGolbalBPFunctionLibrary::CustomCursorManager()->CurrentCursorState() == TEXT("LeftMouseCaptureCursor"))
			{
				bool IsHandled = OnClickDrop(UGolbalBPFunctionLibrary::CustomCursorManager()->GetLeftMouseCaptureData());
				if (IsHandled)
				{
					//处理完清空数据恢复鼠标
					UGolbalBPFunctionLibrary::CustomCursorManager()->CancelLeftMouseCaptureCursor();
				}
				//处理完则结束，没处理完说明不能响应
				return FReply::Handled();
			}
			//其他特殊鼠标状态不处理
			else if (UGolbalBPFunctionLibrary::CustomCursorManager()->CurrentCursorState() == TEXT("SplitCursor"))
			{
				if (!CanRespondSplit())
				{
					//不响应
					return FReply::Handled();
				}
			}
			else if (UGolbalBPFunctionLibrary::CustomCursorManager()->CurrentCursorState() == TEXT("RepairCursor"))
			{
				if (!CanRespondRepair())
				{
					//不响应
					return FReply::Handled();
				}
			}
		}
	}
	//一定要在检查指引之前，检查指引会触发下一步
	FReply TempReply = Super::NativeOnMouseButtonDown(InGeometry, InMouseEvent);
	//检查完成指引
	CheckFinishTutorial();
	return  TempReply;
}

FReply UCS3UserWidget::NativeOnMouseButtonDoubleClick(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
	//如果是特殊鼠标状态，无效
	if (UGolbalBPFunctionLibrary::CustomCursorManager() && UGolbalBPFunctionLibrary::CustomCursorManager()->IsEspecialCursorState())
	{
		return FReply::Handled();
	}
	return  Super::NativeOnMouseButtonDoubleClick(InGeometry, InMouseEvent);
}

FReply UCS3UserWidget::NativeOnMouseButtonUp(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
	//如果是特殊鼠标状态，无效
	if (UGolbalBPFunctionLibrary::CustomCursorManager() && UGolbalBPFunctionLibrary::CustomCursorManager()->IsEspecialCursorState())
	{
		return FReply::Handled().ReleaseMouseCapture();
	}
	return  Super::NativeOnMouseButtonUp(InGeometry, InMouseEvent);
}

void UCS3UserWidget::NativeOnMouseEnter(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
	Super::NativeOnMouseEnter(InGeometry, InMouseEvent);
	if (UGolbalBPFunctionLibrary::GEventManager())
	{
		UGolbalBPFunctionLibrary::GEventManager()->OnCancelMouseEvent.AddUObject(this, &UCS3UserWidget::CancelMouseEvent);
	}
}

void UCS3UserWidget::NativeOnMouseLeave(const FPointerEvent& InMouseEvent)
{
	Super::NativeOnMouseLeave(InMouseEvent);
	if (UGolbalBPFunctionLibrary::GEventManager())
	{
		UGolbalBPFunctionLibrary::GEventManager()->OnCancelMouseEvent.Clear();
	}
}

void UCS3UserWidget::NativeOnDragDetected(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent, UDragDropOperation*& OutOperation)
{
	//清除鼠标持有状态
	if (UGolbalBPFunctionLibrary::CustomCursorManager())
	{
		UGolbalBPFunctionLibrary::CustomCursorManager()->CancelLeftMouseCaptureCursor();
	}
	//调用父类走正常拖拽流程
	Super::NativeOnDragDetected(InGeometry, InMouseEvent, OutOperation);
	//设置RootUI为visible，不然RootUI不能触发OnDrop，比如物品不能拖到界面外边丢掉
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->SetRootUIVisible(ESlateVisibility::Visible);
	}
}

bool UCS3UserWidget::NativeOnDrop(const FGeometry& InGeometry, const FDragDropEvent& InDragDropEvent, UDragDropOperation* InOperation)
{
	//拖拽完之后设置visible值，如果还是visible，会挡住其他鼠标点击事件，比如NPC点不中了
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->SetRootUIVisible(ESlateVisibility::SelfHitTestInvisible);
	}
	return Super::NativeOnDrop(InGeometry, InDragDropEvent, InOperation);
}

void UCS3UserWidget::DetectClickDragIfPressed(const FPointerEvent& MouseEvent)
{
	//鼠标点击持有
	if (MouseEvent.IsMouseButtonDown(EKeys::LeftMouseButton) && UGolbalBPFunctionLibrary::CustomCursorManager() && !UGolbalBPFunctionLibrary::CustomCursorManager()->CheckLockCursor())
	{
		UUserWidget* Widget = nullptr;
		FDragDropOperationData Data = FDragDropOperationData();
		OnClickDrag(Widget, Data);
		UGolbalBPFunctionLibrary::CustomCursorManager()->SetLeftMouseCaptureCursor(Widget, Data);
	}
}

UPanelSlot* UCS3UserWidget::AddChild(UUserWidget* ChildWidget)
{
	if (!IsValid(ChildWidget))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3UserWidget::AddChild : ChildWidget!"));
		return nullptr;
	}
	UCanvasPanel* ChildPanel = NativeGetTutorialPanel();
	if (!IsValid(ChildPanel))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3UserWidget::AddChild : ChildPanel!"));
		return nullptr;
	}
	UPanelSlot* PanelSlot = ChildPanel->AddChild(ChildWidget);
	return PanelSlot;
}

void UCS3UserWidget::SetWidgetName(const FString& NewName)
{
	//FName name = this->GetFName();
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("SetWidgetName[%s],[%s]"), *(FNAME_TO_FSTRING(name)), *NewName);
	this->Rename(*NewName, nullptr, REN_ForceNoResetLoaders | REN_DontCreateRedirectors);
}

void UCS3UserWidget::RemoveFromParentAndRenameNone()
{
	RemoveFromParent();
	LowLevelRename(NAME_None);
}

void UCS3UserWidget::CheckFinishTutorial()
{
	if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->TutorialManager)
	{
		UUECS3GameInstance::Instance->TutorialManager->OnTriggerItemClicked();
	}
}

void UCS3UserWidget::BeginDestroy()
{
	if (IsValid(this) && IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->ClearObjectHandles(this);
	}
	Super::BeginDestroy();
}

UCanvasPanel* UCS3UserWidget::NativeGetTutorialPanel()
{
	return GetTutorialPanel();
}

void UCS3UserWidget::CancelMouseEvent()
{
	OnMouseLeave(FPointerEvent());
}

CONTROL_COMPILE_OPTIMIZE_END
