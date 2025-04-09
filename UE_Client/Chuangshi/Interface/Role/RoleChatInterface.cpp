// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleChatInterface.h"
#include "Entity/Alias.h"
#include "Manager/MessageManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "KBEngine.h"
#include "Util/ConvertUtil.h"
#include "Manager/CfgManager.h"
#include "GameData/ChatData.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "RoleTeamInterface.h"
#include "RoleTongInterface.h"
#include "Kismet/KismetStringLibrary.h"
#include "Manager/LocalDataSaveManager.h"
#include "Regex.h"
#include "Util/CS3Debug.h"
#include "GameData/ChatSettingData.h"
#include "CS3Base/GameObject.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleChatInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onReceivePageData, &URoleChatInterface::onReceivePageData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onReceiveNewPageData, &URoleChatInterface::onReceiveNewPageData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onReceivePageSettings, &URoleChatInterface::onReceivePageSettings, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onReceiveChatMessageCB, &URoleChatInterface::onReceiveChatMessageCB, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleChatInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

CONTROL_COMPILE_OPTIMIZE_START

URoleChatInterface::URoleChatInterface()
{
}

URoleChatInterface::~URoleChatInterface()
{
}

void URoleChatInterface::onEnterWorld()
{
	Supper::onEnterWorld();

	InitChatChannelData();
	InitChatShortCutDatas();
	InitBaseSettingData();
}

void URoleChatInterface::onLeaveWorld()
{
// 	ChatTianYinData.Empty();
// 	ChatXianYinData.Empty();
// 	TabChatDatas.Empty();
// 	ChatPageDatas.Empty();
// 	ChatChannelSettingDatas.Empty();
// 	ChatShortcutDatas.Empty();
// 	ChatTabFindDatas.Empty();
// 	WhisperOrGroupDatas.Empty();
	Supper::onLeaveWorld();
}

void URoleChatInterface::onRoleSendChatMessage(const FVariant& chatData)
{
	//KBEngine::FVariantArray *data = new KBEngine::FVariantArray();
	//data->Add(chatData);
}


void URoleChatInterface::onRoleSendGMCommandMessage(const FString& dstEntityID, const FString& cmd, const FString& message)
{

}

void URoleChatInterface::InitPage(TArray<FChatPageData> PageDatas)
{
	for (FChatPageData TempPageData : PageDatas)
	{
		ChatPageDatas.Add(TempPageData);
		//add标签页下的聊天数据
		FTabChatData TabData;
		TabData.PageType = TempPageData.pageType;
		//聊天数据为空
		TabData.ChatDatas = {};
		TabChatDatas.Add(TabData);
	}
	onReceivePageSettingsDatas(PageDatas);
}

void URoleChatInterface::DeletePage(ChatPageType PageType)
{
	int32 Index;
	FChatPageData PageData = GetPageDataByPageType(PageType, Index);
	if (Index > -1)
	{
		ChatPageDatas.RemoveAt(Index);
	}
	FTabChatData ChatData = GetChatDataByPageType(PageType, Index);
	if (Index > -1)
	{
		TabChatDatas.RemoveAt(Index);
	}
}

void URoleChatInterface::AddNewPage(FChatPageData PageData)
{
	if (ChatPageDatas.Num() < 8)
	{
		//判断是否已经有这个标签页
		bool HasChatFTabType = false;
		for (FChatPageData TempData : ChatPageDatas)
		{
			if (TempData.pageType == PageData.pageType)
			{
				HasChatFTabType = true;
				break;
			}
		}
		//没有这个标签页则加上
		if (!HasChatFTabType)
		{
			//add标签页
			ChatPageDatas.Add(PageData);
			//add标签页下的聊天数据
			FTabChatData TabData;
			TabData.PageType = PageData.pageType;
			//聊天数据为空
			TabData.ChatDatas = {};
			TabChatDatas.Add(TabData);
			//通知蓝图
			onReceiveANewPageData(PageData);
		}
	}
}

