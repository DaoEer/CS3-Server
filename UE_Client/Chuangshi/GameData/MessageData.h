#pragma once

#include "Engine/DataTable.h"
#include "ChatType.h"
#include "GameData/UIDataDefine.h"
#include "GameData/CsvTableRowBase.h"
#include "MessageData.generated.h"

/**
* 文件名称：MessageData.h
* 功能说明：
* 文件作者：luocheng
* 目前维护：wuxiaoou
* 创建时间：2016-11-04
*/

UENUM(Blueprintable)
enum class RT_BTN_TYPE : uint8
{
	RT_OK		UMETA(DisplayName = "RT_OK"),
	RT_CANCEL	UMETA(DisplayName = "RT_CANCEL"),
};


#pragma region 消息类型
/**
* 消息类型
*/
UENUM(Blueprintable)
enum class MESSAGE_TYPE : uint8
{
	///弹出窗口提示
	MESSAGE_TYPE_DIALOG = 101	UMETA(DisplayName = "MESSAGE_TYPE_DIALOG"),
	///聊天窗口提示
	MESSAGE_TYPE_CHAT = 102		UMETA(DisplayName = "MESSAGE_TYPE_CHAT"),
	///屏幕文本提示
	MESSAGE_TYPE_PROMPT = 103	UMETA(DisplayName = "MESSAGE_TYPE_PROMPT"),
	///副本倒计时提示
	MESSAGE_TYPE_COUNTDOWN = 104	UMETA(DisplayName = "MESSAGE_TYPE_COUNTDOWN"),
	///AI小半身像对话提示
	MESSAGE_TYPE_AI_PORTRAIT_DIALOG = 115 UMETA(DisplayName = "MESSAGE_TYPE_AI_PORTRAIT_DIALOG"),
};
#pragma endregion


#pragma region 对话框提示按钮样式
/**
*对话框提示按钮样式
*/
UENUM(BlueprintType)
enum class MESSAGE_BTN_TYPE : uint8
{
	///
	MB_TYPE_OK = 0			UMETA(DisplayName = "MB_OK"),
	///
	MB_TYPE_CANCEL = 1		UMETA(DisplayName = "MB_CANCEL"),
	///
	MB_TYPE_OK_CANCEL = 2	UMETA(DisplayName = "MB_OK_CANCEL"),
};
/**
*对话框按钮倒计时操作类型
*/
UENUM(BlueprintType)
enum class COUNT_DOWN_TIME_TYPE : uint8
{
	///倒计时结束关闭消息窗口
	CD_OVER_CLOSE_WINDOW = 0	UMETA(DisplayName = "CD_OVER_CLOSE_WINDOW"),
	///倒计时结束激活操作按钮：用于对话框消息类型
	CD_OVER_SHOW_BTN = 1		UMETA(DisplayName = "CD_OVER_SHOW_BTN"),
};
#pragma endregion


#pragma region 屏幕提示类型
/**
*屏幕提示类型
*/
UENUM(BlueprintType)
enum class MESSAGE_PROMPT_TYPE : uint8
{
	///无提示
	MESSAGE_TYPE_PROMPT_NONE = 0 UMETA(DisplayName = "MESSAGE_TYPE_PROMPT_NONE"),
	///系统提示：屏幕中央文本提示
	MESSAGE_TYPE_PROMPT_CENTER = 1	UMETA(DisplayName = "MESSAGE_TYPE_PROMPT_CENTER"),
	///屏幕提示：世界公告
	MESSAGE_TYPE_PROMPT_WORLD = 2   UMETA(DisplayName = "MESSAGE_TYPE_PROMPT_WORLD"),
	///屏幕提示：场景提示
	MESSAGE_TYPE_PROMPT_SCENE = 3  UMETA(DisplayName = "MESSAGE_TYPE_PROMPT_SCENE"),
	///屏幕提示：区域提示
	MESSAGE_TYPE_PROMPT_AREA = 4  UMETA(DisplayName = "MESSAGE_TYPE_PROMPT_AREA"),
	///屏幕提示：提醒类提示
	MESSAGE_TYPE_PROMPT_REMIND = 5 UMETA(DisplayName = "MESSAGE_TYPE_PROMPT_REMIND"),
	///屏幕提示：警告类提示
	MESSAGE_TYPE_PROMPT_WARNING = 6 UMETA(DisplayName = "MESSAGE_TYPE_PROMPT_WARNING"),
};
#pragma endregion


