
#include "RolePerformanceInterface.h"

#include "Kismet/KismetMathLibrary.h"

#include "Interface/SkillInterface.h"
#include "Manager/SkillManager.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Interface/Role/RoleStallInterface.h"
#include "Interface/Role/RoleCrondInterface.h"
#include "GameData/Item/Equip.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Runtime/NavigationSystem/Public/NavigationSystem.h"

#include "Manager/StoryManager.h"
#include "Component/Role/RideCarrierComponent.h"
#include "Actor/NPC/FlyBindCharacter.h"
#include "Actor/Player/MagicCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "Component/SpringArmComponentEX.h"
#include "Manager/ParticleManager.h"
#include "Manager/AudioManager.h"
#include "Manager/ForceManager.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "Manager/AtkStateMar.h"
#include "Operation/RoleCtrl/RoleCtrlStateMgr.h"
#include "Manager/SkillManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include"Util\CustomEffect\CameraControl.h"
#include "GameDevelop/CS3GameHUD.h"
#include "Util/ConvertUtil.h"
#include "GameFrameWork/PlayerInput.h"
#include "RoleStateInterface.h"
#include "RoleInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URolePerformanceInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(SGMZOnWinGame, &URolePerformanceInterface::SGMZOnWinGame, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowSkillBarsHighLigh, &URolePerformanceInterface::ShowSkillBarsHighLigh, const int32&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URolePerformanceInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URolePerformanceInterface::URolePerformanceInterface()
{

}

void URolePerformanceInterface::OnEnterScenes()
{
	Super::OnEnterScenes();
	CurVoiceIds = TEXT("");
}

URolePerformanceInterface::~URolePerformanceInterface()
{

}

void URolePerformanceInterface::ShowMessagePlaySound_Implementation(const FString& Ids)
{
	// 解析语音相关数据
	if (CurVoiceIds == Ids || Ids.IsEmpty())
	{
		return;
	}
	CurVoiceIds = Ids;
	TArray<FString> VoiceData_Temp = UGolbalBPFunctionLibrary::SplitString(Ids, false, TEXT(";"));
	FVOICE_PLAY_DATA CurVoiceData;
	if (VoiceData_Temp.IsValidIndex(1))
	{
		CurVoiceData.IsCanInterrupt = VoiceData_Temp[1];
	}

	CurVoiceData.TalkingTargetId = UGolbalBPFunctionLibrary::GetTargetEntityID();
	//VoiceData_Temp[0]之前是必取字段，但偶现崩溃，故加判断和打印Ids日志 CST-9640
	if (VoiceData_Temp.IsValidIndex(0))
	{
		CurVoiceData.PlotList = UGolbalBPFunctionLibrary::SplitString(VoiceData_Temp[0]);
	}
	else
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Error Data(URolePerformanceInterface::ShowMessagePlaySound=%s)"), *Ids);
	}

	if (VoicePlayDataList.Num() == 0 || (VoicePlayDataList.Num() == 1 && VoicePlayDataList[0].IsCanInterrupt == "1"))
	{
		TalkingTarget = UGolbalBPFunctionLibrary::GetActorByID(CurVoiceData.TalkingTargetId);
	}

	if (VoicePlayDataList.Num() == 0)
	{
		if (CurVoiceData.PlotList.Num() > 0)
		{
			VoicePlayDataList.Add(CurVoiceData);
		}
	}
	else
	{
		if (VoicePlayDataList[VoicePlayDataList.Num() - 1].IsCanInterrupt == "1")
		{
			VoicePlayDataList[VoicePlayDataList.Num() - 1] = CurVoiceData; 
		}
		else
		{
			VoicePlayDataList.Add(CurVoiceData);
		}
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("--------------------URolePerformanceInterface::ShowMessagePlaySound:Ids[%s]~"), *Ids);
	//删除镜头的数据[带J标识]
	if (CurVoiceData.PlotList.Num() > 0)
	{
		while (CurVoiceData.PlotList.Last().StartsWith(TEXT("J")))
		{
			if (VoicePlayDataList.IsValidIndex(0))
			{
				FString lastId = VoicePlayDataList[0].PlotList.Pop();
				CS3_Warning(TEXT("Quest description config is wrong.Do not make a story %s at last!"), *lastId);
			}
		}
	}
	PlayNext();
}
///根据配置选择播放语音和镜头，如果任务的description的最后一个配的是镜头则无法显示接任务界面。
void URolePerformanceInterface::PlayNext()
{
	if (VoicePlayDataList.Num() == 0 || VoicePlayDataList[0].PlotList.Num() == 0)
	{
		TalkingTarget = nullptr;
		return;
	}
	PlaySoundsAndStorys();
}
///不要直接调用该函数，请调用PlayNext函数以执行相关判断。
void URolePerformanceInterface::PlaySoundsAndStorys()
{
	FString PlotID = VoicePlayDataList[0].PlotList[0];
	if (VoicePlayDataList[0].PlotList.Num() == 1)
	{
		UGolbalBPFunctionLibrary::AudioManager()->SetLastVoiceId(PlotID);
	}
	bool IsPlaying = false;
	if (PlotID.StartsWith(TEXT("J")))
	{
		FString SequenceId = PlotID.Replace(TEXT("J"),TEXT(""));
		///播放镜头
		UGStoryManager* GStoryManager = UGolbalBPFunctionLibrary::GStoryManager();
		if (GStoryManager)
		{
			IsPlaying = GStoryManager->IsPlaying();
			GStoryManager->PlaySequence(SequenceId);
		}
	}
	else
	{	///播放语音对话
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("URolePerformanceInterface::ShowMessagePlaySound -> %s~"), *PlotID);
		UGolbalBPFunctionLibrary::AudioManager()->AnalysisVoiceData(PlotID);
	}
	//如果PlotID是镜头，PlaySequence的时候，如果当前有镜头在播放，就会停掉镜头，停掉镜头又会调用PlayNext，从而会从PlotList删除一次，而这里还会再次删除一次，导致多删除一次从而崩溃
	//在播放镜头前判断是否正在播放，正在播放的话，肯定就会先停止当前播放的镜头，这里就不需要再次删除一次，以免出现重复删除的情况。
	if (!IsPlaying &&VoicePlayDataList.Num()>0&& VoicePlayDataList[0].PlotList.Num() > 0)
	{
		VoicePlayDataList[0].PlotList.RemoveAt(0);
		if (VoicePlayDataList[0].PlotList.Num() <= 0)
		{
			VoicePlayDataList.RemoveAt(0);
			if (VoicePlayDataList.Num() > 0)
			{
				TalkingTarget = UGolbalBPFunctionLibrary::GetActorByID(VoicePlayDataList[0].TalkingTargetId);
			}
			else
			{
				TalkingTarget = nullptr;
			}
		}
	}
}

