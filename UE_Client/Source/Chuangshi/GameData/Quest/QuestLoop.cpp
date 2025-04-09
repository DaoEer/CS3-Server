// Fill out your copyright notice in the Description page of Project Settings.

#include "QuestLoop.h"
#include "JsonFieldData.h"
#include "Util/ConvertUtil.h"



void UQuestLoop::InitDatas(const FString JsonStr)
{
	Supper::InitDatas(JsonStr);
	auto JsonData = UJsonFieldData::Create(this)->FromString(JsonStr)->GetObject(TEXT("ROOT"));
	loopQuestNum = FSTRING_TO_FLOAT(JsonData->GetString((TEXT("loopQuestNum"))));
}

int32 UQuestLoop::GetLoopQuestNum()
{
	return loopQuestNum;
}
