# Unit 10: Deep Learning in Action

## Appraising deployed technologies

| | Text-to-image generation (e.g. Stable Diffusion) | Facial recognition and analysis |
| --- | --- | --- |
| What it does | Generates images from prompts with latent diffusion (Rombach et al., 2022) | Detects, classifies or identifies faces with deep networks |
| Data | Billions of web image-text pairs such as LAION-5B (Schuhmann et al., 2022), largely without creators' consent | Large face datasets, historically skewed towards lighter-skinned men |
| Benefits | Cheaper illustration and design | Phone unlocking, border checks |
| Harms | Copyright disputes, including Getty Images' 2023 action against Stability AI; deepfakes; stereotyped outputs | Surveillance and misidentification; error rates up to 34.7% for darker-skinned women against 0.8% for lighter-skinned men (Buolamwini and Gebru, 2018) |
| Regulation | Copyright law, under active litigation | The EU AI Act bans untargeted scraping of facial images and restricts real-time remote biometric identification |

In both, the model mirrors its data. Practitioners undervalue data work, which causes compounding failures downstream (Sambasivan et al., 2021).

## Artefact: how imbalanced data hides harm

| Share of group B in training | Overall error | Error on group A | Error on group B |
| --- | --- | --- | --- |
| 2% | 1.0% | 0.4% | 31.8% |
| 10% | 6.2% | 3.7% | 28.1% |
| 30% | 13.3% | 9.6% | 21.9% |
| 50% | 16.1% | 17.4% | 14.8% |

At 2%, the model looks excellent overall while failing nearly a third of group B; only disaggregated evaluation reveals it. Balancing the data evens the errors but raises overall error, because one simple model cannot fit both groups: fairness needed a better model, not just more balanced data.

{{code:unit10/data_imbalance.py}}

::: todo
Add your own notes on this unit: what you found difficult or surprising, how it felt, and what happened in your team that week.
:::
