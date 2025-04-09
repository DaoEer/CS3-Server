// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleLbcTaskInterface.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CS3Base/UIManager.h"
#include "Manager/EventManager.h"
#include "Manager/CfgManager.h"
#include "../../GameData/ShortcutKeyData.h"
#include "../../Actor/Player/PlayerCharacter.h"
#include "../../Util/ConvertUtil.h"
#include "../../Component/SpringArmComponentEX.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base\BaseWindow.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/AtkStateMar.h"



CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleLbcTaskInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RoleMoveToLocation, &URoleLbcTaskInterface::RoleMoveToLocation, const  KBEngine::FVariantArray&, const float&, const float&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(StartRoleLbcTaskOperation, &URoleLbcTaskInterface::StartRoleLbcTaskOperation, const float&, const FVector&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(LbcTaskCreateBody, &URoleLbcTaskInterface::LbcTaskCreateBody, const FString&, const int32&, const float&, const FVector&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(EndRoleLbcTaskOperation, &URoleLbcTaskInterface::EndRoleLbcTaskOperation)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowLbcStartTrainWnd, &URoleLbcTaskInterface::ShowLbcStartTrainWnd)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowLbcTaskResult, &URoleLbcTaskInterface::ShowLbcTaskResult, const int32&, const FString&, const int32&, const int32&, const int32&, const FString&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleLbcTaskInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()



void URoleLbcTaskInterface::InitBlueCB()
{
	//ArrBlueFunc.Add("LbcTaskCreateBody");
	Supper::InitBlueCB();
}

void URoleLbcTaskInterface::OpenLbcTaskUI(int32 type)
{
	FString tempTips = "";
	int32 tempRewardExp = 0;
	if (LBCTaskDatas.Num() <= 0)
	{
		LoadLBCTaskDatas();
	}
	for (auto LBCTask : LBCTaskDatas)
	{
		if (LBCTask->level == type)
		{
			tempTips = LBCTask->tips;
			tempRewardExp = LBCTask->rewardExp;
		}
	}
	//打开练兵任务界面
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TrainSoldierTask"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnOpenTrainSoldierGroundTask.Broadcast(tempTips, tempRewardExp);
	}
}

void URoleLbcTaskInterface::AcceptLbcTask()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLBCTaskInterface::LbcTaskStartPlay : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("acceptLbcTask"), args);
}

void URoleLbcTaskInterface::ShowLbcStartTrainWnd()
{
	//通知UI显示开始练兵界面
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("LBCStartTrain"));
	}
}

void URoleLbcTaskInterface::LbcTaskStartPlay()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleLBCTaskInterface::LbcTaskStartPlay : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("lbcTaskStartPlay"), args);
}


void URoleLbcTaskInterface::RoleMoveToLocation(const  KBEngine::FVariantArray& posList, const float& moveSpeed, const float& dis)
{
	pointList.Empty();
	for (auto& it : posList)
	{
		FVector t_pos = it.GetValue<FVector>();
		pointList.Add(t_pos);
	}
	rolemoveSpeed = moveSpeed;
	RoleDistance = dis;
	RoleMoveToPoint(true);

}

void URoleLbcTaskInterface::StartRoleLbcTaskOperation(const float& armLength, const FVector& cameraRotation)
{
	if (armLength>0)
	{
		NewarmLength = armLength;
		NewcameraRotation = cameraRotation;
	}
	if (UGolbalBPFunctionLibrary::GUIManager()->GetWindow("SkillBar")->IsValidLowLevel())
	{
		UGolbalBPFunctionLibrary::GUIManager()->GetWindow("SkillBar")->Hide();
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if (!IsValid(AtkStateMar))
	{
		return;
	}
	AtkStateMar->SwitchTrainSoldierMode(true, NewarmLength, NewcameraRotation);
	
}

void URoleLbcTaskInterface::EndRoleLbcTaskOperation()
{
	if (UGolbalBPFunctionLibrary::GUIManager()->GetWindow("SkillBar")->IsValidLowLevel())
	{
		UGolbalBPFunctionLibrary::GUIManager()->GetWindow("SkillBar")->Show("SkillBar");
	}

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if (!IsValid(AtkStateMar))
	{
		return;
	}
	AtkStateMar->SwitchTrainSoldierMode(false);
}

void URoleLbcTaskInterface::RPC_RoleMoveToLocationOver()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RoleMoveToLocationOver : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("roleMoveToLocationOver"), args);
}

void URoleLbcTaskInterface::LoadLBCTaskDatas()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (IsValid(CfgManager))
	{
		const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_LBC_TASK);
		if (IsValid(ConfigTable))
		{
			ConfigTable->GetAllRows(LBCTaskDatas);
		}
	}
}

void URoleLbcTaskInterface::RoleMoveToPoint(bool firstOne, bool IsNext)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	//初始化数据
	if (pointList.Num() <= 0) return;
	if (!IsValid(PlayerCharacter))return;
	if (firstOne)
	{
		PlayerCharacter->SetMaxWalkSpeed(rolemoveSpeed);
		CurPlayerMoveSpeed = PlayerCharacter->GetCharacterMovement()->MaxWalkSpeed;
		
		posIndex = 0;
	}
	else
	{
		if (IsNext)
		{
			posIndex += 1;
		}
	}
	if (posIndex == pointList.Num())
	{
		posIndex = 0;
		RPC_RoleMoveToLocationOver();
		PlayerCharacter->SetMaxWalkSpeed(CurPlayerMoveSpeed);
		return;
	}

	FVector pos = pointList[posIndex];
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	TWeakObjectPtr<URoleLbcTaskInterface> DelayThisPtr(this);
	PlayerController->TraceTargetPostion(pos, RoleDistance,
		FTraceCallback::CreateLambda([DelayThisPtr, PlayerCharacter](bool IsSuccess)
			{
				if (DelayThisPtr.IsValid() && IsSuccess)
				{
					if (IsValid(UUECS3GameInstance::Instance))
					{
						UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(PlayerCharacter, DelayThisPtr->DelayMoveEventHandle, FTimerDelegate::CreateLambda([DelayThisPtr]()
							{
								DelayThisPtr->RoleMoveToPoint(false);
							}), 0.1f, false);
					}
				}
			}));
}

void URoleLbcTaskInterface::onLeaveWorld()
{
	LBCTaskDatas.Empty();
}

void URoleLbcTaskInterface::ShowLbcTaskResult(const int32& result, const FString& fistGuardScriptID, const int32& exp, const int32& addExp, const int32& lossNum, const FString& cmdrerScriptID)
{
	//打开战报详情界面
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TrainSoldierWarReport"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowLbcTaskResult.Broadcast(result, fistGuardScriptID, exp, addExp, lossNum, cmdrerScriptID);
	}
}

void URoleLbcTaskInterface::LbcTaskCreateBody(const FString& model, const int32& amount, const float& radius, const FVector& centerPos)
{
	LbcTaskCreateBodyBP(model, amount, radius, centerPos);
}

CONTROL_COMPILE_OPTIMIZE_END