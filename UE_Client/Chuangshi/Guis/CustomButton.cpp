#include "CustomButton.h"
#include "ButtonSlot.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/CustomCursorManager.h"
#include "Util/CS3Debug.h"

#pragma region /** SCustomButton */

CONTROL_COMPILE_OPTIMIZE_START

FReply SCumstomButton::OnMouseMove(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent)
{
	if (!AdvancedHitTexture) return SCS3Button::OnMouseMove(MyGeometry, MouseEvent);
	bool WhatToReturn = true;
	FVector2D LocalPosition = MyGeometry.AbsoluteToLocal(MouseEvent.GetScreenSpacePosition());
	LocalPosition.X = floor(LocalPosition.X);
	LocalPosition.Y = floor(LocalPosition.Y);
	LocalPosition /= MyGeometry.GetLocalSize();
	int32 ImageWidth = AdvancedHitTexture->PlatformData->SizeX;
	int32 ImageHeight = AdvancedHitTexture->PlatformData->SizeY;
	LocalPosition.X *= ImageWidth;
	LocalPosition.Y *= ImageHeight;
	FColor* ImageData = static_cast<FColor*>((AdvancedHitTexture->PlatformData->Mips[0]).BulkData.Lock(LOCK_READ_ONLY));
	if (!ImageData)
	{
		WhatToReturn = false;
	}
	else
	{
		if (LocalPosition.X < ImageWidth && LocalPosition.Y < ImageHeight)
		{
			int32 BufferPosition = (LocalPosition.Y * ImageWidth) + LocalPosition.X;
			if (ImageData[BufferPosition].A <= AdvancedHitAlpha) WhatToReturn = false;
		}
		else
		{
			WhatToReturn = false;
			CS3_Warning(TEXT("-->error:SCumstomButton::OnMouseMove : MousePosition Is Over ImageSize ! Position.X = %f, Position.Y = %f, ImageWidth = %d, ImageHeight = %d"), LocalPosition.X, LocalPosition.Y, ImageWidth, ImageHeight);
		}
	}

	AdvancedHitTexture->PlatformData->Mips[0].BulkData.Unlock();
	if (WhatToReturn != bIsHovered)
	{
		bIsHovered = WhatToReturn;
		if (bIsHovered) SCS3Button::OnMouseEnter(MyGeometry, MouseEvent);
		else SCS3Button::OnMouseLeave(MouseEvent);
	}
	return SCS3Button::OnMouseMove(MyGeometry, MouseEvent);
}

FCursorReply SCumstomButton::OnCursorQuery(const FGeometry& MyGeometry, const FPointerEvent& CursorEvent) const {
	if (!bIsHovered) return FCursorReply::Unhandled();
	TOptional<EMouseCursor::Type> TheCursor = Cursor.Get();
	return (TheCursor.IsSet()) ? FCursorReply::Cursor(TheCursor.GetValue()) : FCursorReply::Unhandled();
}

void SCumstomButton::SetIsHovered(uint8 IsHovered)
{
	bIsHovered = IsHovered;
}

#pragma endregion

#pragma region /** UCustomButton */
UCustomButton::UCustomButton(const FObjectInitializer& ObjectInitializer)
	:Super(ObjectInitializer)
{
	AdvancedHitTexture = NULL;
	AdvancedHitAlpha = NULL;
}

void UCustomButton::SynchronizeProperties()
{
	Super::SynchronizeProperties();
	(static_cast<SCumstomButton*>(MyButton.Get()))->SetAdvancedHitTexture(AdvancedHitTexture);
	(static_cast<SCumstomButton*>(MyButton.Get()))->SetAdvancedHitAlpha(AdvancedHitAlpha);
}

TSharedRef<SWidget> UCustomButton::RebuildWidget()
{
	TSharedPtr<SCumstomButton> CustomButton = SNew(SCumstomButton)
		.OnClicked(BIND_UOBJECT_DELEGATE(FOnClicked, SlateHandleClicked))
		.OnPressed(BIND_UOBJECT_DELEGATE(FSimpleDelegate, SlateHandlePressed))
		.OnReleased(BIND_UOBJECT_DELEGATE(FSimpleDelegate, SlateHandleReleased))
		.OnHovered_UObject(this, &ThisClass::SlateHandleHovered)
		.OnUnhovered_UObject(this, &ThisClass::SlateHandleUnhovered)
		.ButtonStyle(&WidgetStyle)
		.ClickMethod(ClickMethod)
		.TouchMethod(TouchMethod)
		.IsFocusable(IsFocusable)
		;
	if (CustomButton.IsValid())
	{
		CustomButton->SetAdvancedHitTexture(AdvancedHitTexture);
		CustomButton->SetAdvancedHitAlpha(AdvancedHitAlpha);
	}

	MyButton = CustomButton;

	if (GetChildrenCount() > 0) Cast<UButtonSlot>(GetContentSlot())->BuildSlot(MyButton.ToSharedRef());

	return MyButton.ToSharedRef();
}

bool UCustomButton::IsInArea(FVector2D MouseScreenPos)
{
	if (!AdvancedHitTexture) return false;

	FGeometry MyGeometry = GetCachedGeometry();

	FVector2D LocalPosition = MyGeometry.AbsoluteToLocal(MouseScreenPos);
	int32 ImageWidth = AdvancedHitTexture->PlatformData->SizeX;
	int32 ImageHeight = AdvancedHitTexture->PlatformData->SizeY;
	if (!(LocalPosition.X >= 0 && LocalPosition.X < ImageWidth && LocalPosition.Y >= 0 && LocalPosition.Y < ImageHeight))
	{
		return false;
	}

	bool WhatToReturn = true;

	LocalPosition.X = floor(LocalPosition.X);
	LocalPosition.Y = floor(LocalPosition.Y);
	LocalPosition /= MyGeometry.GetLocalSize();
	LocalPosition.X *= ImageWidth;
	LocalPosition.Y *= ImageHeight;
	FColor* ImageData = static_cast<FColor*>((AdvancedHitTexture->PlatformData->Mips[0]).BulkData.Lock(LOCK_READ_ONLY));
	if (!ImageData)
	{
		WhatToReturn = false;
	}
	else
	{
		if (LocalPosition.X < ImageWidth && LocalPosition.Y < ImageHeight)
		{
			int32 BufferPosition = (LocalPosition.Y * ImageWidth) + LocalPosition.X;
			if (ImageData[BufferPosition].A <= AdvancedHitAlpha) WhatToReturn = false;
		}
		else
		{
			WhatToReturn = false;
			CS3_Warning(TEXT("-->error:UCustomButton::IsInArea : MousePosition Is Over ImageSize ! Position.X = %f, Position.Y = %f, ImageWidth = %d, ImageHeight = %d"), LocalPosition.X, LocalPosition.Y, ImageWidth, ImageHeight);
		}
	}

	AdvancedHitTexture->PlatformData->Mips[0].BulkData.Unlock();

	return WhatToReturn;
}

void UCustomButton::SetIsHovered(uint8 IsHovered)
{
	if (MyButton)
	{
		if ((bool)IsHovered != static_cast<SCumstomButton*>(MyButton.Get())->IsHovered())
		{
			static_cast<SCumstomButton*>(MyButton.Get())->SetIsHovered(IsHovered);
		}
	}
}

#pragma endregion

CONTROL_COMPILE_OPTIMIZE_END