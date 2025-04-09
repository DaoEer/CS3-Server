#include "RoleRankInterface.h"
#include "Chuangshi.h"
#include "KBEngine.h"
#include "GameData/ConstData.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Util/GolbalBPFunctionLibrary.h"



CS3_BEGIN_INTERFACE_METHOD_MAP(URoleRankInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenGameRank, &URoleRankInterface::OpenGameRank, const int32&, const int32&, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRequestLevelRankFirstTime, &URoleRankInterface::OnRequestLevelRankFirstTime, const int32&, const int32&, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRequestCombatRankFirstTime, &URoleRankInterface::OnRequestCombatRankFirstTime, const int32&, const int32&, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRequestMoneyRankFirstTime, &URoleRankInterface::OnRequestMoneyRankFirstTime, const int32&, const int32&, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnRequestWeaponRankFirstTime, &URoleRankInterface::OnRequestWeaponRankFirstTime, const int32&, const int32&, const int32&, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleRankInterface, Supper)
//CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(HP, &URoleRankInterface::Set_HP, int32)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleRankInterface::URoleRankInterface()
{
}

URoleRankInterface::~URoleRankInterface()
{

}


void URoleRankInterface::OpenGameRankBP_Implementation(const int32& NpcID, const int32& RankNum, const int32& TotalPage, const TArray<FLevelRankData>& LevelRank)
{
	if (!LevelRankPages.Contains(0))
	{
		LevelRankNum.Add(0,RankNum);
		LevelRankPages.Add(0, TotalPage);
		for (auto rank : LevelRank)
		{
			AllLevelRankList.Add(rank);
		}
	}
}


void URoleRankInterface::RequestRankFirstTime(EGameRank RankType, const int32& Camp)
{
	if (RankType == EGameRank::Level_Rank)
	{
		if (LevelRankPages.Contains(Camp) && LevelRankNum.Contains(Camp))
		{
			TArray<FLevelRankData> rankData;
			GetLevelRankData(Camp, 1, rankData);
			OnRequestLevelRankFirstTimeBP(Camp, LevelRankNum[Camp], LevelRankPages[Camp], LevelRankAscend[Camp], rankData);
			return;
		}
	}
	else if(RankType == EGameRank::Combat_Rank)
	{
		if (CombatRankNum.Contains(Camp) && CombatRankPages.Contains(Camp))
		{
			TArray<FCombatRankData> rankData;
			GetCombatRankData(Camp, 1, rankData);
			OnRequestCombatRankFirstTimeBP(Camp, CombatRankNum[Camp], CombatRankPages[Camp], CombatRankAscend[Camp], rankData);
			return;
		}
	}
	else if (RankType == EGameRank::Money_Rank)
	{
		if (MoneyRankPages.Contains(Camp) && MoneyRankNum.Contains(Camp))
		{
			TArray<FMoneyRankData> rankData;
			GetMoneyRankData(Camp, 1, rankData);
			OnRequestMoneyRankFirstTimeBP(Camp, MoneyRankNum[Camp], MoneyRankPages[Camp], MoneyRankAscend[Camp], rankData);
			return;
		}
	}
	else if (RankType == EGameRank::Weapon_Rank)
	{
		if (WeaponRankPages.Contains(Camp) && WeaponRankNum.Contains(Camp))
		{
			TArray<FWeaponRankData> rankData;
			GetWeaponRankData(Camp, 1, rankData);
			OnRequestWeaponRankFirstTimeBP(Camp, WeaponRankNum[Camp], WeaponRankPages[Camp], WeaponRankAscend[Camp], rankData);
			return;
		}
	}
	KBEngine::FVariantArray args;
	args.Add(int32(RankType));
	args.Add(Camp);
	BaseCall(TEXT("requestGameRankFirstTime"), args);
}

void URoleRankInterface::OnRequestRankStoreMoney_Implementation(const FString& StoreMoney)
{
	if (nullptr != GetEntity())
	{
		int64 OwnMoney = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
		MoneyRankValue = OwnMoney + FSTRING_TO_INT64(StoreMoney);
	}
}

