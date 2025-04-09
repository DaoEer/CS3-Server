
#include "QTEManager.h"
#include "GameData/QTEDate.h"
#include"Chuangshi.h"
#include "TimerManager.h"
#include "StoryManager.h"
#include "ParticleManager.h"
#include "CustomTimerManager.h"
#include "Kismet/KismetMathLibrary.h"
#include "Interface/Role/RoleQTEInterface.h"
#include "LevelSequenceActor.h"
#include "GameDevelop/CS3GameInstance.h"
#include "AudioManager.h"
#include "Interface/Role/RoleSpaceContentInterface.h"
#include "Manager/CfgManager.h"
#include "GameDevelop/CS3PlayerController.h"
#include "GameData/ShortcutKey.h"
#include "EventManager.h"
#include "CS3Base/BaseWindow.h"
#include "CS3Base/UIManager.h"

CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("OnContinueCheckRandomKey"), STAT_OnContinueCheckRandomKey, STATGROUP_QTEManager);
DECLARE_CYCLE_STAT(TEXT("OnStartQTEEventType"), STAT_OnStartQTEEventType, STATGROUP_QTEManager);
DECLARE_CYCLE_STAT(TEXT("ImplementQTETypeEvent"), STAT_ImplementQTETypeEvent, STATGROUP_QTEManager);
DECLARE_CYCLE_STAT(TEXT("ResetContinueRandomKey"), STAT_ResetContinueRandomKey, STATGROUP_QTEManager);

UQTEManager::UQTEManager()
{
	OnResetQTEDate();
}

UQTEManager::~UQTEManager()
{

}

UQTEManager* UQTEManager::GetInstance()
{
	cs3_checkNoReentry();
	return (UQTEManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_QTEManager")));
}

void UQTEManager::OnStartQTEEvent(FString TableRowName)
{
	//获取配置数据
	auto QTETable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_QTE_DATA);
	const FQTE_DATE* qteData = QTETable->GetRow<FQTE_DATE>(TableRowName);
	if (qteData!=nullptr)
	{
		QTETypeDataArray = qteData->QTEData;
		QTEIndex = 0;
		if (QTETypeDataArray.Num() > 0)
		{
			OnResetQTEDate();
			OnStartQTESetTimer();
			ImplementQTETypeEvent(QTE_COMPLETE_TYPE::START_EVENT);
		}
	}
}

