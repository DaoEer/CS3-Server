#pragma once
#include "CoreMinimal.h"
#include "Engine/StreamableManager.h"
#include "GameData/VoiceData.h"
#include "GameFramework/Actor.h"
#include "GameData/AudioData.h"
#include "GameData/StoryData.h"
#include "Sound/SoundClass.h"
#include "Component/CS3AudioComponent.h"
#include "AudioManager.generated.h"

DECLARE_STATS_GROUP(TEXT("AAudioManager"), STATGROUP_AAudioManager, STATCAT_Advanced);
/*
* 文件名称：AudioManager.h
* 功能说明：音频管理类
* 文件作者：LiuShuang
* 目前维护：huting
* 创建时间：2016-08-06
*/
DECLARE_DELEGATE_OneParam(FCClientVoiceComplete, FString);
DECLARE_DYNAMIC_DELEGATE_OneParam(FClientVoiceComplete, FString,ClientVoiceID);
DECLARE_DYNAMIC_DELEGATE(FAsynLoadAudioAssetComplete);

UCLASS(BlueprintType)
class CHUANGSHI_API AAudioManager : public AActor
{
	GENERATED_BODY()

private:
	AAudioManager();

public:
	static AAudioManager* GetInstance();

	virtual void BeginPlay() override;
	virtual void Tick(float DeltaSeconds) override;
	virtual void Destroyed() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void BeginDestroy()override;

#pragma region  多段语音播放支持
	/**
	*BlueprintCallable,播放声音
	*
	*@param AudioId 声音Id
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|Voice")
		void PlayVoice(const FString& AudioId);

	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable, Category = "AudioManager|Voice")
		void LoopPlayVoice(); ///<BlueprintImplementableEvent, 循环播放声音

	UFUNCTION(BlueprintCallable, Category = "AudioManager|Voice")
		void BreakVoice();///<BlueprintImplementableEvent, 中断播放声音

	UFUNCTION(BlueprintCallable, Category = "AudioManager|Voice")
		void StopVoice();///<BlueprintCallable, 停止播放声音

	UFUNCTION(BlueprintImplementableEvent, Category = "AudioManager|Voice")
		void BP_StopVoice();///<BlueprintImplementableEvent,BlueprintCallable, 停止播放声音

	UFUNCTION(BlueprintCallable, Category = "AudioManager|Voice")
		void PausedVoice(bool bPause);///<BlueprintCallable,暂停播放声音
#pragma endregion	

#pragma region  单段语音播放支持
	//单段语音的播放就是最简单的开始和结束，不判断状态，可以被任意结束
	 /**
	 *BlueprintCallable，纯客户端(阵容选择,角色创建等),在该模块结束时需调用ClientVoiceStop结束
	 *
	 *@param AudioId 音频资源Id
	 *
	 *@return 无
	 */
	UFUNCTION(BlueprintCallable, Category = "AudioManager|Voice")
	void ClientVoicePlay(const FString& AudioId, FClientVoiceComplete ClientVoiceComplete)
	{
		ClientVoicePlay(AudioId, FCClientVoiceComplete::CreateLambda([ClientVoiceComplete](FString ClientAudioId)
		{
			ClientVoiceComplete.ExecuteIfBound(ClientAudioId);
		}));
	}

	void ClientVoicePlay(const FString& AudioId, FCClientVoiceComplete ClientVoiceCreate);

	UFUNCTION(BlueprintCallable, Category = "AudioManager|Voice")
		void ClientVoiceStop();///<BlueprintCallable，纯客户端(阵容选择,角色创建等),在该模块结束时需调用ClientVoiceStop结束

