# Projeto de Avaliação de Algoritmos de Filtragem de Áudio em Plataformas de Comunicação

<div style="width: 100%; text-align: center;">
  <img src="https://github.com/user-attachments/assets/f87cf194-4724-4699-bac5-dc759c063e65"
       alt="mp3-logo"
       height="60">
</div>

Este repositório contém os materiais, áudios de teste utilizados no projeto de pesquisa para avaliação da eficácia dos algoritmos de filtragem de áudio utilizados por diferentes plataformas de comunicação por voz.

## Objetivo

Avaliar e comparar a eficácia dos algoritmos de supressão de ruído utilizados nas principais plataformas de chamadas de áudio e vídeo:

* WhatsApp
* Telegram
* Microsoft Teams
* Zoom
* Discord (modo padrão)
* Discord com filtro **Krisp** ativado

## 📉 Metodologia

Para a avaliação, foram construídos áudios de teste compostos por uma gravação de voz clara sobreposta a diferentes ruídos de fundo:

* Bebê chorando
* Conversas ao fundo
* Ruído de trânsito
* Cachorro latindo
* Construções, obras

Cada áudio foi transmitido por meio das plataformas supracitadas, utilizando seus mecanismos de chamada, e em seguida capturado para análise comparativa.

## 🔧 Estrutura do Repositório

```
.
├── Audios originais/            # Áudios originais, da voz e dos ruídos separados
├── filtrados/                   # Áudios gravados após passar por cada plataforma
    ├── discord
    ├── discord - krisp
    ├── Filtro desativado        # áudios que foram passados pelas plataformas porém com a filtragem desligada
    ├── teams
    ├── telegram
    ├── whatsapp
    └── zoom

└── romulo + ruído/              # áudios montados para simularmos um abiente com ruído
```

## 🔍 Métricas Avaliadas

* Não sei

## 📄 Ferramentas Utilizadas

* Audacity para inspeção manual
* OBS Studio para captura de áudio das chamadas

## ✍️ Autores

* Edilson Piattão
* Fábio Casagrande
* João Bravo
* Milton Tomomi Ozeki

## 🔧 Como Contribuir

Contribuições são bem-vindas! Se você deseja propor melhorias na análise, adicionar mais plataformas ou novos ruídos de teste, fique à vontade para abrir uma *issue* ou *pull request*.

