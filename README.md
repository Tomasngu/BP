# Systém pro optimální sledování živých streamů z výběhu slonů

## Pokyny k instalaci


1. **Instalace Anacondy:** Začněte instalací Anacondy, kterou najdete na [oficiálních stránkách](https://docs.anaconda.com/anaconda/install/).

2. **Vytvoření Conda prostředí a aktivace:**  Prostředí vytvoříte pomocí následujícího příkazu v terminálu:
   ```shell
   conda create -n env python=3.9
   conda activate env
   ```
3. **Stažení potřebných balíčků:**  Nakonec nainstalujte všechny potřebné Python balíčky uvedené v souboru requirements.txt do vašeho Conda prostředí:
    ```shell
   pip install -r requirements.txt
   ```
   

## Ukázkové notebooky

Tato práce obsahuje 3 spustitelné ukázkové notebooky demonstrující finální výtvory tohoto projektu.

| Název   | popis        |
|--------|---------------|
| 1. [showcase_heatmaps](showcase_heatmaps.ipynb) | Ukázka tvorby heatmap z obrazového datasetu |
| 2. [showcase_recommend](showcase_recommend.ipynb) | Ukázka vytvořeného doporučovacího systému |
| 3. [showcase_scraping](showcase_scraping.ipynb) | Ukázka systému pro scrapování dat z živých streamů Údolí slonů|
