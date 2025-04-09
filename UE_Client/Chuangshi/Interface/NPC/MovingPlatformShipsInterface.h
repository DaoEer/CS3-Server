#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "MovingPlatformShipsInterface.generated.h"

/*
* 文件名称：MovingPlatformShipsInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-10-08
*/

/*
仙舟渡劫 -- 移动平台接口
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMovingPlatformShipsInterface : public UNPCInterface
{
	GENERATED_BODY()
		typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMovingPlatformShipsInterface();
	~UMovingPlatformShipsInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MovingPlatformShipsInterface'"); } //获取蓝图对象路径
};

