#pragma once
#include "Util/CS3Debug.h"
#include "CS3Base/CS3EntityInterface.h"
#include "RoleGameTimeInterface.generated.h"

/*
* 文件名称：RoleGameTimeInterface.h
* 功能说明：游戏时长付费接口
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2020-8-12
*/
/**
 * 玩家游戏时长收费接口
 */

UCLASS(BlueprintType)
class CHUANGSHI_API URoleGameTimeInterface: public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	URoleGameTimeInterface();
	~URoleGameTimeInterface();

	static FString GetName() { return TEXT("RoleGameTimeInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleGameTimeInterface.BP_RoleGameTimeInterface_C'"); } //获取蓝图对象路径

public:
	void OnGameTimeBalanceCountDown(const int32& TimeBalance);
	void ShowStartBillingWnd(const int32& Level, const int32& CountDownTime);
	void HideStartBillingWnd();

};