void URoleRankInterface::RequestRank(EGameRank RankType, const int32& Camp, const int32& Page)
{
	if (RankType == EGameRank::Level_Rank)
	{
		TArray<FLevelRankData> rankData;
		GetLevelRankData(Camp, Page, rankData);
		if (rankData.Num() != 0)
		{
			OnRequestLevelRankBP(Camp, Page, rankData);
			return;
		}
	}
	else if (RankType == EGameRank::Combat_Rank)
	{
		TArray<FCombatRankData> rankData;
		GetCombatRankData(Camp, Page, rankData);
		if (rankData.Num() != 0)
		{
			OnRequestCombatRankBP(Camp, Page, rankData);
			return;
		}
	}
	else if (RankType == EGameRank::Money_Rank)
	{
		TArray<FMoneyRankData> rankData;
		GetMoneyRankData(Camp, Page, rankData);
		if (rankData.Num() != 0)
		{
			OnRequestMoneyRankBP(Camp, Page, rankData);
			return;
		}
	}
	else if (RankType == EGameRank::Weapon_Rank)
	{
		TArray<FWeaponRankData> rankData;
		GetWeaponRankData(Camp, Page, rankData);
		if (rankData.Num() != 0)
		{
			OnRequestWeaponRankBP(Camp, Page,rankData);
			return;
		}
	}
}

void URoleRankInterface::OnRequestLevelRankBP_Implementation(const int32& Camp, const int32& Page, const TArray<FLevelRankData>& LevelRank)
{
}

void URoleRankInterface::OnRequestCombatRankBP_Implementation(const int32& Camp, const int32& Page, const TArray<FCombatRankData>& CombatRank)
{
}

void URoleRankInterface::OnRequestMoneyRankBP_Implementation(const int32& Camp, const int32& Page, const TArray<FMoneyRankData>& MoneyRank)
{
}

void URoleRankInterface::OnRequestWeaponRankBP_Implementation(const int32& Camp, const int32& Page, const TArray<FWeaponRankData>& WeaponRank)
{
}

void URoleRankInterface::OnRequestLevelRankFirstTimeBP_Implementation(const int32& Camp, const int32& RankNum, const int32& TotalPage, const int32& Ascend, const TArray<FLevelRankData>& LevelRank)
{
}

void URoleRankInterface::OnRequestCombatRankFirstTimeBP_Implementation(const int32& Camp, const int32& RankNum, const int32& TotalPage, const int32& Ascend, const TArray<FCombatRankData>& CombatRank)
{
}

void URoleRankInterface::OnRequestMoneyRankFirstTimeBP_Implementation(const int32& Camp, const int32& RankNum, const int32& TotalPage, const int32& Ascend, const TArray<FMoneyRankData>& MoneyRank)
{
}

void URoleRankInterface::OnRequestWeaponRankFirstTimeBP_Implementation(const int32& Camp, const int32& RankNum, const int32& TotalPage, const int32& Ascend, const TArray<FWeaponRankData>& WeaponRank)
{
}

void URoleRankInterface::OpenGameRank(const int32& INT32_1, const int32& INT32_2, const int32& INT32_3, const FVariant& fixedDict)
{
	FLEVEL_RANK_DICT* rankInfo = new FLEVEL_RANK_DICT(fixedDict);
	TArray<FLevelRankData> rankData;
	for (auto data : rankInfo->datas1)
	{
		FLevelRankData rank;
		rank.playerDBID = INT64_TO_FSTRING(data.playerDBID1);
		rank.playerName = data.playerName2;
		rank.camp = data.camp3;
		rank.profession = data.profession4;
		rank.combatPower = data.combatPower5;
		rank.level = data.level6;
		rank.ascend = data.ascend7;
		rankData.Add(rank);
	}
	OpenGameRankBP(INT32_1, INT32_2, INT32_3, rankData);
}

