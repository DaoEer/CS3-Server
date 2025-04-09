// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "Operation/OperationData.h"
#include "OperationModeMgr.generated.h"

DECLARE_STATS_GROUP(TEXT("UOperationModeMgr"), STATGROUP_UOperationModeMgr, STATCAT_Advanced);

/*
* 文件名称：OperationModeMgr.h
* 功能说明：操作模式管理类
* 文件作者：yanghan
* 目前维护：huting
* 创建时间：2018-01--8
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UOperationModeMgr : public UCS3Object
{
	GENERATED_BODY()
	
public:
	UOperationModeMgr() {};
	~UOperationModeMgr() {};
	virtual void BeginDestroy() override;
	static UOperationModeMgr* GetInstance();
public:
	/**
	*BlueprintCallable,初始化
	*
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable)
		void Init();

	//属性初始化
	void PropertyInit();

	/**
	*BlueprintCallable,分析执行输指令
	*
	*@param TArray<FString> InputInfor 输入指令数组
	*@param FKey InputKey 输入的Key值
	*@param float InputScale 输入的轴值
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable)
		void ExecuteOperation(TArray<FString> Instructions, FString InputKey, const float& InputScale, TArray<FString> OtherValue);
	/**
	*BlueprintCallable,改变模式
	*
	*@param EATTACT_STATE OperationMode 操作模式
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable)
		void ChangeMode(EATTACT_STATE OperationMode, bool bIsBackMode = false);

	/**
	*BlueprintCallable,恢复到正确模式
	*
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable)
		void RecoveryMode();

	/**
	*BlueprintCallable,是否处于该模式
	*
	*@return bool
	*/
	UFUNCTION(BlueprintCallable)
		bool IsHaveMode(EATTACT_STATE ControlMode) { return ControlMode == CurOperationMode; }
private:
	///获取默认表格数据
	void GetDefaultTable(TMap<FString, FString>& TableDatas);
	///创建默认的指令与操作模式字典
	void CreatDeflautInstrNameOperationMap(const TMap<FString, FString>& TableDatas);
	///通过模式获取模式的数据
	void GetModeDataByType(EATTACT_STATE Operation, FOperationModeTable& TableData);
	///更新差异数据
	void UpdataOperation(const TMap<FString, FString>& UpdataDatas);
	///替换数据
	void ReplaceInputInfor(const TMap<FString, FString>& UpdataDatas);
	///切换模式信息
	void SwitchModeInfor(EATTACT_STATE OperationMode);
	///获取优先级
	int32 GetModePriority(EATTACT_STATE OperationMode);
	///根据名字创建操作
	UBaseOperation* CreatOperationByName(FString Name);

public:
#pragma region	C++用操作共用属性
	//向前方向
	FVector ForwardVector;
	//向右方向
	FVector RightVector;
	//是否要保持方向
	bool bIsKeepDirection;
	//摄像机是否有被操作
	bool bIsCameraBeOperationed;
	//玩家是否能转向
	bool bIsCanTurn = true;
#pragma endregion

#pragma region	操作共用属性
	//是否自动移动
	UPROPERTY(BlueprintReadOnly)
	bool bIsAutoMove;
#pragma endregion
private:
	/// 指令与操作字典
	UPROPERTY()
	TMap<FString, FString> m_InstrucAndOperation;
	///默认指令与操作字典
	UPROPERTY()
	TMap<FString, FString> m_DeInstrucAndOperation;
	///所有操作字典
	UPROPERTY()
	TMap<FString, UBaseOperation*> m_AllOperation;


	///当前模式
	EATTACT_STATE CurOperationMode;
	///上一个模式
	EATTACT_STATE OldOperationMode;

	///背景操作模式
	EATTACT_STATE BackOperationMode;
};
