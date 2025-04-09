// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "RoleStoryInterface.generated.h"

UENUM(BlueprintType)
enum class STORYSTATE : uint8
{
	NONE				= 1	,
	STARTPLAY			= 2	,
	CLIENTSTORYREPLACE	= 3 ,
	CLIENTSTOP			= 4	,
	SERVERSTOP			= 5	,
};

USTRUCT()
struct CHUANGSHI_API FStoryBuffData
{
	GENERATED_USTRUCT_BODY()
public:
	FStoryBuffData() {}
	FStoryBuffData(int32 BuffUID, STORYSTATE StoryState, FString StoryID, int32 LoopNum) 
	{
		this->BuffUID = BuffUID;
		this->StoryState = StoryState;
		this->StoryID = StoryID;
		this->LoopNum = LoopNum;
	}

	int32 BuffUID;								//BuffUID
	STORYSTATE StoryState = STORYSTATE::NONE;
	FString StoryID;
	int32 LoopNum;
};
/**
 * 
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleStoryInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleStoryInterface();
	~URoleStoryInterface();
	static FString GetName() { return TEXT("RoleStoryInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.RoleStoryInterface'"); } //获取蓝图对象路径

	void onNotifyDoStoryEvent(FString CurrPlayId, int32 CurrOrderIndex);
	void RPC_onStopPlayStory(FString CurrPlayId);
	void onNotifyAddEffectList(FString SequenceId,TArray<int32> EffectList);
	void onNotifyRemoveEffectList(FString SequenceId);
	/**
	*Define method
	*过场动画播放接口
	*
	*@param SequenceId 过场动画配置表中的每个过场动画资源对应的唯一ID
	*
	*@return 无
	*/
	void StartBuffPlayStory(const FString& SequenceId, const int32& LoopNum, const int32& BuffUID);

	/**
	*Define method
	*结束当前的过场动画
	*
	*@return 无
	*/
	void StopBuffStory(const int32& BuffUID);

	/**
	*Define method
	*过场动画播放接口
	*
	*@param SequenceId 过场动画配置表中的每个过场动画资源对应的唯一ID
	*
	*@return 无
	*/
	void StartPlayStory(const FString& SequenceId, const int32& LoopNum);

	/**
	*Define method
	*结束当前的过场动画
	*
	*
	*@return 无
	*/
	void StopStory();
public:
	TArray<FStoryBuffData> StoryBuffDatas;
};
