#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtArmorLockInterface.generated.h"

/*
* 文件名称：MonsterExtArmorLockInterface.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-10-19
*/
UCLASS(BlueprintType)
class UMonsterExtArmorLockInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtArmorLockInterface();
	virtual ~UMonsterExtArmorLockInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtArmorLockInterface'"); } //获取蓝图对象路径

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterExtArmorLockInterface")
		void EnterArmorLock();

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterExtArmorLockInterface")
		void ExitArmorLock(const float OutTime);

	void MaterialTimer();

	virtual void InitBlueCB() override;

	float DelayTime;

	float CoverParameter;

private:
	FTimerHandle CoverEventHandle;///<检测QTE事件定时器
};

