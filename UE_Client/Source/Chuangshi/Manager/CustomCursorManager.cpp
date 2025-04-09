// Fill out your copyright notice in the Description page of Project Settings.

#include "CustomCursorManager.h"
#include"Chuangshi.h"
#include "GameDevelop/CS3GameInstance.h"
#include "EventManager.h"
#include "CS3Base/UIManager.h"

CONTROL_COMPILE_OPTIMIZE_START
UCustomCursorManager::UCustomCursorManager()
{
	CurCursorState = "";
	CursorUI = nullptr;
}

UCustomCursorManager::~UCustomCursorManager()
{

}

UCustomCursorManager* UCustomCursorManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UCustomCursorManager>();
}

void UCustomCursorManager::ClearInstanceData()
{
	locked = false;///<是否锁定
	CurCursorState = "NormalCursor";///<鼠标类型
	CursorUI = nullptr;
}

void UCustomCursorManager::Init()
{
	InitLeftMouseCaptureData();
}

void UCustomCursorManager::SetCursor(FString cursorState)
{
	if (!IsValid(CursorUI))
	{
		CS3_Warning(TEXT("-->Null Pointer error: UCustomCursorManager::SetCursor: CursorUI !"));
		return;
	}

	if (locked)
		return;
	if (CurCursorState == cursorState)
		return;

	CursorUI->SetCursorTexture(cursorState);

	CurCursorState = cursorState;
}

void UCustomCursorManager::SetCursorUI(UCursorUIWidget* NewCursorUI)
{
	if (!IsValid(this->CursorUI))
	{
		this->CursorUI = NewCursorUI;
		SetCursor("NormalCursor");
	}
}

void UCustomCursorManager::DefaultCursor()
{
	if (locked)
		return;
	SetCursor("NormalCursor");
}

void UCustomCursorManager::LockCursor(FString cursorState)
{
	if (locked)
		return;
	SetCursor(cursorState);
	locked = true;
}

void UCustomCursorManager::UnLockCursor(FString cursorState, FString newCursorState)
{
	if (locked && CurCursorState != cursorState)
		return;
	locked = false;
	SetCursor(newCursorState);
}

bool UCustomCursorManager::CheckLockCursor()
{
	return locked;
}

bool UCustomCursorManager::IsEspecialCursorState()
{
	if (CurrentCursorState() == TEXT("SplitCursor")
		|| CurrentCursorState() == TEXT("RepairCursor")
		|| CurrentCursorState() == TEXT("LeftMouseCaptureCursor"))
	{
		return true;
	}
	return false;
}

void UCustomCursorManager::ResetCursor()
{
	if (IsEspecialCursorState() && UGolbalBPFunctionLibrary::GEventManager())
	{
		if (CurrentCursorState() == TEXT("LeftMouseCaptureCursor"))
		{
			ClearLeftMouseCaptureData();
			FSlateApplication::Get().SetAllowTooltips(true);
		}
		SetCursor("NormalCursor");
	}
}

void UCustomCursorManager::OnHideMouse()
{
	//恢复鼠标
	ResetCursor();
}

#pragma region	/** 持有道具鼠标状态相关 */
void UCustomCursorManager::SetLeftMouseCaptureCursor(UUserWidget* Widget, FDragDropOperationData Data)
{
	if (IsValid(Widget))
	{
		Widget->AddToViewport(5);
		
	}
	SaveLeftMouseCaptureData(Widget, Data);
	SetCursor("LeftMouseCaptureCursor");
	//鼠标左键持有状态，移动到可显示tips目标上时，不显示目标的tips
	FSlateApplication::Get().SetAllowTooltips(false);
}

void UCustomCursorManager::CancelLeftMouseCaptureCursor()
{
	ResetCursor();
}

void UCustomCursorManager::InitLeftMouseCaptureData()
{
	if (IsValid(DraggedWidget))
	{
		DraggedWidget->RemoveFromParent();
		DraggedWidget = nullptr;
	}
	//RootUI可见性
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->SetRootUIVisible(ESlateVisibility::SelfHitTestInvisible);
	}
}

void UCustomCursorManager::SaveLeftMouseCaptureData(UUserWidget* Widget, FDragDropOperationData Data)
{
	if (IsValid(DraggedWidget))
	{
		DraggedWidget->RemoveFromParent();
	}
	DraggedWidget = Widget;
	DraggedData = Data;
	//RootUI可见性
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->SetRootUIVisible(ESlateVisibility::Visible);
	}
}

void UCustomCursorManager::ClearLeftMouseCaptureData()
{
	InitLeftMouseCaptureData();
}

FDragDropOperationData UCustomCursorManager::GetLeftMouseCaptureData()
{
	return DraggedData;
}

#pragma endregion

CONTROL_COMPILE_OPTIMIZE_END