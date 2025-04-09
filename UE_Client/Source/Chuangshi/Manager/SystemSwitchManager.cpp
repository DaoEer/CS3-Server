#include "SystemSwitchManager.h"

#include "CanvasPanelSlot.h"

#include"Chuangshi.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "GameData/UIDataDefine.h"
#include "GameData/UIConfigData.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3PlayerController.h"
#include "CfgManager.h"
#include "QuestManager.h"
#include "ResourceManager.h"
#include "MessageManager.h"
#include "Guis/ActivityFunctionBarWidget.h"
#include "CS3Base/UIManager.h"
#include "GameStatus.h"

CONTROL_COMPILE_OPTIMIZE_START

USystemSwitchManager::USystemSwitchManager()
{

}

USystemSwitchManager::~USystemSwitchManager()
{

}

USystemSwitchManager* USystemSwitchManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<USystemSwitchManager>();
}

void USystemSwitchManager::LoadCfg()
{
	SystemSwitchDatasMap.Empty();
	if (!UGolbalBPFunctionLibrary::CfgManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:USystemSwitchManager::LoadCfg : CfgManager()!"));
		return;
	}
	const UConfigTable* ConfigTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SYATEM_OPEN_DATA);
	if (!ConfigTable)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USystemSwitchManager::LoadCfg : ConfigTable!"));
		return;
	}
	TArray<FName> Rows = ConfigTable->GetRowNames();
	if (Rows.Num() <= 0) return;
	for (FName& Row : Rows)
	{
		const FSystemSwitchData* Data = ConfigTable->GetRow<FSystemSwitchData>(Row);
		if (!Data)
		{
			CS3_Warning(TEXT("-->Null Pointer error:USystemSwitchManager::LoadCfg : Data!"));
			continue;
		}
		if (SystemSwitchDatasMap.Contains(Data->SystemIndex))
		{
			CS3_Warning(TEXT("SystemSwitchCfg Table has two same SystemIndex[%s]"), *(Data->SystemIndex.ToString()));
			continue;
		}
		//程序赋值KeyIndex
		FSystemSwitchData* TempData = const_cast<FSystemSwitchData*>(Data);
		for (FSystemOpenCondition& CNDData : TempData->OpenCnds)
		{
			CNDData.CndParams.SystemIndex = Data->SystemIndex;
		}
		for (FSystemCloseCondition& CNDData : TempData->CloseCnds)
		{
			CNDData.CndParams.SystemIndex = Data->SystemIndex;
		}
		for (FSystemSwitchAction& ACTData : TempData->OpenAction)
		{
			ACTData.ActParams.SystemIndex = Data->SystemIndex;
			ACTData.ActParams.BtnTag = Data->BtnTag;
		}
		//加入到系统开启配置数据
		SystemSwitchDatasMap.Add(Data->SystemIndex);
		SystemSwitchDatasMap[Data->SystemIndex] = *TempData;
	}
}

FSystemSwitchData USystemSwitchManager::GetSystemSwitchDataBySystemIndex(FName SystemIndex, bool& IsSuccess)
{
	for (TPair<FName, FSystemSwitchData>& Data : SystemSwitchDatasMap)
	{
		if (Data.Key == SystemIndex)
		{
			IsSuccess = true;
			return Data.Value;
		}
	}
	IsSuccess = false;
	return FSystemSwitchData();
}

FSystemSwitchData USystemSwitchManager::GetSystemSwitchDataByBtnTag(FName BtnTag, bool& IsSuccess)
{
	for (TPair<FName, FSystemSwitchData>& Data : SystemSwitchDatasMap)
	{
		if (Data.Value.BtnTag == BtnTag)
		{
			IsSuccess = true;
			return Data.Value;
		}
	}
	IsSuccess = false;
	return FSystemSwitchData();
}

FSystemSwitchData USystemSwitchManager::GetSystemSwitchDataBySystemWindowType(FString SystemWindowType, bool& IsSuccess)
{
	for (TPair<FName, FSystemSwitchData>& Data : SystemSwitchDatasMap)
	{
		if (Data.Value.SystemWindowID == SystemWindowType)
		{
			IsSuccess = true;
			return Data.Value;
		}
	}
	IsSuccess = false;
	return FSystemSwitchData();
}

TArray<FSystemSwitchData> USystemSwitchManager::GetSystemSwitchDataByWindowType(FString WindowType)
{
	TArray<FSystemSwitchData> TempArray = {};
	for (TPair<FName, FSystemSwitchData>& Data : SystemSwitchDatasMap)
	{
		if (Data.Value.WindowID == WindowType)
		{
			TempArray.Add(Data.Value);
		}
	}
	return TempArray;
}

