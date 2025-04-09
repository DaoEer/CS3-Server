#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "MovingPlatformRotatorInterface.generated.h"

/*
* 文件名称：MovingPlatformRotatorInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-10-15
*/

/**
*MovingPlatformRotatorInterface接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMovingPlatformRotatorInterface : public UNPCInterface
{
	GENERATED_BODY()
	typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMovingPlatformRotatorInterface();
	~UMovingPlatformRotatorInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MovingPlatformRotatorInterface'"); } //获取蓝图对象路径

	/**
	*Define method
	*BlueprintNativeEvent，通知开始旋转
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MovingPlatformRotator")
		void notifyClientStartRotat(FVector angle, float moveSpeed, int isContinuousMove);

	virtual void InitBlueCB() override;
};