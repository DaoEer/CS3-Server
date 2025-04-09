#pragma once
#include "../CS3Base/BaseWindow.h"
#include "GameData/MessageData.h"
#include "CS3MessageBoxWidget.generated.h"

/*
* 文件名称：MessageBoxWidget.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-01-03
*/

class UMessageManager;

UCLASS(BlueprintType)
class CHUANGSHI_API UCS3MessageBoxWidget : public UBaseWindow
{
	GENERATED_BODY()
public:

	/**
	*BlueprintNativeEvent，显示消息框
	*@param msg 对话框消息实例
	*@param Key 服务器自动生成的值
	*@param Compotent 是cell 还是 base 发过来的
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3MessageBoxWidget")
		void ShowMessage(const UDialogMessage* msg, int32 Key, const FString& Compotent);

	/**
	*BlueprintNativeEvent，响应消息框按钮
	*@param BtnType 按钮类型 是或否
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3MessageBoxWidget")
		void ResponseMessageBtn(RT_BTN_TYPE BtnType);

public:
	///<消息ID
	UPROPERTY(BlueprintReadWrite, category = "MessageBoxWidget")
		FName MessageBoxID;
	///<是否锁屏
	UPROPERTY(BlueprintReadWrite, category = "MessageBoxWidget")
		bool IsCover;
};