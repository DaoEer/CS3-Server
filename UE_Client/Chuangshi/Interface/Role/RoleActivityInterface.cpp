
#include "RoleActivityInterface.h"
#include "KBEngine.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "JsonFieldData.h"
#include "Json.h"
#include "Serialization/JsonWriter.h"
#include "Util/ConvertUtil.h"
#include "Manager/CustomTimerManager.h"
#include "Util/CS3Debug.h"
#include "Manager/MapManager.h"
#include "RoleTongInterface.h"
#include "Manager/CfgManager.h"
#include "GameData/EnumCsvDefine.h"
#include "Entity/Alias.h"
#include "CS3Base/UIManager.h"
#include "CS3Base/BaseWindow.h"
#include "Manager/EventManager.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleActivityInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRequestSameCampPos, &URoleActivityInterface::CLIENT_OnRequestSameCampPos, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenBHZBIntegralRank, &URoleActivityInterface::OpenBHZBIntegralRank, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ClearYXLMMemberData, &URoleActivityInterface::ClearYXLMMemberData)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenSignUpBHZBRankWin, &URoleActivityInterface::OpenSignUpBHZBRankWin, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataToTongMemberClientProtectData, &URoleActivityInterface::UpdataToTongMemberClientProtectData,const int32,const int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataToTongMemberClientAttackData, &URoleActivityInterface::UpdataToTongMemberClientAttackData, const int32, const int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenNPCExtPointDetails, &URoleActivityInterface::OpenNPCExtPointDetails, const FString& , uint8 , uint8 , const FVariant& , const FVariant& , int32 , const FString&, const FVariant&, const FVariant&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitBHZBNPCPointDatas, &URoleActivityInterface::InitBHZBNPCPointDatas,const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataNPCPointRestEndTime, &URoleActivityInterface::UpdataNPCPointRestEndTime,int32,const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataNPCPointReadyEndTime, &URoleActivityInterface::UpdataNPCPointReadyEndTime, int32, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataNPCPointDeclareWarState, &URoleActivityInterface::UpdataNPCPointDeclareWarState, int32,uint8)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataNPCPointOccupyData, &URoleActivityInterface::UpdataNPCPointOccupyData, int32, uint64,uint64,const FString&,const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataHomeBarracksMapDataToAllMember, &URoleActivityInterface::UpdataHomeBarracksMapDataToAllMember, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataMemberPositionToClient, &URoleActivityInterface::UpdataMemberPositionToClient, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataMyGroupIDToClient, &URoleActivityInterface::UpdataMyGroupIDToClient, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowExitPointSaveSpaceBtn, &URoleActivityInterface::ShowExitPointSaveSpaceBtn)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(HideExitPointSaveSpaceBtn, &URoleActivityInterface::HideExitPointSaveSpaceBtn)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataBHZBPointJoinAttackMembers, &URoleActivityInterface::UpdataBHZBPointJoinAttackMembers,int32,const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataBHZBPointJoinProtectMembers, &URoleActivityInterface::UpdataBHZBPointJoinProtectMembers, int32, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowGroupIDAttackPointSign, &URoleActivityInterface::ShowGroupIDAttackPointSign,int32,int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(HideGroupIDAttackPointSign, &URoleActivityInterface::HideGroupIDAttackPointSign,int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowBHZBIntegralRankWin, &URoleActivityInterface::ShowBHZBIntegralRankWin, const FVariant&, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowEnterYeZhanFengQiWindow, &URoleActivityInterface::ShowEnterYeZhanFengQiWindow)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitBHZBWarDetailData, &URoleActivityInterface::InitBHZBWarDetailData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateBHZBWarDetailIntegralData, &URoleActivityInterface::UpdateBHZBWarDetailIntegralData, int32,int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateBHZBWarDetailOccupyNumber, &URoleActivityInterface::UpdateBHZBWarDetailOccupyNumber, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateBHZBWarDetailTeamData, &URoleActivityInterface::UpdateBHZBWarDetailTeamData, int32,int32,int32,const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RemoveBHZBWarDetailTeamData, &URoleActivityInterface::RemoveBHZBWarDetailTeamData, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateBHZBWarDetailOccupyPointData, &URoleActivityInterface::UpdateBHZBWarDetailOccupyPointData, int32,int32,const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RemoveBHZBWarrDetailOccupyPoint, &URoleActivityInterface::RemoveBHZBWarrDetailOccupyPoint, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(AddBHZBWarMsgData, &URoleActivityInterface::AddBHZBWarMsgData, int32,const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdateNPCPointAttackGroupTeamID, &URoleActivityInterface::UpdateNPCPointAttackGroupTeamID, int32, int32,uint64)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(UpdataBHZBPointJoinProtectTeamID, &URoleActivityInterface::UpdataBHZBPointJoinProtectTeamID, int32, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenJoinGCZWin, &URoleActivityInterface::OpenJoinGCZWin, const FVariant&, const FVariant&, const FVariant&,int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(NotifyToStartMatchGCZ, &URoleActivityInterface::NotifyToStartMatchGCZ, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(NotifyCancelMatchGCZ, &URoleActivityInterface::NotifyCancelMatchGCZ)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(QueryAllBHZBIntegralData, &URoleActivityInterface::QueryAllBHZBIntegralData, const FVariant&, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnBattleMatchStart, &URoleActivityInterface::OnBattleMatchStart)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleActivityInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleActivityInterface::URoleActivityInterface()
{

}
 
URoleActivityInterface::~URoleActivityInterface()
{

}

void URoleActivityInterface::CLIENT_UpdateMoneyDataToOtherPlayer_Implementation(const int32& playerID, const int32& money, const FString& playerName, const int32& camp, const int32& profession, const int32& level)
{
	AddMoneyData(playerID, money, playerName, camp, profession, level);
}

void URoleActivityInterface::CLIENT_ReceiveOtherMoneyData_Implementation(const int32& playerID, const int32& money, const FString& playerName, const int32& camp, const int32& profession, const int32& level)
{
	AddMoneyData(playerID, money, playerName, camp, profession, level);
}

void URoleActivityInterface::CLIENT_UpdateIntegralDataToOtherClient_Implementation(const int32& playerID, const int32& integral)
{
	AddIntegralData(playerID, integral);
}

void URoleActivityInterface::CLIENT_ReceiveOtherIntegralData_Implementation(const int32& playerID, const int32& integral)
{
	AddIntegralData(playerID, integral);
}

void URoleActivityInterface::CLIENT_UpdateBeKillDataToOtherClient_Implementation(const int32& playerID, const int32& beKill)
{
	if (moneyDatas.Contains(playerID))
	{
		moneyDatas[playerID].BeKill = beKill;
	}
}

void URoleActivityInterface::CLIENT_ReceiveOtherBeKillData_Implementation(const int32& playerID, const int32& beKill)
{
	if (moneyDatas.Contains(playerID))
	{
		moneyDatas[playerID].BeKill = beKill;
	}
}

void URoleActivityInterface::CLIENT_UpdateKillDataToOtherClient_Implementation(const int32& playerID, const int32& Kill)
{
	if (moneyDatas.Contains(playerID))
	{
		moneyDatas[playerID].Kill = Kill;
	}
}

void URoleActivityInterface::CLIENT_ReceiveOtherKillData_Implementation(const int32& playerID, const int32& Kill)
{
	if (moneyDatas.Contains(playerID))
	{
		moneyDatas[playerID].Kill = Kill;
	}
}

void URoleActivityInterface::AddMoneyData(const int32& playerID, const int32& money, const FString playerName, const int32& camp, const int32& profession, const int32& level)
{
	if (!moneyDatas.Contains(playerID))
	{
		FSPACEHUNTING hunTingData;
		hunTingData.Camp = camp;
		hunTingData.Level = level;
		hunTingData.Money = money;
		hunTingData.PlayerName = playerName;
		hunTingData.Profession = profession;
		hunTingData.Kill = 0;
		hunTingData.BeKill = 0;
		moneyDatas.Add(playerID, hunTingData);
	}
	else
	{
		moneyDatas[playerID].Money = money;
	}
	moneyDatas.ValueSort([](const FSPACEHUNTING& hunTingA, const FSPACEHUNTING& hunTingB) {return hunTingA.Money > hunTingB.Money; });
	OnAddMoneyData(playerID);
}

void URoleActivityInterface::AddIntegralData(const int32& playerID, const int32& integral)
{
	if (!integralDatas.Contains(playerID))
	{
		integralDatas.Add(playerID, integral);
	}
	else
	{
		integralDatas[playerID] = integral;
	}
	OnAddIntegralData(playerID);
}
void URoleActivityInterface::CLIENT_SetIntegralMax_Implementation(const int32& integral)
{
	integralMax = integral;
}

void URoleActivityInterface::CLIENT_HunTingMemberLeave_Implementation(const int32& playerID)
{
	if (moneyDatas.Contains(playerID))
	{
		moneyDatas.Remove(playerID);
	}
	moneyDatas.ValueSort([](const FSPACEHUNTING& hunTingA, const FSPACEHUNTING& hunTingB) {return hunTingA.Money > hunTingB.Money; });
}

void URoleActivityInterface::CLIENT_ShowRankList_Implementation()
{

}

void URoleActivityInterface::CLIENT_OnGodLike_Implementation(const FString& KillerName)
{

}

void URoleActivityInterface::CLIENT_OnFirstKill_Implementation(const FString& KillerName)
{

}

void URoleActivityInterface::CLIENT_OnClearData_Implementation()
{
	moneyDatas.Empty();
	integralMax = 0;
	integralDatas.Empty();
}

int32 URoleActivityInterface::GetPlayerRank(const int32& playerID)
{
	TArray<int32> keyList;
	for (auto data : moneyDatas)
	{
		keyList.Add(data.Key);
	}
	return keyList.IndexOfByKey(playerID) + 1;
}

void URoleActivityInterface::CLIENT_ShowYeZhanFengQiMemberRank_Implementation(const int32& rank, const int32& killNum)
{

}

void URoleActivityInterface::ClIENT_StartReduceYeZhanFengQiArea_Implementation(const float& totalUseTime)
{

}

void URoleActivityInterface::ClIENT_ShowYeZhanFengQiEndArea_Implementation(const FVector& endCenterPos, const float& endRadius)
{

}

void URoleActivityInterface::ClIENT_ShowYeZhanFengQiOriginArea_Implementation(const FVector& originCenterPos, const float& originRadius)
{

}

void URoleActivityInterface::CLIENT_UpdateYeZhanFengQiMyKillNumber_Implementation(const int32& killNum)
{

}

void URoleActivityInterface::CLIENT_UpdateYeZhanFengQiMemberNumber_Implementation(const int32& memberNum)
{

}

void URoleActivityInterface::CLIENT_OnEnterLingMaiTelPortQueue_Implementation(const int32& Key)
{

}

void URoleActivityInterface::CLIENT_ShowShiFangChengPassList_Implementation(const int32& joinNumber, const FString& passDataList)
{
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnValue = temp->FromString(passDataList);
	auto tempArray = returnValue->GetObjectArray(this, TEXT("ROOT"));
	for (auto item : tempArray)
	{
		FString playerName = item->GetString(TEXT("playerName"));
		FString passTime = item->GetString(TEXT("passTime"));
		passDataMap.Add(playerName, passTime);
	}
}
void URoleActivityInterface::CLIENT_ShowEnterActBunchWindow_Implementation()
{

}

void URoleActivityInterface::CELL_LeaveYeZhanFengQi()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::CELL_LeaveYeZhanFengQi : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("CELL_leaveYeZhanFengQi"), args);
}

void URoleActivityInterface::ShowEnterYeZhanFengQiWindow_Implementation()
{

}

void URoleActivityInterface::EnterYeZhanFengQi()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::EnterYeZhanFengQi : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("enterYeZhanFengQi"), args);
}

void URoleActivityInterface::RequestSameCampPos()
{
	KBEngine::FVariantArray args;
	if (nullptr != GetEntity())
	{
		GetEntity()->CellCall(TEXT("CELL_requestSameCampPos"), args);
	}
}


void URoleActivityInterface::CLIENT_OnRequestSameCampPos(const FVariant& BIGMAP_SAME_CAMP_LIST_1)
{
	FBIGMAP_SHOW_INFOS BigmapDict = FBIGMAP_SHOW_INFOS(BIGMAP_SAME_CAMP_LIST_1);
	TArray<FBigmapActInfo> BigmapActInfo;
	for (auto element : BigmapDict.infos1)
	{
		FBigmapActInfo Bmap;
		Bmap.objectID = element.objectID1;
		Bmap.position = element.position2;
		Bmap.playerName = element.name3;
		BigmapActInfo.Add(Bmap);
	}
	CLIENT_OnRequestSameCampPos_BP(BigmapActInfo);
}

void URoleActivityInterface::EnterActBunch()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::EnterActBunch : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("enterActBunch"), args);
}

void URoleActivityInterface::AbandonActBunch()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::AbandonActBunch : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("abandonActBunch"), args);
}

void URoleActivityInterface::CELL_EnterShiFangCheng()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::CELL_EnterShiFangCheng : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("CELL_enterShiFangCheng"), args);
}

void URoleActivityInterface::CELL_AbandonShiFangeCheng()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::CELL_AbandonShiFangeCheng : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("CELL_abandonShiFangeCheng"), args);
}

void URoleActivityInterface::CLIENT_ShowPassShiFangChengNumber_Implementation(const int32& passNumber)
{

}

