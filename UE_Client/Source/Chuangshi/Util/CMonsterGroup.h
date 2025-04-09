#pragma once
#include<list>
#include<map>
#include <string>
#include "Runtime\Core\Public\Containers\UnrealString.h"
#include "Runtime\Core\Public\Containers\Map.h"
#include "Runtime\Core\Public\Containers\Array.h"
#include "Math\Rotator.h"
#include "Math\Vector.h"



/*
* 文件名称：CMonsterGroup.h
* 功能说明：集群CMonster
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-11-15
*/

class CMonsterGroup {
public:
	void AddMember(FString ScriptID, int32 MemberID);
	void RemoveMember(FString ScriptID, int32 MemberID);
	void CmdFollow(int32 FollowID);
	void CmdAttack();
	void CmdUseSkill();
	void CmdArrayRectangle(FVector Location, FRotator Rotation);
	void CmdArrayCircle(); 

public:
	TMap<FString, TArray<int32>> GroupData;
	int32 OwnerID;
};




