#pragma once
#include "GameData/CS3Object.h"
#include "UIFixerManager.generated.h"

/*
* 文件名称：UIFixerManager.h
* 功能说明：界面位置管理类
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-06-14
*/

class UBaseWindow;

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UUIFixerManager : public UCS3Object
{
	GENERATED_BODY()
		UUIFixerManager();
	~UUIFixerManager();

public:

	static UUIFixerManager* GetInstance();
	/**
	*当调用创建界面时，初始化界面的位置
	*
	*@param UBaseWindow* 界面窗口
	*
	*@return 无
	*/
	void OnWindowInit(UBaseWindow* window);

	/**
	*界面打开时重置界面位置（初始位置）
	*
	*@param window 显示的界面
	*
	*@return 无
	*/
	void OnRecovery(UBaseWindow* window);
	
	/**
	*设置窗口DockStyle
	*
	*@param window 设置的界面
	*
	*@return 无
	*/
	void UpdateDockStyle(UBaseWindow* window);

	/**
	*当角色进入世界时重置界面位置
	*
	*@param UBaseWindow* 界面窗口
	*
	*@return 无
	*/
	void OnRoleEnterWorld();

	/**
	*当分辨率改变时被调用
	*
	*@param preReso 旧分辨率
	*
	*@return 无
	*/
	void OnResolutionChanged(FVector2D preReso, float PreScale, FVector2D NewReso);

private:
	/**
	*初始化界面的位置
	*
	*@param UBaseWindow* 界面窗口
	*
	*@return 无
	*/
	void FirstInitFix(UBaseWindow* window);
	/**
	*当分辨率改变时，调用它来修正 ui 的位置
	*
	*@param preReso 旧分辨率
	*@param UBaseWindow* 界面窗口
	*
	*@return 无
	*/
	void AdaptDock(FVector2D preReso, float PreScale, FVector2D newReso, UBaseWindow* window);
/*
private:
	static UUIFixerManager* Instance;*/
};