void URoleActivityInterface::CLIENT_ShowFirstPassShiFangCheng_Implementation(const FString& passName, const int32& passTime)
{

}

void URoleActivityInterface::CLIENT_FengQiMemberLeave_Implementation(const int32& playerID)
{
	if (YeZhanFengQiMemberDatas.Contains(playerID))
	{
		YeZhanFengQiMemberDatas.Remove(playerID);
	}
}

void URoleActivityInterface::CLIENT_UpdateFengQiMemberDataToOtherClient_Implementation(const int32& playerID, const int32& integral, const FString& playerName, const int32& profession, const int32& killNum)
{
	if (!YeZhanFengQiMemberDatas.Contains(playerID))
	{
		FSPACEYEZHANFENGQI member;
		member.Integral = integral;
		member.KillNum = killNum;
		member.Profession = profession;
		member.PlayerName = playerName;
		YeZhanFengQiMemberDatas.Add(playerID, member);
	}
	else
	{
		YeZhanFengQiMemberDatas[playerID].Integral = integral;
		YeZhanFengQiMemberDatas[playerID].KillNum = killNum;
	}
}

void URoleActivityInterface::CLIENT_ReceiveFengQiOtherMemberData_Implementation(const int32& playerID, const int32& integral, const FString& playerName, const int32& profession, const int32& killNum)
{
	if (!YeZhanFengQiMemberDatas.Contains(playerID))
	{
		FSPACEYEZHANFENGQI member;
		member.Integral = integral;
		member.KillNum = killNum;
		member.Profession = profession;
		member.PlayerName = playerName;
		YeZhanFengQiMemberDatas.Add(playerID, member);
	}
	else
	{
		YeZhanFengQiMemberDatas[playerID].Integral = integral;
		YeZhanFengQiMemberDatas[playerID].KillNum = killNum;
	}
}

void URoleActivityInterface::CLIENT_UpdateFengQiIntegralToOtherClient_Implementation(const int32& playerID, const int32& integral)
{
	if (YeZhanFengQiMemberDatas.Contains(playerID))
	{
		YeZhanFengQiMemberDatas[playerID].Integral = integral;
	}
	YeZhanFengQiMemberDatas.ValueSort([](const FSPACEYEZHANFENGQI& FengQiA, const FSPACEYEZHANFENGQI& FengQiB) {return FengQiA.Integral > FengQiB.Integral; });
}

void URoleActivityInterface::CLIENT_UpdateFengQiKillDataToOtherClient_Implementation(const int32& playerID, const int32& killNum)
{
	if (YeZhanFengQiMemberDatas.Contains(playerID))
	{
		YeZhanFengQiMemberDatas[playerID].KillNum = killNum;
	}
}

void URoleActivityInterface::CLIENT_ShowFengQiRank_Implementation()
{

}

void URoleActivityInterface::CLIENT_ShowOriginArea_Implementation(const FVector& upLeftOriginPos, const FVector& upRightOriginPos, const FVector& downLeftOriginPos, const FVector& downRightOriginPos)
{
	OriginPosList.Empty();
	OriginPosList.Add(upLeftOriginPos);
	OriginPosList.Add(upRightOriginPos);
	OriginPosList.Add(downLeftOriginPos);
	OriginPosList.Add(downRightOriginPos);
}

void URoleActivityInterface::CLIENT_ShowEndArea_Implementation(const FVector& upLeftEndPos, const FVector& upRightEndPos, const FVector& downLeftEndPos, const FVector& downRightEndPos)
{
	EndPosList.Empty();
	EndPosList.Add(upLeftEndPos);
	EndPosList.Add(upRightEndPos);
	EndPosList.Add(downLeftEndPos);
	EndPosList.Add(downRightEndPos);
}

void URoleActivityInterface::CLIENT_StartReduceArea_Implementation(float totalUseTime)
{

}

void URoleActivityInterface::CLIENT_UpdateFengQiMemberDataToOtherOnLogin_Implementation(const int32& srcMemberID, const int32& dstMemberID)
{
	if (YeZhanFengQiMemberDatas.Contains(srcMemberID))
	{
		FSPACEYEZHANFENGQI memberData = YeZhanFengQiMemberDatas[srcMemberID];
		YeZhanFengQiMemberDatas.Remove(srcMemberID);
		YeZhanFengQiMemberDatas.Add(dstMemberID, memberData);
	}
}
void URoleActivityInterface::CLIENT_ShowFirstWindow_Implementation(const FString& firstName)
{

}

void URoleActivityInterface::CLIENT_OnEnterLingMaiMatchQueue_Implementation()
{

}

void URoleActivityInterface::CLIENT_OnEnterLingMaiReadyQueue_Implementation()
{

}

void URoleActivityInterface::CLIENT_OnLingMaiActivityEnd_Implementation()
{

}

void URoleActivityInterface::CLIENT_AddLingMaiMember_Implementation(const int32& PlayerID, const FString& Name, const int32& camp)
{
	FLingMaiData data;
	data.id = PlayerID;
	data.name = Name;
	data.camp = camp;
	data.kill = 0;
	data.dead = 0;
	data.assist = 0;
	data.occupy = 0;
	data.grab = 0;
	LingMaiActivityData.Add(PlayerID, data);
}

void URoleActivityInterface::CLIENT_OnLeaveLingMai_Implementation()
{
	LingMaiActivityData.Empty();
	TaosimPownerPoint = 0;
	DemonPownerPoint = 0;
	for (auto It = PagodaTimerDict.CreateIterator(); It; ++It)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(It.Value());
	}
	PagodaTimerDict.Empty();
	for (auto It = LingMaiOccupyLingMais.CreateIterator(); It; ++It) 
	{
		It.Value().Empty();
	}
	LingMaiOccupyLingMais.Empty();
	LingMaiOccupyPagodas.Empty();

}

void URoleActivityInterface::CLIENT_ShowLingMaiLife_Implementation(const FString& Time)
{

}

void URoleActivityInterface::CLIENT_OnKillLingMai_Implementation(const int32& DiePlayerID, const int32& KillerID)
{
	if (LingMaiActivityData.Contains(KillerID))
	{
		LingMaiActivityData[KillerID].kill += 1;
		LingMaiActivityData.ValueSort([](const FLingMaiData& A, const FLingMaiData& B) {return A.kill > B.kill; });
		if (LingMaiActivityData[KillerID].camp == 1)
		{
			TaosimPownerPoint += 2;
		}
		else
		{
			DemonPownerPoint += 2;
		}
		CLIENT_OnPowerPointChange(TaosimPownerPoint, DemonPownerPoint);
	}
	if (LingMaiActivityData.Contains(DiePlayerID))
	{
		
		LingMaiActivityData[DiePlayerID].dead += 1;
		
	}
}

void URoleActivityInterface::CLIENT_OnAssistsLingMai_Implementation(const TArray<int32>& PlayerIDList)
{
	for (int32 id : PlayerIDList)
	{
		if (LingMaiActivityData.Contains(id))
		{
			LingMaiActivityData[id].assist += 1;
		}
	}
}

void URoleActivityInterface::CLIENT_OccupyPagodaBase_Implementation(const int32& PlayerID)
{
	if (LingMaiActivityData.Contains(PlayerID))
	{
		LingMaiActivityData[PlayerID].occupy += 1;
	}
}

void URoleActivityInterface::CLIENT_OccupyPagoda_Implementation(const FString& ScriptID, const int32& Camp)
{
	FString campStr(TEXT("蓝方"));
	FString pagodaStr(TEXT("极阳"));
	LingMaiOccupyPagodas.Add(Camp, ScriptID);
	if (Camp == 2)
	{
		campStr = TEXT("红方");
	}
	if (ScriptID.Equals("40000137"))
	{
		pagodaStr = TEXT("极阴");
	}
	UGolbalBPFunctionLibrary::StatusMessage(4145, campStr + "|" + pagodaStr);
}

void URoleActivityInterface::CLIENT_OccupyLingMai_Implementation(const FString& ScriptID, const int32& Camp, const int32& TaosimPoint, const int32& DemonPoint, const TArray<int32>& AssistAttack)
{
	CLIENT_OnPowerPointChange(TaosimPoint, DemonPoint);
	if (PagodaTimerDict.Contains(ScriptID))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(PagodaTimerDict[ScriptID]);
	}

	FTimerHandle Timer;
	FString campStr;
	if (Camp == 1)
	{
		campStr = TEXT("蓝方");
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(Timer, this, &URoleActivityInterface::AddTaosimPointPerSecond, 1.0, true);
		if (LingMaiOccupyLingMais.Contains(2)) 
		{
			if(LingMaiOccupyLingMais[2].Contains(ScriptID)) 
			{
				LingMaiOccupyLingMais[2].Remove(ScriptID);
			}
		}
	}
	else if (Camp == 2)
	{
		campStr = TEXT("红方");
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(Timer, this, &URoleActivityInterface::AddDemonPointPerSecond, 1.0, true);
		if (LingMaiOccupyLingMais.Contains(1))
		{
			if (LingMaiOccupyLingMais[1].Contains(ScriptID))
			{
				LingMaiOccupyLingMais[1].Remove(ScriptID);
			}
		}
	}
	PagodaTimerDict.Add(ScriptID, Timer);
	if (LingMaiOccupyLingMais.Contains(Camp))
	{
		LingMaiOccupyLingMais[Camp].AddUnique(ScriptID);
	}
	else
	{
		LingMaiOccupyLingMais.Add(Camp, { ScriptID });
	}
	FString direction;
	if (ScriptID.Equals("20006563"))
	{
		direction = TEXT("北部");
	}
	else if (ScriptID.Equals("20006564"))
	{
		direction = TEXT("中部");
	}
	else if (ScriptID.Equals("20006565"))
	{
		direction = TEXT("南部");
	}
	UGolbalBPFunctionLibrary::StatusMessage(4144, campStr + "|" + direction);

	for (auto id : AssistAttack)
	{
		if (LingMaiActivityData.Contains(id))
		{
			LingMaiActivityData[id].occupy += 1;
		}
	}
}

void URoleActivityInterface::CLIENT_OnGrabGourdLeave_Implementation(const int32& PlayerID, const int32& TaosimPoint, const int32& DemonPoint)
{
	CLIENT_OnPowerPointChange(TaosimPoint, DemonPoint);
	if (LingMaiActivityData.Contains(PlayerID))
	{
		LingMaiActivityData[PlayerID].grab += 1;
		FString campStr(TEXT("蓝方"));
		if (LingMaiActivityData[PlayerID].camp == 2)
		{
			campStr = TEXT("红方");
		}
		UGolbalBPFunctionLibrary::StatusMessage(4143, campStr + "|" + LingMaiActivityData[PlayerID].name);
	}
}

void URoleActivityInterface::CLIENT_OnPowerPointChange_Implementation(const int32& TaosimPoint, const int32& DemonPoint)
{
	TaosimPownerPoint = TaosimPoint;
	DemonPownerPoint = DemonPoint;
}

void URoleActivityInterface::CLIENT_OnWinGameLingMai_Implementation(const int32& Camp, const int32& LeftTime, const int32& TaosimPoint, const int32& DemonPoint)
{
	for (auto It = PagodaTimerDict.CreateIterator(); It; ++It)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(It.Value());
	}
	PagodaTimerDict.Empty();
	CLIENT_OnPowerPointChange(TaosimPoint, DemonPoint);
}

void URoleActivityInterface::CLIENT_OnEndLegendary_Implementation(const FString& Name)
{

}

TArray<FString> URoleActivityInterface::GetOccupyLingMaisByCamp(int32 Camp)
{
	TArray<FString> OccupyLingMais;
	OccupyLingMais.Empty();
	if (LingMaiOccupyLingMais.Contains(Camp))
	{
		OccupyLingMais = LingMaiOccupyLingMais[Camp];
	}
	return OccupyLingMais;	
}

bool URoleActivityInterface::IsLingMaiOccupyByCamp(int32 Camp, FString LingMaiScriptID)
{
	bool IsOccupyByCamp = false;
	if (LingMaiOccupyLingMais.Contains(Camp))
	{
		IsOccupyByCamp = LingMaiOccupyLingMais[Camp].Contains(LingMaiScriptID);
	}
	return IsOccupyByCamp;
}

void URoleActivityInterface::CLIENT_UpdateYXLMMemberDataToOtherClient_Implementation(const int32& roleID, const FString& roleName, const int32& roleCamp, const int32& roleKill, const int32& roleBeKill, const TArray<int32>& roleItemIDList)
{
	AddYXLMMemberData(roleID, roleName, roleCamp, roleKill, roleBeKill, roleItemIDList);
}

void URoleActivityInterface::CLIENT_ReceiveYXLMOtherMemberData_Implementation(const int32& roleID, const FString& roleName, const int32& roleCamp, const int32& roleKill, const int32& roleBeKill, const TArray<int32>& roleItemIDList)
{
	AddYXLMMemberData(roleID, roleName, roleCamp, roleKill, roleBeKill, roleItemIDList);
}

void URoleActivityInterface::CLIENT_UpdateYXLMKillDataToOtherClient_Implementation(const int32& roleID, const int32& roleKill)
{
	if (YXLMMemberDatas.Contains(roleID))
	{
		YXLMMemberDatas[roleID].Kill = roleKill;
	}
}

