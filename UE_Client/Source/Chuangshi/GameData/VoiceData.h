#pragma once

#include "CsvTableRowBase.h"
#include "VoiceData.generated.h"

/**
* 文件名称：VoiceData.h
* 功能说明：语音数据配置表
* 文件作者：LiuShuang
* 目前维护：wuxiaoou
* 创建时间：2016-11-23
*/

/**
 *	#语音播放优先级
 */
UENUM(Blueprintable)
enum class EVOICE_TYPE : uint8
{
	///默认语音
	DEFAULT = 0,
	///对话语音
	TALK,
	///技能语音
	SKILL,
	///死亡语音
	DEAD,
	///场景语音
	SCENE,
	///任务语音
	QUEST
};

/**
 * #语音相关数据
 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FVOICE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	/** 服务器发送编号,首字母:A:AI, Q:任务 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Id = TEXT("Q00001");

	/** 阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ECAMP_TYPE Camp = ECAMP_TYPE::XIAN;*/
	
	/** 职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		EPROFESSION_TYPE Profession = EPROFESSION_TYPE::UNKNOWN;*/

	/** 优先级 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		EVOICE_TYPE Priority = EVOICE_TYPE::DEFAULT;

	/** 延时 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Delay = 0.f;

	/** 音频资源ID */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString AudioId = TEXT("S00001");

	/** 是否显示界面 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 IsShowUI = 1;

	/** 界面类型(0:任务,1:AI-大半身像,2:AI-小半身像-左,3:AI-小半身像-右) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 WindowType = 0;

	/** 界面头像路径 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> HeadCoinPath;

	/** 界面动态头像ID */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString DynamicHeadID;

	/** 内容 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Content = TEXT("你好");

	/** 说话对象名字 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SpeakName;

	/** 任务半身像界面，固定视角的偏移配置 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector2D PitchAndYaw;

	/** 任务半身像界面，固定视角的摄像机远近 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Length;

	/** 此声音是否给跳过 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsSkip = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool  bIsForcePlay = false;
public:
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) {
		bool IDResult = this->Id.TrimStartAndEnd().IsEmpty();
		bool AudioIdResult = this->AudioId.TrimStartAndEnd().IsEmpty();
		bool ContentResult = this->Content.TrimStartAndEnd().IsEmpty();
		bool HeadCoinPathResult = this->HeadCoinPath.IsNull() ? true : FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->HeadCoinPath.ToString());
		bool IsError = IDResult || AudioIdResult || ContentResult;
		if (IsError || !HeadCoinPathResult)
		{
			ResultInfo.Result = Error;
		}
		else {
			ResultInfo.Result = Ok;
		}
		if (IDResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("ID Format Is Empty, "));
		}
		if (AudioIdResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("AudioId Format Is Empty, "));
		}
		if (ContentResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("Content Format Is Empty, "));
		}
		if (!HeadCoinPathResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("%s Is Error!"), *this->HeadCoinPath.ToString());
		}
		if (IsError || !HeadCoinPathResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	}

	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FHEAD_MODEL_ACTION_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///玩家播放前景动画ActionID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ModelFrontActionID")
		FString ModelFrontActionID;

	///玩家播放背景动画ActionID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ModelBackActionID")
		FString ModelBackActionID;

	///玩家延迟播放动画时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ModelActionTime")
		float ModelActionTime;

};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FHEAD_BUST_MODEL_ACTION_DATA
{
	GENERATED_USTRUCT_BODY()
public:

	///半身像播放前景动画ActionID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "HeadModelFrontActionID")
		FString HeadModelFrontActionID;

	///半身像播放背景动画ActionID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "HeadModelBackActionID")
		FString HeadModelBackActionID;

	///半身像延迟播放动画时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "BustActionTime")
		float BustActionTime;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FHEAD_MODEL_EFFECT_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///播放的光效ID（@DT_EffectCfg）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "EffectID")
		FString EffectID;
	///播放延迟时间（秒）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "EffectTime")
		float EffectTime;
	///是否对玩家播放
	///	是，对玩家播放光效
	///	否，对目标单位播放光效
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool isPlayer;
};

/**
**动态半身像配置
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FHEAD_MODEL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///半身像配置ID（本配置表被引用时对应的配置ID）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString HeadID;
	///半身像模型ID（@DT_ModelCfg）
	///	半身像的模型、表现，与目标单位，完全无关
	///注意：
	///	半身像模型ID留空时，目标单位是，PC自身
	///	否则，目标单位是，离PC距离最近的指定ID的NPC
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ModelID;
	///目标单位播放指定动画表现
	///	目标单位（离PC最近的指定NPC单位，或PC自身）播放动画表现
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FHEAD_MODEL_ACTION_DATA> ModelActionData;
	///半身像播放指定动画表现
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FHEAD_BUST_MODEL_ACTION_DATA> HeadModelActionData;
	///目标单位或PC播放光效表现
	///	不支持半身像播放表现，这里都是指的单位本身播放光效
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FHEAD_MODEL_EFFECT_DATA> ModelEffectData;
	///目标单位的NPCID要求（@DT_NpcCfg）
	///	目标单位是NPC时，指定离PC距离最近的指定ID的NPC为目标单位
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "备注")
		FString Remarks;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		FString TempHeadID = this->HeadID.TrimStartAndEnd();
		if (TempHeadID.IsEmpty())
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("HeadID Is Empty!\n"));
		}
		else
		{
			ResultInfo.Result = Ok;
		}
		
	};

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

/**
**动态半身像配置
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FHEAD_MODEL_TRANSFORM_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///绑定的骨骼点/插槽名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SocketName = "None";
	///位置偏移（由工具导出，无需手配）
	///	用以描述半身像模型的表现
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTransform Transform;
	///摄像机FOV偏移（由工具导出，无需手配）
	///	用以描述半身像模型的表现
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float FOVAngle;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "备注")
		FString Remarks;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FVOICE_PLAY_DATA
{
	GENERATED_BODY()
public:
	///语音对话能否别中断
	FString IsCanInterrupt = "1";
	///语音ID列表
	TArray<FString> PlotList;
	///对话目标的EntityID
	int32 TalkingTargetId;
};