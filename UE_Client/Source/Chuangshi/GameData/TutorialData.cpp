

#include "TutorialData.h"
#include "Blueprint/WidgetLayoutLibrary.h"
#include "Components/CanvasPanelSlot.h"
#include "Runtime/Engine/Classes/Engine/UserInterfaceSettings.h"
#include "Interface/Role/RoleTutorialInterface.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Manager/StoryManager.h"
#include "CS3Base/UIManager.h"
#include "GameDeFine.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/TutorialManager.h"
#include "CS3Base/UIManager.h"
#include "CS3Base/RootUIWidget.h"
#include "Manager/QuestManager.h"
#include "Manager/SkillManager.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/QuickBarManager.h"
#include "Interface/SkillInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

bool UTriggerCampCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 PlayerCamp = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("camp"));
	if (PlayerCamp == FSTRING_TO_INT(CndParams.Param1))
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool UTriggerLevelCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 PlayerLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("level"));
	if (PlayerLevel >= FSTRING_TO_INT(CndParams.Param1))
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool UTriggerLvRangeCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 MinLv = FSTRING_TO_INT(CndParams.Param1);
	int32 MaxLv = FSTRING_TO_INT(CndParams.Param2);
	int32 PlayerLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("level"));
	if ((PlayerLevel >= MinLv) && (PlayerLevel <= MaxLv))
	{
		return true;
	}
	else
	{
		return false;
	}

}

bool UTriggerEquipPartCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	URoleKitBagInterface* RoleKitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	UEquip* NewEquip = Cast<UEquip>(RoleKitBagInterface->FindItemByUID(Param2));
	if ( NewEquip && NewEquip->GetModelPartType() == (MODEL_PART_TYPE)(FSTRING_TO_INT(CndParams.Param1)))
	{
		return true;
	}
	else
	{
		return false;
	}

}

bool UTriggerProfessionCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 PlayerProfession = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("profession"));
	if (PlayerProfession == FSTRING_TO_INT(CndParams.Param1))
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool UTriggerGenderCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 PlayerGender = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("gender"));
	if (PlayerGender == FSTRING_TO_INT(CndParams.Param1))
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool UTriggerQuestCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 QuestID = FSTRING_TO_INT(CndParams.Param1);
	int32 QuestIDStatus = FSTRING_TO_INT(CndParams.Param2);
	return UGolbalBPFunctionLibrary::QuestManager()->IsQuestStatus(QuestID, QuestIDStatus);
}

bool UTriggerQuestTaskCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 QuestID = FSTRING_TO_INT(CndParams.Param1);
	//先判断任务是否已接受，因为任务目标只有未完成和已完成的状态，没有接没接的状态，未接未完成也会判断为true
	if (UGolbalBPFunctionLibrary::QuestManager()->IsQuestStatus(QuestID, (int32)QUEST_STATE::QUEST_IS_DONE)
		|| UGolbalBPFunctionLibrary::QuestManager()->IsQuestStatus(QuestID, (int32)QUEST_STATE::QUEST_NOT_DONE))
	{
		int32 TaskID = FSTRING_TO_INT(CndParams.Param2);
		int32 TaskIDStatus = FSTRING_TO_INT(CndParams.Param3);
		return UGolbalBPFunctionLibrary::QuestManager()->IsTaskStatus(QuestID, TaskID, TaskIDStatus);
	}
	return false;
}

bool UTriggerAddItemCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 ItemID = FSTRING_TO_INT(CndParams.Param1);
	return (ItemID == FSTRING_TO_INT(Param1));
}

bool UTriggerItemInKitbagCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	UCS3EntityInterface* TempInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0);
	if (!IsValid(TempInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerItemInKitbagCND::CheckCondition : TempInterface!"));
		return false;
	}
	URoleKitBagInterface* kbinterface = Cast<URoleKitBagInterface>(TempInterface);
	if (!IsValid(kbinterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerItemInKitbagCND::CheckCondition : kbinterface!"));
		return false;
	}
	TArray<UItemBase*> items = kbinterface->GetItemsByItemID(FSTRING_TO_INT(CndParams.Param1));
	if (items.Num() > 0) return true;
	return false;
}

bool UTriggerAddSkillCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 SkilID = FSTRING_TO_INT(CndParams.Param1);
	return (SkilID == FSTRING_TO_INT(Param1));
}

