// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "../MediaAssets/Public/MediaPlayer.h"
#include "GameData/MediaPlayerData.h"
#include "MediaPlayerManager.generated.h"

DECLARE_MULTICAST_DELEGATE(FLoadMediaOverDelegate);
DECLARE_MULTICAST_DELEGATE(FOnMediaEndReachedDelegate);
DECLARE_MULTICAST_DELEGATE(FOnMediaOpenedDelegate);

/*
* 文件名称：MediaPlayerManager.h
* 功能说明：媒体管理类
* 文件作者：huting
* 目前维护：huting
* 创建时间：2018-9-18
*/
UCLASS()
class CHUANGSHI_API UMediaPlayerManager : public UCS3Object
{
	GENERATED_BODY()
public:
	static UMediaPlayerManager* GetInstance();

	UFUNCTION(BlueprintNativeEvent, Category = "Media|MediaPlayer")
		void OnInitMediaPlayer();///<BlueprintNativeEvent,初始化MediaPlayer
	/**
	* Close the currently open media, if any.
	*
	* @see OnMediaClosed, OpenPlaylist, OpenPlaylistIndex, OpenSource, OpenUrl, Pause, Play
	*/
	UFUNCTION(BlueprintCallable, Category = "Media|MediaPlayer")
		void Close(bool bIsForcedClose = false);
	/**
	* Pauses media playback.
	*
	* This is the same as setting the playback rate to 0.0.
	*
	* @return true if playback is being paused, false otherwise.
	* @see CanPause, Close, Next, Play, Previous, Rewind, Seek
	*/
	UFUNCTION(BlueprintCallable, Category = "Media|MediaPlayer")
		bool Pause();

	/**
	* Starts media playback.播放
	*
	* This is the same as setting the playback rate to 1.0.
	*
	* @return true if playback is starting, false otherwise.
	* @see CanPlay, GetRate, Next, Pause, Previous, SetRate
	*/
	UFUNCTION(BlueprintCallable, Category = "Media|MediaPlayer")
		bool Play();

	UFUNCTION(BlueprintCallable, Category = "Media|MediaPlayer")
		bool Rewind();///<倒回功能回退到初始位置
	/**
	 * Changes the media's playback rate.快进（+）后退（-）
	 *
	 * @param Rate The playback rate to set.
	 * @return true on success, false otherwise.
	 * @see GetRate, SupportsRate
	 */
	UFUNCTION(BlueprintCallable, Category="Media|MediaPlayer")
	bool SetRate(float Rate);
	/**
	* Open the specified media source.当前媒体是打开就播放
	*
	* A return value of true indicates that the player will attempt to open
	* the media, but it may fail to do so later for other reasons, i.e. if
	* a connection to the media server timed out. Use the OnMediaOpened and
	* OnMediaOpenFailed delegates to detect if and when the media is ready!
	*
	* @param MediaSource The media source to open.
	* @return true if the source will be opened, false otherwise.
	* @see Close, OpenFile, OpenPlaylist, OpenPlaylistIndex, OpenUrl, Reopen
	*/
	UFUNCTION(BlueprintCallable, Category = "Media|MediaPlayer")
		bool OpenSource(UMediaSource* MediaSource);

	///<播放媒体包括一些操作如关闭界面、屏蔽输入、隐藏鼠标 游戏当中一般播放媒体的接口 Play()方法只是播放不进行额外操作暂停了之后在播放使用Play()
	UFUNCTION(BlueprintCallable, Category = "Media|MediaPlayer")
		void PlayMedia(FString MediaPlayerId);

	UFUNCTION()
		void OnEndReached();///<媒体播放完的事件回调方法	
	UFUNCTION()
		void OnMediaClosed();///<媒体关闭事件回调方法	
	UFUNCTION()
		void OnMediaOpened(FString OpenedUrl);///<媒体打开事件回调方法
	UFUNCTION()
		void OnMediaOpenFailed(FString FailedUrl);///<媒体打开失败事件回调方法