void URoleRankInterface::OnRequestLevelRankFirstTime(const int32& Camp, const int32& RankNum, const int32& TotalPage, const FVariant& fixedDict )
{
	FLEVEL_RANK_DICT* levelRankDict = new FLEVEL_RANK_DICT(fixedDict);
	TArray<FLevelRankData> rankData;
	TArray<FLevelRankData> firstPageData;
	int32 playerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString playerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(playerId,"playerName");
	LevelRankAscend.Add(Camp, 0);
	for (auto data : levelRankDict->datas1)
	{
		FLevelRankData rank;
		rank.playerDBID = INT64_TO_FSTRING(data.playerDBID1);
		rank.playerName = data.playerName2;
		rank.camp = data.camp3;
		rank.profession = data.profession4;
		rank.combatPower = data.combatPower5;
		rank.level = data.level6;
		rank.ascend = data.ascend7;
		rankData.Add(rank);
		if (playerName.Equals(rank.playerName))
		{
			LevelRankAscend.Add(Camp, rank.ascend);
		}
	}
	rankData.Sort([](const FLevelRankData& A, const FLevelRankData& B) {return A.level > B.level; });
	LevelRankNum.Add(Camp, RankNum);
	LevelRankPages.Add(Camp, TotalPage);
	if (Camp == 0)
	{
		AllLevelRankList.Append(rankData);
	}
	else if (Camp == 1)
	{
		XianLevelRankList.Append(rankData);
	}
	else
	{
		MoLevelRankList.Append(rankData);
	}

	for (auto i = 0; i < GAME_RANKING_PAGE_NUM; i++)
	{	
		if (i < rankData.Num())
		{
			firstPageData.Add(rankData[i]);
		}
	}
	OnRequestLevelRankFirstTimeBP(Camp, RankNum, TotalPage, LevelRankAscend[Camp], firstPageData);
}

void URoleRankInterface::OnRequestCombatRankFirstTime(const int32& Camp, const int32& RankNum, const int32& TotalPage, const FVariant& fixedDict )
{
	FCOMBAT_RANK_DICT* rcombatRankDict = new FCOMBAT_RANK_DICT(fixedDict);
	TArray<FCombatRankData> rankData;
	TArray<FCombatRankData> firstPageData;
	int32 playerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString playerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(playerId, "playerName");
	CombatRankAscend.Add(Camp, 0);
	for (auto data : rcombatRankDict->datas1)
	{
		FCombatRankData rank;
		rank.playerDBID = INT64_TO_FSTRING(data.playerDBID1);
		rank.playerName = data.playerName2;
		rank.camp = data.camp3;
		rank.profession = data.profession4;
		rank.combatPower = data.combatPower5;
		rank.level = data.level6;
		rank.ascend = data.ascend7;
		rankData.Add(rank);
		if (playerName.Equals(rank.playerName))
		{
			CombatRankAscend.Add(Camp, rank.ascend);
		}
	}
	rankData.Sort([](const FCombatRankData& A, const FCombatRankData& B) {return A.combatPower > B.combatPower; });
	CombatRankNum.Add(Camp, RankNum);
	CombatRankPages.Add(Camp, TotalPage);
	if (Camp == 0)
	{
		AllCombatRankList.Append(rankData);
	}
	else if (Camp == 1)
	{
		XianCombatRankList.Append(rankData);
	}
	else
	{
		MoCombatRankList.Append(rankData);
	}

	for (auto i = 0; i < GAME_RANKING_PAGE_NUM; i++)
	{
		if (i < rankData.Num())
		{
			firstPageData.Add(rankData[i]);
		}
	}
	OnRequestCombatRankFirstTimeBP(Camp, RankNum, TotalPage, CombatRankAscend[Camp], firstPageData);
}

void URoleRankInterface::OnRequestMoneyRankFirstTime(const int32& Camp, const int32& RankNum, const int32& TotalPage, const FVariant& fixedDict)
{
	FMONEY_RANK_DICT* fmoneyRankDict = new FMONEY_RANK_DICT(fixedDict);
	TArray<FMoneyRankData> rankData;
	TArray<FMoneyRankData> firstPageData;
	int32 playerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString playerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(playerId, "playerName");
	MoneyRankAscend.Add(Camp, 0);
	for (auto data : fmoneyRankDict->datas1)
	{
		FMoneyRankData rank;
		rank.playerDBID = INT64_TO_FSTRING(data.playerDBID1);
		rank.playerName = data.playerName2;
		rank.camp = data.camp3;
		rank.profession = data.profession4;
		rank.money = data.money5;
		rank.level = data.level6;
		rank.ascend = data.ascend7;
		rankData.Add(rank);
		if (playerName.Equals(rank.playerName))
		{
			MoneyRankAscend.Add(Camp, rank.ascend);
		}
	}
	rankData.Sort([](const FMoneyRankData& A, const FMoneyRankData& B) {return A.money > B.money; });
	MoneyRankNum.Add(Camp, RankNum);
	MoneyRankPages.Add(Camp, TotalPage);
	if (Camp == 0)
	{
		AllMoneyRankList.Append(rankData);
	}
	else if (Camp == 1)
	{
		XianMoneyRankList.Append(rankData);
	}
	else
	{
		MoMoneyRankList.Append(rankData);
	}

	for (auto i = 0; i < GAME_RANKING_PAGE_NUM; i++)
	{
		if (i < rankData.Num())
		{
			firstPageData.Add(rankData[i]);
		}
	}
	OnRequestMoneyRankFirstTimeBP(Camp, RankNum, TotalPage, MoneyRankAscend[Camp], firstPageData);
}