	UFUNCTION(Category = "AudioManager|Voice")
		void OnClientVoiceFinished(UAudioComponent* AudioComponent);
#pragma endregion

#pragma region  UI声音播放支持
	/**
	*BlueprintCallable，播放UI相关
	*
	*@param AssetId 资源Id
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|SoundUI")
		void PlaySoundUI(const FString& AssetId);
#pragma endregion

#pragma region  背景音乐播放	
	

	/**
	*BlueprintCallable，停止播放背景(战斗)音乐
	*
	*@param IsPlayBgMusic True:背景音乐,False:战斗音乐
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|SceneMusic")
		void StopSceneMusic(bool IsPlayBgMusic);

	/**
	*BlueprintImplementableEvent，BlueprintCallable，循环播放背景(战斗)音乐
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|SceneMusic")
		void LoopPlaySceneMusicByPlayerState(bool bIsBgMusic = true, bool bIsPlay = true, bool bByPlayerState = false);
#pragma endregion	

#pragma region  播放3D音效
	/**
	*播放3D声音
	*注：3D声音组件的bOverrideAttenuation属性应为true
	*
	*@param AudioComponent 3D声音组件(UCS3AudioComponent*)
	*@param AudioId	声音Id(FString)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		UCS3AudioComponent* Play3DSound(AActor* TargetActor, const FString& AudioId, FVector Postion = FVector::ZeroVector, EAUDIOCOMPTYLE AudioCompType = EAUDIOCOMPTYLE::NONE, bool bIsLoop = false, USceneComponent* AttachComp = nullptr);

	/**
	*异步播放3D声音
	*注：3D声音组件的bOverrideAttenuation属性应为true
	*播放时间会加上加载资源得时间,可能导致播放一半或没播放
	*
	*@param AudioComponent 3D声音组件(UCS3AudioComponent*)
	*@param AudioId	声音Id(FString)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		UCS3AudioComponent* AsyncPlay3DSound(AActor* TargetActor, const FString& AudioId, FVector Postion = FVector::ZeroVector, EAUDIOCOMPTYLE AudioCompType = EAUDIOCOMPTYLE::NONE, bool bIsLoop = false, USceneComponent* AttachComp = nullptr);

	/**
	*播放3D声音
	*注：3D声音组件的bOverrideAttenuation属性应为true
	*
	*@param AudioComponent 3D声音组件(UCS3AudioComponent*)
	*@param AudioId	声音Id(FString)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		UCS3AudioComponent* Play3DSoundByAsset(AActor* TargetActor, TSoftObjectPtr<USoundBase> AudioAsset, FVector Postion = FVector::ZeroVector, EAUDIOCOMPTYLE AudioCompType = EAUDIOCOMPTYLE::NONE, bool bIsLoop = false, USceneComponent* AttachComp = nullptr, float StartTime = 0.0f);

	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		void StopAllSkill3DSound();///<停止播放所有技能3D声音
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		void Stop3DSound(UCS3AudioComponent* AudioComponent);///<停止播放单个3D声音

#pragma endregion

#pragma region  播放客户端预览音效
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		bool PlayPreviewSound(const FString& AudioPath);///<播放客户端预览音效
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		void StopPreviewSound();///<停止播放客户端预览音效
#pragma endregion

#pragma region  环境音效		
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		void PlayEnvironmentSound();///<播放客户端预览音效
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		void StopEnvironmentSound();///<停止播放客户端预览音效
#pragma endregion

#pragma region  镜头音效		
	void AddStoryAudio(const FString& Id);///<镜头音效
	void ResetStoryAudio();
#pragma endregion

#pragma region  天气音效		
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		void PlayWeatherSound(TSoftObjectPtr<USoundBase> AudioAsset);///<播放天气音效
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		void StopWeatherSound();///<停止天气音效
	void UpdateWeatherComp(USceneComponent* SceneComp);///<更新天气音效组件
	void UnBindWeatherSoundComp();///<更新天气音效组件
#pragma endregion

#pragma region  音量调整
	/**
	*BlueprintCallable，设置背景(战斗)音乐音量
	*
	*@param inVol 音量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|AboutVol")
		void SetBgVol(float inVol);

	/**
	*BlueprintCallable，设置Voice音量
	*
	*@param inVol 音量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|AboutVol")
		void SetSingleVoiceVol(float inVol);

	/**
	*BlueprintCallable，设置ClientVoice音量
	*
	*@param inVol 音量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|AboutVol")
		void SetVoiceVol(float inVol);

	/**
	*BlueprintCallable，设置EffVol音量
	*
	*@param inVol 音量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|AboutVol")
		void SetEffVol(float inVol);

	/**
	*BlueprintCallable，设置BgEffectComp音量
	*
	*@param inVol 音量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|AboutVol")
		void SetBgEffVol(float inVol);

	/**
	*BlueprintCallable，设置MasterVol音量
	*
	*@param inVol 音量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|AboutVol")
		void SetMasterVol(float inVol);

	/**
	*BlueprintPure，获取背景(战斗)音乐音量
	*
	*@return float 背景(战斗)音乐音量
	*/
	UFUNCTION(BlueprintPure, Category = "AudioManager|AboutVol")
		float GetBgVol();

