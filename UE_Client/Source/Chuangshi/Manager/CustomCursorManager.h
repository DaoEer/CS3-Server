// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "GameData/CS3Object.h"
#include "Guis/CursorUIWidget.h"
#include "GameData/CursorData.h"
#include "CustomCursorManager.generated.h"

/*
* 文件名称：CustomCursorManager.h
* 功能说明：
* 文件作者：shenbing
* 目前维护：zhangdan
* 创建时间：2016-10-20
*/

/**
*自定义光标管理器
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UCustomCursorManager : public UCS3Object
{
	GENERATED_BODY()

public:
	UCustomCursorManager();
	~UCustomCursorManager();

	static UCustomCursorManager* GetInstance();
	void ClearInstanceData();
	void Init();///<初始鼠标数据

	/**
	*BlueprintCallable,设置光标类型
	*
	*@param cursorType 光标类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CustomCursorManager")
	void SetCursor(FString cursorState);

	UFUNCTION(BlueprintCallable, Category = "CustomCursorManager")
	void SetCursorUI(UCursorUIWidget* NewCursorUI);

	UFUNCTION(BlueprintCallable, Category = "CustomCursorManager")
	void DefaultCursor();///<默认光标

	/**
	*获得鼠标状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintPure, Category = "CustomCursorManager")
	FString CurrentCursorState() { return CurCursorState; }///<默认光标
	/**
	*BlueprintCallable,锁定光标
	*
	*@param cursorType 光标类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CustomCursorManager")
	void LockCursor(FString cursorState);

	/**
	*BlueprintCallable,修改光标类型
	*
	*@param cursorType 光标类型
	*@param newCursorType 光标新类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CustomCursorManager")
	void UnLockCursor(FString cursorState, FString newCursorState);

	/**
	*鼠标是否锁定
	*
	*/
	UFUNCTION(BlueprintCallable, Category = "CustomCursorManager")
		bool CheckLockCursor();

	/**
	*当前是否是特殊鼠标状态
	*
	*/
	UFUNCTION(BlueprintPure, Category = "CustomCursorManager")
		bool IsEspecialCursorState();
	/**
	*恢复鼠标状态
	*
	*/
	UFUNCTION(BlueprintCallable, Category = "CustomCursorManager")
		void ResetCursor();
	/**
	*当隐藏鼠标操作时被调用
	*
	*@return 无
	*/
	void OnHideMouse();
	
#pragma region	/** 持有道具鼠标状态相关 */

public:
	/**
	*BlueprintCallable,左键点击抓取
	*
	*@param Widget 左键抓取状态鼠标跟随控件
	*@param Data 抓取的道具数据
	*
	*@return 无
	*/
	void SetLeftMouseCaptureCursor(UUserWidget* Widget, FDragDropOperationData Data);
	/**
	*BlueprintCallable,清除抓取鼠标
	*
	*@return 无
	*/
	void CancelLeftMouseCaptureCursor();
	/**
	*BlueprintCallable,获取抓取数据
	*
	*@return LeftMouseCaptureData 抓取数据
	*/
	FDragDropOperationData GetLeftMouseCaptureData();

private:

	void InitLeftMouseCaptureData();///<初始抓取数据
	/**
	*保存抓取数据
	*
	*@param Widget 左键抓取状态鼠标跟随控件
	*@param Data 抓取数据
	*
	*@return 无
	*/
	void SaveLeftMouseCaptureData(UUserWidget* Widget, FDragDropOperationData Data);
	
	void ClearLeftMouseCaptureData();///<清除抓取数据

#pragma endregion

private:
	bool locked = false;///<是否锁定
	FString CurCursorState;///<鼠标状态
	UPROPERTY()
	UCursorUIWidget* CursorUI;

	UPROPERTY()
	UUserWidget* DraggedWidget;///<左键抓取状态鼠标跟随控件
	FDragDropOperationData DraggedData;///<左键抓取数据
	//static UCustomCursorManager* Instance;
};
