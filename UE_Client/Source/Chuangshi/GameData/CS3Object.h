// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Object.h"
#include "CoreMinimal.h"
#include "Misc/Variant.h"
#include "CS3Object.generated.h"

/**
* 文件名称：CS3Object.h
* 功能说明：
* 文件作者：zhangyuxing
* 目前维护：wuxiaoou
* 创建时间：2017-04-01
*/

/**
 * 基础对象类
 */
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UCS3Object : public UObject
{
	GENERATED_BODY()
public:
	virtual void BeginDestroy() override;

	virtual UWorld* GetWorld() const override;///<获取世界（ 世界包含了所加载的一系列关卡，它处理关卡的动态载入及动态Actor的生成(创建)）

	/**
	*蓝图可调用，通过Key值获取String类型的属性
	*
	*@param name Key值得名字
	*
	*@return FString Key的属性值
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		const FString GetFStringPropertyByKey(const FString& name);

	/**
	*Define method
	*蓝图可调用，设置String类型的属性
	*
	*@param name Key的名字
	*@param value Key的值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		void SetFStringPropertyByKey(const FString& name, const FString& value);

	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		void CLIENT_SetFStringPropertyByKey(const FString& name, const FString& value);

	/**
	*蓝图可调用，通过Key值获取Float类型的属性
	*
	*@param name Key的名字
	*
	*@return float Key的属性值
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		const float GetFloatPropertyByKey(const FString& name);

	/**
	*Define method
	*蓝图可调用，设置Float类型的属性
	*
	*@param name Key的名字
	*@param value Key的值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		void SetFloatPropertyByKey(const FString& name, float value);

	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		void CLIENT_SetFloatPropertyByKey(const FString& name, float value);

	/**
	*蓝图可调用，通过Key值获取Int类型的属性
	*
	*@param name Key的名字
	*
	*@return Int Key的属性值
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		const int GetIntPropertyByKey(const FString& name);

	/**
	*Define method
	*蓝图可调用，设置Int类型的属性
	*
	*@param name Key的名字
	*@param value Key的值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		void SetIntPropertyByKey(const FString &name, int32 value);

	/**
	*Define method
	*蓝图可调用，设置Int类型的属性
	*
	*@param name Key的名字
	*@param value Key的值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		void CLIENT_SetIntPropertyByKey(const FString &name, int32 value);

	/**
	*蓝图可调用，通过Key值获取Int类型的属性
	*
	*@param name Key的名字
	*
	*@return Int Key的属性值
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		const int GetBoolPropertyByKey(const FString& name);
	/**
	*Define method
	*蓝图可调用，设置bool类型的属性
	*
	*@param name Key的名字
	*@param value Key的值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		void SetBoolPropertyByKey(const FString& name, bool value);

	UFUNCTION(BlueprintCallable, Category = "CS3Object")
		void CLIENT_SetBoolPropertyByKey(const FString& name, uint8 value);

	/**
	*获取到参数
	*
	*@param val ，参数引用（FVariant &）
	*
	*@return FString
	*/
	static const FString GetArgumentsString(const FVariant &val);

	//TArray<FVariant> 参数 转换成 CallFunctionByNameWithArguments 的参数
	static void Parameter_FVariantToFString(const TArray<FVariant> &InParameter, FString &OutParameter);

	/**
	*远程调用方法
	*
	*@param name 方法名
	*@param args 参数数组
	*
	*@return 无
	*/
	void CallFuncToBlue(const FString &name, const FString &Parameter);
	void CallFuncToBlueArgs( const FString &name, const TArray<FVariant> &args );

	void CallPropertyChangeToBlue(const FString &name, const FVariant &newVal, const FVariant &oldVal);
};
