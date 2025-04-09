// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "RoleTitleInterface.generated.h"

/*
* 文件名称：RoleTitleInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

/**
*	称号数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTITLE_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TitleID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float LimitTime;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString AttackProperties;
	bool operator ==(const FTITLE_DATA& other)
	{
		if (other.TitleID == TitleID)
		{
			return true;
		}
		else
		{
			return false;
		}
	}

};

/**
 * 
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleTitleInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleTitleInterface();
	~URoleTitleInterface();
	static FString GetName() { return TEXT("RoleTitleInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleTitleInterface.BP_RoleTitleInterface_C'"); } //获取蓝图对象路径

	virtual void onLeaveWorld() override;

	virtual void InitBlueCB() override;

	//选择一个称号
	UFUNCTION(BlueprintCallable, Category = "Client | Role")
	void SelectTitle(int32 TitleID);
	
	//服务器添加称号
	UFUNCTION(BlueprintCallable, Category = "Client | Role")
	void CLIENT_OnTitleAdded(int32 TitleID);

	//服务器移除称号
	UFUNCTION(BlueprintCallable, Category = "Client | Role")
	void CLIENT_OnTitleRemoved(int32 TitleID);

	//服务器发送称号数据
	UFUNCTION(BlueprintCallable, Category = "Client | Role")
	void CLIENT_OnSetTitleData(int32 TitleID, FString AttackPropertiesStr, float LimitTime);

	//服务器发送可获得称号数据
	UFUNCTION(BlueprintCallable, Category = "Client | Role")
	void CLIENT_OnSetAvailableTitleData(int32 TitleID, FString AttackPropertiesStr, float LimitTime);

	//解析服务器发送的称号属性数据
	UFUNCTION(BlueprintCallable, Category = "Client | Role")
	FString ParseAttackPropertiesStr(FString AttackPropertiesStr);


	UFUNCTION(BlueprintCallable, Category = "Client | Role")
	FTITLE_DATA  GetTitleDataByID(int32 TitleID);

	UFUNCTION(BlueprintCallable, Category = "Client | Role")
	FTITLE_DATA  GetAvailableTitleDataByID(int32 TitleID);

	//是否已拥有
	UFUNCTION(BlueprintCallable, Category = "Client | Role")
	bool IsOwnTitle(int32 TitleID);

	/**
	*添加称号
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Client | Role")
		void OnTitleAddedCB(int32 TitleID);

	/**
	*移除称号
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Client | Role")
		void OnTitleRemovedCB(int32 TitleID);

	//通知蓝图倒计时
	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable, Category = "Client | Role")
		void OnStartOwnTime();


	UFUNCTION(BlueprintCallable, Category = "Title | Describe")
	FString ParsePropertiesStr(const FString& propstr, const FString& propcolor);

	FString ParsePropertiesStr_v(const FString& propstr, const FString& propcolor);

	/**
	*BlueprintCallable，获取对propstr和propvalue封装后的值颜色转换成propcolor之后的描述
	*
	*@param propstr 参数
	*@param propvalue 参数值
	*@param propcolor 参数颜色
	*
	*@return FString 对propstr和propvalue封装后的值颜色转换成propcolor之后的描述
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
	FString GetPropertyStr(const FString& propid, const FString& propvalue, const FString& propcolor);

	/**
	*virtual，获取对propstr和propvalue封装后的值颜色转换成propcolor之后的描述
	*
	*@param propstr 参数
	*@param propvalue 参数值
	*@param propcolor 参数颜色
	*
	*@return FString 对propstr和propvalue封装后的值颜色转换成propcolor之后的描述
	*/
	FString GetPropertyStr_v(const FString& propid, const FString& propvalue, const FString& propcolor);

	/**
	*BlueprintCallable，按插件格式化字符串
	*
	*@param inputstr 要格式化的字符串
	*@param colorstr 字体颜色
	*@param shadowcolor 字体阴影颜色
	*@param shadowoffset 字体阴影像素
	*
	*@return FString 按插件格式化后的字符串
	*/
	FString StrToColorStr(const FString& inputstr, const FString& colorstr, const FString& shadowcolor, const FString& shadowoffset);

public:
	//玩家已拥有的称号数据
	UPROPERTY(BlueprintReadWrite)
	TArray<FTITLE_DATA> TitleData;

	//玩家可获得的称号数据
	UPROPERTY(BlueprintReadWrite)
	TArray<FTITLE_DATA> AvailableTitleData;

protected:
	UPROPERTY()
		FTimerHandle OwnTimerHandle;///<持续时间计时器

};