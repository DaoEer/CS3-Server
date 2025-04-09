#pragma once
#include "CoreMinimal.h"
#include "Misc/Variant.h"

/**
* 文件名称：CacheMsg.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-07-27
*/

enum MessageType : uint8
{
	RemoteMethodCall,
	UpdateProperty,
};

struct Message_RemoteMethodCall
{
	FString name;
	TArray<FVariant> args;

	Message_RemoteMethodCall() {};
	Message_RemoteMethodCall(const FString& name, const TArray<FVariant>& args) :
		name(name),
		args(args)
	{};
};

struct Message_UpdateProperty
{
	FString name;
	FVariant newVal;
	FVariant oldVal;

	Message_UpdateProperty() {};
	Message_UpdateProperty(const FString& name, const FVariant& newVal, const FVariant& oldVal) :
		name(name),
		newVal(newVal),
		oldVal(oldVal)
	{};
};

struct CS3EntityMessage
{
	int32 EntityId;
	MessageType Type;

	Message_RemoteMethodCall RemoteMethodCall;
	Message_UpdateProperty UpdateProperty;

	CS3EntityMessage(int32 EntityId, Message_RemoteMethodCall&& Data) :
		EntityId(EntityId),
		Type(MessageType::RemoteMethodCall),
		RemoteMethodCall(Data)
	{};
	CS3EntityMessage(int32 EntityId, Message_UpdateProperty&& Data) :
		EntityId(EntityId),
		Type(MessageType::UpdateProperty),
		UpdateProperty(Data)
	{};

	bool Process();
};