void URoleActivityInterface::CLIENT_UpdateYXLMBeKillDataToOtherClient_Implementation(const int32& roleID, const int32& roleBeKill)
{
	if (YXLMMemberDatas.Contains(roleID))
	{
		YXLMMemberDatas[roleID].BeKill = roleBeKill;
	}
}

void URoleActivityInterface::CLIENT_UpdateYXLMAddItemToOtherClient_Implementation(const int32& roleID, const int32& itemID)
{
	if (YXLMMemberDatas.Contains(roleID))
	{
		YXLMMemberDatas[roleID].ItemIDList.Add(itemID);
	}
}

void URoleActivityInterface::CLIENT_UpdateYXLMRemoveItemToOtherClient_Implementation(const int32& roleID, const int32& itemID)
{
	if (YXLMMemberDatas.Contains(roleID))
	{
		for (auto hasItemID : YXLMMemberDatas[roleID].ItemIDList)
		{
			if (hasItemID == itemID)
			{
				YXLMMemberDatas[roleID].ItemIDList.Remove(itemID);
				break;
			}
		}
	}
}

void URoleActivityInterface::AddYXLMMemberData(const int32& roleID, const FString& roleName, const int32& roleCamp, const int32& roleKill, const int32& roleBeKill, const TArray<int32>& roleItemIDList)
{
	if (!YXLMMemberDatas.Contains(roleID))
	{
		FSPACEYXLMDATA YXLMData;
		YXLMData.BeKill = roleBeKill;
		YXLMData.Camp = roleCamp;
		YXLMData.Kill = roleKill;
		YXLMData.PlayerName = roleName;
		for (auto itemID : roleItemIDList)
		{
			YXLMData.ItemIDList.Add(itemID);
		}
		YXLMMemberDatas.Add(roleID, YXLMData);
	}
}

void URoleActivityInterface::CampYXLMonAffirm(int32 result)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::CampYXLMonAffirm : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(result);
	GetEntity()->BaseCall(TEXT("campYXLMonAffirm"), args);
}

void URoleActivityInterface::CampYXLMCancelSignUp()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::CampYXLMCancelSignUp : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->BaseCall(TEXT("campYXLMCancelSignUp"), args);
}

void URoleActivityInterface::CLIENT_ShowEnterYXLMTime_Implementation(float enterTime)
{

}

void URoleActivityInterface::CLIENT_CampYXLMOnMatchSuccess_Implementation()
{

}

void URoleActivityInterface::CLIENT_CampYXLMHideAffirmWindow_Implementation()
{

}

void URoleActivityInterface::CLIENT_CampYXLMUpdateWaitAffirmList_Implementation(const TArray<int32>& idList)
{

}

void URoleActivityInterface::CLIENT_CampYXLMShowAffirmData_Implementation(const FString& affirmData)
{
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnValue = temp->FromString(affirmData);
	auto tempArray = returnValue->GetObjectArray(this, TEXT("ROOT"));
	for (auto item : tempArray)
	{
		auto xianTeamItemArray = item->GetObjectArray(this, TEXT("xianTeamData"));
		auto moTeamItemArray = item->GetObjectArray(this, TEXT("moTeamData"));
		for (auto xianItem : xianTeamItemArray)
		{
			FYXLMMATCHDATA matchData;
			matchData.Camp = FSTRING_TO_INT(xianItem->GetString(TEXT("camp")));
			matchData.Id = FSTRING_TO_INT(xianItem->GetString(TEXT("id")));
			matchData.Level = FSTRING_TO_INT(xianItem->GetString(TEXT("level")));
			matchData.Name = xianItem->GetString(TEXT("name"));
			YXLMXianTeamData.Add(matchData);
		}
		for (auto moItem : moTeamItemArray)
		{
			FYXLMMATCHDATA matchData;
			matchData.Camp = FSTRING_TO_INT(moItem->GetString(TEXT("camp")));
			matchData.Id = FSTRING_TO_INT(moItem->GetString(TEXT("id")));
			matchData.Level = FSTRING_TO_INT(moItem->GetString(TEXT("level")));
			matchData.Name = moItem->GetString(TEXT("name"));
			YXLMMoTeamData.Add(matchData);
		}
	}
}

void URoleActivityInterface::CLIENT_UpdateYXLMMemberDataToOtherOnLogin_Implementation(const int32& srcMemberID, const int32& dstMemberID)
{
	if (YXLMMemberDatas.Contains(srcMemberID))
	{
		FSPACEYXLMDATA memberData = YXLMMemberDatas[srcMemberID];
		YXLMMemberDatas.Remove(srcMemberID);
		YXLMMemberDatas.Add(dstMemberID, memberData);
	}
}

void URoleActivityInterface::CLIENT_ShowYXLMBattlefieldWin_Implementation(const int32& winCamp, const int32& rewardExp)
{

}
void URoleActivityInterface::CLIENT_CampYXLMSignUpSuccess_Implementation()
{
	YXLMXianTeamData.Empty();
	YXLMMoTeamData.Empty();
}

void URoleActivityInterface::CELL_YXLMBackToCity()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::CELL_YXLMBackToCity : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("CELL_YXLMBackToCity"), args);
}

void URoleActivityInterface::CLIENT_ShowYXLMRandomScriptIDs_Implementation(const FString& jsonData)
{
	YXLMRandomScriptIDDatas.Empty();
	UJsonFieldData* fieldData = UJsonFieldData::Create(this);
	auto returnValue = fieldData->FromString(jsonData);
	auto datas = returnValue->GetObjectArray(this,TEXT("ROOT"));
	if (!datas.Num()) return;
	TArray<FString> keys = datas[0]->GetObjectKeys(this);
	for (auto key: keys)
	{
		int32 value = FSTRING_TO_INT(datas[0]->GetString(key));
		YXLMRandomScriptIDDatas.Add(key, value);
	}
}
void URoleActivityInterface::CELL_YXLMBuyRandomScriptID(const FString& scriptID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::CELL_YXLMBuyRandomScriptID : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(scriptID);
	GetEntity()->CellCall(TEXT("CELL_YXLMBuyRandomScriptID"), args);
}



void URoleActivityInterface::CLIENT_showEnemyPos_Implementation(const TArray<FVector>& enemyMemberPos)
{
	
}

void URoleActivityInterface::CLIENT_HideEnemyPos_Implementation()
{

}

void URoleActivityInterface::ClearYXLMMemberData()
{
	YXLMMemberDatas.Empty();
	YXLMRandomScriptIDDatas.Empty();
	YXLMXianTeamData.Empty();
	YXLMMoTeamData.Empty();
	
}

void URoleActivityInterface::TongStarcraft_firstSignUp(TArray<FString> firstTeamNames, TArray<FString> secondTeamNames, TArray<FString> thirdTeamNames, TArray<FString> fourTeamNames)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::TongStarcraft_firstSignUp : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(firstTeamNames));
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(secondTeamNames));
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(thirdTeamNames));
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(fourTeamNames));
	GetEntity()->CellCall(TEXT("tongStarcraft_firstSignUp"), args);
}

void URoleActivityInterface::CLIENT_ShowTongMemberWindow_Implementation(const int32& number)
{

}

void URoleActivityInterface::CLIENT_ShowTongSignSuccessWindow_Implementation(const FString& signData)
{
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnValue = temp->FromString(signData);
	auto tempArray = returnValue->GetObjectArray(this, TEXT("ROOT"));
	for (auto data:tempArray)
	{
		FFIRST_TONGSTARCRAFT_SIGNDATA tongSignData;
		tongSignData.TongName = data->GetString(TEXT("tongName"));
		tongSignData.TongLevel = FSTRING_TO_INT(data->GetString(TEXT("tongLevel")));
		FirstTongStarcraftSignDatas.Add(tongSignData);
	}
}

void URoleActivityInterface::CLIENT_ShowPassFirstTongStarcraft_Implementation(const FString& passData)
{
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnValue = temp->FromString(passData);
	auto tempArray = returnValue->GetObjectArray(this, TEXT("ROOT"));
	for (auto data : tempArray)
	{
		FFIRST_TONGSTARCRAFT_PASSDATA tongPassData;
		tongPassData.TongName = data->GetString(TEXT("tongName"));
		tongPassData.TongLevel = FSTRING_TO_INT(data->GetString(TEXT("tongLevel")));
		tongPassData.PassTime = FSTRING_TO_INT(data->GetString(TEXT("passTime")));
		FirstTongStarcraftPassDatas.Add(tongPassData);
	}
}
void URoleActivityInterface::CLIENT_UpdateMemberIntegral_Implementation(const int32& playerID, const int32& integral)
{
	if (MemberIntegralMap.Contains(playerID))
	{
		MemberIntegralMap[playerID] = integral;
	}
	else
	{
		MemberIntegralMap.Add(playerID, integral);
	}
}

void URoleActivityInterface::CLIENT_UpdateTongIntegral_Implementation(const FString& tongName, const int32& tongIntegral)
{
	if (TongIntegralMap.Contains(tongName))
	{
		TongIntegralMap[tongName] = tongIntegral;
	}
	else
	{
		TongIntegralMap.Add(tongName, tongIntegral);
	}
	TongIntegralMap.ValueSort([](const int32& IntegralA, const int32& IntegralB) {return IntegralA > IntegralB;});
}
void URoleActivityInterface::CLIENT_OpenSecondTongStarcraftGroup_Implementation(const TArray<FString>& firstGroupNames, const TArray<FString>& secondGroupNames)
{

}
void URoleActivityInterface::ShowTongStarcraftFirstSignUpTong_Implementation(const TArray<FString>& firstGroupNames, const TArray<FString>& secondGroupNames)
{

}
void URoleActivityInterface::TongStarcraft_SecondSignUp(TArray<FString> signUpNames)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::TongStarcraft_SecondSignUp : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(signUpNames));
	GetEntity()->CellCall(TEXT("tongStarcraft_SecondSignUp"), args);
}

void URoleActivityInterface::firstTongStarcraftSignUp(TArray<FString> signUpPlayerNames)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::firstTongStarcraftSignUp : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(signUpPlayerNames));
	GetEntity()->CellCall(TEXT("firstTongStarcraftSignUp"), args);
}

void URoleActivityInterface::UpdateTongStarcraftLoginMemToOtherClient_Implementation(const int32 & srcEntityID, const int32 & dstEntityID)
{
	if (MemberIntegralMap.Contains(srcEntityID))
	{
		int32 integral = MemberIntegralMap[srcEntityID];
		MemberIntegralMap.Remove(srcEntityID);
		MemberIntegralMap.Add(dstEntityID, integral);
	}
}

TArray<FString> URoleActivityInterface::GetThirdTongStarcraftOccupySpellBoxByTongSide(int32 tongSide)
{
	if (ThirdTongOccupyBoxMap.Contains(tongSide))
	{
		return ThirdTongOccupyBoxMap[tongSide];
	}
	TArray<FString> tempBoxScirpIDs;
	return tempBoxScirpIDs;
}

FTHIRD_TONGSTARCRAFT_MEMBERDATA URoleActivityInterface::GetThirdTongStarcraftMemberData(int32 tongSide, int32 roleID)
{
	if (ThirdTongMemberDict.Contains(tongSide))
	{
		if (ThirdTongMemberDict[tongSide].Contains(roleID))
		{
			return ThirdTongMemberDict[tongSide][roleID];
		}
	}
	FTHIRD_TONGSTARCRAFT_MEMBERDATA memberData;
	return memberData;
}

TMap<int32, FTHIRD_TONGSTARCRAFT_MEMBERDATA> URoleActivityInterface::GetThirdTongStarcraftAllMemberData(int32 tongSide)
{
	if (ThirdTongMemberDict.Contains(tongSide))
	{
		return ThirdTongMemberDict[tongSide];
	}
	TMap<int32, FTHIRD_TONGSTARCRAFT_MEMBERDATA> memberData;
	return memberData;
}

void URoleActivityInterface::AddThirdTongStarcraftMember(const int32& tongSide, const int32& roleID, const FString& roleName, const int32& kill, const int32& beKill, const int32& assists, const int32& occupy)
{
	if (ThirdTongMemberDict.Contains(tongSide))
	{
		if (ThirdTongMemberDict[tongSide].Contains(roleID))
		{
			ThirdTongMemberDict[tongSide][roleID].Kill = kill;
			ThirdTongMemberDict[tongSide][roleID].BeKill = beKill;
			ThirdTongMemberDict[tongSide][roleID].Assists = assists;
			ThirdTongMemberDict[tongSide][roleID].Occupy = occupy;
			return;
		}
		else
		{
			FTHIRD_TONGSTARCRAFT_MEMBERDATA memberData;
			memberData.RoleID = roleID;
			memberData.RoleName = roleName;
			memberData.Kill = kill;
			memberData.BeKill = beKill;
			memberData.Assists = assists;
			memberData.Occupy = occupy;
			memberData.TongSide = tongSide;
			ThirdTongMemberDict[tongSide].Add(roleID, memberData);
		}
	}
	else
	{
		FTHIRD_TONGSTARCRAFT_MEMBERDATA memberData;
		memberData.RoleID = roleID;
		memberData.RoleName = roleName;
		memberData.Kill = kill;
		memberData.BeKill = beKill;
		memberData.Assists = assists;
		memberData.Occupy = occupy;
		memberData.TongSide = tongSide;
		TMap<int32, FTHIRD_TONGSTARCRAFT_MEMBERDATA> memberMap;
		memberMap.Add(roleID, memberData);
		ThirdTongMemberDict.Add(tongSide, memberMap);
	}
}

