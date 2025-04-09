// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Object.h"
#include "GameDefault.generated.h"

/**
* 文件名称：.GameDefaulth
* 功能说明：
* 文件作者：luocheng
* 目前维护：wuxiaoou
* 创建时间：2016-10-14
*/

UCLASS(Config=Game)
class CHUANGSHI_API UGameDefault : public UObject
{
	GENERATED_BODY()public:

	UPROPERTY(Config)
	FString DefaultModelNumber_M;

	UPROPERTY(Config)
	FString DefaultModelNumber_N;
	
	UPROPERTY(Config)
	FString CsvConfigPath;

	///是否在切换关卡时重新创建玩家actor
	UPROPERTY(Config)
	bool bReCreatePlayerCharacter;
	
	///角色选择关卡index为0处起始角度，用弧度表示，-90度用PI*3/2表示
	UPROPERTY(Config)
		float StartAngle;
	///角色选择关卡角色所站位置距转盘中心半径, 单位是cm
	UPROPERTY(Config)
		float radius;
	///角色选择关卡可以摆放的角色的数量，目前是5个
	UPROPERTY(Config)
		int32 RoleNumLimit = 0;
	///随机动作的时间下限
	UPROPERTY(Config)
		int32 RandomActionTimeMin = 0;
	///随机动作的时间上限
	UPROPERTY(Config)
		int32 RandomActionTimeMax = 0;
	///是否开启边缘辅助跳跃
	UPROPERTY(Config)
		bool IsOpenLedgesJump;
	
	///是否开启统计日志
	UPROPERTY(Config)
		bool bAutoLogStatistics;

	///服务器的IP地址
	UPROPERTY(Config)
		FString ServerIPAddress;

	UPROPERTY(Config)
		FString ServerStateHostAndPort; //服务器状态数据端口地址

	UPROPERTY(Config, BlueprintReadOnly, DisplayName = "GameDefault|IsChangeServer")
		bool IsChangeServer;		///是否切换服务器

	UPROPERTY(Config)
		bool IsEnterGame;		///是否不选人直接进游戏

	UPROPERTY(Config)
		bool bOpenNotifyObject;	///开启监视UObject的创建和删除

	UPROPERTY(Config)
		bool bContinueHandleAT;	///是否在客户端返回到登录之后，再登录之后可以继续执行上次的AutoTest任务

	///是否启用屏蔽字系统
	UPROPERTY(Config)
		bool bIsUseShieldText;

	///引擎球体资源的路径
	UPROPERTY(Config)
		FString EngineSpherePath;

	UPROPERTY(Config, BlueprintReadOnly, DisplayName = "GameDefault|NPCTalkStartDistance")
		float NPCTalkStartDistance;			///玩家双击NPC或自动寻路和NPC对话进行交互距离

	UPROPERTY(Config, BlueprintReadOnly, DisplayName = "GameDefault|NPCTalkStopMoveDistance")
		float NPCTalkStopMoveDistance;		///玩家双击NPC或自动寻路和NPC对话停止移动距离

	UPROPERTY(Config, BlueprintReadOnly, DisplayName = "GameDefault|QrCodeServerHostAndPort")
		FString QrCodeServerHostAndPort;		///扫码端口地址

	UPROPERTY(Config, BlueprintReadWrite, DisplayName = "GameDefault|ServerName")
		FString ServerName;//区服务器名字

	/** 动画速率LOD, 以下是FAnimUpdateRateParameters::BaseVisibleDistanceFactorThesholds注释
	 * Array of MaxDistanceFactor to use for AnimUpdateRate when mesh is visible (rendered).
	 * MaxDistanceFactor is size on screen, as used by LODs
	 * Example:
	 *		BaseVisibleDistanceFactorThesholds.Add(0.4f)
	 *		BaseVisibleDistanceFactorThesholds.Add(0.2f)
	 * means:
	 *		0 frame skip, MaxDistanceFactor > 0.4f
	 *		1 frame skip, MaxDistanceFactor > 0.2f
	 *		2 frame skip, MaxDistanceFactor > 0.0f
	 */
	
	UPROPERTY(Config)
		TArray<float> AnimUpdateRateLOD;

	///是否开启动画速率LOD调试信息
	///	红色：跳过0帧，绿色：跳过1帧，蓝色：跳过2帧，黑色：跳过2帧以上
	UPROPERTY(Config)
		bool bDisplayDebugAnimUpdateRateLOD;

	///SignificanceType对应的重要度
	///SignificanceType::Complete对应下标0的值…
	UPROPERTY(Config)
		TArray<float> SignificanceLOD;

	///AGameCharacter::OnSignificanceChange()中不同重要度时的Tick间隔
	UPROPERTY(Config)
		TArray<float> SignificanceLOD_TickInterval_HeadInfo3DUI;

	///AGameCharacter::OnSignificanceChange()中不同重要度时的Tick间隔
	UPROPERTY(Config)
		TArray<float> SignificanceLOD_TickInterval_GameCharacter;

	///AGameCharacter::OnSignificanceChange()中不同重要度时的Tick间隔
	UPROPERTY(Config)
		TArray<float> SignificanceLOD_TickInterval_Actor;

	///本地屏幕输出打印
	UPROPERTY(Config)
		bool IsEnabledScreenPrint = false;

	///自定义游戏窗口分辨率
	UPROPERTY(Config)
		FString CustomWindowResolution;
};