bool USystemSwitchManager::IsOpenBySystemIndex(FName SystemIndex)
{
	bool IsSuccess;
	FSystemSwitchData SwitchData = GetSystemSwitchDataBySystemIndex(SystemIndex, IsSuccess);
	if (IsSuccess)
	{
		if (SwitchData.CheckOpenCondition() && !SwitchData.CheckCloseCondition())
		{
			return true;
		}
	}
	return false;
}

bool USystemSwitchManager::IsOpenByBtnTag(FName BtnTag)
{
	bool IsSuccess;
	FSystemSwitchData SwitchData = GetSystemSwitchDataByBtnTag(BtnTag, IsSuccess);
	if (IsSuccess)
	{
		if (SwitchData.CheckOpenCondition() && !SwitchData.CheckCloseCondition())
		{
			return true;
		}
	}
	return false;
}

bool USystemSwitchManager::CheckOpenByWindowType(FString SystemWindowType)
{
	bool IsSuccess;
	FSystemSwitchData SwitchData = GetSystemSwitchDataBySystemWindowType(SystemWindowType, IsSuccess);
	if (IsSuccess)
	{
		if (SwitchData.CheckOpenCondition() && !SwitchData.CheckCloseCondition())
		{
			return true;
		}
		else
		{
			for (FSystemOpenCondition& OpenCnd : SwitchData.OpenCnds)
			{
				//开启条件
				if (OpenCnd.CndParams.Script == TEXT("SystemOpenLevelCND"))
				{
					FString Level = OpenCnd.CndParams.Param1;
					FString args = Level + TEXT("|") + SwitchData.SystemName;
					UUECS3GameInstance::Instance->MessageManager->ShowMessage(405, args);
					return false;
				}
			}
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(2901);
			return false;
		}
	}
	return true;
}

void USystemSwitchManager::InitOpenStateByWindowType(FString WindowType)
{
	TArray<FSystemSwitchData> DataArray = GetSystemSwitchDataByWindowType(WindowType);
	for (FSystemSwitchData Data : DataArray)
	{
		Data.DoAction();
	}
}

FString USystemSwitchManager::GetTipsByBtnTag(FName BtnTag, bool& IsOpen)
{
	bool IsSuccess1;
	FSystemSwitchData SwitchData = GetSystemSwitchDataByBtnTag(BtnTag, IsSuccess1);
	if (IsSuccess1)
	{
		//条件tips
		FString TempTips = GetSystemConditionTips(IsOpen, SwitchData);
		bool IsSuccess2;
		FFunctionBtnData BtnData = GetBtnCfgByBtnTag(BtnTag, IsSuccess2);
		if (!IsSuccess2)
		{
			return TempTips;
		}
		//已经开启 && ActName不为空（即有快捷键），则显示快捷键
		if (IsOpen && !BtnData.ActName.IsEmpty())
		{
			//快捷键tips
			FGROUPKEY_DATA KeyValue;
			FString Key = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetKeyNameByActName(FSTRING_TO_FNAME(BtnData.ActName), KeyValue);
			return SwitchData.SystemName + TEXT(" ") + Key;
		}
		else
		{
			return TempTips;
		}
	}
	return TEXT("");
}

FFunctionBtnData USystemSwitchManager::GetBtnCfgByBtnTag(FName BtnTag, bool& IsSuccess)
{
	if (UGolbalBPFunctionLibrary::CfgManager())
	{
		const UConfigTable* ConfigTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_FUNCTION_BTN_DATA);
		if (ConfigTable)
		{
			const FFunctionBtnData* BtnData = ConfigTable->GetRow<FFunctionBtnData>(BtnTag);
			FFunctionBtnData* TempData = const_cast<FFunctionBtnData*>(BtnData);
			if (TempData)
			{
				IsSuccess = true;
				return *TempData;
			}
		}
	}
	IsSuccess = false;
	return FFunctionBtnData();
}

UClass* USystemSwitchManager::GetClassByScript(FString Script)
{
	FString ClassStr = TEXT("Class'/Script/Chuangshi.") + Script + TEXT("'");
	return (UClass*)UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(FSoftObjectPath(ClassStr));
}

int32 USystemSwitchManager::GetRemainTime(FName BtnTag)
{
	if (IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UActivityFunctionBarWidget* ActivityBarWidnow = Cast<UActivityFunctionBarWidget>(UUECS3GameInstance::Instance->GUIManager->GetWindow(TEXT("ActivityFunctionBar")));
		if (IsValid(ActivityBarWidnow))
		{
			return ActivityBarWidnow->GetRemainTime(BtnTag);
		}
	}
	return 0;
}

void USystemSwitchManager::OnChangeMyRoleLevel(int32 Level)
{
	//等级变化，重新检查所有系统开启条件
	CheckLevelSwitch(Level);
}

