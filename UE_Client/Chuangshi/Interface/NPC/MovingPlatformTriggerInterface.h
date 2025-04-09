#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "MovingPlatformTriggerInterface.generated.h"

/*
* 文件名称：MovingPlatformTriggerInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-01-18
*/

/**
*MovingPlatformTrigger接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMovingPlatformTriggerInterface : public UNPCInterface
{
	GENERATED_BODY()
	typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMovingPlatformTriggerInterface();
	~UMovingPlatformTriggerInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MovingPlatformTriggerInterface'"); } //获取蓝图对象路径
	/**
	*Define method
	*BlueprintNativeEvent，往回移动
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MovingPlatformTrigger")
		void OnReadyToMoveBack();

	/**
	*Define method
	*BlueprintNativeEvent，开始移动 
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MovingPlatformTrigger")
		void OnReadyToMove();

	virtual void InitBlueCB() override;
};