void URoleChatInterface::ChangePage(FChatPageData PageData)
{
	int32 Index;
	GetPageDataByPageType(PageData.pageType, Index);
	if (Index > -1)
	{
		ChatPageDatas[Index] = PageData;
	}
	FTabChatData ChatData = GetChatDataByPageType(PageData.pageType, Index);
	if (Index > -1)
	{
		TArray<FChatData> TempChatData;
		TempChatData.Empty();
		TArray<ChatType> ChannelList = PageData.channelList;
		for (FChatData TempData : ChatData.ChatDatas)
		{
			if (ChannelList.Contains(TempData.type))
			{
				if (TempChatData.Num() >= MaxChatDataCount)
				{
					TempChatData.RemoveAt(0);
				}
				TempChatData.Add(TempData);
			}
		}
		FTabChatData TempTabChatData;
		TempTabChatData.PageType = ChatData.PageType;
		TempTabChatData.ChatDatas = TempChatData;
		TabChatDatas.Add(TempTabChatData);
	}
	onReceiveAPageData(PageData);
}

bool URoleChatInterface::CanCreateNewPage(FChatPageData& PageData)
{
	if (ChatPageDatas.Num() <= 7)
	{
		TArray<ChatType> TempList;
		FChatPageData TempCustom1;
		TempCustom1.pageType = ChatPageType::Custom1;
		TempCustom1.pageName = TEXT("自定义1");
		TempCustom1.channelList = TempList;
		FChatPageData TempCustom2;
		TempCustom2.pageType = ChatPageType::Custom2;
		TempCustom2.pageName = TEXT("自定义2");
		TempCustom2.channelList = TempList;

		TArray<FChatPageData> TempPageDatas;
		TempPageDatas.Add(TempCustom1);
		TempPageDatas.Add(TempCustom2);

		for (FChatPageData TempData : ChatPageDatas)
		{
			if (TempData.pageType == ChatPageType::Custom1)
			{
				TempPageDatas.RemoveAt(0);
			}
			else if (TempData.pageType == ChatPageType::Custom2)
			{
				TempPageDatas.RemoveAt(1);
			}
		}
		if (TempPageDatas.Num() > 0)
		{
			PageData = TempPageDatas[0];
			return true;
		}
	}
	return false;
}

void URoleChatInterface::InitChatChannelData()
{
	if (!UGolbalBPFunctionLibrary::LocalDataSaveManager() )
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::InitChatChannelData : LocalDataSaveManager()!"));
		return;
	}
	if (!IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalChatSettingData))
	{
		UGolbalBPFunctionLibrary::LocalDataSaveManager()->InitLocalChatSettingData();
	}
	ChatChannelCfgDatas = UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalChatSettingData->ChatSettingData.ChannelSettingData;
	for (FChatChannelCfg TempCfgData : ChatChannelCfgDatas)
	{
		FChatChannelSettingData SettingData;
		SettingData.ChannelType = TempCfgData.ChannelType;
		SettingData.Name = TempCfgData.Name;
		SettingData.Shorthand = TempCfgData.Shorthand;
		SettingData.Color = TempCfgData.Color;
		SettingData.IsCanModify = TempCfgData.IsCanModify;
		SettingData.ShortcutKey = TempCfgData.ShortcutKey;
		SettingData.SwitchingConditions = TempCfgData.SwitchingConditions;
		SettingData.OpenLevel = TempCfgData.OpenLevel;

		ChatChannelSettingDatas.Add(SettingData);
	}
	BP_ChangeShortCutData();
}

FString URoleChatInterface::ConvertColorToHex(FColor Color, bool IsShowA /*= false*/)
{
	if (IsShowA)
	{
		return FString::Printf(TEXT("%02X%02X%02X%02X"), Color.R, Color.G, Color.B, Color.A);
	} 
	else
	{
		return FString::Printf(TEXT("%02X%02X%02X"), Color.R, Color.G, Color.B);
	}
}

FColor URoleChatInterface::ConvertColorFromHex(FString HexString)
{
	return FColor::FromHex(HexString);
}

void URoleChatInterface::ChangeChatTypeColor(TArray<FChatChannelSettingData> ChatChannelSettingData)
{
	int32 Index = -1;
	for (FChatChannelSettingData TempData : ChatChannelSettingData)
	{
		GetChannelDataByChatType(TempData.ChannelType, Index);
		if (Index>-1)
		{
			ChatChannelSettingDatas[Index].Color = TempData.Color;
		}
		Index = -1;
	}
	BP_ChangeChatTypeColor();
	SaveChatBaseSetting();
}

