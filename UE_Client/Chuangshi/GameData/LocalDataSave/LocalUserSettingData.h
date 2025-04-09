// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/ShortcutKey.h"
#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "LocalUserSettingData.generated.h"

/**
* 文件名称：LocalUserSettingData.h
* 功能说明：系统设置数据
* 文件作者：zhangdan
* 目前维护：huting
* 创建时间：2018-04-18
*/

/**
 *	文件:			UserSettingData.h
*	描述:			系统设置数据
*	配置:
*	作者:			张丹
*	日期:			2018-04-18
*	更改:			舒清平
 */

DECLARE_MULTICAST_DELEGATE_OneParam(FVideoSettingChange, FVIDEOSETTING_DATA&);

 ///@struct FVIDEOSETTING_DATA 视频设置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FVIDEOSETTING_DATA
{
	GENERATED_USTRUCT_BODY()
	///画质
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		int32 ScreenPercentage = 0;
	///游戏分辨率
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		FString Resolution;
	///全屏模式
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsFullScreenMode;
	///垂直同步
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsVerticalSynchronization;
	///人物同模
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsCharacterMode;
	///镜头最大距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float CameraMaxLen;
	///广角
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float WideAngle;
	///UI缩放
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float UIScale;
	///摄像机转向速度（鼠标灵敏度）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float CameraTurnSpeed;
	///镜头最大臂长距离（镜头距离）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float CameraMaxArmLen;
};


///@struct 画质对应的渲染数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSCREENPERCENTAGES_RENDER_DATA
{
	GENERATED_USTRUCT_BODY()

	///后处理抗锯齿
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcessAAQuality")
		int32 PostProcessAAQuality = 6;

	///可视距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ViewDistance")
		int32 SkeletalMeshLODBias = 0;
	///可视距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ViewDistance")
		float ViewDistanceScale = 10.0f;

	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		int32 LightFunctionQuality = 1;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		int32 ShadowQuality = 5;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		int32 Shadow_CSM_MaxCascades = 10;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		int32 Shadow_MaxResolution = 4096;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		int32 Shadow_MaxCSMResolution = 4096;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		float Shadow_RadiusThreshold = 0.0f;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		float Shadow_DistanceScale = 1.0f;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		float Shadow_CSM_TransitionScale = 1.0f;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		float Shadow_PreShadowResolutionFactor = 1.0f;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		int32 DistanceFieldShadowing = 1;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		int32 DistanceFieldAO = 1;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow|VolumetricFog")
		int32 VolumetricFog = 1;///<1开启才需要设置以下3个参数
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow|VolumetricFog")
		int32 VolumetricFog_GridPixelSize = 4;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow|VolumetricFog")
		int32 VolumetricFog_GridSizeZ =128;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow|VolumetricFog")
		int32 VolumetricFog_HistoryMissSupersampleCount = 16;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Shadow")
		int32 LightMaxDrawDistanceScale = 1;

	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 MotionBlurQuality = 4;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		float AmbientOcclusionMipLevelFactor = 0.4f;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 AmbientOcclusionMaxQuality = 100;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 AmbientOcclusionLevels = -1;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		float AmbientOcclusionRadiusScale = 1.0f;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 DepthOfFieldQuality = 4;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 RenderTargetPoolMin = 1000;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 LensFlareQuality = 3;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 SceneColorFringeQuality = 1;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 EyeAdaptationQuality = 2;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 BloomQuality = 5;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 FastBlurThreshold = 100;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 Upscale_Quality = 3;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 Tonemapper_GrainQuantization = 1;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 LightShaftQuality = 1;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		float Filter_SizeScale = 1.0f;
	///后处理质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PostProcess")
		int32 Tonemapper_Quality = 5;

	///贴图质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Textures")
		float Streaming_MipBias = 0.0f;
	///贴图质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Textures")
		int32 MaxAnisotropy = 8;
	///贴图质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Textures")
		int32 Streaming_LimitPoolSizeToVRAM = 0;
	///贴图质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Textures")
		int32 Streaming_PoolSize = 3000;
	///贴图质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Textures")
		int32 Streaming_MaxEffectiveScreenSize = 0;

	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 TranslucencyLightingVolumeDim = 64;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 RefractionQuality =2 ;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 SSR_Quality =4;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 SceneColorFormat = 4;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 DetailMode = 2;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 TranslucencyVolumeBlur = 1;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 MaterialQualityLevel = 1;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		float SSS_Scale = 1;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 SSS_SampleSet = 2;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 SSS_Quality = 1;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 SSS_HalfRes = 0;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		float EmitterSpawnRateScale = 1.0;
	///特效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Effect")
		int32 ParticleLightQuality = 2;

	///植物质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Grass")
		float Foliage_DensityScale = 1.0f;
	///植物质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Grass")
		float Grass_DensityScale = 1.0f;

	///Panini投影
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Upscale")
		float Upscale_PaniniD = 0.1f;
};

