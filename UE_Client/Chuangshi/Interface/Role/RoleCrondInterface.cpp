// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleCrondInterface.h"
//插件
#include "JsonFieldData.h"
#include "Entity/Alias.h"
//CS3数据
#include "GameData/MessageID.h"
#include "GameData/CrondDatas.h"
#include "GameData/EnumCsvDefine.h"
//CS3
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Manager/CfgManager.h"
#include "Manager/MessageManager.h"
#include "Manager/MapManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleCrondInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(receiveCrondRemindData, &URoleCrondInterface::receiveCrondRemindData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recviveTodayActivitiesData, &URoleCrondInterface::recviveTodayActivitiesData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recviveUpdateTodayActivitiesData, &URoleCrondInterface::recviveUpdateTodayActivitiesData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(receiveWeekActivitiesData, &URoleCrondInterface::receiveWeekActivitiesData, const FVariantArray&, const uint8&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recvActivityTimesData, &URoleCrondInterface::recvActivityTimesData, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(updateActivityTimesData, &URoleCrondInterface::updateActivityTimesData, const int32&, const int32&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleCrondInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleCrondInterface::URoleCrondInterface()
{
}

URoleCrondInterface::~URoleCrondInterface()
{
}

void URoleCrondInterface::SetCrondRemindSettingData(const FString& scriptID, CROND_REMIND_TYPE remindType)
{
	if (scriptID == "") return;

	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleCrondInterface::SetCrondRemindSettingData no this Entity!"));
		return;
	}

	if (CrondRemindSettingDatas.Contains(scriptID))
	{
		CrondRemindSettingDatas[scriptID].remindType = remindType;
		KBEngine::FVariantArray args;
		args.Add(scriptID);
		args.Add((uint8)remindType);
		entity->BaseCall(TEXT("requestSetCrondRemind"), args);
	}
}

TArray<FCrondRemindSettingData> URoleCrondInterface::GetCrondRemindSettingDatas()
{
	TArray<FCrondRemindSettingData> datas;
	if (CrondRemindSettingDatas.Num() < CrondConfigDatas.Num())
	{
		for (const FNewCrondConfigData* CrondConfigData : CrondConfigDatas)
		{
			if (CrondConfigData != nullptr)
			{
				FCrondRemindSettingData data;
				if (GetCrondRemindSettingData(CrondConfigData->scriptID, data))
				{
					datas.Add(data);
				}
			}
		}
	}

	CrondRemindSettingDatas.GenerateValueArray(datas);
	return datas;
}

bool URoleCrondInterface::GetCrondRemindSettingData(const FString& scriptID, FCrondRemindSettingData& OutRemindSettingData)
{
	SetCrondRemindDefault(scriptID);

	if (CrondRemindSettingDatas.Contains(scriptID))
	{
		OutRemindSettingData = CrondRemindSettingDatas[scriptID];
		return true;
	}
	return false;
}

void URoleCrondInterface::RPC_requestCrondRemindData()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleCrondInterface::RPC_requestCrondRemindData no this Entity!"));
		return;
	}
	if (CrondRemindSettingDatas.Num()>0)
	{
		return;//有数据则不需要请求
	}
	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("requestCrondRemindData"), args);
}

void URoleCrondInterface::receiveCrondRemindData(const FVariant& datas)
{
	REMIND_CROND_DATAS* _datas = new REMIND_CROND_DATAS(datas);
	for (auto d : _datas->datas)
	{
		const FNewCrondConfigData* crondConfigData = GetNewCrondConfigData(d.scriptID);
		if (crondConfigData != nullptr)
		{
			FCrondRemindSettingData data;
			data.scriptID = crondConfigData->scriptID;
			data.name = crondConfigData->crondName;
			data.time = crondConfigData->timeSlot;
			data.remindType = (CROND_REMIND_TYPE)(d.remindType);
			if (CrondRemindSettingDatas.Contains(data.scriptID))
				CrondRemindSettingDatas.Remove(data.scriptID);
			CrondRemindSettingDatas.Add(data.scriptID, data);
		}
	}
	BP_ReceiveCrondRemind();
}