void URolePerformanceInterface::ShowStopSpaceLife_Implementation(int32 RemainTime)
{

}

void URolePerformanceInterface::ShowSpaceLife_Implementation(const FString& EndTime,const int32& isMoveDown, const FString& CurTime)
{

}

void URolePerformanceInterface::HideSpaceLife_Implementation()
{

}

void URolePerformanceInterface::OnChangeBodyStart_Implementation()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_CHANGE_BODY, true);
}

void URolePerformanceInterface::OnChangeBodyEnd_Implementation()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	PlayerController->GetStateCtrlComp()->OnLeaveState(EROLE_CTRL_STATE::RCS_CHANGE_BODY);
}

void URolePerformanceInterface::onXinMoCtrlStart_Implementation(const TArray<int32>& ExcludeSkillList, const TArray<int32>& ActForbidList)
{
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchFightInXinMo(true, UGolbalBPFunctionLibrary::IntListToStringList(ExcludeSkillList), UGolbalBPFunctionLibrary::IntListToStringList(ActForbidList));
}

void URolePerformanceInterface::onXinMoCtrlEnd_Implementation()
{
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchFightInXinMo(false, TArray<FString>(), TArray<FString>());
}

void URolePerformanceInterface::OnBeginTrapSuck_Implementation(const FVector& SuckPos, const float SuckSpeed)
{
	//if (UGolbalBPFunctionLibrary::GetPlayerID() != EntityID) return;
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::OnBeginTrapSuck_Implementation : PlayerController!"));
		return;
	}
	PlayerController->SuckPosition = SuckPos;
	PlayerController->SuckMoveSpeed = SuckSpeed;
}

void URolePerformanceInterface::OnEndTrapSuck_Implementation()
{
	//if (UGolbalBPFunctionLibrary::GetPlayerID() != EntityID) return;
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::OnEndTrapSuck_Implementation : PlayerController!"));
		return;
	}
	PlayerController->SuckPosition = FVector::ZeroVector;
	PlayerController->SuckMoveSpeed = 0.0f;
}

void URolePerformanceInterface::ShowSpellBoxResultMessage_Implementation(const int32& type, const int32& vlue)
{

}

void URolePerformanceInterface::ShowPrompetOper_Implementation(const int32& PromptID, const FString& PromptTip, const FString& OffsetPos)
{
	//FString ItemIcon, Describe;
	//UTexture2D *SkillIcon;
	PrompetItemID = 0;
	PrompetskillID = 0;
	URoleKitBagInterface *kitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), EntityID));
	if (kitBagInterface)
	{
		TArray<UItemBase*> ItemList = kitBagInterface->GetItemsByItemID(PromptID);
		// 物品为空，说明是技能提示
		if (ItemList.Num()==0)
		{
			USkillManager* skillManger = UGolbalBPFunctionLibrary::GameInstance()->SkillManager;
			if (skillManger)
			{
				USkillData * skillData = skillManger->GetSkillDataById(PromptID);
				if (skillData)
				{
					PrompetskillID = PromptID;
					//SkillIcon = skillData->GetIcon();
					//Describe = skillData->GetDescription();
				}
			}
		}
		else
		{
			PrompetItemID = PromptID;
			//ItemIcon = ItemList[0]->Icon;
			//Describe = ItemList[0]->GetDescribe();
		}
	}
	if (PrompetItemID !=0)
	{
		//通知界面处理
		OnShowPrompetOper(0, PrompetItemID, PromptTip, OffsetPos);
	}
	else if(PrompetskillID != 0)
	{
		//通知界面处理
		OnShowPrompetOper(1, PrompetskillID, PromptTip, OffsetPos);
	}
	else
	{
		CS3_Warning(TEXT("ShowPrompetOper(id:%d) is error!"), PromptID);
	}
}

void URolePerformanceInterface::HidePrompetOper_Implementation()
{
	PrompetItemID = 0;
	PrompetskillID = 0;
	OnHidePrompetOper();
}

void URolePerformanceInterface::StartGuessGame_Implementation(const int32& progress, const FString& initMsg)
{

}

void URolePerformanceInterface::RightGuess_Implementation(const FString& winMsg)
{

}

void URolePerformanceInterface::WrongGuess_Implementation(const FString& lostMsg)
{

}

void URolePerformanceInterface::FinishGuess_Implementation(const FString& finishMsg)
{

}

void URolePerformanceInterface::RequestOpenSpaceSettlementRewdBox(const int32 BoxIndex)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RequestOpenSpaceSettlementRewdBox : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(BoxIndex);
	this->GetEntity()->CellCall(TEXT("openSpaceSettlementRewdBox"), args);
}

void URolePerformanceInterface::ShowEquipHardiness_Implementation(const FString& itemUid)
{
	URoleKitBagInterface *kitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), EntityID));
	if (kitBagInterface)
	{
		UEquip* Equip = Cast<UEquip>(kitBagInterface->FindItemByUID(itemUid));
		if (Equip)
		{
			OnShowEquipHardiness(Equip->GetHardiness());
		}
	}
}

void URolePerformanceInterface::EnterAimStatus_Implementation()
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(true, TEXT("HUOLINGFU"));
	}
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor)&& IsValid(PlayerActor->SpringArmCompent))
	{
		if (PlayerActor->ProfessionID == 4)
		{
			UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerActor->SpringArmCompent, 550.0f);
			UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(1.0f, 0.0f, 225.0f));
		}
		else
		{
			UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerActor->SpringArmCompent, 550.0f);
			UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(1.0f, 0.0f, 125.0f));
		}
	}
}

void URolePerformanceInterface::LeaveAimStatus_Implementation()
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(false);
	}
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor) && IsValid(PlayerActor->SpringArmCompent))
	{
		UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(1.0f, 0.0f, 0.0f));
	}
}


void URolePerformanceInterface::EnterShootModel_Implementation()
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->PlayerInput->FlushPressedKeys();
		if (IsValid(UUECS3GameInstance::Instance))
		{
			FTimerHandle TimerHandle;
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, TimerHandle, FTimerDelegate::CreateLambda([]() {
				if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
				{///CST-5288 镇海弓
					UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(true, TEXT("ZHG"));
					APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
					if (IsValid(PlayerActor) && IsValid(PlayerActor->SpringArmCompent))
					{
						UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerActor->SpringArmCompent, 550.0f);
						UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(1.0f, 0.0f, 125.0f));
					}
				}
			}), 0.25, false);
		}		
	}
}

void URolePerformanceInterface::LeaveShootModel_Implementation()
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(false);
	}
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor) && IsValid(PlayerActor->SpringArmCompent))
	{
		UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(1.0f, 0.0f, 0.0f));
}
}

