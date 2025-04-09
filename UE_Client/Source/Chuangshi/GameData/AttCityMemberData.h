#pragma once

#include "CoreMinimal.h"
#include "GameDeFine.h"
#include "AttCityMemberData.generated.h"


USTRUCT(BlueprintType)
struct CHUANGSHI_API FAttCityMemberData
{
	GENERATED_USTRUCT_BODY()
		FAttCityMemberData() {};
public:
	/// 名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "Name")
		FString Name;
	/// 归属方
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "BelongSide")
		BELONG_SIDE BelongSide = BELONG_SIDE::BELONG_SIDE_ATTACK;
	/// 击杀数量
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "KillEnemy")
		int32 KillEnemy = 0;
	/// 死亡次数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "Dead")
		int32 Dead = 0;
	/// 助攻次数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "Assist")
		int32 Assists = 0;
	/// 击杀小兵数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "KillSoldier")
		int32 KillSoldier = 0;
	/// 获得总军功
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "TotalExploit")
	int32 TotalExploit = 0;
	/// 己方士兵损失的总数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "OwnerSoldierDeadNum")
	int32 OwnerSoldierDeadNum = 0;
};