	/**
	*BlueprintPure，获取ClientVoice音量
	*
	*@return float ClientVoice音量
	*/
	UFUNCTION(BlueprintPure, Category = "AudioManager|AboutVol")
		float GetVoiceVol();

	/**
	*BlueprintPure，获取设置EffVol音量
	*
	*@return float EffVol音量
	*/
	UFUNCTION(BlueprintPure, Category = "AudioManager|AboutVol")
		float GetEffVol();

	/**
	*BlueprintPure，获取BgEffectComp音量
	*
	*@return float BgEffectComp音量
	*/
	UFUNCTION(BlueprintPure, Category = "AudioManager|AboutVol")
		float GetBgEffVol();

	/**
	*BlueprintPure，获取MasterVol
	*
	*@return float MasterVol音量
	*/
	UFUNCTION(BlueprintPure, Category = "AudioManager|AboutVol")
		float GetMasterVol();
#pragma endregion

#pragma region  检测是否能播放某音效
	
#pragma endregion

	UFUNCTION(BlueprintCallable, Category = "AudioManager|Callback")
		void OnLeaveWorld();///<离开世界

	UFUNCTION(BlueprintCallable, Category = "AudioManager|Callback")
		void ClearAudioData();///<清除音频数据 

	/**
	*BlueprintCallable，调用该函数解析语音资源、返回语音内容（语音入口）
	*
	*@param Id 解析语音编号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|Analysis")
		void AnalysisVoiceData(const FString& Id);

	/**
	*BlueprintCallable，是否正在播放声音
	*
	*@param VoiceId 声音ID
	*
	*@return bool
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		bool IsPlaying(const FString& VoiceId = TEXT(""));

	/**
	*设置最后语音Id
	*
	*@param LastVoiceId 最后语音Id
	*
	*@return 无
	*/
	void SetLastVoiceId(FString LastVoiceId);

	/**
	BlueprintPure，获取语音对应的文本内容
	*
	*@param VoiceId 语音资源Id
	*
	*@return FString 语音对应的文本内容
	*/
	UFUNCTION(BlueprintPure, Category = "AudioManager|Voice")
		FString GetVoiceContentText(const FString& VoiceId) const;

	/**
	BlueprintCallable，播放环境音效和背景音效
	*
	*@return
	*/
	UFUNCTION(BlueprintCallable, Category = "AudioManager|Voice")
		void PlaySceneAndEnvironmentMusic();

	///<根据隐藏类型暂停声音,
	void SetPausedVoice(TArray<FString> CurPauseTypes, TArray<FString> CurHideTypes, bool bPause = true,bool bIsHideVoiceType = true);

	//因为需要在异步播放音效得回调中使用,防止重复写一样得代码
	void SetAudioComponent_AudioAsset(AActor* TargetActor, UCS3AudioComponent* AudioComponent, bool bIsLoop, float StartTime, TSoftObjectPtr<USoundBase> AudioAsset, EAUDIOCOMPTYLE AudioCompType);

	void TogglePlayAudioSystem();
	
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		bool CheckPlayVoice(CSTORY_VOICE_TYPE VoiceType);///<检查是否能否播放声音
	UFUNCTION(BlueprintCallable, Category = "AudioManager")
		void SetIsPlayRumorVoice(bool isPlayRumorVoice){ bIsPlayRumorVoice = isPlayRumorVoice; };///<设置是否为传话状态
protected:
	UFUNCTION(BlueprintCallable, Category = "AudioManager|CallBack")
		void OnVoicesFinishedCB(FVOICE_DATA& VoiceData);///<语音播放完成回调 参数为播放完的语音的信息
	UFUNCTION()
		void OnSceneAudioFinishedNative(UAudioComponent* AudioComponent);///<背景播完回调事件
	UFUNCTION()
		void On3DAudioFinishedNative(UAudioComponent* AudioComponent);///<3D播完回调事件
private:
	/**
	*播放延时
	*
	*@param Delay 延时时间
	*
	*@return 无
	*/
	void DelayPlayVoice(float Delay = 0.f);

