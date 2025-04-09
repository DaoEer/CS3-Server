
#include "UIDockManager.h"
#include "UIManager.h"
#include "UIFixerManager.h"
#include "GameData/UIDataDefine.h"
#include "Runtime/Engine/Classes/Engine/UserInterfaceSettings.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Chuangshi.h"
#include "CS3Base/BaseWindow.h"


UUIDockManager::UUIDockManager()
{
	StartPos.X = 20;
	StartPos.Y = 80;
	Initialize();
}

UUIDockManager::~UUIDockManager()
{

}

UUIDockManager* UUIDockManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UUIDockManager>();
}

void UUIDockManager::OnWindowCreatedOver(FString WindowType)
{
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		if (SortWindowsType.Contains(WindowType))
		{
			UBaseWindow* window = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(WindowType);
			if (window)
			{
				window->OnBeforeShowDelegate.AddUObject(this, &UUIDockManager::SortWindowsByShow);
				window->OnAfterClosedDelegate.AddUObject(this, &UUIDockManager::SortWindowsByHide);
			}
		}
		if (RecoveryWindowsType.Contains(WindowType))
		{
			UBaseWindow* window = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(WindowType);
			if (window)
			{
				window->OnBeforeShowDelegate.AddUObject(this, &UUIDockManager::RecoveryWindow);
			}
		}
	}
}

void UUIDockManager::RecoveryWindow(UBaseWindow * window)
{
	UGolbalBPFunctionLibrary::UIFixerManager()->OnRecovery(window);
}

void UUIDockManager::SortWindowsByShow(UBaseWindow * window)
{
	if (!IsValid(GEngine->GameViewport) || GEngine->GameViewport->Viewport == nullptr)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("----------------UUIDockManager::OnWindowShow:the CS3 game quit."))
		return;
	}
	int num = ShowedWindows.Num();
	if (num > 0)
	{
		window->Left = ShowedWindows[num - 1]->Right;
	}
	if (ShowedWindows.Find(window) < 0)
	{
		ShowedWindows.Add(window);
	}
	Layout();
}

void UUIDockManager::SortWindowsByHide(UBaseWindow * window)
{
	if (!SortWindowsType.Contains(window->WindowType))
	{
		return;
	}
	if (ShowedWindows.Find(window) >= 0)
	{
		ShowedWindows.Remove(window);
	}
	Layout();
}

void UUIDockManager::Initialize()
{
	///<还原初始位置界面
	RecoveryWindowsType.Empty();
	RecoveryWindowsType.AddUnique(TEXT("KitBag"));
	RecoveryWindowsType.AddUnique(TEXT("RankList"));
	RecoveryWindowsType.AddUnique(TEXT("SystemMenu"));
	RecoveryWindowsType.AddUnique(TEXT("GameSetting"));
	RecoveryWindowsType.AddUnique(TEXT("CustomGameSetting"));
	RecoveryWindowsType.AddUnique(TEXT("Equip"));
	RecoveryWindowsType.AddUnique(TEXT("ActivityCalendar"));
	RecoveryWindowsType.AddUnique(TEXT("OnlineGift"));
	RecoveryWindowsType.AddUnique(TEXT("SigninGift"));
	RecoveryWindowsType.AddUnique(TEXT("Camp"));
	RecoveryWindowsType.AddUnique(TEXT("ChangeAppearance"));
	RecoveryWindowsType.AddUnique(TEXT("ChangeAppearWearLen"));

	///<排序停靠界面
	SortWindowsType.Empty();
	SortWindowsType.AddUnique(TEXT("CommonDialog"));
	SortWindowsType.AddUnique(TEXT("TaskDialog"));
	SortWindowsType.AddUnique(TEXT("TaskList"));
	SortWindowsType.AddUnique(TEXT("SkillLearned"));
	SortWindowsType.AddUnique(TEXT("SkillUpgraded"));
	SortWindowsType.AddUnique(TEXT("NPCShop"));
	SortWindowsType.AddUnique(TEXT("RoleProperty"));
	SortWindowsType.AddUnique(TEXT("OtherRoleProperty"));
	SortWindowsType.AddUnique(TEXT("Mail"));
}

void UUIDockManager::Layout()
{
	float left = StartPos.X;
	float top = StartPos.Y;
	for (int idx = 0; idx <= ShowedWindows.Num() - 1; idx++)
	{
		if (idx > 0)
		{
			left = ShowedWindows[idx - 1]->Right;
		}
		ShowedWindows[idx]->H_DockStyle = EUIHDOCKSTYLE::LEFT;
		ShowedWindows[idx]->V_DockStyle = EUIVDOCKSTYLE::TOP;
		ShowedWindows[idx]->Right = left + ShowedWindows[idx]->Size.X;
		ShowedWindows[idx]->Pos.X = left;
		ShowedWindows[idx]->Pos.Y = top;
		ShowedWindows[idx]->SetPosition(ShowedWindows[idx]->Pos);
		ShowedWindows[idx]->SetSize(ShowedWindows[idx]->Size);
	}
}