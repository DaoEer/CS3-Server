// Fill out your copyright notice in the Description page of Project Settings.


#include "ControllerModeMgr.h"
#include "OperationModeMgr.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/LocalDataSave/LocalUserSettingData.h"
#include "Manager/LocalDataSaveManager.h"
#include "Manager/CfgManager.h"
#include "Actor/ServerCharacter.h"
#include "Util/CS3Debug.h"
#include"Chuangshi.h"

CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("Init"), STAT_UControllerModeMgr_Init, STATGROUP_UControllerModeMgr);
DECLARE_CYCLE_STAT(TEXT("ExecuteInputInfor"), STAT_ExecuteInputInfor, STATGROUP_UControllerModeMgr);
DECLARE_CYCLE_STAT(TEXT("ChangeControllerMode"), STAT_UControllerModeMgr_ChangeMode, STATGROUP_UControllerModeMgr);
DECLARE_CYCLE_STAT(TEXT("ChangeControlModeToActive"), STAT_ChangeControlModeToActive, STATGROUP_UControllerModeMgr);
DECLARE_CYCLE_STAT(TEXT("GetModeDataByType"), STAT_GetModeDataByType, STATGROUP_UControllerModeMgr);
DECLARE_CYCLE_STAT(TEXT("SwitchModeInfor"), STAT_SwitchModeInfor, STATGROUP_UControllerModeMgr);
DECLARE_CYCLE_STAT(TEXT("ExecuteInstructionIfModeActive"), STAT_ExecuteInstructionIfModeActive, STATGROUP_UControllerModeMgr);

void UControllerModeMgr::BeginDestroy()
{
	Super::BeginDestroy();
}

UControllerModeMgr* UControllerModeMgr::GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<UControllerModeMgr>();
}

void UControllerModeMgr::Init()
{
	SCOPE_CYCLE_COUNTER(STAT_UControllerModeMgr_Init);
	CurControllerMode = ECONTROL_MODE::DefaultControlMode;
	OldControllerMode = ECONTROL_MODE::DefaultControlMode;
	BackControllerMode = ECONTROL_MODE::DefaultControlMode;

	//获取默认表格数据
	TMap<FString, FInputInforAndInstruction> TableDatas;
	GetDefaultTable(TableDatas);

	//创建默认的信息与指令字典
	CreatDeflautInputInforInstrMap(TableDatas);

	//获取默认操作模式的数据
	FControModeTable ControModeData;
	GetModeDataByType(ECONTROL_MODE::DefaultControlMode, ControModeData);

	//创建注册事件
	CreatRegisterEvent(ControModeData.RegisterEvent);
	OtherValue = ControModeData.OtherValue;
}

void UControllerModeMgr::ExecuteInputInfor(FString InputInfor, FString InputKey, const float& InputScale, TArray<FString> TempOtherValue)
{
	//CS3_Log(TEXT("UControllerModeMgr::ExecuteInputInfor --- InputInfor is %s,InputKey is %s!"), *InputInfor, *InputKey);
	SCOPE_CYCLE_COUNTER(STAT_ExecuteInputInfor);
	if (!(IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter())))
	{
		return;
	}

	//获取操作模式
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("UControllerModeMgr::ExecuteInputInfor --- OperationModeMgr Is Null !"));
		return;
	}

	//判断注册事件
	if (RegisterEvent.Contains(InputInfor))
	{
		//将指令传给操作管理，让其执行操作
		OperationModeMgr->ExecuteOperation(RegisterEvent[InputInfor].Instructions, InputKey, InputScale, TempOtherValue);

		return;
	}

	//通过输入信息获执行功能
	if (m_InforAndInstructions.Contains(InputInfor))
	{
		//将指令传给操作管理，让其执行操作
		OperationModeMgr->ExecuteOperation(m_InforAndInstructions[InputInfor].Instructions, InputKey, InputScale, TempOtherValue);
	}
	else
	{
		//CS3_Warning(TEXT("UControllerModeMgr::ExecuteInputInfor --- InputInfor Is Not Valid !"));
	}
}