#pragma region 提示消息管理配置数据
/**
* 提示消息管理配置数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMESSAGE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
	///消息内容
	UPROPERTY(EditAnywhere, BlueprintReadWrite,DisplayName = "Message")
		FString Message;
	///消息标题：用于对话框类型或者有标题的消息类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Title")
		FString Title;
	///消息类型（数组可配1个或多个，配多个会弹出多种提示）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MessageTypes")
		TArray<MESSAGE_TYPE> MessageTypes;
	///消息框按钮样式：用于对话框或者具有按钮的消息类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "DialogType")
		MESSAGE_BTN_TYPE DialogType;
	///对话框按钮显示文本：用于对话框消息类型（默认“确定”、“取消”文本显示）（若按钮样式是MB_CANCEL，想配置按钮显示文本为“否”，则修改数组第二个元素值，即将“取消”改为“否”）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "DialogBtnTexts")
		TArray<FString> DialogBtnTexts = {TEXT("确定"),TEXT("取消") };
	///父窗口消息类型：用于对话框消息类型（若配置了父窗口类型，则关闭对应的父窗口界面时同时关闭该消息框）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ParentWindowType")
		FString ParentWindowType;
	///是否遮盖其他窗口【消息类型为MESSAGE_TYPE_DIALOG对话框才需要配这项，默认为False不遮盖】
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsCover")
		bool IsCover = false;
	///是否显示对话框文本消息参数倒计时，倒计时时间由参数配置，倒计时结束默认点确定按钮【消息类型为MESSAGE_TYPE_DIALOG对话框才需要配这项，默认为False不显示对话框文本消息倒计时】
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsDialogArgCountDown")
		bool IsDialogArgCountDown = false;
	///对话框文本倒计时消息 配置参数索引即配置倒计时时间的那个字段在参数列表中的索引（默认0，表示第一个参数）【消息类型为MESSAGE_TYPE_DIALOG对话框，IsDialogArgCountDown配True才需要配这项】
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TimerArgIndex")
		int32 TimerArgIndex = 0;
	///持续时间：可用作对话框按钮倒计时持续时间 或 屏幕文本提示显示持续时间 或 半身像消息界面持续时间（默认-1不显示倒计时，目前只有对话框消息MESSAGE_TYPE_DIALOG、小半身像消息MESSAGE_TYPE_AI_PORTRAIT_DIALOG和屏幕提示消息MESSAGE_PROMPT_TYPE需要）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "HoldTime")
		int32 HoldTime = -1;
	///对话框按钮倒计时操作类型【消息类型为MESSAGE_TYPE_DIALOG，并且配了HoldTime才需要配这项】
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CountDownType")
		COUNT_DOWN_TIME_TYPE CountDownType;
	///聊天频道消息类型（数组可配多个）【消息类型为MESSAGE_TYPE_CHAT聊天窗口提示才需要配这项】
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ChatGroups")
		TArray<ChatType> ChatGroups;
	///屏幕提示消息类型【消息类型为MESSAGE_TYPE_PROMPT屏幕提示才需要配这项】
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PromptType")
		MESSAGE_PROMPT_TYPE PromptType;


public:

	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		bool MessageResult = !Message.TrimStartAndEnd().IsEmpty();
		bool MessageTypesResult = true;
		bool ChatGroupsResult = true;
		if (!MessageResult) ResultInfo.CheckLog += FString::Printf(TEXT("Message cannot be empty!  "));
		if (MessageTypes.Num() == 0)
		{
			MessageTypesResult = false;
			ResultInfo.CheckLog += FString::Printf(TEXT("MessageTypes cannot be empty!  "));
		}
		else
		{
			for (auto type : MessageTypes)
			{
				int index = 0;
				if (!(type >= (MESSAGE_TYPE)101 && type <= (MESSAGE_TYPE)115))
				{
					MessageTypesResult = false;
					ResultInfo.CheckLog += FString::Printf(TEXT("MessageTypes: index(%d) is config error!  "), index);
				}
				else
				{
					if (type == (MESSAGE_TYPE)102 && ChatGroups.Num() == 0)
					{
						ChatGroupsResult = false;
						ResultInfo.CheckLog += FString::Printf(TEXT("ChatGroups need to config!  "));
					}
				}
				index++;
			}
		}
		if (MessageResult && MessageTypesResult && ChatGroupsResult)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	};
};
#pragma endregion

/*
*成功或失败等文字动画提示
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTextAnimationMessage : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<界面类型（界面打开才显示，不填则没有限制，数组成员之间是或的关系）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> WindowType;
	///<动画序列帧纹理贴图
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> Texture;
	///<动画序列帧列数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Column;
	///<动画序列帧行数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Row;
	///<动画序列帧忽略最后N帧
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Ignore;
	///<动画总播放时间（秒）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float PlayTime;
	///<动画尺寸
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector2D Size;
	///<语音ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString AudioID;
	///<备注说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Note;
};

/**
* 今日不再提示记录
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FUnRepeatData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FUnRepeatData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MsgID;
};