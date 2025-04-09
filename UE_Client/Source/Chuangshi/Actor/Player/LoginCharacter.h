#pragma once

#include "Actor/GameCharacter.h"
#include "LoginCharacter.generated.h"

/*
* 文件名称：LoginCharacter.h
* 功能说明：登录流程中的Character
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-05-15
*/

/*
* 登录Character基类
*/

class ACS3LevelScriptActor;
UCLASS(BlueprintType)
class CHUANGSHI_API ALoginCharacter :public AGameCharacter
{
	GENERATED_BODY()
public:
	ALoginCharacter();///<构造函数
	virtual void BeginPlay()override;
	virtual void BeginDestroy()override;
	virtual void OnCreateApperanceOver() override;
	virtual void OnChangePartOver() override;

	void SetRoleLevelActor(ACS3LevelScriptActor *InRoleLevelActor);
	UFUNCTION(BlueprintCallable, Category = "LoginCharacter")
		void SetIsSelect() { IsSelect = true; };

	/**
	*通知登录排队信息
	*
	*@param rank 排名队列中每次
	*@param time 平均登陆时间
	*@param count 排队总人数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "LoginCharacter")
		void OnReceiveWattingInfo(const int32& rank, const float& time, const int32& count);

	/**
	*播放或停止[选择角色界面]的角色动作
	*
	*@param IsStand 是否恢复站立（是:停止动作; 否:进入IsSelect判断）
	*@param IsSelect 是否为选中（是:停止动作; 否:播放动作）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginCharacter")
		void PlayLoginSelectAction(bool IsStand = false, bool IsSelect = false);


	/**
	*播放或停止[创建角色界面]的角色动作
	*
	*@param IsStand 是否恢复站立（是:停止动作; 否:播放动作）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "LoginCharacter")
		void PlayLoginCreatAction(bool IsStand = false);

	/**
	*通知取消登录排队
	*
	*@param isInQueue,是否还在排队队列中(如果还在，意味着取消失败)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "LoginCharacter")
		void OnCancelLoginQueue(const int32& isInQueue);

	/**
	* 设置模型高亮
	*
	*@param isInQueue,是否还在排队队列中(如果还在，意味着取消失败)
	*
	*@return 无
	*/
	void SetModelLight(bool IsLight);

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent

public:
	UPROPERTY(BlueprintReadOnly)
	int32 CampID;///<角色阵营
	
	UPROPERTY(BlueprintReadOnly)
	int32 Index;///<角色ID, index索引

	UPROPERTY(BlueprintReadOnly)
	FString PlayerDbid;///<角色Dbid

	int32 GenderID;///角色性别
	uint64 OfflineTime;///<角色上次离线时间(服务器存的是UTC世界时间)
	UPROPERTY(BlueprintReadOnly)
	TArray<FString> Bonedatas;
	UPROPERTY(BlueprintReadOnly)
	TArray<FString> BoneNames;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsSelect;///<是否被选中
private:
	ACS3LevelScriptActor *RoleLevelActor;

	
};