void URolePerformanceInterface::EnterFlyModel_Implementation()
{
	AServerCharacter* Actor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(Actor) && IsValid(Cast<APlayerCharacter>(Actor)))
	{
		Cast<APlayerCharacter>(Actor)->SwitchFly(false, true);
	}
}

void URolePerformanceInterface::LeaveFlyModel_Implementation()
{
	AServerCharacter* Actor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(Actor) && IsValid(Cast<APlayerCharacter>(Actor)))
	{
		Cast<APlayerCharacter>(Actor)->SwitchFly(false, false);
	}
}

void URolePerformanceInterface::ShowPutDownJinDanBtn_Implementation()
{

}

void URolePerformanceInterface::HidePutDownJinDanBtn_Implementation()
{

}

void URolePerformanceInterface::DownJinDan_Implementation(const FString& AttachMeshID)
{
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{	
		PlayerActor->DownJinDan(FSTRING_TO_FNAME(AttachMeshID));
	}

	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->RecoveryMode();
	}
}

void URolePerformanceInterface::HoldJinDan_Implementation(const FString& AttachMeshID, float buffRemainTime, float TimerInterval)
{
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{
		PlayerActor->HoldJinDan(FSTRING_TO_FNAME(AttachMeshID),buffRemainTime, TimerInterval);
	}

	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::JinDanMode, CC_MODE_REASON::CCM_JINDAN_CONTROLLER_MODE);
	}
}

void URolePerformanceInterface::HoldPet_Implementation(const FString& AttachMeshID)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{
		PlayerActor->HoldPet(FSTRING_TO_FNAME(AttachMeshID));
	}
}

void URolePerformanceInterface::DownPet_Implementation(const FString& AttachMeshID)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{
		PlayerActor->DownPet(FSTRING_TO_FNAME(AttachMeshID));
	}
}

void URolePerformanceInterface::StartHLDRound()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::StartHLDRound : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("StartHLDRound"), args);
}

void URolePerformanceInterface::PlayBindEffect_Implementation(const int32& targetID, const FString& effectID)
{
	int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(effectID, 0.0f, UGolbalBPFunctionLibrary::GetActorByID(targetID), UGolbalBPFunctionLibrary::GetActorByID(targetID));
	BindEffectUID.Add(targetID, EffectUID);
}

void URolePerformanceInterface::EndPlayBindEffect_Implementation(const int32& targetID)
{
	if (BindEffectUID.Find(targetID))
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(BindEffectUID[targetID]);
		BindEffectUID.Remove(targetID);
	}
}

void URolePerformanceInterface::onBeginConfusion_Implementation()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->GetAtkStateMar()->SwitchConfusionMode(true);
	}
}

void URolePerformanceInterface::onEndConfusion_Implementation()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		PlayerController->GetAtkStateMar()->SwitchConfusionMode(false);
	}
}

void URolePerformanceInterface::OnStartThroughCanyon(const FString& MountModelId, const float& ForwardForceSpeed, const float& DownForceSpeed)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());

	// 当有玩家并且玩家是本地玩家
	if (PlayerActor && PlayerActor->ActorIsPlayer())
	{
		PlayerActor->RideCarrierComponent->RideOnCarrier(MountModelId);
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchGlidingMode(true, ForwardForceSpeed, DownForceSpeed);
	}
	else if(!GetActor())
	{
		TWeakObjectPtr<URolePerformanceInterface> DelayThisPtr(this);
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, GlidingHandle, FTimerDelegate::CreateLambda([DelayThisPtr, MountModelId, ForwardForceSpeed, DownForceSpeed]()
			{
				if (DelayThisPtr.IsValid())
				{
					URolePerformanceInterface* ThisPtr = DelayThisPtr.Get();
					if (ThisPtr->GetActor())
					{
						APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(ThisPtr->GetActor());
						if (PlayerActor->ActorIsPlayer() && PlayerActor->ActorIsPlayer())
						{
							PlayerActor->RideCarrierComponent->RideOnCarrier(MountModelId);
							UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchGlidingMode(true, ForwardForceSpeed, DownForceSpeed);
						}

						if (IsValid(UUECS3GameInstance::Instance))
						{
							UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->GlidingHandle);
						}
					}
				}
			}), 0.2f, true);
		}
	}
}

void URolePerformanceInterface::OnEndThroughCanyon()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());

	if (PlayerActor && PlayerActor->ActorIsPlayer())
	{
		PlayerActor->RideCarrierComponent->DisRideOnCarrier();
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchGlidingMode(false, 0.0f, 0.0f);
	}
}

int32 URolePerformanceInterface::AddFlyForce(int Dire, float ForceSpeed, float ForceTime)
{
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();

	if (IsValid(AtkStateMar))
	{
		return AtkStateMar->AddFlyForce(Dire, ForceSpeed, ForceTime);
	}
	else
	{
		CS3_Warning(TEXT("URolePerformanceInterface::OnEndThroughCanyo ---- AtkStateMar Is Null!"));
		return -1;
	}
}

void URolePerformanceInterface::OnStoryPlayEnd()
{
	PlayNext();
	if (!CurrentMapQuestTargetInfo.TargetInfo.SpaceName.IsEmpty())
	{
		APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
		if (IsValid(PlayerActor))
		{
			ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(PlayerActor->GetController());
			if (IsValid(PlayerController))
			{
				CS3_MOVE_TYPE MoveType = PlayerController->GetMoveType();
				if (MoveType != CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE)
				{
					CrossMapNavigateHandle();
				}
			}
		}
	}
}

void URolePerformanceInterface::OnLoadSpaceCompleted(bool IsFirst)
{
	if (!IsFirst)
	{
		if (CrossMapTargetInfo.Num() > 0)
		{
			CurrentMapQuestTargetInfo.TargetInfo = CrossMapTargetInfo[0];
			CrossMapTargetInfo.RemoveAt(0);
			const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
			UGStoryManager* GStoryManager = UGolbalBPFunctionLibrary::GStoryManager();
			bool CanExec;
			FString StoryID;
			if (IsValid(GStoryManager))
			{
				GStoryManager->CheckPreLoadStory(SpaceScriptID, CanExec, StoryID);
				if (!CanExec)
				{
					//开始寻路
					APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
					if (IsValid(PlayerActor))
					{
						CrossMapNavigateHandle();
					}
				}
			}
		}
		else
		{
			ClearTargetInfo();
			CurrentMapQuestTargetInfo.IsCompletedQuest = false;
			CurrentMapQuestTargetInfo.QuestTaskClass = "";
			CurrentMapQuestTargetInfo.AutoQuestID = 0;
			CurrentMapQuestTargetInfo.GossipWithType = 0;
		}
	}
	OnLoadSpaceCompletedBP();
}