	int PreLoadMediaAsset(const FLoadMediaOverDelegate& InLoadMediaOverDelegate = FLoadMediaOverDelegate());
	void PreLoadMediaAssetByGameStatus();///<在玩家还没有进入世界之前加载媒体资源，如在登录界面时需要预加载CG、在选择角色界面预加载CG。
	void PreLoadAllMediaAsset();///<预加载所有的媒体资源
	void ClearMediaAsset();///<切换关卡时清除预加载的媒体资源

	bool IsNeedHideUI();///<在媒体播放时是否需要隐藏界面

	UFUNCTION(BlueprintCallable, Category = "Media|MediaPlayer")
		void GetSkipTimeData(float& HoldTime, float& CurTime, float& SkipTime,bool& bIsCanSkip,bool& bIsShowUI);///<获取当前可跳过的时长

	UFUNCTION(BlueprintImplementableEvent, Category = "Media|MediaPlayer")
	void OnShowMediaSkipTime_BP();

	bool IsStopLoadingLevel();
	bool IsStopInWorldOver();

	bool IsCanStopByMinimumTime() { return bIsCanStopByMinimumTime; };

	UFUNCTION(BlueprintCallable, Category = "Media|MediaPlayer")
		bool IsPlaying();///<当前是否正在播放中

private:
	void DelayRemoveCGWindow();///<关闭CG界面
	void OnEnableInput(bool bIsEnable);///<玩家输入的设置处理
	/**
	*获取媒体数据相关
	*
	*@param MediaPlayerId 媒体ID
	*
	*@return FSTORY_DATA* 媒体数据
	*/
	const FMEDIA_PLAYER_DATA* GetMediaPlayerData(const FString& MediaPlayerId);

	void OnMediaStoped();///<媒体结束或者关闭事件后需要处理的逻辑
	void StartPlayMedia(TSoftObjectPtr<UMediaSource> MediaAss, const FString& MediaId);///<获取到资源开始播放媒体
	void GetMediaSource(TSoftObjectPtr<UMediaSource> MediaAss, const FString& MediaId);///<获取要播放的媒体资源

	void LoadMediaAssetEnd(TSoftObjectPtr<UMediaSource> MediaAss = nullptr);///<加载单个资源结束
	void LoadMediaAsset(FString MediaID, TSoftObjectPtr<UMediaSource> MediaAss);///<加载单个资源

	void ClearMediaEvent();///<清除媒体事件
	void ResetMediaData();///<重置媒体数据 除资源之外

	UFUNCTION()
		void InWorldLoadingOverEvent(); 

	void onNotifyServerEvent(FString Params);
public:
	UPROPERTY(BlueprintReadWrite)
		UMediaPlayer*  MediaPlayer;///<媒体播放器
	UPROPERTY(BlueprintReadWrite)
		FString  CurMediaPlayerId = TEXT("");///<当前媒体播放ID
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, UMediaSource*>MediaAssList;///<关卡媒体资源列表
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, TSoftObjectPtr<UMediaSource>>MediaAss;///<媒体加载资源
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, TSoftObjectPtr<UMediaSource>>AllMediaAss;///<当前地图所有需要预加载媒体资源
	FOnMediaOpenedDelegate OnMediaOpenedDelegate;///<媒体打开成功播放事件
	FOnMediaEndReachedDelegate  OnMediaEndReachedDelegate;///<媒体播放完成事件
private:
	FLoadMediaOverDelegate LoadMediaOverDelegate;///<媒体加载事件委托
	FTimerHandle DelayLoadAllMediaHandle;///<加载所有媒体资源定时器
	FTimerHandle MinimumTimeHandle;///<最小时间定时器
	bool bIsCanStopByMinimumTime = true;///<是否达到最小时间停止播放
	bool bIsStopByLoadingOver = true; ///<游戏状态变为世界状态加载结束
};