void UQTEManager::OnStartQTESetTimer()
{
	FQTE_TYPE_DATA  QTEType = QTETypeDataArray[QTEIndex];
	if (QTEType.QTEEventData.Num() > 0)
	{
		QTEEventDataArray.Empty();
		QTEEventDataArray = QTEType.QTEEventData;
	}
	if (QTEType.QTEType == QTE_TYPE::MOBILE_MOUSE)
	{
		OnCreatOperation(1);
		Mouseistrue = true;
		TWeakObjectPtr<UQTEManager> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(CheckQTEEventHandle, this, &UQTEManager::OnCheckQTEEvent, 0.01f, true);
	}
	else if (QTEType.QTEType == QTE_TYPE::KEYBOARD_KEYS)
	{
		OnKeyInputEvent.AddDynamic(this, &UQTEManager::OnCheckKey);

	}
	else if (QTEType.QTEType == QTE_TYPE::CONTINUITY_KEYBOARD)
	{
		ContinueInedx = 0;
		ContinueKeyList.Reset();
		ContinueName = "";
		OnKeyInputEvent.Clear();
		FString Keys = (QTEType.Param1 == "") ? "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z" : QTEType.Param1;
		TArray<FString> KeyList = UGolbalBPFunctionLibrary::SplitString(Keys);
		TArray<FString> RandomIntegerList = UGolbalBPFunctionLibrary::SplitString(QTEType.Param3);
		int32 RandomIntegerMin = ((RandomIntegerList.Num() > 0) && (FSTRING_TO_INT(RandomIntegerList[0]) > -1) && (FSTRING_TO_INT(RandomIntegerList[0]) < KeyList.Num()) ? FSTRING_TO_INT(RandomIntegerList[0]) : KeyList.Num());
		int32 RandomIntegerMax = ((RandomIntegerList.Num() > 1) && (FSTRING_TO_INT(RandomIntegerList[1]) > -1) && (FSTRING_TO_INT(RandomIntegerList[1]) < KeyList.Num()) ? FSTRING_TO_INT(RandomIntegerList[1]) : KeyList.Num());
		if (bool(FSTRING_TO_INT(QTEType.Param2)) || QTEType.Param2 == "")
		{
			int32 KeyListCount = UKismetMathLibrary::RandomIntegerInRange(RandomIntegerMin, RandomIntegerMax);
			int32 keyRandomInRangeMax = (QTEType.Param3 == "") ? 4 : (KeyList.Num() - 1);
			for (int i = 0; i < KeyListCount; i++)
			{
				FString KeyNum = KeyList[UKismetMathLibrary::RandomInteger(keyRandomInRangeMax)];
				ContinueKeyList.Add(KeyNum);
				if (i == (KeyListCount - 1))
				{
					ContinueName += KeyNum;
				}
				else
				{
					ContinueName += KeyNum + "|";
				}
			}
			if(QTEType.Param3 == "")
			{
				OnKeyInputEvent.AddDynamic(this, &UQTEManager::OnContinueCheckKey);
			}
			else
			{
				OnKeyInputEvent.AddDynamic(this, &UQTEManager::OnContinueCheckRandomKey);
			}
			
		}
		else
		{
			for (FString key : KeyList)
			{
				ContinueKeyList.Add(key);
			}
			ContinueName = QTEType.Param1;
			OnKeyInputEvent.AddDynamic(this, &UQTEManager::OnContinuityKeyboard);
		}
		SetContinueRandomKeyActionEnable(true);
	}
	else if (QTEType.QTEType == QTE_TYPE::DEFAULT_Mode)
	{
	}
	if (FMath::IsNearlyZero(QTEType.QTESurvivalTime))
	{
		ImplementQTETypeEvent(QTE_COMPLETE_TYPE::END_EVENT);
	}
	else if (QTEType.QTESurvivalTime > 0)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayQTEEventHandle, this, &UQTEManager::OnDeathQTEEvent, QTEType.QTESurvivalTime, false);
	}
}

void UQTEManager::OnCheckKey(FKey Key)
{
	FQTE_TYPE_DATA  QTEType = QTETypeDataArray[QTEIndex];
	if (QTEType.Param1.IsEmpty())
	{
		TArray<FString> KeyList = UGolbalBPFunctionLibrary::SplitString(QTEType.Param1);
		if (KeyList.Num() > 0)
		{
			if (Key.GetDisplayName().ToString() == KeyList[0])
			{
				ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result1_EVENT);
			}
			else if (Key.GetDisplayName().ToString() == KeyList[1])
			{
				ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result2_EVENT);
			}
			else if (Key.GetDisplayName().ToString() == KeyList[2])
			{
				ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result3_EVENT);
			}
			else
			{
				ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result4_EVENT);
			}
		}
		KeyValue = Key;
		OnKeyInputEvent.Clear();
	}
}

void UQTEManager::OnContinueCheckKey(FKey Key)
{
	KeyValue = Key;
	FQTE_TYPE_DATA  QTEType = QTETypeDataArray[QTEIndex];
	if (!QTEType.Param1.IsEmpty())
	{
		if (ContinueKeyList.Num() > 0)
		{
			if (Key.GetDisplayName().ToString() == ContinueKeyList[ContinueInedx])
			{
				if(ContinueKeyList.Num()-1 == ContinueInedx)
				{
					ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result1_EVENT);
					ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result3_EVENT);
					OnKeyInputEvent.Clear();
					SetContinueRandomKeyActionEnable(false);
					return ;
				}
				ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result1_EVENT);
				ContinueInedx += 1;
			}
			else
			{
				ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result2_EVENT);
			}
		}
	}
}

