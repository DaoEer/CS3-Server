
#include "Manager/MessageManager.h"
#include"Chuangshi.h"
#include "Util/CS3Debug.h"
#include "PaperFlipbook.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CfgManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/UIManager.h"
#include "Manager/AudioManager.h"
#include "Guis/TextAnimMessageWidget.h"
#include "Manager/LocalDataSaveManager.h"

CONTROL_COMPILE_OPTIMIZE_START
#pragma region UMessage

void UMessage::CreateFromConfig(const FMESSAGE_DATA* CfgData, const FString& args)
{
	ID = CfgData->RowName;
	messageTypes = CfgData->MessageTypes;
	Message = GetReplaceMessage(CfgData->Message, args);
	Args = args;
	MessageCfg = CfgData->Message;
	HoldTime = CfgData->HoldTime;
}
void UMessage::Show() const
{
}

FString UMessage::GetReplaceMessage(const FString& replaceMessage, const FString args/* = TEXT("")*/,FString SplitChar /*= TEXT("|")*/)
{
	//把提示信息中的参数用传入的参数进行填充
	FString MsgArgs = args;
	TArray<FStringFormatArg> ArgsArray;
	FString left, right;
	bool result = true;
	while (!MsgArgs.IsEmpty())
	{
		result = MsgArgs.Split(SplitChar, &left, &right, ESearchCase::Type::CaseSensitive);
		if (result)
		{
			MsgArgs = right;
			ArgsArray.Add(GetColorStr(left));
		}
		else
		{
			ArgsArray.Add(GetColorStr(MsgArgs));
			MsgArgs = TEXT("");
		}
	}
	FString infoMessage;
	if (ArgsArray.Num() > 0)
		infoMessage = FString::Format(*(GetFormatColorMessage(replaceMessage)), ArgsArray);
	else
		infoMessage = GetFormatColorMessage(replaceMessage);
	return infoMessage;
}

FString UMessage::GetFormatColorMessage(const FString& replaceMessage)
{
	return replaceMessage;
}

FString UMessage::GetColorStr(const FString& ColorStr)
{
	return ColorStr;
}

#pragma endregion

#pragma region UDialogMessage

void UDialogMessage::Show() const
{
	if (UGolbalBPFunctionLibrary::GameInstance())
	{
		UGolbalBPFunctionLibrary::GameInstance()->MessageManager->ShowMessageBox(this, 0, "");
	}
	else
	{
		CS3_Warning(TEXT("UGolbalBPFunctionLibrary::GameInstance() == null   !!!!!!  UDialogMessage::Show()"));
	}
}
void UDialogMessage::CreateFromConfig(const FMESSAGE_DATA* CfgData, const FString& args)
{
	DialogType = CfgData->DialogType;
	DialogBtnTexts = CfgData->DialogBtnTexts;
	ParentWindowType = CfgData->ParentWindowType;
	Title = CfgData->Title;
	CDTimerType = CfgData->CountDownType;
	IsCover = CfgData->IsCover;
	IsDialogArgCountDown = CfgData->IsDialogArgCountDown;
	TimerArgIndex = CfgData->TimerArgIndex;
	Super::CreateFromConfig(CfgData, args);
}

FDelegateHandle UDialogMessage::AddClickDelegate(FBtnClick EventBack)
{
	return ClickEventList.Add(EventBack);
}

void UDialogMessage::RevmoeClickDelegate(FDelegateHandle EventBackHandle)
{
	ClickEventList.Remove(EventBackHandle);
}

void UDialogMessage::OnTrigerClick(RT_BTN_TYPE BtnType)
{
	ClickEventList.Broadcast(BtnType);
}

#pragma endregion

#pragma region UChatMessage
void UChatMessage::Show() const
{
	if (UGolbalBPFunctionLibrary::GameInstance())
	{
		UGolbalBPFunctionLibrary::GameInstance()->MessageManager->ShowChatMessage(this);
	}
	else
	{
		CS3_Warning(TEXT("UGolbalBPFunctionLibrary::GameInstance() == null   !!!!!!  UChatMessage::Show()"));
	}
}
void UChatMessage::CreateFromConfig(const FMESSAGE_DATA* CfgData, const FString& args)
{
	ChatGroups = CfgData->ChatGroups;
	Super::CreateFromConfig(CfgData, args);
}

#pragma endregion

