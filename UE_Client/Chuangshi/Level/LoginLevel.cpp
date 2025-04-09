// Fill out your copyright notice in the Description page of Project Settings.


#include "LoginLevel.h"
#include "CS3Base/UIManager.h"
#include "Manager/GameStatus.h"
#include "Manager/LevelManager.h"
#include "Manager/MediaPlayerManager.h"
#include "Manager/CustomTimerManager.h"
#include "Engine/Engine.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
void ALoginLevel::BeginPlay()
{
	Super::BeginPlay();
	
	if (IsValid(InputComponent))
	{
		InputComponent->BindKey(EKeys::Escape, EInputEvent::IE_Pressed, this, &ALoginLevel::StopMediaSkip);
	}

	const FVector2D ViewportSize = FVector2D(GEngine->GameViewport->Viewport->GetSizeXY());
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("ALoginLevel::BeginPlay():ViewportSize.X = %f, ViewportSize.Y = %f"), ViewportSize.X, ViewportSize.Y);

	//编辑器模式下，此时ViewportSize不为0，并且在不手动改变分辨率的情况下，不会再发生ViewportResizedEvent事件；
	//独立窗口以及打包版本模式下，此时ViewportSize为0
	//ViewportSize不为0时直接显示登录界面；为0时，监听ViewportResizedEvent事件，等不为0时再打开登录界面
	if (ViewportSize != FVector2D::ZeroVector)
	{
		//显示登录界面
		OpenLoginUI();
	}
	else
	{
		ViewportResizedHandle = GEngine->GameViewport->Viewport->ViewportResizedEvent.AddUObject(this, &ALoginLevel::OnViewportResized);
	}
	
}
bool  ALoginLevel::CheckLoginRun()
{
	return (Super::CheckLoginRun()) ? ((IsValid(UUECS3GameInstance::Instance->GameStatus) && IsValid(GEngine->GameViewport) && GEngine->GameViewport->Viewport != nullptr) ? true : false) : false;
}

void ALoginLevel::StopMediaSkip()
{
	UGolbalBPFunctionLibrary::MediaPlayerManager()->OnShowMediaSkipTime_BP();
}

void ALoginLevel::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
	{
		UBaseWindow* LoginWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("Login"));
		if (LoginWidget)
		{
			LoginWidget->Destroy();
		}
	}
	Super::EndPlay(EndPlayReason);
}

void ALoginLevel::OnLoadLevelFinished()
{
	UUECS3GameInstance::Instance->LevelManager->OnEndTeleportLoginLevel();
}

void ALoginLevel::OnViewportResized(FViewport* InViewPort, uint32 Inval)
{
	const FVector2D ViewportSize = FVector2D(InViewPort->GetSizeXY());
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("ALoginLevel::OnViewportResized():ViewportSize.X = %f, ViewportSize.Y = %f"), ViewportSize.X, ViewportSize.Y);
	if (ViewportSize != FVector2D::ZeroVector)
	{
		//此回调方法中，里面不能去加载一些需要渲染的资源。否则引擎会崩溃（CST-6231）。故延迟打开界面
		FTimerHandle DelayHandle;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, this, &ALoginLevel::OpenLoginUI, 0.1f, false);

		if (ViewportResizedHandle.IsValid())
		{
			GEngine->GameViewport->Viewport->ViewportResizedEvent.Remove(ViewportResizedHandle);
		}
	}
}

void ALoginLevel::OpenLoginUI()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LoginLevel::OpenLoginUI---------------"));
	//显示RootUI，按虚幻4.21来看，是先将默认关卡加载，再去加载HUD的，所以在HUD再创建显示RootUI就晚了，导致登录界面显示不出来
	UGolbalBPFunctionLibrary::GUIManager()->ShowRootUI();
	//创建登录界面，并显示
	UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::Login, TEXT("Login"));
}
CONTROL_COMPILE_OPTIMIZE_END