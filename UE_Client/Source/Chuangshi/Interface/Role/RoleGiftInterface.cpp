
#include "RoleGiftInterface.h"
#include "KBEngine.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Chuangshi.h"
#include "Manager/CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CfgManager.h"
#include "GameData/EnumCsvDefine.h"
#include "Manager/SystemSwitchManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleGiftInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnShowSignInReward, &URoleGiftInterface::OnShowSignInReward, const int32& , const int32& , const FVariant& , const FVariant& )
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleGiftInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleGiftInterface::URoleGiftInterface()
{

}

URoleGiftInterface::~URoleGiftInterface()
{

}

void URoleGiftInterface::OnShowOnlineReward_Implementation(const int32& LiftTime, const FString& Reward, const int32& BindType)
{
	OnLineRewardItems.Empty();
	AnalysisItemStr(Reward, BindType, OnLineRewardItems);

	//开启在线奖励
	UUECS3GameInstance::Instance->SystemSwitchManager->OnOpenActivitySystem(TEXT("OnlineReward"), LiftTime);
}

void URoleGiftInterface::ReceiveNewPlayerGift()
{
	KBEngine::FVariantArray param;
	BaseCall(TEXT("receiveNewPlayerGift"), param);
}

void URoleGiftInterface::OnFinishReceiveNewPlayerGift_Implementation()
{
	OnLineRewardItems.Empty();

	//关闭在线奖励
	UUECS3GameInstance::Instance->SystemSwitchManager->OnCloseActivitySystem(TEXT("OnlineReward"));
}

void URoleGiftInterface::OnShowSignInReward(const int32& SignInTotalNum, const int32& SignInTotalRewardNum, const FVariant& SignInRewardList, const FVariant& SignInJson)
{
	SignInNum = SignInTotalNum;
	SignInRewardNum = SignInTotalRewardNum;
	SignInRewardMap.Empty();
	KBEngine::FVariantMap variantMap = SignInRewardList.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray variantArray_Data = variantMap[TEXT("signindata")].GetValue<KBEngine::FVariantArray>();
	for (FVariant& signRewards : variantArray_Data)
	{
		int32 signReward = signRewards.GetValue<int32>();
		if (signReward != 0)
		{
			SignInRewardMap.Add(signReward, SIGN_IN_REWARD_TYPE::REWARD_RECEIVER);
		}
	}
	//for (int32 signReward : SignInRewardList)
	//{
		 //客户端转化的原因，服务器传入一个空的列表，客户端会转化为[0]
	//	if (signReward != 0)
	//	{
	//		SignInRewardMap.Add(signReward, SIGN_IN_REWARD_TYPE::REWARD_RECEIVER);
	//	}
		
	//}
	InitTotalSignInNum();

	SignInList.Empty();
	FSIGN_DATAS tempSignData = FSIGN_DATAS(SignInJson);
	for (auto data : tempSignData.signDatas)
	{
		FSignInData signInData;
		signInData.Year = data.yearMonth / 100;
		signInData.Month = data.yearMonth % 100;
		for (auto day : data.dayList)
		{
			signInData.Days.Add(day);
		}
		SignInList.Add(signInData);
	}
	OnShowSignInRewardEnd();
}

void URoleGiftInterface::OnShowSignInRewardEnd_Implementation()
{

}

TArray<FSignInReward> URoleGiftInterface::GetSignInReward(const int32& Day)
{
	TArray<FSignInReward> Rewards;
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SIGN_IN_REWARD_DATA);
	if (ConfigTable)
	{
		const FSignInRewardData* rewarData = ConfigTable->GetRow<FSignInRewardData>(FSTRING_TO_FNAME(INT_TO_FSTRING(Day)));
		if (rewarData != nullptr)
		{
			AnalysisItemStr(rewarData->Gift, FSTRING_TO_INT(rewarData->BindType), Rewards);
			/*
			TArray<FString> giftStrs = UGolbalBPFunctionLibrary::SplitString(rewarData->Gift, false, TEXT(";"));
			for (auto str : giftStrs)
			{
				FSignInReward Reward;
				TArray<FString> rewardStr = UGolbalBPFunctionLibrary::SplitString(str, false, TEXT(":"));
				Reward.GiftID = FSTRING_TO_INT(rewardStr[0]);
				Reward.BindType = FSTRING_TO_INT(rewarData->BindType);
				if (rewardStr.Num() >= 2)
				{
					Reward.Amount = FSTRING_TO_INT(rewardStr[1]);
				}
				else
				{
					Reward.Amount = 1;
				}
				Rewards.Add(Reward);
			}*/
		}

	}
	return Rewards;
}