void URoleActivityInterface::CLIENT_ReceiveAllThirdTongStarcraftMemberData_Implementation(const int32& tongSide, const int32& roleID, const FString& roleName, const int32& kill, const int32& beKill, const int32& assists, const int32& occupy)
{
	AddThirdTongStarcraftMember(tongSide, roleID, roleName, kill, beKill, assists, occupy);
}

void URoleActivityInterface::CLIENT_UpdateThirdTongStarcraftMemToOtherClient_Implementation(const int32& tongSide, const int32& roleID, const FString& roleName, const int32& kill, const int32& beKill, const int32& assists, const int32& occupy)
{
	AddThirdTongStarcraftMember(tongSide, roleID, roleName, kill, beKill, assists, occupy);
}

void URoleActivityInterface::CLIENT_UpdateThirdTongStarcraftLoginMemToOtherClient_Implementation(const int32& tongSide, const int32& srcRoleID, const int32& dstRoleID)
{
	if (ThirdTongMemberDict.Contains(tongSide))
	{
		if (ThirdTongMemberDict[tongSide].Contains(srcRoleID))
		{
			FTHIRD_TONGSTARCRAFT_MEMBERDATA memberData = ThirdTongMemberDict[tongSide][srcRoleID];
			ThirdTongMemberDict[tongSide].Remove(srcRoleID);
			memberData.RoleID = dstRoleID;
			ThirdTongMemberDict[tongSide].Add(dstRoleID, memberData);
		}
	}
}

void URoleActivityInterface::CLIENT_UpdateThirdTongStarcraftMemKill_Implementation(const int32& tongSide, const int32& roleID, const int32& kill)
{
	if (ThirdTongMemberDict.Contains(tongSide))
	{
		if (ThirdTongMemberDict[tongSide].Contains(roleID))
		{
			ThirdTongMemberDict[tongSide][roleID].Kill = kill;
		}
	}
}

void URoleActivityInterface::CLIENT_UpdateThirdTongStarcraftMemBeKill_Implementation(const int32& tongSide, const int32& roleID, const int32& beKill)
{
	if (ThirdTongMemberDict.Contains(tongSide))
	{
		if (ThirdTongMemberDict[tongSide].Contains(roleID))
		{
			ThirdTongMemberDict[tongSide][roleID].BeKill = beKill;
		}
	}
}

void URoleActivityInterface::CLIENT_UpdateThirdTongStarcraftMemAssists_Implementation(const int32& tongSide, const int32& roleID, const int32& assists)
{
	if (ThirdTongMemberDict.Contains(tongSide))
	{
		if (ThirdTongMemberDict[tongSide].Contains(roleID))
		{
			ThirdTongMemberDict[tongSide][roleID].Assists = assists;
		}
	}
}

void URoleActivityInterface::CLIENT_UpdateThirdTongStarcraftMemOccupy_Implementation(const int32& tongSide, const int32& roleID, const int32& occupy)
{
	if (ThirdTongMemberDict.Contains(tongSide))
	{
		if (ThirdTongMemberDict[tongSide].Contains(roleID))
		{
			ThirdTongMemberDict[tongSide][roleID].Occupy = occupy;
		}
	}
}

void URoleActivityInterface::CLIENT_ShowThirdTongStarcraftLife_Implementation(const FString& spaceLife)
{

}

void URoleActivityInterface::CLIENT_ShowWinTong_Implementation(const int32& isWin)
{

}

void URoleActivityInterface::CLIENT_ReceiveThirdTongStarcraftAllOccupySpellBox_Implementation(const int32& tongSide, const TArray<FString>& boxScriptIDs)
{
	if (ThirdTongOccupyBoxMap.Contains(tongSide))
	{
		ThirdTongOccupyBoxMap.Remove(tongSide);
	}
	ThirdTongOccupyBoxMap.Add(tongSide, boxScriptIDs);
}

void URoleActivityInterface::CLIENT_AddThirdTongStarcraftOccupySpellBox_Implementation(const int32& tongSide, const FString& boxScriptID)
{
	if (ThirdTongOccupyBoxMap.Contains(tongSide))
	{
		if (!ThirdTongOccupyBoxMap[tongSide].Contains(boxScriptID))
		{
			ThirdTongOccupyBoxMap[tongSide].Add(boxScriptID);
		}
	}
	else
	{
		TArray<FString> tempBoxScirpIDs;
		tempBoxScirpIDs.Add(boxScriptID);
		ThirdTongOccupyBoxMap.Add(tongSide, tempBoxScirpIDs);
	}	
}

void URoleActivityInterface::CLIENT_RemoveThirdTongStarcraftOccupySpellBox_Implementation(const int32& tongSide, const FString& boxScriptID)
{
	if (ThirdTongOccupyBoxMap.Contains(tongSide) && ThirdTongOccupyBoxMap[tongSide].Contains(boxScriptID))
	{
		ThirdTongOccupyBoxMap[tongSide].Remove(boxScriptID);
	}
}

void URoleActivityInterface::CLIENT_UpdateThirdTongStarcraftIntegral_Implementation(const int32& tongSide, const int32& tongIntegral)
{
	if (ThirdTongIntegralMap.Contains(tongSide))
	{
		ThirdTongIntegralMap[tongSide] = tongIntegral;
	}
}
void URoleActivityInterface::CLIENT_ReceiveAllThirdTongStarcraftIntegral_Implementation(const int32& tongSide, const FString& tongName,const int32& tongIntegral)
{
	if (ThirdTongIntegralMap.Contains(tongSide))
	{
		ThirdTongIntegralMap[tongSide] = tongIntegral;
	}
	else
	{
		ThirdTongIntegralMap.Add(tongSide, tongIntegral);
	}
	if (ThirdTongNameMap.Contains(tongSide))
	{
		ThirdTongNameMap[tongSide] = tongName;
	}
	else
	{
		ThirdTongNameMap.Add(tongSide, tongName);
	}
}

//冰雪之战
void URoleActivityInterface::CLIENT_OnEnterFrozenFightMatchQueue_Implementation()
{

}

void URoleActivityInterface::CLIENT_OnEnterFrozenFightReadyQueue_Implementation()
{

}

void URoleActivityInterface::CLIENT_OnFrozenFightActivityEnd_Implementation()
{

}

void URoleActivityInterface::CLIENT_OnEnterFrozenFightTelPortQueue_Implementation(const int32& Key)
{

}

void URoleActivityInterface::CLIENT_AddFrozenFightMember_Implementation(const int32& PlayerID, const FString& Name, const int32& camp)
{
	FFrozenFightData data;
	data.id = PlayerID;
	data.name = Name;
	data.camp = camp;
	data.kill = 0;
	data.dead = 0;
	data.assist = 0;
	data.occupy = 0;
	data.submits = 0;
	FrozenFightActivityData.Add(PlayerID, data);
}

void URoleActivityInterface::CLIENT_OnLeaveFrozenFight_Implementation()
{
	FrozenFightActivityData.Empty();
}

void URoleActivityInterface::CLIENT_ShowFrozenFightLife_Implementation(const FString& Time)
{

}

void URoleActivityInterface::CLIENT_OnKillFrozenFight_Implementation(const int32& DiePlayerID, const int32& KillerID)
{
	if (FrozenFightActivityData.Contains(DiePlayerID) && FrozenFightActivityData.Contains(KillerID))
	{
		FrozenFightActivityData[KillerID].kill += 1;
		FrozenFightActivityData[DiePlayerID].dead += 1;
	}
}

void URoleActivityInterface::CLIENT_OnAssistsFrozenFight_Implementation(const TArray<int32>& PlayerIDList)
{
	for (int32 id : PlayerIDList)
	{
		if (FrozenFightActivityData.Contains(id))
		{
			FrozenFightActivityData[id].assist += 1;
		}
	}
}


void URoleActivityInterface::CLIENT_OnFrozenFightOccupyTower_Implementation(const FString& ScriptID, const int32& PlayerCamp, const int32& PlayerID)
{
	FString campStr(TEXT("魔道"));
	FString towerStr(TEXT("西侧"));
	if (PlayerCamp == 1)
	{
		campStr = TEXT("仙道");
	}
	if (ScriptID == "40000172")
	{
		towerStr = TEXT("东侧");
	}
	UGolbalBPFunctionLibrary::StatusMessage(4232, campStr + "|" + towerStr);

	if (FrozenFightActivityData.Contains(PlayerID))
	{
		FrozenFightActivityData[PlayerID].occupy += 1;
	}
}

void URoleActivityInterface::CLIENT_OnFrozenFightOccupyRivivePos_Implementation(const FString& ScriptID, const int32& PlayerCamp,  const int32& PlayerID)
{

	FString campStr;
	if (PlayerCamp == 1)
	{
		campStr = TEXT("仙道");
		
	}
	else if (PlayerCamp == 2)
	{
		campStr = TEXT("魔道");
		
	}

	FString direction;
	if (ScriptID.Equals("40000173"))
	{
		direction = TEXT("西侧");
	}
	else if (ScriptID.Equals("40000174"))
	{
		direction = TEXT("东侧");
	}
	else if (ScriptID.Equals("40000175"))
	{
		direction = TEXT("中心");
	}
	UGolbalBPFunctionLibrary::StatusMessage(4231, campStr + "|" + direction);

	if (FrozenFightActivityData.Contains(PlayerID))
	{
		FrozenFightActivityData[PlayerID].occupy += 1;
	}
}



void URoleActivityInterface::CLIENT_OnFrozenFightPointChanged_Implementation(const int32& TaosimPoint, const int32& DemonPoint)
{

}

void URoleActivityInterface::CLIENT_OnFrozenFightSubmit_Implementation(const int32& playerID, const int32& submits)
{

	if (FrozenFightActivityData.Contains(playerID))
	{
		FrozenFightActivityData[playerID].submits = submits;
	}
}


void URoleActivityInterface::CLIENT_OnWinGameFrozenFight_Implementation(int32 WinnerCamp, int32 WinnerPoint, int32 LoserPoint, int32 Duration)
{

}

void URoleActivityInterface::CancelMatchFrozenFight()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::CancelMatchFrozenFight : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->BaseCall(TEXT("cancelMatchFrozenFight"), args);
}

void URoleActivityInterface::BeginEnterFrozenFight(int32 key)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::BeginEnterFrozenFight : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(key);
	GetEntity()->BaseCall(TEXT("beginEnterFrozenFight"), args);
}

void URoleActivityInterface::Cell_leaveFrozenFight()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::Cell_leaveFrozenFight : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("leaveFrozenFight"), args);
}


void URoleActivityInterface::onLeaveWorld()
{
	integralMax = 0;
	moneyDatas.Empty();
	integralDatas.Empty();
	YeZhanFengQiMemberDatas.Empty();
	YXLMRandomScriptIDDatas.Empty();
	OriginPosList.Empty();
	EndPosList.Empty();
	passDataMap.Empty();
	for (auto It = PagodaTimerDict.CreateIterator(); It; ++It)
	{
		if (It.Value().IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(It.Value());
		}
	}
	PagodaTimerDict.Empty();
	YXLMMemberDatas.Empty();
	YXLMXianTeamData.Empty();
	YXLMMoTeamData.Empty();
	FirstTongStarcraftSignDatas.Empty();
	FirstTongStarcraftPassDatas.Empty();
	MemberIntegralMap.Empty();
	TongIntegralMap.Empty();
	ThirdTongIntegralMap.Empty();
	ThirdTongOccupyBoxMap.Empty();
	ThirdTongNameMap.Empty();
	ThirdTongMemberDict.Empty();
	SGMZXianTeamData.Empty();
	SGMZMoTeamData.Empty();
	TongCampWarSignUpMaxNumber = 0;
	Supper::onLeaveWorld();
}

void URoleActivityInterface::RPC_cancelMatchLingMai()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::RPC_cancelMatchLingMai : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->BaseCall(TEXT("cancelMatchLingMai"), args);
}

void URoleActivityInterface::RPC_beginEnterLingMai(const int32& INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::RPC_beginEnterLingMai : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);

	entity->BaseCall(TEXT("beginEnterLingMai"), args);
}

void URoleActivityInterface::CLIENT_ShowGoldTreeCompass_Implementation(const int32& Compass)
{

}

void URoleActivityInterface::CLIENT_ShowAreaInBigMapUI_Implementation(const FString& SpaceScriptID, const FVector& position, const float& Range)
{

}

void URoleActivityInterface::CLIENT_AddActivityCircleArea_Implementation(const FString& SpaceScriptID, const FVector& position, const float& Range, const int32& Index)
{
	UUECS3GameInstance::Instance->MapManager->AddActivityCircleArea(SpaceScriptID, position, Range, Index);
}

void URoleActivityInterface::CLIENT_ClearActivityCircleArea_Implementation()
{
	UUECS3GameInstance::Instance->MapManager->ClearActivityCircleArea();
}

void URoleActivityInterface::RPC_OnEnterActivityCircleArea(const int32& index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RPC_OnEnterActivityCircleArea no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT_TO_FSTRING(index));

	entity->CellCall(TEXT("CELL_onEnterActivityCircleArea"), args);
}

void URoleActivityInterface::RPC_OnLeaveActivityCircleArea(const int32& index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RPC_OnLeaveActivityCircleArea no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT_TO_FSTRING(index));

	entity->CellCall(TEXT("CELL_onLeaveActivityCircleArea"), args);
}
void URoleActivityInterface::CLIENT_beginJZYT_Implementation(const FString& RewardList, const FString& uid, const FString& SpaceStr)
{

}

