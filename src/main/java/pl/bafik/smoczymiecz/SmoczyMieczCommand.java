package pl.bafik.smoczymiecz;

import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

public final class SmoczyMieczCommand implements CommandExecutor {

    private final SmoczyMieczPlugin plugin;

    public SmoczyMieczCommand(SmoczyMieczPlugin plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        Player target;
        if (args.length >= 1) {
            target = Bukkit.getPlayerExact(args[0]);
            if (target == null) {
                sender.sendMessage("§cGracz §e" + args[0] + " §cnie jest online.");
                return true;
            }
        } else if (sender instanceof Player player) {
            target = player;
        } else {
            sender.sendMessage("§cZ konsoli musisz podać gracza: /smoczymiecz <gracz>");
            return true;
        }

        target.getInventory().addItem(SmoczyMieczItem.create(plugin));
        target.sendMessage("§5§lSmoczy Miecz §dwylądował w Twoim ekwipunku!");
        if (!sender.equals(target)) {
            sender.sendMessage("§aDano Smoczy Miecz graczowi §e" + target.getName() + "§a.");
        }
        return true;
    }
}
