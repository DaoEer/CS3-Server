

#include "HyperlinkManager.h"
#include "Regex.h"
#include "Kismet/KismetStringLibrary.h"
#include "Guis/QuestRichTextBlock.h"
#include "Actor/Player/PlayerCharacter.h"
#include "WidgetBlueprintLibrary.h"
#include "CS3Base/UIManager.h"
#include "CS3Base/RootUIWidget.h" 
#include "GameDevelop/CS3PlayerController.h"
#include"Chuangshi.h"
#include "Operation/ControllerModeMgr.h"
#include "Interface/Role/RoleTeamInterface.h"

CONTROL_COMPILE_OPTIMIZE_START
/*
* 文件名称：HyperlinkManager.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-09-01
*/


UHyperlinkManager::UHyperlinkManager()
{
	init();
}

UHyperlinkManager::~UHyperlinkManager()
{

}

UHyperlinkManager* UHyperlinkManager::GetInstance()
{
	cs3_checkNoReentry();
	return (UHyperlinkManager*)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_HyperlinkManager")));

//	return NewObject<UHyperlinkManager>();
}

void UHyperlinkManager::init()
{
	HyperLinks = { "goto:", "chat_item:", "chat_role:", "chat_quest:", "joinTeam:", "openUI:" };
}

void UHyperlinkManager::OnHyperlinkClicked(UCS3RichTextBlock* RichText, FString LinkMark)
{
	//清除当前的focus
	//FSlateApplication::Get().ClearKeyboardFocus(EFocusCause::Mouse);

	//设置输入模式
	//if (UGolbalBPFunctionLibrary::GetCS3PlayerController() && UGolbalBPFunctionLibrary::GUIManager())
	//{
	//	UWidgetBlueprintLibrary::SetInputMode_GameAndUIEx(UGolbalBPFunctionLibrary::GetCS3PlayerController()
    // 			, UGolbalBPFunctionLibrary::GUIManager()->RootUIWidget, EMouseLockMode::DoNotLock, true);
	//}
	ACS3PlayerController* CS3PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (CS3PlayerController->bIsCtrlDown)
	{
		//按下ctrl键则复制超链接到聊天栏
		CopyHyperLinkProcess(RichText, LinkMark);
	}
	else
	{
		//解析超链接href
		ParseProcess(RichText, LinkMark);
	}

}

FString UHyperlinkManager::ConvertRichTextToCommonText(FString InRichText)
{
	FString NewStr = InRichText;
	//去掉超链接
	if (NewStr.Contains(TEXT("@L")))//有超链接
	{
		bool IsChatItem = InRichText.Contains(TEXT("chat_item"));
		if (IsChatItem)//聊天里面的道具超链接特殊，里面有json格式，不好用{}匹配，使用[]找出来替换完再走一般流程
		{
			//获得道具[@L{t='道具';m=chat_item:{/ROOT/:{...};cfc=(230,227,185,255)}]x1
			NewStr = ConvertHyperLinkRichTextToCommonText(NewStr, TEXT("(?=\\[).+?(?=\\])"));
			if (NewStr.Contains(TEXT("@L")))
			{
				//还有其他的超链接
				//比如：大家快去@L{t='NPC名字';m=goto:20151025;cfc=(230, 227, 185, 255)}处领取[@L{t='道具';m=xxxxxxx;cfc=(230,227,185,255)}]
				NewStr = ConvertHyperLinkRichTextToCommonText(NewStr, TEXT("(@L)\\{[^\\}]*\\}"));
			}
		}
		else
		{
			//大家快去@L{t='NPC名字';m=goto:20151025;cfc=(230, 227, 185, 255)}处
			NewStr = ConvertHyperLinkRichTextToCommonText(NewStr, TEXT("(@L)\\{[^\\}]*\\}"));
		}
	}
	FString ReturnStr = NewStr;
	//去掉其他格式字符
	//正则表达式：(@F|@B|@S)\{[^\}]*\}|@B|@S|@D
	FRegexPattern StrPattern(TEXT("(@F|@B|@S)\\{[^\\}]*\\}|@B|@S|@D"));
	FRegexMatcher StrMatcher(StrPattern, NewStr);
	while (StrMatcher.FindNext())
	{
		int32 MatchStart = StrMatcher.GetMatchBeginning();
		int32 MatchEnd = StrMatcher.GetMatchEnding();
		FString MatchStr = NewStr.Mid(MatchStart, MatchEnd - MatchStart);
		ReturnStr = ReturnStr.Replace(*MatchStr, TEXT(""));
	}
	return ReturnStr;
}

