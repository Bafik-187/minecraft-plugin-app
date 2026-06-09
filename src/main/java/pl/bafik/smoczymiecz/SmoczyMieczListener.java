package pl.bafik.smoczymiecz;

import net.kyori.adventure.text.Component;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.entity.EnderDragon;
import org.bukkit.entity.EnderPearl;
import org.bukkit.entity.Enderman;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.entity.EntityDamageByEntityEvent;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.inventory.EquipmentSlot;
import org.bukkit.inventory.ItemStack;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public final class SmoczyMieczListener implements Listener {

    private final SmoczyMieczPlugin plugin;
    private final Map<UUID, Long> cooldowns = new HashMap<>();

    public SmoczyMieczListener(SmoczyMieczPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler
    public void onRightClick(PlayerInteractEvent event) {
        if (event.getHand() != EquipmentSlot.HAND) {
            return;
        }
        if (event.getAction() != Action.RIGHT_CLICK_AIR && event.getAction() != Action.RIGHT_CLICK_BLOCK) {
            return;
        }

        Player player = event.getPlayer();
        ItemStack item = player.getInventory().getItemInMainHand();
        if (!SmoczyMieczItem.isSmoczyMiecz(plugin, item)) {
            return;
        }
        event.setCancelled(true);

        if (!player.hasPermission("smoczymiecz.use")) {
            return;
        }

        long cooldownMillis = plugin.getConfig().getLong("pearl-cooldown", 3) * 1000L;
        long now = System.currentTimeMillis();
        long readyAt = cooldowns.getOrDefault(player.getUniqueId(), 0L);
        if (now < readyAt) {
            double left = (readyAt - now) / 1000.0;
            player.sendActionBar(Component.text(
                    String.format("§5Smoczy Miecz §7ładuje się... §d%.1fs", left)));
            return;
        }

        if (plugin.getConfig().getBoolean("consume-pearl", false)
                && !player.getInventory().containsAtLeast(new ItemStack(Material.ENDER_PEARL), 1)) {
            player.sendActionBar(Component.text("§cPotrzebujesz Ender Perły!"));
            return;
        }
        if (plugin.getConfig().getBoolean("consume-pearl", false)) {
            player.getInventory().removeItem(new ItemStack(Material.ENDER_PEARL, 1));
        }

        cooldowns.put(player.getUniqueId(), now + cooldownMillis);

        double velocity = plugin.getConfig().getDouble("pearl-velocity", 2.0);
        player.launchProjectile(EnderPearl.class,
                player.getLocation().getDirection().multiply(velocity));

        player.getWorld().playSound(player.getLocation(), Sound.ENTITY_ENDER_DRAGON_FLAP, 1.0f, 1.5f);
        player.getWorld().playSound(player.getLocation(), Sound.ENTITY_ENDER_PEARL_THROW, 1.0f, 0.8f);
    }

    @EventHandler
    public void onAttack(EntityDamageByEntityEvent event) {
        if (!(event.getDamager() instanceof Player player)) {
            return;
        }
        if (!SmoczyMieczItem.isSmoczyMiecz(plugin, player.getInventory().getItemInMainHand())) {
            return;
        }
        if (event.getEntity() instanceof Enderman || event.getEntity() instanceof EnderDragon) {
            double bonus = plugin.getConfig().getDouble("bonus-ender-damage", 4.0);
            event.setDamage(event.getDamage() + bonus);
            player.getWorld().playSound(event.getEntity().getLocation(),
                    Sound.ENTITY_ENDER_DRAGON_HURT, 0.6f, 1.4f);
        }
    }
}
