// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleTeleportInterface.h"

#include "Json.h"
#include "JsonFieldData.h"

#include "KBEngine.h"

#include "GameData/NPCPointDatas.h"
#include "GameData/TeleportPointData.h"
#include "GameData/Item/ItemUse.h"
#include "GameData/GameDeFine.h"
#include "GameData/MessageID.h"
#include "GameData/ConstDataBP.h"

#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "RoleKitBagInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/ServerCharacter.h"
#include "Manager/CfgManager.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/MessageManager.h"


CONTROL_COMPILE_OPTIMIZE_START
	
CS3_BEGIN_INTERFACE_METHOD_MAP(URoleTeleportInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleTeleportInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleTeleportInterface::URoleTeleportInterface()
{
}

URoleTeleportInterface::~URoleTeleportInterface()
{
}

bool URoleTeleportInterface::IsOpen(const FString& point)
{
	TArray<FString> Temp = UGolbalBPFunctionLibrary::SplitString(teleportPointNPCs);
	if (Temp.Contains(point))
	{
		return true;
	}
	else
	{
		return false;
	}
}

void URoleTeleportInterface::RPC_TeleportPoint(const FString& point, int32 teleportType)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::RPC_TeleportPoint : GetEntity()!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(teleportType);
	args.Add(point);
	this->GetEntity()->CellCall(TEXT("CELL_TeleportPoint"), args);
}

void URoleTeleportInterface::OnOpenMapWin_Implementation()
{

}