void UControllerModeMgr::ChangeControllerMode(ECONTROL_MODE ControlMode, CC_MODE_REASON InReason, bool bIsBackMode, bool bIsIgnorePriority)
{
	CS3_Log(TEXT("UControllerModeMgr::ChangeControllerMode --- ControlMode is %d,CurControllerMode is %d, ChangeReason %d, bIsBackMode %d, bIsIgnorePriority %d"), ControlMode, CurControllerMode, InReason, bIsBackMode, bIsIgnorePriority);
	SCOPE_CYCLE_COUNTER(STAT_UControllerModeMgr_ChangeMode);
	//判断是否为一个模式
	if (ControlMode == CurControllerMode)
	{
		return;
	}
	/*
	如果忽略优先级，直接替换控制模式，根据是否是后台模式，将BackControllerMode赋值。
	如果考虑优先级，则比较了优先级在决定是否替换。
	*/
	if (bIsIgnorePriority)
	{
		SwitchModeInfor(ControlMode);
		if (bIsBackMode)
		{		
			BackControllerMode = ControlMode;
		}
	}
	else
	{
		if (bIsBackMode && GetModePriority(ControlMode) >= GetModePriority(BackControllerMode))
		{
			if (GetModePriority(ControlMode) >= GetModePriority(CurControllerMode))
			{
				SwitchModeInfor(ControlMode);
			}
			BackControllerMode = ControlMode;
		}
		if (GetModePriority(ControlMode) >= GetModePriority(CurControllerMode))
		{
			SwitchModeInfor(ControlMode);
		}
	}
	return;
}

void UControllerModeMgr::RecoveryMode()
{
	//判断背景模式和当前模式
	if (BackControllerMode == CurControllerMode)
	{
		return;
	}
	//切换模式
	ChangeControllerMode(BackControllerMode, CC_MODE_REASON::CCM_RECOVERY_CONTROLLER_MODE, true, true);
}

void UControllerModeMgr::RecoverySettingMode()
{
	ULocalUserSettingData* SettingData = UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalUserSettingData;

	if (IsValid(SettingData))
	{
		if (SettingData->CombatSettingData.IsACTMode)
		{
			ChangeControllerMode(ECONTROL_MODE::ActionControlMode, CC_MODE_REASON::CCM_RECOVERY_SETTING_CONTROLLER_MODE,true, true);
		}
		else
		{
			ChangeControllerMode(ECONTROL_MODE::DefaultControlMode, CC_MODE_REASON::CCM_RECOVERY_SETTING_CONTROLLER_MODE,true, true);
		}
	}
	else
	{
		CS3_Warning(TEXT("UControllerModeMgr::RecoverySettingMode --- SettingDataManager Is Null!"));
	}
}

bool UControllerModeMgr::ChangeControlModeFromACTToALT(bool bIsActToAlt /*= true*/)
{
	if (bIsActToAlt)
	{
		if (IsHaveMode(ECONTROL_MODE::ActionControlMode))
		{
			ChangeControllerMode(ECONTROL_MODE::AltControlMode, CC_MODE_REASON::CCM_ACTTOALT_CONTROLLER_MODE);
			return true;
		}
	}
	else
	{
		if (IsHaveMode(ECONTROL_MODE::AltControlMode))
		{
			RecoveryMode();
			return true;
		}
	}
	return false;
}

void UControllerModeMgr::ChangeControlModeToActive(bool bIsActive /*= false*/, bool bIsExcInst /*= true*/)
{
	SCOPE_CYCLE_COUNTER(STAT_ChangeControlModeToActive);
	if (CurControllerMode == ECONTROL_MODE::NoneMode)
	{
		return;
	}
	FControModeTable ControModeData;	
	//通过模式获取模式的数据
	GetModeDataByType(CurControllerMode, ControModeData);

	TMap<FString, FInputInforAndInstruction> TableDatas;
	
	if (bIsActive)
	{
		if (ControModeData.ActiveStatusInputInforAndInstruction.bIsClearData)
		{
			UGolbalBPFunctionLibrary::OperationModeMgr()->PropertyInit();
		}
		for (auto TableData : ControModeData.ActiveStatusInputInforAndInstruction.InputInforAndInstructions)
		{
			TableDatas.Add(TableData.InputInfor, TableData);
		}

		if (ControModeData.ActiveStatusInputInforAndInstruction.bIsReplace)
		{
			//更新信息与指令字典
			UpdataInputInfor(TableDatas);
		}
		else
		{
			ReplaceInputInfor(TableDatas);
		}
	}
	else
	{		
		if (ControModeData.UnActiveStatusInputInforAndInstruction.bIsClearData)
		{
			UGolbalBPFunctionLibrary::OperationModeMgr()->PropertyInit();
		}
		for (auto TableData : ControModeData.UnActiveStatusInputInforAndInstruction.InputInforAndInstructions)
		{
			TableDatas.Add(TableData.InputInfor, TableData);
		}

		if (ControModeData.UnActiveStatusInputInforAndInstruction.bIsReplace)
		{
			//更新信息与指令字典
			UpdataInputInfor(TableDatas);
		}
		else
		{
			ReplaceInputInfor(TableDatas);
		}
	}
	OtherValue = ControModeData.OtherValue;
	if (bIsExcInst)
	{
		ExecuteInstructionIfModeActive(CurControllerMode, !bIsActive, false);
		ExecuteInstructionIfModeActive(CurControllerMode, bIsActive, true);
	}
}