void USystemSwitchManager::OnChangeQuestState(int32 QuestID)
{
	//放弃任务，取消提示
	if (UGolbalBPFunctionLibrary::QuestManager()->IsQuestStatus(QuestID, (int32)QUEST_STATE::QUEST_NOT_ACCEPT))
	{
		AbandonQuest(QuestID);
	}
	//触发新提示
	else
	{
		CheckQuestSwitch(QuestID);
	}
}

void USystemSwitchManager::OnOpenActivitySystem(FName BtnTag, int32 RemainTime)
{
	if (IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UActivityFunctionBarWidget* ActivityBarWidnow = Cast<UActivityFunctionBarWidget>(UUECS3GameInstance::Instance->GUIManager->GetWindow(TEXT("ActivityFunctionBar")));
		if (IsValid(ActivityBarWidnow))
		{
			ActivityBarWidnow->AddActivitySystem(BtnTag, RemainTime);
		}
	}
}

void USystemSwitchManager::OnCloseActivitySystem(FName BtnTag)
{
	if (IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UActivityFunctionBarWidget* ActivityBarWidnow = Cast<UActivityFunctionBarWidget>(UUECS3GameInstance::Instance->GUIManager->GetWindow(TEXT("ActivityFunctionBar")));
		if (IsValid(ActivityBarWidnow))
		{
			ActivityBarWidnow->RemoveActivitySystem(BtnTag);
		}
	}
}

void USystemSwitchManager::OnEnterSpaceNotify(FString SpaceScriptID)
{
	if (UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == EGameStatus::InWorld)
	{
		CheckSpaceSwitch(SpaceScriptID);
	}
}

void USystemSwitchManager::OnEnterWorld()
{
	//刷新所有系统开启状态
	for (TPair<FName, FSystemSwitchData>& Data : SystemSwitchDatasMap)
	{
		Data.Value.DoAction();
	}
}

void USystemSwitchManager::OnLeaveWorld()
{

}

void USystemSwitchManager::CheckLevelSwitch(int32 Level)
{
	for (TPair<FName, FSystemSwitchData>& Data : SystemSwitchDatasMap)
	{
		Data.Value.DoAction();
	}
}

void USystemSwitchManager::CheckQuestSwitch(int32 QuestID)
{
	for (TPair<FName, FSystemSwitchData>& Data : SystemSwitchDatasMap)
	{
		Data.Value.DoAction();
	}
}

void USystemSwitchManager::CheckSpaceSwitch(FString SpaceScriptID)
{
	//刷新所有系统开启状态
	for (TPair<FName, FSystemSwitchData>& Data : SystemSwitchDatasMap)
	{
		Data.Value.DoAction();
	}
}

void USystemSwitchManager::AbandonQuest(int32 QuestID)
{
	for (TPair<FName, FSystemSwitchData>& Data : SystemSwitchDatasMap)
	{
		Data.Value.DoAction();
	}
}

FString USystemSwitchManager::GetSystemConditionTips(bool& IsOpen, FSystemSwitchData Data)
{
	TArray<FSystemOpenCondition> OpenCnds = Data.OpenCnds;
	//没有配置开启条件，则开启
	if (OpenCnds.Num() <= 0)
	{
		IsOpen = true;
		return TEXT("");
	}
	else
	{
		for (FSystemOpenCondition& OpenCnd : OpenCnds)
		{
			//只要有一条不符合或者满足关闭条件则未开启
			if (!OpenCnd.CheckOpenCondition() || Data.CheckCloseCondition())
			{
				if (OpenCnd.CndParams.Script == TEXT("SystemOpenLevelCND"))
				{
					FString CfgStr = GetTipsCfg(Data.SystemTipsID);
					FString Level = OpenCnd.CndParams.Param1;
					FString args = Level + TEXT("|") + Data.SystemName;
					FString tips = UGolbalBPFunctionLibrary::GetReplaceString(CfgStr, args);
					IsOpen = false;
					return tips;
				}
				else
				{
					IsOpen = false;
					return TEXT("");
				}
			}
		}
		//开启条件符合，不显示tips
		IsOpen = true;
		return TEXT("");
	}
}

FString USystemSwitchManager::GetTipsCfg(FString TipsID)
{
	if (!UGolbalBPFunctionLibrary::CfgManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:USystemSwitchManager::LoadCfg : CfgManager()!"));
		return TEXT("");
	}
	const UConfigTable* ConfigTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TIPS_DATA);
	if (!ConfigTable)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USystemSwitchManager::LoadCfg : ConfigTable!"));
		return TEXT("");
	}
	const FCS3TipsData* TipsData = ConfigTable->GetRow<FCS3TipsData>(FSTRING_TO_FNAME(TipsID));
	if (!TipsData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USystemSwitchManager::LoadCfg : TipsData!"));
		return TEXT("");
	}
	return TipsData->Tips;
}

CONTROL_COMPILE_OPTIMIZE_END