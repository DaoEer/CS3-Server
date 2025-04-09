#include "SystemSwitchData.h"

#include "Util/ConvertUtil.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/QuestManager.h"
#include "Manager/SystemSwitchManager.h"
#include "Manager/TutorialManager.h"
#include "CS3Base/UIManager.h"
#include "Guis/ActivityFunctionBarWidget.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

bool USystemOpenLevelCND::CheckOpenCondition(const FSystemOpenCNDParam& CndParams)
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

bool USystemOpenQuestCND::CheckOpenCondition(const FSystemOpenCNDParam& CndParams)
{
	int32 QuestID = FSTRING_TO_INT(CndParams.Param1);
	int32 QuestIDStatus = FSTRING_TO_INT(CndParams.Param2);
	return UGolbalBPFunctionLibrary::QuestManager()->IsQuestStatus(QuestID, QuestIDStatus);
}

bool USystemOpenQuestTaskCND::CheckOpenCondition(const FSystemOpenCNDParam& CndParams)
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

bool USystemOpenSpaceCND::CheckOpenCondition(const FSystemOpenCNDParam& CndParams)
{
	if (CndParams.Param1.Equals(TEXT("")))
	{
		return true;
	}
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	TArray<FString> Maps = UGolbalBPFunctionLibrary::SplitString(CndParams.Param1, false, "|");
	if (Maps.Contains(SpaceScriptID))
	{
		return true;
	}
	return false;
}

bool USystemCloseLevelCND::CheckCloseCondition(const FSystemCloseCNDParam& CndParams)
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

bool USystemCloseQuestCND::CheckCloseCondition(const FSystemCloseCNDParam& CndParams)
{
	int32 QuestID = FSTRING_TO_INT(CndParams.Param1);
	int32 QuestIDStatus = FSTRING_TO_INT(CndParams.Param2);
	return UGolbalBPFunctionLibrary::QuestManager()->IsQuestStatus(QuestID, QuestIDStatus);
}

bool FSystemOpenCondition::CheckOpenCondition()
{
	if (!CndParams.Script.IsEmpty())
	{
		UClass* ScriptClass = UUECS3GameInstance::Instance->SystemSwitchManager->GetClassByScript(CndParams.Script);
		if (ScriptClass)
		{
			CndObj = NewObject<USystemOpenBaseCND>(GetTransientPackage(), ScriptClass);
			return CndObj->CheckOpenCondition(CndParams);
		}
	}
	return false;
}

bool FSystemCloseCondition::CheckCloseCondition()
{
	if (!CndParams.Script.IsEmpty())
	{
		UClass* ScriptClass = UUECS3GameInstance::Instance->SystemSwitchManager->GetClassByScript(CndParams.Script);
		if (ScriptClass)
		{
			CndObj = NewObject<USystemCloseBaseCND>(GetTransientPackage(), ScriptClass);
			return CndObj->CheckCloseCondition(CndParams);
		}
	}
	return false;
}

void USystemSwitchLightACT::DoOpenAction(const FSystemSwitchACTParam& ActParams)
{
	//按钮可点击
	UWidget* LocalWidget = UGolbalBPFunctionLibrary::TutorialManager()->GetWidgetFromWidgetPath(ActParams.UIType, ActParams.UILinkTarget);
	if (LocalWidget)
	{
		LocalWidget->SetIsEnabled(true);
	}
}

void USystemSwitchLightACT::DoCloseAction(const FSystemSwitchACTParam& ActParams)
{
	//按钮可点击
	UWidget* LocalWidget = UGolbalBPFunctionLibrary::TutorialManager()->GetWidgetFromWidgetPath(ActParams.UIType, ActParams.UILinkTarget);
	if (LocalWidget)
	{
		LocalWidget->SetIsEnabled(false);
	}
}

void USystemSwitchEffectACT::DoOpenAction(const FSystemSwitchACTParam& ActParams)
{
	UActivityFunctionBarWidget* FunctionBarWidget = Cast<UActivityFunctionBarWidget>(UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("ActivityFunctionBar")));
	if (FunctionBarWidget)
	{
		FunctionBarWidget->AddActivitySystem(ActParams.BtnTag);
	}
}

void USystemSwitchEffectACT::DoCloseAction(const FSystemSwitchACTParam& ActParams)
{
	UActivityFunctionBarWidget* FunctionBarWidget = Cast<UActivityFunctionBarWidget>(UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("ActivityFunctionBar")));
	if (FunctionBarWidget)
	{
		FunctionBarWidget->RemoveActivitySystem(ActParams.BtnTag);
	}
}

void FSystemSwitchAction::DoOpenAction()
{
	if (!ActParams.Script.IsEmpty())
	{
		UClass* ScriptClass = UUECS3GameInstance::Instance->SystemSwitchManager->GetClassByScript(ActParams.Script);
		if (ScriptClass)
		{
			ActObj = NewObject<USystemSwitchBaseACT>(GetTransientPackage(), ScriptClass);
			ActObj->DoOpenAction(ActParams);
		}
	}
}

void FSystemSwitchAction::DoCloseAction()
{
	if (!ActParams.Script.IsEmpty())
	{
		UClass* ScriptClass = UUECS3GameInstance::Instance->SystemSwitchManager->GetClassByScript(ActParams.Script);
		if (ScriptClass)
		{
			ActObj = NewObject<USystemSwitchBaseACT>(GetTransientPackage(), ScriptClass);
			ActObj->DoCloseAction(ActParams);
		}
	}
}

void FSystemSwitchData::DoAction()
{
	//有开启行为，显示开启效果
	if (OpenAction.Num() > 0)
	{
		//符合开启条件 && 不符合关闭条件
		if (CheckOpenCondition() && !CheckCloseCondition())
		{
			OpenAction[0].DoOpenAction();
		}
		//符合关闭条件,则取消开启效果
		else if (CheckCloseCondition())
		{
			OpenAction[0].DoCloseAction();
		}
		//不符合开启条件，则取消开启效果
		else if (!CheckOpenCondition())
		{
			OpenAction[0].DoCloseAction();
		}
	}
}

CONTROL_COMPILE_OPTIMIZE_END