///@struct 视频设置 配置多个数据（如最大最小）
USTRUCT(BlueprintType)
struct CHUANGSHI_API FVIDEOSETTING_RANGEVALUE_DATA
{
	GENERATED_USTRUCT_BODY()

	///游戏分辨率
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		TArray<FString> Resolution = {"1280x720","1600x900","1920x1080"};

	///游戏分辨率对应最大游戏臂长
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		TArray<float> CameraArmLenMax = { 2500.0f };
	///游戏分辨率对应最小游戏臂长
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		TArray<float> CameraArmLenMin = { -100.0f };
	///画质
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		TArray<int> ScreenPercentages = { 50,70,85,100 };

	///画质渲染设置数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		TArray<FSCREENPERCENTAGES_RENDER_DATA> ScreenPercentagesRender;

	///镜头最大距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float CameraLenMax = -100.0f;
	///镜头最小距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float CameraLenMin = -300.0f;
	///摄像机最大转向速度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float CameraTurnSpeedMax = 1.5f;
	///摄像机最大转向速度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float CameraTurnSpeedMin = 0.5f;
	///最大广角
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float WideAngleMax = 90.0f;
	///最小广角
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float WideAngleMin = 60.0f;
};

///@struct 抗锯齿强度设置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FANTI_ALIASING_DATA
{
	GENERATED_USTRUCT_BODY()
	///抗锯齿
	///	0：无抗锯齿
	///	1：FXAA
	///	2：Temporal
	///	3：MSAA
	///注意：除了以上数值填写其他的数值没有效果
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Anti-Aliasing")
		int32 AntiAliasingMethod = 0;
	
};


///@struct FCUSTOMSETTING_DATA 自定义设置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCUSTOMSETTING_DATA: public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///抗锯齿
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		int32 AntiAliasingQuality = 0;
	///同屏人数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		int32 ScreenRoleNum = 0;
	///同屏特效数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		int32 ScreenEffectNum = 0;
	///天气效果
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsWeatherEffect;
	///屏蔽雨雪
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShieldRainAndSnow;
	///地表细节
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsGroundSurfaceDetail;
	///草地动画
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsGrassAnimation;
	///透明混合渲染
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsTransparentBlendRendering;
	///植被交互
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsVegetationInteraction;
	///全屏泛光
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsFullScreenFloodlight;
	///地表泛光
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsSurfaceFloodlight;
	///云层阴影
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsCloudShadow;
	///实时阴影
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsRealtimeShadow;
	///雾化效果
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsAtomizationEffect;
	///水面精度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		int32 WaterSurfaceAccuracy = 0;
	///远景显示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		int32 LongRangeDisplay = 0;
	///植被精度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		int32 VegetationAccuracy = 0;
	///材质过滤
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		int32 TextureFiltering = 0;
	///阴影质量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		int32 ShadowQuality = 0;
	///地表精度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		int32 GroundSurfaceAccuracy = 0;
};

