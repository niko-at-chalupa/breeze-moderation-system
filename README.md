<div align="center">
<img src="images/breeze.png" alt="breeze" width="300"/>

# breeze - chat management plugin for Endstone/Kherimoya
</div>

> [!NOTE]
> This is still being worked on!

> [!IMPORTANT]
> Breeze isn't very good right now. I'd recommend [Ky_AntiSpam](https://github.com/Kevin-SalazarG/Ky_AntiSpam/tree/master) instead.

## introduction
Breeze is a chat management system that provides things like **chat filtering** and **extension support** right out of the box, so you can do pretty much anything with it.

Breeze isn't very feature-rich out of the box *(for now)*, but you can make it feature rich using the extension API, which lets you modify and add on to Breeze.

The mean appeal of Breeze right now is its chat filtering.

Right now, Breeze is meant to work with Kherimoya. In the future **Breeze will be able to work 100% independantly**.

# setup
1. Download the latest .whl from [releases](https://github.com/niko-at-chalupa/kheremara-breeze/releases/tag/v1.0.0)

2. Copy the downloaded .whl into the plugins/ folder of your server

<br />

### *why is it a "chat management" system instead of a "chat filtering" system?*
Because features like tags *(like a prefix berfore one's name, e.g. `[tag] <name> hello`)*, stripping out formatting stuff from messages, and other chat management stuff can *(somewhat)* easily be implemented by the extension system AND are upcoming.