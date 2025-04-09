// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Util/CS3Debug.h"
#include "JsonObject.h"
#include <vector>
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/ChatType.h"
#include "Entity/Alias.h"
#include "GameData/ChatData.h"
#include "GameData/ChatPageData.h"
#include "GameData/ChatChannelData.h"
#include "GameData/ChatSettingData.h"
#include "RoleChatInterface.generated.h"

/*
* 文件名称：RoleChatInterface.h
* 功能说明：角色聊天接口类
* 文件作者：huangshijie
* 目前维护：hejingke
* 创建时间：2016-08-22
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URoleChatInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleChatInterface();
	~URoleChatInterface();
	static FString GetName() { return TEXT("RoleChatInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleChatInterface.BP_RoleChatInterface_C'"); } //获取蓝图对象路径

	virtual void onEnterWorld()override;///< 当Entity进入世界时，此方法被调用
	virtual void onLeaveWorld()override; ///< 当Entity离开世界（被销毁时）时，此方法被调用

	/**
	*Define Method
	*BlueprintCallable, 接收页签数据
	*
	*@param pageDatas 页签数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
		void onReceivePageSettings(const FVariant& pageDatas);

	/**
	*Define Method
	*BlueprintCallable, 接收页签设置数据
	*
	*@param pageDatas 页签数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
	void onReceivePageData(const FVariant& pageData);

	/**
	*Define Method
	*BlueprintCallable, 新建一个页签
	*
	*@param pageDatas 页签数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
	void onReceiveNewPageData(const FVariant& newPageData);

	/**
	*Define method
	*BlueprintImplementableEvent, 通知蓝图，页签删除回调
	*
	*@param pageType 页签类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
		void onReceiveDeletePage(int pageType);

	/**
	*Define method
	*BlueprintCallable, 接收聊天数据
	*
	*@param data 聊天数据
	*
	*@return 无
	*/
	//UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
	void onReceiveChatMessageCB(const FVariant& chatData);

	virtual void InitBlueCB() override;
	/**
	*Define method
	*
	*
	*@param bool 是否存在该玩家
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
		void CLINT_onChatQueryRoleExist(const bool RoleExist);

public:
	/**
	*BlueprintImplementableEvent, 接收聊天数据
	*
	*@param data 聊天数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|Entity")
		void onReceiveChatMessage(const FChatData& data);
	/**
	*BlueprintImplementableEvent, 通知蓝图，聊天页签数据
	*
	*@param pageDatas 页签数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|Entity")
		void onReceivePageSettingsDatas(const TArray<FChatPageData>& pageDatas);

	/**
	*BlueprintImplementableEvent, 通知蓝图，一条页签数据
	*
	*@param pageDatas 页签数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|Entity")
		void onReceiveAPageData(const FChatPageData& pageData);

	/**
	*BlueprintImplementableEvent, 通知蓝图，新的页签创建回调
	*
	*@param pageDatas 页签数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "cs3|Entity")
		void onReceiveANewPageData(const FChatPageData& pageData);

	/**
	*BlueprintImplementableEvent, 通知蓝图，增加私聊联系人
	*
	*@param Name 私聊玩家名
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleChatInterface|WhisperOrGroup")
		void OnAddWhisper(const FString& WhisperName);

public:
	/**
	*BlueprintCallable，通过标签页类型获取标签页数据
	*
	*@param PageType 标签页
	*@param Index 索引
	*
	*@return FPageChatData 标签页数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|Tab")
		FChatPageData GetPageDataByPageType(ChatPageType PageType, int32& Index);
	/**
	*BlueprintCallable，通过标签页获取此标签页下的聊天数据
	*
	*@param PageType 标签页
	*@param Index 索引
	*
	*@return FPageChatData 标签页的聊天数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|Tab")
		FTabChatData GetChatDataByPageType(ChatPageType PageType, int32& Index);
	/**
	*BlueprintCallable，通过标签页获取此标签页下的聊天搜索数据
	*
	*@param PageType 标签页
	*@param Index 索引
	*
	*@return FPageChatData 标签页的聊天搜索数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|Find")
		FTabFindChatData GetFindChatDataByPageType(ChatPageType PageType, int32& Index);
	/**
	*BlueprintCallable，通过聊天频道获取频道设置
	*
	*@param ChannelType 频道类型
	*@param Index 索引
	*
	*@return FPageChatData 频道设置数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|Channel")
		FChatChannelSettingData GetChannelDataByChatType(ChatType ChannelType, int32& Index);

	/**
	*BlueprintCallable，通过频道类型获取私聊或讨论组数据
	*
	*@param ChannelType 频道类型
	*
	*@return TArray<FChatWhisperAndGroupData> 私聊或讨论组数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|WhisperOrGroup")
		TArray<FChatWhisperAndGroupData> GetWhisperOrGroupDataByChatType(ChatType ChannelType);
	/**
	*BlueprintCallable，通过私聊玩家名获取私聊数据
	*
	*@param Name 玩家名
	*@param Index 索引
	*
	*@return FChatWhisperAndGroupData 私聊数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|WhisperOrGroup")
		FChatWhisperAndGroupData GetWhisperDataByName(FString Name, int32& Index);
	/**
	*BlueprintCallable，增加私聊玩家
	*
	*@param WhisperName 玩家名
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|WhisperOrGroup")
		void AddWhisper(FString WhisperName, bool bNotifyBP = true);
	/**
	*BlueprintCallable，获取能使用的频道类型
	*
	*@return TArray<ChatType> 能使用的频道类型
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|ChatSetting")
		TArray<ChatType> GetCanUseChatTypeDatas();
	/**
	*BlueprintCallable，获取开启等级
	*
	*@return TArray<ChatType> 已开启的频道类型
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|ChatSetting")
		TArray<ChatType> GetOpenLevelChatTypeDatas();
	/**
	*BlueprintCallable，获取开启条件
	*
	*@return ChannelType 频道类型
	*
	*@return int32 消息ID
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|ChatSetting")
		int32 GetSwitchConditionsByChatType(ChatType ChannelType);

public:
	/**
	*请求增加新的标签页
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|Tab")
		void RequestMakeNewPage();
	/**
	*修改频道颜色设置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|ChatSetting")
		void ChangeChatChannelColor(TArray<FChatChannelSettingData> Datas);

	///<保存聊天设置数据
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|ChatSetting")
		void SaveChatBaseSetting();
	
	///<根据名字获取聊天设置数据
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface|ChatSetting")
		FChatSettingData GetChatBaseSettingByName(FString Name);

	/**
	*FColor值转为十六进制字符串
	*
	*@param IsShowA 是否显示透明度
	*
	*@return 十六进制字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface")
		FString ConvertColorToHex(FColor Color, bool IsShowA = false);
	/**
	*十六进制字符串转为FColor
	*
	*@return FColor
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface")
		FColor ConvertColorFromHex(FString HexString);

	///<重置聊天频道颜色
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface")
		void ChangeChatTypeColor(TArray<FChatChannelSettingData>  ChatChannelSettingData);
	///<重置聊天频道颜色
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface")
		void RestoreDefaultsChatTypeColor();
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleChatInterface")
		void BP_ChangeChatTypeColor();

	///<重置聊天频道快捷键
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface")
		void RestoreDefaultsShortCut();
	///<重置聊天频道快捷键
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface")
		void ChangeShortCutData(TArray<FChatChannelSettingData>  ChatChannelSettingData);
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleChatInterface")
		void BP_ChangeShortCutData();

	///<重置聊天界面设置
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface")
		void RestoreDefaultsWinSetting();
	///<聊天界面设置
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface")
		void ChangeChatBaseSettingsDatas(bool IsHide,bool IsSHowTime,float BgAlpha,FColor BgColor);
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleChatInterface")
		void BP_ChangeChatBaseSettingsDatas();

	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface")
		void OnChatShortcutSwitchConditionsChange();
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleChatInterface")
		void BP_ChangeChatShortcutDatas();
	UFUNCTION(BlueprintCallable, Category = "RoleChatInterface")
		bool CheckChatShortcutDatas();
private:
	/**
	*发送聊天数据
	*
	*@param chatData 聊天数据
	*
	*@return 无
	*/
	void onRoleSendChatMessage(const FVariant& chatData);

	/**
	*发送聊天GM数据
	*
	*@param dstEntityID 目标EntityID
	*@param cmd GM命令
	*@param message GM消息
	*
	*@return 无
	*/
	void onRoleSendGMCommandMessage(const FString& dstEntityID, const FString& cmd, const FString& message);
	/**
	*初始化标签页和页签下聊天数据
	*
	*@param PageDatas 标签页数据
	*
	*@return 无
	*/
	void InitPage(TArray<FChatPageData> PageDatas);
	/**
	*删除标签页
	*
	*@param PageType 标签页
	*
	*@return 无
	*/
	void DeletePage(ChatPageType PageType);
	/**
	*增加标签页
	*
	*@param PageData 标签页数据
	*
	*@return 无
	*/
	void AddNewPage(FChatPageData PageData);
	/**
	*修改标签页
	*
	*@param PageData 标签页数据
	*
	*@return 无
	*/
	void ChangePage(FChatPageData PageData);
	/**
	*是否能增加新的标签页
	*
	*@param PageData 标签页数据
	*
	*@return 无
	*/
	bool CanCreateNewPage(FChatPageData& PageData);
	/**
	*初始化聊天设置配置表数据
	*
	*@return 无
	*/
	void InitChatChannelData();

	/**
	*改变快捷键设置
	*
	*@return 无
	*/
	void ChangeQuickSetting(TArray<FChatChannelData> ChannelData);
	/**
	*初始化快捷键设置
	*
	*@return 无
	*/
	void InitChatShortCutDatas();

	///<初始化Base设置数据
	void InitBaseSettingData();


	//Exposed调用
