
#include "UIFixerManager.h"
#include "GameData/UIDataDefine.h"
#include "UIManager.h"
#include "Runtime/Engine/Classes/Engine/UserInterfaceSettings.h"
#include"Chuangshi.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "BaseWindow.h"

CONTROL_COMPILE_OPTIMIZE_START

UUIFixerManager::UUIFixerManager()
{
	
}

UUIFixerManager::~UUIFixerManager()
{

}

UUIFixerManager* UUIFixerManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UUIFixerManager>();
}

void UUIFixerManager::OnWindowInit(UBaseWindow* window)
{
	FirstInitFix(window);
}

void UUIFixerManager::OnRecovery(UBaseWindow* window)
{
	FirstInitFix(window);
}

void UUIFixerManager::UpdateDockStyle(UBaseWindow* window)
{
	FirstInitFix(window);
}

void UUIFixerManager::OnRoleEnterWorld()
{
	//遍历所有窗口
	for (auto win : UGolbalBPFunctionLibrary::GUIManager()->GetWindows())
	{
		if (win->WindowType != TEXT("ChatChild"))
		{
			//初始化界面位置
			FirstInitFix(win);
		}
	}
}

void UUIFixerManager::FirstInitFix(UBaseWindow * window)
{
	if (!IsValid(window))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUIFixerManager::FirstInitFix : window!"));
		return;
	}
	const FVector2D ViewportSize = UGolbalBPFunctionLibrary::GetViewportSize();
	const float ViewportScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(ViewportSize.X, ViewportSize.Y));
	FVector2D NewPos = window->Pos;
	//水平方向
	if (window->H_DockStyle == EUIHDOCKSTYLE::LEFT)
	{
		NewPos.X = window->Left;
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::CENTER)
	{
		NewPos.X = ViewportSize.X / ViewportScale * 0.5 - window->Size.X * 0.5 + window->Center;
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::RIGHT)
	{
		NewPos.X = ViewportSize.X / ViewportScale - window->Size.X - window->Right;
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::S_LEFT)
	{
		NewPos.X = ViewportSize.X / ViewportScale * window->R_Left;
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::S_CENTER)
	{
		NewPos.X = ViewportSize.X / ViewportScale * window->R_Center - window->Size.X * 0.5;
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::S_RIGHT)
	{
		NewPos.X = ViewportSize.X / ViewportScale * window->R_Right - window->Size.X;
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::HFILL)
	{
		window->Size.X = ViewportSize.X / ViewportScale;
		NewPos.X = 0;
	}
	//垂直方向
	if (window->V_DockStyle == EUIVDOCKSTYLE::TOP)
	{
		NewPos.Y = window->Top;
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::MIDDLE)
	{
		NewPos.Y = ViewportSize.Y / ViewportScale * 0.5 - window->Size.Y * 0.5 + window->Middle;
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::BOTTOM)
	{
		NewPos.Y = ViewportSize.Y / ViewportScale - window->Size.Y - window->Bottom;
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::S_TOP)
	{
		NewPos.Y = ViewportSize.Y / ViewportScale * window->R_Top;
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::S_MIDDLE)
	{
		NewPos.Y = ViewportSize.Y / ViewportScale * window->R_Middle - window->Size.Y * 0.5;
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::S_BOTTOM)
	{
		NewPos.Y = ViewportSize.Y / ViewportScale * window->R_Bottom - window->Size.Y;
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::VFILL)
	{
		window->Size.Y = ViewportSize.Y / ViewportScale;
		NewPos.Y = 0;
	}
	window->SetPosition(NewPos);
	window->SetSize(window->Size);
}