bool UTriggerHasSkillCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	USkillManager* SkillManager = UGolbalBPFunctionLibrary::SkillManager();
	if (!IsValid(SkillManager))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerHasSkillCND::CheckCondition : SkillManager!"));
		return false;
	}
	TArray<int32> SkillIDList = SkillManager->GetPlayerSkillIdList();
	for (int32 SkillID : SkillIDList)
	{
		if (INT_TO_FSTRING(SkillID) == CndParams.Param1)
		{
			return true;
		}
	}
	return false;
}

bool UTriggerHasQuickSkillCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuickBarManager))
	{
		TArray<FQB_ITEM> QbItems = UUECS3GameInstance::Instance->QuickBarManager->GetQbItemList();
		if (CndParams.Param1 == TEXT("0"))
		{
			for (FQB_ITEM QbItem : QbItems)
			{
				if (QbItem.QbID == FSTRING_TO_INT(CndParams.Param1))
				{
					return false;
				}
			}
			return true;
		}
		else
		{
			for (FQB_ITEM QbItem : QbItems)
			{
				if (QbItem.QbID == FSTRING_TO_INT(CndParams.Param1))
				{
					return true;
				}
			}
			return false;
		}
	}
	return false;
}

bool UTriggerAddBuffCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 BuffID = FSTRING_TO_INT(CndParams.Param1);
	return (BuffID == FSTRING_TO_INT(Param1));
}

bool UTriggerHasBuffCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	USkillInterface* SkillInterface = Cast<USkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(USkillInterface::GetName(), 0));
	if (IsValid(SkillInterface))
	{
		TMap<int32, BuffDataType> BuffDatasMap = SkillInterface->getAttrBuffs();
		for (TPair<int32, BuffDataType>& BuffData : BuffDatasMap)
		{
			int32 BuffID = BuffData.Value.buffID;
			if (BuffID == FSTRING_TO_INT(CndParams.Param1))
			{
				return true;
			}
		}
	}
	return false;
}

bool UTriggerStoryCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	int32 StoryID = FSTRING_TO_INT(CndParams.Param1);
	int32 StoryStatus = FSTRING_TO_INT(CndParams.Param2);
	//当前触发的是这个镜头，并且状态符合
	if (StoryID == FSTRING_TO_INT(Param1) && StoryStatus == FSTRING_TO_INT(Param2))
	{
		return true;
	}
	return false;
}

bool UTriggerQuickBarSlotCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->QuickBarManager))
	{
		return false;
	}
	int32 IsFixed = FSTRING_TO_INT(CndParams.Param1);
	if (IsFixed == 0)
	{
		//不固定，判断当前页是否有空位
		int32 SlotIndex = UUECS3GameInstance::Instance->QuickBarManager->GetQuickBarSlotIndex();
		//没有空位不触发，-1表示无空位
		if (SlotIndex > -1)
		{
			return true;
		}
	}
	else if (IsFixed == 1)
	{
		//固定位置，判断当前页SlotIndex位置有没有被占
		int32 SlotIndex = FSTRING_TO_INT(CndParams.Param2);
		//快捷栏当前页SlotIndex位置没有被占，才能触发
		if (!UUECS3GameInstance::Instance->QuickBarManager->HasQuickItemInIndex(SlotIndex))
		{
			return true;
		}
	}
	return false;
}

bool UTriggerOpenWindowCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	if (CndParams.Param1 == Param1)
	{
		return true;
	}
	return false;
}

bool UTriggerMatchIndexCND::CheckCondition(const FTCNDPARAM& CndParams, const FString& Param1, const FString& Param2)
{
	if (CndParams.Param1 == Param2)
	{
		return true;
	}
	return false;
}

bool FTriggerCondition::CheckCondition(const FString& Param1, const FString& Param2)
{
	if (CndParams.ScriptID)
	{
		CndObj = NewObject<UTriggerBaseCND>(GetTransientPackage(), CndParams.ScriptID);
		return CndObj->CheckCondition(CndParams, Param1, Param2);
	}
	return false;
}

