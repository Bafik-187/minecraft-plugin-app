# SmoczyMiecz 🐉

Plugin do Minecrafta (Spigot/Paper 1.20+) dodający **Smoczy Miecz** — super item
wzorowany na przedmiocie z serwera **anarchia.gg**.

## Co potrafi Smoczy Miecz?

- ⚔️ Netheritowy miecz z **Sharpness VI**, **Unbreaking V** i **Fire Aspect II**
- 🟣 **PPM (prawy przycisk myszy)** — wystrzeliwuje **Ender Perłę** z cooldownem (domyślnie 3s)
- 🐲 Zadaje **dodatkowe obrażenia** Endermanom i Smokowi Kresu
- 💎 Niezniszczalny

## Komendy

| Komenda | Opis | Permisja |
|---|---|---|
| `/smoczymiecz [gracz]` | Daje Smoczy Miecz (aliasy: `/sm`, `/dragonsword`) | `smoczymiecz.give` (domyślnie OP) |

Permisja `smoczymiecz.use` (domyślnie wszyscy) pozwala strzelać perłami.

## Konfiguracja (`config.yml`)

```yaml
pearl-cooldown: 3        # cooldown strzału w sekundach
pearl-velocity: 2.0      # prędkość perły
consume-pearl: false     # czy strzał zużywa perłę z ekwipunku
bonus-ender-damage: 4.0  # bonusowe obrażenia dla Endermanów/Smoka
```

## Budowanie

Wymagane: Java 17+ i Maven.

```bash
mvn package
```

Gotowy plugin znajdziesz w `target/SmoczyMiecz-1.0.0.jar` — wrzuć go do
folderu `plugins/` serwera Paper/Spigot 1.20+.