void URolePerformanceInterface::SetCrossMapTargetInfo(TArray<FCROSS_MAP_TARGET_INFO>& CrossMapInfos)
{
	CrossMapTargetInfo = CrossMapInfos;
}

TArray<FCROSS_MAP_TARGET_INFO> URolePerformanceInterface::GetCrossMapTargetInfo()
{
	return CrossMapTargetInfo;
}

FCROSS_MAP_QUEST_TARGET_INFO URolePerformanceInterface::GetCurrentMapTargetInfo()
{
	return CurrentMapQuestTargetInfo;
}

void URolePerformanceInterface::SetCurrentMapTargetInfo(FCROSS_MAP_TARGET_INFO& MapTargetInfo, bool IsCompletedQuest, FString QuestTaskClass, int AutoQuestID /* = 0 */,int32 GossipWithType/* = 0*/)
{
	CurrentMapQuestTargetInfo.TargetInfo = MapTargetInfo;
	CurrentMapQuestTargetInfo.IsCompletedQuest = IsCompletedQuest;
	CurrentMapQuestTargetInfo.QuestTaskClass = QuestTaskClass;
	CurrentMapQuestTargetInfo.AutoQuestID = AutoQuestID;
	CurrentMapQuestTargetInfo.GossipWithType = GossipWithType;
}

void URolePerformanceInterface::ClearTargetInfo()
{
	CurrentMapQuestTargetInfo.TargetInfo.SpaceName = "";
	CurrentMapQuestTargetInfo.TargetInfo.ScriptID = "";
	CurrentMapQuestTargetInfo.TargetInfo.Position = FVector::ZeroVector;
	CurrentMapQuestTargetInfo.TargetInfo.TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportDefault;
	CurrentMapQuestTargetInfo.TargetInfo.Param1 = "";
	CurrentMapQuestTargetInfo.TargetInfo.Param2 = "";
	CurrentMapQuestTargetInfo.TargetInfo.Param3 = "";
}

void URolePerformanceInterface::StartPerformCrossMapNavigate(TArray<FCROSS_MAP_TARGET_INFO>& CrossMapInfos, FString DstSpaceName, bool IsCompletedQuest, FString QuestTaskClass /*= ""*/, FString NPCScriptID /*= ""*/, FVector FinalPosition /*= FVector::ZeroVector*/, float NearbyRange /*= 2.0f*/, int AutoQuestID /*= 0*/,int32 GossipWithType/*=0*/)
{
	SetCrossMapTargetInfo(CrossMapInfos);
	SetCurrentMapTargetInfo(CrossMapInfos[0], IsCompletedQuest, QuestTaskClass, AutoQuestID, GossipWithType);
	CrossMapTargetInfo.RemoveAt(0);
	HandleCrossMapNavigate();
	/*APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{
		PlayerActor->OnStartCrossMapNavigate(CurrentMapQuestTargetInfo);
	}*/
}

void URolePerformanceInterface::CrossMapNavigateHandle()
{
	//UNavigationSystem *const NavSys = GetWorld()->GetNavigationSystem();
	UNavigationSystemV1 *const NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());

	bool IsNavigateBuilding = NavSys->IsNavigationBeingBuilt(GetWorld());
	if (IsNavigateBuilding && !NavigateDataDoneHandle.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			TWeakObjectPtr<URolePerformanceInterface> DelayThisPtr(this);
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, NavigateDataDoneHandle, FTimerDelegate::CreateLambda([DelayThisPtr]() {
					if (DelayThisPtr.IsValid())
					{
						URolePerformanceInterface* ThisPtr = DelayThisPtr.Get();
						UNavigationSystemV1 *const NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(ThisPtr->GetWorld());
						if (IsValid(NavSys))
						{
							bool IsNavigateBuildingFinish = NavSys->IsNavigationBeingBuilt(ThisPtr->GetWorld());
							if (!IsNavigateBuildingFinish)
							{
								ThisPtr->HandleCrossMapNavigate();
							}
						}
					}
				}), 0.5, true);
			}
		}	
	}
	else
	{
		HandleCrossMapNavigate();
	}
	
}

void URolePerformanceInterface::HandleCrossMapNavigate()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{
		PlayerActor->OnStartCrossMapNavigate(CurrentMapQuestTargetInfo);
		ClearTargetInfo();
	}
	if (NavigateDataDoneHandle.IsValid() && UUECS3GameInstance::Instance)
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(NavigateDataDoneHandle);
		}
	}
}

void URolePerformanceInterface::OnNavigateArriveFinalSpace()
{
	//摆摊寻路
	if (NavigateActionType == ENUM_NAVIGATE_ACTION_TYPE::NavigateActionStall)
	{
		URoleStallInterface* StallInterface = Cast<URoleStallInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStallInterface")));
		if (IsValid(StallInterface))
		{
			StallInterface->OnNavigateStallFinish();
		}
	}
	//活动寻路
	else if (NavigateActionType == ENUM_NAVIGATE_ACTION_TYPE::NavigateActionCrond)
	{
		URoleCrondInterface* CrondInterface = Cast<URoleCrondInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("URoleCrondInterface")));
		if (IsValid(CrondInterface))
		{
			CrondInterface->OnNavigateCrondFinish();
		}
	}

	//达到终点后将NavigateActionType改为默认
	NavigateActionType = ENUM_NAVIGATE_ACTION_TYPE::NavigateActionDefault;
}

void URolePerformanceInterface::OnNavigateStop()
{
	//摆摊寻路
	if (NavigateActionType == ENUM_NAVIGATE_ACTION_TYPE::NavigateActionStall)
	{
		URoleStallInterface* StallInterface = Cast<URoleStallInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStallInterface")));
		if (IsValid(StallInterface))
		{
			StallInterface->OnNavigateStallFail();
		}
	}
	//活动寻路
	else if (NavigateActionType == ENUM_NAVIGATE_ACTION_TYPE::NavigateActionCrond)
	{
		URoleCrondInterface* CrondInterface = Cast<URoleCrondInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("URoleCrondInterface")));
		if (IsValid(CrondInterface))
		{
			CrondInterface->OnNavigateCrondFail();
		}
	}

	//达到终点后将NavigateActionType改为默认
	NavigateActionType = ENUM_NAVIGATE_ACTION_TYPE::NavigateActionDefault;
}

void URolePerformanceInterface::SetNavigateActionType(ENUM_NAVIGATE_ACTION_TYPE Type)
{
	NavigateActionType = Type;
}

