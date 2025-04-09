// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleCompeteInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleCompeteInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleCompeteInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleCompeteInterface::URoleCompeteInterface()
{
}

URoleCompeteInterface::~URoleCompeteInterface()
{
}



void URoleCompeteInterface::CLIENT_RoleCompeteBeInvited_Implementation(const int32& inviterID)
{

}

void URoleCompeteInterface::CLIENT_RoleCompeteStart_Implementation(const int32& targetID)
{
	CompeteTargetID = targetID;
}

void URoleCompeteInterface::CLIENT_OnRoleCompeteEnd_Implementation()
{
	CompeteTargetID = 0;
}


void URoleCompeteInterface::CLIENT_ShowCompeteCountDown_Implementation(const int32& type, const int32& time)
{
	
}

void URoleCompeteInterface::CLIENT_CloseCompeteCountDown_Implementation()
{

}

void URoleCompeteInterface::CLIENT_OnDoubleHit_Implementation(const int32& DoubleHitTimes)
{

}


void URoleCompeteInterface::RPC_CELL_requestRoleCompete(const int32& INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleCompeteInterface::RPC_CELL_requestRoleCompete : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);

	entity->CellCall(TEXT("CELL_requestRoleCompete"), args);
}


void URoleCompeteInterface::RPC_CELL_requestAgreeRoleCompete(const int32& INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleCompeteInterface::RPC_CELL_requestAgreeRoleCompete : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);

	entity->CellCall(TEXT("CELL_requestAgreeRoleCompete"), args);
}

void URoleCompeteInterface::RPC_CELL_requestRefuseRoleCompete(const int32& INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleCompeteInterface::RPC_CELL_requestRefuseRoleCompete : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);

	entity->CellCall(TEXT("CELL_requestRefuseRoleCompete"), args);
}


void URoleCompeteInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_RoleCompeteBeInvited");
	ArrBlueFunc.Add("CLIENT_RoleCompeteStart");
	ArrBlueFunc.Add("CLIENT_OnRoleCompeteEnd");
	ArrBlueFunc.Add("CLIENT_ShowCompeteCountDown");
	ArrBlueFunc.Add("CLIENT_CloseCompeteCountDown");
	ArrBlueFunc.Add("CLIENT_OnDoubleHit");
	Supper::InitBlueCB();
}
