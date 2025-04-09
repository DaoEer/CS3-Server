/**
* Fill out your copyright notice in the Description page of Project Settings.
*/

#pragma once

#include "Engine/GameInstance.h"
#include "KBEngineApp.h"
#include "CS3GameInstance.generated.h"

/*
* 文件名称：CS3GameInstance.h
* 功能说明：
* 文件作者：wuxiaoou
* 目前维护：wuxiaoou
* 创建时间：2018-04-28
*/
DECLARE_MULTICAST_DELEGATE_OneParam(FCS3PostLoadMapDelegate, UWorld* /* LoadedWorld */);

using namespace KBEngine;

class CS3PlayRole;
class Account;

/**
 * 
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UUECS3GameInstance : public UGameInstance
{
	GENERATED_BODY()
	
	virtual void Init() override;
	virtual void BeginDestroy() override;
	virtual void FinishDestroy() override;
	bool bIsFristBindPostLoadMap;
	FDelegateHandle PreLoadMapHandle;
	FDelegateHandle LoadMapFinishHandle;
public:

	//是否退出了GameInstance
	bool bIsShutDown = false;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "GameDefault")
		class UGameDefault* GameDefault;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "ConstData")
		class UConstDataBP* ConstDataBP;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UResourceManager* ResourceManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UCfgManager* CfgManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UParticleManager* ParticleManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class ULoginManager* LoginManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UGStoryManager* GStoryManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UMediaPlayerManager* MediaPlayerManager;
	
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UUIDockManager* UIDockManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UUIFixerManager* UIFixerManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class ULevelManager* LevelManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UActionManager *ActionManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UMessageManager* MessageManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UGameStatus* GameStatus;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class AAudioManager* AudioManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class ULocalDataSaveManager* LocalDataSaveManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class USkillManager* SkillManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UQuestManager* QuestManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UBuffManager* BuffManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UCustomCursorManager* CustomCursorManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UMapManager* MapManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UPlaneTriggerManager* PlaneTriggerManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UMessageID* GMessageID;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UGLoaderManager* GLoaderManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UVisibleManager* VisibleManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UQuestEntityVisibleManager* QuestEntityVisibleManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UBuffEntityVisibleManager* BuffEntityVisibleManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UGEventManager* GEventManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UGameplayEventManager* GameplayEventManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UGUIManager* GUIManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UHyperlinkManager* HyperlinkManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UTipsManager* TipsManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class USpaceEntityRelationMgr* SpaceEntityRelationMgr;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class USpaceDynamicEffectManager* SpaceDynamicEffectManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UItemFactory* ItemFactory;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UEmoteManager* EmoteManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UAreaWallData* AreaWallData;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UDecalManager* DecalManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UTextParseManger* TextParseMgr;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UAutoNavigatePathMgr* AutoNavigatePathMgr;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UForceManager* ForceManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UAutoTestManager* AutoTestManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UAutoFightMar* AutoFightMar;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UCharacterRideManager *CharacterRideManager;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UModifyFaceManager *ModifyFaceManager;

	//新手指引系统 
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UTutorialManager* TutorialManager;

	//系统开启
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class USystemSwitchManager* SystemSwitchManager;

	//跨地图寻路路径查找管理 
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UCrossMapNavigateMgr* CrossMapNavigateMgr;

	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UClientGMCMDToServer* ClientGMCMDToServer;
	//控制模式管理 
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UControllerModeMgr* ControllerModeMgr;
	//操作模式管理 
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UOperationModeMgr* OperationModeMgr;
	//QTE管理器
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UQTEManager* QTEManager;
	//屏蔽字管理器 
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UTextShieldMgr* TextShieldMgr;

	//客户端时间管理器 
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UTimeManager* TimeManager;

	//客户端定时器管理器 
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UCustomTimerManager* CustomTimerManager;

	//客户端自定义碰撞检测管理器
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UShapeManager* ShapeManager;

	//头像（半身像）系统 
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class AHeadManager* HeadManager;
	
	//快捷栏管理器
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Manager")
		class UQuickBarManager* QuickBarManager;

	//图片加载器
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Tool")
		class UImageLoader* ImageLoader;

	//技能加载器
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Tool")
		class USkillLoader* SkillLoader;
	//效果加载器
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Tool")
		class UEffectLoader* EffectLoader;
	//buff加载器
	UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Tool")
		class UBuffLoader* BuffLoader;

	//UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "PC")
		class ACS3PlayerController* CS3PC;		///< 玩家的playercontroller

	//UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "PC")
	//class AServerCharacter* PlayerCharacter;	///< 玩家控制的Characher

	static FCS3PostLoadMapDelegate LevelBeginPlayDelegate;

	FDateTime RecordServerTime;		// 记录服务器与客户端运行时间的差值

	bool bIsGameReturnLogin = false;//是否游戏返回登陆
private:
	class CS3CreateListener* CreateListener;
	class CS3DeleteListener* DeleteListener;
	//游戏窗口是否为激活状态
	bool bIsGameWindowActive;
	FDelegateHandle GameWindowHandle;
	
public:
	static KBEngine::KBEngineApp * pKBEApp;
	static UUECS3GameInstance* Instance;

	virtual void Shutdown() override;

	bool IsGameWindowActive() { return bIsGameWindowActive; }

	UFUNCTION(BlueprintCallable, Category = "cs3")
	void RoleEnterWorld(FString Name);

	UPROPERTY(BlueprintReadOnly, Category = "Player")
	class USavePlayerData* SaveData;		///< 玩家在每次OpenLevel时需要保存的数据


	/**
	*蓝图可调用，恢复UI
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Player")
		void ReStoreUI();

	bool ProcessConsoleExec(const TCHAR* Cmd, FOutputDevice& Ar, UObject* Executor) override;

	virtual void LoadComplete(const float LoadTime, const FString& MapName) override;

	//开启怪物/NPC掉落宝箱特效
	UFUNCTION(BlueprintCallable, Category = "cs3")
		void SetAllDropBoxTipsEffect(bool bIsDropTipsEffect);

	UFUNCTION()
		void OnActorEndPlay(AActor* Actor, EEndPlayReason::Type EndPlayReason);

	//是否在进入游戏之前
	bool IsEnterGameBefor();
	//同步服务器时间
	void TimeSynchronization(FString& ServerTime);

	void CheckApplicationActivation(bool bIsActive);

	void ClearObjectHandles(const void * UserObject);

private:
	void CheckLanderSystemSetting();//检测登陆器过来的系统设置

	// 这个函数限制了客户端调用GetTimerManager()方法，请使用CustomTimerManager调用SetTimer()等方法
	inline FTimerManager& GetTimerManager()
	{
		return Super::GetTimerManager();
	}

	FTimerManager* TimerManager;

private:
	CS3PlayRole *_cs3plyerPtr;

public:
	inline CS3PlayRole *CS3Player() { return _cs3plyerPtr; }
	void CS3Player(CS3PlayRole* cs3Player) { _cs3plyerPtr = cs3Player; }

};


