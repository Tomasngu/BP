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
| 1. [showcase_scraping](showcase_scraping.ipynb) | Ukázka systému pro scrapování dat z živých streamů Údolí slonů|
| 2. [showcase_heatmaps](showcase_heatmaps.ipynb) | Ukázka tvorby heatmap z obrazového datasetu |
| 3. [showcase_recommend](showcase_recommend.ipynb) | Ukázka vytvořeného doporučovacího systému |

Ve složce [model_dt](model_dt) se nachází 3 notebooky obsahující statistickou analýzu dat a trénování výsledného predikčního modelu.

## Moduly

Práce obsahuje 4 Python moduly, které obsahují mnoho pomocných funkcí.

| Název modulu   | popis        |
|--------|---------------|
| 1. [detector](detector/) | Modul se třídou `ElephantDetector`, která zastřešuje detekci slonů.|
| 2. [preprocess_functions](preprocess_functions/) | Pomocné funkce pro zpracování surových obrazových dat. |
| 3. [yolo_preprocess](yolo_preprocess/) | Předzpracování obrazových dat slonů s anotacemi pro YOLOV8 model.|
| 4. [visualize](visualize/) | Pomocné funkce a soubory potřebné k vytváření heatmap. |

## Trénování modelu detekce slonů
Ve složce [train_detector](train_detector) se nachází trénovácí skript, konfigurační soubory a data využita k trénování modelu detekce slonů.



