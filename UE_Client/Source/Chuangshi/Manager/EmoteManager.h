// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/EmoteData.h"
#include "GameData/TextEmoteData.h"
#include "EmoteManager.generated.h"

/*
* 文件名称：EmoteManager.h
* 功能说明：
* 文件作者：fangpengjun
* 目前维护：fangpengjun
* 创建时间：2017-07-22
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UEmoteManager : public UCS3Object
{
	GENERATED_BODY()
public:
	UEmoteManager();
	~UEmoteManager();

	static UEmoteManager* GetInstance();
	/*初始化
	*/
	void Init();

	/*获取指定表情数据
	*
	*@param Sign 表情符
	*
	*@return FEmoteData	
	*/
	UFUNCTION(BlueprintCallable, Category = "EmoteManager")
		struct FEMOTE_DATA GetDefaultEmoteDataBySign(FString Sign, bool& IsSuccess);

	UFUNCTION(BlueprintCallable, Category = "EmoteManager")
		struct FEMOTE_DATA GetDefaultEmoteDataByName(FString Name, bool& IsSuccess);

	UFUNCTION(BlueprintCallable, Category = "EmoteManager")
		struct FTEXT_EMOTE_DATA GetTextEmoteDataBySign(FString Sign);

	/*恢复指定表情数据为系统默认
	*@param Sign 表情符
	*
	*@return null
	*/
	UFUNCTION(BlueprintCallable , Category = "EmoteManager")
		void RestoreEmoteData(FString Sign);


	/*新建语言类表情
	*@param Sign 表情符号
	*@param Name 表情名称
	*@param NoTargetDes 没有目标时的描述
	*@param HasTargetDes 有目标时的描述
	*@return bool
	*/
	UFUNCTION(BlueprintCallable, Category = "EmoteManager")
		bool CreateNewTextEmoteData(const FString &Sign, const FString &Name, const FString &NoTargetDes, const FString &HasTargetDes);

	/*删除指定表情数据
	*@param Sign 表情符
	*
	*@return null
	*/
	UFUNCTION(BlueprintCallable, Category = "EmoteManager")
		void RemoveTextEmoteData(FString Sign);

	/*更改指定字符表情数据
	*@param Sign 表情符
	*@param Name 表情名称
	*@param NoTargetDes 没有目标时的描述
	*@param HasTargetDes 有目标时的描述
	*@return null
	*/
	UFUNCTION(BlueprintCallable, Category = "EmoteManager")
		void ChangeTextEmoteData(const FString&Sign, const FString &Name, const FString &NoTargetDes, const FString &HasTargetDes);


	/*新建表情蓝图回调
	*@param Sign 表情符
	*
	*@return null
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "EmoteManager")
		void OnCreateTextEmoteDataBP(const FString& Sign);

	/*删除表情蓝图回调
	*@param Sign 表情符
	*
	*@return null
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "EmoteManager")
		void OnRemoveTextEmoteDataBP( const FString& Sign);

	/*恢复表情蓝图回调
	*@param Sign 表情符
	*
	*@return null
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "EmoteManager")
		void OnRestoreTextEmoteDataBP(const FString& Sign);

	/*恢复表情蓝图回调
	*@param Sign 表情符
	*
	*@return null
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "EmoteManager")
		void OnChangeTextEmoteDataBP(const FString& Sign);


	/**
	*BlueprintCallable,表情字符串替换为富文本，比如：左边内容[#Name]右边内容 替换为 左边内容@I{p=Sign} 右边内容
	*
	*@param	replaceString 原字符串
	*@param	ColorStr RGBA值
	*
	*@return FString 替换后的字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "EmoteManager")
		FString GetFormatEmoteStr(const FString& replaceString);

	/**
	*BlueprintCallable,通过表情名称获得表情富文本
	*
	*@param	EmoteName 表情名称
	*
	*@return FString 表情富文本
	*/
	UFUNCTION(BlueprintCallable, Category = "EmoteManager")
		FString GetEmoteStr(const FString& EmoteName, bool& IsSuccess);

protected:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "EmoteManager")
		TMap<FString, FEMOTE_DATA> DefaultEmotes;	///<默认表情数据

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "EmoteManager")
		TMap<FString, FTEXT_EMOTE_DATA> CustomTextEmotes;	///<自定义表情数据


private:
	void InitDefaultEmoteData();
	void InitCustomTextEmoteData();

	//static UEmoteManager* Instance;
};