void URoleTeleportInterface::TeleportPoint(const FString& point, ENUM_STONE_TELEPORT_TYPE TeleportType /*= ENUM_STONE_TELEPORT_TYPE::StoneTeleportTypeDefault*/)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::TeleportPoint : GetEntity()!"));
		return;
	}

	AServerCharacter* playerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(playerCharacter) && playerCharacter->IsState(ENTITY_STATE::EntityStateDead))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(2457);//当前为死亡状态，无法使用神行石进行传送！
		return;
	}

	if (point.IsEmpty()) return;
	if (!IsOpen(point))
	{
		//传送点未开启
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(2456);
		return;
	}

	const UConfigTable* TeleportPointTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TELEPORT_POINT_DATA);
	const FTELEPORT_POINT_DATA* TeleportPoint = TeleportPointTable->GetRow<FTELEPORT_POINT_DATA>(point);
	
	//获取背包
	URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (!IsValid(kitbatInst))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::TeleportPoint : kitbatInst!"));
		return;
	}

	// 默认是传送石传送
	TArray<UItemBase*> ItemList = kitbatInst->GetItemsByItemID(UUECS3GameInstance::Instance->ConstDataBP->TELEPORT_STONE_ID);
	if (ItemList.Num() == 0) 
	{
		int64 money = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
		if (money < TeleportPoint->MoneyCost) 
		{
			//看看金钱够不够,不够的话直接给无法传送的提示
			//消息提示   "没有神行石，无法传送"
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(2453);
			return;
		}
		else	
		{
			//金钱够的话，那就提示通过金钱进行传送
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(2455, UGolbalBPFunctionLibrary::GetRichTextMoney((int64)(TeleportPoint->MoneyCost)), FBtnClick::CreateLambda([this, point, TeleportType](RT_BTN_TYPE RtType)
			{
				if (RtType == RT_BTN_TYPE::RT_OK)
				{
					RPC_TeleportPoint(point, UUECS3GameInstance::Instance->ConstDataBP->TELEPORT_BY_MONEY);
				}
				else
				{
					OnCancelTeleport(TeleportType);
				}
			}));
			return;
		}
	}
	else
	{
		AServerCharacter* UseCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
		if (!IsValid(UseCharacter)) return;

		UItemUse * itemPtr = static_cast<UItemUse *>(ItemList[0]);
		int32 CheckUseResult = itemPtr->UseQuery(UseCharacter);

		//判断物品是否符合使用的条件
		if (UUECS3GameInstance::Instance->GMessageID->ITEM_USE_GO_ON_MSG != CheckUseResult)
		{
			// 加上定时器，神行石CD时间一到，相应的界面要变化
			float CDRemainningTime = itemPtr->GetCDRemainningTime();
			if (CDRemainningTime > 0.0)
			{
				if (this->DelayHandle.IsValid())
				{
					if (IsValid(UUECS3GameInstance::Instance))
					{
						UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(this->DelayHandle);
					}
				}
				if (IsValid(UUECS3GameInstance::Instance))
				{
					UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle, FTimerDelegate::CreateLambda([this, point, TeleportPoint, TeleportType]() {
						// 消息提示	“是否要传送到 "{0}" 传送点？”
						UUECS3GameInstance::Instance->MessageManager->ShowMessage(2411, TeleportPoint->DstName, FBtnClick::CreateLambda([this, point, TeleportType](RT_BTN_TYPE RtType)
						{
							if (RtType == RT_BTN_TYPE::RT_OK)
							{
								APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetActor());
								if (PlayerCharacter)
								{
									if (PlayerCharacter->IsState(ENTITY_STATE::EntityStateFight))
									{
										UUECS3GameInstance::Instance->MessageManager->ShowMessage(4298);//当前为战斗状态，无法使用传送点进行寻路!
										return;
									}
								}
								RPC_TeleportPoint(point, UUECS3GameInstance::Instance->ConstDataBP->TELEPORT_BY_TELEPORTSTONE);
							}
							else
							{
								OnCancelTeleport(TeleportType);
							}
						}));

						UUECS3GameInstance::Instance->MessageManager->HideMessage(2455);
						return;
					}), CDRemainningTime, false);
				}
			}

			// 消息提示	“通过金钱进行传送”
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(2455, UGolbalBPFunctionLibrary::GetRichTextMoney((int64)(TeleportPoint->MoneyCost)), FBtnClick::CreateLambda([this, point, TeleportType](RT_BTN_TYPE RtType)
			{
				if (IsValid(UUECS3GameInstance::Instance) && RtType == RT_BTN_TYPE::RT_OK)
				{
					RPC_TeleportPoint(point, UUECS3GameInstance::Instance->ConstDataBP->TELEPORT_BY_MONEY);
				}
				else
				{
					OnCancelTeleport(TeleportType);
				}
				//这里停掉定时器
				if (this->DelayHandle.IsValid())
				{
					if (IsValid(UUECS3GameInstance::Instance))
					{
						UUECS3GameInstance::Instance->CustomTimerManager->PauseTimer(this->DelayHandle);
					}
				}
			}));
			return;
		}
		else
		{
			// 消息提示	“是否要传送到 "{0}" 传送点？”
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(2411, TeleportPoint->DstName, FBtnClick::CreateLambda([this, point, TeleportType](RT_BTN_TYPE RtType)
			{
				if (RtType == RT_BTN_TYPE::RT_OK)
				{
					APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetActor());
					if(PlayerCharacter)
					{ 
						if (PlayerCharacter->IsState(ENTITY_STATE::EntityStateFight))
						{
							UUECS3GameInstance::Instance->MessageManager->ShowMessage(4298);//当前为战斗状态，无法使用传送点进行寻路!
							return;
						}
					}
					RPC_TeleportPoint(point, UUECS3GameInstance::Instance->ConstDataBP->TELEPORT_BY_TELEPORTSTONE);
				}
				else
				{
					OnCancelTeleport(TeleportType);
				}
			}));
			return;
		}
	}
}

FString URoleTeleportInterface::GetPointByNPCID(const FString& NPCID)
{
	const UConfigTable* TeleportPointTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TELEPORT_POINT_DATA);
	TArray<FName> TeleportPointIndexs = TeleportPointTable->GetRowNames();
	for (auto TeleportPointIndex : TeleportPointIndexs)
	{
		const FTELEPORT_POINT_DATA* TeleportPoint = TeleportPointTable->GetRow<FTELEPORT_POINT_DATA>(TeleportPointIndex);
		if (NPCID.Equals(TeleportPoint->DstNPCID))
		{
			return FNAME_TO_FSTRING(TeleportPoint->RowName);
		}
	}
	return FString("");
}

void URoleTeleportInterface::InitBlueCB()
{
	ArrBlueFunc.Add("OnOpenMapWin");
	Supper::InitBlueCB();
}

void URoleTeleportInterface::OnCancelTeleport(ENUM_STONE_TELEPORT_TYPE TeleportType)
{
	if (TeleportType != ENUM_STONE_TELEPORT_TYPE::StoneTeleportTypeNavigate) return;
	CancelTeleport();
}

void URoleTeleportInterface::CancelTeleport()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (Player)
	{
		Player->ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, false);
	}
}

CONTROL_COMPILE_OPTIMIZE_END
