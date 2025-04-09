// Fill out your copyright notice in the Description page of Project Settings.


#include "QuestQiYuan.h"
#include "Util/ConvertUtil.h"
#include "JsonFieldData.h"

void UQuestQiYuan::InitDatas(const FString JsonStr)
{
	Super::InitDatas(JsonStr);

	//动态数据从服务器传来的JsonStr里面获取
	auto JsonData = UJsonFieldData::Create(this)->FromString(JsonStr)->GetObject(TEXT("ROOT"));

	//建造洞府的任务特殊处理一下，需要显示倒计时
	mCountDown = JsonData->GetString(TEXT("countDown"));
	isShowTime = FSTRING_TO_INT(JsonData->GetString(TEXT("isShowTime")));
}