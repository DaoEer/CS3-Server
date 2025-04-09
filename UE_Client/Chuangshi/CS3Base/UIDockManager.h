#pragma once
#include "GameData/CS3Object.h"
#include "GameData/UIDataDefine.h"
#include "UIDockManager.generated.h"

/*
* 文件名称：UIDockManager.h
* 功能说明：界面停靠管理类
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-01-10
*/

class UBaseWindow;

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UUIDockManager : public UCS3Object
{
	GENERATED_BODY()
	UUIDockManager();
	~UUIDockManager();

public:
	static UUIDockManager* GetInstance();
	void OnWindowCreatedOver(FString WindowType);///<界面创建完

private:
	/**
	*界面打开时重置界面位置（初始位置）
	*
	*@param window 显示的界面
	*
	*@return 无
	*/
	void RecoveryWindow(UBaseWindow* window);

	/**
	*当有一个窗口打开时排序界面位置
	*
	*@param window 显示的界面
	*
	*@return 无
	*/
	void SortWindowsByShow(UBaseWindow* window);

	/**
	*当有一个窗口隐藏时排序界面位置
	*
	*@param window 隐藏的界面
	*
	*@return 无
	*/
	void SortWindowsByHide(UBaseWindow* window);
	
	void Initialize();///<初始化	
	void Layout();///<排列所有 UI 停靠的位置

private:
	FVector2D StartPos;///<开始位置
	TArray<FString> SortWindowsType;///<排序停靠界面
	TArray<FString> RecoveryWindowsType;///<还原初始位置界面
	TArray<UBaseWindow*> ShowedWindows;///<显示的界面表

	//static UUIDockManager* Instance;
};
