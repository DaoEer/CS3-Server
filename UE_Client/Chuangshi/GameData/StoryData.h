#pragma once


#include "CsvTableRowBase.h"
#include "LevelSequence.h"
#include "Animation/AnimInstance.h"
#include "GameData/Skill/SkillTableData.h"
#include "StoryData.generated.h"


/**
* 文件名称：StoryData.h
* 功能说明：
* 文件作者：LiuShuang
* 目前维护：huting
* 创建时间：2016-11-01
*/

/**
 *	#屏蔽相关数据
 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FHIDEENTITY_DATA
{
	GENERATED_USTRUCT_BODY()

	///依据单位类型屏蔽（如，0|1|2|4）
	///	0：隐藏其他玩家
	///	1：隐藏玩家自己
	///	2：隐藏其他玩家的宠物
	///	3：隐藏玩家自己的宠物
	///	4：隐藏周围战斗实体随机组合（如：0|1|2|4）
	///	5：隐藏纯客户端表现Actor（@CST-4360）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString HideType;
	/** 只隐藏ScriptId的Entity, 例ScriptId0|ScriptId1|ScriptId2, HideType不包含4才执行 */
	
	///隐藏以下ScriptID的Entity
	///	如，10000000|100000001|10000002
	///注意：
	///	只有HideType不包含4时，才生效
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	/** 显示ScriptId的Entity, 例ScriptId0|ScriptId1|ScriptId2 */
	
	///显示以下ScriptID的
	///	如，20000000|20000001|20000002
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	/** 显示ClassName的entity, 例NPC|Monster|DropBox */
	
	///只显示HideType4中的某些类型
	///	如，NPC|Monster|DropBox
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
	/** 显示纯客户端Actor的UID */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param4;
};

/**
 *	#摄像机数据
 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCAMERA_DATA
{
	GENERATED_USTRUCT_BODY()

	/** 剧情摄像机位置和旋转 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Time = 0.0f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Point = FVector::ZeroVector;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FRotator Rotator = FRotator::ZeroRotator;
};

/**
*	#摄像机数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCAMERA_SETTINGS_DATA
{
	GENERATED_USTRUCT_BODY()
	///是：CineCamera，否：GameCamera
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bCineCamera = 1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (EditCondition = "bCineCamera"))
		float ManualFocusDistance = 100000.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (EditCondition = "bCineCamera"))
		float CurrentFocalLength = 35.0f;

	/** Current aperture, in terms of f-stop (e.g. 2.8 for f/2.8) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (EditCondition = "bCineCamera"))
		float CurrentAperture = 22.0f;

	///位置和时间信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FCAMERA_DATA CameraPosInfo;
};

/**
*	#摄像机数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FENDCAMERA_SETTINGS_DATA
{
	GENERATED_USTRUCT_BODY()		

	/** 结束时摄像机类型;-1保持在镜头结束前摄像机的角度,0回到玩家背后视角 CST-1408*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 CameraType = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FCAMERA_SETTINGS_DATA CameraSettingInfo;
};

#pragma region	/** 镜头字幕相关 */
/**
*	镜头字幕水平停靠方式
*/
UENUM(Blueprintable)
enum class ETEXTHDOCKSTYLE : uint8
{
	///水平靠左（像素）
	LEFT = 0,
	///水平居中（像素）
	CENTER,
	///水平靠右（像素）
	RIGHT,
};

/**
*	镜头字幕垂直停靠方式
*/
UENUM(Blueprintable)
enum class ETEXTVDOCKSTYLE : uint8
{
	///垂直靠左（像素）
	TOP = 0,
	///垂直居中（像素）
	MIDDLE,
	///垂直靠右（像素）
	BOTTOM,
};