bool FTriggerTutorialAction::DoAction(const FString& Param1, const FString& Param2)
{
	///触发条件不满足时返回
	if (!CheckCondition(Param1, Param2))	return false;
	if (ActParams.ScriptID)
	{
		ActObj = NewObject<UTriggerBaseACT>(GetTransientPackage(), ActParams.ScriptID);
		ActObj->DoAction(ActParams, Param1, Param2);
		return true;
	}
	return false;
}

void UTriggerArrowACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	UGolbalBPFunctionLibrary::TutorialManager()->DoArrowAction(ActParams);
}

void UTriggerDragItemACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	//隐藏当前消息指引
	UGolbalBPFunctionLibrary::TutorialManager()->HideCurrentMessageTutorial();

	FString WindowType = TEXT("DragItemTutorial");
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		//界面用完就销毁了（只是到销毁池了并没有真正销毁），如果马上又触发了同类指引的话，还是能获取到之前的界面对象，所以重新创建一个，并允许创建多个
		UBaseWindow* DragItemWnd = UGolbalBPFunctionLibrary::GUIManager()->CreateUIWindow(WindowType, true);
		if (!IsValid(DragItemWnd))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTriggerDragItemACT::DoAction : DragItemWnd!"));
			return;
		}
		DragItemWnd->Show();
		UGolbalBPFunctionLibrary::TutorialManager()->AddShowTriggerWnd(ActParams.KeyIndex, DragItemWnd);
		//设置内容
		FString arg = TEXT("AddItem");
		FOutputDeviceNull ar;
		FString Temp1 = FNAME_TO_FSTRING(ActParams.KeyIndex);
		arg = *FString::Printf(TEXT("%s \"%s\" \"%s\" \"%s\""), *arg, *Param2, *(ActParams.Param2), *Temp1);
		DragItemWnd->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
		//播放语音
		UGolbalBPFunctionLibrary::TutorialManager()->PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
		//设置当前消息提示指引数据
		UGolbalBPFunctionLibrary::TutorialManager()->SetCurrentShowMessageData(ActParams.KeyIndex, ActParams);
	}
}

void UTriggerFirstLearnSkillACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	//隐藏当前箭头指引
	UGolbalBPFunctionLibrary::TutorialManager()->HideCurrentArrowTutorial();

	FString WindowType = TEXT("FirstLearnSkillTutorial");
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		//界面用完就销毁了（只是到销毁池了并没有真正销毁），如果马上又触发了同类指引的话，还是能获取到之前的界面对象，所以重新创建一个，并允许创建多个
		UBaseWindow* SkillTutorialWnd = UGolbalBPFunctionLibrary::GUIManager()->CreateUIWindow(WindowType, true);
		if (!IsValid(SkillTutorialWnd))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTriggerFirstLearnSkillACT::DoAction : SkillTutorialWnd!"));
			return;
		}
		SkillTutorialWnd->Show();
		UGolbalBPFunctionLibrary::TutorialManager()->AddShowTriggerWnd(ActParams.KeyIndex, SkillTutorialWnd);
		//设置内容
		FString arg = TEXT("ShowSkills");
		FOutputDeviceNull ar;
		FString Temp1 = FNAME_TO_FSTRING(ActParams.KeyIndex);
		//参数：Param1包含 技能或药品ID，ID类型（1表示技能，3表示药品），是否固定快捷栏格子索引，快捷栏格子相对索引值
		arg = *FString::Printf(TEXT("%s \"%s\""), *arg, *(ActParams.Param1));
		SkillTutorialWnd->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
		//播放语音
		UGolbalBPFunctionLibrary::TutorialManager()->PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
		//设置当前箭头提示指引数据
		UGolbalBPFunctionLibrary::TutorialManager()->SetCurrentShowArrowData(ActParams.KeyIndex, ActParams);
	}
}

void UTriggerMessageACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	//隐藏当前消息指引
	UGolbalBPFunctionLibrary::TutorialManager()->HideCurrentMessageTutorial();

	FString WindowType = TEXT("MessageTutorial");
	//显示操作提示框
	//界面用完就销毁了（只是到销毁池了并没有真正销毁），如果马上又触发了同类指引的话，还是能获取到之前的界面对象，所以重新创建一个，并允许创建多个
	UBaseWindow* MessageTutorialWnd = UGolbalBPFunctionLibrary::GUIManager()->CreateUIWindow(WindowType, true);
	if (!IsValid(MessageTutorialWnd))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerMessageACT::DoAction : MessageTutorialWnd!"));
		return;
	}
	
	//设置提示内容
	FString arg = TEXT("SetMessageInfo");
	FOutputDeviceNull ar;
	FString Temp1 = FNAME_TO_FSTRING(ActParams.KeyIndex);
	//参数分别为KeyIndex、消息类型、ItemID、UID、是否显示物品图标、是否显示提示箭头、内容、标题、确定按钮文本、取消按钮文本
	arg = *FString::Printf(TEXT("%s \"%s\" \"%s\" \"%s\" \"%s\" \"%s\" \"%s\" \"%s\" \"%s\" \"%s\" \"%s\""), *arg, *Temp1, *(ActParams.Param2), *Param1, *Param2, *(ActParams.Param3), *(ActParams.Param4), *(ActParams.Param6), *(ActParams.Param5), *(ActParams.Param7), *(ActParams.Param8));
	MessageTutorialWnd->CallFunctionByNameWithArguments(*arg, ar, NULL, true);

	MessageTutorialWnd->Show();
	UGolbalBPFunctionLibrary::TutorialManager()->AddShowTriggerWnd(ActParams.KeyIndex, MessageTutorialWnd);
	//播放语音
	UGolbalBPFunctionLibrary::TutorialManager()->PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
	//设置当前消息提示指引数据
	UGolbalBPFunctionLibrary::TutorialManager()->SetCurrentShowMessageData(ActParams.KeyIndex, ActParams);
}

void UTriggerImageACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	//隐藏当图片指引
	UGolbalBPFunctionLibrary::TutorialManager()->HideCurrentImageTutorial();

	FString WindowType = TEXT("ImageTutorial");
	//显示操作提示框
	//界面用完就销毁了（只是到销毁池了并没有真正销毁），如果马上又触发了同类指引的话，还是能获取到之前的界面对象，所以重新创建一个，并允许创建多个
	UBaseWindow* ImageWnd = UGolbalBPFunctionLibrary::GUIManager()->CreateUIWindow(WindowType, true);
	if (!IsValid(ImageWnd))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerOperationACT::DoAction : ImageWnd!"));
		return;
	}
	//设置提示内容
	FString arg = TEXT("SetImageInfo");
	FOutputDeviceNull ar;
	FString Temp1 = FNAME_TO_FSTRING(ActParams.KeyIndex);
	//参数分别为KeyIndex、图片资源路径、是否显示“下一步”按钮
	arg = *FString::Printf(TEXT("%s \"%s\" \"%s\" \"%s\" \"%s\""), *arg, *Temp1, *(ActParams.Param1), *(ActParams.Param2));
	ImageWnd->CallFunctionByNameWithArguments(*arg, ar, NULL, true);

	ImageWnd->Show();
	UGolbalBPFunctionLibrary::TutorialManager()->AddShowTriggerWnd(ActParams.KeyIndex, ImageWnd);
	//播放语音
	UGolbalBPFunctionLibrary::TutorialManager()->PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
	//设置当前图片指引数据
	UGolbalBPFunctionLibrary::TutorialManager()->SetCurrentShowImageData(ActParams.KeyIndex, ActParams);
}

void UTriggerOperationACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	//隐藏当图片指引
	UGolbalBPFunctionLibrary::TutorialManager()->HideCurrentImageTutorial();

	FString WindowType = TEXT("OperationTutorial");
	//显示操作提示框
	//界面用完就销毁了（只是到销毁池了并没有真正销毁），如果马上又触发了同类指引的话，还是能获取到之前的界面对象，所以重新创建一个，并允许创建多个
	UBaseWindow* OperationWnd = UGolbalBPFunctionLibrary::GUIManager()->CreateUIWindow(WindowType, true);
	if (!IsValid(OperationWnd))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerOperationACT::DoAction : OperationWnd!"));
		return;
	}
	OperationWnd->Show();
	UGolbalBPFunctionLibrary::TutorialManager()->AddShowTriggerWnd(ActParams.KeyIndex, OperationWnd);
	//播放语音
	UGolbalBPFunctionLibrary::TutorialManager()->PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
	//设置当前图片指引数据
	UGolbalBPFunctionLibrary::TutorialManager()->SetCurrentShowImageData(ActParams.KeyIndex, ActParams);
}

void UTriggerKeyACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	//隐藏当图片指引
	UGolbalBPFunctionLibrary::TutorialManager()->HideCurrentImageTutorial();

	FString WindowType = TEXT("ShortcutTutorial");
	//显示按键提示框
	//界面用完就销毁了（只是到销毁池了并没有真正销毁），如果马上又触发了同类指引的话，还是能获取到之前的界面对象，所以重新创建一个，并允许创建多个
	UBaseWindow* KeyWnd = UGolbalBPFunctionLibrary::GUIManager()->CreateUIWindow(WindowType, true);
	if (!IsValid(KeyWnd))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerKeyACT::DoAction : KeyWnd!"));
		return;
	}
	KeyWnd->Show();
	UGolbalBPFunctionLibrary::TutorialManager()->AddShowTriggerWnd(ActParams.KeyIndex, KeyWnd);
	//设置提示框标题、内容、是否显示关闭按钮
	FString arg = TEXT("SetTitleAndContent");
	FOutputDeviceNull ar;
	arg = *FString::Printf(TEXT("%s \"%s\" \"%s\" \"%s\""), *arg, *(ActParams.Param1), *(ActParams.Param2), *(ActParams.Param3));
	KeyWnd->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
	//播放语音
	UGolbalBPFunctionLibrary::TutorialManager()->PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
	//设置当前图片指引数据
	UGolbalBPFunctionLibrary::TutorialManager()->SetCurrentShowImageData(ActParams.KeyIndex, ActParams);
}

void UTriggerBuyTipsACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	//隐藏当前箭头指引
	UGolbalBPFunctionLibrary::TutorialManager()->HideCurrentArrowTutorial();

	UWidget* TargetWidget = UGolbalBPFunctionLibrary::TutorialManager()->GetWidgetFromWidgetPath(ActParams.UIType, ActParams.UILinkTarget);
	if (!IsValid(TargetWidget))
	{
		//指引目标没有了
		return;
	}

	if (!UGolbalBPFunctionLibrary::GUIManager()) return;
	UCS3UserWidget* ParentWindow;
	if (ActParams.UILinkTarget == TEXT(""))
	{
		ParentWindow = UGolbalBPFunctionLibrary::GUIManager()->RootUIWidget;
	}
	else
	{
		ParentWindow = UGolbalBPFunctionLibrary::TutorialManager()->GetParentWindowFromWidgetPath(ActParams.UILinkTarget);
	}
	if (!IsValid(ParentWindow)) return;
	//目标的位置和大小
	FVector2D Pos = UGolbalBPFunctionLibrary::TutorialManager()->GetWidgetPosition(ActParams.UIType, ActParams.UILinkTarget);;
	FVector2D Size = UGolbalBPFunctionLibrary::TutorialManager()->GetWidgetSize(ActParams.UIType, ActParams.UILinkTarget);
	//显示提示
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController)) return;
	UUserWidget* Tips = CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_BuyTips")));
	if (!IsValid(Tips)) return;
	UPanelSlot* PanelSlot = ParentWindow->AddChild(Tips);
	if (!IsValid(PanelSlot))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerBuyTipsACT::DoAction : PanelSlot!"));
		return;
	}
	UCanvasPanelSlot* CanvasPanelSlot = Cast<UCanvasPanelSlot>(PanelSlot);
	if (!IsValid(CanvasPanelSlot))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerBuyTipsACT::DoAction : CanvasPanelSlot!"));
		return;
	}
	CanvasPanelSlot->SetAutoSize(true);
	//根据使用的类型来计算窗口位置
	//FVector2D WidgetSize = Tips->GetCachedGeometry().GetDrawSize();
	FVector2D WidgetSize = FVector2D(315.0, 167.0);
	float ViewportScale = UGolbalBPFunctionLibrary::GetViewportScale();
	FVector2D FilterPos = FVector2D(Pos.X + Size.X / ViewportScale / 2 - 21, Pos.Y + 20 - WidgetSize.Y);
	Tips->SetRenderTranslation(FilterPos);
	//将指引增加到管理器数组
	UGolbalBPFunctionLibrary::TutorialManager()->AddShowTriggerWnd(ActParams.KeyIndex, Tips);
	//设置图片文字和内容
	FString arg = TEXT("SetContent");
	FOutputDeviceNull ar;
	arg = *FString::Printf(TEXT("%s \"%s\" \"%s\" \"%s\""), *arg, *(FNAME_TO_FSTRING(ActParams.KeyIndex)), *(ActParams.Param1), *(ActParams.Param2));
	Tips->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
	//播放语音
	UGolbalBPFunctionLibrary::TutorialManager()->PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
	//设置当前箭头指引数据
	UGolbalBPFunctionLibrary::TutorialManager()->SetCurrentShowArrowData(ActParams.KeyIndex, ActParams);
}

void UTriggerMoveTipsACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	//隐藏当图片指引
	UGolbalBPFunctionLibrary::TutorialManager()->HideCurrentImageTutorial();

	FString WindowType = TEXT("MoveTutorial");
	//显示移动提示框
	//界面用完就销毁了（只是到销毁池了并没有真正销毁），如果马上又触发了同类指引的话，还是能获取到之前的界面对象，所以重新创建一个，并允许创建多个
	UBaseWindow* MoveTipsWnd = UGolbalBPFunctionLibrary::GUIManager()->CreateUIWindow(WindowType, true);
	if (!IsValid(MoveTipsWnd))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerMoveTipsACT::DoAction : MoveTipsWnd!"));
		return;
	}
	MoveTipsWnd->Show();
	UGolbalBPFunctionLibrary::TutorialManager()->AddShowTriggerWnd(ActParams.KeyIndex, MoveTipsWnd);
	//播放语音
	UGolbalBPFunctionLibrary::TutorialManager()->PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
	//设置当前图片指引数据
	UGolbalBPFunctionLibrary::TutorialManager()->SetCurrentShowImageData(ActParams.KeyIndex, ActParams);
}

void UTriggerStoryACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	//播放镜头
	UGStoryManager* GStoryManager = UGolbalBPFunctionLibrary::GStoryManager();
	if (GStoryManager) GStoryManager->PlaySequence(ActParams.Param1);
}

void UTriggerDragGestureACT::DoAction(const FTUTORIALPARAM& ActParams, const FString& Param1, const FString& Param2)
{
	//隐藏当图片指引
	UGolbalBPFunctionLibrary::TutorialManager()->HideCurrentImageTutorial();

	UWidget* TargetWidget = UGolbalBPFunctionLibrary::TutorialManager()->GetWidgetFromWidgetPath(ActParams.UIType, ActParams.UILinkTarget);
	if (!IsValid(TargetWidget))
	{
		//指引目标没有了
		return;
	}

	if (!UGolbalBPFunctionLibrary::GUIManager()) return;
	UCS3UserWidget* ParentWindow;
	if (ActParams.UILinkTarget == TEXT(""))
	{
		ParentWindow = UGolbalBPFunctionLibrary::GUIManager()->RootUIWidget;
	}
	else
	{
		ParentWindow = UGolbalBPFunctionLibrary::TutorialManager()->GetParentWindowFromWidgetPath(ActParams.UILinkTarget);
	}
	if (!IsValid(ParentWindow)) return;
	//目标的位置和大小
	FVector2D Pos = UGolbalBPFunctionLibrary::TutorialManager()->GetWidgetPosition(ActParams.UIType, ActParams.UILinkTarget);;
	FVector2D Size = UGolbalBPFunctionLibrary::TutorialManager()->GetWidgetSize(ActParams.UIType, ActParams.UILinkTarget);
	//显示提示
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController)) return;
	UUserWidget* DragGestureTips = CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_DragGesture")));
	if (!IsValid(DragGestureTips)) return;
	UPanelSlot* PanelSlot = ParentWindow->AddChild(DragGestureTips);
	if (!IsValid(PanelSlot))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerDragGestureACT::DoAction : PanelSlot!"));
		return;
	}
	UCanvasPanelSlot* CanvasPanelSlot = Cast<UCanvasPanelSlot>(PanelSlot);
	if (!IsValid(CanvasPanelSlot))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTriggerDragGestureACT::DoAction : CanvasPanelSlot!"));
		return;
	}
	CanvasPanelSlot->SetAutoSize(true);
	//计算窗口位置
	float ViewportScale = UGolbalBPFunctionLibrary::GetViewportScale();
	FVector2D FilterPos = FVector2D(Pos.X + Size.X / ViewportScale / 2 - 22, Pos.Y);
	DragGestureTips->SetRenderTranslation(FilterPos);
	//将指引增加到管理器数组
	UGolbalBPFunctionLibrary::TutorialManager()->AddShowTriggerWnd(ActParams.KeyIndex, DragGestureTips);
	//播放手势动画
	FString arg = TEXT("StartAnimation");
	FOutputDeviceNull ar;
	arg = *FString::Printf(TEXT("%s"), *arg);
	DragGestureTips->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
	//播放语音
	UGolbalBPFunctionLibrary::TutorialManager()->PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
	//设置当前图片指引数据
	UGolbalBPFunctionLibrary::TutorialManager()->SetCurrentShowImageData(ActParams.KeyIndex, ActParams);
}