void URoleActivityInterface::RPC_OnUseJZYT(const FString& uid, const FString& SpaceStr)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RPC_OnUseJZYT no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(uid);
	args.Add(SpaceStr);

	entity->CellCall(TEXT("CELL_onUseItemJZYT"), args);
}

void URoleActivityInterface::OnNotifyStartXKTB_Implementation(const FString& RewardList, const FString& uid, const FString& SpaceStr)
{
}

void URoleActivityInterface::NotifyRechargeableValue_Implementation(const float& rechargeableValue)
{
}

void URoleActivityInterface::RPC_onUseItemXKTB(const FString& uid, const FString& SpaceStr)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RPC_onUseItemXKTB no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(uid);
	args.Add(SpaceStr);
	entity->CellCall(TEXT("onUseItemXKTB"), args);
}

void URoleActivityInterface::CampSGMZSignUpSuccess_Implementation()
{
	SGMZXianTeamData.Empty();
	SGMZMoTeamData.Empty();
}

void URoleActivityInterface::CampSGMZOnMatchSuccess_Implementation()
{
}

void URoleActivityInterface::CampSGMZHideAffirmWindow_Implementation()
{
}

void URoleActivityInterface::CampSGMZShowAffirmData_Implementation(const FString& affirmData)
{
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnValue = temp->FromString(affirmData);
	auto tempArray = returnValue->GetObjectArray(this, TEXT("ROOT"));
	for (auto item : tempArray)
	{
		auto xianTeamItemArray = item->GetObjectArray(this, TEXT("xianTeamData"));
		auto moTeamItemArray = item->GetObjectArray(this, TEXT("moTeamData"));
		for (auto xianItem : xianTeamItemArray)
		{
			FSGMZMATCHDATA matchData;
			matchData.Camp = FSTRING_TO_INT(xianItem->GetString(TEXT("camp")));
			matchData.Id = FSTRING_TO_INT(xianItem->GetString(TEXT("id")));
			matchData.Level = FSTRING_TO_INT(xianItem->GetString(TEXT("level")));
			matchData.Name = xianItem->GetString(TEXT("name"));
			matchData.Profession = FSTRING_TO_INT(xianItem->GetString(TEXT("profession")));
			SGMZXianTeamData.Add(matchData);
		}
		for (auto moItem : moTeamItemArray)
		{
			FSGMZMATCHDATA matchData;
			matchData.Camp = FSTRING_TO_INT(moItem->GetString(TEXT("camp")));
			matchData.Id = FSTRING_TO_INT(moItem->GetString(TEXT("id")));
			matchData.Level = FSTRING_TO_INT(moItem->GetString(TEXT("level")));
			matchData.Name = moItem->GetString(TEXT("name"));
			matchData.Profession = FSTRING_TO_INT(moItem->GetString(TEXT("profession")));
			SGMZMoTeamData.Add(matchData);
		}
	}
}

void URoleActivityInterface::ShowEnterSGMZTime_Implementation(float enterTime)
{
}

void URoleActivityInterface::RPC_CampSGMZCancelSignUp()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::RPC_CampSGMZCancelSignUp : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->BaseCall(TEXT("campSGMZCancelSignUp"), args);
}

void URoleActivityInterface::RPC_CampSGMZOnAffirmp(const int32& result)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::RPC_CampSGMZOnAffirmp : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(result);
	GetEntity()->BaseCall(TEXT("campSGMZOnAffirm"), args);
}

void URoleActivityInterface::OnQueryTongSignUpData_Implementation(const TArray<FString>& signUpMemberNames, const int32& signUpMaxNumber)
{
	TongCampWarSignUpMaxNumber = signUpMaxNumber;
}
void URoleActivityInterface::TongCampWarSignUp(const TArray<FString>& signUpMemberNames)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::TongCampWarSignUp : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(signUpMemberNames));
	GetEntity()->CellCall(TEXT("tongCampWarSignUp"), args);
}

void URoleActivityInterface::CLIENT_beginTJP_Implementation(const FString& RewardList, const FString& uid, const FString& SpaceStr)
{

}

void URoleActivityInterface::RPC_OnUseTJP(const FString& uid, const FString& SpaceStr)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RPC_OnUseTJP no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(uid);
	args.Add(SpaceStr);

	entity->CellCall(TEXT("CELL_onUseItemTJP"), args);
}

void URoleActivityInterface::OnEnterFHLTMatchQueue_Implementation(const int32& Number)
{
}

void URoleActivityInterface::OnFHLTActivityEnd_Implementation()
{
}

void URoleActivityInterface::OnEnterFHLTReadyQueue_Implementation()
{
}

void URoleActivityInterface::OnEnterFHLTTelPortQueue_Implementation(const int32& Key)
{
}

void URoleActivityInterface::OnAddFHLTMember_Implementation(const int32& PlayerID, const FString& Name, const int32& camp)
{
	FFHLTMemberData data;
	data.id = PlayerID;
	data.name = Name;
	data.camp = camp;
	data.kill = 0;
	data.dead = 0;
	data.assist = 0;
	FHLTActivityData.Add(PlayerID, data);
}

void URoleActivityInterface::OnLeaveFHLT_Implementation()
{
	FHLTActivityData.Empty();
	TaosimIntegral = 0;
	DemonIntegral = 0;
}

void URoleActivityInterface::OnKillFHLT_Implementation(const int32& DiePlayerID, const int32& KillerID)
{
	if (FHLTActivityData.Contains(KillerID))
	{
		FHLTActivityData[KillerID].kill += 1;
		FHLTActivityData.ValueSort([](const FFHLTMemberData& A, const FFHLTMemberData& B) {return A.kill > B.kill; });
		if (FHLTActivityData[KillerID].camp == 1)
		{
			TaosimIntegral += 2;
		}
		else
		{
			DemonIntegral += 2;
		}
		OnIntegralChange(TaosimIntegral, DemonIntegral);
	}
	if (FHLTActivityData.Contains(DiePlayerID))
	{
		FHLTActivityData[DiePlayerID].dead += 1;
	}
}

void URoleActivityInterface::OnAssistsFHLT_Implementation(const TArray<int32>& PlayerIDList)
{
	for (int32 id : PlayerIDList)
	{
		if (FHLTActivityData.Contains(id))
		{
			FHLTActivityData[id].assist += 1;
		}
	}
}

void URoleActivityInterface::OnIntegralChange_Implementation(const int32& taosimIntegral, const int32& demonIntegral)
{
	TaosimIntegral = taosimIntegral;
	DemonIntegral = demonIntegral;
}

void URoleActivityInterface::OnWinGameFHLT_Implementation(const int32& Camp, const int32& taosimIntegral, const int32& demonIntegral)
{
	OnIntegralChange(taosimIntegral, demonIntegral);
}

void URoleActivityInterface::ShowFHLTLife_Implementation(const FString& Time)
{
}

void URoleActivityInterface::RPC_cancelMatchFHLT()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::RPC_cancelMatchFHLT : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("cancelMatchFHLT"), args);
}

void URoleActivityInterface::RPC_beginEnterFHLT(const int32& INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::RPC_beginEnterFHLT : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(INT32_1);
	entity->BaseCall(TEXT("beginEnterFHLT"), args);
}

void URoleActivityInterface::RPC_onLeaveActivityFHLTCopy()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleActivityInterface::RPC_onLeaveActivityFHLTCopy : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("onLeaveActivityFHLTCopy"), args);
}

void URoleActivityInterface::CLIENT_beginJXLC_Implementation(const FString & RewardList, const FString & uid, const FString & SpaceStr)
{
}

void URoleActivityInterface::RPC_OnUseWSYC(const FString & uid, const FString & SpaceStr)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RPC_OnUseWSYC no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(uid);
	args.Add(SpaceStr);

	entity->CellCall(TEXT("CELL_onUseItemWSYC"), args);
}

void URoleActivityInterface::CLIENT_AddCampYCJMDMember_Implementation(const int32 & PlayerID, const FString & Name, const int32 & camp)
{
	FCampYCJMDData data;
	data.id = PlayerID;
	data.name = Name;
	data.camp = camp;
	data.kill = 0;
	data.dead = 0;
	data.assist = 0;
	CampYCJMDActivityData.Add(PlayerID, data);
}

void URoleActivityInterface::CLIENT_OnLeaveCampYCJMD_Implementation()
{
	CampYCJMDActivityData.Empty();
}


void URoleActivityInterface::CLIENT_OnKillCampYCJMD_Implementation(const int32 & DiePlayerID, const int32 & KillerID)
{
	if (CampYCJMDActivityData.Contains(KillerID))
	{
		CampYCJMDActivityData[KillerID].kill += 1;
		CampYCJMDActivityData.ValueSort([](const FCampYCJMDData& A, const FCampYCJMDData& B) {return A.kill > B.kill; });
	}
	if (CampYCJMDActivityData.Contains(DiePlayerID))
	{
		CampYCJMDActivityData[DiePlayerID].dead += 1;
	}
}

void URoleActivityInterface::CLIENT_OnAssistsCampYCJMD_Implementation(const TArray<int32>& PlayerIDList)
{
	for (int32 id : PlayerIDList)
	{
		if (CampYCJMDActivityData.Contains(id))
		{
			CampYCJMDActivityData[id].assist += 1;
		}
	}
}

void URoleActivityInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_UpdateMoneyDataToOtherPlayer");
	ArrBlueFunc.Add("CLIENT_ReceiveOtherMoneyData");
	ArrBlueFunc.Add("CLIENT_UpdateIntegralDataToOtherClient");
	ArrBlueFunc.Add("CLIENT_ReceiveOtherIntegralData");
	ArrBlueFunc.Add("CLIENT_UpdateBeKillDataToOtherClient");
	ArrBlueFunc.Add("CLIENT_ReceiveOtherBeKillData");
	ArrBlueFunc.Add("CLIENT_UpdateKillDataToOtherClient");
	ArrBlueFunc.Add("CLIENT_ReceiveOtherKillData");
	ArrBlueFunc.Add("CLIENT_SetIntegralMax");
	ArrBlueFunc.Add("CLIENT_HunTingMemberLeave");
	ArrBlueFunc.Add("CLIENT_ShowRankList");
	ArrBlueFunc.Add("CLIENT_OnGodLike");
	ArrBlueFunc.Add("CLIENT_OnFirstKill");
	ArrBlueFunc.Add("CLIENT_OnClearData");
	ArrBlueFunc.Add("CLIENT_FengQiMemberLeave");
	ArrBlueFunc.Add("CLIENT_UpdateFengQiMemberDataToOtherClient");
	ArrBlueFunc.Add("CLIENT_ReceiveFengQiOtherMemberData");
	ArrBlueFunc.Add("CLIENT_UpdateFengQiIntegralToOtherClient");
	ArrBlueFunc.Add("CLIENT_UpdateFengQiKillDataToOtherClient");
	ArrBlueFunc.Add("CLIENT_ShowFengQiRank");
	ArrBlueFunc.Add("CLIENT_ShowOriginArea");
	ArrBlueFunc.Add("CLIENT_ShowEndArea");
	ArrBlueFunc.Add("CLIENT_StartReduceArea");
	ArrBlueFunc.Add("CLIENT_UpdateFengQiMemberDataToOtherOnLogin");
	ArrBlueFunc.Add("CLIENT_OnEnterLingMaiMatchQueue");
	ArrBlueFunc.Add("CLIENT_OnEnterLingMaiReadyQueue");
	ArrBlueFunc.Add("CLIENT_OnEnterLingMaiTelPortQueue");
	ArrBlueFunc.Add("CLIENT_OnLingMaiActivityEnd");
	ArrBlueFunc.Add("CLIENT_AddLingMaiMember");
	ArrBlueFunc.Add("CLIENT_OnLeaveLingMai");
	ArrBlueFunc.Add("CLIENT_ShowLingMaiLife");
	ArrBlueFunc.Add("CLIENT_OnKillLingMai");
	ArrBlueFunc.Add("CLIENT_OnAssistsLingMai");
	ArrBlueFunc.Add("CLIENT_OccupyPagodaBase");
	ArrBlueFunc.Add("CLIENT_OccupyPagoda");
	ArrBlueFunc.Add("CLIENT_OccupyLingMai");
	ArrBlueFunc.Add("CLIENT_OnGrabGourdLeave");
	ArrBlueFunc.Add("CLIENT_OnPowerPointChange");
	ArrBlueFunc.Add("CLIENT_OnWinGameLingMai");
	ArrBlueFunc.Add("CLIENT_OnEndLegendary");
	ArrBlueFunc.Add("CLIENT_ShowShiFangChengPassList");
	ArrBlueFunc.Add("CLIENT_ShowEnterActBunchWindow");
	ArrBlueFunc.Add("ShowEnterYeZhanFengQiWindow");
	ArrBlueFunc.Add("CLIENT_UpdateYXLMMemberDataToOtherClient");
	ArrBlueFunc.Add("CLIENT_ReceiveYXLMOtherMemberData");
	ArrBlueFunc.Add("CLIENT_UpdateYXLMKillDataToOtherClient");
	ArrBlueFunc.Add("CLIENT_UpdateYXLMBeKillDataToOtherClient");
	ArrBlueFunc.Add("CLIENT_UpdateYXLMAddItemToOtherClient");
	ArrBlueFunc.Add("CLIENT_UpdateYXLMRemoveItemToOtherClient");
	ArrBlueFunc.Add("CLIENT_CampYXLMOnMatchSuccess");
	ArrBlueFunc.Add("CLIENT_CampYXLMHideAffirmWindow");
	ArrBlueFunc.Add("CLIENT_CampYXLMUpdateWaitAffirmList");
	ArrBlueFunc.Add("CLIENT_CampYXLMShowAffirmData");
	ArrBlueFunc.Add("CLIENT_UpdateYXLMMemberDataToOtherOnLogin");
	ArrBlueFunc.Add("CLIENT_ShowYXLMBattlefieldWin");
	ArrBlueFunc.Add("CLIENT_CampYXLMSignUpSuccess");
	ArrBlueFunc.Add("CLIENT_ShowYXLMSpaceLife");
	ArrBlueFunc.Add("CLIENT_ShowYXLMRandomScriptIDs");
	ArrBlueFunc.Add("CLIENT_showEnemyPos");
	ArrBlueFunc.Add("CLIENT_HideEnemyPos");
	ArrBlueFunc.Add("CLIENT_ShowTongSignSuccessWindow");
	ArrBlueFunc.Add("CLIENT_ShowPassFirstTongStarcraft");
	ArrBlueFunc.Add("CLIENT_OnEnterFrozenFightMatchQueue");
	ArrBlueFunc.Add("CLIENT_OnEnterFrozenFightReadyQueue");
	ArrBlueFunc.Add("CLIENT_OnEnterFrozenFightTelPortQueue");
	ArrBlueFunc.Add("CLIENT_OnFrozenFightActivityEnd");
	ArrBlueFunc.Add("CLIENT_AddFrozenFightMember");
	ArrBlueFunc.Add("CLIENT_OnLeaveFrozenFight");
	ArrBlueFunc.Add("CLIENT_OnFrozenFightOccupyTower");
	ArrBlueFunc.Add("CLIENT_OnFrozenFightOccupyRivivePos");
	ArrBlueFunc.Add("CLIENT_ShowFrozenFightLife");
	ArrBlueFunc.Add("CLIENT_OnKillFrozenFight");
	ArrBlueFunc.Add("CLIENT_OnAssistsFrozenFight");
	ArrBlueFunc.Add("CLIENT_OnFrozenFightPointChanged");
	ArrBlueFunc.Add("CLIENT_OnFrozenFightSubmit");
	ArrBlueFunc.Add("CLIENT_OnWinGameFrozenFight");
	ArrBlueFunc.Add("CLIENT_UpdateMemberIntegral");
	ArrBlueFunc.Add("CLIENT_UpdateTongIntegral");
	ArrBlueFunc.Add("CLIENT_OpenSecondTongStarcraftGroup");
	ArrBlueFunc.Add("ShowTongStarcraftFirstSignUpTong");
	ArrBlueFunc.Add("UpdateTongStarcraftLoginMemToOtherClient");
	ArrBlueFunc.Add("CLIENT_ShowTongMemberWindow");
	ArrBlueFunc.Add("CLIENT_ShowFirstWindow");
	ArrBlueFunc.Add("CLIENT_UpdateThirdTongStarcraftIntegral");
	ArrBlueFunc.Add("CLIENT_ReceiveAllThirdTongStarcraftIntegral");
	ArrBlueFunc.Add("CLIENT_ReceiveThirdTongStarcraftAllOccupySpellBox");
	ArrBlueFunc.Add("CLIENT_AddThirdTongStarcraftOccupySpellBox");
	ArrBlueFunc.Add("CLIENT_RemoveThirdTongStarcraftOccupySpellBox");
	ArrBlueFunc.Add("CLIENT_ReceiveAllThirdTongStarcraftMemberData");
	ArrBlueFunc.Add("CLIENT_UpdateThirdTongStarcraftMemToOtherClient");
	ArrBlueFunc.Add("CLIENT_UpdateThirdTongStarcraftLoginMemToOtherClient");
	ArrBlueFunc.Add("CLIENT_UpdateThirdTongStarcraftMemKill");
	ArrBlueFunc.Add("CLIENT_UpdateThirdTongStarcraftMemBeKill");
	ArrBlueFunc.Add("CLIENT_UpdateThirdTongStarcraftMemAssists");
	ArrBlueFunc.Add("CLIENT_UpdateThirdTongStarcraftMemOccupy");
	ArrBlueFunc.Add("CLIENT_ShowEnterYXLMTime");
	ArrBlueFunc.Add("CLIENT_UpdateYeZhanFengQiMemberNumber");
	ArrBlueFunc.Add("CLIENT_UpdateYeZhanFengQiMyKillNumber");
	ArrBlueFunc.Add("ClIENT_ShowYeZhanFengQiOriginArea");
	ArrBlueFunc.Add("ClIENT_ShowYeZhanFengQiEndArea");
	ArrBlueFunc.Add("ClIENT_StartReduceYeZhanFengQiArea");
	ArrBlueFunc.Add("CLIENT_ShowGoldTreeCompass");
	ArrBlueFunc.Add("CLIENT_AddActivityCircleArea");
	ArrBlueFunc.Add("CLIENT_ClearActivityCircleArea");
	ArrBlueFunc.Add("CLIENT_ShowAreaInBigMapUI");
	ArrBlueFunc.Add("CLIENT_ShowYeZhanFengQiMemberRank");
	ArrBlueFunc.Add("CLIENT_ShowFirstPassShiFangCheng");
	ArrBlueFunc.Add("CLIENT_ShowPassShiFangChengNumber");
	ArrBlueFunc.Add("CLIENT_ShowWinTong");
	ArrBlueFunc.Add("CLIENT_ShowThirdTongStarcraftLife");
	ArrBlueFunc.Add("CLIENT_showYXLMQuickBag");
	ArrBlueFunc.Add("CLIENT_hideYXLMQuickBag");
	ArrBlueFunc.Add("CLIENT_beginJZYT");
	ArrBlueFunc.Add("OnNotifyStartXKTB");
	ArrBlueFunc.Add("NotifyRechargeableValue");
	ArrBlueFunc.Add("CampSGMZSignUpSuccess");
	ArrBlueFunc.Add("CampSGMZOnMatchSuccess");
	ArrBlueFunc.Add("CampSGMZHideAffirmWindow");
	ArrBlueFunc.Add("CampSGMZShowAffirmData");
	ArrBlueFunc.Add("ShowEnterSGMZTime");
	ArrBlueFunc.Add("OnQueryTongSignUpData");
	ArrBlueFunc.Add("CLIENT_beginTJP");
	ArrBlueFunc.Add("OnEnterFHLTMatchQueue");
	ArrBlueFunc.Add("OnFHLTActivityEnd");
	ArrBlueFunc.Add("OnEnterFHLTReadyQueue");
	ArrBlueFunc.Add("OnEnterFHLTTelPortQueue");
	ArrBlueFunc.Add("OnAddFHLTMember");
	ArrBlueFunc.Add("OnLeaveFHLT");
	ArrBlueFunc.Add("OnKillFHLT");
	ArrBlueFunc.Add("OnIntegralChange");
	ArrBlueFunc.Add("OnWinGameFHLT");
	ArrBlueFunc.Add("ShowFHLTLife");
	ArrBlueFunc.Add("CLIENT_beginJXLC");
	ArrBlueFunc.Add("CLIENT_AddCampYCJMDMember");
	ArrBlueFunc.Add("CLIENT_OnLeaveCampYCJMD");
	ArrBlueFunc.Add("CLIENT_OnKillCampYCJMD");
	ArrBlueFunc.Add("CLIENT_OnAssistsCampYCJMD");
	ArrBlueFunc.Add("OnCampRandomFitStart");
	ArrBlueFunc.Add("OnCampRandomFitSuccess");
	ArrBlueFunc.Add("OnCampRandomFitInterrupt");
	ArrBlueFunc.Add("ShowEnterRandomFitTime");
	ArrBlueFunc.Add("ShowPublicActRecordUI");
	Supper::InitBlueCB();
}

void URoleActivityInterface::OnLeaveScenes()
{
	BHZBTeamProtectDict.Empty();
	BHZBTeamAttackDict.Empty();
	BHZBPointDict.Empty();
	BHZBHomeBarrackMapDict.Empty();
	BHZBMemberPosDatas.Empty();
	BHZBPointCfgData.Empty();
	YXLMMemberDatas.Empty();
	YXLMRandomScriptIDDatas.Empty();
	YXLMXianTeamData.Empty();
	YXLMMoTeamData.Empty();
	Supper::OnLeaveScenes();
}

void URoleActivityInterface::OnCampRandomFitStart_Implementation()
{
}

void URoleActivityInterface::OnCampRandomFitSuccess_Implementation()
{
}

void URoleActivityInterface::OnCampRandomFitInterrupt_Implementation()
{
}

void URoleActivityInterface::ShowEnterRandomFitTime_Implementation(float enterTime)
{

}

void URoleActivityInterface::ShowPublicActRecordUI_Implementation(const TArray<int32>& ActivityTypeList, const TArray<int32>& MaxDegreeList, const TArray<int32>& DegreeList)
{
}

void URoleActivityInterface::RPC_CampRandomFitInterrupt()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RPC_CampRandomFitInterrupt no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("campRandomFitInterrupt"), args);
}

void URoleActivityInterface::DeclareBHZBPoint(const int32& pointIndex, const int32& groupID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::DeclareBHZBPoint no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(pointIndex);
	args.Add(groupID);
	entity->CellCall(TEXT("declareBHZBPoint"), args);
}

void URoleActivityInterface::CancelDeclareBHZBPoint(const int32& pointIndex)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::CancelDeclareBHZBPoint no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(pointIndex);
	entity->CellCall(TEXT("cancelDeclareBHZBPoint"), args);
}

void URoleActivityInterface::JoinBHZBPointFight(const int32& pointIndex, const int32& groupID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::JoinBHZBPointFight no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(pointIndex);
	args.Add(groupID);
	entity->CellCall(TEXT("joinBHZBPointFight"), args);
}

void URoleActivityInterface::cancelJoinBHZBPointFight(const int32& pointIndex)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::cancelJoinBHZBPointFight no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(pointIndex);
	entity->CellCall(TEXT("cancelJoinBHZBPointFight"), args);
}

void URoleActivityInterface::OpenBHZBIntegralRank(const FVariant& Var)
{
	TArray<FBHZBTONGINTEGRALDATA> rankDatas = GetBHZBRankDatasByFVariant(Var);
	if (rankDatas.Num())
	{
		rankDatas.Sort([](const FBHZBTONGINTEGRALDATA& tempRank1, const FBHZBTONGINTEGRALDATA& tempRank2)
		{
			return tempRank1.Integral > tempRank2.Integral;
		});
	}
	OnOpenBHZBIntegralRank(rankDatas);
}

void URoleActivityInterface::OpenSignUpBHZBRankWin(const FVariant& Var)
{
	KBEngine::FVariantArray rankList = Var.GetValue<KBEngine::FVariantArray>();
	TArray<FBHZBTONGSIGNUPRANKDATA> rankDatas = TArray<FBHZBTONGSIGNUPRANKDATA>();
	for (FVariant& data : rankList)
	{
		BHZB_TONG_SIGNUP_RANK_DATA element1 = BHZB_TONG_SIGNUP_RANK_DATA(data);
		FBHZBTONGSIGNUPRANKDATA tempRank;
		tempRank.TongDBID = INT64_TO_FSTRING(element1.tongDBID);
		tempRank.TongName = element1.tongName;
		tempRank.TongLevel = element1.tongLevel;
		tempRank.Activity = INT_TO_FSTRING(element1.activity);
		tempRank.TongMemNum =  element1.tongMemNum;
		tempRank.Camp = element1.camp;
		rankDatas.Add(tempRank);
	}
	OnOpenSignUpBHZBRankWin(rankDatas);
}

void URoleActivityInterface::CallTeamToProtect(const int32& groupTeamID, const int32& pointIndex, const FString& pointName)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::CallTeamToProtect no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(groupTeamID);
	args.Add(pointIndex);
	args.Add(pointName);
	entity->CellCall(TEXT("callTeamToProtect"), args);
}

void URoleActivityInterface::CallTeamToAttack(const int32& groupTeamID, const int32& pointIndex, const FString& pointName)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::CallTeamToAttack no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(groupTeamID);
	args.Add(pointIndex);
	args.Add(pointName);
	entity->CellCall(TEXT("callTeamToAttack"), args);
}

void URoleActivityInterface::UpdataToTongMemberClientProtectData(int32 groupTeamID,int32 pointIndex)
{
	if (BHZBTeamProtectDict.Contains(pointIndex))
	{
		BHZBTeamProtectDict[pointIndex] = groupTeamID;
	}
	else
	{
		BHZBTeamProtectDict.Add(pointIndex, groupTeamID);
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataToTongMemberClientProtectData.Broadcast(groupTeamID, pointIndex);
	}
}

void URoleActivityInterface::UpdataToTongMemberClientAttackData(int32 groupTeamID,int32 pointIndex)
{
	if (BHZBTeamAttackDict.Contains(pointIndex))
	{
		BHZBTeamAttackDict[pointIndex] = groupTeamID;
	}
	else
	{
		BHZBTeamAttackDict.Add(pointIndex, groupTeamID);
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataToTongMemberClientAttackData.Broadcast(groupTeamID, pointIndex);
	}
}

