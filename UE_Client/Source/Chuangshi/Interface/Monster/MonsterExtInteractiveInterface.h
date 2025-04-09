#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtInteractiveInterface.generated.h"

/*
* 文件名称：MonsterExtInteractiveInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-05-08
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtInteractiveInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtInteractiveInterface();
	~UMonsterExtInteractiveInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtInteractiveInterface'"); } //获取蓝图对象路径

	/**
	*服务器通知添加交互陷阱
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterExtInteractiveInterface")
	void AddInitiativeTrap();

	void OnPlayerBeginOverlap();

	void OnPlayerEndOverlap();

	virtual void InitBlueCB() override;

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterExtInteractiveInterface")
	void RPC_InteractiveWith();

private:
	float Radius = 5.0f;
	UBaseShape* pInitiativeShape = nullptr;
};