void URoleCrondInterface::SetCrondRemindDefault(FString scriptID)
{
	if (CrondRemindSettingDatas.Contains(scriptID))
		return;

	const FNewCrondConfigData* crondConfigData = GetNewCrondConfigData(scriptID);
	if (crondConfigData != nullptr)
	{
		FCrondRemindSettingData data;
		data.scriptID = crondConfigData->scriptID;
		data.name = crondConfigData->crondName;
		data.time = crondConfigData->timeSlot;
		data.remindType = CROND_REMIND_TYPE::Before_TenMinutes;
		CrondRemindSettingDatas.Add(scriptID, data);
	}
}

void URoleCrondInterface::RPC_RequestTodayActivitiesData()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleCrondInterface::RPC_RequestTodayActivitiesData no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("requestTodayActivitiesData"), args);
}

void URoleCrondInterface::recviveTodayActivitiesData(const FVariant& activityCronds)
{
	InitLoadCrondConfigDatas();
	FACTIVITIES_DATA_DICT data = FACTIVITIES_DATA_DICT(activityCronds);
	todayDatas.date = data.month + TEXT("月") + data.day + TEXT("日");
	todayDatas.wday = FSTRING_TO_INT(data.wday);

	for (auto _data : data.table)
	{
		FCrondData CrondData = getParseCrondData(todayDatas.date, todayDatas.wday, _data);
		todayDatas.crondDatas.Add(CrondData.scriptID, CrondData);
	}
	BP_RefreshCrondDatasForWDay();
}

void URoleCrondInterface::recviveUpdateTodayActivitiesData(const FVariant& activityCronds)
{
	FACTIVITIES_DATA_DICT data = FACTIVITIES_DATA_DICT(activityCronds);
	int32 wday = FSTRING_TO_INT(data.wday);
	if (todayDatas.wday == wday)
	{
		for (auto _data : data.table)
		{
			FCrondData CrondData = getParseCrondData(todayDatas.date, todayDatas.wday, _data);
			if (todayDatas.crondDatas.Contains(CrondData.scriptID))
				todayDatas.crondDatas.Remove(CrondData.scriptID);
			todayDatas.crondDatas.Add(CrondData.scriptID, CrondData);
		}
	}
	BP_RefreshCrondDatasForWDay();
}

void URoleCrondInterface::RPC_RequestWeekActivitiesData()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleCrondInterface::RPC_RequestWeekActivitiesData no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("requestWeekActivitiesData"), args);
}

void URoleCrondInterface::receiveWeekActivitiesData(const FVariantArray& activityCronds, const uint8& clearDataFlag)
{
	if (clearDataFlag != 0)
	{
		InitLoadCrondConfigDatas();
		nextSixDayDatas.Empty();

		for (auto it : activityCronds)
		{
			FACTIVITIES_DATA_DICT data = FACTIVITIES_DATA_DICT(it);
			FDayCrondData dayCrondData;
			dayCrondData.date = data.month + TEXT("月") + data.day + TEXT("日");
			dayCrondData.wday = FSTRING_TO_INT(data.wday);

			for (auto _data : data.table)
			{
				FCrondData CrondData = getParseCrondData(dayCrondData.date, dayCrondData.wday, _data);
				dayCrondData.crondDatas.Add(CrondData.scriptID, CrondData);
			}
			nextSixDayDatas.Add(dayCrondData);
		}
	}
	BP_RefreshCrondDatasForWDay();
}

FCrondData URoleCrondInterface::getParseCrondData(const FString& date, const int32& wday, const FACTIVITY_DATA_DICT& data)
{
	FCrondData CrondData;
	CrondData.scriptID = data.scriptID;
	CrondData.date = date;
	CrondData.wday = wday;

	if (GetNewCrondConfigData(CrondData.scriptID) == nullptr) return CrondData;
	CrondData.crondConfig = *GetNewCrondConfigData(CrondData.scriptID);
	
	for (auto crond : data.crondList)
	{
		FCrondActivityStatus activityStatus;
		activityStatus.status = (ACTIVE_STATUS)crond.status;
		activityStatus.startTime = crond.nextStartTime;
		activityStatus.statusInfo = crond.timeTxt;
		CrondData.status.Add(activityStatus);

		if (activityStatus.status == ACTIVE_STATUS::ACTIVE_STATUS_ALL_DAY)
		{
			CrondData.curStatus.status = activityStatus.status;
			CrondData.curStatus.statusInfo == "全天开放";
		}
		else if (activityStatus.status == ACTIVE_STATUS::ACTIVE_STATUS_ACTIVATING)
		{
			CrondData.curStatus.status = activityStatus.status;
			CrondData.curStatus.statusInfo == "正在进行";
		}
		else
		{
			if (CrondData.curStatus.startTime <= 0 || activityStatus.startTime < CrondData.curStatus.startTime)
				CrondData.curStatus = activityStatus;
		}
	}
	return CrondData;
}