#pragma region UPromptMessage
void UPromptMessage::Show() const
{
	if (UGolbalBPFunctionLibrary::GameInstance())
	{
		UGolbalBPFunctionLibrary::GameInstance()->MessageManager->ShowPromptMessage(this);
	}
	else
	{
		CS3_Warning(TEXT("UGolbalBPFunctionLibrary::GameInstance() == null   !!!!!!  UPromptMessage::Show()"));
	}
}
void UPromptMessage::CreateFromConfig(const FMESSAGE_DATA* CfgData, const FString& args)
{
	promptMsgType = CfgData->PromptType;
	Super::CreateFromConfig(CfgData, args);
}

#pragma endregion

#pragma region UCountDownMessage
void UCountDownMessage::Show() const
{
	if (UGolbalBPFunctionLibrary::GameInstance())
	{
		UGolbalBPFunctionLibrary::GameInstance()->MessageManager->ShowCountDownMessage(this);
	}
	else
	{
		CS3_Warning(TEXT("UGolbalBPFunctionLibrary::GameInstance() == null   !!!!!!  UCountDownMessage::Show()"));
	}
}
#pragma endregion

#pragma region UAIPortraitDialogMessage
void UAIPortraitDialogMessage::Show() const
{
	if (UGolbalBPFunctionLibrary::GameInstance())
	{
		UGolbalBPFunctionLibrary::GameInstance()->MessageManager->ShowAIPortraitDialogMessage(this);
	}
	else
	{
		CS3_Warning(TEXT("UGolbalBPFunctionLibrary::GameInstance() == null   !!!!!!  UPortraitDialogMessage::Show()"));
	}
}

#pragma endregion

#pragma region UMessageManager
UMessageManager::UMessageManager()
{

}
UMessageManager* UMessageManager::GetInstance()
{
	cs3_checkNoReentry();

	return (UMessageManager*)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MessageManager")));
}

const UConfigTable* UMessageManager::GetSafeMessageTable()
{
	if (!IsValid(MessageTable))
	{
		MessageTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_MESSAGE);
	}
	return MessageTable;
	InitUnRepeatData();
}

void UMessageManager::ShowMessage(const int32& MessageID, FBtnClick EventBack/* = nullptr*/)
{
	ShowMessage(MessageID, TEXT(""), EventBack);
}


void UMessageManager::ShowMessage(const int32& MessageID, const FString args, FBtnClick EventBack /*= nullptr*/, int32 Key /*= 0 */, const FString& Compotent  /*= "" */)
{
	auto MsgTable = GetSafeMessageTable();
	const FMESSAGE_DATA* MessageData = MsgTable->GetRow<FMESSAGE_DATA>(FString::FromInt(MessageID));
	bool bIsError = false;
	if (!MessageData)
	{
		//如果当前数据为空，则使用默认数据
		MessageData = MsgTable->GetRow<FMESSAGE_DATA>(FString( TEXT("1") ));
		bIsError = true;
	}
	if (MessageData)
	{
		TArray<MESSAGE_TYPE> MessageTypes = MessageData->MessageTypes;
		for (auto MessageType : MessageTypes)
		{
			UMessage* Msg = nullptr;
			switch (MessageType)
			{
			case MESSAGE_TYPE::MESSAGE_TYPE_DIALOG://对话框模式
			{
				if ( IsUnRepeat(MessageID) )
				{
					break;
				}
				Msg = NewObject<UDialogMessage>();
				if (bIsError)
				{
					Msg->CreateFromConfig(MessageData, INT_TO_FSTRING(MessageID));
				}
				else
				{
					Msg->CreateFromConfig(MessageData, args);
				}
				if (EventBack.IsBound())
				{
					((UDialogMessage*)Msg)->AddClickDelegate(EventBack);
				}
				this->ShowMessageBox((UDialogMessage*)Msg, Key, Compotent);
				break;
			}
			case MESSAGE_TYPE::MESSAGE_TYPE_CHAT://聊天窗口模式直接上屏
			{
				Msg = NewObject<UChatMessage>();
				Msg->CreateFromConfig(MessageData, args);
				this->ShowChatMessage((UChatMessage*)Msg);
				break;
			}
			case MESSAGE_TYPE::MESSAGE_TYPE_COUNTDOWN://倒计时模式
			{
				Msg = NewObject<UCountDownMessage>();
				Msg->CreateFromConfig(MessageData, args);
				this->ShowCountDownMessage((UCountDownMessage*)Msg);
				break;
			}
			case MESSAGE_TYPE::MESSAGE_TYPE_AI_PORTRAIT_DIALOG://AI小半身像提示界面
			{
				Msg = NewObject<UAIPortraitDialogMessage>();
				Msg->CreateFromConfig(MessageData, args);
				Msg->Show();
				break;
			}
			case MESSAGE_TYPE::MESSAGE_TYPE_PROMPT:// 屏幕消息提示
			{
				Msg = NewObject<UPromptMessage>();
				Msg->CreateFromConfig(MessageData, args);
				this->ShowPromptMessage((UPromptMessage*)Msg);
				break;
			}
			default:
				break;
			}
		}
	}
}