public:
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onRoleSendChatMessage(const FString& UNICODE_1, const FString& STRING_1, const FString& UNICODE_2, const FString& STRING_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onRoleSendGMCommandMessage(const FString& STRING_1, const FString& STRING_2, const FString& UNICODE_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_onRoleSendGroupMessage(const int32& INT32_1, const FString& UNICODE_1, const FString& STRING_1, const FString& UNICODE_2, const FString& STRING_2, const int32& INT32_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_receiveReviseQS(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_receivePageSettings();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_receiveResetPageSettings(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_receiveMakeNewPage(const FString& STRING_1, const FString& UNICODE_1, const FString& STRING_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_receiveDeletePage(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_receiveChangePageData(const FString& UNICODE_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_chatQueryRoleIsInTable(const FString& UNICODE_1);

public:
	//聊天消息最大条数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MaxChatDataCount = 200;
	//密语消息最大条数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MaxWhisperAndGroupData = 3;
	//密聊最新其他玩家
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString LastWhisperPlayerName;
	//天音聊天数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FChatData> ChatTianYinData;
	//仙音聊天数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FChatData> ChatXianYinData;
	//标签页聊天数据 
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FTabChatData> TabChatDatas;
	//聊天设置数据 
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FChatPageData> ChatPageDatas;
	//频道设置数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FChatChannelSettingData> ChatChannelSettingDatas;
	//快捷键
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<ChatType> ChatShortcutDatas;
	//查询出的数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FTabFindChatData> ChatTabFindDatas;
	//私聊和讨论组数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FChatWhisperAndGroupData> WhisperOrGroupDatas;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FChatBaseSettingData BaseSettingData;
private:
	//频道配置表数据
	TArray<FChatChannelCfg> ChatChannelCfgDatas;
	FString WhisperPlayerName;
};