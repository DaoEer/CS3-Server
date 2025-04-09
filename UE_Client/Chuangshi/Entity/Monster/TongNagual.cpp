// Fill out your copyright notice in the Description page of Project Settings.


#include "TongNagual.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/TongNagualInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(TongNagual, Supper)
DEF_INTERFACE( UTongNagualInterface)
DEF_INTERFACE_END()
	
KBE_BEGIN_ENTITY_METHOD_MAP(TongNagual, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(TongNagual, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


TongNagual::TongNagual()
{
}

TongNagual::~TongNagual()
{
}

UClass* TongNagual::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_TongNagual")); 
}


CONTROL_COMPILE_OPTIMIZE_END
