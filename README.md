<br />
<p align="center">
  <img src="img/icon_app.png" alt="Logo" width="64" height="64">

  <h1 align="center">Smol Ame Launcher</h1>

  <p align="center">
    <i>Keep all your Smol Ame versions in one easy to access place.</i>
  </p>
</p>


# About

When speedrunning the indie game [Smol Ame](https://moocow-games.itch.io/smol-ame) by KevinCow (MooCow Games), it is often optimal to use different versions of the game for different stages and categories. 
This can result in a bit of a mess when runners have to juggle multiple copies of the game and it takes up a needless amount of disk space. 
The Smol Ame Laucher is made to help organize the various game versions in a simple and efficient way.
Sort the game versions into custom defined categories and launch the version you wish to play through the launcher.

<p align="center">
    <img src="img/launcher.png" 
      alt="interface">
</p>
<p align="center">
  <i>The Smol Ame Launcher interface.</i>
</p>
<br />


# Features

* Store and sort Smol Ame game versions.

* Launch your desired game version and play some Smol Ame.

* Launch TAS and training tools alongside the game.

* Track your playtime in individual versions as well as across all versions.

* Customize the colors of the the interface by editing HEX codes in  the "settings.json" file.


# How to Use

<!-- **If you would rather watch a video guide then go [here](https://www.youtube.com/watch?v=tgFAWxCUGZY).** Note that this is slightly outdated by now but the workflow remains mostly the same. -->

1. Download the most recent version from the [releases page](../../releases). Download the .zip file and extract it in your desired location. Navigate into the extracted folder and run SmolAmeLauncher.exe.

2. The Launcher comes with two version categories preinstalled. To add new custom versions click the "Add category" button and type in the name of your new category.

<p align="center">
    <img src="img/seg1.gif" 
      alt="main folder">
</p>

3. To add a game version to the Launcher, first select a category from the drop-down menu and then click the "Import files to selected category" button. A file navigation window should pop up in which you can navigate to and select the .zip archive of the desired Smol Ame game version. On where to find and download various Smol Ame game versions, see [here](#download-game-versions)

<p align="center">
    <img src="img/seg2.gif" 
      alt="main folder">
</p>

4. To remove a game version from the Launcher, select the category which the version belongs to and click the "Remove files from selected category" button. Select all the game versions you wish to delete and press Confirm.

<p align="center">
    <img src="img/seg3.gif" 
      alt="main folder">
</p>

5. To remove a category and all the game versions associated with it click the "Remove categories" button. Select all the categories you wish to delete and press Confirm.

<p align="center">
    <img src="img/seg4.gif" 
      alt="main folder">
</p>

6. We are now ready to play some Smol Ame! Select the desired game version from the list on the left side of the Launcher and hit the Play button.

7. To launch the game together with the YetAnotherTAS tool by DemoJameson, tick the box that says TAS below the list of game versions before pressing Play. Be aware that the TAS tool will not work with all versions of Smol Ame.

<!-- <p align="center">
    <img src="img/SAL_folder.png" 
      alt="main folder">
</p>

2. Before running the launcher we need to set up categories and install the desired versions of Smol Ame. To do this, first navigate into the "versions" folder (highlighted in the image above).

3. The versions directory is where the different version categories are sorted. The launcher comes with the categories "Modded" and "Vanilla" pre-installed (as seen in the image below). To create a new category, simply create a new folder in the versions directory. To remove categories, simply delete the associated folder.

<p align="center">
    <img src="img/versions_folder.png" 
      alt="versions folder">
</p>

4. To install any Smol Ame version into the launcher, copy the .zip archive of the desired game version into any of the category directories (see how to download game versions [here](#download-game-versions)). In the example image below, we have installed versions 1.0 and 210418.1 in the Vanilla category.

<p align="center">
    <img src="img/folder_structure.png" 
      alt="folder structure">
</p>

5. We are now ready to play some Smol Ame! Return to the main directory and run SmolAmeLauncher.exe. Choose the category from the dropdown menu on the top left corner, select the game version from the list underneath and hit Play in the bottom right. If any game versions or categories do not appear in the launcher, try clicking the Refresh button in the bottom left. -->

If any game versions of categories don't update correctly, try clicking the "Refresh" button in the bottom left.

In step 3 above, it is essential that the game folder is compressed into a .zip format and that the game's .exe file is located directly inside the .zip folder. Other compression formats or folder structures will not work. Fortunately, most game versions are available in this format by default in the download sources listed below.

The Smol Ame Launcher is currently only available for Windows. However, both Smol Ame and the Launcher run well using Wine or Proton.


# Download Game Versions

The latest official version of Smol Ame is always available on [itch.io](https://moocow-games.itch.io/smol-ame).
For a repository of all published versions (official, testing, and speedrun patch versions), see the resources tab at [speedrun.com/smol_ame](https://www.speedrun.com/smol_ame/resources).
Modded versions used for speedrunning can be found under the resources tab at [speedrun.com/Smol_Ame_Mods](https://www.speedrun.com/Smol_Ame_Mods/resources).
Alternatively, join the Smol Ame Speedrunning community Discord server [here](https://discord.gg/WpZydmdUGP) to browse the game-versions and modded-game-versions channels.


# Credits

- [KevinCow](https://bsky.app/profile/kevincow.bsky.social): Developer of the Smol Ame game.
- [DemoJameson](https://github.com/DemoJameson): Developer of the [SmolAme.YetAnotherTAS](https://github.com/DemoJameson/SmolAme.YetAnotherTAS) tool.
