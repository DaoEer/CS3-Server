// Fill out your copyright notice in the Description page of Project Settings.


#include "OperationModeMgr.h"
#include "Operation/BaseOperation.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Fight/AtkState/AtkState.h"
#include "Operation/OperationData.h"
#include <exception>
#include <stdexcept>
#include"Chuangshi.h"
#include "Util/CS3Debug.h"
#include "Manager/CfgManager.h"

DECLARE_CYCLE_STAT(TEXT("ExecuteOperation"), STAT_ExecuteOperation, STATGROUP_UOperationModeMgr);
DECLARE_CYCLE_STAT(TEXT("ChangeMode"), STAT_UOperationModeMgr_ChangeMode, STATGROUP_UOperationModeMgr);
DECLARE_CYCLE_STAT(TEXT("GetModeDataByType"), STAT_UOperationModeMgr_GetModeDataByType, STATGROUP_UOperationModeMgr);
DECLARE_CYCLE_STAT(TEXT("SwitchModeInfor"), STAT_UOperationModeMgr_SwitchModeInfor, STATGROUP_UOperationModeMgr);
DECLARE_CYCLE_STAT(TEXT("CreatOperationByName"), STAT_UOperationModeMgr_CreatOperationByName, STATGROUP_UOperationModeMgr);

CONTROL_COMPILE_OPTIMIZE_START
void UOperationModeMgr::BeginDestroy()
{
	Super::BeginDestroy();
}

UOperationModeMgr* UOperationModeMgr::GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<UOperationModeMgr>();
}

void UOperationModeMgr::Init()
{
	ForwardVector = FVector::ZeroVector;
	RightVector = FVector::ZeroVector;
	bIsKeepDirection = false;
	bIsCameraBeOperationed = false;
	bIsAutoMove = false;
	bIsCanTurn = true;
	CurOperationMode = EATTACT_STATE::NULL_ATT;
	OldOperationMode = EATTACT_STATE::NULL_ATT;
	BackOperationMode = EATTACT_STATE::NULL_ATT;

	//获取默认表格数据
	TMap<FString, FString> TableDatas;
	GetDefaultTable(TableDatas);

	//创建默认的指令与操作模式字典
	CreatDeflautInstrNameOperationMap(TableDatas);
}

void UOperationModeMgr::PropertyInit()
{
	ForwardVector = FVector::ZeroVector;
	RightVector = FVector::ZeroVector;
	bIsKeepDirection = false;
	bIsCameraBeOperationed = false;
	bIsAutoMove = false;
	bIsCanTurn = true;
}

void UOperationModeMgr::ExecuteOperation(TArray<FString> Instructions, FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_ExecuteOperation);
	//获取操作对象并执行
	for (auto Instruction : Instructions)
	{
		if (m_InstrucAndOperation.Contains(Instruction))
		{
			try
			{
				//获取操作对象
				UBaseOperation* Operation = CreatOperationByName(m_InstrucAndOperation[Instruction]);

				if (IsValid(Operation))
				{
					//CS3_Log(TEXT("UOperationModeMgr::ExecuteOperation --- InputKey is %s, Instruction is %s !"), *InputKey, *Instruction);
					Operation->ExecuteOperation(InputKey, InputScale, OtherValue);
				}
				else
				{
					CS3_Warning(TEXT("UOperationModeMgr::ExecuteInputInfor --- Operation Is Null !"));
				}
			}
			catch (const std::exception &e)
			{
				CS3_Warning(TEXT("Exception: UOperationModeMgr::ExecuteOperation Instruction:%s operation:%s InputKey:%s InputScale:%f reason:%s"), *Instruction, *(m_InstrucAndOperation[Instruction]), *InputKey, InputScale, e.what());
			}
			catch (...)
			{
				CS3_Warning(TEXT("Exception: UOperationModeMgr::ExecuteOperation Instruction:%s operation:%s InputKey:%s InputScale:%f reason:unknown"), *Instruction, *(m_InstrucAndOperation[Instruction]), *InputKey, InputScale);
			}
			
		}
	}
}

