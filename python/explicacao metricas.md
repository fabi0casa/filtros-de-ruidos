
### 🔊 **SNR (dB) — Signal-to-Noise Ratio (Relação Sinal-Ruído)**

* **O que é:** Mede a relação entre o **sinal útil** (áudio original) e o **ruído** (diferença entre o original e o filtrado).
* **Unidade:** decibéis (dB).
* **Como interpretar:**

  * **Maior SNR = melhor qualidade**: o áudio filtrado manteve mais do sinal original e tem menos ruído.
  * Exemplo:

    * `SNR = 25 dB` → sinal útil muito mais forte que o ruído.
    * `SNR = 5 dB` → o ruído está quase tão forte quanto o sinal útil.

---

### 🔁 **SDR (dB) — Signal-to-Distortion Ratio**

* **O que é:** Mede o quanto **distorcido** está o áudio filtrado comparado ao original.
* **Diferença em relação ao SNR:**

  * Enquanto o **SNR foca em ruído**, o **SDR considera todas as alterações** no sinal, inclusive distorções e artefatos da filtragem.
* **Unidade:** decibéis (dB).
* **Como interpretar:**

  * **Maior SDR = menos distorção.**
  * `SDR = 20 dB` → sinal filtrado está bem parecido com o original.
  * `SDR = 2 dB` → sinal bastante distorcido.

---

### 📈 **Nível Médio (Base) \[dBFS]**

### 📉 **Nível Médio (Filtrado) \[dBFS]**

* **O que é:** Uma estimativa de **quão alto está o som** do ponto de vista de amplitude RMS.

* **Unidade:** dBFS (decibéis em relação à escala de valor máximo, usada em áudio digital).

* **Valores típicos:**

  * 0 dBFS = volume máximo digital (clipping)
  * -6 a -12 dBFS = bom nível de voz
  * -20 dBFS ou menos = som bem baixo

* **Como interpretar:**

  * Compare o nível médio **antes e depois da filtragem**.
  * Se o nível do filtrado for muito menor, talvez tenha removido partes demais do sinal.
  * Exemplo:

    * Base: `-12 dBFS`, Filtrado: `-18 dBFS` → houve uma redução considerável.
    * Pode indicar que o áudio foi atenuado (redução de volume global), o que **não é ruim** se significar menos ruído.

---

### 📌 **Resumo de como usar no artigo**

| Métrica            | Alta é boa? | Indica o quê?                               |
| ------------------ | ----------- | ------------------------------------------- |
| **SNR**            | Sim         | Sinal útil mais forte que ruído             |
| **SDR**            | Sim         | Sinal com menos distorção                   |
| **Nível Base**     | —           | Volume médio do original                    |
| **Nível Filtrado** | —           | Volume médio do filtrado (com ou sem ruído) |

---

