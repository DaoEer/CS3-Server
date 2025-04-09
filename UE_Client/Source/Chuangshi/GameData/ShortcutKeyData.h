#pragma once

#include "InputData.h"
#include "ShortcutKeyData.generated.h"

/**
* 文件名称：ShortcutKeyData.h
* 功能说明：按键配置表
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-03-06
*/

/**
 *	#角色控制状态
 */
UENUM(BlueprintType)
enum class EROLE_CTRL_STATE : uint8
{
	// 普通状态
	RCS_COMMON = 0,
	// 飞行控制状态
	RCS_FLY = 1,
	// 变身控制状态
	RCS_CHANGE_BODY = 2,
	// 剧情控制状态
	RCS_STORY = 3,
	// 仙魔录触发控制状态
	RCS_MEMOIR = 4,
	// 心魔附身触发控制状态
	RCS_XINMO = 5,
	// 野外竞速状态
	RCS_JING_SU = 6,
	// 钓鱼状态
	RCS_FISH = 7,
	// 混乱状态
	RCS_CONFUSION = 8,
	// 滑翔状态
	RCS_GLIDING = 9,
	// 举盾状态
	RCS_SHIELD = 10,
	// 轨道飞行状态
	RCS_FLY_ORBIT = 11,
	// 火灵符射击状态
	RCS_HUOLINGFU = 12,
	// 荷花状态
	RCS_HEHUA = 13,
	// 雷阵状态
	RCS_LEIZHEN = 14,
	// 镇海弓状态
	RCS_ZHENHAIGONG = 15,
	// 摆摊状态
	RCS_STALL = 16,
	// 十方城状态
	RCS_SHIFANGCHENG = 17,
	// 对话状态
	RCS_TALK = 18,
	// 操作火炮状态
	RCS_BATTERY = 19,
	// 鬼瞳之眼探查状态
	RCS_GHOSTEYE = 20,
	//勇闯绝命岛射击模式状态
	RCS_YCJMD = 21,
	//推箱子副本向下俯视状态
	RCS_OBERLOOK = 22,
};

/**
*	#角色控制状态的按键控制
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSHORTCUTKEYCTRL
{
	GENERATED_USTRUCT_BODY()

	/** 按键激活相关 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "NotActiveAnyKey")
		bool bNotActiveAnyKey;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FKey> OnlyActiveKeys;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FKey> NotActiveKeys;

	/** Action激活相关 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "NotActiveAnyActions")
		bool bNotActiveAnyActions = false;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FName> OnlyActiveActions;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FName> NotActiveActions;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FName> NotActiveAxis;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FKey> NotActiveAxisKey;
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FSHORTCUTKEY_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	/** 角色控制状态 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		EROLE_CTRL_STATE CtrlState;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSHORTCUTKEYCTRL>  ShortcutKeyCtrl;
};