void URoleChatInterface::RestoreDefaultsChatTypeColor()
{
	if (IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalChatSettingData))
	{
		FChatSettingData  TempChatSettingData = UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalChatSettingData->GetDefaultChatSettingData();
		
		int32 Index = -1;
		for (FChatChannelCfg TempData : TempChatSettingData.ChannelSettingData)
		{
			FChatChannelSettingData ChatChannelSettingData = GetChannelDataByChatType(TempData.ChannelType, Index);
			if (Index > -1)
			{
				ChatChannelSettingDatas[Index].Color = TempData.Color;				
			}
			Index = -1;
		}
		BP_ChangeChatTypeColor();
		SaveChatBaseSetting();
	}
}

void URoleChatInterface::RestoreDefaultsShortCut()
{
	if (IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalChatSettingData))
	{
		FChatSettingData  TempChatSettingData = UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalChatSettingData->GetDefaultChatSettingData();

		int32 Index = -1;
		for (FChatChannelCfg TempData : TempChatSettingData.ChannelSettingData)
		{
			GetChannelDataByChatType(TempData.ChannelType, Index);
			if (Index > -1)
			{
				ChatChannelSettingDatas[Index].ShortcutKey = TempData.ShortcutKey;
			}
			Index = -1;
		}
		BP_ChangeShortCutData();
		SaveChatBaseSetting();
	}	
}

void URoleChatInterface::ChangeShortCutData(TArray<FChatChannelSettingData> ChatChannelSettingData)
{
	int32 Index = -1;
	for (FChatChannelSettingData TempData : ChatChannelSettingData)
	{
		GetChannelDataByChatType(TempData.ChannelType, Index);
		if (Index > -1)
		{
			ChatChannelSettingDatas[Index].ShortcutKey = TempData.ShortcutKey;
		}
		Index = -1;
	}
	BP_ChangeShortCutData();
	SaveChatBaseSetting();
}

void URoleChatInterface::RestoreDefaultsWinSetting()
{
	if (IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalChatSettingData))
	{
		FChatSettingData  TempChatSettingData = UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalChatSettingData->GetDefaultChatSettingData();

		BaseSettingData= TempChatSettingData.BaseSettingData;
		SaveChatBaseSetting();
		BP_ChangeChatBaseSettingsDatas();
	}
}

void URoleChatInterface::ChangeChatBaseSettingsDatas(bool IsHide, bool IsSHowTime, float BgAlpha, FColor BgColor)
{
	BaseSettingData.isHideAuto = IsHide;
	BaseSettingData.IsShowTime = IsSHowTime;
	BaseSettingData.Transparency = BgAlpha;
	FLinearColor LocalLinearColor = BgColor.FromRGBE();
	LocalLinearColor.A = BgAlpha;
	BaseSettingData.BGColor = LocalLinearColor.ToFColor(true);
	SaveChatBaseSetting();
	BP_ChangeChatBaseSettingsDatas();
}

void URoleChatInterface::OnChatShortcutSwitchConditionsChange()
{
	if (CheckChatShortcutDatas())
	{
		BP_ChangeChatShortcutDatas();
	}
}

void URoleChatInterface::ChangeQuickSetting(TArray<FChatChannelData> ChannelData)
{
	if (ChatChannelSettingDatas.Num() == 0)
	{
		InitChatChannelData();
		for (FChatChannelData TempData : ChannelData)
		{
			for (FChatChannelCfg TempCfgData : ChatChannelCfgDatas)
			{
				if (TempData.channelType == TempCfgData.ChannelType)
				{
					FChatChannelSettingData SettingData;
					SettingData.ChannelType = TempCfgData.ChannelType;
					SettingData.Name = TempCfgData.Name;
					SettingData.Shorthand = TempCfgData.Shorthand;
					SettingData.Color = TempCfgData.Color;
					SettingData.IsCanModify = (bool)TempData.isCanModify;
					SettingData.ShortcutKey = TempData.shortcutKey;
					SettingData.SwitchingConditions = TempCfgData.SwitchingConditions;
					SettingData.OpenLevel = TempCfgData.OpenLevel;

					ChatChannelSettingDatas.Add(SettingData);
				}
			}
		}
	}
	else
	{
		for (FChatChannelData TempData : ChannelData)
		{
			int32 Index;
			FChatChannelSettingData LocalData = GetChannelDataByChatType(TempData.channelType, Index);
			if (Index > -1)
			{
				LocalData.IsCanModify = (bool)TempData.isCanModify;
				LocalData.ShortcutKey = TempData.shortcutKey;
				//更新数据
				ChatChannelSettingDatas[Index] = LocalData;
			}
		}
	}
}

