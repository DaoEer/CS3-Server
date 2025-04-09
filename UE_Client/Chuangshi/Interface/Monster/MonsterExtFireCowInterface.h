

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtFireCowInterface.generated.h"


UCLASS()
class CHUANGSHI_API UMonsterExtFireCowInterface : public UMonsterInterface
{

	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	UMonsterExtFireCowInterface();
	~UMonsterExtFireCowInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtFireCowInterface'"); } //获取蓝图对象路径

};