TArray<int32> URoleCrondInterface::GetCrondRewardList(const FString& InRewardStr, TArray<int32>& ItemNumList)
{
	//物品ID:物品数量|....
	TArray<FString> tempStrList = UGolbalBPFunctionLibrary::SplitString(InRewardStr, true, TEXT("|"));
	TArray<int32> tempItemList;
	TArray<int32> tempItemNumList;
	for (auto str : tempStrList)
	{
		bool Result = true;
		FString Left, Right;
		Result = str.Split(TEXT(":"), &Left, &Right, ESearchCase::Type::CaseSensitive);
		if (Result)
		{
			tempItemList.Add(FSTRING_TO_INT(Left));
			tempItemNumList.Add(FSTRING_TO_INT(Right));
		}
	}
	return tempItemList;
}

TArray<FCrondData> URoleCrondInterface::GetCrondDatasByActiveType(TArray<int32>& OutActivityJoinTimes, ACTIVE_TYPE ActiveType)
{
	TArray < FCrondData > CrondDatas;
	if (todayDatas.crondDatas.Num() > 0)
	{
		TArray<FCrondData> datas;
		todayDatas.crondDatas.GenerateValueArray(datas);
		TArray<FCrondData> sortDatas = SortCrondDatas(datas);
		for (TArray<FCrondData>::TIterator it = sortDatas.CreateIterator(); it; ++it)
		{
			ACTIVE_TYPE tempActType = it->crondConfig.actType;
			if (tempActType == ActiveType)
			{
				CrondDatas.Add(*it);
				int32 times = 0;
				int32* Value = ActivityJoinTimes.Find(it->scriptID);
				if (Value != nullptr)
				{
					times = *Value;//活动次数
				}
				OutActivityJoinTimes.Add(times);
			}
		}
	}
	return CrondDatas;
}

const FNewCrondConfigData* URoleCrondInterface::GetNewCrondConfigData(const FString scriptID)
{
	if ( CrondConfigDatas.Num() == 0)
	{
		InitLoadCrondConfigDatas();
	}
	for (auto data : CrondConfigDatas)
	{
		if(data->scriptID == scriptID)
			return data;
	}
	return nullptr;
}

void URoleCrondInterface::LoadCrondRewardDatas()
{
	//先初始化
	if (CrondRewardDatas.Num() == 0)
	{
		for (auto data : CrondConfigDatas)
		{
			if (data)
			{
				if (data->rewardType != TEXT(""))
				{
					TArray<FString> idandvalues;
					data->rewardType.ParseIntoArray(idandvalues, TEXT("|"), true);
					for (auto item : idandvalues)
					{
						ACTIVE_REWARD_TYPE _type = (ACTIVE_REWARD_TYPE)FSTRING_TO_INT(item);
						if (!CrondRewardDatas.Contains(_type))
						{
							TArray<FNewCrondConfigData> ids;
							CrondRewardDatas.Add(_type, ids);
						}
						CrondRewardDatas[_type].Add(*data);
					}
				}
			}
		}
	}
}

void URoleCrondInterface::InitLoadCrondConfigDatas()
{
	if (CrondConfigDatas.Num() > 0) return;
	const UConfigTable* table = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_NEW_CONFIG_CROND);
	if (IsValid(table))
	{
		table->GetAllRows<FNewCrondConfigData>(CrondConfigDatas);
	}
}

void URoleCrondInterface::InitLoadWeekCrondConfigDatas()
{
	if (WeekCrondConfigDatas.Num() > 0) return;
	const UConfigTable* table = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_WEEK_CROND_DATA);
	if (IsValid(table))
	{
		TArray<FWeekCrondConfigData*> tempWeekCrondConfigDatas;
		table->GetAllRows<FWeekCrondConfigData>(tempWeekCrondConfigDatas);
		for (auto data : tempWeekCrondConfigDatas)
		{
			WeekCrondConfigDatas.Add(data->wday, data);
		}
	}
}

