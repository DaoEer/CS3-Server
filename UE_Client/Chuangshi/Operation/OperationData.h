#pragma once

#include "CoreMinimal.h"
#include "BaseOperation.h"
#include "Fight/AtkState/AtkState.h"
#include "GameData/CsvTableRowBase.h"
#include "OperationData.generated.h"

/*
* 文件名称：OperationData.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：huting
* 创建时间：2018-01-09
*/

UENUM(BlueprintType)
enum class ECONTROL_MODE : uint8
{
	NoneMode                         = 0,//没由模式
	DefaultControlMode               = 1,//默认控制模式
	ActionControlMode                = 2,//动作控制模式
	VehicleControlMode               = 3,//载具控制模式
	YControlMode                     = 4,//默认控制模式下的Y模式，默认控制模式下按下鼠标右键的模式
	AltControlMode                   = 5,//动作模式下的按Alt的模式
	ShootMode                        = 6,//射击模式
	JinDanMode                       = 7,//金丹模式
	HeHuaMode						 = 8,//荷花模式
	FuShenMode						 = 9,//附身模式
	LeiZhen							 = 11,//雷阵模式
	FlyDekuvery						 = 12,// 轨道飞行模式
	GlidingMode						 = 13,///<滑翔模式
	ShenFengMiJing					 = 14,///<神风秘径
	Fall							 = 15,///<降落模式
	GoUp							 = 16,///<上升模式 
	BatteryMode						 = 17,///<操作火炮模式
	GhostEye						 = 19,///<鬼瞳之眼探查模式
	MoveVehicle						 = 20,///<可移动载具模式（多人载具）
	YcjmdSkyCarrier					 = 21,///<勇闯绝命岛大鸟空中飞行载具模式
	YcjmdParachute					 = 22,///<勇闯绝命岛空中跳伞模式
	TrainSoldierMode				 = 23 ///<练兵模式
};

///输入信息和指令数组
USTRUCT(BlueprintType)
struct CHUANGSHI_API FInputInforAndInstruction
{
	GENERATED_BODY()

	/// 输入信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "InputInfor")
		FString InputInfor;
	/// 指令数组
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Instructions")
		TArray<FString> Instructions;
};

///非激活状态输入信息和指令信息
USTRUCT(BlueprintType)
struct CHUANGSHI_API FActiveStatusInputInforAndInstruction
{
	GENERATED_BODY()
	
	/// 差异替换（如果是true则是对比默认模式将需要更改的更改，其他的则不会修改，
	/// false则只将配置的数据填入，没有配置的输入和指令将没有）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsReplace")
		bool bIsReplace = true;
	/// 切换激活与非激活状态是否清除数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsClearData")
		bool bIsClearData = true;
	/// 输入信息和指令数组
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "InputInforAndInstructions")
		TArray<FInputInforAndInstruction> InputInforAndInstructions;

	/// 进入该模式时要运行的指令
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "InstructionsIfSwitchMode")
		TArray<FString> InstructionsIfSwitchMode;

	/// 离开该模式时要运行的指令
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "InstructionsIfSwitchOffMode")
		TArray<FString> InstructionsIfSwitchOffMode;
};

/// 控制模式表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FControModeTable : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()

	/// 控制模式
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ControlMode")
	ECONTROL_MODE ControlMode;
	
	/// 激活状态输入信息和指令信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ActiveStatusInfos")
		FActiveStatusInputInforAndInstruction  ActiveStatusInputInforAndInstruction;
	/// 非激活状态输入信息和指令信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "UnActiveStatusInfos")
	FActiveStatusInputInforAndInstruction  UnActiveStatusInputInforAndInstruction;

	/// 注册事件（当执行某个信息时，执行某个操作）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RegisterEvent")
	TArray<FInputInforAndInstruction> RegisterEvent;

	/// 优先级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Priority")
	int32 Priority;

	/// 多个功能用到该模式，但是中间有限差别需要区别出来，如射击模式的  使用射击连线技能、 使用射击技能等 如("TPS","HUOLINGFU|140094001|140095001|140096001|140097001")
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "OtherValue")
		TArray<FString> OtherValue;
	/// 备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Remarks")
	FString Remarks;
};

///操作模式表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FOperationModeTable : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()

	/// 操作模式
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "OperationMode")
	EATTACT_STATE OperationMode;
	/// 差异替换（如果是true则是对比默认模式将需要更改的更改，其他的则不会修改，
	/// false则只将配置的数据填入，没有配置的将没有）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsReplace")
	bool bIsReplace = true;
	/// 指令与操作
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "InstructionAndOperations")
	TMap<FString, FString> InstructionAndOperations;

	/// 进入该模式时要运行的指令
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "InstructionsIfSwitchMode")
	TArray<FString> InstructionsIfSwitchMode;
	/// 离开该模式时要运行的指令
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "InstructionsIfSwitchOffMode")
	TArray<FString> InstructionsIfSwitchOffMode;
	
	/// 优先级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Priority")
		int32 Priority;

	/// 备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Remarks")
	FString Remarks;
};

/// 默认控制模式表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FDefaultControModeTable : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()

	/// 输入信息和指令数组
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "InputInforAndInstruction")
	FInputInforAndInstruction InputInforAndInstruction;

	/// 备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Remarks")
	FString Remarks;
};

/// 默认操作模式表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FDefaultOperationModeTable : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()

	/// 指令
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Instruction")
	FString Instruction;
	/// 操作
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Operation")
	FString Operation;

	/// 备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Remarks")
	FString Remarks;
};

/// 操作类表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FOperationClassTable : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()

	/// 操作名字与操作类
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "OperationClasses")
	TMap<FString, TSubclassOf<UBaseOperation>> OperationClasses;

	/// 备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Remarks")
	FString Remarks;
};

/// 控制模式优先级表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FControllerPriorityTable : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()

	/// 控制模式
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ControlMode")
		ECONTROL_MODE ControlMode;

	/// 优先级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Priority")
		int32 Priority;

	/// 备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Remarks")
		FString Remarks;
};