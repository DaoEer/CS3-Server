

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtCanPushInterface.generated.h"


UCLASS()
class CHUANGSHI_API UMonsterExtCanPushInterface : public UMonsterInterface
{

	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	UMonsterExtCanPushInterface();
	~UMonsterExtCanPushInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtCanPushInterface'"); } //获取蓝图对象路径

	//获取客户端导航点
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|UMonsterExtDemonGuardInterface")
		void CLIENT_OnRoleNearbyMonster(int32 MonsterID);

	/*玩家推完*/
	void RPC_OnRolePushComplete();

	virtual void InitBlueCB() override;
private:
	FTimerHandle KeyDownTimerEventHandle;///<检测当前按键是否有超过规定时间定时器
};