TArray<FNewCrondConfigData> URoleCrondInterface::GetActivitiesByRewardType(ACTIVE_REWARD_TYPE type)
{
	TArray<FNewCrondConfigData> tempCrondConfigData;
	if (CrondRewardDatas.Num() == 0)
	{
		LoadCrondRewardDatas();
	}
	if (CrondRewardDatas.Contains(type))
		return CrondRewardDatas[type];
	return tempCrondConfigData;
}

TArray<FNewCrondConfigData> URoleCrondInterface::GetActivitiesByCrondType(CROND_TYPE CrondType)
{
	TArray<FNewCrondConfigData> tempCrondConfigData;
	if (CrondConfigDatas.Num() == 0)
	{
		InitLoadCrondConfigDatas();
	}
	for (auto CrondConfigData : CrondConfigDatas)
	{
		if (CrondConfigData && CrondConfigData->crondType == CrondType)
		{
			tempCrondConfigData.Add(*CrondConfigData);
		}
	}
	return tempCrondConfigData;
}
	


void URoleCrondInterface::InitBlueCB()
{
	ArrBlueFunc.Add("receiveCrondRemind");
	Supper::InitBlueCB();
}

void URoleCrondInterface::NavigateToPoint(const FString& scriptID)
{
	if (GetNewCrondConfigData(scriptID) == nullptr) return;
	FString place = GetNewCrondConfigData(scriptID)->place;
	if (!place.IsEmpty())
	{
		TArray<FString> values;
		place.ParseIntoArray(values, TEXT("|"), true);
		if (values.Num() >= 2)
		{
			const FString currentSpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
			//若玩家不在活动NPC所在地图，则弹出相应提示
			if (!currentSpaceScriptID.Equals(values[0]))
			{
				FString dstSpaceName = UUECS3GameInstance::Instance->MapManager->ChangeSpaceScriptIDToAreaName(values[0]);
				if (!dstSpaceName.IsEmpty())
				{
					UUECS3GameInstance::Instance->MessageManager->ShowMessage(5973, dstSpaceName);
					return;
				}
			}
			APlayerCharacter* playerActor = Cast<APlayerCharacter>(GetActor());
			if (IsValid(playerActor))
			{
				playerActor->StartCrossMapNavigate(values[0], false, TEXT(""), values[1], FVector::ZeroVector, 1.0, 0, ENUM_NAVIGATE_ACTION_TYPE::NavigateActionCrond);
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("Crond start navigate!!"));
				return;
			}	
		}
	}
}

void URoleCrondInterface::OnNavigateCrondFinish()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Crond end navigate!!"));

}

void URoleCrondInterface::OnNavigateCrondFail()
{

}

TArray<FCrondData> URoleCrondInterface::SortCrondDatas(TArray<FCrondData> cronds)
{
	TArray<FCrondData> crondDatas;
	for (auto crond : cronds)
	{
		if (crondDatas.Num() <= 0)
		{
			crondDatas.Add(crond);
			continue;
		}

		bool flag = false;
		for (int i = 0; i<crondDatas.Num(); i++)
		{
			//先根据星级进行排序
			if (crondDatas[i].crondConfig.star < crond.crondConfig.star)
			{
				crondDatas.Insert(crond, i);
				flag = true;
				break;
			}

			//根据开放时间进行排序（全天开放的排在最前面）
			if ((crond.curStatus.status == ACTIVE_STATUS::ACTIVE_STATUS_ALL_DAY && crondDatas[i].curStatus.status != ACTIVE_STATUS::ACTIVE_STATUS_ALL_DAY)
				|| (crond.curStatus.status == ACTIVE_STATUS::ACTIVE_STATUS_ACTIVATING && (crondDatas[i].curStatus.status != ACTIVE_STATUS::ACTIVE_STATUS_ALL_DAY && crondDatas[i].curStatus.status != ACTIVE_STATUS::ACTIVE_STATUS_ACTIVATING))
				|| (crond.curStatus.startTime < crondDatas[i].curStatus.startTime))
			{
				crondDatas.Insert(crond, i);
				flag = true;
				break;
			}
		}

		if (flag) continue;
		//直接加在最后面
		crondDatas.Add(crond);
	}
	return crondDatas;
}

