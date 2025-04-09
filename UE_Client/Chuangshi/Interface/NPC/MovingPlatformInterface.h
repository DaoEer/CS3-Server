#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "MovingPlatformInterface.generated.h"

/*
* 文件名称：MovingPlatformInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

/**
*NPC接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMovingPlatformInterface: public UNPCInterface
{
	GENERATED_BODY()
	typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMovingPlatformInterface();
	~UMovingPlatformInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MovingPlatformInterface'"); } //获取蓝图对象路径

};