void UControllerModeMgr::GetDefaultTable(TMap<FString, FInputInforAndInstruction>& TableDatas)
{
	//获取配置数据
	auto ControlModeTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_DEFAULT_CONTROL_MODE);
	TArray<FDefaultControModeTable*> ControlDatas;
	if (IsValid(ControlModeTable))
	{
		//获取表里所有的数据
		ControlModeTable->GetAllRows<FDefaultControModeTable>(ControlDatas);

		for (auto ControData : ControlDatas)
		{
			//将表里的数据读取出来
			TableDatas.Add(ControData->InputInforAndInstruction.InputInfor,
				ControData->InputInforAndInstruction);
		}
	}
	else
	{
		CS3_Warning(TEXT("UControllerModeMgr::GetDefaultTable --- ControModeTable Is Null!"));
	}
}

void UControllerModeMgr::CreatDeflautInputInforInstrMap(const TMap<FString, FInputInforAndInstruction>& TableDatas)
{
	for (auto TableData : TableDatas)
	{
		///数据记录到默认和一般信息标识和指令字典
		m_DefaultInforAndInstructions.Add(TableData.Key, TableData.Value);
		m_InforAndInstructions.Add(TableData.Key, TableData.Value);
	}
}

void UControllerModeMgr::CreatRegisterEvent(TArray<FInputInforAndInstruction>& Events)
{
	for (auto EventOfRegister : Events)
	{
		RegisterEvent.Add(EventOfRegister.InputInfor, EventOfRegister);
	}
}

void UControllerModeMgr::GetModeDataByType(ECONTROL_MODE ControlMode, FControModeTable& ControModeData)
{
	SCOPE_CYCLE_COUNTER(STAT_GetModeDataByType);
	//获取配置数据
	auto ControlModeTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CONTROL_MODE);
	TArray<FControModeTable*> ControlDatas;
	if (IsValid(ControlModeTable))
	{
		//获取表里所有的数据
		ControlModeTable->GetAllRows<FControModeTable>(ControlDatas);

		for (auto ControData : ControlDatas)
		{
			//筛选合适的模式
			if (ControData->ControlMode == ControlMode)
			{
				ControModeData.ControlMode = ControData->ControlMode;
				ControModeData.ActiveStatusInputInforAndInstruction = ControData->ActiveStatusInputInforAndInstruction;
				ControModeData.UnActiveStatusInputInforAndInstruction = ControData->UnActiveStatusInputInforAndInstruction;
				ControModeData.RegisterEvent.Append(ControData->RegisterEvent);
				ControModeData.OtherValue= ControData->OtherValue;
				return;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("UControllerModeMgr::GetModeDataByType --- ControModeTable Is Null!"));
	}
}

void UControllerModeMgr::UpdataInputInfor(TMap<FString, FInputInforAndInstruction>& TableDatas)
{
	//先恢复到默认模式
	m_InforAndInstructions.Empty();
	m_InforAndInstructions.Append(m_DefaultInforAndInstructions);

	//再将要切换的模式进行差异替换
	for (auto TableData : TableDatas)
	{
		//判断是否存在这个Key
		if (m_InforAndInstructions.Contains(TableData.Key))
		{
			//替换数据
			m_InforAndInstructions[TableData.Key] = TableData.Value;
		}
		else
		{
			//添加数据
			m_InforAndInstructions.Add(TableData.Key, TableData.Value);
		}

	}
}