TArray<FSignInReward> URoleGiftInterface::GetTotalSignInReward(const int32& AccumulateDay)
{
	TArray<FSignInReward> Rewards;
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TOTAL_SIGN_REWARD_DATA);
	if (ConfigTable)
	{
		const FSignInRewardData* rewarData = ConfigTable->GetRow<FSignInRewardData>(FSTRING_TO_FNAME(INT_TO_FSTRING(AccumulateDay)));
		if (rewarData != nullptr)
		{
			AnalysisItemStr(rewarData->Gift, FSTRING_TO_INT(rewarData->BindType), Rewards);
		}
	}
	return Rewards;
}

bool URoleGiftInterface::bSignIn(const int32& year, const int32& month, const int32& day)
{
	for (auto stall : SignInList)
	{
		if (stall.Year == year && stall.Month == month)
		{
			return stall.Days.Contains(day);
		}
	}
	return false;
}

void URoleGiftInterface::SignInOnline()
{
	KBEngine::FVariantArray param;
	BaseCall(TEXT("signInOnline"), param);
}

void URoleGiftInterface::OnSignInOnlineSuccess_Implementation()
{
	FDateTime CurTime = FDateTime::Now();
	int32 year = CurTime.GetYear();
	int32 month = CurTime.GetMonth();
	int32 day = CurTime.GetDay();
	AddSignInNum();
	bool isFind(false);
	for (auto It = SignInList.CreateConstIterator(); It ; ++It)
	{
		if (It->Year == year && It->Month == month)
		{
			SignInList[It.GetIndex()].Days.Add(day);
			isFind = true;
			break;
		}
		
	}
	if (!isFind)
	{
		FSignInData signInData;
		signInData.Year = year;
		signInData.Month = month;
		signInData.Days.Add(day);
		SignInList.Add(signInData);
	}
}

void URoleGiftInterface::AugmentSignIn(const int32& Year, const int32& Month, const int32& Day)
{
	if (bSignIn(Year, Month, Day))
	{
		return;
	}
	KBEngine::FVariantArray param;
	param.Add(Year);
	param.Add(Month);
	param.Add(Day);
	BaseCall(TEXT("augmentSignIn"), param);
}

void URoleGiftInterface::OnAugmentSignInSuccess_Implementation(const int32& Year, const int32& Month, const int32& Day)
{
	AddSignInNum();
	bool isFind(false);
	for (auto It = SignInList.CreateConstIterator(); It; ++It)
	{
		if (It->Year == Year && It->Month == Month)
		{
			SignInList[It.GetIndex()].Days.Add(Day);
			isFind = true;
			break;
		}
	}
	if (!isFind)
	{
		FSignInData signInData;
		signInData.Year = Year;
		signInData.Month = Month;
		signInData.Days.Add(Day);
		SignInList.Add(signInData);
		return;
	}
}

void URoleGiftInterface::AugmentSignInMonth(const int32& Year, const int32& Month)
{
	KBEngine::FVariantArray param;
	param.Add(Year);
	param.Add(Month);
	BaseCall(TEXT("augmentSignInMonth"), param);
}

void URoleGiftInterface::OnAugmentSignInMonthSuccess_Implementation(const int32& Year, const int32& Month)
{
	FDateTime CurTime = FDateTime::Now();
	int32 days = FDateTime::DaysInMonth(Year, Month);
	bool isFind(false);
	for (auto It = SignInList.CreateConstIterator(); It; ++It)
	{
		if (It->Month == Month)
		{
			for (int32 i = 1; i <= days; ++i)
			{
				if (!It->Days.Contains(i))
				{
					if (CurTime.GetMonth() == Month && CurTime.GetDay() >=i)				//补签当前月份
					{
						continue;
					}
					isFind = true;
					AddSignInNum();
					SignInList[It.GetIndex()].Days.AddUnique(i);
				}
			}
			break;
		}
	}
	if (!isFind)
	{
		FSignInData signInData;
		signInData.Year = Year;
		signInData.Month = Month;
		for (int32 i = 1; i <= days; ++i)
		{
			if (CurTime.GetMonth() == Month && CurTime.GetDay() >= i)				//补签当前月份
			{
				continue;
			}
			AddSignInNum();
			signInData.Days.AddUnique(i);
		}
		SignInList.Add(signInData);
		return;
	}
}

void URoleGiftInterface::ReceiveTotalSignReward(const int32& AccumulateNum)
{
	KBEngine::FVariantArray param;
	param.Add(AccumulateNum);
	BaseCall(TEXT("receiveTotalSignReward"), param);
}

