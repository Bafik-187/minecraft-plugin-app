package pl.bafik.smoczymiecz;

import org.bukkit.Material;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.inventory.ItemFlag;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.persistence.PersistentDataType;

import java.util.List;

/** Fabryka i rozpoznawanie Smoczego Miecza. */
public final class SmoczyMieczItem {

    private SmoczyMieczItem() {
    }

    public static ItemStack create(SmoczyMieczPlugin plugin) {
        ItemStack item = new ItemStack(Material.NETHERITE_SWORD);
        ItemMeta meta = item.getItemMeta();

        meta.setDisplayName("§5§lSmoczy Miecz");
        meta.setLore(List.of(
                "§7Legendarny super item z §canarchia.gg",
                "",
                "§5▸ §dPPM §7- wystrzeliwuje §5Ender Perlę",
                "§5▸ §7Dodatkowe obrażenia dla §5Endermanów i Smoka",
                "",
                "§8§oKto włada smokiem, włada anarchią..."
        ));

        meta.addEnchant(Enchantment.DAMAGE_ALL, 6, true);   // Sharpness VI
        meta.addEnchant(Enchantment.DURABILITY, 5, true);   // Unbreaking V
        meta.addEnchant(Enchantment.FIRE_ASPECT, 2, true);  // Fire Aspect II
        meta.addItemFlags(ItemFlag.HIDE_UNBREAKABLE);
        meta.setUnbreakable(true);

        meta.getPersistentDataContainer().set(plugin.getItemKey(), PersistentDataType.BYTE, (byte) 1);

        item.setItemMeta(meta);
        return item;
    }

    public static boolean isSmoczyMiecz(SmoczyMieczPlugin plugin, ItemStack item) {
        if (item == null || !item.hasItemMeta()) {
            return false;
        }
        return item.getItemMeta().getPersistentDataContainer()
                .has(plugin.getItemKey(), PersistentDataType.BYTE);
    }
}