void UQTEManager::OnContinueCheckRandomKey(FKey Key)
{
	SCOPE_CYCLE_COUNTER(STAT_OnContinueCheckRandomKey);
	KeyValue = Key;
	FQTE_TYPE_DATA  QTEType = QTETypeDataArray[QTEIndex];

	if (ContinueKeyList.Num() > 0)
	{
		if (Key.GetDisplayName().ToString() == ContinueKeyList[ContinueInedx])
		{
			if (ContinueKeyList.Num() - 1 == ContinueInedx)
			{
				ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result1_EVENT);
				ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result3_EVENT);
				OnKeyInputEvent.Clear();
				SetContinueRandomKeyActionEnable(false);
				return;
			}
			ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result1_EVENT);
			ContinueInedx += 1;
		}
		else
		{
			TArray<FString> RandomIntegerList = UGolbalBPFunctionLibrary::SplitString(QTEType.Param3);
			if (RandomIntegerList.Num() == 3)
			{
				//按错规则
				int32 Result = FSTRING_TO_INT(RandomIntegerList[2]);
				switch (Result)
				{
				case 1:///<全部键重来，QTE不结束，恢复前面按对的字符状态，重新从第一个开始
					ContinueInedx = 0;
					ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result2_EVENT);
					break;
				case 2:///<不重来，QTE结束
					ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result4_EVENT);
					break;
				case 3:///<重新生成随机字符串，QTE不结束
					ResetContinueRandomKey(QTEType);
					ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result2_EVENT);
					break;
				case 4:///<当前键重来，QTE不结束，字符不刷新，进度不变
					ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result2_EVENT);
					break;
				default:///<（缺省默认1）全部键重来，QTE不结束，恢复前面按对的字符状态，重新从第一个开始
					ContinueInedx = 0;
					ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result2_EVENT);
					break;
				}
			}
			else///<（缺省默认1）按全部键重来，QTE不结束，恢复前面按对的字符状态，重新从第一个开始
			{
				ContinueInedx = 0;
				ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result2_EVENT);
			}
		}
	}
}

void UQTEManager::OnContinuityKeyboard(FKey Key)
{
	if (!Key.IsMouseButton())
	{
		KeyValue = Key;
		FQTE_TYPE_DATA  QTEType = QTETypeDataArray[QTEIndex];
		if (!QTEType.Param1.IsEmpty())
		{
			if (ContinueKeyList.Num() > 0)
			{
				if (Key.GetDisplayName().ToString() == ContinueKeyList[ContinueInedx])
				{
					if (ContinueKeyList.Num() - 1 == ContinueInedx)
					{
						ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result1_EVENT);
						ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result3_EVENT);
						OnKeyInputEvent.Clear();
						SetContinueRandomKeyActionEnable(false);
						return;
					}
					ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result1_EVENT);
					ContinueInedx += 1;
				}
				else
				{
					ContinueInedx = 0;
					ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result2_EVENT);
				}
			}
		}
	}
}

void UQTEManager::OnCheckQTEEvent()
{
	
	if (IsValid(Operation))
	{
		if (Mouseistrue)
		{
			QTEValue = Operation->ExecuteOperation();
			if (QTEValue >= 1.0f)
			{
				Mouseistrue = false;
				ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result1_EVENT);
			}
		}
	}
}

void UQTEManager::OnDeathQTEEvent()
{
	OnClearTimer();
	FQTE_TYPE_DATA  QTEType = QTETypeDataArray[QTEIndex];
	if (QTEType.QTEType == QTE_TYPE::MOBILE_MOUSE)
	{
		if (QTEValue >= 1.0f)
		{
			ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result1_EVENT);
		}
		else
		{
			ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result2_EVENT);
		}
	}else if (QTEType.QTEType == QTE_TYPE::KEYBOARD_KEYS)
	{
		OnKeyInputEvent.Clear();
		ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result2_EVENT);
	}
	else if(QTEType.QTEType == QTE_TYPE::CONTINUITY_KEYBOARD)
	{
		if (OnKeyInputEvent.IsBound())
		{
			OnKeyInputEvent.Clear();
			SetContinueRandomKeyActionEnable(false);
			if (!bool(FSTRING_TO_INT(QTEType.Param2)))
			{
				if (ContinueInedx < ContinueKeyList.Num())
				{
					ImplementQTETypeEvent(QTE_COMPLETE_TYPE::Result4_EVENT);
				}
			}

		}
	}
	else if (QTEType.QTEType == QTE_TYPE::DEFAULT_Mode)
	{
	}
	ImplementQTETypeEvent(QTE_COMPLETE_TYPE::END_EVENT);

}

