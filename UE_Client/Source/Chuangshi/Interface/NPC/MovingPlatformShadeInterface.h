#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "MovingPlatformShadeInterface.generated.h"

/*
* 文件名称：MovingPlatformShadeInterface.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2018-02-06
*/

/**
*UMovingPlatformShadeInterface接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMovingPlatformShadeInterface : public UNPCInterface
{
	GENERATED_BODY()
	typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMovingPlatformShadeInterface() {};
	~UMovingPlatformShadeInterface() {};
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MovingPlatformShadeInterface'"); } //获取蓝图对象路径
		
	UFUNCTION(BlueprintCallable, Category = "MovingPlatformShadeInterface")
		void OnRep_shadeTime();
};