void UOperationModeMgr::ChangeMode(EATTACT_STATE OperationMode, bool bIsBackMode)
{
	SCOPE_CYCLE_COUNTER(STAT_UOperationModeMgr_ChangeMode);
	//判断是否为一个模式
	if (bIsBackMode)
	{
		if (OperationMode == BackOperationMode)
		{
			return;
		}
	}
	else
	{
		if (OperationMode == CurOperationMode)
		{
			return;
		}
	}

	//获取想要替换的模式的优先级
	int32 WantToSwitchModePriority = GetModePriority(OperationMode);
	//获取当前模式的优先级
	int32 CurModePriority = GetModePriority(CurOperationMode);

	if (bIsBackMode)
	{
		//获取背景模式优先级
		int32 BackModePriority = GetModePriority(BackOperationMode);
		//判断背景优先级
		if (WantToSwitchModePriority >= BackModePriority)
		{
			//判断当前模式和想要换的模式的优先级
			if (WantToSwitchModePriority >= CurModePriority || EATTACT_STATE::NULL_ATT == OperationMode)
			{
				SwitchModeInfor(OperationMode);
			}

			//替换背景模式
			BackOperationMode = OperationMode;
		}
	}
	else if (WantToSwitchModePriority >= CurModePriority || EATTACT_STATE::NULL_ATT == OperationMode)
	{
		SwitchModeInfor(OperationMode);
	}
}

void UOperationModeMgr::RecoveryMode()
{
	ChangeMode(EATTACT_STATE::NULL_ATT);
}

void UOperationModeMgr::GetDefaultTable(TMap<FString, FString>& TableDatas)
{
	//获取配置数据
	auto OperationModeTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_DEFAULT_OPERATION_MODE);
	TArray<FDefaultOperationModeTable*> OperationDatas;
	if (IsValid(OperationModeTable))
	{
		//获取表里所有的数据
		OperationModeTable->GetAllRows<FDefaultOperationModeTable>(OperationDatas);

		for (auto OperationData : OperationDatas)
		{
			//将表里的数据读取出来
			TableDatas.Add(OperationData->Instruction, OperationData->Operation);
		}
	}
	else
	{
		CS3_Warning(TEXT("UOperationModeMgr::GetDefaultTable --- OperationModeTable Is Null!"));
	}
}

void UOperationModeMgr::CreatDeflautInstrNameOperationMap(const TMap<FString, FString>& TableDatas)
{
	//创建操作并加入字典
	for (auto TableData : TableDatas)
	{
		//添加到字典
		m_DeInstrucAndOperation.Add(TableData.Key, TableData.Value);
		m_InstrucAndOperation.Add(TableData.Key, TableData.Value);
	}
}

void UOperationModeMgr::GetModeDataByType(EATTACT_STATE Operation, FOperationModeTable& TableData)
{
	SCOPE_CYCLE_COUNTER(STAT_UOperationModeMgr_GetModeDataByType);
	//获取配置数据
	auto OperationModeTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_OPERATION_MODE);
	TArray<FOperationModeTable*> OperationModeDatas;

	if (IsValid(OperationModeTable))
	{
		//获取所有操作
		OperationModeTable->GetAllRows<FOperationModeTable>(OperationModeDatas);

		for (auto OperationModeData : OperationModeDatas)
		{
			//筛选出正确的模式
			if (OperationModeData->OperationMode == Operation)
			{
				TableData.OperationMode = OperationModeData->OperationMode;
				TableData.bIsReplace = OperationModeData->bIsReplace;
				TableData.InstructionAndOperations = OperationModeData->InstructionAndOperations;
				TableData.InstructionsIfSwitchMode = OperationModeData->InstructionsIfSwitchMode;
				TableData.InstructionsIfSwitchOffMode = OperationModeData->InstructionsIfSwitchOffMode;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("UOperationModeMgr::GetModeDataByType --- OperationModeTable is Null!"))
	}
}

