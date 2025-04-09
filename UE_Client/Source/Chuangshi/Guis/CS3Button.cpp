#include "CS3Button.h"
#include "ButtonSlot.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Manager/CustomCursorManager.h"
#include "Manager/TutorialManager.h"
#include "Manager/AudioManager.h"

CONTROL_COMPILE_OPTIMIZE_START

#pragma region /** SCS3Button */

FReply SCS3Button::OnMouseButtonDown(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent)
{
	bool isEspecialCursorState = DealEspecialCursorState(MouseEvent);
	if(isEspecialCursorState) return FReply::Handled();
	//一定要在检查指引之前，检查指引会触发下一步
	FReply TempReply = SButton::OnMouseButtonDown(MyGeometry, MouseEvent);
	//检查完成指引
	CheckFinishTutorial();
	return TempReply;
}

FReply SCS3Button::OnMouseButtonUp(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent)
{
	return SButton::OnMouseButtonUp(MyGeometry, MouseEvent);
}

bool SCS3Button::DealEspecialCursorState(const FPointerEvent& MouseEvent)
{
	//如果是特殊鼠标状态
	if (UGolbalBPFunctionLibrary::CustomCursorManager() && UGolbalBPFunctionLibrary::CustomCursorManager()->IsEspecialCursorState())
	{
		//右键
		if (MouseEvent.IsMouseButtonDown(EKeys::RightMouseButton))
		{
			//右键恢复鼠标状态
			UGolbalBPFunctionLibrary::CustomCursorManager()->ResetCursor();
			return true;
		}
		//左键
		else if (MouseEvent.IsMouseButtonDown(EKeys::LeftMouseButton))
		{
			//左键点击无效
			return true;
		}
	}
	return false;
}

void SCS3Button::CheckFinishTutorial()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->TutorialManager))
	{
		UUECS3GameInstance::Instance->TutorialManager->OnTriggerItemClicked();
	}
}

#pragma endregion

#pragma region /** UCustomButton */
UCS3Button::UCS3Button(const FObjectInitializer& ObjectInitializer)
	:Super(ObjectInitializer)
{

}

TSharedRef<SWidget> UCS3Button::RebuildWidget()
{
	TSharedPtr<SCS3Button> CS3Button = SNew(SCS3Button)
		.OnClicked(BIND_UOBJECT_DELEGATE(FOnClicked, SlateHandleClicked))
		.OnPressed(BIND_UOBJECT_DELEGATE(FSimpleDelegate, CS3SlateHandlePressed))
		.OnReleased(BIND_UOBJECT_DELEGATE(FSimpleDelegate, SlateHandleReleased))
		.OnHovered_UObject(this, &ThisClass::CS3SlateHandleHovered)
		.OnUnhovered_UObject(this, &ThisClass::SlateHandleUnhovered)
		.ButtonStyle(&WidgetStyle)
		.ClickMethod(ClickMethod)
		.TouchMethod(TouchMethod)
		.IsFocusable(IsFocusable)
		;

	MyButton = CS3Button;

	if (GetChildrenCount() > 0) Cast<UButtonSlot>(GetContentSlot())->BuildSlot(MyButton.ToSharedRef());

	return MyButton.ToSharedRef();
}

void UCS3Button::CS3SlateHandlePressed()
{
	if (!PressedSoundID.IsEmpty() && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
	{
		UUECS3GameInstance::Instance->AudioManager->PlaySoundUI(PressedSoundID);
	}
	SlateHandlePressed();
}

void UCS3Button::CS3SlateHandleHovered()
{
	if (!HoveredSoundID.IsEmpty() && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
	{
		UUECS3GameInstance::Instance->AudioManager->PlaySoundUI(HoveredSoundID);
	}
	SlateHandleHovered();
}

#pragma endregion
CONTROL_COMPILE_OPTIMIZE_END