void URolePerformanceInterface::onStartMoveByMoveTrap_Implementation(const int32& trapID, const float& speed)
{
	//获取陷阱Actor
	ACharacter* OtherActor = Cast<ACharacter>(UGolbalBPFunctionLibrary::GetActorByID(trapID));
	//获取力管理器
	UForceManager* ForceManager = UGolbalBPFunctionLibrary::ForceManager();
	//获取Role
	ACharacter* RoleActor = Cast<ACharacter>(GetActor());

	if (IsValid(OtherActor) && IsValid(ForceManager) && IsValid(RoleActor))
	{
		int32 ForceID = ForceManager->AddForceUseOtherLocDire
					(RoleActor, OtherActor, speed * 100.0f, ELOCAL_FORCE_DIRE::FORWARD_DIRE);

		MoveTrapForceIDs.Add(ForceID);
	}
	else
	{
		CS3_Warning(TEXT("URolePerformanceInterface::onStartMoveByMoveTrap --- trapID or ForceManager Is UnValid!"));
	}
}

void URolePerformanceInterface::onStopMoveByMoveTrap_Implementation()
{
	//获取力管理器
	UForceManager* ForceManager = UGolbalBPFunctionLibrary::ForceManager();
	//获取Role
	ACharacter* RoleActor = Cast<ACharacter>(GetActor());

	if (IsValid(ForceManager) && IsValid(RoleActor))
	{
		ForceManager->StopAllForces(RoleActor, MoveTrapForceIDs);
	}
	else
	{
		CS3_Warning(TEXT("URolePerformanceInterface::onStopMoveByMoveTrap --- ForceManager or RoleActor Is unValid!"));
	}

}

void URolePerformanceInterface::CLIENT_AddTrapVortex_Implementation(const int32 trapID, const float speed)
{
	//获取陷阱Actor
	ACharacter* OtherActor = Cast<ACharacter>(UGolbalBPFunctionLibrary::GetActorByID(trapID));
	//获取力管理器
	UForceManager* ForceManager = UGolbalBPFunctionLibrary::ForceManager();
	//获取Role
	ACharacter* RoleActor = Cast<ACharacter>(GetActor());

	if (IsValid(OtherActor) && IsValid(ForceManager) && IsValid(RoleActor))
	{
		int32 ForceID = ForceManager->AddForceUseOtherLocDire
		(RoleActor, OtherActor, speed * 100.0f, ELOCAL_FORCE_DIRE::LOOKAT_DIRE);
		
		ClientTriggerTrapVortex.Add(trapID, ForceID);
		
	}
	else
	{
		CS3_Warning(TEXT("URolePerformanceInterface::CLIENT_AddTrapVortex_Implementation --- trapID or ForceManager Is UnValid!"));
	}
}

void URolePerformanceInterface::CLIENT_RemoveTrapVortex_Implementation(const int32 trapID)
{
	//获取力管理器
	UForceManager* ForceManager = UGolbalBPFunctionLibrary::ForceManager();
	//获取Role
	ACharacter* RoleActor = Cast<ACharacter>(GetActor());

	if (IsValid(ForceManager) && IsValid(RoleActor))
	{
		if (ClientTriggerTrapVortex.Contains(trapID))
		{
			ForceManager->StopForces(RoleActor, ClientTriggerTrapVortex[trapID]);
		}
		
	}
	else
	{
		CS3_Warning(TEXT("URolePerformanceInterface::CLIENT_RemoveTrapVortex_Implementation --- ForceManager or RoleActor Is unValid!"));
	}

}



void URolePerformanceInterface::GetMovingPlatFormControl_Implementation()
{


}


void URolePerformanceInterface::LoseMovingPlatFormControl_Implementation()
{


}

void URolePerformanceInterface::RoleCameraMoveToEntity_Implementation(int32 targetEntityID, const FString& effectID, float MoveTime, float DelayTime)
{
	

}


void URolePerformanceInterface::RoleCameraMoveToEntityCB_Implementation(const FString& effectID)
{
}

void URolePerformanceInterface::EnterModelTPS()
{
	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor) && IsValid(PlayerActor->SpringArmCompent))
	{
		UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(1.0f, 0.0f, 125.0f));
	}
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController())&&IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(true, TEXT("TPS"));
	}	
}

void URolePerformanceInterface::LeaveModelTPS()
{
	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor) && IsValid(PlayerActor->SpringArmCompent))
	{
		UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(1.0f, 0.0f, 0.0f));
	}
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(false);
	}	
}

void URolePerformanceInterface::CameraLookAtTarget_Implementation(const int32& targetID, const FString& CameraTime, const FString& CameraTargetLotation, const FString& CameraTargetRotator)
{

}

void URolePerformanceInterface::CLIENT_EnterModelTPSParam_Implementation(const FString& Param)
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(true, TEXT("SFC"), Param);
	}
}

void URolePerformanceInterface::CLIENT_LeaveModelTPSParam_Implementation()
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(false);
	}
}

void URolePerformanceInterface::AircraftUseSkill_Implementation(int32 TargetID)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
	Player->FlyBindCharacter->UseSkill(TargetID,0);
}

void URolePerformanceInterface::CLIENT_CreateAircraft_Implementation(const FString& FlybindmeshID, int32 TargetID)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
	if (Player)
	{
		Player->CreateFlyBindActor(FlybindmeshID);
	}
	
}

void URolePerformanceInterface::CLIENT_RemoveAircraft_Implementation(int32 TargetID)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
	if (Player)
	{
		Player->DestroyFlyBindActor();
	}
	
}

void URolePerformanceInterface::CLIENT_AircraftUseSkill_Implementation(int32 CasterID, int32 TargetID)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(CasterID));
	if (IsValid(Player)&&IsValid(Player->FlyBindCharacter))
	{
		Player->FlyBindCharacter->UseSkill(CasterID, TargetID);
	}	
}

void URolePerformanceInterface::CreateFaBao_Implementation(int32 playerID, const FString& FaoBaoID)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(playerID));
	if (IsValid(Player))
	{
		Player->CreateFaBao(FaoBaoID);
	}
}

void URolePerformanceInterface::RemoveFaBao_Implementation()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(Player))
	{
		Player->DestroyFaBao();
	}
}

void URolePerformanceInterface::OpenAreaWall_Implementation(const FString& number)
{

}

void URolePerformanceInterface::CloseAreaWall_Implementation(const FString& number)
{

}

void URolePerformanceInterface::ShowMessageUpPlayerHead_Implementation(const int32& msgID)
{

}

void URolePerformanceInterface::UpdateScoreForLHSL_Implementation(int32 isOpen, int32 score)
{

}