void URoleChatInterface::InitChatShortCutDatas()
{
	ChatShortcutDatas = GetCanUseChatTypeDatas();
}

void URoleChatInterface::InitBaseSettingData()
{
	if (!UGolbalBPFunctionLibrary::LocalDataSaveManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::InitChatChannelData : LocalDataSaveManager()!"));
		return;
	}
	if (!IsValid(UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalChatSettingData))
	{
		UGolbalBPFunctionLibrary::LocalDataSaveManager()->InitLocalChatSettingData();
	}
	BaseSettingData = UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalChatSettingData->ChatSettingData.BaseSettingData;
}

bool URoleChatInterface::CheckChatShortcutDatas()
{
	TArray<ChatType> TempList = GetCanUseChatTypeDatas();

	bool HasChanged = false;

	for (int i = 0; i < TempList.Num(); i++)
	{
		if (!ChatShortcutDatas.Contains(TempList[i]))
		{
			ChatShortcutDatas.Add(TempList[i]);
			HasChanged = true;
		}
	}
	TArray<ChatType> TempChatShortcutDatas = ChatShortcutDatas;
	for (int i = 0; i < TempChatShortcutDatas.Num(); i++)
	{
		if (!TempList.Contains(TempChatShortcutDatas[i]))
		{
			ChatShortcutDatas.Remove(TempChatShortcutDatas[i]);
			HasChanged = true;
		}
	}
	return HasChanged;
}

TArray<ChatType>  URoleChatInterface::GetCanUseChatTypeDatas()
{
	TArray<ChatType> List = GetOpenLevelChatTypeDatas();
	TArray<ChatType> ChatTypeList;
	ChatTypeList.Empty();
	for (ChatType TempType : List)
	{
		if (TempType == ChatType::Group)
		{
			for (FChatWhisperAndGroupData TempData : WhisperOrGroupDatas)
			{
				if (TempData.ChannelType == TempType)
				{
					int32 MessageID = GetSwitchConditionsByChatType(TempType);
					if (MessageID == 0)
					{
						ChatTypeList.Add(TempType);
					}
				}
			}
		}
		else
		{
			int32 MessageID = GetSwitchConditionsByChatType(TempType);
			if (MessageID == 0)
			{
				ChatTypeList.Add(TempType);
			}
		}
	}
	return ChatTypeList;
}

TArray<ChatType> URoleChatInterface::GetOpenLevelChatTypeDatas()
{
	TArray<ChatType> TempChatTypeList;
	TempChatTypeList.Empty();
	for (FChatChannelSettingData TempData : ChatChannelSettingDatas)
	{
		//-1为不可打开频道，比如系统频道
		if (TempData.OpenLevel != -1)
		{
			int32 PlayerLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("level"));
			if (PlayerLevel >= TempData.OpenLevel)
			{
				TempChatTypeList.Add(TempData.ChannelType);
			}
		}
	}
	return TempChatTypeList;
}