void URoleRankInterface::OnRequestWeaponRankFirstTime(const int32& Camp, const int32& RankNum, const int32& TotalPage, const FVariant& fixedDict)
{
	FWEAPON_COMBAT_DICT * fweaponCombatDict = new FWEAPON_COMBAT_DICT(fixedDict);
	TArray<FWeaponRankData> rankData;
	TArray<FWeaponRankData> firstPageData;
	int32 playerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString playerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(playerId, "playerName");
	WeaponRankAscend.Add(Camp, 0);
	for (auto data : fweaponCombatDict->datas1)
	{
		FWeaponRankData rank;
		rank.playerDBID = INT64_TO_FSTRING(data.playerDBID1);
		rank.playerName = data.playerName2;
		rank.camp = data.camp3;
		rank.weaponUID = INT64_TO_FSTRING(data.weaponUID4);
		rank.weaponID = data.weaponID5;
		rank.quality = data.quality6;
		rank.combatPower = data.combatPower7;
		rank.attackProperties = data.attackProperties8;
		rank.attachProperties = data.attachProperties9;
		rank.intensifyProperties = data.intensifyProperties10;
		rank.ascend = data.ascend11;
		rankData.Add(rank);
		if (playerName.Equals(rank.playerName))
		{
			WeaponRankAscend.Add(Camp, rank.ascend);
		}
	}
	rankData.Sort([](const FWeaponRankData& A, const FWeaponRankData& B) {return A.combatPower > B.combatPower; });
	WeaponRankNum.Add(Camp, RankNum);
	WeaponRankPages.Add(Camp, TotalPage);
	if (Camp == 0)
	{
		AllWeaponRankList.Append(rankData);
	}
	else if (Camp == 1)
	{
		XianWeaponRankList.Append(rankData);
	}
	else
	{
		MoWeaponRankList.Append(rankData);
	}

	for (auto i = 0; i < GAME_RANKING_PAGE_NUM; i++)
	{
		if (i < rankData.Num())
		{
			firstPageData.Add(rankData[i]);
		}
	}
	OnRequestWeaponRankFirstTimeBP(Camp, RankNum, TotalPage, WeaponRankAscend[Camp], firstPageData);
}


void URoleRankInterface::Client_updateRankData_Implementation(const uint8& RankType)
{
	if (RankType == uint8(EGameRank::Level_Rank)) 
	{
		levelUptadeMark = true;
	}
	else if (RankType == uint8(EGameRank::Combat_Rank))
	{
		combatUptadeMark = true;
	}
	else if (RankType == uint8(EGameRank::Money_Rank))
	{
		moneyUptadeMark = true;
	}
	else
	{
		weaponUptadeMark = true;
	}

}

void URoleRankInterface::clearRankData()
{
	if (levelUptadeMark)
	{
		AllLevelRankList.Empty();
		XianLevelRankList.Empty();
		MoLevelRankList.Empty();
		LevelRankPages.Empty();
		LevelRankNum.Empty();
		LevelRankAscend.Empty();
		levelUptadeMark = false;
	}
	if (combatUptadeMark)
	{
		AllCombatRankList.Empty();
		XianCombatRankList.Empty();
		MoCombatRankList.Empty();
		CombatRankPages.Empty();
		CombatRankNum.Empty();
		CombatRankAscend.Empty();
		combatUptadeMark = false;
	}
	if (moneyUptadeMark)
	{
		AllMoneyRankList.Empty();
		XianMoneyRankList.Empty();
		MoMoneyRankList.Empty();
		MoneyRankPages.Empty();
		MoneyRankNum.Empty();
		MoneyRankAscend.Empty();
		moneyUptadeMark = false;
	}
	if (weaponUptadeMark)
	{
		AllWeaponRankList.Empty();
		XianWeaponRankList.Empty();
		MoWeaponRankList.Empty();
		WeaponRankPages.Empty();
		WeaponRankNum.Empty();
		WeaponRankAscend.Empty();
		weaponUptadeMark = false;
	}
}