void URolePerformanceInterface::FabaoPlayEffect_Implementation(int32 targetID, int32 playerID, const FString& actionID, const FString& effectID, const FString& playTime)
{ 
	APlayerCharacter* PlayerCharacter = Cast <APlayerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(playerID));
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(targetID));
	if (IsValid(PlayerCharacter)&& IsValid(PlayerCharacter->FabaoCharacter)&& IsValid(TargetCharacter))
	{
		PlayerCharacter->FabaoCharacter->UseSkill(TargetCharacter, PlayerCharacter, actionID, effectID, playTime);
	}
}

void URolePerformanceInterface::FabaoPlayEffectEnd_Implementation()
{

}

void URolePerformanceInterface::ExpelTheSoul_Implementation(const int32& targetID, const FString& effectID, float delayDestroyTime)
{

}

void URolePerformanceInterface::AbsorbTheSoul_Implementation(const int32& targetID)
{

}

void URolePerformanceInterface::RoleCameraShake_Implementation(float intensity, float rate, float time,int32 priority)
{

}

void URolePerformanceInterface::OnTauntBegin_Implementation()
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController())&&IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchChaoFengMode(true);
	}	
}

void URolePerformanceInterface::OnTauntEnd_Implementation()
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchChaoFengMode(false);
	}
}


void URolePerformanceInterface::OnSetViewTarget_Implementation(int32 TargetID, const FString& DurationTimeStr /*= 0 0 0*/, float Range /*= 0.0f*/, const FString& StartViewRotatorStr /*= 0 0 0*/, const FString& TargetViewRotatorStr /*= 0 0 0*/, uint8 bIsResetPlayerCamera /*= true*/)
{
	FVector DurationTime = UGolbalBPFunctionLibrary::FStringToFVector(DurationTimeStr);
	FVector StartViewRotator = UGolbalBPFunctionLibrary::FStringToFVector(StartViewRotatorStr);
	FVector TargetViewRotator = UGolbalBPFunctionLibrary::FStringToFVector(TargetViewRotatorStr);
	bool _bIsResetPlayerCamera = bIsResetPlayerCamera == 0 ? false : true;
	
	APlayerCharacter* player = Cast<APlayerCharacter>(GetActor());
	if (player)
	{
		player->SetViewTarget(TargetID, DurationTime, Range, StartViewRotator, TargetViewRotator, _bIsResetPlayerCamera);
	}
}
void URolePerformanceInterface::CLIENT_ThrowJinDan_Implementation(const FString& AttachMeshID, float buffRemainTime, float TimerInterval)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{
		PlayerActor->HoldJinDan(FSTRING_TO_FNAME(AttachMeshID), buffRemainTime, TimerInterval);
	}
}

void URolePerformanceInterface::CLIENT_OnThrowJinDan_Implementation(const FString& AttachMeshID)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{
		PlayerActor->DownJinDan(FSTRING_TO_FNAME(AttachMeshID));
	}
}

void URolePerformanceInterface::OnDialogWithNPCTaskScriptID_Implementation(const FString& NPCScriptID)
{

}

void URolePerformanceInterface::CLIENT_ClearChasePosInfo_Implementation()
{
	ChasePosInfo.Empty();
}

void URolePerformanceInterface::InitBlueCB()
{
	ArrBlueFunc.Add("ShowMessagePlaySound");
	ArrBlueFunc.Add("ShowSpaceLife");
	ArrBlueFunc.Add("ShowStopSpaceLife");	
	ArrBlueFunc.Add("HideSpaceLife");
	ArrBlueFunc.Add("OnChangeBodyStart");
	ArrBlueFunc.Add("OnChangeBodyEnd");
	ArrBlueFunc.Add("onXinMoCtrlStart");
	ArrBlueFunc.Add("onXinMoCtrlEnd");
	ArrBlueFunc.Add("OnBeginTrapSuck");
	ArrBlueFunc.Add("OnEndTrapSuck");
	ArrBlueFunc.Add("ShowSpellBoxResultMessage");
	ArrBlueFunc.Add("ShowPrompetOper");
	ArrBlueFunc.Add("HidePrompetOper");
	ArrBlueFunc.Add("StartGuessGame");
	ArrBlueFunc.Add("RightGuess");
	ArrBlueFunc.Add("WrongGuess");
	ArrBlueFunc.Add("FinishGuess");
	ArrBlueFunc.Add("ShowSpaceSettlementWin");
	ArrBlueFunc.Add("UpdateSpaceSettlementRewdBox");
	ArrBlueFunc.Add("ShowEquipHardiness");
	ArrBlueFunc.Add("ShowSwordAmount");
	ArrBlueFunc.Add("CreateLightWallBP");
	ArrBlueFunc.Add("RemoveLightWallBP");
	ArrBlueFunc.Add("HoldPet");
	ArrBlueFunc.Add("DownPet");
	ArrBlueFunc.Add("HLDCanStart");
	ArrBlueFunc.Add("HLDEnd");
	ArrBlueFunc.Add("StartFish");
	ArrBlueFunc.Add("ChangeWrestlingWidget");
	ArrBlueFunc.Add("PlayBindEffect");
	ArrBlueFunc.Add("EndPlayBindEffect");
	ArrBlueFunc.Add("onBeginConfusion");
	ArrBlueFunc.Add("onEndConfusion");
	ArrBlueFunc.Add("onStartMoveByMoveTrap");
	ArrBlueFunc.Add("onStopMoveByMoveTrap");
	ArrBlueFunc.Add("HoldJinDan");
	ArrBlueFunc.Add("DownJinDan");
	ArrBlueFunc.Add("ShowPutDownJinDanBtn");
	ArrBlueFunc.Add("HidePutDownJinDanBtn");
	ArrBlueFunc.Add("OnStartThroughCanyon");
	ArrBlueFunc.Add("OnEndThroughCanyon");
	ArrBlueFunc.Add("AddFlyForce");
	ArrBlueFunc.Add("EnterAimStatus");
	ArrBlueFunc.Add("LeaveAimStatus");
	ArrBlueFunc.Add("GetMovingPlatFormControl");
	ArrBlueFunc.Add("LoseMovingPlatFormControl");
	ArrBlueFunc.Add("RoleCameraMoveToEntity");
	ArrBlueFunc.Add("EnterModelTPS");
	ArrBlueFunc.Add("LeaveModelTPS");
	ArrBlueFunc.Add("RoleCameraMoveToEntityCB");
	ArrBlueFunc.Add("ShowMessageUpPlayerHead");
	ArrBlueFunc.Add("UpdateScoreForLHSL");
	ArrBlueFunc.Add("AlchemyStart");
	ArrBlueFunc.Add("CopyRemainTime");
	ArrBlueFunc.Add("OpenAreaWall");
	ArrBlueFunc.Add("CloseAreaWall");
	ArrBlueFunc.Add("SendRandomList");
	ArrBlueFunc.Add("FabaoPlayEffect");
	ArrBlueFunc.Add("FabaoPlayEffectEnd");
	ArrBlueFunc.Add("ExpelTheSoul");
	ArrBlueFunc.Add("AbsorbTheSoul");
	ArrBlueFunc.Add("RemoveFaBao");
	ArrBlueFunc.Add("CreateFaBao");
	ArrBlueFunc.Add("CLIENT_CreateAircraft");
	ArrBlueFunc.Add("CLIENT_RemoveAircraft");
	ArrBlueFunc.Add("AircraftUseSkill");
	ArrBlueFunc.Add("RoleCameraShake");
	ArrBlueFunc.Add("SendGameCopyTime");
	ArrBlueFunc.Add("OnTauntBegin");
	ArrBlueFunc.Add("OnTauntEnd");
	ArrBlueFunc.Add("CLIENT_ResetJump");
	ArrBlueFunc.Add("OnSetViewTarget");
	ArrBlueFunc.Add("CLIENT_AircraftUseSkill");
	ArrBlueFunc.Add("EnterFlyModel");
	ArrBlueFunc.Add("LeaveFlyModel");
	ArrBlueFunc.Add("EnterShootModel");
	ArrBlueFunc.Add("LeaveShootModel");
	ArrBlueFunc.Add("CLIENT_ThrowJinDan");
	ArrBlueFunc.Add("CLIENT_OnThrowJinDan");
	ArrBlueFunc.Add("OnDialogWithNPCTaskScriptID");
	ArrBlueFunc.Add("CLIENT_EnterModelTPSParam");
	ArrBlueFunc.Add("CLIENT_LeaveModelTPSParam");
	ArrBlueFunc.Add("CLIENT_AddTrapVortex");
	ArrBlueFunc.Add("CLIENT_RemoveTrapVortex");
	ArrBlueFunc.Add("CLIENT_ShowSpaceSettlementWin");
	ArrBlueFunc.Add("CLIENT_showSurvivalTime");
	ArrBlueFunc.Add("CLIENT_startSurvivalTime");
	ArrBlueFunc.Add("CLIENT_endSurvivalTime");
	ArrBlueFunc.Add("CLIENT_ClearChasePosInfo");
	ArrBlueFunc.Add("CLIENT_AddPerspectiveTarget");
	ArrBlueFunc.Add("CLIENT_RemovePerspectiveTarget");
	ArrBlueFunc.Add("CLIENT_ShowHPPercentAboveQuestBar");
	ArrBlueFunc.Add("CLIENT_CloseHPPercentAboveQuestBar");
	ArrBlueFunc.Add("CLIENT_SetMiniMapViewDefaultScale");
	ArrBlueFunc.Add("CameraLookAtTarget");
	ArrBlueFunc.Add("EnterYCJMDModelTPS");
	ArrBlueFunc.Add("LeaveYCJMDModelTPS");
	ArrBlueFunc.Add("ChangeYCJMDModelTPSSkillID");	
	ArrBlueFunc.Add("CLIENT_SGMZBossKilled");
	ArrBlueFunc.Add("SGMZOnWinGameShow");
	ArrBlueFunc.Add("SGMZLeadTeamChange");
	ArrBlueFunc.Add("SGMZSendMonsterHp");
	ArrBlueFunc.Add("SGMZSendScore");
	ArrBlueFunc.Add("SGMZSendScoreChange");
	ArrBlueFunc.Add("ShowSkillBarsHighLigh");
	Supper::InitBlueCB();
}

