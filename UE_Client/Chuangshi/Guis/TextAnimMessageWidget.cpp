#include "TextAnimMessageWidget.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ResourceManager.h"
#include "WidgetLayoutLibrary.h"
#include "Manager/CustomTimerManager.h"
#include "CanvasPanelSlot.h"
#include "Util/CS3Debug.h"
#include "Manager/AudioManager.h"

CONTROL_COMPILE_OPTIMIZE_START
UTextAnimMessageWidget::UTextAnimMessageWidget(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{

}

void UTextAnimMessageWidget::SetInfo(FTextAnimationMessage TextData)
{
	//有新的直接显示新的，旧的没播完的，直接顶掉
	ResetAnimation();

	UMaterialInstanceDynamic* MaterialInst = TextAnimImage->GetDynamicMaterial();
	if (!IsValid(MaterialInst))
	{
		return;
	}
	if (IsValid(TextData.Texture.Get()))
	{
		MaterialInst->SetTextureParameterValue(FSTRING_TO_FNAME(UGolbalBPFunctionLibrary::GetChinese(TEXT("MaterialTextureParam"))), TextData.Texture.Get());
	}
	else if (TextData.Texture.ToSoftObjectPath().IsValid())
	{
		UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(TextData.Texture.ToSoftObjectPath());
		MaterialInst->SetTextureParameterValue(FSTRING_TO_FNAME(UGolbalBPFunctionLibrary::GetChinese(TEXT("MaterialTextureParam"))), TextData.Texture.Get());
	}
	MaterialInst->SetScalarParameterValue(FSTRING_TO_FNAME(UGolbalBPFunctionLibrary::GetChinese(TEXT("MaterialColumnParam"))), TextData.Column);
	MaterialInst->SetScalarParameterValue(FSTRING_TO_FNAME(UGolbalBPFunctionLibrary::GetChinese(TEXT("MaterialRowParam"))), TextData.Row);
	MaterialInst->SetScalarParameterValue(FSTRING_TO_FNAME(UGolbalBPFunctionLibrary::GetChinese(TEXT("MaterialIgnoreParam"))), TextData.Ignore);
	MaterialInst->SetScalarParameterValue(FSTRING_TO_FNAME(UGolbalBPFunctionLibrary::GetChinese(TEXT("MaterialPlayTimeParam"))), TextData.PlayTime);

	UCanvasPanelSlot* CanvasPanelSlot = Cast<UCanvasPanelSlot>(UWidgetLayoutLibrary::SlotAsCanvasSlot(TextAnimImage));
	if (CanvasPanelSlot)
	{
		CanvasPanelSlot->SetSize(TextData.Size);
	}

	PlayTime = TextData.PlayTime;
	AnimPhase = 0.0f;
	if (!TextData.AudioID.Equals(TEXT("")))
	{
		UGolbalBPFunctionLibrary::AudioManager()->PlayVoice(TextData.AudioID);
	}
	PlayAnimation();
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(AnimEventHandle, this,
		&UTextAnimMessageWidget::PlayAnimation, 0.1f, true);
}

void UTextAnimMessageWidget::PlayAnimation()
{
	UMaterialInstanceDynamic* MaterialInst = TextAnimImage->GetDynamicMaterial();
	if (!IsValid(MaterialInst))
	{
		return;
	}
	AnimPhase += 0.1f;
	if (AnimPhase <= PlayTime)
	{
		MaterialInst->SetScalarParameterValue(TEXT("Phase"), AnimPhase);
	}
	else
	{
		ResetAnimation();
		Hide();
	}
}

void UTextAnimMessageWidget::ResetAnimation()
{
	UMaterialInstanceDynamic* MaterialInst = TextAnimImage->GetDynamicMaterial();
	if (!IsValid(MaterialInst))
	{
		return;
	}
	if (AnimEventHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(AnimEventHandle);
	}
	AnimPhase = 0.0f;
	MaterialInst->SetTextureParameterValue(FSTRING_TO_FNAME(UGolbalBPFunctionLibrary::GetChinese(TEXT("MaterialTextureParam"))), nullptr);
}

CONTROL_COMPILE_OPTIMIZE_END
