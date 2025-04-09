#pragma once

#include "GameData/StoryData.h"
#include "GameData/CS3Object.h"
#include "LevelSequenceActor.h"
#include "DelegateCombinations.h"
#include "GameData/StoryLoadModelData.h"
#include "StoryManager.generated.h"

/*
* 文件名称：StoryManager.h
* 功能说明：剧情管理类
* 文件作者：liushuang
* 目前维护：huting
* 创建时间：2016-11-01
*/

DECLARE_STATS_GROUP(TEXT("UGStoryManager"), STATGROUP_UGStoryManager, STATCAT_Advanced);

DECLARE_MULTICAST_DELEGATE(FLoadStoryOverDelegate);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FPlayAnimEventDelegate, UAnimSequenceBase*, AnimSequence, float, PlayRate, bool, bLoop);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FStopAnimEventDelegate);
DECLARE_MULTICAST_DELEGATE_OneParam(FStartSequenceDelegate, FString);///<镜头开始（前过渡摄像机完成之后）
DECLARE_MULTICAST_DELEGATE_OneParam(FStopSequenceDelegate, FString);///<镜头结束（后过渡摄像机完成之后）
/**
*
*/
UCLASS(BlueprintType)
class  ACS3LevelSequenceActor : public ALevelSequenceActor
{
	GENERATED_BODY()
public:

	ACS3LevelSequenceActor(const FObjectInitializer& Init);

	virtual void BeginDestroy()override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

};



UCLASS(Blueprintable)
class CHUANGSHI_API UGStoryManager : public UCS3Object
{
public:
	GENERATED_BODY()

		UGStoryManager();
	~UGStoryManager();

	static UGStoryManager* GetInstance();

	virtual void BeginDestroy()override;

	void ResetStoryData();///<重置剧情数据相关

	/**
	*蓝图可调用，播放剧情
	*
	*@param SequenceId 剧情ID
	*@param NumLoops 剧情循环次数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void PlaySequence(const FString& SequenceId, int32 NumLoops = 1);

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void PauseSequence();///<暂停播放剧情
	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void StopSequence();///<停止播放剧情

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void JumpToFrameSequence(int32 NewPosition);///<调到镜头多少帧

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void PlayToFrameSequence(FFrameTime NewPosition);
	/**
	*BlueprintPure， 获取当前播放剧情Id
	*
	*@return FString 当前播放剧情Id
	*/
	UFUNCTION(BlueprintPure, Category = "StoryManager")
		FString GetCurrPlayId();
	/**
	*BlueprintPure，当前剧情是否播放
	*
	*@return bool 当前剧情播放返回TRUE，否则返回FALSE。
	*/
	UFUNCTION(BlueprintPure, Category = "StoryManager")
		bool IsPlaying();
	/**
	*当前LevelSequence是否播放,主要是给显示Entity的IsShowModel()函数(假如有过度摄像机先显示已隐藏的Entity，
	*若用IsPlaying()CurrPlayId数据没有重置导致不能正确显示已隐藏的Entity)以及按ESC跳过动画界面使用
	*@return bool 当前LevelSequence播放返回TRUE，否则返回FALSE。
	*/
	UFUNCTION(BlueprintPure, Category = "StoryManager")
		bool IsLevelSequencePlaying();
	/**
	*BlueprintNativeEvent，BlueprintCallable，预加载镜头相关
	*
	*@param SpaceId 关卡ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void PreLoadStory(const FName& SpaceId);

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void StoryEventByParams(CSTORY_EVENT_PARAM_TYPE_ENUM EventName, const FString& Param1, const FString& Param2, const FString& Param3, const FString& Param4);///<BlueprintCallable，Begin Story Sequence Event 事件：带参数事件

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void NotifyServerEvent();///<BlueprintCallable，Begin Story Sequence Event 事件：通知服务器

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void PlayVoiceWords();///<BlueprintCallable， 事件：播放语音文字

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void PlayVoiceWordsByParam(const FString& VoiceWords);///<BlueprintCallable， 事件：播放语音文字

	UFUNCTION(BlueprintCallable, BlueprintNativeEvent, Category = "StoryManager")
		void PlayTextEvent();///<BlueprintCallable， 事件：播放字幕

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void PlayRedrawViewports();///<BlueprintCallable， 事件：停止渲染

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void PlayAnimEvent();///<BlueprintCallable，Begin Story Sequence Event 事件：播放动作资源

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void PlayAnimByIndexEvent(int32 Index);///<BlueprintCallable，Begin Story Sequence Event 事件：播放动作资源

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void PlayAnimEventByParam(const FString& AnimName, float PlayRate = 1.0f, bool bLoop = true);///<BlueprintCallable，Begin Story Sequence Event 事件：播放动作资源

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void StopAnimEvent();///<BlueprintCallable，Begin Story Sequence Event 事件：停止播放动作资源

	/**
	*是否符合显示模型条件
	*
	*@param Actor Actor对象
	*@param EntityId EntityId
	*
	*@return bool 符合显示模型条件返回TRUE，否则返回FALSE。
	*/
	bool IsShowModel(AActor* Actor, int32 EntityId);

