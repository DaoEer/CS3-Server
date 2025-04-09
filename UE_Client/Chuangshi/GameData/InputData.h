#pragma once

#include "CsvTableRowBase.h"
#include "InputData.generated.h"

/**
* 文件名称：InputData.h
* 功能说明：按键配置表
* 文件作者：LiuShuang
* 目前维护：wuxiaoou
* 创建时间：2016-03-03
*/

/**
 *	#输入类型
 */
UENUM(BlueprintType)
enum class EINPUT_TYPE : uint8
{
	IT_Key		= 0,	// 按键输入
	IT_Action	= 1,	// 动作输入
	IT_Axis		= 2,	// 轴输入
	IT_AxisKey	= 3,	// 轴键输入
};

/**
 *	#输入事件
 */
UENUM(BlueprintType)
enum class EINPUT_EVENT : uint8
{
	IE_Pressed		= 0,	// 按下
	IE_Released		= 1,	// 释放
	IE_Repeat		= 2,	// 重复
	IE_DoubleClick	= 3,	// 双击
	IE_Axis			= 4,	// 轴
	IE_MAX			= 5,	// 最大值
};

/**
 *	#组合按键相关
 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FGROUPKEY_DATA
{
	GENERATED_USTRUCT_BODY()

public:
	/*UPROPERTY()
		bool bIsFinish;*/
	
	/** 键链表 */
	UPROPERTY()
		FKey Key;
	/** Action Shift */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Shift;
	/** Action Ctrl */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Ctrl;
	/** Action Alt */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Alt;
	/** Action Cmd */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Cmd;
	/** Action DoubleClick */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool DoubleClick;
};

/**
*key对应的数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FInputKeyData
{
	GENERATED_USTRUCT_BODY()
public:
	/** 输入类型 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		EINPUT_TYPE Type;
	/** Axis Scale */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Scale;
	/** Action Shift */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Shift;
	/** Action Ctrl */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Ctrl;
	/** Action Alt */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Alt;
	/** Action Cmd */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Cmd;
	/** 输入事件 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		EINPUT_EVENT IE;
	/** 对应函数名 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName FuncName;
};

/**
*key的事件
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FInputKeyEvent
{
	GENERATED_USTRUCT_BODY()
public:
	/** 按键/轴键 Key/AxisKey */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FKey Key;
	/** 是否是主键 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool BIsMainKey = true;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FInputKeyData> KeyDatas;
};

USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FINPUT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	
	/** 动作/轴/组合键 Action("Jump")/Axis() */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName ActName;
	
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FInputKeyEvent> KeyEvents;
};


/**
*	快捷键是否存在在当前快捷键中，或已修改快捷键中
*/
UENUM(BlueprintType)
enum class ESHORTCUT_EXISTING_TYPE : uint8
{
	// 不存在
	SET_FALSE = 0,
	// 存在在原有快捷键中
	SET_TRUE_IN_OLDKEYS = 1,
	// 存在在修改的快捷键中
	SET_TRUE_IN_CHANGEDKEYS = 2,
	// 该快捷键是否与原有的快捷键一致
	SET_OLDKEYS = 3,
	// 该快捷键是否与修改后的快捷键一致
	SET_CHANGEDKEYS = 4,
};