void UQTEManager::OnStopQTEEvent()
{
	OnResetQTEDate();
	if (QTEIndex < QTETypeDataArray.Num())
	{
		OnStartQTESetTimer();
		ImplementQTETypeEvent(QTE_COMPLETE_TYPE::START_EVENT);
	}
	else
	{
		QTEIndex = 0;
	}
}

void UQTEManager::OnStartQTEEventType(FQTE_EVENT_DATA QTEEventData)
{
	SCOPE_CYCLE_COUNTER(STAT_OnStartQTEEventType);
	if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::BOSSDEMO_EVENT)
	{
			OnCellCall(bool(FSTRING_TO_INT(QTEEventData.Param1)));
			OnBPNotifyClinetQTEResult(bool(FSTRING_TO_INT(QTEEventData.Param1)), FSTRING_TO_FLOAT(QTEEventData.Param2));

	}else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::BOSSDEMO_PROGRESS)
	{
			ShowWobbleMouseBar(bool(FSTRING_TO_INT(QTEEventData.Param1)));
			ShowHPProgressBar(FSTRING_TO_INT(QTEEventData.Param1), 0, 100);
			if (FSTRING_TO_INT(QTEEventData.Param1))
			{
				OnBPStartQTEEvent();
			}
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::CAMERA_EVENT)
	{
		UGStoryManager* GStroryManager = UGolbalBPFunctionLibrary::GStoryManager();
		if (IsValid(GStroryManager))
		{
			if (QTEEventData.Param2.IsEmpty())
			{
				GStroryManager->PlaySequence(QTEEventData.Param1, 1);
			}
			GStroryManager->PlaySequence(QTEEventData.Param1, FSTRING_TO_INT(QTEEventData.Param2));
		}
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::INTERNALJUMP_EVENT)
	{
		QTEIndex = FSTRING_TO_INT(QTEEventData.Param1);
		OnStopQTEEvent();
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::CUSTOM_EVENT)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Custom_Event is start"));
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::PLAYEFFECT_EVENT)
	{
		AActor* Player = Cast<AActor>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		UUECS3GameInstance::Instance->ParticleManager->PlayParticle(QTEEventData.Param1, 0.0f, Player, Player);
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::RETREAT_EVENT)
	{
		FQTE_TYPE_DATA  QTEType = QTETypeDataArray[QTEIndex];
		if (QTEType.QTEType == QTE_TYPE::MOBILE_MOUSE)
		{
			URoleQTEInterface * RoleQTEInterface = Cast<URoleQTEInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleQTEInterface")));
			if (RoleQTEInterface)
			{
				RoleQTEInterface->onCompleteBuffQTE();
			}
		}
		ImplementQTETypeEvent(QTE_COMPLETE_TYPE::END_EVENT);
		QTEIndex = QTETypeDataArray.Num() +1 ;
		OnStopQTEEvent();
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::LENSKEY_EVENT)
	{
		UGStoryManager* GStroryManager = UGolbalBPFunctionLibrary::GStoryManager();
		if (IsValid(GStroryManager))
		{
			if (QTEEventData.Param3 == "1")
			{
				GStroryManager->PlayAnimEventByParam(QTEEventData.Param1, FSTRING_TO_FLOAT(QTEEventData.Param2), true);
			}
			else
			{
				GStroryManager->PlayAnimEventByParam(QTEEventData.Param1, FSTRING_TO_INT(QTEEventData.Param2),false);
			}
		}
	}else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::HAOLINGGUUI_EVENT)
	{
		FQTE_TYPE_DATA  QTEType = QTETypeDataArray[QTEIndex];
		if (IsValid(UUECS3GameInstance::Instance))
		{
			if (IsValid(UUECS3GameInstance::Instance->GUIManager))
			{
				if (QTEEventData.Param1 == TEXT("1"))//打开
				{
					UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("HaoLingGuQTE"));
					if (IsValid(UUECS3GameInstance::Instance->GEventManager))
					{
						UUECS3GameInstance::Instance->GEventManager->OnShowHaoLinGuUIEvent.Broadcast(QTEType.QTESurvivalTime, ContinueName);
					}
				}
				else//关闭
				{
					UBaseWindow *HaoLingGuQTE = UUECS3GameInstance::Instance->GUIManager->GetWindow(TEXT("HaoLingGuQTE"));
					if (IsValid(HaoLingGuQTE))
					{
						HaoLingGuQTE->Hide();
					}
				}
			}
		}
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::HAOLINGGUKEY_EVENT)
	{
		if (KeyValue.IsValid())
		{
			FQTE_TYPE_DATA  QTEType = QTETypeDataArray[QTEIndex];
			if (QTEEventData.QTEComplete == QTE_COMPLETE_TYPE::Result1_EVENT)//成功
			{
				if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
				{
					UUECS3GameInstance::Instance->GEventManager->OnHaoLinGuKeyBackEvent.Broadcast(0, KeyValue.GetDisplayName().ToString(), ContinueInedx);
				}
			}
			else if (QTEEventData.QTEComplete == QTE_COMPLETE_TYPE::Result2_EVENT)//失败
			{
				//顺序随机
				if (bool(FSTRING_TO_INT(QTEType.Param2)) || QTEType.Param2 == "")
				{
					TArray<FString> RandomIntegerList = UGolbalBPFunctionLibrary::SplitString(QTEType.Param3);
					//1（缺省默认1）全部键重来，2不重来，3重新生成随机字符串，4当前键重来
					if (RandomIntegerList.Num() == 3)
					{
						int32 Result = FSTRING_TO_INT(RandomIntegerList[2]);
						switch (Result)
						{
						case 1://刷新字符串（字符串不变，状态变化）
						case 3://刷新字符串（字符串重新生成）
							if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
							{
								UUECS3GameInstance::Instance->GEventManager->OnHaoLinGuUpdateAllKeysEvent.Broadcast(ContinueName);
							}
						default://不处理字符串
							break;
						}
					}
					else//（缺省默认1）全部键重来，刷新字符串（字符串不变，状态变化）
					{
						if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
						{
							UUECS3GameInstance::Instance->GEventManager->OnHaoLinGuUpdateAllKeysEvent.Broadcast(ContinueName);
						}
					}
				}
				//顺序固定
				else
				{
					//全部键重来，刷新字符串（字符串不变，状态变化）
					if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
					{
						UUECS3GameInstance::Instance->GEventManager->OnHaoLinGuUpdateAllKeysEvent.Broadcast(ContinueName);
					}
				}
			}
		}
// 		else
// 		{
// 			if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
// 			{
// 				UUECS3GameInstance::Instance->GEventManager->OnHaoLinGuKeyBackEvent.Broadcast(1, "", ContinueInedx);
// 			}
// 		}
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::PLAYSOUND_EVENT)
	{ 
		UGolbalBPFunctionLibrary::AudioManager()->AnalysisVoiceData(QTEEventData.Param1);
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::LENSKEYRATE_EVENT)
	{
		UGStoryManager* GStroryManager = UGolbalBPFunctionLibrary::GStoryManager();
		if (IsValid(GStroryManager))
		{
			GStroryManager->SetPlayRate(FSTRING_TO_FLOAT(QTEEventData.Param1));
		}
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::CELLCALL_EVENT)
	{
		OnCellCall(bool(FSTRING_TO_INT(QTEEventData.Param1)));
	}
	else if (QTEEventData.QTEEventType == QTE_EVENT_TYPE::SERVERCALL_EVENT)
	{
		if (QTEEventData.Param1=="1")
		{
			URoleSpaceContentInterface* RoleSpaceContentInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"), 0));
			if (RoleSpaceContentInterface)
			{
				RoleSpaceContentInterface->RPC_onCompleteQTENotyfy(FSTRING_TO_INT(QTEEventData.Param2));
			}
		}
	}
}

