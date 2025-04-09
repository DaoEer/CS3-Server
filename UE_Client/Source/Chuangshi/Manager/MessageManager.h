#pragma once
#include "CoreMinimal.h"
//#include "CfgManager.h"
#include "../GameData/ChatType.h"
#include "GameData/MessageData.h"
#include "GameData/CS3Object.h"
#include "GameData/UIDataDefine.h"
#include "Guis/CS3MessageBoxWidget.h"
#include "MessageManager.generated.h"

/*
* 文件名称：MessageManager.h
* 功能说明：提示消息管理类
* 文件作者：luocheng
* 目前维护：liyuxia
* 创建时间：2016-12-07
*/

DECLARE_DELEGATE_OneParam(FBtnClick, RT_BTN_TYPE);
DECLARE_MULTICAST_DELEGATE_OneParam(FBtnClickListener, RT_BTN_TYPE);
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnBtnClick, RT_BTN_TYPE,ClickBtnType);


class UConfigTable;
#pragma region 消息类及其扩展 : UMessage

/**
提示消息基类 : UMessage
*/
UCLASS(Blueprintable)
class CHUANGSHI_API UMessage:public UCS3Object
{
	friend class UMessageManager;
	GENERATED_BODY()

public:
	/**
	*从配置初始化消息
	*
	*@param	CfgData		配置表数据
	*@param args		替换参数
	*
	*@return 无
	*/
	virtual void CreateFromConfig(const FMESSAGE_DATA* CfgData, const FString& args);

protected:	
	virtual void Show() const;///<显示消息:虚方法，子类需实现对应的显示方式
	
	/**
	*字符串替换
	*
	*@param	replaceMessage 原字符串
	*@param	args			替换参数
	*@param	SplitChar		可选分隔符，默认“|”
	*
	*@return FString 替换后的字符串
	*/
	FString GetReplaceMessage(const FString& replaceMessage, const FString args = TEXT(""), FString SplitChar = TEXT("|"));

	/**
	*消息字符串替换为富文本，比如：参数1{0}参数2{1}  变成 <text color="#FFFFFFFF">参数1</text >{0}<text color="#FFFFFFFF">参数2</text >{1}现改用CS3RichText
	*
	*@param	replaceMessage 原字符串
	*
	*@return FString 替换后的字符串
	*/
	virtual FString GetFormatColorMessage(const FString& replaceMessage);

	virtual FString GetColorStr(const FString& ColorStr);

public:	
	///<消息ID	
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager")
		FName ID;
	///<消息内容
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager")
		FString Message;
	///<消息参数
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager")
		FString Args;
	///<消息配置内容（参数未合并之前的消息内容，即MessageCfg表格里面配置的Message字段）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager")
		FString MessageCfg;
	///<持续时间
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager")
		int32 HoldTime;
	///<消息类型
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager")
		TArray<MESSAGE_TYPE> messageTypes;
};

/**
对话框提示消息类  UDialogMessage
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UDialogMessage :public UMessage
{
	GENERATED_BODY()
public:
	///添加回调函数
	FDelegateHandle AddClickDelegate(FBtnClick EventBack);

	///移除回调函数
	void RevmoeClickDelegate(FDelegateHandle EventBackHandle);

	/**
	*触发回调事件
	*
	*@param	BtnType 点击按钮类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "MessageManager|DialogMessage")
		void OnTrigerClick(RT_BTN_TYPE BtnType);

protected:	
	virtual void Show() const override;///<	显示消息

	/** 
	*从配置初始化消息:重写父类方法
	*
	*@param	CfgData		配置表数据
	*@param	args		替换参数
	*
	*@return 无
	*/
	virtual void CreateFromConfig(const FMESSAGE_DATA* CfgData, const FString& args) override;

public:
	///<弹出框按钮类型
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager|DialogMessage")
		MESSAGE_BTN_TYPE DialogType;
	///<对话框按钮显示文本
	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, category = "MessageManager|DialogMessage")
		TArray<FString> DialogBtnTexts;
	///<父窗口消息类型
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager|DialogMessage")
		FString ParentWindowType;
	///<弹出框标题
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager|DialogMessage")
		FString Title;
	///<倒计时操作类型
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager|DialogMessage")
		COUNT_DOWN_TIME_TYPE CDTimerType;
	///<是否遮盖其他窗口
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager|DialogMessage")
		bool IsCover;
	///<是否显示对话框文本消息参数倒计时
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager|DialogMessage")
		bool IsDialogArgCountDown;
	///<配置倒计时时间的那个参数字段在参数列表中的索引	
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager|DialogMessage")
		int32 TimerArgIndex;
