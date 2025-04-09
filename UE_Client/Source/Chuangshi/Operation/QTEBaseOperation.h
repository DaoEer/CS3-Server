#pragma once
#include "GameData/CS3Object.h"
#include "QTEBaseOperation.generated.h"

/*
* 文件名称：QTEBaseOperation.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2018-07-17
*/



UCLASS(Abstract)
class CHUANGSHI_API UQTEBaseOperation : public UCS3Object
{
	GENERATED_BODY()

public:
	void Init();///<初始化
	virtual float ExecuteOperation();///<执行操作,是否完成操作

	UFUNCTION(BlueprintImplementableEvent)
		void BP_ExecuteOperation();///<蓝图执行操作
protected:
	/// 是否能执行
	UFUNCTION(BlueprintCallable)
		virtual bool IsCanExecuteOperation();

	/// 是否能执行蓝图重载
	UFUNCTION(BlueprintNativeEvent)
		bool BP_IsCanExecuteOperation();

public:
	float Value = 0.0f;
};



UCLASS()
class CHUANGSHI_API UMouseQTEOperation : public UQTEBaseOperation
{
	GENERATED_BODY()

public:	
	virtual float ExecuteOperation();

private: 	
	float CurMousePostion = 0.0f;
	float OldMousePostion = 0.0f;
	float L_Postion = 0.0f;
	float R_Postion = 0.0f;
};