void UQTEManager::ImplementQTETypeEvent(QTE_COMPLETE_TYPE QTECompleteType)
{
	SCOPE_CYCLE_COUNTER(STAT_ImplementQTETypeEvent);
	for (TArray<FQTE_EVENT_DATA>::TConstIterator It(QTEEventDataArray); It; ++It)
	{
		if (It->QTEComplete == QTECompleteType)
		{
			OnStartQTEEventType(*It);
		}
	}
}

void UQTEManager::OtherShowQTE()
{
	OnBPOtherShowQTE();
}

void UQTEManager::ShowHPProgressBar(uint8 bIsShow, int32 Percent, int32 HurtPercent)
{
	OnBPShowHPProgressBar(bIsShow, Percent, HurtPercent);
}

void UQTEManager::OnCellCall(bool bIsSuccess)
{
	URoleQTEInterface * RoleQTEInterface = Cast<URoleQTEInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleQTEInterface")));
	if (RoleQTEInterface)
	{
		RoleQTEInterface->onCompleteQTEBuffEvent(bIsSuccess);
	}
}

void UQTEManager::OnCreatOperation(int32 QteType)
{
	UMouseQTEOperation*  MOperation = NewObject<UMouseQTEOperation>();
	if (IsValid(MOperation))
	{
		Operation = MOperation;
	}
}