void URolePerformanceInterface::CLIENT_ResetJump()
{
	APlayerCharacter* player = Cast<APlayerCharacter>(GetActor());
	if (player && player->JumpComponent)
	{
		player->JumpComponent->ResetJumpCount();
	}
}

void URolePerformanceInterface::SGMZOnWinGame(const FVariant& variant)
{
	SGMZ_TEAM_DATAS SGMZTeamData = SGMZ_TEAM_DATAS(variant);
	TArray<FSGMZTEAM0DATA> data;
	for (auto tempData : SGMZTeamData.datas)
	{
		FSGMZTEAM0DATA dat;
		dat.extraExp = tempData.extraExp;
		dat.teamCamp = tempData.teamCamp;
		dat.isKillBoss = tempData.isKillBoss;
		dat.isWin = tempData.isWin;
		dat.score = tempData.score;
		dat.BossKiller = tempData.BossKiller;
		dat.feats = tempData.feats;
		for (auto bossData : tempData.bossDatas)
		{
			FSGMZBOSSDATA bdata;
			bdata.exp = bossData.exp;
			bdata.level = bossData.level;
			bdata.bossName = bossData.name;
			bdata.stage = bossData.stage;
			bdata.PerHP = bossData.PerHP;
			bdata.time = bossData.time;
			dat.bossDatas.Add(bdata);
		}
		data.Add(dat);
	};
	SGMZOnWinGameShow(data);
	SGMZFinishedStage.Empty();
}

void URolePerformanceInterface::SGMZOnWinGameShow_Implementation(const TArray<FSGMZTEAM0DATA>& SGMZTeamData)
{

}

void URolePerformanceInterface::CLIENT_ShowSpaceSettlementWin_Implementation(const int32& spaceType, const int32& rewardValue, const int32& spacetime,const int32& dieNumber, const int32& level)
{

}

void URolePerformanceInterface::SGMZLeadTeamChange_Implementation(const int32& camp)
{

}
void URolePerformanceInterface::SGMZSendScoreChange_Implementation(const int32& killerCamp, const int32& value)
{

}

void URolePerformanceInterface::SGMZSendMonsterHp_Implementation(const int32& camp, const int32& stage, const int32& perHp)
{

}

void URolePerformanceInterface::SGMZSendScore_Implementation(const int32 & camp, const int32 & stage, const int32 & score)
{
}

void URolePerformanceInterface::CLIENT_SGMZBossKilled_Implementation(const int32 & camp, const int32 & stage)
{
	if (SGMZFinishedStage.Contains(camp))
	{
		SGMZFinishedStage[camp] = stage;
	}
	else
	{
		SGMZFinishedStage.Add(camp, stage);
	}
}

void URolePerformanceInterface::CLIENT_SetMiniMapViewDefaultScale_Implementation(float DefaultScale)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		ACS3GameHUD * MyHUD = Cast<ACS3GameHUD>(PlayerController->GetHUD());
		if (IsValid(MyHUD))
		{
			MyHUD->SetViewDefaultScale(DefaultScale);
		}
	}
}