FString UHyperlinkManager::ConvertHyperLinkRichTextToCommonText(FString InRichText, FString Regex)
{
	FString ReturnStr = InRichText;

	FRegexPattern StrPattern(Regex);
	FRegexMatcher StrMatcher(StrPattern, InRichText);
	while (StrMatcher.FindNext())
	{
		int32 MatchStart = StrMatcher.GetMatchBeginning();
		int32 MatchEnd = StrMatcher.GetMatchEnding();
		FString MatchStr = InRichText.Mid(MatchStart, MatchEnd - MatchStart);//@L{t='道具';m=xxxxxxx;cfc=(230,227,185,255)}

		if (MatchStr.Contains(TEXT("@L")))
		{
			TArray<FString> SplitArray1 = UGolbalBPFunctionLibrary::SplitString(MatchStr, false, "@L{t='");
			if (SplitArray1.Num() > 1)
			{
				TArray<FString> SplitArray2 = UGolbalBPFunctionLibrary::SplitString(SplitArray1[1], false, "';");
				if (SplitArray2.Num() > 0)
				{
					FString ReplaceStr = SplitArray2[0];
					if (Regex == TEXT("(?=\\[).+?(?=\\])"))
					{
						ReplaceStr = TEXT("[") + ReplaceStr;
					}
					ReturnStr = ReturnStr.Replace(*MatchStr, *ReplaceStr);
				}
			}
		}
	}
	return ReturnStr;
}

void UHyperlinkManager::ParseProcess(UCS3RichTextBlock* RichText, FString LinkMark)
{
	FString Prefix = "";
	for (auto Pref : HyperLinks)
	{
		if (LinkMark.StartsWith(Pref))
		{
			Prefix = Pref;
			break;
		}
	}
	if (Prefix == "")
	{
		return;
	} 
	FString Mark = UKismetStringLibrary::GetSubstring(LinkMark, Prefix.Len(), LinkMark.Len() - 1);
	if (Prefix ==  "goto:")
	{
		HLGoto(RichText, Mark);
	}
	else if (Prefix == "joinTeam:")
	{
		JoinTeam(RichText, Mark);
	}
	else if (Prefix == "openUI:")
	{
		OpenUI(RichText, Mark);
	}
	else
	{
		FString MarkPrefix = Prefix.Replace(TEXT(":"), TEXT(""), ESearchCase::IgnoreCase);
		HLChatRichText(RichText, MarkPrefix, Mark);
	}
}

void UHyperlinkManager::HLGoto(UCS3RichTextBlock* RichText, FString LinkMark)
{
	RunToNpc(RichText, LinkMark);
}