int32 URoleChatInterface::GetSwitchConditionsByChatType(ChatType ChannelType)
{
	int32 Index;
	FChatChannelSettingData SettingData = GetChannelDataByChatType(ChannelType, Index);
	if (Index > -1)
	{
		for (FChatTypeSwitchingCondition TempCond : SettingData.SwitchingConditions)
		{
			int32 MessageID = 0;
			switch (TempCond)
			{
			case FChatTypeSwitchingCondition::CHAT_NONE:
				break;
			case FChatTypeSwitchingCondition::CHAT_HAS_GROUP:
			{
				MessageID = 4416;
				break;
			}
			case FChatTypeSwitchingCondition::CHAT_HAS_TEAM:
			{
				URoleTeamInterface * RoleTeamInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? 
					UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.RoleTeamInterface : nullptr;
				if (IsValid(RoleTeamInterface))
				{
					if (!RoleTeamInterface->HasTeam())
					{
						MessageID = 4414;
					}
				}
				break;
			}
			case FChatTypeSwitchingCondition::CHAT_HAS_COLLECTIVE:
			{
				MessageID = 4416;
				break;
			}
			case FChatTypeSwitchingCondition::CHAT_HAS_GANG:
			{
				URoleTongInterface * TongInterface = Cast<URoleTongInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTongInterface"), 0));
				if (IsValid(TongInterface))
				{
					if (!TongInterface->hasTong())
					{
						MessageID = 4413;
					}
				}
				break;
			}
			case FChatTypeSwitchingCondition::CHAT_IS_ONBATTLESPACE:
			{
				MessageID = 4416;
				break;
			}
			case FChatTypeSwitchingCondition::CHAT_WHISPER_NAME:
				break;
			case FChatTypeSwitchingCondition::CHAT_FORBID:
			{
				MessageID = -1; ///<CST-7681 策划禁止显示相关频道
				break;
			}
			default:
				break;
			}
			return MessageID;
		}
		int32 PlayerLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("level"));
		if (PlayerLevel < SettingData.OpenLevel)
		{
			return 4412;
		}
	}
	else
	{
		return 1;
	}
	return 0;
}


void URoleChatInterface::RequestMakeNewPage()
{
	FChatPageData PageData;
	bool CanCreate = CanCreateNewPage(PageData);
	if (CanCreate)
	{
		TArray<FString> ChatTypeList;
		ChatTypeList.Empty();
		for (ChatType TempType : PageData.channelList)
		{
			ChatTypeList.Add(INT_TO_FSTRING((int32)TempType));
		}
		FString TypeListStr = UKismetStringLibrary::JoinStringArray(ChatTypeList, FString(TEXT("#")));
		RPC_receiveMakeNewPage(INT_TO_FSTRING((int32)PageData.pageType), PageData.pageName, TypeListStr);
	}
}

void URoleChatInterface::ChangeChatChannelColor(TArray<FChatChannelSettingData> Datas)
{
	ChatChannelSettingDatas = Datas;
}

void URoleChatInterface::SaveChatBaseSetting()
{
	TArray<FChatChannelCfg> TempChannelDatas;
	FChatChannelCfg ChannelInfo;
	for (int i = 0; i < ChatChannelSettingDatas.Num(); i++)
	{
		ChannelInfo.ChannelType = ChatChannelSettingDatas[i].ChannelType;
		ChannelInfo.Color = ChatChannelSettingDatas[i].Color;
		ChannelInfo.IsCanModify = ChatChannelSettingDatas[i].IsCanModify;
		ChannelInfo.Name = ChatChannelSettingDatas[i].Name;
		ChannelInfo.OpenLevel=ChatChannelSettingDatas[i].OpenLevel;
		ChannelInfo.ShortcutKey= ChatChannelSettingDatas[i].ShortcutKey;
		ChannelInfo.SwitchingConditions = ChatChannelSettingDatas[i].SwitchingConditions;
		ChannelInfo.Shorthand = ChatChannelSettingDatas[i].Shorthand;

		TempChannelDatas.Add(ChannelInfo);
	}
	
	FChatSettingData TempChatSettingData;
	TempChatSettingData.BaseSettingData = BaseSettingData;
	TempChatSettingData.ChannelSettingData = TempChannelDatas;

	ULocalDataSaveManager* LocalDataSaveManager = UGolbalBPFunctionLibrary::LocalDataSaveManager();
	if (IsValid(LocalDataSaveManager) && IsValid(LocalDataSaveManager->LocalChatSettingData))
	{
		LocalDataSaveManager->LocalChatSettingData->SaveDataToFile(TempChatSettingData);
	}
}

FChatSettingData URoleChatInterface::GetChatBaseSettingByName(FString Name)
{
	return FChatSettingData();
}

FChatPageData URoleChatInterface::GetPageDataByPageType(ChatPageType PageType, int32& Index)
{
	for (int32 TempIndex = 0; TempIndex < ChatPageDatas.Num(); TempIndex++)
	{
		FChatPageData Data = ChatPageDatas[TempIndex];
		if (Data.pageType == PageType)
		{
			Index = TempIndex;
			return Data;
		}
	}
	Index = -1;
	return FChatPageData();
}

