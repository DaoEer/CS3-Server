#include "ChatChildWindow.h"
#include "../Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

UChatChildWindow::UChatChildWindow(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{

}

UChatChildWindow::~UChatChildWindow()
{

}

FReply UChatChildWindow::NativeOnMouseButtonDown(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
	return OnMouseButtonDown(InGeometry, InMouseEvent).NativeReply;
}

CONTROL_COMPILE_OPTIMIZE_END