///@struct FSOUNDSETTING_DATA 音效设置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSOUNDSETTING_DATA
{
	GENERATED_USTRUCT_BODY()

	///主音量是否静音
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsMainVolumeOff;
	///主音量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float MainVolume;
	///背景音量是否静音
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsBGMVolumeOff;
	///背景音量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float BGMVolume;
	///音效音量是否静音
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsEffectVolumeOff;
	///音效音量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float EffectVolume;
	///语音音量是否静音
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsVoiceVolumeOff;
	///语音音量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		float VoiceVolume;
};

///@struct FBASESETTING_DATA 基础设置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBASESETTING_DATA
{
	GENERATED_USTRUCT_BODY()

	///掉落提示光效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsDropTipsEffect;
	///屏蔽系统提示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShieldSystemTips;
	///关闭进入剧情模式
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsCloseEnterStoryMode;
	///队友
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowTeammate;
	///NPC
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowNPC;
	///怪物
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowMonster;
	///开启新手帮助
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsOpenHelp;
	///自动显示上线提醒
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowOnlineRemind;
	///自动全部拾取
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsAutoPickUpAll;
	///自动追踪任务
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsAutoTrackingQuest;
	///鼠标位置打开拾取窗口
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsMousePickUp;
	///开启新装备获得提示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsOpenGetEquipTips;
	///自动显示符咒
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsAutoShowSpell;
};

///@struct FUISHOWSETTING_DATA 界面选项设置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FUISHOWSETTING_DATA
{
	GENERATED_USTRUCT_BODY()

	///显示其他玩家名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowOtherPlayerName;
	///显示其他玩家头衔
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowOtherPlayerTitle;
	///显示NPC名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowNPCName;
	///显示NPC头衔
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowNPCTitle;
	///显示自己名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowSelfName;
	///显示自己头衔
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowSelfTitle;
	///显示幻兽名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowMagicPetName;
	///显示其他玩家血条
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowOtherPlayerBloodBar;
	///显示NPC血条
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowNPCBloodBar;
	///显示自己血条
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowSelfBloodBar;
	///显示幻兽血条
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowMagicPetBloodBar;
	///显示他人的帮会名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowOtherPlayerGangName;
	///显示自己的帮会名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowSelfGangName;
	///显示玩家对话泡泡
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowPlayerTalkBox;
	///显示NPC对话泡泡
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowNPCTalkBox;
	///显示目标的目标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowTargetTarget;
	///显示队友任务情况
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowProgressOfTeammateQuest;
};

///@struct FQUICKBAESETTING_DATA 快捷栏设置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FQUICKBAESETTING_DATA
{
	GENERATED_USTRUCT_BODY()

	///轨迹提示释放
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsSkillTrack;
	///快速智能释放
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsSkillSmart;
	///显示侧边快捷栏1
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowSideBar1;
	///显示侧边快捷栏2
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowSideBar2;
	///显示侧边快捷栏3
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowSideBar3;
	///显示侧边快捷栏4
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowSideBar4;
	///显示侧边快捷栏5
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowSideBar5;
	///显示拓展快捷栏1
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowExpandBar1;
	///显示拓展快捷栏2
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowExpandBar2;
	///显示拓展快捷栏3
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowExpandBar3;
	///显示拓展快捷栏4
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowExpandBar4;
	///显示拓展快捷栏5
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowExpandBar5;
	///显示拓展快捷栏6
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowExpandBar6;
};