void UUIFixerManager::AdaptDock(FVector2D preReso, float PreScale, FVector2D NewReso, UBaseWindow * window)
{
	if (!IsValid(window))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUIFixerManager::AdaptDock : window!"));
		return;
	}
	if (!IsValid(GEngine->GameViewport) || GEngine->GameViewport->Viewport == nullptr)
	{
		return;
	}
	const FVector2D ViewportSize = NewReso;
	const float NewScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(ViewportSize.X, ViewportSize.Y));
	float oldWidth = preReso.X;
	float newWidth = ViewportSize.X;
	float oldHeight = preReso.Y;
	float newHeight = ViewportSize.Y;
	float hscale = newWidth / oldWidth;
	float vscale = newHeight / oldHeight;
	FVector2D OldPos = window->Pos;
	FVector2D NewPos = OldPos;
	
	//水平方向
	if (window->H_DockStyle == EUIHDOCKSTYLE::LEFT)
	{
		
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::CENTER)
	{
		float dx = oldWidth / 2 - (OldPos.X + window->Size.X / 2) * PreScale;	//旧分辨率状态下界面中心点离屏幕中间的距离
		NewPos.X = (newWidth / 2  - dx * hscale - window->Size.X / 2 * NewScale) / NewScale;
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::RIGHT)
	{
		float dx = oldWidth - (OldPos.X + window->Size.X) * PreScale;			//旧分辨率状态下界面右边离屏幕右边的距离
		NewPos.X = (newWidth - dx * hscale - window->Size.X * NewScale) / NewScale;
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::S_LEFT)
	{
		
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::S_CENTER)
	{
		float dx = oldWidth / 2 - (OldPos.X + window->Size.X / 2) * PreScale;	//旧分辨率状态下界面中心点离屏幕中间的距离
		float percent = dx / oldWidth;											//旧分辨率状态下界面中心点离屏幕中间的距离的占屏幕百分比
		NewPos.X = (newWidth / 2 - newWidth * percent - window->Size.X / 2 * NewScale) / NewScale;
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::S_RIGHT)
	{
		float dx = oldWidth - (OldPos.X + window->Size.X) * PreScale;			//旧分辨率状态下界面右边离屏幕右边的距离
		float percent = dx / oldWidth;											//旧分辨率状态下界面右边离屏幕右边的距离的占屏幕百分比
		NewPos.X = (newWidth - newWidth * percent - window->Size.X * NewScale) / NewScale;
	}
	else if (window->H_DockStyle == EUIHDOCKSTYLE::HFILL)
	{
		window->Size.X = ViewportSize.X / NewScale;
		NewPos.X = 0;
	}
	//垂直方向
	if (window->V_DockStyle == EUIVDOCKSTYLE::TOP)
	{
		
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::MIDDLE)
	{
		float dy = oldHeight / 2 - (OldPos.Y + window->Size.Y / 2) * PreScale;	//旧分辨率状态下界面中心点离屏幕中间的距离
		NewPos.Y = (newHeight / 2 - dy * vscale - window->Size.Y / 2 * NewScale) / NewScale;
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::BOTTOM)
	{
		float dy = oldHeight - (OldPos.Y + window->Size.Y) * PreScale;			//旧分辨率状态下界面下边离屏幕下边的距离
		NewPos.Y = (newHeight - dy * vscale - window->Size.Y * NewScale) / NewScale;
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::S_TOP)
	{
		
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::S_MIDDLE)
	{
		float dy = oldHeight / 2 - (OldPos.Y + window->Size.Y / 2) * PreScale;	//旧分辨率状态下界面中心点离屏幕中间的距离
		float percent = dy / oldHeight;											//旧分辨率状态下界面中心点离屏幕中间的距离的占屏幕百分比
		NewPos.Y = (newHeight / 2 - newHeight * percent - window->Size.Y / 2 * NewScale) / NewScale;
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::S_BOTTOM)
	{
		float dy = oldHeight - (OldPos.Y + window->Size.Y) * PreScale;			//旧分辨率状态下界面下边离屏幕下边的距离
		float percent = dy / oldHeight;											//旧分辨率状态下界面下边离屏幕下边的距离的占屏幕百分比
		NewPos.Y = (newHeight - newHeight * percent - window->Size.Y * NewScale) / NewScale;
	}
	else if (window->V_DockStyle == EUIVDOCKSTYLE::VFILL)
	{
		window->Size.Y = ViewportSize.Y / NewScale;
		NewPos.Y = 0;
	}
	window->SetPosition(NewPos);
	window->SetSize(window->Size);
}

void UUIFixerManager::OnResolutionChanged(FVector2D preReso, float PreScale, FVector2D newReso)
{
	TArray<UBaseWindow*> windows = UUECS3GameInstance::Instance->GUIManager->GetWindows();
	for (auto window : windows)						//遍历所有窗口
	{
		if (window->WindowType != TEXT("ChatChild"))
		{
			AdaptDock(preReso, PreScale, newReso, window);
		}		
	}
}

CONTROL_COMPILE_OPTIMIZE_END