void URoleActivityInterface::OpenNPCExtPointDetails(const FString& name, uint8 pointType, uint8 npcState, const FVariant& warNameList, const FVariant& warMemberNumList, int32 maxJoinNum, const FString& endTime, const FVariant& warTongDBIDList, const FVariant& joinAttackMems, const FVariant& joinProtectMems)
{
	KBEngine::FVariantArray warNameArray = warNameList.GetValue<KBEngine::FVariantArray>();
	TArray<FString> WarNames;
	for (FVariant& element : warNameArray)
	{
		FString value = element.GetValue<FString>();
		WarNames.Add(value);
	}
	KBEngine::FVariantArray warMemberNumArray = warMemberNumList.GetValue<KBEngine::FVariantArray>();
	TArray<int32> WarMemberNums;
	for (FVariant& element : warMemberNumArray)
	{
		int32 value = element.GetValue<int32>();
		WarMemberNums.Add(value);
	}
	KBEngine::FVariantArray warTongDBIDArray = warTongDBIDList.GetValue<KBEngine::FVariantArray>();
	TArray<FString> warTongDBIDs;
	for (FVariant& element: warTongDBIDArray)
	{
		FString value = element.GetValue<FString>();
		warTongDBIDs.Add(value);
	}
	KBEngine::FVariantArray joinAttackMemArray = joinAttackMems.GetValue<KBEngine::FVariantArray>();
	TArray<FString> joinAttackMemList;
	for (FVariant& element : joinAttackMemArray)
	{
		FString value = element.GetValue<FString>();
		joinAttackMemList.Add(value);
	}
	KBEngine::FVariantArray joinProtectMemArray = joinProtectMems.GetValue<KBEngine::FVariantArray>();
	TArray<FString> joinProtectMemList;
	for (FVariant& element : joinProtectMemArray)
	{
		FString value = element.GetValue<FString>();
		joinProtectMemList.Add(value);
	}
	if(PointRequryType == POINTREQURY_TYPE::POINTREQURY_TYPE_RMOUSE_MENUE)
	{
		OnOpenNPCExtPointDetails(name, int32(pointType), int32(npcState), WarNames, WarMemberNums, maxJoinNum, endTime, warTongDBIDs, joinAttackMemList, joinProtectMemList);
	}
	else if (PointRequryType == POINTREQURY_TYPE::REQURYPOINT_TYPE_RMOUSE_CLICK)
	{
		OnPopRightMouseMenu(int32(npcState), WarNames, endTime, warTongDBIDs, joinAttackMemList, joinProtectMemList);
	}
	else if (PointRequryType == POINTREQURY_TYPE::REQURYPOINT_TYPE_NO_OPERATE)
	{
		OnRequryWarTongDBIDsCB(warTongDBIDs);
	}
}

void URoleActivityInterface::RequestOpenBHZBNpcPointMap(const bool IsManualRequestOpen)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RequestOpenBHZBNpcPointMap no this Entity!"));
		return;
	}
	bIsManualRequestOpen = IsManualRequestOpen;
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("requestOpenBHZBNpcPointMap"), args);
}

void URoleActivityInterface::InitBHZBNPCPointDatas(const FVariant& Var)
{
	BHZBPointDict.Empty();
	KBEngine::FVariantArray bhzbPointDatas = Var.GetValue<KBEngine::FVariantArray>();
	for (FVariant& data : bhzbPointDatas)
	{
		BHZB_POINT_DATA element1 = BHZB_POINT_DATA(data);
		FBHZBPOINTDATA tempData;
		tempData.Index = element1.index;
		tempData.PointType = element1.pointType;
		tempData.OccupyTongDBID = INT64_TO_FSTRING(element1.occupyTongDBID);
		tempData.declareWarState = element1.declareWarState;
		tempData.OccupyPlayerDBID = INT64_TO_FSTRING(element1.occupyPlayerDBID);
		tempData.FightEndTime = element1.fightEndTime;
		tempData.RestEndTime = element1.restEndTime;
		tempData.ReadyEndTime = element1.readyEndTime;
		tempData.OccupyTongName = element1.occupyTongName;
		tempData.AttackGroupTeamID = element1.attackGroupTeamID;
		tempData.JoinProtectGroupTeamID = element1.joinProtectGroupTeamID;
		tempData.DeclareTongDBID = INT64_TO_FSTRING(element1.declareTongDBID);
		BHZBPointDict.Add(tempData.Index, tempData);
	}
	if (bIsManualRequestOpen)
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TrainSoldierGroundMap"));
		}
		bIsManualRequestOpen = false;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnInitBHZBNPCPointDatas.Broadcast();
	}
}

void URoleActivityInterface::UpdataNPCPointRestEndTime(int32 pointIndex, const FString& restEndTime)
{
	if (BHZBPointDict.Contains(pointIndex))
	{
		BHZBPointDict[pointIndex].RestEndTime = restEndTime;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataNPCPointRestEndTime.Broadcast(pointIndex, restEndTime);
	}
}


void URoleActivityInterface::UpdataNPCPointReadyEndTime(int32 pointIndex, const FString& readyEndTime)
{
	if (BHZBPointDict.Contains(pointIndex))
	{
		BHZBPointDict[pointIndex].ReadyEndTime = readyEndTime;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataNPCPointReadyEndTime.Broadcast(pointIndex, readyEndTime);
	}
}

void URoleActivityInterface::UpdataNPCPointDeclareWarState(int32 pointIndex, uint8 declareWarState)
{
	if (BHZBPointDict.Contains(pointIndex))
	{
		BHZBPointDict[pointIndex].declareWarState = declareWarState;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataNPCPointDeclareWarState.Broadcast(pointIndex, declareWarState);
	}
}

void URoleActivityInterface::UpdateNPCPointAttackGroupTeamID(int32 pointIndex, int32 attackGroupTeamID, uint64 declareTongDBID)
{
	
	if (BHZBPointDict.Contains(pointIndex))
	{
	        FString tongDBIDString = INT64_TO_FSTRING(declareTongDBID);
		BHZBPointDict[pointIndex].AttackGroupTeamID = attackGroupTeamID;
		BHZBPointDict[pointIndex].DeclareTongDBID = tongDBIDString;
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnUpdateNPCPointAttackGroupTeamID.Broadcast(pointIndex, attackGroupTeamID, tongDBIDString);
		}
	}
}

void URoleActivityInterface::UpdataBHZBPointJoinProtectTeamID(int32 pointIndex, int32 joinProtectTeamID)
{
	if (BHZBPointDict.Contains(pointIndex))
	{
		BHZBPointDict[pointIndex].JoinProtectGroupTeamID = joinProtectTeamID;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataBHZBPointJoinProtectTeamID.Broadcast(pointIndex, joinProtectTeamID);
	}
}

void URoleActivityInterface::UpdataNPCPointOccupyData(int32 pointIndex, uint64 occupyTongDBID, uint64 playerDBID, const FString& playerName, const FString& tongName)
{
	FString TongDBIDString = INT64_TO_FSTRING(occupyTongDBID);
	if (BHZBPointDict.Contains(pointIndex))
	{
		BHZBPointDict[pointIndex].OccupyTongDBID = TongDBIDString;
		BHZBPointDict[pointIndex].OccupyPlayerDBID = INT64_TO_FSTRING(playerDBID);
		BHZBPointDict[pointIndex].OccupyTongName = tongName;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataNPCPointOccupyTongDBID.Broadcast(pointIndex, TongDBIDString);
	}
}

bool URoleActivityInterface::IsOccupyBHZBPoint(const int32& pointIndex)
{
	if (!BHZBPointDict.Contains(pointIndex))
	{
		return false;
	}
	URoleTongInterface * TongInterface = Cast<URoleTongInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTongInterface"), 0));
	if (IsValid(TongInterface) && IsValid(TongInterface->Tong))
	{
		return BHZBPointDict[pointIndex].OccupyTongDBID == TongInterface->Tong->TongDBID;
	}
	return false;
}

bool URoleActivityInterface::IsBHZBPointNeutrally(const int32& pointIndex)
{
	if (!BHZBPointDict.Contains(pointIndex))
	{
		return true;
	}
	return BHZBPointDict[pointIndex].OccupyTongDBID == "0";
}

void URoleActivityInterface::UpdataHomeBarracksMapDataToAllMember(const FVariant& Var)
{
	BHZBHomeBarrackMapDict.Empty();
	KBEngine::FVariantArray bhzbHomeBarrackMapDatas = Var.GetValue<KBEngine::FVariantArray>();
	for (FVariant& data : bhzbHomeBarrackMapDatas)
	{
		BHZB_MAP_HOMEBARRACKSDATA element1 = BHZB_MAP_HOMEBARRACKSDATA(data);
		FBHZBMAPHOMEBARRACKSDATA tempData;
		tempData.Index = element1.index;
		tempData.BelongTongDBID = INT64_TO_FSTRING(element1.belongTongDBID);
		tempData.Name = element1.name;
		tempData.Position = element1.position;
		BHZBHomeBarrackMapDict.Add(tempData.Index, tempData);
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataHomeBarracksMapDataToAllMember.Broadcast();
	}
}

bool URoleActivityInterface::IsMyBHZBHomeBarrack(const int32& index)
{
	if (!BHZBHomeBarrackMapDict.Contains(index))
	{
		return false;
	}
	URoleTongInterface * TongInterface = Cast<URoleTongInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTongInterface"), 0));
	if (IsValid(TongInterface) && IsValid(TongInterface->Tong))
	{
		return BHZBHomeBarrackMapDict[index].BelongTongDBID == TongInterface->Tong->TongDBID;
	}
	return false;
}

void URoleActivityInterface::RequestGotoStandMapPoint(const FVector& position)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RequestGotoStandMapPoint no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(position);
	entity->CellCall(TEXT("requestGotoStandMapPoint"), args);
}

void URoleActivityInterface::RequestGotoBHZBHomeBarrack(const FString& tongDBID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RequestGotoBHZBHomeBarrack no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(tongDBID);
	entity->CellCall(TEXT("requestGotoBHZBHomeBarrack"), args);
}

void URoleActivityInterface::UpdataMemberPositionToClient(const FVariant& Var)
{
	BHZBMemberPosDatas.Empty();
	KBEngine::FVariantArray bhzbMemberPosMapDatas = Var.GetValue<KBEngine::FVariantArray>();
	for (FVariant& data : bhzbMemberPosMapDatas)
	{
		BHZB_MAP_MEMBERPOSDATA element1 = BHZB_MAP_MEMBERPOSDATA(data);
		FBHZBMEMBERPOSDATA tempData;
		tempData.GroupID = element1.groupID;
		tempData.Position = element1.position;
		BHZBMemberPosDatas.Add(tempData);
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataMemberPositionToClient.Broadcast();
	}
}

void URoleActivityInterface::LoadBHZBPointCfgData(bool bIsClickMKeyOpen)
{
	if (BHZBPointCfgData.Num())
	{
		LoadBHZBPointCfgDataOver();
		return;
	}
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (IsValid(CfgManager))
	{
		const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BHZB_POINT_DATA);
		if (IsValid(ConfigTable))
		{
			TArray<FBHZB_POINT_TABLE_DATA*> TempBHZBPointDatas;
			ConfigTable->GetAllRows(TempBHZBPointDatas);
			for (auto data: TempBHZBPointDatas)
			{
				BHZBPointCfgData.Add(data->Index, *data);
			}
		}
	}
	if(bIsClickMKeyOpen)
	{
		LoadBHZBPointCfgDataOver();
	}
	
}

FBHZB_POINT_TABLE_DATA URoleActivityInterface::GetBHZBPointCfgData(const int32& Index)
{
	if (BHZBPointCfgData.Contains(Index))
	{
		return BHZBPointCfgData[Index];
	}
	FBHZB_POINT_TABLE_DATA tempData;
	return tempData;
}

void URoleActivityInterface::UpdataMyGroupIDToClient(int32 groupID)
{
	MyTeamGroupID = groupID;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataMyGroupIDToClient.Broadcast(groupID);
	}
}

void URoleActivityInterface::RequestPointDetails(const int32& pointIndex, const POINTREQURY_TYPE RequryOperteType)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RequestPointDetails no this Entity!"));
		return;
	}
	RequestPointIndex = pointIndex;
	PointRequryType = RequryOperteType;
	KBEngine::FVariantArray args;
	args.Add(pointIndex);
	entity->CellCall(TEXT("requestPointDetails"), args);
}

void URoleActivityInterface::DefenseBHZBPoint(const int32& pointIndex, const int32& groupID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RequestPointDetails no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(pointIndex);
	args.Add(groupID);
	entity->CellCall(TEXT("defenseBHZBPoint"), args);
}

void URoleActivityInterface::ShowExitPointSaveSpaceBtn()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowExitPointSaveSpaceBtn.Broadcast();
	}
}

void URoleActivityInterface::HideExitPointSaveSpaceBtn()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnHideExitPointSaveSpaceBtn.Broadcast();
	}
}

void URoleActivityInterface::UpdataBHZBPointJoinAttackMembers(int32 pointIndex, const FVariant& var)
{
	TArray<FString> joinAttackMemberDBIDs;
	KBEngine::FVariantArray memberDBIDArray = var.GetValue<KBEngine::FVariantArray>();
	for (FVariant& element : memberDBIDArray)
	{
		FString value = element.GetValue<FString>();
		joinAttackMemberDBIDs.Add(value);
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataBHZBPointJoinAttackMembers.Broadcast(pointIndex, joinAttackMemberDBIDs);
	}
}