///@struct FCOMBATSETTING_DATA 战斗信息设置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCOMBATSETTING_DATA
{
	GENERATED_USTRUCT_BODY()

	///创世推荐模式（可通过拖拽鼠标调整镜头方向）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsRecommendMode;
	///ACT动作模式（鼠标移动可直接控制角色和镜头方向）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsACTMode;
	///自动反击
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsAutoFightBack;
	///我对目标造成的效果（包括幻兽）,技能名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowPlayerSkillName;
	///我对目标造成的效果（包括幻兽）,状态信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowTargetStateInfo;
	///我对目标造成的效果（包括幻兽）,命中与伤害
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowTargetDamage;
	///目标对我造成的效果,技能名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowTargetSkillName;
	///目标对我造成的效果,状态信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowPlayerStateInfo;
	///目标对我造成的效果,命中与伤害
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UserSettingData")
		bool IsShowPlayerDamage;
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FSYSTEM_DEFAULT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///视频设置 配置多个数据（如最大最小）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Video")
		FVIDEOSETTING_RANGEVALUE_DATA RangeValueVideoData;
	///视频设置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Video")
		FVIDEOSETTING_DATA VideoData;
	///音效设置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Sound")
		FSOUNDSETTING_DATA SoundData;
	///基础设置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Base")
		FBASESETTING_DATA BaseData;
	///界面选项设置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UIShow")
		FUISHOWSETTING_DATA UIShowData;
	///快捷栏设置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuickBase")
		FQUICKBAESETTING_DATA QuickBaseData;
	///战斗信息设置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat")
		FCOMBATSETTING_DATA CombatData;
	///（自定义）抗锯齿设置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Custom")
		FANTI_ALIASING_DATA AntiAliasingMethod;
};

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API ULocalUserSettingData : public USaveGame
{
	GENERATED_BODY()
public:
	ULocalUserSettingData() :FileName(TEXT("_LocalUserSettingData")) {}
	virtual void BeginDestroy() override;
public:

	///初始化数据
	UFUNCTION(BlueprintCallable, Category = "Manager|LocalUserSettingDataManager")
		void InitLocalUserSettingData();

	/**
	*获取系统默认数据
	*
	*@return 无
	*/
	const FSYSTEM_DEFAULT_DATA* GetDefaultSystemData();

	/**
	*获取当前画质配置表中对应的臂长的范围
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Manager|LocalUserSettingDataManager")
	void GetCameraArmLenDataByCfg(float& CameraArmLenMax, float& CameraArmLenMin);
	/**
	*获取当前对应的臂长
	*
	*@return 无
	*/
	void GetCameraArmLenData(float& CameraArmLenMax, float& CameraArmLenMin);

	///设置玩家摄像机插槽偏移
	UFUNCTION(BlueprintCallable, Category = "Manager|LocalUserSettingDataManager")
		void SetPlayerCameraSocketOffset();
	/**
	*获取视频设置数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		FVIDEOSETTING_RANGEVALUE_DATA GetRangeValueVideoData();
	/**
	*默认视频设置数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void DefaultVideoDataToFile();

	/**
	*默认自定义设置数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void DefaultCustomDataToFile();

	/**
	*默认音频设置数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void DefaultSoundDataToFile();

	/**
	*默认基础设置数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void DefaultBaseDataToFile();

	/**
	*默认界面选项设置数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void DefaultUIShowDataToFile();

	/**
	*n默认快捷栏设置数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void DefaultQuickBarDataToFile();

	/**
	*默认战斗信息设置数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void DefaultCombatDataToFile();

	/**
	*默认所有快捷键设置数据，数据文件创建时初始化时调用
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void DefaultAllShortcutKeyDataToFile();

	/**
	*默认快捷键设置数据
	*
	*@param KeyType 快捷键类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void DefaultShortcutKeyDataToFile(SHORTCUTKEY_TYPE_ENUM KeyType);

	/**
	*保存本地视频设置数据
	*
	*@param VideoSettingData 视频设置结构体
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void SaveVideoDataToFile(FVIDEOSETTING_DATA data);

	/**
	*保存视频设置数据到Config/Windows/launcherRecord.ini
	*
	*@param VideoSettingData 视频设置结构体
	*
	*@return 无
	*/
	void SaveVideoDataToLauncherRecordIniFile(FVIDEOSETTING_DATA data);

	/**
	*保存本地自定义设置数据
	*
	*@param FCUSTOMSETTING_DATA 自定义设置结构体
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void SaveCustomDataToFile(FCUSTOMSETTING_DATA data);

	/**
	*保存本地音频设置数据
	*
	*@param SoundSettingData 音效设置结构体
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void SaveSoundDataToFile(FSOUNDSETTING_DATA data);

	/**
	*保存音频设置数据到Config/Windows/launcherRecord.ini
	*
	*@param SoundSettingData 音效设置结构体
	*
	*@return 无
	*/
	void SaveSoundDataToLauncherRecordIniFile(FSOUNDSETTING_DATA data);

	/**
	*保存本地基础设置数据
	*
	*@param BaseSettingData 基本设置结构体
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void SaveBaseDataToFile(FBASESETTING_DATA data);

	/**
	*保存本地界面选项设置数据
	*
	*@param UIShowSettingData 界面选项设置结构体
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void SaveUIShowDataToFile(FUISHOWSETTING_DATA data);

	/**
	*保存本地快捷栏设置数据
	*
	*@param QuickBarSettingData 快捷栏设置结构体
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void SaveQuickBarDataToFile(FQUICKBAESETTING_DATA data);

	/**
	*保存本地战斗信息设置数据
	*
	*@param CombatSettingData 战斗信息设置结构体
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void SaveCombatDataToFile(FCOMBATSETTING_DATA data);

	/**
	*应用Config/DefaultGame.ini中配置的自定义游戏窗口分辨率
	*
	*@return 无
	*/
	void ApplyCustomWindowResolution();

	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void ApplySystemSettingData();

	/**
	*BlueprintCallable视频设置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UserSettingData")
		void ApplySettingVideoSettingData();

	/**
	*BlueprintCallable自定义设置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void ApplySettingCustomData();

	/**
	*BlueprintCallable音效设置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UserSettingData")
		void ApplySoundSettingData();

	/**
	*BlueprintCallable基础设置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UserSettingData")
		void ApplyBaseSettingData();

	/**
	*BlueprintCallable界面选项设置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UserSettingData")
		void ApplyUIShowSettingData();

	/**
	*BlueprintCallable快捷栏设置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UserSettingData")
		void ApplyQuickBarSettingData();

	/**
	*BlueprintCallable战斗信息设置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "UserSettingData")
		void ApplyCombatSettingData();

	float GetMainVolume();
	float GetBgVol();
	float GetVoiceVol();
	float GetEffVol();

	void IsValidVideoData();//视频设置数据的有效性检测

	bool GetIsShowOnlineRemind() {	return BaseSettingData.IsShowOnlineRemind;	}
public:
	UFUNCTION(BlueprintCallable, Category = "LocalDataManager|ULocalData")
		const FString& GetFileName();

	void SaveVideoSettingDataToConfig();//保存分辨率窗口模式到Config中

	void SetVideoSetting(float CameraTurnSpeed,float CameraMaxArmLen,float WideAngle);
private:
	void ApplyScreenPercentagesRender();///<不同分辨率下渲染相关设置
	void DelayExecuteCmds();///<周期执行渲染指令
	void ClearTimerHandle();///<清除定时器
private:
	FString FileName;
	FTimerHandle DelayHandle;
	TArray<FString> RenderCmds;///<渲染命令
public:
	///视频设置
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		FVIDEOSETTING_DATA VideoSettingData;

	///自定义设置
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		FCUSTOMSETTING_DATA CustomSettingData;

	///音效设置
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		FSOUNDSETTING_DATA SoundSettingData;

	///基础设置
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		FBASESETTING_DATA BaseSettingData;

	///界面选项设置
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		FUISHOWSETTING_DATA UIShowSettingData;

	///快捷栏设置
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		FQUICKBAESETTING_DATA QuickBarSettingData;

	///战斗信息设置
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		FCOMBATSETTING_DATA CombatSettingData;

	///视频设置改变事件广播
	FVideoSettingChange OnVideoSettingChange;

	///是否已经应用过修改分辨率
	bool bApplyResolutionChanged = false;
	
};
