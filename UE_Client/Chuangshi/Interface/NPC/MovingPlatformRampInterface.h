#pragma once
#include "Interface/NPC/MovingPlatformShadeInterface.h"
#include "MovingPlatformRampInterface.generated.h"

/*
* 文件名称：MovingPlatformRampInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-05-30
*/

/**
*MovingPlatformRampInterface接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMovingPlatformRampInterface : public UMovingPlatformShadeInterface
{
	GENERATED_BODY()
	typedef UMovingPlatformShadeInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMovingPlatformRampInterface();
	~UMovingPlatformRampInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MovingPlatformRampInterface'"); } //获取蓝图对象路径

};