void UControllerModeMgr::ReplaceInputInfor(TMap<FString, FInputInforAndInstruction>& TableDatas)
{
	//置空
	m_InforAndInstructions.Empty();

	//直接填充
	for (auto TableData : TableDatas)
	{
		//添加数据
		m_InforAndInstructions.Add(TableData.Key, TableData.Value);
	}
}

void UControllerModeMgr::SwitchModeInfor(ECONTROL_MODE ControlMode)
{
	SCOPE_CYCLE_COUNTER(STAT_SwitchModeInfor);
	//判断当前是否已经是这个模式了
	if (CurControllerMode == ControlMode)
	{
		return;
	}
	
    UGolbalBPFunctionLibrary::OperationModeMgr()->PropertyInit();	

	OldControllerMode = CurControllerMode;
	CurControllerMode = ControlMode;
	ChangeControlModeToActive(true,false);
	//离开模式时执行
	ExecuteInstructionIfModeActive(OldControllerMode,true, false);
	//进入模式时执行
	ExecuteInstructionIfModeActive(CurControllerMode,true,true);
	FControModeTable ControModeData;

	//通过模式获取模式的数据
	GetModeDataByType(ControlMode, ControModeData);
	//切换注册事件
	SwitchRegisterEvent(ControModeData.RegisterEvent);
	OtherValue = ControModeData.OtherValue;
	///<当前模式为非激活状态
	if (IsValid(UUECS3GameInstance::Instance)&& !UUECS3GameInstance::Instance->IsGameWindowActive())
	{
		ChangeControlModeToActive(false);
	}	
}

void UControllerModeMgr::SwitchRegisterEvent(TArray<FInputInforAndInstruction>& Events)
{
	RegisterEvent.Empty();

	for (auto EventOfRegister : Events)
	{
		RegisterEvent.Add(EventOfRegister.InputInfor, EventOfRegister);
	}
}

int32 UControllerModeMgr::GetModePriority(ECONTROL_MODE ControlMode)
{
	//获取配置数据
	auto ModePriorityTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CONTROL_MODE);
	TArray<FControModeTable* > ModePriorities;

	if (ModePriorityTable)
	{
		//获取所有优先级数据
		ModePriorityTable->GetAllRows<FControModeTable>(ModePriorities);

		//匹配模式
		for (auto ModePriority : ModePriorities)
		{
			if (ControlMode == ModePriority->ControlMode)
			{
				return ModePriority->Priority;
			}
		}
	}
	return -1;
}

void UControllerModeMgr::ExecuteInstructionIfModeActive(ECONTROL_MODE ControlMode,bool bIsActive /*= true*/, bool bIsEnter /*= true*/)
{
	SCOPE_CYCLE_COUNTER(STAT_ExecuteInstructionIfModeActive);
	//获取操作模式
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr) || CurControllerMode == ECONTROL_MODE::NoneMode)
	{
		CS3_Warning(TEXT("UControllerModeMgr::ExecuteInputInfor --- OperationModeMgr Is Null or CurControllerMode == ECONTROL_MODE::NoneMode!"));
		return;
	}
	//控制模式数据
	FControModeTable ControModeData;

	//通过模式获取模式的数据
	GetModeDataByType(ControlMode, ControModeData);

	TArray<FString> TempOtherValue;
	if (bIsActive)
	{		
		if (bIsEnter)
		{//将指令传给操作管理，让其执行操作
			OperationModeMgr->ExecuteOperation(ControModeData.ActiveStatusInputInforAndInstruction.InstructionsIfSwitchMode, TEXT(""), 0.0f, TempOtherValue);
		}
		else
		{
			OperationModeMgr->ExecuteOperation(ControModeData.ActiveStatusInputInforAndInstruction.InstructionsIfSwitchOffMode, TEXT(""), 0.0f, TempOtherValue);
		}
	}
	else
	{
		if (bIsEnter) 
		{//将指令传给操作管理，让其执行操作
			OperationModeMgr->ExecuteOperation(ControModeData.UnActiveStatusInputInforAndInstruction.InstructionsIfSwitchMode, TEXT(""), 0.0f, TempOtherValue);
		}
		else
		{
			//将指令传给操作管理，让其执行操作
			OperationModeMgr->ExecuteOperation(ControModeData.UnActiveStatusInputInforAndInstruction.InstructionsIfSwitchOffMode, TEXT(""), 0.0f, TempOtherValue);
		}		
	}
}

CONTROL_COMPILE_OPTIMIZE_END