void UQTEManager::OnResetQTEDate()
{
	OnClearTimer();
	Operation = nullptr;
	QTEValue = 0.0f;
	if (OnKeyInputEvent.IsBound())
	{
		OnKeyInputEvent.Clear();
		SetContinueRandomKeyActionEnable(false);
	}
}

void UQTEManager::OnClearTimer()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (CheckQTEEventHandle.IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CheckQTEEventHandle);
		}
		if (StopQTEEventHandle.IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(StopQTEEventHandle);
		}
		if (DelayQTEEventHandle.IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayQTEEventHandle);
		}
	}
}

void UQTEManager::ResetContinueRandomKey(FQTE_TYPE_DATA QTEType)
{
	SCOPE_CYCLE_COUNTER(STAT_ResetContinueRandomKey);
	ContinueInedx = 0;
	ContinueKeyList.Reset();
	ContinueName = "";
	FString Keys = (QTEType.Param1 == "") ? "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z" : QTEType.Param1;
	TArray<FString> KeyList = UGolbalBPFunctionLibrary::SplitString(Keys);
	TArray<FString> RandomIntegerList = UGolbalBPFunctionLibrary::SplitString(QTEType.Param3);
	int32 RandomIntegerMin = ((RandomIntegerList.Num() > 0) && (FSTRING_TO_INT(RandomIntegerList[0]) > -1) && (FSTRING_TO_INT(RandomIntegerList[0]) < KeyList.Num()) ? FSTRING_TO_INT(RandomIntegerList[0]) : KeyList.Num());
	int32 RandomIntegerMax = ((RandomIntegerList.Num() > 1) && (FSTRING_TO_INT(RandomIntegerList[1]) > -1) && (FSTRING_TO_INT(RandomIntegerList[1]) < KeyList.Num()) ? FSTRING_TO_INT(RandomIntegerList[1]) : KeyList.Num());

	int32 KeyListCount = UKismetMathLibrary::RandomIntegerInRange(RandomIntegerMin, RandomIntegerMax);
	int32 keyRandomInRangeMax = KeyList.Num() - 1;
	for (int i = 0; i < KeyListCount; i++)
	{
		FString KeyNum = KeyList[UKismetMathLibrary::RandomInteger(keyRandomInRangeMax)];
		ContinueKeyList.Add(KeyNum);
		if (i == (KeyListCount - 1))
		{
			ContinueName += KeyNum;
		}
		else
		{
			ContinueName += KeyNum + "|";
		}
	}
}

void UQTEManager::SetContinueRandomKeyActionEnable(bool Enable)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_STORY, Enable);
	}
}

CONTROL_COMPILE_OPTIMIZE_END