	void InitAudioComp();///<初始化音频组件
	void InitAudioData();///< 初始化基础数据

	bool GetEnableAudioPlay() { return bEnableAudioPlay; };

	/**
	*检查是否能播放声音
	*
	*@param VoiceData
	*
	*@return bool 能播放声音返回True，否则返回False。
	*/
	bool CheckVoicePlay(FVOICE_DATA VoiceData);

	void RefreshVoiceData(FVOICE_DATA& VoiceData);

	void NotifyPerformanceInterfaceToPlayNext();

	/**
	*播放背景(战斗)音乐
	*
	*@param IsPlayBgMusic True:背景音乐,False:战斗音乐
	*
	*@return
	*/
	void PlaySceneMusic(bool IsPlayBgMusic);
	/**
	*获取CSV_CONFIG_TYPE_SCENE_MUSIC->SceneMusicConfig数据
	*
	*@param IsBgMusic 选择加载背景音乐或战斗音乐
	*@param SceneName 当前关卡Id，作为获取数据表RowName
	*@param IsFindPlayList 是否找到播放链表,用于迭代操作
	*
	*@return USoundBase* 背景音乐或战斗音乐
	*/
	TSoftObjectPtr<USoundBase> GetSceneMusicAsset(bool IsBgMusic, bool& IsFindPlayList);
	/**
	*随机场景音乐播放数组排列
	*
	*@param IsBgMusic 是否背景音乐
	*@param MaxRandomNum 最大随机数
	*
	*@return 无
	*/
	void RandomSceneMusicPlayArray(bool IsBgMusic, int MaxRandomNum);
	
	void PlaySceneMusicByAsset(bool IsPlayBgMusic, USoundBase* SoundAsset, bool IsFindPlayList);

	void ResetSceneMusicData();///<清除背景音乐和战斗音乐的数据

	void CheckSceneMusic();///<背景音乐或战斗音乐组件是否需要播放和停止（由于音效是音效线程，在主线程中获取到的组件数据不同步，在停止音效的时候条件判断不一定正确导致组件没有正常停止）
	/**
	*BlueprintPure，获取CSV_CONFIG_TYPE_AUDIO->AudioConfig数据
	*
	*@param AudioId 音频资源Id
	*
	*@return USoundBase* 音频资源
	*/
	USoundBase* GetAudioAsset(const FString& AudioId, bool IsAsync = false, FStreamableDelegate DelegateToCall = nullptr) const;

	/**
	* 异步加载音频资源
	*@param AudioId 音频资源Id
	*/
	UFUNCTION(BlueprintCallable, Category="AudioManager")
	void AsynLoadAudioAsset(const FString& AudioId, FAsynLoadAudioAssetComplete OnComplete);

	UFUNCTION(BlueprintCallable, Category="AudioManager")
    void PreLoadAudioAsset(const FString& AudioId);
	
	USoundBase* GetEnvironmentMusicAsset(const FString& SpaceId);///<获取环境音效
	void PausedEnvironment(bool bIsPaused = false);///<暂停播放环境音效
	void SetEnvironmentMusicVol(float Vol);///<设置环境音效的音量
	void PausedWeather(bool bIsPaused = false);///<暂停播放天气音效
	void SetWeatherMusicVol(float Vol);///<设置天气音效的音量
	const FString GetCurSpaceId();///<获取当前地图的名字

	void PausedAll3DSound(bool bIsPaused = false);///<暂停播放所有3D声音
	void StopAll3DSound();///<停止播放所有3D声音
	void Remove3DAudioComponent(UAudioComponent* AudioComponent);///<移除单个3D组件
	UCS3AudioComponent* CreateAudioComponent(AActor* TargetActor, FVector Postion = FVector::ZeroVector, USceneComponent* AttachComp = nullptr);

