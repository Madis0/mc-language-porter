# Eesti keele pakk Minecraftile
See pakk muudab Minecrafti eestikeelseks, kasutades juba olemasolevaid tõlkeid Minecrafti platvormilt Java Edition.

## Kuidas paigaldada?
#### Windows, Mac, Linux (Java Edition)
1. Vajuta avamenüüs ![gloobusega jutumullile](https://i.imgur.com/fzYkvEw.png)
2. Vali **Eesti keel (Eesti)**
3. Vajuta **Done**

#### Android, iOS, Windows 10/11 (Bedrock Edition)
1. [Laadi pakk alla siit](https://www.curseforge.com/minecraft-bedrock/addons/estonian-language-pack/files), vajutades kõige ülemisele `Download` nupule
2. Vajuta allalaaditud `.mcpack` failile (nt telefonis tekib teade)
3. Mine **Settings** > **Global Resources** > **My Packs** > **vajuta paki juures Activate**
4. Välju seadetest, oota kuni pakk laeb
5. Vali **Settings** > **Language** > **Eesti keel (Eesti)**

##### Uuendamiseks:

1. Laadi pakk uuesti alla
2. Vajuta allalaaditud `.mcpack` failile
3. Mine **Seaded** > **Mäluruum** > **Ressursipakid** > **Eesti keele pakk** (vali vanem versioon) > **vajuta prügikastile** > **Kustuta**
4. Mine seadetest välja, keel laaditakse uuesti

#### Oculus Rift (Bedrock Edition)

[Kasuta paki tööle saamiseks ametlikku õpetust](https://learn-microsoft-com.translate.goog/en-us/minecraft/creator/documents/gettingstarted?view=minecraft-bedrock-stable&tabs=oculusrift&_x_tr_sl=auto&_x_tr_tl=et&_x_tr_hl=et&_x_tr_pto=wapp#installing-add-on-instructions) [(inglise keeles)](https://learn.microsoft.com/en-us/minecraft/creator/documents/gettingstarted?view=minecraft-bedrock-stable&tabs=oculusrift#installing-add-on-instructions), seejärel vaata keele aktiveerimiseks eelmist õpetust.

#### Konsoolid (Bedrock Edition)

Konsoolides pole kohandatud ressursipakid ametlikult toetatud ning ka teatud keelefraasid on erinevad, seega kõik ei pruugi toimida nagu oodatud. 

Siiski võib proovida järgnevaid õppevideoid: [Xbox One](https://www.youtube.com/watch?v=MFKO1HdwTlE&t=123), [Nintendo Switch](https://www.youtube.com/watch?v=qNwvtSXQH2A), [PlayStation 4](https://www.youtube.com/watch?v=Y08IUPJM1Tw). Keele aktiveerimiseks vaata ülemist õpetust.

## Mis on tõlgitud?

Antud pakk tõlgib hetkel järgnevat:

* Plokid, esemed, elukad
* Loomingurežiimi seljakott
* Olulisemad menüüd
* Olulisemad seaded
* Vestlus ja mõned süsteemisõnumid

Paki versiooni 1.21.1 seisuga tõlgib see pakk mängu 39.1% ulatuses. Java Editionis on eesti keel ametlikult toetatud, seega seal on mäng 100% tõlgitud 🙂

## Kuidas tõlge on toetatud?

Plaanin uuendada ressursipakki iga kord, kui Bedrock Editioni tuleb uus beeta, mille väljendeid saab viia vastavusse Java Editioni omadega.
Parima tõlke saamiseks kasuta alati uusimat mängu ja pakki, mina toetan vaid neid.

Uusimat pakki igale versioonile saab mugavalt alla laadida [Curseforgest](https://www.curseforge.com/minecraft-bedrock/addons/estonian-language-pack/filess), uuemad versioonid leiab [GitHubist](https://github.com/Madis0/mc-language-porter/releases).

## Kuidas saan kaasa aidata?

Kõige paremini saad tõlkele kaasa aidata [Java Editioni kogukonnatõlke platvormil](https://crowdin.com/project/minecraft). 
Seal saad tõlgetele hääli anda ja uusi juurde pakkuda.

Kui aga on konkreetne soov Bedrocki tõlget täiendada, siis tee siia pull request failile [extra-et_EE.lang](/extra-et_EE.lang) [(originaalväljendid saad siit)](https://raw.githubusercontent.com/Mojang/bedrock-samples/preview/resource_pack/texts/en_US.lang).

## Kuidas on see seotud äpiga "Tõlked Minecraftile"?

Esialgu püüdsingi ma seda äppi tõlgetega toetada, siis aga leidsin, et see uueneb veidi liiga aeglaselt ning tõlkeid portiv skript on suletud lähtekoodiga (s.t. keegi peale omaniku ei saa seda kasutada). See inspireeris mind sõbra abiga looma oma skripti ning pakki. 

Eraldiseisev skript võimaldab muuhulgas:

* tõlkeid kiiremini uuendada
* võtta rohkem tõlkeid automaatselt üle
* hoida paki mahtu minimaalsena (ainult eesti keel) 