void UHyperlinkManager::RunToNpc(UCS3RichTextBlock* RichText, FString LinkMark)
{
	UQuestRichTextBlock* Rich = Cast<UQuestRichTextBlock>(RichText);
	int32 AutoQuestID = 0;
	bool IsCompleted = false;
	FString TaskClass = TEXT("");
	if (IsValid(Rich))
	{
		AutoQuestID = Rich->QuestID;
		IsCompleted = Rich->IsCompletedQuest;
		TaskClass = Rich->QuestTaskClass;
	}
	FVector DstPos = FVector::ZeroVector;
	FString NpcID = "";
	FString	DstSpace = "";
	int32 GossipWithType = 0;
	//LinkMark = TEXT("(51341.816406 7969.181641 17175.724609)#fengming");
	//正则表达式：(?!\().+?(?=\))
	//https://regex101.com/r/WLyZn6/1
	FRegexPattern FileAndLinePattern(TEXT("(?!\\().+?(?=\\))"));
	FRegexMatcher FileAndLineRegexMatcher(FileAndLinePattern, LinkMark);
	FString sreDstPos = "";
	if (FileAndLineRegexMatcher.FindNext())
	{
		sreDstPos = FileAndLineRegexMatcher.GetCaptureGroup(0);
	}

	if (sreDstPos != "")  //若提供的标签是坐标和目标地图
	{
		if (LinkMark.Contains("#"))  //是否提供所在地图，如果没有，则不允许自动寻路
		{
			//获取目的地的坐标
			TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(sreDstPos, false, " ");
			if (SplitArray.Num() == 3)
			{
				DstPos.X = FSTRING_TO_FLOAT(SplitArray[0]);
				DstPos.Y = FSTRING_TO_FLOAT(SplitArray[1]);
				DstPos.Z = FSTRING_TO_FLOAT(SplitArray[2]);
			}

			TArray<FString> SplitMark = UGolbalBPFunctionLibrary::SplitString(LinkMark, false, "#");
			
			int32 Num = SplitMark.Num();
			if (Num > 0)
			{
				DstSpace = SplitMark[Num - 1];
			}
				

			//暂时不处理
			//LinkMark = TEXT("(51341.816406 7969.181641 17175.724609)#1#fengming");//有分线
			/*
			if (SplitMark.Num() == 3)  
			{
				FString DstLineNumberDstLineNumber = SplitMark[1];
			}
			*/
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("----------------LinkMark=(%f,%f,%f)#%s"), DstPos.X, DstPos.Y, DstPos.Z, *DstSpace);
		}
	}
	else  //按照NPC ID来进行寻路
	{
		if (LinkMark.Contains("#"))
		{
			TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(LinkMark, false, "#");
			if (SplitArray.Num() > 1)
			{
				NpcID = SplitArray[0];
				DstSpace = SplitArray[1];
			}
			if (SplitArray.Num() > 2)
			{
				GossipWithType = FSTRING_TO_INT(SplitArray[2]);				
			}
		}
		else
		{
			NpcID = LinkMark;
		}
	}
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(ServerCharacter);
	if (IsValid(PlayerCharacter))
	{
		float NearbyRange = 2.0f;
		if (PlayerCharacter->IsCarrierState())
		{
			NearbyRange = 4.0f;		
		}
		UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

		if (IsValid(ControllerModeMgr))
		{
			TArray<FString> OtherValue;
			FString DstPositionString = FLOAT_TO_FSTRING(DstPos.X) + TEXT("|") + FLOAT_TO_FSTRING(DstPos.Y) + TEXT("|") + FLOAT_TO_FSTRING(DstPos.Z);
			OtherValue.Add(DstSpace);
			OtherValue.Add(INT_TO_FSTRING(IsCompleted));
			OtherValue.Add(TaskClass);
			OtherValue.Add(NpcID);
			OtherValue.Add(DstPositionString);
			OtherValue.Add(FLOAT_TO_FSTRING(NearbyRange));
			OtherValue.Add(INT_TO_FSTRING(AutoQuestID));
			OtherValue.Add(INT_TO_FSTRING(int(ENUM_NAVIGATE_ACTION_TYPE::NavigateActionDefault)));
			OtherValue.Add(INT_TO_FSTRING(GossipWithType));
			ControllerModeMgr->ExecuteInputInfor(TEXT("StartCrossMapNavigate"), TEXT(""), 0.0f, OtherValue);
		}
		else
		{
			PlayerCharacter->StartCrossMapNavigate(DstSpace, IsCompleted, TaskClass, NpcID, DstPos, NearbyRange, AutoQuestID, ENUM_NAVIGATE_ACTION_TYPE::NavigateActionDefault, GossipWithType);
		}
	}
}

void UHyperlinkManager::HLChatRichText(UCS3RichTextBlock* RichText, FString MarkPrefix, FString MarkValue)
{	
	OnHLChatRichText(RichText, MarkPrefix, MarkValue);
}


void UHyperlinkManager::CopyHyperLinkProcess(UCS3RichTextBlock* RichText, FString LinkMark)
{
	FString Prefix = "";
	for (auto Pref : HyperLinks)
	{
		if (LinkMark.StartsWith(Pref))
		{
			Prefix = Pref;
			break;
		}
	}
	if (Prefix == "")
	{
		return;
	}
	FString Mark = UKismetStringLibrary::GetSubstring(LinkMark, Prefix.Len(), LinkMark.Len() - 1);
	if (Prefix != "goto:")
	{
		OnCopyHyperLinkToChat(Prefix, Mark);
	}
}

void UHyperlinkManager::JoinTeam(UCS3RichTextBlock* RichText, FString LinkMark)
{
	URoleTeamInterface* RoleTeamInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.RoleTeamInterface : nullptr;
	if (IsValid(RoleTeamInterface))
	{
		RoleTeamInterface->CELL_ApplyJoinFastTeam(LinkMark);
	}
}

void UHyperlinkManager::OpenUI(UCS3RichTextBlock* RichText, FString LinkMark)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, LinkMark);
	}
}

CONTROL_COMPILE_OPTIMIZE_END