	/**
	*检测能否播预加载镜头
	*
	*@return 无
	*/
	void CheckPreLoadStory(FString SpaceID, bool& bCanExec, FString& StoryID);

	int PreLoadStoryAsset(const FLoadStoryOverDelegate& InLoadStoryOverDelegate = FLoadStoryOverDelegate());

	void PreLoadAllStoryAsset();

	///处理跳过事件
	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		bool CanSkip(bool& IsMedia);///<是否可跳过

	///处理跳过事件
	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		float GetSkipTimeData(float& EndTime, float& CurTime, float& StartTime);///<获取当前可跳过的时长

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void OnSkipEvent();///<跳过事件

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		bool IsControlledByPlayer();///<当前是否使用玩家的摄像机

	void ClearStoryAsset();///<清除镜头资源释放内存

	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void BP_GetStoryData(const FString& SequenceId, FSTORY_DATA& StoryData);

	bool IsNeedHideUI();///<当前剧情是否需要隐藏UI

	void SetPlayRate(float rate);///修改播放速率

	bool IsStopLoadingLevel();
	UFUNCTION(BlueprintCallable)
		void IsOpenMediaUI(bool IsOpen = true);
	UFUNCTION(BlueprintCallable)
		void ResetHZMGStoryOperate();
protected:
	/**
	*获取剧情数据相关
	*
	*@param SequenceId 剧情ID
	*
	*@return FSTORY_DATA* 剧情数据
	*/
	const FSTORY_DATA* GetStoryData(const FString& SequenceId);

	/**
	*获取剧情事件数据相关
	*
	*@param SequenceId 剧情ID
	*
	*@return FSTORY_DATA* 剧情数据
	*/
	const FSTORY_EVENT_DATA* GetStoryEventData(const FString& SequenceId);

	/**
	*获取剧情动画事件数据相关
	*
	*@param SequenceId 剧情ID
	*
	*@return FSTORY_DATA* 剧情数据
	*/
	const FSTORY_ANIM_EVENT* GetStoryAnimEventData(const FString& AnimName);

	UFUNCTION(Category = "StoryManager")
		void OnStoryStop();///<BlueprintNativeEvent,停止播放剧情回调	

	UFUNCTION(BlueprintImplementableEvent, Category = "StoryManager")
		void BP_OnStoryStop();

	FString GetPausedVoiceType(bool bIsHideNewVioce = false);///<获取当前暂停的音效类型	

	UFUNCTION(BlueprintImplementableEvent, Category = "StoryManager")
		void StoryTriggerUI(bool bIsPlaying = false);
	/**
	*获取前过渡摄像机
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void GetPreCameraData(FCAMERA_SETTINGS_DATA& PreCameraSettings);

	/**
	*前过渡摄像机
	*
	*@param NumLoops 剧情循环次数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "StoryManager")
		void PlayPreCamera(int32 NumLoops = 1);

	/** 镜头开始 前过渡摄像机操作之后延时处理播放镜头部分
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "StoryManager")
		void OnDelayPlayStoryOperate(int32 NumLoops = 1);


	UFUNCTION(BlueprintImplementableEvent, Category = "StoryManager")
		void LoadStroyModel(const TArray<FString>& HeadModelID);

private:
	/**
	*预加载镜头语音半身像所需的模型资源
	*
	*@return FSTROY_LOAD_MODEL_DATA 配置数据
	*/
	const FSTROY_LOAD_MODEL_DATA* GetPreLoadStoryVoiceModelAsset(FString SequenceId);

	void PrePlaySequence(ULevelSequence* StroyAss, int32 NumLoops, const FString& SequenceId);///<正式播放定序器前操作（前过渡摄像机、Entity的隐藏、下马、玩家镜头模式切换等）

	/**
	* 暂停播放声音
	*
	*	@param	bPause :True(暂停), False(播放)
	*
	*@return 无
	*/
	void PausedVoice(bool bPause, const FString HideVoiceType);

	/**
	*结束镜头摄像机操作
	*
	*@return float 结束镜头摄像机操作是否有平滑操作时间
	*/
	float EndCameraAnim();

	/**
	*开始镜头前过渡摄像机操作
	*
	*@return float 是否有平滑操作时间
	*/
	float PreCameraTime();

	/**
	* 播放和结束剧情,切换到剧情模式（按键的输入输出）
	*
	*@param	IsPlay :True(播放), False(停止)
	*
	*@return 无
	*/
	void SwitchStoryMode(bool IsPlay);

	void StartPlaySequence(int32 NumLoops = 1);

	void OnStoryOperation();///<隐藏entity、玩家下马、设置AOI范围等操作
	/** 客户端设置AOI
	*
	*@param Radius 	AOI半径(单位:米)
	*
	*@return 无
	*/
	void ClientSetAoi();