FTabChatData URoleChatInterface::GetChatDataByPageType(ChatPageType PageType, int32& Index)
{
	for (int32 TempIndex = 0; TempIndex < TabChatDatas.Num(); TempIndex++)
	{
		FTabChatData Data = TabChatDatas[TempIndex];
		if (Data.PageType == PageType)
		{
			Index = TempIndex;
			return Data;
		}
	}
	Index = -1;
	return FTabChatData();
}

FTabFindChatData URoleChatInterface::GetFindChatDataByPageType(ChatPageType PageType, int32& Index)
{
	for (int32 TempIndex = 0; TempIndex < ChatTabFindDatas.Num(); TempIndex++)
	{
		FTabFindChatData Data = ChatTabFindDatas[TempIndex];
		if (Data.PageType == PageType)
		{
			Index = TempIndex;
			return Data;
		}
	}
	Index = -1;
	return FTabFindChatData();
}

FChatChannelSettingData URoleChatInterface::GetChannelDataByChatType(ChatType ChannelType, int32& Index)
{
	for (int32 TempIndex = 0; TempIndex < ChatChannelSettingDatas.Num(); TempIndex++)
	{
		FChatChannelSettingData Data = ChatChannelSettingDatas[TempIndex];
		if (Data.ChannelType == ChannelType)
		{
			Index = TempIndex;
			return Data;
		}
	}
	Index = -1;
	return FChatChannelSettingData();
}

TArray<FChatWhisperAndGroupData> URoleChatInterface::GetWhisperOrGroupDataByChatType(ChatType ChannelType)
{
	TArray<FChatWhisperAndGroupData> TempList;
	TempList.Empty();
	for (FChatWhisperAndGroupData TempData : WhisperOrGroupDatas)
	{
		if (TempData.ChannelType == ChannelType)
		{
			TempList.Add(TempData);
		}
	}
	return TempList;
}

FChatWhisperAndGroupData URoleChatInterface::GetWhisperDataByName(FString Name, int32& Index)
{
	for (int32 TempIndex = 0; TempIndex < WhisperOrGroupDatas.Num(); TempIndex++)
	{
		FChatWhisperAndGroupData Data = WhisperOrGroupDatas[TempIndex];
		if (Data.ChannelType == ChatType::Whisper && Data.Name == Name)
		{
			Index = TempIndex;
			return Data;
		}
	}
	Index = -1;
	return FChatWhisperAndGroupData();
}


void URoleChatInterface::AddWhisper(FString WhisperName, bool bNotifyBP/* = true*/)
{
	///<密聊对象不是玩家自己 
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	FString PlayerName = UGolbalBPFunctionLibrary::GetFStringPropertyValue(PlayerId, TEXT("playerName"));
	if (PlayerName.IsEmpty() || (!PlayerName.Compare(WhisperName)))
		return;

	int32 Index;
	FChatWhisperAndGroupData WhisperData = GetWhisperDataByName(WhisperName, Index);
	if (Index > -1)
	{
		WhisperOrGroupDatas.RemoveAt(Index);
		WhisperOrGroupDatas.Add(WhisperData);
	}
	else
	{
		FChatWhisperAndGroupData TempData;
		TempData.ChannelType = ChatType::Whisper;
		TempData.Name = WhisperName;
		if (WhisperOrGroupDatas.Num() >= MaxWhisperAndGroupData)
		{
			WhisperOrGroupDatas.RemoveAt(0);
			
			WhisperOrGroupDatas.Add(TempData);
		}
		else
		{
			WhisperOrGroupDatas.Add(TempData);
		}
	}
	if(bNotifyBP)
		OnAddWhisper(WhisperName);
}


void URoleChatInterface::onReceiveDeletePage_Implementation(int pageType)
{
	DeletePage((ChatPageType)pageType);
}

void URoleChatInterface::onReceiveChatMessageCB(const FVariant& chatData)
{
	FChatData data;
	AliasChatData::CreateFromVariant(chatData, data);
	onReceiveChatMessage(data);
}

