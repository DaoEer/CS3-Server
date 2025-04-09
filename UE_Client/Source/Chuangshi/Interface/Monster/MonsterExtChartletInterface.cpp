// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtChartletInterface.h"
#include "Util/CustomEffect/DecalEffect.h"
#include "Actor/Particle/DecalEffectEmitter.h"
#include "Actor/Monster/MonsterExtChartletCharacter.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtChartletInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtChartletInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtChartletInterface::UMonsterExtChartletInterface()
{
}

UMonsterExtChartletInterface::~UMonsterExtChartletInterface()
{
}

void UMonsterExtChartletInterface::onDisappearChartlet_Implementation(const int32& type)
{
	AMonsterExtChartletCharacter* monsterextchartletCH = Cast<AMonsterExtChartletCharacter>(GetActor());
	monsterextchartletCH->onDisappearChartlet(type);
}

void UMonsterExtChartletInterface::onDisplayChartlet_Implementation()
{

	AMonsterExtChartletCharacter* monsterextchartletCH = Cast<AMonsterExtChartletCharacter>(GetActor());
	monsterextchartletCH->onDisplayChartlet();
	
}

void UMonsterExtChartletInterface::InitBlueCB()
{
	ArrBlueFunc.Add("onDisappearChartlet");
	ArrBlueFunc.Add("onDisplayChartlet");
	Supper::InitBlueCB();
}

