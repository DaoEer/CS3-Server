#include "RootUIWidget.h"
#include "WidgetLayoutLibrary.h"
#include "CanvasPanelSlot.h"
#include "Util/GolbalBPFunctionLibrary.h"

URootUIWidget::URootUIWidget(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	
}

UCanvasPanel* URootUIWidget::NativeGetTutorialPanel()
{
	return ChildLevelPanel;
}

UCanvasPanelSlot* URootUIWidget::AddToRootUI(UBaseWindow* Window, FVector2D Position)
{
	if (Window)
	{
		UCanvasPanelSlot* CanvasPanelSlot = nullptr;
		switch (Window->PosZSegment)
		{
		case 0:
		{
			CanvasPanelSlot = Cast<UCanvasPanelSlot>(BottomLevel->AddChild(Window));
			break;
		}
		case 1:
		{
			CanvasPanelSlot = Cast<UCanvasPanelSlot>(CommonLevel->AddChild(Window));
			break;
		}
		case 2:
		{
			CanvasPanelSlot = Cast<UCanvasPanelSlot>(AlwayTopLevel->AddChild(Window));
			break;
		}
		case 3:
		{
			CanvasPanelSlot = Cast<UCanvasPanelSlot>(SwitchPanel->AddChild(Window));
			break;
		}
		default:
			break;
		}
		if (CanvasPanelSlot)
		{
			CanvasPanelSlot->SetPosition(Position);
			return CanvasPanelSlot;
		}
	}
	return nullptr;
}

void URootUIWidget::RefreshChildZOrder(int32 PosZSegment)
{
	UCanvasPanel* LocalPanel = nullptr;
	switch (PosZSegment)
	{
	case 0:
	{
		LocalPanel = BottomLevel;
		break;
	}
	case 1:
	{
		LocalPanel = CommonLevel;
		break;
	}
	case 2:
	{
		LocalPanel = AlwayTopLevel;
		break;
	}
	default:
		break;
	}
	if (LocalPanel)
	{
		int32 Num = LocalPanel->GetChildrenCount();
		if (Num > 0)
		{
			for (int32 index = 0; index <= Num - 1; index++)
			{
				UCanvasPanelSlot* CanvasPanelSlot = Cast<UCanvasPanelSlot>(UWidgetLayoutLibrary::SlotAsCanvasSlot(LocalPanel->GetChildAt(index)));
				UBaseWindow* LocalWindow = Cast<UBaseWindow>(LocalPanel->GetChildAt(index));
				if (CanvasPanelSlot && LocalWindow)
				{
					CanvasPanelSlot->SetZOrder(LocalWindow->PosZ);
				}
			}
		}
	}
}

void URootUIWidget::SetRootUIVisible(ESlateVisibility InVisibility)
{
	if (RootPanel)
	{
		RootPanel->SetVisibility(InVisibility);
	}
}