// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Task_EnterShow.h"
#include "Util/CS3Debug.h"

EBTNodeResult::Type UMAI_Task_EnterShow::ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
	CS3_Log(TEXT("==============================================>>>UMAI_Task_EnterShow::ExecuteTask"));
	return EBTNodeResult::Succeeded;
}