void URoleActivityInterface::UpdataBHZBPointJoinProtectMembers(int32 pointIndex, const FVariant& var)
{
	TArray<FString> JoinProtectMemberDBIDs;
	KBEngine::FVariantArray memberDBIDArray = var.GetValue<KBEngine::FVariantArray>();
	for (FVariant& element : memberDBIDArray)
	{
		FString value = element.GetValue<FString>();
		JoinProtectMemberDBIDs.Add(value);
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdataBHZBPointJoinProtectMembers.Broadcast(pointIndex, JoinProtectMemberDBIDs);
	}
}

void URoleActivityInterface::ShowGroupIDAttackPointSign(int32 pointIndex, int32 groupID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowGroupIDAttackPointSign.Broadcast(pointIndex, groupID);
	}
}

void URoleActivityInterface::HideGroupIDAttackPointSign(int32 pointIndex)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnHideGroupIDAttackPointSign.Broadcast(pointIndex);
	}
}

void URoleActivityInterface::RequestOpenBHZBIntegralRank()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::RequestOpenBHZBIntegralRank no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("requestOpenBHZBIntegralRank"), args);
}

void URoleActivityInterface::ShowBHZBIntegralRankWin(const FVariant& Var, int32 delayCloseTime)
{
	TArray<FBHZBTONGINTEGRALDATA> rankDatas = GetBHZBRankDatasByFVariant(Var);
	if (rankDatas.Num())
	{
		rankDatas.Sort([](const FBHZBTONGINTEGRALDATA& tempRank1, const FBHZBTONGINTEGRALDATA& tempRank2)
		{
			return tempRank1.Integral > tempRank2.Integral;
		});
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TongBattleIntegralWnd"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowBHZBIntegralRankWin.Broadcast(rankDatas, delayCloseTime);
	}
}

TArray<FBHZBTONGINTEGRALDATA> URoleActivityInterface::GetBHZBRankDatasByFVariant(const FVariant& Var)
{
	KBEngine::FVariantArray integralRankList = Var.GetValue<KBEngine::FVariantArray>();
	TArray<FBHZBTONGINTEGRALDATA> rankDatas = TArray<FBHZBTONGINTEGRALDATA>();
	for (FVariant& data : integralRankList)
	{
		FBHZB_TONG_INTEGRALDATA element1 = FBHZB_TONG_INTEGRALDATA(data);
		FBHZBTONGINTEGRALDATA tempRank;
		tempRank.TongDBID = INT64_TO_FSTRING(element1.tongDBID);
		tempRank.TongName = element1.tongName;
		tempRank.TongLevel = element1.tongLevel;
		tempRank.OccupyPointAmount = element1.occupyPointAmount;
		tempRank.Integral = element1.integral;
		tempRank.Camp = element1.camp;
		rankDatas.Add(tempRank);
	}
	return rankDatas;
}

void URoleActivityInterface::InitBHZBWarDetailData(const FVariant& Var)
{
	FBHZBTONGWARDETAIL tempTongWarDetailMgr;
	BHZBTongWarDetailMgr = tempTongWarDetailMgr;
	BHZB_TONG_WAR_DETAIL element = BHZB_TONG_WAR_DETAIL(Var);
	BHZBTongWarDetailMgr.Integral = element.integral;
	BHZBTongWarDetailMgr.OccupyPointAmount = element.occupyPointAmount;
	BHZBTongWarDetailMgr.Rank = element.rank;
	BHZBTongWarDetailMgr.TongDBID = INT64_TO_FSTRING(element.tongDBID);
	for (auto tempTeamData: element.teamDatas)
	{
		FBHZBTONGTEAMDATA temp;
		temp.PointName = tempTeamData.pointName;
		temp.PointNumber = tempTeamData.pointNumber;
		temp.PointState = tempTeamData.pointState;
		temp.TeamNumber = tempTeamData.teamNumber;
		BHZBTongWarDetailMgr.TeamDatas.Add(temp.TeamNumber, temp);
	}
	for (auto tempOccupyData : element.occupyPointDatas)
	{
		FBHZBTONGOCCUPYPOINTDATA tempOccupy;
		tempOccupy.PointName = tempOccupyData.pointName;
		tempOccupy.PointNumber = tempOccupyData.pointNumber;
		tempOccupy.PointState = tempOccupyData.pointState;
		BHZBTongWarDetailMgr.OccupyPointDatas.Add(tempOccupy);
	}
	for (auto tempMsgData : element.warMsgDatas)
	{
		FBHZBTONGWARMSGDATA tempMsg;
		tempMsg.StatusID = tempMsgData.statusID;
		tempMsg.StatusArgs = tempMsgData.statusArgs;
		BHZBTongWarDetailMgr.warMsgDatas.Add(tempMsg);
	}
}

void URoleActivityInterface::UpdateBHZBWarDetailIntegralData(int32 integral, int32 rank)
{
	BHZBTongWarDetailMgr.Integral = integral;
	BHZBTongWarDetailMgr.Rank = rank;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateBHZBWarDetailIntegralData.Broadcast(integral, rank);
	}
}

void URoleActivityInterface::UpdateBHZBWarDetailOccupyNumber(int32 occupyPointAmount)
{
	BHZBTongWarDetailMgr.OccupyPointAmount = occupyPointAmount;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateBHZBWarDetailOccupyNumber.Broadcast(occupyPointAmount);
	}
}

void URoleActivityInterface::UpdateBHZBWarDetailTeamData(int32 teamNumber, int32 pointIndex, int32 pointState, const FString& pointName)
{
	if (BHZBTongWarDetailMgr.TeamDatas.Contains(teamNumber))
	{
		BHZBTongWarDetailMgr.TeamDatas.Remove(teamNumber);
	}
	FBHZBTONGTEAMDATA temp;
	temp.PointNumber = pointIndex;
	temp.PointName = pointName;
	temp.PointState = pointState;
	temp.TeamNumber = teamNumber;
	BHZBTongWarDetailMgr.TeamDatas.Add(teamNumber, temp);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnUpdateBHZBWarDetailTeamData.Broadcast(teamNumber, pointIndex, pointState, pointName);
	}
}

void URoleActivityInterface::RemoveBHZBWarDetailTeamData(int32 teamNumber)
{
	if (BHZBTongWarDetailMgr.TeamDatas.Contains(teamNumber))
	{
		BHZBTongWarDetailMgr.TeamDatas.Remove(teamNumber);
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRemoveBHZBWarDetailTeamData.Broadcast(teamNumber);
	}
}

void URoleActivityInterface::UpdateBHZBWarDetailOccupyPointData(int32 pointIndex, int32 pointState, const FString& pointName)
{
	bool isFindPoint = false;
	for (auto& OccupyPointData : BHZBTongWarDetailMgr.OccupyPointDatas)
	{
		if (OccupyPointData.PointNumber == pointIndex)
		{
			isFindPoint = true;
			OccupyPointData.PointState = pointState;
			if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
			{
				UUECS3GameInstance::Instance->GEventManager->OnUpdateBHZBWarDetailOccupyPointData.Broadcast(pointIndex, pointState);
			}
		}
	}
	if (!isFindPoint)
	{
		FBHZBTONGOCCUPYPOINTDATA temp;
		temp.PointNumber = pointIndex;
		temp.PointName = pointName;
		temp.PointState = pointState;
		BHZBTongWarDetailMgr.OccupyPointDatas.Add(temp);
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnAddBHZBWarDetailOccupyPointData.Broadcast(pointIndex, pointState, pointName);
		}
	}
}

void URoleActivityInterface::RemoveBHZBWarrDetailOccupyPoint(int32 pointIndex)
{
	for (auto OccupyPointData : BHZBTongWarDetailMgr.OccupyPointDatas)
	{
		if (OccupyPointData.PointNumber == pointIndex)
		{
			BHZBTongWarDetailMgr.OccupyPointDatas.Remove(OccupyPointData);
			if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
			{
				UUECS3GameInstance::Instance->GEventManager->OnRemoveBHZBWarrDetailOccupyPoint.Broadcast(pointIndex);
			}
			break;
		}
	}
}

void URoleActivityInterface::AddBHZBWarMsgData(int32 statusID, const FString& statusArgs)
{
	FBHZBTONGWARMSGDATA temp;
	temp.StatusID = statusID;
	temp.StatusArgs = statusArgs;
	BHZBTongWarDetailMgr.warMsgDatas.Add(temp);
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnAddBHZBWarMsgData.Broadcast(statusID, statusArgs);
	}
}

void URoleActivityInterface::QueryAllBHZBIntegralData(const FVariant& Var, int32 npcID)
{
	KBEngine::FVariantArray allIntegralRankList = Var.GetValue<KBEngine::FVariantArray>();
	//TArray<FALLBHZBTONGINTEGRALDATA> rankDatas = TArray<FALLBHZBTONGINTEGRALDATA>();
	for (FVariant& data : allIntegralRankList)
	{
		
		FALLBHZB_TONG_INTEGRALDATA element1 = FALLBHZB_TONG_INTEGRALDATA(data);
		FALLBHZBTONGINTEGRALDATA tempRank;
		tempRank.TongDBID = INT64_TO_FSTRING(element1.tongDBID);
		tempRank.TongName = element1.tongName;
		tempRank.TongLevel = element1.tongLevel;
		tempRank.TotalIntegral = element1.totalIntegral;
		tempRank.Integral = element1.integral;
		tempRank.Camp = element1.camp;
		tempRank.StartTime = element1.startTime;
		if (AllBHZBTongIntegralDatas.Contains(element1.startTime) )
		{
			AllBHZBTongIntegralDatas[element1.startTime].Add(tempRank);
		}
		else
		{
			TArray<FALLBHZBTONGINTEGRALDATA> tempArray;
			tempArray.Add(tempRank);
			AllBHZBTongIntegralDatas.Add(element1.startTime, tempArray);
		}	
	}
}

void URoleActivityInterface::OpenJoinGCZWin(const FVariant& numGCZsVar, const FVariant& gczStartTimesVar, const FVariant& gczRemainJoinNumsVar, int32 npcID)
{
	TArray<int32> numGCZs;
	KBEngine::FVariantArray numGCZArray = numGCZsVar.GetValue<KBEngine::FVariantArray>();
	for (FVariant& element : numGCZArray)
	{
		int32 numGCZ = element.GetValue<int32>();
		numGCZs.Add(numGCZ);
	}
	TArray<FString> gczStartTimes;
	KBEngine::FVariantArray gczStartTimeArray = gczStartTimesVar.GetValue<KBEngine::FVariantArray>();
	for (FVariant& element : gczStartTimeArray)
	{
		FString gczStartTime = element.GetValue<FString>();
		gczStartTimes.Add(gczStartTime);
	}
	TArray<int32> gczRemainJoinNums;
	KBEngine::FVariantArray gczRemainJoinNumArray = gczRemainJoinNumsVar.GetValue<KBEngine::FVariantArray>();
	for (FVariant& element : gczRemainJoinNumArray)
	{
		int32 gczRemainJoinNum = element.GetValue<int32>();
		gczRemainJoinNums.Add(gczRemainJoinNum);
	}

	//打开界面
	if (IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("AttackCityWarJoin"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnOpenJoinGCZWinEvent.Broadcast(npcID, numGCZs, gczStartTimes, gczRemainJoinNums);
	}
}

void URoleActivityInterface::SignUpGCZ(const int32 number, const int32& npcID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::SignUpGCZ no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(number);
	args.Add(npcID);
	entity->CellCall(TEXT("signUpGCZ"), args);
}

void URoleActivityInterface::NotifyToStartMatchGCZ(int32 curNumber)
{
	if (IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("AttackCityWarMatch"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnNotifyToStartMatchGCZEvent.Broadcast(curNumber);
	}
}

void URoleActivityInterface::NotifyCancelMatchGCZ()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnNotifyCancelMatchGCZEvent.Broadcast();
	}
	if (IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UBaseWindow *AttackCityWarMatch = UUECS3GameInstance::Instance->GUIManager->GetWindow(TEXT("AttackCityWarMatch"));
		if (IsValid(AttackCityWarMatch))
		{
			AttackCityWarMatch->Destroy();
		}
	}
}

void URoleActivityInterface::CancelMatchGCZ()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleActivityInterface::CancelMatchGCZ no this Entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->BaseCall(TEXT("cancelMatchGCZ"), args);
}

void URoleActivityInterface::AddTaosimPointPerSecond()
{
	TaosimPownerPoint += 1;
	CLIENT_OnPowerPointChange(TaosimPownerPoint, DemonPownerPoint);
}

void URoleActivityInterface::AddDemonPointPerSecond()
{
	DemonPownerPoint += 1;
	CLIENT_OnPowerPointChange(TaosimPownerPoint, DemonPownerPoint);
}

void URoleActivityInterface::OnBattleMatchStart()
{
  if (IsValid(UUECS3GameInstance::Instance->GUIManager)) 
  {
	  UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("YXLMMatch"));
  }
  if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
  {
	  UUECS3GameInstance::Instance->GEventManager->OnBattleMatchStart.Broadcast();
  }
}

void URoleActivityInterface::InterruptBattleActivityMatch()
{
  KBEngine::Entity* entity = GetEntity();
  if (entity == nullptr)
    {
	CS3_Warning(TEXT("--URoleActivityInterface::InterruptBattleActivityMatch no this Entity!"));
	return;
    }
  KBEngine::FVariantArray args;
  entity->BaseCall(TEXT("battleActivityInterrupt"), args);
}
CONTROL_COMPILE_OPTIMIZE_END