void UMessageManager::BP_ShowMessageWithID(const int32 MessageID, const FString args, FOnBtnClick EventBack)
{
	ShowMessage(MessageID, args, FBtnClick::CreateLambda([EventBack](RT_BTN_TYPE RtType)
	{
		EventBack.ExecuteIfBound(RtType);
	}));
}

void UMessageManager::BP_ShowMessage(UMessage* Message)
{
	ShowMessage(Message);
}

void UMessageManager::ShowMessage(UMessage* Message)
{
	UClass* msgClass = Message->GetClass();
	if (msgClass->IsChildOf(UDialogMessage::StaticClass()))
	{
		Message->Show();
	}
	else if (msgClass->IsChildOf(UChatMessage::StaticClass()))
	{
		Message->Show();
	}
}

void UMessageManager::HideMessage(const int32 MessageID)
{
	for (UCS3MessageBoxWidget* Widget : MessageBoxWidgetArray)
	{
		//有同MessageID的消息框
		if (Widget && Widget->MessageBoxID == FSTRING_TO_FNAME(INT_TO_FSTRING(MessageID)))
		{
			if (Widget->IsVisible())
			{
				Widget->ResponseMessageBtn(RT_BTN_TYPE::RT_CANCEL);
			}
			return;
		}
	}
}

void UMessageManager::HideAllMessage()
{
	for (UCS3MessageBoxWidget* Widget : MessageBoxWidgetArray)
	{
		if (Widget && Widget->IsVisible())
		{
			Widget->ResponseMessageBtn(RT_BTN_TYPE::RT_CANCEL);
		}
	}
}

void UMessageManager::HideCountDownMessage(const int32 MessageID)
{
	BP_HideCountDownMessage(MessageID);
}

void UMessageManager::ShowCoverPanel()
{
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::InWorld, TEXT("CoverPanel"));
	}
}

bool UMessageManager::HasCoverMessage()
{
	for (UCS3MessageBoxWidget* Widget : MessageBoxWidgetArray)
	{
		if (Widget && Widget->IsVisible() && Widget->IsCover)
		{
			return true;
		}
	}
	return false;
}

void UMessageManager::RemoveMessageBoxData(FName MessageID)
{
	for (UCS3MessageBoxWidget* Widget : MessageBoxWidgetArray)
	{
		if (Widget && Widget->MessageBoxID == MessageID)
		{
			MessageBoxWidgetArray.Remove(Widget);
			return;
		}
	}
}

void UMessageManager::ShowMessageBox_Implementation(const UDialogMessage* msg, int32 Key, const FString& Compotent)
{
	//如果配了遮挡底层界面鼠标事件，显示消息前先显示遮盖面板，这样消息面板会在遮盖面板上一层
	if (msg->IsCover)
	{
		ShowCoverPanel();
	}
	//显示消息框
	bool HasBpx = false;
	for (UCS3MessageBoxWidget* Widget : MessageBoxWidgetArray)
	{
		if (Widget && Widget->MessageBoxID == msg->ID)
		{
			//有同MessageID的消息框
			if ((Widget->IsVisible()))
			{
				Widget->Hide();
			}
			Widget->Show(msg->ParentWindowType);
			HasBpx = true;
			Widget->ShowMessage(msg, Key, Compotent);
		}
	}
	if (HasBpx == false)
	{
		//没有同MessageID的消息框，创建新的消息框
		UCS3MessageBoxWidget* Widget = Cast<UCS3MessageBoxWidget>(UGolbalBPFunctionLibrary::GUIManager()->CreateUIWindow(TEXT("MessageBox"), true));
		if (Widget)
		{
			Widget->Show(msg->ParentWindowType);
			MessageBoxWidgetArray.Add(Widget);
			Widget->ShowMessage(msg, Key, Compotent);
		}
	}
}

