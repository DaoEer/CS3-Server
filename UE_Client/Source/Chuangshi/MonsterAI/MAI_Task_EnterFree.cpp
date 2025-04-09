// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Task_EnterFree.h"
#include "Util/CS3Debug.h"

EBTNodeResult::Type UMAI_Task_EnterFree::ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
	CS3_Log(TEXT("==============================================>>>UMAI_Task_EnterFree::ExecuteTask"));
	return EBTNodeResult::Succeeded;
}