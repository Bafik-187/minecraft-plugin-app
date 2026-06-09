package pl.bafik.smoczymiecz;

import org.bukkit.NamespacedKey;
import org.bukkit.plugin.java.JavaPlugin;

public final class SmoczyMieczPlugin extends JavaPlugin {

    private NamespacedKey itemKey;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        itemKey = new NamespacedKey(this, "smoczy_miecz");

        getCommand("smoczymiecz").setExecutor(new SmoczyMieczCommand(this));
        getServer().getPluginManager().registerEvents(new SmoczyMieczListener(this), this);

        getLogger().info("Smoczy Miecz aktywowany! Super item z anarchia.gg gotowy.");
    }

    public NamespacedKey getItemKey() {
        return itemKey;
    }
}
