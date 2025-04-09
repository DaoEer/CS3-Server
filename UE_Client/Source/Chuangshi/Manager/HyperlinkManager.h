#pragma once
#include "GameData/CS3Object.h"
#include "Guis/CS3RichTextBlock.h"
#include "HyperlinkManager.generated.h"

/*
* 文件名称：HyperlinkManager.h
* 功能说明：超链接管理类
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-08-29
*/

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UHyperlinkManager : public UCS3Object
{
	GENERATED_BODY()
		UHyperlinkManager();
	~UHyperlinkManager();

public:
	static UHyperlinkManager* GetInstance();

	/**
	*初始化
	*
	*@return 无
	*/
	void init();

	void OnHyperlinkClicked(UCS3RichTextBlock* RichText, FString LinkMark);

	UFUNCTION(BlueprintImplementableEvent, Category = "HyperlinkManager")
	void OnHLChatRichText(const UCS3RichTextBlock* RichText, const FString& MarkPrefix, const FString& MarkValue);

	UFUNCTION(BlueprintImplementableEvent, Category = "HyperlinkManager")
		void OnCopyHyperLinkToChat(const FString& MarkPrefix, const FString& MarkValue);

	///<将转义符格式富文本字符串替换为普通字符串
	UFUNCTION(BlueprintCallable, Category = "HyperlinkManager")
		FString ConvertRichTextToCommonText(FString InRichText);

private:
	/**
	*将转义符格式富文本字符串（纯超链接）替换为普通字符串
	*
	*@param	InRichText 富文本字符串
	*@param	Regex 正则表达式
	*@return 转换后的字符串
	*/
	FString ConvertHyperLinkRichTextToCommonText(FString InRichText, FString Regex);

	/**
	*根据不同的超链接类型，进行细分处理
	*
	*@param	CS3RichTextBlock RichText	 : 显示超链接的多行文本控件
	*@param	FString	linkMark : 超链接标记
	*@return 无
	*/
	void ParseProcess(UCS3RichTextBlock* RichText, FString LinkMark);
	/**
	*实现导航到 NPC 的超链接
	*
	*@param	CS3RichTextBlock RichText	 : 显示超链接的多行文本控件
	*@param	FString	linkMark : 超链接标记
	*@return 无
	*/
	void HLGoto(UCS3RichTextBlock* RichText, FString LinkMark);
	/**
	*自动寻路到 NPC 位置
	*
	*@return 无
	*/
	void RunToNpc(UCS3RichTextBlock* RichText, FString LinkMark);

	/**
	*实现显示聊天物品信息显示超链接
	*
	*@param	CS3RichTextBlock RichText	 : 显示超链接的多行文本控件
	*@param	FString	linkMark : 超链接标记
	*@return 无
	*/
	void HLChatItem(UCS3RichTextBlock* RichText, FString LinkMark);
	/**
	*实现聊天玩家名称超链接
	*
	*@param	CS3RichTextBlock RichText	 : 显示超链接的多行文本控件
	*@param	FString	linkMark : 超链接标记
	*@return 无
	*/

	void HLChatRichText(UCS3RichTextBlock* RichText, FString MarkPrefix, FString MarkValue);
	/**
	*点击超链接时被调用
	*
	*@param	CS3RichTextBlock RichText	 : 显示超链接的多行文本控件
	*@param	FString	linkMark : 超链接标记
	*@return 无
	*/
	void CopyHyperLinkProcess(UCS3RichTextBlock* RichText, FString LinkMark);

	/**
	*实现导航到 NPC 的超链接
	*
	*@param	CS3RichTextBlock RichText	 : 显示超链接的多行文本控件
	*@param	FString	linkMark : 超链接标记
	*@return 无
	*/
	void JoinTeam(UCS3RichTextBlock* RichText, FString LinkMark);

	/**
	*打开界面
	*
	*@param	CS3RichTextBlock RichText	 : 显示超链接的多行文本控件
	*@param	FString	linkMark : 超链接标记
	*@return 无
	*/
	void OpenUI(UCS3RichTextBlock* RichText, FString LinkMark);

private:
	//static UHyperlinkManager* Instance;

	TArray<FString> HyperLinks;
};