private:
	FBtnClickListener ClickEventList;	///<按钮点击回调事件

};

///聊天窗口提示消息类 : UChatMessage
UCLASS(BlueprintType)
class CHUANGSHI_API UChatMessage :public UMessage
{
	GENERATED_BODY()
protected:
	///显示消息:虚方法，子类需实现对应的显示方式
	virtual void Show() const override;

	/**
	*从配置初始化消息:重写父类方法
	*
	*@param	CfgData		配置表数据
	*@param	args		替换参数
	*
	*@return 无
	*/
	virtual void CreateFromConfig(const FMESSAGE_DATA* CfgData, const FString& args) override;

public:
	///<聊天频道类型
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager|ChatMessage")
	TArray<ChatType> ChatGroups;
};

/**
屏幕提示消息类  UPromptMessage
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UPromptMessage :public UMessage
{
	GENERATED_BODY()
protected:
	virtual void Show() const override;///<	显示消息

	/**
	*从配置初始化消息:重写父类方法
	*
	*@param	CfgData		配置表数据
	*@param	args		替换参数
	*
	*@return 无
	*/
	virtual void CreateFromConfig(const FMESSAGE_DATA* CfgData, const FString& args) override;

public:
	///<屏幕提示消息类型
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "MessageManager|PromptMessage")
	MESSAGE_PROMPT_TYPE promptMsgType;
};

/**
* 副本关闭倒计时提示消息类 : UCountDownMessage
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UCountDownMessage :public UMessage
{
	GENERATED_BODY()
protected:
	///显示消息:虚方法，子类需实现对应的显示方式
	virtual void Show() const override;
};


/**
* 半身像对话提示消息类 : UPortraitDialogMessage
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAIPortraitDialogMessage :public UMessage
{
	GENERATED_BODY()
protected:
	///显示消息:虚方法，子类需实现对应的显示方式
	virtual void Show() const override;
};

#pragma endregion


#pragma region 消息管理类 : UMessageManager

/**
* 消息管理类
*/
UCLASS(Blueprintable)
class CHUANGSHI_API UMessageManager : public UObject,public FTickableGameObject
{
	GENERATED_BODY()
public:
	///构造函数
	UMessageManager();

	/// 获取管理类实例
	static UMessageManager* GetInstance();

	/** 
	*显示消息
	*
	*@param  MessageID	消息ID
	*@param  EventBack    按钮回调事件:仅提示框消息会执行回调
	*
	*@return 无
	*/
	void ShowMessage(const int32& MessageID, FBtnClick EventBack = nullptr);

	/** 
	*显示消息
	*
	*@param  MessageID	消息ID
	*@param  args			替换参数
	*@param  EventBack    按钮回调事件:仅提示框消息会执行回调
	*
	*@return 无
	*/
	void ShowMessage(const int32& MessageID, const FString args, FBtnClick EventBack = nullptr, int32 Key = 0, const FString& Compotent = "");

	/**
	*BlueprintCallable，显示消息
	*
	*@param  MessageID	消息ID
	*@param  args			替换参数
	*@param  EventBack    按钮回调事件:仅提示框消息会执行回调
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, DisplayName = "ShowMessage", Category = "MessageManager")
	void BP_ShowMessageWithID(const int32 MessageID, const FString args, FOnBtnClick EventBack);

	/**
	*BlueprintCallable，显示消息:自定义消息
	*
	*@param  Message	自定义消息
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, DisplayName = "ShowMessage", Category = "MessageManager")
	void BP_ShowMessage(UMessage* Message);
	
	/**
	*显示消息:自定义消息
	*
	*@param  Message 自定义消息
	*
	*@return 无
	*/
	void ShowMessage(UMessage* Message);

