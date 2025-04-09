// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/GameDefine.h"
#include "GameData/CS3Object.h"
#include "Operation/OperationData.h"
#include "ControllerModeMgr.generated.h"

/*
* 文件名称：ControllerModeMgr.h
* 功能说明：控制模式管理类
* 文件作者：yanghan
* 目前维护：huting
* 创建时间：2018-01-08
*/
DECLARE_STATS_GROUP(TEXT("UControllerModeMgr"), STATGROUP_UControllerModeMgr, STATCAT_Advanced);

UCLASS(BlueprintType)
class CHUANGSHI_API UControllerModeMgr : public UCS3Object
{
	GENERATED_BODY()
public:
	UControllerModeMgr() {};
	~UControllerModeMgr() {};
	virtual void BeginDestroy() override;
	static UControllerModeMgr* GetInstance();
public:
	/**
	*BlueprintCallable,初始化
	*
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable)
	void Init();
	/**
	*BlueprintCallable,分析执行输入信息
	*
	*@param FString InputInfor 输入信息
	*@param FKey InputKey 输入的Key值
	*@param float InputScale 输入的轴值
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable)
	void ExecuteInputInfor(FString InputInfor, FString InputKey, const float& InputScale, TArray<FString> OtherValue);
	/**
	*BlueprintCallable,改变模式
	*
	*@param ECONTROL_MODE ControlMode 控制模式
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable)
	void ChangeControllerMode(ECONTROL_MODE ControlMode, CC_MODE_REASON InReason, bool bIsBackMode = false, bool bIsIgnorePriority = false);

	/**
	*BlueprintCallable,恢复模式
	*从一个模式恢复到当前应当的模式（主要为背景模式）
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable)
	void RecoveryMode();

	/**
	*BlueprintCallable,恢复到系统设定模式
	*当想从一个背景模式（在设置界面无法设定的）
	*恢复到当前系统设定的模式时调用。
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable)
		void RecoverySettingMode();

	/**
	*BlueprintCallable,是否处于该模式
	*
	*@return bool
	*/
	UFUNCTION(BlueprintCallable)
	bool IsHaveMode(ECONTROL_MODE ControlMode) { return ControlMode == CurControllerMode; }
	
	/**
	*BlueprintCallable,是否从ACT模式转换成ALT模式,否则从ALT模式转换成ACT模式
	*
	*@return bool
	*/
	UFUNCTION(BlueprintCallable)
		bool ChangeControlModeFromACTToALT(bool bIsActToAlt = true);

	/**
	*BlueprintCallable,改变当前模式为非激活状态（离开窗口变为非激活状态）
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable)
		void ChangeControlModeToActive(bool bIsActive = false, bool bIsExcInst = true);

	TArray<FString> GetOtherValue() { return OtherValue; };
private:
	///获取默认表格数据
	void GetDefaultTable(TMap<FString, FInputInforAndInstruction>& TableDatas);
	///创建默认的信息与指令字典
	void CreatDeflautInputInforInstrMap(const TMap<FString, FInputInforAndInstruction>& TableDatas);
	///创建注册事件
	void CreatRegisterEvent(TArray<FInputInforAndInstruction>& Events);
	///通过模式获取模式的数据
	void GetModeDataByType(ECONTROL_MODE ControlMode,FControModeTable& ControModeData);
	///更新差异数据
	void UpdataInputInfor(TMap<FString, FInputInforAndInstruction>& TableDatas);
	///替换数据
	void ReplaceInputInfor(TMap<FString, FInputInforAndInstruction>& TableDatas);
		///切换模式信息
	void SwitchModeInfor(ECONTROL_MODE ControlMode);
	///切换注册事件
	void SwitchRegisterEvent(TArray<FInputInforAndInstruction>& Events);
	///获取优先级
	int32 GetModePriority(ECONTROL_MODE ControlMode);
	///在激活模式时执行指令)(bIsActive是否激活状态，bIsEnter是否进入执行指令还是离开执行指令)
	void ExecuteInstructionIfModeActive(ECONTROL_MODE ControlMode,bool bIsActive = true,bool bIsEnter = true);
public:
	///信息标识与指令字典
	TMap<FString,FInputInforAndInstruction> m_InforAndInstructions;
	///默认信息标识与指令字典
	TMap<FString, FInputInforAndInstruction> m_DefaultInforAndInstructions;
	/// 注册事件（当执行某个信息时，执行某个指令）
	TMap<FString,FInputInforAndInstruction> RegisterEvent;

	///当前控制模式
	ECONTROL_MODE CurControllerMode;
	///旧的控制模式
	ECONTROL_MODE OldControllerMode;

	///背景模式
	ECONTROL_MODE BackControllerMode;
	/// 多个功能用到该模式，但是中间有限差别需要区别出来，如射击模式的  使用射击连线技能、 使用射击技能等 如("TPS","HUOLINGFU|140094001|140095001|140096001|140097001")
	TArray<FString> OtherValue;
};