void UOperationModeMgr::UpdataOperation(const TMap<FString, FString>& UpdataDatas)
{
	//先恢复到默认模式
	m_InstrucAndOperation.Empty();
	m_InstrucAndOperation.Append(m_DeInstrucAndOperation);

	//遍历要变化的数据列表
	for (auto UpdataData : UpdataDatas)
	{
		//判断是否有这个指令
		if (m_InstrucAndOperation.Contains(UpdataData.Key))
		{

			m_InstrucAndOperation[UpdataData.Key] = UpdataData.Value;
		}
		else
		{
			m_InstrucAndOperation.Add(UpdataData.Key, UpdataData.Value);
		}
	}
}

void UOperationModeMgr::ReplaceInputInfor(const TMap<FString, FString>& UpdataDatas)
{
	//置空
	m_InstrucAndOperation.Empty();

	//填充
	for (auto UpdataData : UpdataDatas)
	{
		m_InstrucAndOperation.Add(UpdataData.Key, UpdataData.Value);
	}
}

void UOperationModeMgr::SwitchModeInfor(EATTACT_STATE OperationMode)
{
	SCOPE_CYCLE_COUNTER(STAT_UOperationModeMgr_SwitchModeInfor);
	//判断当前是否已经是这个模式了
	if (CurOperationMode == OperationMode)
	{
		return;
	}

	PropertyInit();

	FOperationModeTable OldOperationModeTable;
	FOperationModeTable CurOperationModeTable;

	TArray<FString> OtherValue;

	OldOperationMode = CurOperationMode;
	CurOperationMode = OperationMode;

	//通过当前的模式获取模式的数据
	GetModeDataByType(OldOperationMode, OldOperationModeTable);
	//切出模式时执行的操作
	ExecuteOperation(OldOperationModeTable.InstructionsIfSwitchOffMode, TEXT(""), 0.0f, OtherValue);

	//通过将要切换到的模式获取模式的数据
	GetModeDataByType(CurOperationMode, CurOperationModeTable);	
	if (CurOperationModeTable.bIsReplace)
	{
		//更新指令与操作字典
		UpdataOperation(CurOperationModeTable.InstructionAndOperations);
	}
	else
	{
		ReplaceInputInfor(CurOperationModeTable.InstructionAndOperations);
	}
		
	//切换时要执行的操作
	ExecuteOperation(CurOperationModeTable.InstructionsIfSwitchMode, TEXT(""), 0.0f, OtherValue);
}

int32 UOperationModeMgr::GetModePriority(EATTACT_STATE OperationMode)
{
	if (UAtkStateBase::PriorityDictionary.Contains(OperationMode))
	{
		return UAtkStateBase::PriorityDictionary[OperationMode];
	}

	return -1;
}

UBaseOperation* UOperationModeMgr::CreatOperationByName(FString Name)
{
	SCOPE_CYCLE_COUNTER(STAT_UOperationModeMgr_CreatOperationByName);
	//如果已经有过创建就直接返回
	if (m_AllOperation.Contains(Name))
	{
		return m_AllOperation[Name];
	}

	//获取配置数据
	auto OperationClassTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_OPERATION_CLASS);
	const FOperationClassTable* OperationClassData;

	if (IsValid(OperationClassTable))
	{
		//获取表里所有的数据
		OperationClassData = OperationClassTable->GetRow<FOperationClassTable>(FName(TEXT("0")));

		if (OperationClassData)
		{
			//CS3_Warning(TEXT("UOperationModeMgr::CreatDeflautInstrNameOperationMap ---%s"),*Name);
			if (OperationClassData->OperationClasses.Contains(Name))
			{
				UBaseOperation* Operation = NewObject<UBaseOperation>
					(GetOuter(), OperationClassData->OperationClasses[Name].Get());
				Operation->Init(Name);

				//将新建的操作加入到字典里
				m_AllOperation.Add(Name, Operation);

				return Operation;
			}
			else
			{
				CS3_Warning(TEXT("UOperationModeMgr::CreatDeflautInstrNameOperationMap --- Name Is Not Valid!"));
				return nullptr;
			}
		}
	}

	CS3_Warning(TEXT("UOperationModeMgr::CreatDeflautInstrNameOperationMap --- OperationClassTable Is Null!"));
	return nullptr;
}

CONTROL_COMPILE_OPTIMIZE_END
