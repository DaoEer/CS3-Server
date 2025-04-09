// Fill out your copyright notice in the Description page of Project Settings.

#pragma once


#include "FileManager.h"
#include "Map.h"
#include "UObject/Object.h"
#include "UnrealString.h"
#include "Util/CS3Debug.h"
#include "CS3ConsoleMgr.generated.h"

/*
* 文件名称：CS3ConsoleMgr.h
* 功能说明：
* 文件作者：wuxiaoou
* 目前维护：zhangyuxing
* 创建时间：2018-04-28
*/

UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class CHUANGSHI_API UCS3ConsoleMgr : public UObject
{
	GENERATED_BODY()

public:
	// Sets default values for this component's properties
	UCS3ConsoleMgr();

	//对当前场景性能信息进行自动化采样
	UFUNCTION(Exec)
		void CS3_SampleLevel(bool isConfig = false, float xDelta = 4000, float yDelta = 4000, float sampleTime = 0.5);

	/*基础调试*/
//------------------GameState-------------------

//当前游戏状态
	UFUNCTION(Exec)
		void CS3_CurrGameState();

	/**
	*开启和关闭屏幕输出日志
	*	@param	isToggled:	如果为True，则使用开启/关闭模式；否则依据isEnabled开启或关闭输出
	*/
	UFUNCTION(Exec)
		static void CS3_SetScreenPrintLog(bool isToggled = true, bool isEnabled = true);

	//------------------Level-------------------

	//当前关卡
	UFUNCTION(Exec)
		void CS3_CurrLevel();

	//------------------Entity-------------------

	//Entity数量显示
	UFUNCTION(Exec)
		void CS3_EntityNumber();

	//范围内的Entity显示
	UFUNCTION(Exec)
		void CS3_EntityInRange(float Range);

	//entity 位置
	UFUNCTION(Exec)
		void CS3_Pos(int32 EntityID);

	//------------------Actor-------------------	

	//GameActor数量显示 _____________________________***
	UFUNCTION(Exec)
		void CS3_GameActorNumber();

	//查询Actor的可见性参数entityID
	UFUNCTION(Exec)
		void CS3_QueryActorVS(int32 entityid);

	//------------------Player-------------------	

	//Player数量
	UFUNCTION(Exec)
		void CS3_PlayerNumber();

	//飞行
	UFUNCTION(Exec)
		void CS3_SwitchFly();

	///开启/关闭钓鱼
	UFUNCTION(Exec)
		void CS3_SwitchFish();

	//------------------Monster-------------------	

	//Monster数量
	UFUNCTION(Exec)
		void CS3_MonsterNumber();


	//------------------NPC-------------------	

	//NPC数量
	UFUNCTION(Exec)
		void CS3_NPCNumber();

	//------------------Monster-------------------	

					/*基础功能调试*/
	//------------------网络-------------------	

	UFUNCTION(Exec)
		void CS3_TestCallCell(const int32&  entityID, const FString &methodname, const FString& argument);

	UFUNCTION(Exec)
		void CS3_TestCallClient(const int32& entityID, const FString& methodname, const FString& argument);

	UFUNCTION(Exec)
		void CS3_TestCallBase(const int32&  entityID, const FString &methodname, const FString& argument);

	//------------------日志-------------------	


	//------------------网格-------------------	

	//加载所有网格
	UFUNCTION(Exec)
		void CS3_TestAsyncLoadAllMesh(const FString& Args);

	//------------------粒子-------------------	

	//加载所有粒子
	UFUNCTION(Exec)
		void CS3_TestLoadParticles();

	UFUNCTION(Exec)
		void CS3_PlayParticles(FString EffectId);

	//------------------登录-------------------	

	//更改服务器IP
	UFUNCTION(Exec)
		void CS3_ChangeServerIP(const FString& ServerIP);

	//更改登录方式	参数0，直接登录，1选择角色登录
	UFUNCTION(Exec)
		void CS3_ChangeLoginMode(int32 Type);

	//------------------声音-------------------	

	//播放声音，需要输入声音路径
	UFUNCTION(Exec)
		void CS3_PlaySound(const FString& AudioPath);

	//结束刚才播放的语音
	UFUNCTION(Exec)
		void CS3_StopSound();

	//切换打开关闭音效系统
	UFUNCTION(Exec)
		void CS3_TogglePlayAudioSystem();

	//------------------剧情-------------------	

	//播放剧情，需要剧情ID 	/** 客户端播放剧情资源 */
	UFUNCTION(Exec)
		void CS3_PlayStory(const FString& SequenceId);

	//结束刚才播放的剧情
	UFUNCTION(Exec)
		void CS3_StopStory();

	//------------------媒体视频-------------------	

	//播放媒体视频，需要媒体视频ID 
	UFUNCTION(Exec)
		void CS3_PlayMedia(const FString& MediaId);

	//结束刚才播放的媒体视频
	UFUNCTION(Exec)
		void CS3_StopMedia();

	//------------------界面-------------------	

	//查询所有可视窗口
	UFUNCTION(Exec)
		void CS3_QueryVSWnd();

	//			  /*游戏功能调试*/
	////------------------队伍-------------------	

	////------------------技能-------------------	
	//是否显示释放技能名称提示
	UFUNCTION(Exec)
		void CS3_SetIsPromptSkillName(bool IsPromptSkillName);

	////------------------物品-------------------	

	////显示物品信息，需要输入序号（物品在背包的位置）
	UFUNCTION(Exec)
		void CS3_ItemInfo(int32 order);

	//------------------战斗-------------------	

	//查询战斗关系
	UFUNCTION(Exec)
		void CS3_QueryRelation();


	/*游戏功能调试*/
//------------------任务-------------------	


//------------------副本-------------------	

			  /*游戏功能调试*/
//------------------测试-------------------	

///测试
	UFUNCTION(Exec)
		void CS3_Test(const FString& FunctionName);

	//开始自动测试
	UFUNCTION(Exec)
		void CS3_StartAT(const FString& FunctionName);

	/**	查询当前输入状态
	*	@IT_Type	:	输入类型(eg. 0:按键/ 1:动作/ 2:轴/ 3:轴键/ 4:组合)
	*	@IT_Key		:	输入键或值(eg. K/L/... )
	*/
	UFUNCTION(Exec)
		void CS3_SearchInputState(int32 IT_Type, FName IT_Key);

	///查询entity当前播放的动画
	UFUNCTION(Exec)
		void CS3_CurrEntityAnimation();


	///恢复玩家
	UFUNCTION(Exec)
		void CS3_TestLG();

	///<全辅助
	UFUNCTION(Exec)
		void CS3_SwitchHomingSpellAtt();

	///<半辅助
	UFUNCTION(Exec)
		void CS3_SwitchHalfHomingSpellAtt();

	///<无辅助
	UFUNCTION(Exec)
		void CS3_SwitchNullAtt();

	//	测试指引
	UFUNCTION(Exec)
		void CS3_Trigger(const int32& Type, const FString& Param1, const FString& Param2);

	///<获取Actor数量
	UFUNCTION(Exec)
		void CS3_GetAllActorsNum();

	///<获取Actor类型及各类型数量
	UFUNCTION(Exec)
		void CS3_GetAllActorsTypeAndNum();

	///<获一定范围内的Actor数量
	UFUNCTION(Exec)
		void CS3_GetAllActorsInRangeTypeAndNum(float Range);

	///<获取Entity数量
	UFUNCTION(Exec)
		void CS3_GetAllEntitiesNum();

	///<获取Entity数量
	UFUNCTION(Exec)
		void CS3_GetAllEntitiesTypeAndNum();

	///<获一定范围内的entity数量
	UFUNCTION(Exec)
		void CS3_GetAllEntitiesInRangeTypeAndNum(float Range);

	///<获取entity的def属性
	UFUNCTION(Exec)
		void CS3_GetEntityDefProperty(int32 EntityID, FString Attr);

	///控制台切换单击玩家控制台命令
	UFUNCTION(Exec)
		void CS3_SwtichGameMode();

	UFUNCTION(Exec)
		void CS3_ModelsProfile(int32 modelnumer);

	UFUNCTION(Exec)
		void CS3_CreateFile(bool ModelorEffect);

	UFUNCTION(BlueprintCallable, Category = "consoleMgr")
		void CS3_WriteFile(TArray<FString> content, bool ModelorEffect);

	UFUNCTION(BlueprintCallable, Category = "consoleMgr")
		void CS3_WriteText(FString content, bool Peer);

	UFUNCTION(Exec)
		void CS3_TestShieldText();

	UFUNCTION(Exec)
		void CS3_SetIsUseShield(bool UseShield);

	///控制台命令隐藏或显示全部界面,此命令用于策划录像临时命令
	UFUNCTION(Exec)
		void CS3_HideOrShowVSWindows(bool bIsHide);
	///控制台命令隐藏或显示登录界面,此命令用于策划录像临时命令
	UFUNCTION(Exec)
		void CS3_HideOrShowLoginWindow(bool bIsHide);
	///查询Effect文件读取粒子特效资源并写入表中
	UFUNCTION(Exec)
		void CS3_GetAssetsByEffect();

	UFUNCTION(Exec)
		void CS3_GetAssetsByRoleLight();

	UFUNCTION(Exec)
		void CS3_TestAutoNavigate(const FVector& DstPosition);

	UFUNCTION(Exec)
		void CS3_TestQuestNavigate(const FString& NPCScriptID, FString DstSpaceName = "");

	UFUNCTION(Exec)
		void CS3_TestSpaceAllQuestNavigate(const FString& DstSpaceName);

	//创建一个单机的玩家（切换控制的角色测试用）
	UFUNCTION(Exec)
		void CS3_CreateClientPlayer();

	//切换控制的player（选中一个playerCharacter再调用）
	UFUNCTION(Exec)
		void CS3_SwitchControlPlayer();

	///测试指令，输出当前玩家的世界坐标和本地坐标
	UFUNCTION(Exec)
		void CS3_GetPlayerPos();

	///测试指令，输出当前玩家向下射线碰撞的位置高度
	UFUNCTION(Exec)
		void CS3_GetPlayerFloorTracePos();

	UFUNCTION(Exec)
		void CS3_ForceGarbageCollection();

	UFUNCTION(BlueprintCallable)
		TArray<FString> CS3_StringSort(TArray<FString> stringarray);

	UFUNCTION(Exec)
		void CS3_SwitchEmptyLogicLevel();

	UFUNCTION(Exec)
		void CS3_ChangeSubLebelLoadMode(int32 LoadMode);

	///显示当前玩家与目标的距离
	UFUNCTION(Exec)
		void CS3_TargetDistanceDIsplay();

	///隐藏当前玩家与目标的距离
	UFUNCTION(Exec)
		void CS3_TargetDistanceHiding();

	///暂停角色模型动画
	UFUNCTION(Exec)
		void CS3_PauseActorAnims(bool bIsPause, float FindRangle);

	///暂停角色模型布料计算
	UFUNCTION(Exec)
		void CS3_PauseActorCloth(bool bIsPause, float FindRangle);

	///暂停角色模型布料计算
	UFUNCTION(Exec)
		void CS3_OpenScope();

	///切换摄像机镜头模式
	UFUNCTION(Exec)
		void CS3_CareamModeChange();
	///切换摄像机飞行速度
	UFUNCTION(Exec)
		void CS3_ChangeFlySpeed (float MaxSpeed);
	///围绕目标旋转 目标单位为当前玩家选中目标
	UFUNCTION(Exec)
		void CS3_RotateRroundToTarget(float Speed, float Disatance, float Height, float angle);
	///停止围绕目标旋转
	UFUNCTION(Exec)
		void CS3_StopRotateRroundToTarget();
	///开启玩家转向摄像机开关 CST-7541
	UFUNCTION(Exec)
		void CS3_OpenLookCamera();
	///<改变玩家部件
	UFUNCTION(Exec)
		void CS3_ChangePart(int32 PartType, FString PartId);
	///<切换玩家骑乘
	UFUNCTION(Exec)
		void CS3_ChangeRidePet(FString CarrideId);
	///<切换玩家环身光效
	UFUNCTION(Exec)
		void CS3_ChangeBodyLightEffect(FString EffectId);
	///<切换玩家环身光效
	UFUNCTION(Exec)
		void CS3_ShowControllerModeInfo();

	///<异步播放声音
	UFUNCTION(Exec)
		void CS3_AsyncPlay3DSound(FString AudioId, int32 count=1);

	///<随机异步播放声音
	UFUNCTION(Exec)
	void CS3_AsyncPlay3DSoundRandomCount(int32 count, int32 times);
	



	//------------------用于调试或性能测试-------------------
	UFUNCTION(Exec)
		void CS3_SetComponentTickState(FString& ComponentName, bool NewTickState);
	UFUNCTION(Exec)
		void CS3_SetPlayerAllComponentTickState(bool NewTickState);
	UFUNCTION(Exec)
		void CS3_SetPlayerVisibleState(bool NewVisibleState);
	UFUNCTION(Exec)
		void CS3_RetainPlayerSkeletalMesh();
	UFUNCTION(Exec)
		void CS3_ToggleEntityServerPos(bool bIsPlayer);
	UFUNCTION(Exec)
		void CS3_Debug(bool isDebug);
	UFUNCTION(Exec)
		void CS3_DebugByName(FString& CS3DebugTypeName, bool isDebug);
	UFUNCTION(Exec)
		void CS3_NotEnablePhysics();
	UFUNCTION(Exec)
		void CS3_NotHair();
	UFUNCTION(Exec)
		void CS3_NotModel();
	UFUNCTION(Exec)
		void CS3_ChangeJobCreateRoleLevel(int32 Job);//切换创建角色四职业关卡
	UFUNCTION(Exec)
		void CS3_SetModelHide(FString ScriptId);//隐藏模型（后面不传则是恢复隐藏的模型）
	UFUNCTION(Exec)
		void CS3_StopModeCurAction(FString ScriptId);//停止当前动作
	UFUNCTION(Exec)
		void CS3_CancelStopModeCurAction(FString ScriptId);//取消停止当前动作
	UFUNCTION(Exec)
		void CS3_StopModelAnim(FString ScriptId);//停止动作及动画蓝图
	UFUNCTION(Exec)
		void CS3_CancelStopModelAnim(FString ScriptId);//取消停止动作及动画蓝图
	void ExectModelActionSetup(int32 type, FString ScriptId);
	UFUNCTION(Exec)
		void CS3_LedgesJumpDrawDebug(int32 DrawType);//射线碰撞线条显示
	UFUNCTION(Exec)
		void CS3_DisplayStoryLog(bool isDebug);//显示镜头日志

	void DisplayStoryLog(FString StoryID, bool bIsPlay);//显示镜头日志
	//-----------------------------------------

	/** 监测输入事件是否激活 // @NOTE 该处判断多个状态中有不激活则不激活该输入 */
	UFUNCTION(BlueprintPure, Category = "CS3layerController|Input")
		bool CheckBindKeyActive(FKey Key);
	UFUNCTION(BlueprintPure, Category = "CS3PlayerController|Input")
		bool CheckBindActionActive(FName Name);
	UFUNCTION(BlueprintPure, Category = "CS3PlayerController|Input")
		bool CheckBindAxisActive(FName Name);
	UFUNCTION(BlueprintPure, Category = "CS3PlayerController|Input")
		bool CheckBindAxisKeyActive(FKey Key);

	void SetEnableEntityServerPos(bool bEnabled) { bEnableEntityServerPos = bEnabled; };
	bool GetEnableEntityServerPos() { return bEnableEntityServerPos; };
	void SetEnablePlayerServerPos(bool bEnabled) { bEnablePlayerServerPos = bEnabled; };
	bool GetEnablePlayerServerPos() { return bEnablePlayerServerPos; };

	///<由于AudioMananger是Actor 关卡切换会销毁
	void SetEnableAudioSystem(bool bEnabled) { bEnableAudioSystem = bEnabled; };
	bool GetEnableAudioSystem() { return bEnableAudioSystem; };
	AActor* oldPlayer;

public:
	bool isArmLimit;//是否限制摄像机缩放 CST-CST-7046

private:
	TArray<FString> CacheModelIds;
	bool bEnableEntityServerPos = true;
	bool bEnablePlayerServerPos = true;
	bool bEnableAudioSystem = true;
	bool bEnableDisplayStoryLog = false;
};