void URoleCrondInterface::receiveCrondRemind_Implementation(const FString& scriptID, const CROND_REMIND_TYPE& remindType)
{
	const FNewCrondConfigData* crondConfigData = GetNewCrondConfigData(scriptID);
	if (crondConfigData != nullptr)
	{
		FString args = crondConfigData->crondName;
		switch (remindType)
		{
		case CROND_REMIND_TYPE::Is_Opening:
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5339, args, FBtnClick::CreateLambda([this, crondConfigData](RT_BTN_TYPE RtType)
			{
				if (RtType == RT_BTN_TYPE::RT_OK)
				{
					if (!crondConfigData->place.IsEmpty())
					{
						//导航到目标位置
						this->NavigateToPoint(crondConfigData->scriptID);
					}
				}
			}));
			break;
		case CROND_REMIND_TYPE::Before_FiveMinutes:
			args = args + "|" + INT_TO_FSTRING(5);
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5338, args, FBtnClick::CreateLambda([](RT_BTN_TYPE RtType){}));
			break;
		case CROND_REMIND_TYPE::Before_TenMinutes:
			args = args + "|" + INT_TO_FSTRING(10);
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5338, args, FBtnClick::CreateLambda([](RT_BTN_TYPE RtType) {}));
			break;
		case CROND_REMIND_TYPE::Before_HalfAnHour:
			args = args + "|" + INT_TO_FSTRING(30);
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5338, args, FBtnClick::CreateLambda([](RT_BTN_TYPE RtType) {}));
			break;
		default:
			break;
		}
	}
}

void URoleCrondInterface::recvActivityTimesData(const FString& datas)
{
	UJsonFieldData* jsonData = UJsonFieldData::Create(this);
	auto returnValue = jsonData->FromString(datas);
	auto _datas = returnValue->GetObjectArray(this, TEXT("ROOT"));
	TMap<int32, int32> tempDatas;//key为actType，Value为times
	for (auto _data : _datas)
	{
		int32 actType = FSTRING_TO_INT(_data->GetString(TEXT("type")));//服务器的活动类型与ACTIVE_TYPE不一样
		int32 times = FSTRING_TO_INT(_data->GetString(TEXT("times")));
		tempDatas.Add(actType, times);
	}

	for (const FNewCrondConfigData* CrondConfigData : CrondConfigDatas)
	{
		if (CrondConfigData)
		{
			int32 times = 0;
			int32* Value = tempDatas.Find(CrondConfigData->type);
			if (Value != nullptr)
			{
				times = *Value;//活动次数赋值
			}
			ActivityJoinTimes.Add(CrondConfigData->scriptID, times);
		}
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRecvActivityTimesDataEvent.Broadcast();
	}
}

void URoleCrondInterface::updateActivityTimesData(const int32& type, const int32& times)
{
	for (const FNewCrondConfigData* CrondConfigData : CrondConfigDatas)
	{
		if (CrondConfigData->type == type)
		{
			ActivityJoinTimes.Add(CrondConfigData->scriptID, times);//字典Add Key一样会覆盖不需要判断Contains
			BP_UpdateActivityTimesData(CrondConfigData->scriptID, times, CrondConfigData->amount);
			return;
		}
	}
}

int32 URoleCrondInterface::GetActivityTimes(const FString& scriptID)
{
	if (ActivityJoinTimes.Contains(scriptID))
		return ActivityJoinTimes[scriptID];
	return 0;
}

FString URoleCrondInterface::GetInfoByWeekDay(int32 weekDay, FString& OutSpecialPlaySummary)
{
	if (WeekCrondConfigDatas.Num() == 0)
	{
		InitLoadWeekCrondConfigDatas();
	}
	if (WeekCrondConfigDatas.Contains(weekDay))
	{
		OutSpecialPlaySummary = WeekCrondConfigDatas[weekDay]->SpecialPlaySummary;
		return WeekCrondConfigDatas[weekDay]->ActivitySummary;
	}
	return FString("");
}

TArray<FDayCrondData> URoleCrondInterface::GetWeekCrondDatas()
{
	TArray<FDayCrondData> weekCrondDatas;
	weekCrondDatas.Add(todayDatas);
	for (auto it : nextSixDayDatas)
	{
		weekCrondDatas.Add(it);
	}
	return weekCrondDatas;
}

ACTIVE_STATUS URoleCrondInterface::GetCrondStatusByScriptID(FString& scriptID)
{
	if (todayDatas.crondDatas.Contains(scriptID))
	{
		return todayDatas.crondDatas[scriptID].curStatus.status;
	}
	return ACTIVE_STATUS::ACTIVE_STATUS_NOT_START;
}