	bool CheckNewAudioComponent(CSTORY_VOICE_TYPE VoiceType); ///<检测当前类型是否是否能创建音效组件
	bool CheckHideVoice(CSTORY_VOICE_TYPE VoiceType);///<检查是否屏蔽该音效类型
	void SetHideVoice(TArray<FString> HideTypes);///<设置屏蔽的音效类型(镜头中屏蔽类型)
	void SetDefualtHideVoiceTypes(TArray<FString> HideTypes);///<CST-5703 在某个区域屏蔽一些类型音效播完镜头后还需要该屏蔽音效的状态
public:
	UPROPERTY()
		UCS3AudioComponent* WeatherSoundComp = nullptr;///< 天气音效资源
protected:
	USoundClass* MasterSoundClass = nullptr;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		UCS3AudioComponent* VoiceComp = nullptr;///< 音频组件 RootComp
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		UCS3AudioComponent* ClientVoiceComp = nullptr;///< 音频组件 ClientVoiceComp
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		UCS3AudioComponent* BgMusicComp = nullptr;///< 音频组件 BgMusicComp
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		UCS3AudioComponent* FightMusicComp = nullptr;///< 音频组件 FightMusicComp
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		UCS3AudioComponent* BgEffectComp = nullptr;///< 音频组件 BgEffectComp
	UPROPERTY()
		UCS3AudioComponent* PreviewSoundComp = nullptr;///< 客户端预览声音资源
	UPROPERTY()
		UCS3AudioComponent* EnvironmentSoundComp = nullptr;///< 环境音效资源	

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		TArray<FVOICE_DATA> VoiceDelayList;///<语音延迟播放链表
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
		TArray<FString> StoryVoiceList;///<语音延迟播放链表

	UPROPERTY(BlueprintReadWrite)
		FString LastVoiceId = TEXT("");///<最后一段语音
	UPROPERTY(BlueprintReadOnly)
		USoundBase* EmptySound = nullptr;///< 空语音资源
	UPROPERTY(BlueprintReadOnly)
		bool bIsPlayRumorVoice = false;///< 是否在播放传话任务语音
	
private:
	UPROPERTY()
		TArray<UAudioComponent*> SkillEffectAudioComponent;	///技能施展音效
	UPROPERTY()
		TArray<UAudioComponent*> Audio3DComponent;	///3D音效
	bool bEnableAudioPlay = true;///<是否可以播放音效	

	float BgMusicFadeTimer = 3.f;///<背景音乐淡出延时
	float FightMusicFadeTimer = 3.f;///<战斗音乐淡出延时
	/// 随机相关，控制随机顺序
	bool bBgMusicRandomFinished = false;///<背景音乐随机相关，控制随机顺序
	bool bFightMusicRandomFinished = false;///<战斗音乐随机相关，控制随机顺序
	int32 CurrentBgMusicIndex = 0;///<当前背景音乐Index
	int32 CurrentFightMusicIndex = 0;///<当前战斗音乐Index
	TArray<int32> BgMusicRandomArray;///<背景音乐随机数组
	TArray<int32> FightMusicRandomArray;///<战斗音乐随机数组
	
	bool bIsPlaySceneMusic = false;
	bool bIsPlayFightMusic = false;
	bool bIsStopSceneMusic = false;
	bool bIsStopFightMusic = false;

	bool bDelayStopMusic = false;	// 解决在异步加载资源中，stop音效失败

	uint8 VoicePriority = 0;		///<语音优先级	
	FTimerHandle DelayTimerHandle;	///<延迟播放使用的Timer

	TArray<int32> HideVoiceTypes;///<声音屏蔽类型（镜头中设置的屏蔽类型）
	TArray<int32> DefualtHideVoiceTypes;///<默认的声音屏蔽类型(CST-5703 在某个区域屏蔽一些类型音效播完镜头后还需要该屏蔽音效的状态)

	FString ClientVoiceId = TEXT("");
	FCClientVoiceComplete OnCClientVoiceComplete;
};