/**
*	镜头字幕数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORY_TEXT_DATA
{
	GENERATED_USTRUCT_BODY()
	///文字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Text;
	///是否竖排
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsVertical;
	///文字类型
	///	0：普通文本
	///	1：逐字显示
	///	2：淡入淡出
	///	3：滚动
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TextType = 0;
	///字幕效果时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float EffectTime;
	///字幕持续时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float KeepTime;
	///字幕水平锚点
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ETEXTHDOCKSTYLE HDockStyle = ETEXTHDOCKSTYLE::LEFT;
	///字幕垂直锚点
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ETEXTVDOCKSTYLE VDockStyle = ETEXTVDOCKSTYLE::TOP;
	///字幕位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector2D Position;
};

/**
*	镜头字幕四职业配置信息
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORY_PROFESSION_TEXT_Info
{
	GENERATED_USTRUCT_BODY()
	///字幕数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSTORY_TEXT_DATA> ProfessionTextData;
};

/**
*	镜头字幕配置信息
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORY_TEXT_Info
{
	GENERATED_USTRUCT_BODY()
	///字幕数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSTORY_PROFESSION_TEXT_Info> TextData;
};

#pragma endregion

/**
 *	#剧情数据
 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORY_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///剧情动画资源
	///	单个动画资源，代表“全部职业都播放同一个剧情动画”
	///	多个动画资源，代表”不同职业播放不同的剧情动画“（顺序：战士、剑客、链刃、法师）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<TSoftObjectPtr<ULevelSequence>> Assets;
	
	///地图MapScriptID（如”L_YXG“，@DT_HashMapCfg）
	///	进入该地图时，可预加载此行动画，以保障初次播放流畅
	///注意：
	///	打包版有效，开发版无效
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Space;
	
	///任务ID列表（|竖号分隔）
	///	进入上述地图时，若持有以下任务，则预加载此行动画
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString QuestID;
	
	///几秒后可跳过（秒，＜0代表“不可以跳过”）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Skip;
	
	///镜头过程AOI半径（缺省80米，有效范围(0,507]）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Aoi;
	
	/** 是否幻阵迷宫 开启传送门镜头CST-7240*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HZMG")
		bool IsHZMGOpenDoorStory = false;
	
	/** 幻阵迷宫 从某帧播放的数据 CST-7240*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HZMG")
		int32  PlayToFrameData = 0;
	
	/**是否是媒体视频 CST-7240*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsMedia = false;
	
	/** 是否进入世界时停止播放CST-7240*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HZMG")
		bool IsStopInWorldOver = false;
	
	/** 是否过图停止播放镜头CST-7240*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HZMG")
		bool IsStopLoadingLevel = true;
	
	///是否屏蔽UI
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool HideUI;
	
	///是否允许玩家控制摄像机
	///	如，操控摄像机、玩家移动……
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsControlledByPlayer = false;
	
	///是否强制下马（默认否）
	///注意：
	///	一般都应该选择“是，强制下马”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool DisRide = false;
	
	///剧情过程中，是否屏蔽游戏中的新建单位
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool HideNewEntity;
	
	///剧情开始时，屏蔽以下单位
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FHIDEENTITY_DATA HideEntity;
	
	///镜头中的半身像喊话列表（@VoiceConfig）
	///	按照在镜头定序器事件轨迹中PlayVoiceWords函数的关键帧顺序填入即可
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> VoiceWords;
	
	///剧情过程中，屏蔽游戏中的新建声音（|竖号分隔，如“0|1|2|3|4|5”）
	///	0：语音（即VoiceConfig中的语音，不会屏蔽镜头本身配置的语音）
	///	1：战斗音乐
	///	2：背景音乐
	///	3：纯客户端声音（阵营选择，角色创建等声音）
	///	4：3D声音（技能声音）
	///	5：环境音乐
	///	6：天气音乐
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> HideNewVoice;
	
	///剧情开始时，屏蔽游戏中的声音（|竖号分隔，如“0|1|2|3|4|5”）
	///	0：语音（即VoiceConfig中的语音，不会屏蔽镜头本身配置的语音）
	///	1：战斗音乐
	///	2：背景音乐
	///	3：纯客户端声音（阵营选择，角色创建等声音）
	///	4：3D声音（技能声音）
	///	5：环境音乐
	///	6：天气音乐
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> HideVoiceType;
	
	///镜头动画字幕功能相关，详见镜头使用文档
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSTORY_TEXT_Info>TextInfo;	
	
	/** 0代表GameCamera 1代表CineCamera */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCAMERA_SETTINGS_DATA> PreCameraSettings;
	
	///是否执行摄像机开始操作
	///	如：Entity屏蔽操作、下马、设置AOI
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool PreCameraOperation;
	
	///前过渡摄像机，是否屏蔽玩家鼠键操作
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool HideInputByPreCamera;
	
	///镜头结束后，镜头视角复位表现类型
	///	0：摄像机回到玩家身后
	///	1：摄像机维持镜头结束时的朝向
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FENDCAMERA_SETTINGS_DATA> EndCameraSettings;
	
	///四职业通用镜头配置，详见镜头使用文档
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> AnimName;
	
	///镜头持有效果列表（@DT_SkillHoldEffectCfg）
	///支持：
	///	播放镜头的过程中，为玩家单位注册持有效果（@CST-10895）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> EffectList;
	
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Description;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		CheckParamIntData(ResultInfo, QuestID, "QuestID", true, "|");
		CheckParamIntData(ResultInfo, HideEntity.HideType, "HideEntity.HideType", true, "|");

		for (int i = 0; i < HideNewVoice.Num(); i++)
		{
			FString Param = FString::Printf(TEXT("HideNewVoice index(%d)"), i);
			CheckParamIntData(ResultInfo, HideNewVoice[i], Param, true, "|");
		}
		for (int i = 0; i < HideVoiceType.Num(); i++)
		{
			FString Param = FString::Printf(TEXT("HideVoiceType index(%d)"), i);
			CheckParamIntData(ResultInfo, HideVoiceType[i], Param, true, "|");
		}
		for (int i = 0; i < AnimName.Num(); i++)
		{
			TArray<FString> AnimIndex = SplitString(AnimName[i], true);
			if (AnimIndex.Num() >= 2)
			{
				FString Param = FString::Printf(TEXT("AnimName index(%d)"), i);
				CheckParamFloatData(ResultInfo, AnimIndex[1], Param, false);
			}
			if (AnimIndex.Num() == 3)
			{
				FString Param = FString::Printf(TEXT("AnimName index(%d)"), i);
				CheckParamIntData(ResultInfo, AnimIndex[2], Param, false);
			}

		}
		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/**
*	#剧情事件数据类型
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORY_EVENT_TYPE
{
	GENERATED_USTRUCT_BODY()
		
	///剧情动画效果脚本
	///	详见alienbrain://NEWAB/创世3/策划配置/08_镜头/DT_StoryEventCfg.xlsx说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString script;
	///参数1，由剧情动画效果脚本定义
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString param1;
	///参数2，由剧情动画效果脚本定义
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString param2;
	///参数3，由剧情动画效果脚本定义
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString param3;
	///参数4，由剧情动画效果脚本定义
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString param4;
};

/**
*	#剧情事件数据类型
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORY_EVENT_LIST
{
	GENERATED_USTRUCT_BODY()

	///镜头事件编号
	///	对应镜头动画关键帧编号，镜头时间轴从左到右，依次按0,1,2……顺序触发
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Index = 0;

	///镜头效果列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSTORY_EVENT_TYPE> StoryEvents;
};


/**
*	#剧情事件数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORY_EVENT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///镜头事件列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSTORY_EVENT_LIST> StoryEventList;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		for (int i = 0; i < StoryEventList.Num(); i++)
		{
			auto EventData = StoryEventList[i];
			for (int j = 0; j < EventData.StoryEvents.Num(); j++)
			{
				auto Data = EventData.StoryEvents[j];
				if (Data.script == "SETeleportPlayerByClass" || Data.script == "SETeleportPlanesPlayerByClass"
					|| Data.script == "SERandomTeleportPlayer")
				{
					TArray<FString> Param2Split = SplitString(Data.param2);
					for (auto Split: Param2Split)
					{
						FString Param = FString::Printf(TEXT("StoryEventList index(%d), StoryEvents index(%d) Param2"), i, j);
						if (!CheckPosDirCheckData(ResultInfo, Split, Param))
						{
							break;
						}
					}
					TArray<FString> Param3Split = SplitString(Data.param3);
					for (auto Split : Param3Split)
					{
						FString Param = FString::Printf(TEXT("StoryEventList index(%d), StoryEvents index(%d) Param3"), i, j);
						if (!CheckPosDirCheckData(ResultInfo, Split, Param))
						{
							break;
						}
					}
				}
				else if (Data.script == "SETeleportPlayer" || Data.script == "SERingTaskTeleportPlayer"
					|| Data.script == "SETeleportPlanesPlayer")
				{
					FString Param2 = FString::Printf(TEXT("StoryEventList index(%d), StoryEvents index(%d) Param2"), i, j);
					FString Param3 = FString::Printf(TEXT("StoryEventList index(%d), StoryEvents index(%d) Param3"), i, j);
					CheckPosDirCheckData(ResultInfo, Data.param2, Param2);
					CheckPosDirCheckData(ResultInfo, Data.param3, Param3);
				}
				else if (Data.script == "SESendAICommand")
				{
					FString Param = FString::Printf(TEXT("StoryEventList index(%d), StoryEvents index(%d) Param1"), i, j);
					CheckParamIntData(ResultInfo, Data.param1, Param, false);
				}
				else if (Data.script == "SEPlayerGetItem")
				{
					TArray<FString> Param1Split = SplitString(Data.param1);
					for (auto Split : Param1Split)
					{
						FString Param = FString::Printf(TEXT("StoryEventList index(%d), StoryEvents index(%d) Param1"), i, j);
						CheckParamIntData(ResultInfo, Data.param1, Param, true, ":");
					}
				}
			}

		}

		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/**
*	#剧情动画事件数据类型
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORY_ANIM_EVENT : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///各职业动画资源列表（顺序：战士、剑客、链刃、法师）
	///支持：
	///	镜头编辑器分职业功能拓展（@CST-2634）
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		TArray<TSoftObjectPtr<UAnimationAsset>> AnimPath;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		for (int i = 0; i < AnimPath.Num(); i++)
		{
			auto Anim = AnimPath[i];
			if (Anim.ToSoftObjectPath().IsValid())
			{
				if (!CheckResourceFileIsExist(Anim.ToString()))
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog += FString::Printf(TEXT("; \"AnimPath\" index(%d) resource does not exist"), i);
				}
			}
		}


		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

UENUM(BlueprintType)
enum class CSTORY_EVENT_PARAM_TYPE_ENUM : uint8
{
	CNONE = 0						UMETA(DisplayName = "CNONE"),
	CNOTIFY_SERVER = 1				UMETA(DisplayName = "CNOTIFY_SERVER"),
	CPLAY_VOICE = 2					UMETA(DisplayName = "CPLAY_VOICE"),
	CPLAY_REDRAW_VIEWPORTS = 3		UMETA(DisplayName = "CPLAY_REDRAW_VIEWPORTS"),
	CPLAY_ANIM = 4					UMETA(DisplayName = "CPLAY_ANIM"),
	CSTOP_ANIM = 5					UMETA(DisplayName = "CSTOP_ANIM"),
};


/**
*	#剧情事件数据类型
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORY_CHARACTER_ANIM
{
	GENERATED_USTRUCT_BODY()

	/** 动作 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UAnimSequenceBase* AnimSequenceBase;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bDefaultEnableRootMotion;
};

UENUM(BlueprintType)
enum class CSTORY_VOICE_TYPE : uint8
{
	///语音
	VOICE = 0,
	///战斗音乐
	FIGHTNUSIC = 1,
	///背景音乐
	BGMUSIC = 2,
	///纯客户端声音
	CLIENTVOICE = 3,
	///3D声音
	SOUND3D = 4,
	///环境音乐
	ENVIRONMENT = 5,
	///天气音乐
	WEATHER = 6,
};

/**
*	#剧情动画蓝图数据（主要用于动作融合播放）
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORY_MODEL_ANIMATION_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///模型动画路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftClassPtr<UAnimInstance> AnimationPath;
};