	/**
	*BlueprintCallable，隐藏消息（隐藏只处理对话框消息类型，其他不管）
	*
	*@param  MessageID	消息ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, DisplayName = "HideMessage", Category = "MessageManager")
		void HideMessage(const int32 MessageID);

	/**
	*BlueprintCallable，隐藏全部消息（隐藏只处理对话框消息类型，其他不管）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, DisplayName = "HideAllMessage", Category = "MessageManager")
		void HideAllMessage();

	/**
	*BlueprintCallable，隐藏倒计时消息
	*
	*@param  MessageID	消息ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, DisplayName = "HideCountDownMessage", Category = "MessageManager")
		void HideCountDownMessage(const int32 MessageID);

	/**
	*BlueprintCallable，显示遮盖面板，锁屏
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "MessageManager")
		void ShowCoverPanel();

	/**
	*BlueprintCallable，是否有锁屏的消息框
	*
	*@return bool 是否有锁屏的消息框
	*/
	UFUNCTION(BlueprintCallable, Category = "MessageManager")
		bool HasCoverMessage();

	/**
	*BlueprintCallable，移除消息框
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "MessageManager")
		void RemoveMessageBoxData(FName MessageID);

public:
	/**
	*BlueprintNativeEvent，显示消息
	*
	*@param  msg 对话框消息实例
	*@param Key 服务器自动生成的值
	*@param Compotent 是cell 还是 base 发过来的
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "MessageManager")
	void ShowMessageBox(const UDialogMessage* msg, int32 Key, const FString& Compotent);

	/**
	*BlueprintNativeEvent,屏幕提示消息
	*
	*@param msg 消息
	*@param messageType 消息类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "MessageManager")
	void ShowPromptMessage(const UPromptMessage* msg);

	/**
	*BlueprintNativeEvent,显示聊天消息
	*
	*@param msg 消息
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "MessageManager")
	void ShowChatMessage(const UChatMessage* msg);

	/**
	*BlueprintNativeEvent,倒计时提示消息
	*
	*@param msg 消息
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "MessageManager")
	void ShowCountDownMessage(const UCountDownMessage* msg);

	/**
	*BlueprintNativeEvent,显示半身像消息
	*
	*@param msg 消息
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "MessageManager")
	void ShowAIPortraitDialogMessage(const UAIPortraitDialogMessage* msg);
	
	/**
	*BlueprintImplementableEvent,回调通知蓝图隐藏消息（倒计时消息类型）
	*
	*@param  MessageID	消息ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "MessageManager")
		void BP_HideCountDownMessage(const int32 MessageID);

	/**
	*BlueprintCallable，显示文字动画消息提示
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "MessageManager")
		void ShowTextAnimationMessage(FName AnimationID);
	/**
	*BlueprintCallable，获取文字提示动画资源
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "MessageManager")
		bool GetTextAnimation(FName AnimationID, FTextAnimationMessage& OutTextAnimationMessage);


	//今日不再提示数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FUnRepeatData> UnRepeatDatas;
	///<改变今日不再提示的配置
	UFUNCTION(BlueprintCallable, Category = "MessageManager")
		void ChangeRepeatData(const int32 MessageID);
	///保存今日不再提醒的消息配置
	UFUNCTION(BlueprintCallable, Category = "MessageManager")
		void SaveRepeatData();
	///是否今日不再提示
	UFUNCTION(BlueprintCallable, Category = "MessageManager")
		bool IsUnRepeat(const int32 MessageID);

public:
	/**
	*FTickableGameObject interface
	*
	*@param DeltaTime Tick一次时间
	*
	*@return 无
	*/
	virtual void Tick(float DeltaTime) override;

	/**
	*是否可tick，重写父类方法
	*
	*@return 可tick返回TRUE，否则返回FALSE
	*/
	virtual bool IsTickable() const override;

	/**
	*获取Tick ID
	*
	*@return TStatId Tick ID
	*/
	virtual TStatId GetStatId() const override;

public:
	UPROPERTY()
		TArray<UCS3MessageBoxWidget*> MessageBoxWidgetArray;

private:	
	const UConfigTable* GetSafeMessageTable();///<获取消息配置表
	
private:	
	//static UMessageManager* Instance;///<消息管理类实例	
	const UConfigTable* MessageTable;///<消息配置表	
	/**
	*初始化不再提示表
	*@return 无
	*/
	void InitUnRepeatData();

};

#pragma endregion