void UMessageManager::ShowPromptMessage_Implementation(const UPromptMessage* msg)
{
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::InWorld, TEXT("PromptMessage"));
	}
}

void UMessageManager::ShowChatMessage_Implementation(const UChatMessage* msg)
{
	
}

void UMessageManager::ShowCountDownMessage_Implementation(const UCountDownMessage* msg)
{
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(false, EGameStatus::InWorld, TEXT("CountDownMessage"));
	}
}

void UMessageManager::ShowAIPortraitDialogMessage_Implementation(const UAIPortraitDialogMessage* msg)
{
	if (UGolbalBPFunctionLibrary::AudioManager())
	{
		UGolbalBPFunctionLibrary::AudioManager()->StopVoice();
	}
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(false, EGameStatus::InWorld, TEXT("MonsterAIDialog"));
	}
}

void UMessageManager::ShowTextAnimationMessage(FName AnimationID)
{
	if (!IsValid(UGolbalBPFunctionLibrary::GUIManager()))
	{
		return;
	}
	FTextAnimationMessage TextAnimation;
	if (!GetTextAnimation(AnimationID, TextAnimation))
	{
		return;
	}
	TArray<FString> WindowTypes = TextAnimation.WindowType;
	bool IsShow = true;
	for (auto WindowType : WindowTypes)
	{
		UBaseWindow* Window = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(WindowType);
		if (!IsValid(Window) || (IsValid(Window) && !Window->IsVisible()))
		{
			IsShow = false;
			break;
		}
	}
	if (IsShow)
	{
		UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::InWorld, TEXT("TextAnimationMessage"));
		UTextAnimMessageWidget* TextAnimationMessage = Cast<UTextAnimMessageWidget>(UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("TextAnimationMessage")));
		if (IsValid(TextAnimationMessage))
		{
			TextAnimationMessage->SetInfo(TextAnimation);
		}
	}
}

bool UMessageManager::GetTextAnimation(FName AnimationID, FTextAnimationMessage& OutTextAnimationMessage)
{
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TEXT_ANIMATION_MESSAGE_DATA);
	FTextAnimationMessage* data = const_cast<FTextAnimationMessage*>(table->GetRow<FTextAnimationMessage>(AnimationID));
	if (data == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMessageManager::GetTextAnimation : data!"));
		return false;
	}
	OutTextAnimationMessage = *data;
	return true;
}

void UMessageManager::Tick(float DeltaTime)
{

}

bool UMessageManager::IsTickable() const
{
	return true;
}

TStatId UMessageManager::GetStatId() const
{
	RETURN_QUICK_DECLARE_CYCLE_STAT(UMessageManager, STATGROUP_Tickables);
}

void UMessageManager::InitUnRepeatData()
{
	if (!UGolbalBPFunctionLibrary::LocalDataSaveManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::InitChatChannelData : LocalDataSaveManager()!"));
		return;
	}
	if (!IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalMessageData))
	{
		UGolbalBPFunctionLibrary::LocalDataSaveManager()->InitLocalMessageDataFile();
	}
	UnRepeatDatas = UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalMessageData->GetMessageData();
}

void UMessageManager::ChangeRepeatData(const int32 MsgID)
{
	FUnRepeatData TempData;
	TempData.MsgID = MsgID;
	UnRepeatDatas.Add(TempData);
	SaveRepeatData();
}

void UMessageManager::SaveRepeatData()
{
	ULocalDataSaveManager* LocalDataSaveManager = UGolbalBPFunctionLibrary::LocalDataSaveManager();
	if (IsValid(LocalDataSaveManager) && IsValid(LocalDataSaveManager->LocalMessageData))
	{
		LocalDataSaveManager->LocalMessageData->SaveDataToFile(UnRepeatDatas);
	}
}
bool UMessageManager::IsUnRepeat(const int32 MsgID)
{
	ULocalDataSaveManager* LocalDataSaveManager = UGolbalBPFunctionLibrary::LocalDataSaveManager();
	if (IsValid(LocalDataSaveManager) && IsValid(LocalDataSaveManager->LocalMessageData))
	{
		UnRepeatDatas = LocalDataSaveManager->LocalMessageData->GetMessageData();
		for (auto msgData : UnRepeatDatas)
		{
			if (msgData.MsgID == MsgID) { return true; }
		}
		return false;
	}
	return false;
}

CONTROL_COMPILE_OPTIMIZE_END