void URolePerformanceInterface::EnterYCJMDModelTPS_Implementation( const int32& skillID, const int32& weaponItemID)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor) && PlayerActor->ActorIsPlayer())
	{
		if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
		{
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(true, TEXT("YCJMD"), INT_TO_FSTRING(skillID));
		}
		if (IsValid(PlayerActor->SpringArmCompent))
		{
			PlayerActor->OnChangeArmLength(150.0f, 0.2f);
			//UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerActor->SpringArmCompent, 150.0);
			PlayerCameraArmLength =PlayerActor->SpringArmCompent->TargetArmLength;
			UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(-300.0f, 42.5f, 70.0f));
		}
		PlayerActor->bIsYCJMDCopy = true;
		GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
		if (CS3PlayerEntity == nullptr) return;
		URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
		if (RoleInterface)
		{
			RoleInterface->RequestChangeYCJMDCopyState(PlayerActor->bIsYCJMDCopy ? 1 : 0);//同步其他客户端射击状态
		}
	}
}

void URolePerformanceInterface::LeaveYCJMDModelTPS_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor) && PlayerActor->ActorIsPlayer())
	{
		if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
		{
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchShootMode(false);
		}
		if (IsValid(PlayerActor->SpringArmCompent))
		{
			PlayerActor->OnChangeArmLength(PlayerCameraArmLength, 0.35f);
			UGolbalBPFunctionLibrary::SetCameraSocketOffset(PlayerActor->SpringArmCompent, FVector(1.0f, 0.0f, 0.0f));
		}
		//远程吃鸡中与动作相关设置
		PlayerActor->bIsYCJMDCopy = false;
		PlayerActor->bIsYCJMDAimOffsetState = false;
		PlayerActor->StopFrontAction();
		if (IsValid(PlayerActor->GetBaseAnimInstance()))
		{
			PlayerActor->GetBaseAnimInstance()->PlayStandbyAction();//因bIsYCJMDAimOffsetState=false,需更新一下动作为自由待机
		}

		GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
		if (CS3PlayerEntity == nullptr) return;
		URoleInterface * RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
		if (RoleInterface)
		{
			RoleInterface->RequestChangeYCJMDCopyState(PlayerActor->bIsYCJMDCopy ? 1 : 0);//同步其他客户端射击状态
		}
	}
}

void URolePerformanceInterface::ChangeYCJMDModelTPSSkillID_Implementation(const int32& skillID)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor) && PlayerActor->ActorIsPlayer())
	{
		if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
		{
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SetShootModeOtherValue(INT_TO_FSTRING(skillID));
		}		
	}
}

void URolePerformanceInterface::ShowSkillBarsHighLigh(const int32 & highLighID)
{
	ShowSkillBarsHighLighBP(highLighID);
}

void URolePerformanceInterface::RPC_guessGameSize(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_guessGameSize : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("guessGameSize"), args);
}

void URolePerformanceInterface::RPC_guessGameRoll(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_guessGameRoll : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("guessGameRoll"), args);
}

void URolePerformanceInterface::RPC_endGuessGame()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_endGuessGame : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("endGuessGame"), args);
}

void URolePerformanceInterface::RPC_ldwj_putDownJinDan()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_ldwj_putDownJinDan : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("ldwj_putDownJinDan"), args);
}

void URolePerformanceInterface::RPC_onSwordCollisionBegin(const FString& STRING_1, const int32& INT32_1, const FVector& POSITION_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_onSwordCollisionBegin : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(INT32_1);
	args.Add(POSITION_1);

	entity->CellCall(TEXT("onSwordCollisionBegin"), args);
}

void URolePerformanceInterface::RPC_onObtainCountAddList(const FString& STRING_1, const int32& INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_onObtainCountAddLis : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(INT32_1);

	entity->CellCall(TEXT("onObtainCountAddList"), args);
}

void URolePerformanceInterface::RPC_onBaGuaJigsawCompleted()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_onBaGuaJigsawCompleted : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("onBaGuaJigsawCompleted"), args);
}

void URolePerformanceInterface::RPC_onRoleCameraMoveToEntity()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_onRoleCameraMoveToEntity : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("onRoleCameraMoveToEntity"), args);
}

void URolePerformanceInterface::RPC_createMonsterExtLightWall(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_createMonsterExtLightWall : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("createMonsterExtLightWall"), args);
}

void URolePerformanceInterface::RPC_requestRandomDice()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_requestRandomDice : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_requestRandomDice"), args);
}

void URolePerformanceInterface::RPC_TriggerQuestDialogWithNPC(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_TriggerQuestDialogWithNPC : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("triggerQuestDialogWithNPC"), args);
}

void URolePerformanceInterface::RPC_StopPlaySound(FString soundID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_StopPlaySound : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(soundID);

	entity->CellCall(TEXT("stopPlaySound"), args);
}

void URolePerformanceInterface::SelectMonsterMenu(const int32& MonsterID, const int32& Index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URolePerformanceInterface::RPC_RequestReturnServer : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(MonsterID);
	args.Add(Index);
	entity->CellCall(TEXT("selectMonsterMenu"), args);
}

void URolePerformanceInterface::CLIENT_showSurvivalTime_Implementation(const int32 & totalSurverTime, const TArray<int32>& gradeList, const TArray<int32>& expList, const TArray<int32>& moneyList)
{
}

void URolePerformanceInterface::CLIENT_startSurvivalTime_Implementation()
{
}

void URolePerformanceInterface::CLIENT_endSurvivalTime_Implementation(const int32 & surverTime)
{
}


void URolePerformanceInterface::CLIENT_AddPerspectiveTarget_Implementation(int32 targetID, float maxDist, float minDist, float maxHeigth )
{
	AServerCharacter* AActor = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(targetID));
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(AActor) && IsValid(Player))
	{
		AActor->SetCustomDepthStncilValue(CUSTOM_DEPTH_STENCIL::CUSTOM_DEPTH_STENCIL_OUTLINE_COVER);
		Player->CameraControl->AddPerspectiveTarget(targetID, maxDist, minDist, maxHeigth);
	}

}

void URolePerformanceInterface::CLIENT_RemovePerspectiveTarget_Implementation(int32 targetID, float maxDist, float minDist, float maxHeigth)
{
	AServerCharacter* AActor = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(targetID));
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(AActor) && IsValid(Player))
	{
		AActor->SetCustomDepthStncilValue(CUSTOM_DEPTH_STENCIL::CUSTOM_DEPTH_STENCIL_NORMAL);
		Player->CameraControl->RemovePerspectiveTarget(targetID);
	}
}

void URolePerformanceInterface::CLIENT_ShowHPPercentAboveQuestBar_Implementation(int32 targetID)
{

}

void URolePerformanceInterface::CLIENT_CloseHPPercentAboveQuestBar_Implementation()
{

}

CONTROL_COMPILE_OPTIMIZE_END