void URoleRankInterface::InitBlueCB()
{
	ArrBlueFunc.Add(TEXT("OnRequestRankStoreMoney"));
	ArrBlueFunc.Add(TEXT("Client_updateRankData"));
	Supper::InitBlueCB();
}

void URoleRankInterface::onLeaveWorld()
{
	Super::onLeaveWorld();
}

void URoleRankInterface::GetLevelRankData(const int32& Camp, const int32& Page, TArray<FLevelRankData>& RankType)
{
	TArray<FLevelRankData> RankList;
	int32 begin((Page-1)*GAME_RANKING_PAGE_NUM);
	int32 end(begin + GAME_RANKING_PAGE_NUM);

	if (Camp == 0)
	{
		RankList.Append(AllLevelRankList);
	}
	else if (Camp == 1)
	{
		RankList.Append(XianLevelRankList);
	}
	else if (Camp == 2)
	{
		RankList.Append(MoLevelRankList);
	}
	RankList.Sort([](const FLevelRankData& A, const FLevelRankData& B) {return A.level > B.level; });
	int32 num = RankList.Num();
	if (num != 0)
	{
		for (auto it = begin; it < end; ++it)
		{
			if (num > it)
			{
				RankType.Add(RankList[it]);
			}
		}
	}
	
}

void URoleRankInterface::GetCombatRankData(const int32& Camp, const int32& Page, TArray<FCombatRankData>& RankType)
{
	TArray<FCombatRankData> RankList;
	int32 begin((Page-1)*GAME_RANKING_PAGE_NUM);
	int32 end(begin + GAME_RANKING_PAGE_NUM);

	if (Camp == 0)
	{
		RankList.Append(AllCombatRankList);
	}
	else if (Camp == 1)
	{
		RankList.Append(XianCombatRankList);
	}
	else if (Camp == 2)
	{
		RankList.Append(MoCombatRankList);
	}
	RankList.Sort([](const FCombatRankData& A, const FCombatRankData& B) {return A.combatPower > B.combatPower; });
	int32 num = RankList.Num();
	if (num != 0)
	{
		for (auto it = begin; it < end; ++it)
		{
			if (num > it)
			{
				RankType.Add(RankList[it]);
			}
		}
	}

}

void URoleRankInterface::GetMoneyRankData(const int32& Camp, const int32& Page, TArray<FMoneyRankData>& RankType)
{
	TArray<FMoneyRankData> RankList;
	int32 begin((Page-1)*GAME_RANKING_PAGE_NUM);
	int32 end(begin + GAME_RANKING_PAGE_NUM);

	if (Camp == 0)
	{
		RankList.Append(AllMoneyRankList);
	}
	else if (Camp == 1)
	{
		RankList.Append(XianMoneyRankList);
	}
	else if (Camp == 2)
	{
		RankList.Append(MoMoneyRankList);
	}
	RankList.Sort([](const FMoneyRankData& A, const FMoneyRankData& B) {return A.money > B.money; });
	int32 num = RankList.Num();
	if (num != 0)
	{
		for (auto it = begin; it < end; ++it)
		{
			if (num > it)
			{
				RankType.Add(RankList[it]);
			}
		}
	}
	
}

void URoleRankInterface::GetWeaponRankData(const int32& Camp, const int32& Page, TArray<FWeaponRankData>& RankType)
{
	TArray<FWeaponRankData> RankList;
	int32 begin((Page-1)*GAME_RANKING_PAGE_NUM);
	int32 end(begin + GAME_RANKING_PAGE_NUM);

	if (Camp == 0)
	{
		RankList.Append(AllWeaponRankList);
	}
	else if (Camp == 1)
	{
		RankList.Append(XianWeaponRankList);
	}
	else if (Camp == 2)
	{
		RankList.Append(MoWeaponRankList);
	}
	RankList.Sort([](const FWeaponRankData& A, const FWeaponRankData& B) {return A.combatPower > B.combatPower; });
	int32 num = RankList.Num();
	if (num != 0)
	{
		for (auto it = begin; it < end; ++it)
		{
			if (num > it)
			{
				RankType.Add(RankList[it]);
			}
		}
	}
	
}