void URoleGiftInterface::OnReceiveTotalSignRewardSuccess_Implementation(const int32& AccumulateNum)
{
	SignInRewardNum += 1;
	if (SignInRewardMap.Contains(AccumulateNum))
	{
		SignInRewardMap[AccumulateNum] = SIGN_IN_REWARD_TYPE::REWARD_RECEIVER;
	}
	else
	{
		SignInRewardMap.Add(AccumulateNum, SIGN_IN_REWARD_TYPE::REWARD_RECEIVER);
	}
	// 完成一轮 （累计签到）奖励
	for (auto it = SignInRewardMap.CreateConstIterator(); it; ++it)
	{
		if (it.Value() != SIGN_IN_REWARD_TYPE::REWARD_RECEIVER)
		{
			return;
		}
	}
	OnFinishRecSignReward();

}

void URoleGiftInterface::OnReachSignRewardNum_Implementation(const int32& num)
{
	if (SignInRewardMap.Contains(num))
	{
		SignInRewardMap[num] = SIGN_IN_REWARD_TYPE::REWARD_ACTIVE;
	}
}

void URoleGiftInterface::OnFinishRecSignReward_Implementation()
{
	SignInRewardMap.Empty();
	InitTotalSignInNum();
}

void URoleGiftInterface::InitBlueCB()
{
	ArrBlueFunc.Add("OnShowOnlineReward");
	ArrBlueFunc.Add("OnShowSignInReward");
	ArrBlueFunc.Add("OnFinishReceiveNewPlayerGift");
	ArrBlueFunc.Add("OnSignInOnlineSuccess");
	ArrBlueFunc.Add("OnAugmentSignInSuccess");
	ArrBlueFunc.Add("OnAugmentSignInMonthSuccess");
	ArrBlueFunc.Add("OnReceiveTotalSignRewardSuccess");
	Supper::InitBlueCB();
}

void URoleGiftInterface::onLeaveWorld()
{
	OnLineRewardItems.Empty();
	SignInList.Empty();
	SignInNum = 0;
	SignInRewardNum = 0;
	SignInRewardMap.Empty();
	Super::onLeaveWorld();
}

void URoleGiftInterface::InitTotalSignInNum()
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TOTAL_SIGN_REWARD_DATA);
	if (ConfigTable)
	{
		TArray<FName> rowNames = ConfigTable->GetRowNames();
		TArray<int32> AcculateNums;
		for (FName name : rowNames)
		{
			AcculateNums.Add(FSTRING_TO_INT(FNAME_TO_FSTRING(name)));
		}
		for (int32 num : AcculateNums)
		{
			if (SignInRewardMap.Contains(num))continue;
			if (SignInRewardNum / AcculateNums.Num() * AcculateNums.Max() + num <= SignInNum)
			{

				SignInRewardMap.Add(num, SIGN_IN_REWARD_TYPE::REWARD_ACTIVE);
			}
			else
			{
				SignInRewardMap.Add(num, SIGN_IN_REWARD_TYPE::REWARD_NONE);
			}
		}
		SignInRewardMap.KeySort([](const int32 KeyA, const int32 KeyB) {return KeyA < KeyB; });
	}
}

void URoleGiftInterface::AnalysisItemStr(const FString& ItemStr, const int32& BindType, TArray<FSignInReward>& ItemList)
{
	TArray<FString> splitStr = UGolbalBPFunctionLibrary::SplitString(ItemStr, false, TEXT(";"));
	for (FString str : splitStr)
	{
		if (!str.IsEmpty())
		{
			TArray<FString> secSplitStr = UGolbalBPFunctionLibrary::SplitString(str, false, TEXT(":"));
			FSignInReward reward;
			if (secSplitStr.Num() >= 2)
			{
				reward.GiftID = FSTRING_TO_INT(secSplitStr[0]);
				reward.Amount = FSTRING_TO_INT(secSplitStr[1]);
				reward.BindType = BindType;
				ItemList.Add(reward);
			}
		}
	}
}

void URoleGiftInterface::CalculateAugmentSignInMonth(const int32& Month, TArray<int32>& Days)
{
	int32 days = FDateTime::DaysInMonth(FDateTime::Now().GetYear(), Month);
	for (int32 i = 1; i <= days; ++i)
	{
		Days.AddUnique(i);
	}
}

void URoleGiftInterface::AddSignInNum()
{
	SignInNum += 1;
	for (auto It = SignInRewardMap.CreateConstIterator(); It; ++It)
	{
		// 只检查第一个数据
		if (It.Value() == SIGN_IN_REWARD_TYPE::REWARD_NONE)
		{
			int32 num = It.Key();
			TArray<int32> keys;
			SignInRewardMap.GetKeys(keys);
			if (SignInRewardNum / SignInRewardMap.Num() * keys.Max() + num <= SignInNum)
			{
				OnReachSignRewardNum(num);
			}
		
			return;
		}
	}
}

