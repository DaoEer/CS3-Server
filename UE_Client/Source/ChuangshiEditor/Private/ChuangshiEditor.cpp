
#include "ChuangshiEditor.h"
#include "ISettingsModule.h"
#include "Util/SmallResourceCache/SmallResourceCache.h"

#define LOCTEXT_NAMESPACE "ChuangshiEditor"

void FLove4EditorModule::StartupModule()
{
	ISettingsModule& SettingsModule = FModuleManager::LoadModuleChecked<ISettingsModule>("Settings");
	SettingsModule.RegisterSettings("Project", "ChuangshiConfig", "SmallResourceCacheConfig",
        LOCTEXT("RuntimeSettingsName", "小资源缓存"),
        LOCTEXT("RuntimeSettingsDescription", "利用空闲物理内存缓存资源,缓解同步加载造成的卡顿"),
        GetMutableDefault<USmallResourceCacheConfig>()
    );
}

void FLove4EditorModule::ShutdownModule()
{
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_GAME_MODULE(FLove4EditorModule, ChuangshiEditor);