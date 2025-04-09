#include "CacheMsg.h"
#include "CS3Base/CS3Entity.h"
#include "Util/GolbalBPFunctionLibrary.h"

bool CS3EntityMessage::Process()
{
	CS3Entity* entity = (CS3Entity*)(UGolbalBPFunctionLibrary::FindEntity(EntityId));
	if (entity == nullptr) return false;

	switch (Type)
	{
	case MessageType::RemoteMethodCall:
		entity->ProcessRemoteMethodCall(RemoteMethodCall.name, RemoteMethodCall.args);
		break;
	case MessageType::UpdateProperty:
		entity->ProcessUpdateProperty(UpdateProperty.name, UpdateProperty.newVal, UpdateProperty.oldVal);;
		break;
	}

	return true;
}