	/** 重置AOI
	*
	*@return 无
	*/
	void ClientResetAoi();

	/** 设置玩家摄像机朝向
	*
	*@param Radius 	AOI半径(单位:米,默认80)
	*
	*@return 无
	*/
	void SetPlayerCamera(FRotator Rotater);

	/** 结束镜头摄像机操作之后延时处理停止镜头部分
	*
	*@return 无
	*/
	void OnDelayStoppingStoryOperate();

	void SetManualCameraFade();
	void StopAllCameraShakes();// 停止镜头抖动相关

	/** 真正播放资源
	*
	*@return 无
	*/
	void RelPlaySequence(TSoftObjectPtr<ULevelSequence> StroyAss, int32 NumLoops, const FString& SequenceId);

	void ClearDelayDestroyCameraTimer();//删除延时销毁摄像机定时器

	void LoadStoryAsset(FString storyID, TSoftObjectPtr<ULevelSequence> StroyAss);///<加载镜头资源
	void LoadStoryAssetEnd(TSoftObjectPtr<ULevelSequence> stroyAss = nullptr);///<加载单个资源结束

	void HidePlayer();///<隐藏玩家自己
	void HideOtherPlayer();///< 隐藏其他玩家类型
	void HideOtherPlayerPet();///<隐藏其他玩家宠物
	void HidePlayerPet();///<隐藏玩家宠物
	void HideNonPlayerEntity(); ///<隐藏非玩家对象
	void StoryHideEntities(bool bIsHide); ///<屏蔽功能主要执行函数
	void HideSceneCharacter(TArray<FString> IgnoreUIDs);///<屏蔽场景纯客户端Actor

	void DisRideOnCarrier();///<下马操作
	
	UFUNCTION()
		void LoadNextSubLevelFinished(FString NextSubLevelName);
	UFUNCTION()
		void InWorldLoadingOverEvent();///<

	void CheckStopInWorldOver();
	void CheckIsStopLoop();///<检测循环镜头是否结束HZMG CST-7240


	bool CheckCanJumpToFrame(FFrameTime NewPosition);///<检测是否能跳到某帧
	bool CheckCanPlayToFrame(FFrameTime NewPosition);///<检测是否能跳到某帧

	FFrameTime GetPlayToFrameData();

	void onNotifyAddEffectList();
	void onNotifyRemoveEffectList();
public:
	UPROPERTY(BlueprintAssignable, Category = "StoryManager")
		FPlayAnimEventDelegate OnPlayAnimEventDelegate;

	UPROPERTY(BlueprintAssignable, Category = "StoryManager")
		FStopAnimEventDelegate OnStopAnimEventDelegate;
protected:
	UPROPERTY(BlueprintReadOnly)
		ACS3LevelSequenceActor* LevelSequenceActor; ///< 在PlaySequence时如果不存在就会自动创建
	UPROPERTY(BlueprintReadWrite)
		FString CurrPlayId = TEXT("");///<当前剧情Id
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> HideEntitiesList;///<屏蔽功能隐藏链表	
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, ULevelSequence*>StoryAssList;///<关卡镜头资源列表
	UPROPERTY(BlueprintReadOnly)
		int32 CurrTextIndex = -1;	///<当前文本事件索引
	UPROPERTY(BlueprintReadOnly)
		int32 CurrVoiceIndex = -1;	///<当前剧情语音索引
	UPROPERTY(BlueprintReadWrite)
		bool bIsPreCamera = false; ///<是否处于前过渡摄像机

	FStartSequenceDelegate StartSequenceDelegate;
	FStopSequenceDelegate StopSequenceDelegate;
private:
	FTimerHandle DelayStopInWorldOverHandle;///<是否传送到世界中结束播放镜头
	FTimerHandle CheckOneTimeHandle;///<检测镜头播放一次是否结束HZMG CST-7240
	FTimerHandle DelayDestroyCameraHandle;///<延时销毁后过渡摄像机
	FTimerHandle DelayHandle;
	FLoadStoryOverDelegate LoadStoryOverDelegate;///<镜头加载事件委托
	UPROPERTY()
		TMap<FString, TSoftObjectPtr<ULevelSequence>>StoryAss;///<镜头加载资源
	UPROPERTY()
		TMap<FString, TSoftObjectPtr<ULevelSequence>>AllStoryAss;///<当前地图所有需要预加载镜头资源
	int Count = 0;///< 当前镜头加载数量
	float FadeTimer = 0.0f;///<设置淡入淡出延迟时间
	int32 CurrOrderIndex = -1;	///< 当前剧情服务器指令索引
	int32 CurrAnimIndex = -1;	///<当前剧情动画索引	
	bool bIsPlayingToUI = false;///<给UI显示使用
	FTimerHandle DelayLoadAllStoryHandle;

	bool bIsEndCamera = false; ///<是否处于后过渡摄像机

	int32 JumpToFrameCount = 0;
	bool bIsJumpToOpenDoorFinished = false;
};