void URoleChatInterface::CLINT_onChatQueryRoleExist_Implementation(const bool RoleExist)
{
	//密语对象是否存在，如果存在就切换到私聊频道
	if (RoleExist)
	{
		AddWhisper(WhisperPlayerName);
	}
	else
	{
		WhisperPlayerName = TEXT("");
	}
}


void URoleChatInterface::InitBlueCB()
{
	ArrBlueFunc.Add("onReceiveChatMessageCB");
	ArrBlueFunc.Add("onStatusMessage");
	ArrBlueFunc.Add("onReceiveQuickSettings");
	ArrBlueFunc.Add("onChangeQuickSettings");
	ArrBlueFunc.Add("onReceivePageSettings");
	ArrBlueFunc.Add("onReceiveDeletePage");
	ArrBlueFunc.Add("onReceivePageData");
	ArrBlueFunc.Add("onReceiveNewPageData");
	ArrBlueFunc.Add("CLINT_onChatQueryRoleExist");
	Supper::InitBlueCB();
}

void URoleChatInterface::onReceivePageSettings(const FVariant& variant)
{
	TArray<FChatPageData> data;
	AliasChatData::CreateFromVariantToPage(variant, data);
	//初始化标签页数据和标签页下聊天数据
	InitPage(data);
}

void URoleChatInterface::onReceivePageData(const FVariant& variant)
{
	FChatPageData data;
	AliasChatData::CreateFromVariantToPageData(variant, data);
	
	ChangePage(data);
}

void URoleChatInterface::onReceiveNewPageData(const FVariant& variant)
{
	FChatPageData data;
	AliasChatData::CreateFromVariantToPageData(variant, data);
	//增加标签页
	AddNewPage(data);
}

void URoleChatInterface::RPC_onRoleSendChatMessage(const FString& UNICODE_1, const FString& STRING_1, const FString& UNICODE_2, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::RPC_onRoleSendChatMessage : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(UNICODE_1);
	args.Add(STRING_1);
	args.Add(UNICODE_2);
	args.Add(STRING_2);

	entity->CellCall(TEXT("onRoleSendChatMessage"), args);
}

void URoleChatInterface::RPC_onRoleSendGMCommandMessage(const FString& STRING_1, const FString& STRING_2, const FString& UNICODE_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::RPC_onRoleSendGMCommandMessage : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);
	args.Add(UNICODE_1);

	entity->CellCall(TEXT("onRoleSendGMCommandMessage"), args);
}

void URoleChatInterface::RPC_onRoleSendGroupMessage(const int32& INT32_1, const FString& UNICODE_1, const FString& STRING_1, const FString& UNICODE_2, const FString& STRING_2, const int32& INT32_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::RPC_onRoleSendGroupMessage : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);
	args.Add(UNICODE_1);
	args.Add(STRING_1);
	args.Add(UNICODE_2);
	args.Add(STRING_2);
	args.Add(INT32_2);

	entity->CellCall(TEXT("onRoleSendGroupMessage"), args);
}


void URoleChatInterface::RPC_receiveReviseQS(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface:::RPC_receiveReviseQS : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("receiveReviseQS"), args);
}

void URoleChatInterface::RPC_receivePageSettings()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::RPC_receivePageSettings : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("receivePageSettings"), args);
}

void URoleChatInterface::RPC_receiveResetPageSettings(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::RPC_receiveResetPageSettings : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("receiveResetPageSettings"), args);
}

void URoleChatInterface::RPC_receiveMakeNewPage(const FString& STRING_1, const FString& UNICODE_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::RPC_receiveMakeNewPage : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(UNICODE_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("receiveMakeNewPage"), args);
}

void URoleChatInterface::RPC_receiveDeletePage(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::RPC_receiveDeletePage : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("receiveDeletePage"), args);
}

void URoleChatInterface::RPC_receiveChangePageData(const FString& UNICODE_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::RPC_receiveChangePageData : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(UNICODE_1);

	entity->CellCall(TEXT("receiveChangePageData"), args);
}

void URoleChatInterface::RPC_chatQueryRoleIsInTable(const FString& UNICODE_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleChatInterface::RPC_chatQueryRoleIsInTable : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(UNICODE_1);

	entity->CellCall(TEXT("CELL_chatQueryRoleIsInTable"), args);
}

CONTROL_COMPILE_OPTIMIZE_END