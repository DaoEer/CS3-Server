#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "MovingPlatformLotusInterface.generated.h"

/*
* 文件名称：MovingPlatformLotusInterface.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-03-29
*/

/*
莲叶移动平台接口
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMovingPlatformLotusInterface : public UNPCInterface
{
	GENERATED_BODY()
	typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMovingPlatformLotusInterface();
	~UMovingPlatformLotusInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MovingPlatformLotusInterface'"); } //获取蓝图对象路径

};