void FTUTORIALDATA::SaveTriggerIndex()
{
	if (bIsTriggerOnce)
	{
		URoleTutorialInterface* RoleTutorialInterface = Cast<URoleTutorialInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTutorialInterface"), 0));
		if (IsValid(RoleTutorialInterface))
		{
			RoleTutorialInterface->FinishTriggerOnceTurtorial(KeyIndex);
		}
	}
}

void FTUTORIALDATA::DoAction(const FString& Param1, const FString& Param2)
{
	//不符合触发条件 || 符合关闭条件 || 没有配置指引行为，则不显示指引
	if (!CheckCondition(Param1, Param2) || CheckCloseCondition(Param1, true) || TriggerActs.Num() <= 0)	return;
	UGolbalBPFunctionLibrary::TutorialManager()->DoAction(KeyIndex, TutorialType, DelayTime, Param1, Param2);
}

bool FCloseCondition::CheckCloseCondition(const FString& Param1, const bool& IsOpenCheck /*= false*/)
{
	if (CndParams.ScriptID)
	{
		CndObj = NewObject<UCloseBaseCND>(GetTransientPackage(), CndParams.ScriptID);
		return CndObj->CheckCloseCondition(CndParams, Param1, IsOpenCheck);
	}
	return false;
}

bool UCloseMaxLevelCND::CheckCloseCondition(const FCLOSECNDPARAM& CndParams, const FString& Param1, const bool& IsOpenCheck /*= false*/)
{
	int32 PlayerLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("level"));
	if (PlayerLevel >= FSTRING_TO_INT(CndParams.Param1))
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool UCloseQuestCND::CheckCloseCondition(const FCLOSECNDPARAM& CndParams, const FString& Param1, const bool& IsOpenCheck /*= false*/)
{
	int32 QuestID = FSTRING_TO_INT(CndParams.Param1);
	int32 QuestIDStatus = FSTRING_TO_INT(CndParams.Param2);
	return UGolbalBPFunctionLibrary::QuestManager()->IsQuestStatus(QuestID, QuestIDStatus);
}

bool UClosePlaySkillCND::CheckCloseCondition(const FCLOSECNDPARAM& CndParams, const FString& Param1, const bool& IsOpenCheck /*= false*/)
{
	if (IsOpenCheck)
	{
		//触发开启指引的时候不检查关闭条件
		return false;
	}
	int32 PlaySkillID = FSTRING_TO_INT(Param1);
	int32 SkillID = FSTRING_TO_INT(CndParams.Param1);
	if (PlaySkillID == SkillID)
	{
		return true;
	}
	return false;
}

bool UCloseSkillInQuickBarCND::CheckCloseCondition(const FCLOSECNDPARAM& CndParams, const FString& Param1, const bool& IsOpenCheck /*= false*/)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuickBarManager))
	{
		TArray<FQB_ITEM> QbItems = UUECS3GameInstance::Instance->QuickBarManager->GetQbItemList();
		if (CndParams.Param1 == TEXT("0"))
		{
			for (FQB_ITEM QbItem : QbItems)
			{
				if (QbItem.QbID == FSTRING_TO_INT(CndParams.Param1))
				{
					return false;
				}
			}
			return true;
		}
		else
		{
			for (FQB_ITEM QbItem : QbItems)
			{
				if (QbItem.QbID == FSTRING_TO_INT(CndParams.Param1))
				{
					return true;
				}
			}
			return false;
		}
	}
	return false;
}

CONTROL_COMPILE_OPTIMIZE_END
